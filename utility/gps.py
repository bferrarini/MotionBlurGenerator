import gpmf
import gpxpy
import cv2
import datetime
import csv
import copy
import math
import os
from collections import OrderedDict
from utility import Unspooler
import folium
import pandas
from abc import ABC, abstractmethod


class GpsExtractor():

    def __init__(self, video_fn, frameId_offset = 0, fill_the_gaps = False) -> None:
        self.fn = video_fn
        video = cv2.VideoCapture(video_fn)
        self.fps = video.get(cv2.CAP_PROP_FPS)
        self.fT = 1 / self.fps * 1000 * 1000 #microseconds

        #self.points = OrderedDict()
        self.points = list()

        stream = gpmf.io.extract_gpmf_stream(video_fn)
        gps_blocks = gpmf.gps.extract_gps_blocks(stream)
        self.gps_data = list(map(gpmf.gps.parse_gps_block, gps_blocks))
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(gpmf.gps.make_pgx_segment(self.gps_data))
        seg = 0
        t0 = None
        idx = 0
        for segment in gpx_track.segments:
            #seq_idx = 0
            #self.points[f"S{seg}"] = OrderedDict()
            for point in segment.points:
                if t0 is None:
                    t0 = point.time
                pt = OrderedDict()
                # The offset is used when a video is fractioned into multiple files
                frameId = self._getFrameId(point, t0) + frameId_offset
                pt['idx'] = str(idx)
                pt['seq'] = f"S{seg}"
                # this point is a 'real mesument' and than flagged to '0'
                pt['true_gps'] = "1"
                pt['frameId'] = str(frameId)
                # pt['bond_frame_id'] = str(frameId)
                pt['label'] = Unspooler.BuildLabel(frameId)
                pt['latitude'] = point.latitude
                pt['longitude'] = point.longitude
                pt['elevation'] = point.elevation
                pt['speed'] = point.speed
                pt['pos_diluition'] = point.position_dilution
                pt['datetime'] = point.time
                pt['yy'] = point.time.year
                pt['MM'] = point.time.month
                pt['dd'] = point.time.day
                pt['hh'] = point.time.hour
                pt['mm'] = point.time.minute
                pt['ss'] = point.time.second
                pt['us'] = point.time.microsecond

                #self.points[f"S{seg}"][idx] = pt
                #self.points[idx] = pt
                self.points.append(pt)
                idx += 1
            seg += 1

        self.points.sort(key=lambda x: int(x['frameId']), reverse=False)
        idx = 0
        for pt in self.points:
            pt['idx'] = idx
            idx += 1

        if fill_the_gaps:            
            self._fill_the_gaps()

    def _fill_the_gaps(self):
        new_pts = list()
        idx = 0
        new_frameId = None
        for point in self.points:
            if int(point['frameId']) > 510 and int(point['frameId']) < 600:
                #print(point['frameId'])
                pass
            if new_frameId is None:
                new_frameId = int(point['frameId'])
            if new_frameId < int(point['frameId']):
                for i in range(new_frameId, int(point['frameId'])):
                    pt = copy.copy(pt)
                    pt['idx'] = str(idx)
                    pt['frameId'] = str(i)
                    pt['label'] = Unspooler.BuildLabel(i)
                    # Update 'syntetically' the timestamp
                    dt = pt['datetime']
                    dt += datetime.timedelta(microseconds = math.floor(self.fT))
                    pt['datetime'] = dt
                    pt['us'] = dt.microsecond
                    pt['ss'] = dt.second
                    # this point is 'syntetic' and than flagged to '0'
                    pt['true_gps'] = "0"
                    new_pts.append(pt)
                    idx += 1
                    new_frameId += 1

            pt = copy.copy(point)
            pt['idx'] = str(idx)
            new_pts.append(pt)
            idx += 1
            new_frameId += 1

        self.points = new_pts


    def writeToCSV(self, outfile):
        first_point = self.points[0]
        header = list(first_point.keys())
        with open(outfile, 'w', newline='') as csvfile: 
            writer = csv.DictWriter(csvfile, fieldnames = header) 
            writer.writeheader() 
            writer.writerows(self.points) 

    def toConsole(self):
        first_point = self.points[0]
        header = list(first_point.keys())
        row = ",".join(header)
        print(row)
        for item in self.points:
            data = list(item.values())
            data = list(map(str,data))
            row = ",".join(data)
            print(row)

    def points_as_list(self):
        points = [(pt['latitude'], pt['longitude']) for pt in self.points]
        return points

    def visualize_on_map(self, out_fn):
        map_center = self.points[0]
        map_osm = folium.Map(location=(map_center['latitude'], map_center['longitude']), zoom_start=15)
        start = (self.points[0]['latitude'], self.points[0]['longitude'])
        end = (self.points[-1]['latitude'], self.points[-1]['longitude'])
        for point in self.points:
            color = "red" if point["true_gps"] == "1" else "blue"
            folium.Circle((point['latitude'], point['longitude']), radius=1, color = color).add_to(map_osm)
            #folium.Marker((point['latitude'], point['longitude'])).add_to(map_osm)
        map_osm.save(out_fn)        

        
    def _getFrameId(self, point, t0):
        tot_us = (point.time - t0).total_seconds() * 1000.0 * 1000.0
        frame_id = tot_us // self.fT
        return int(frame_id)
  

class Visualizer():

    def __init__(self):
        self.colors = [
                'red',
                'blue',
                'green',
                'gray',
                'darkred',
                'lightred',
                'orange',
                'beige',
                'darkgreen',
                'lightgreen',
                'darkblue',
                'lightblue',
                'purple',
                'darkpurple',
                'pink',
                'cadetblue',
                'lightgray',
                'black'
        ]

        self.extractors = OrderedDict()

    def append(self, label : str, gpsExtractor : GpsExtractor):
        self.extractors[label] = gpsExtractor

    def draw_map(self, to_file):
        m = None
        i = 0
        for name, ex in self.extractors.items():
            color = self.colors[i]
            points = ex.points_as_list()
            start = points[0]
            end = points[-1]
            if m is None:
                map_center = points[0]
                m = folium.Map(location=(start[0], start[1]), zoom_start=15)
            folium.Marker((start[0], start[1]), color = color, tooltip=f"{name}:Start").add_to(m)
            folium.Marker((end[0], end[1]), color = color, tooltip=f"{name}:End").add_to(m)
            for j in range(1,len(points) - 1):
                folium.Circle((points[j][0], points[j][1]), radius=1, color = color).add_to(m)
            i += 1
        m.save(to_file)  
        


class Wrapper():

    def __init__(self, fn : str) -> None:
        self.data = {}
        self.fn = fn
        self._load_data()        

    def __getitem__(self,index):
        c = self.data[index]
        return c
    
    def items(self):
        return self.data.items()
    
    def keys(self):
        return self.data.keys()
    
    @staticmethod
    def _load_data(self):
        pass

class GPSWrapper(Wrapper):
    
    def __init__(self, fn : str):
        super().__init__(fn)

    def _load_data(self):
        with open(self.fn, 'r') as f:
            headers = f.readline().rstrip().split(",")

        isHeader = True
        with open(self.fn, 'r') as csvfile: 
            reader = csv.DictReader(csvfile, fieldnames = headers) 
            for line in reader:
                if not isHeader:
                    coords = (float(line['latitude']), float(line['longitude']))
                    self.data[line['label']] = coords
                else:
                    isHeader = False

class PerfWrapper(Wrapper):

    def __init__(self, fn : str, metric = "EP"):
        self.metric = metric
        super().__init__(fn)

    def _load_data(self):
        with open(self.fn, 'r') as f:
            headers = f.readline().rstrip().split(";")

        isHeader = True
        with open(self.fn, 'r') as csvfile: 
            csv.register_dialect('dialect1', delimiter=';', quoting=csv.QUOTE_NONE)
            reader = csv.DictReader(csvfile, fieldnames = headers, dialect = 'dialect1')   
            for line in reader:
                if not isHeader:
                    self._add_to_dict(line)
                    #self.data[line['Q.LABEL']] = float(line[self.metric])
                else:
                    isHeader = False

    def _add_to_dict(self, line):
        vpr = line['VPR']
        ds = line['DATASET']
        T = str(float(line['TOLERANCE']))
        L = line['Q.LABEL']
        if not vpr in self.data:
            self.data[vpr] = OrderedDict()       
        if not ds in self.data[vpr]:
            self.data[vpr][ds] = OrderedDict()
        if not T in self.data[vpr][ds]:
            self.data[vpr][ds][T] = OrderedDict()
        if not L in self.data[vpr][ds][T]:
            self.data[vpr][ds][T][L] = OrderedDict()        
        self.data[vpr][ds][T][L] = float(line[self.metric])

    def filter(self, vpr, dataset, tolerance):
        d = self.data[vpr][dataset][tolerance]
        return d

class PerformanceVisualizer(Visualizer):
    
    def __init__(self, gps : GPSWrapper, perf : PerfWrapper, vpr, dataset, tolerance = "10.0"):
        self.gps = gps
        self.perf = perf.filter(vpr=vpr, dataset=dataset, tolerance=tolerance)

    def draw_map(self, to_file):
        m = None
        i = 0
        qLabels = list(self.perf.keys())
        start = self.gps[qLabels[0]]
        end = self.gps[qLabels[-1]]
        vstart = self.perf[qLabels[0]]
        vend = self.perf[qLabels[-1]]
        m = folium.Map(location=(start[0], start[1]), zoom_start=15)
        folium.Marker((start[0], start[1]), color = self._color(vstart), tooltip=f"Start").add_to(m)
        folium.Marker((end[0], end[1]), color = self._color(vend), tooltip=f"End").add_to(m)
        for j in range(1,len(qLabels) - 1):
            point = self.gps[qLabels[j]]
            value = self.perf[qLabels[j]]
            folium.CircleMarker((point[0], point[1]), radius=4, color = self._color(value), fill = True, fill_color = self._color(value), fill_opacity=0.7).add_to(m)
        i += 1
        m.save(to_file)

    def _color(self, measurment):
        if measurment < 0.5:
            return "red"
        if measurment < 0.75:
            return "orange"
        return "green"

                