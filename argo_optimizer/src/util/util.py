from constants import *
from functools import partial
import math
import pyproj
from pyproj import Proj
import shapely
from shapely.geometry import shape
from shapely.geometry.polygon import Polygon
import shapely.ops as ops
import sys


class Util:
    
    def __init__(self):
        self.const = Constants()

    def get_time_delta(self, start, end):
        start_date = datetime.strptime(start, self.const.date_format)
        end_date = datetime.strptime(end, self.const.date_format)
        delta = end_date-start_date
        return delta.total_seconds()
    
    def get_time_delta(self, start, end):
        delta = end-start
        return delta    
    
    #Code from http://stackoverflow.com/questions/13148037/calculating-area-from-lat-lon-polygons-in-python
    def get_area(self, lat_min, lat_max, lon_min, lon_max):
        co = {"type": "Polygon", "coordinates": [
            [(lon_min, lat_max),
            (lon_min, lat_min),
            (lon_max, lat_min),
            (lon_max, lat_max)]]}   
            
        lon, lat = zip(*co['coordinates'][0])
        from pyproj import Proj
        pa = Proj("+proj=cea +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs")
        x, y = pa(lon, lat)
        cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
        from shapely.geometry import shape
        return shape(cop).area
    
    def get_area(self, box):
        lon_min = box[self.const.lon_min_tag]
        lon_max = box[self.const.lon_max_tag]
        lat_min = box[self.const.lat_min_tag]
        lat_max = box[self.const.lat_max_tag]
        co = {"type": "Polygon", "coordinates": [
            [(lon_min, lat_max),
            (lon_min, lat_min),
            (lon_max, lat_min),
            (lon_max, lat_max)]]}   
            
        lon, lat = zip(*co['coordinates'][0])
        from pyproj import Proj
        pa = Proj("+proj=cea +lon_0=0 +lat_ts=45 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs")
        x, y = pa(lon, lat)
        cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
        from shapely.geometry import shape
        return shape(cop).area    
    
    
    def convert_dates_to_string(self, task):
        
        if not (isinstance(task[self.const.time_tag][self.const.time_start_tag], str) or isinstance(task[self.const.time_tag][self.const.time_start_tag], unicode)):
            time_start  = task[self.const.time_tag][self.const.time_start_tag].strftime(self.const.date_format) 
            task[self.const.time_tag][self.const.time_start_tag] = time_start
        if not (isinstance(task[self.const.time_tag][self.const.time_end_tag], str) or isinstance(task[self.const.time_tag][self.const.time_end_tag], unicode)):
            time_end  = task[self.const.time_tag][self.const.time_end_tag].strftime(self.const.date_format)
            task[self.const.time_tag][self.const.time_end_tag] = time_end
                    
        if not (isinstance(task[self.const.subs_date_tag], str) or isinstance(task[self.const.subs_date_tag], unicode)):
            subs_date  = task[self.const.subs_date_tag].strftime(self.const.date_format)
            task[self.const.subs_date_tag] = subs_date
        if not (isinstance(task[self.const.end_subs_date_tag], str) or isinstance(task[self.const.end_subs_date_tag], unicode)):
            end_subs_date  = task[self.const.end_subs_date_tag].strftime(self.const.date_format)
            task[self.const.end_subs_date_tag] = end_subs_date       
        if not (isinstance(task[self.const.deadline_date_tag], str)or isinstance(task[self.const.deadline_date_tag], unicode)):
            deadline_date  = task[self.const.deadline_date_tag].strftime(self.const.date_format)
            task[self.const.deadline_date_tag] = deadline_date                   
        return task
    
    
    def uid_to_string(self, task):
        task['_id'] = str(task['_id'])
        return task
    
    def build_output(self, task, elapsed, execution_date, num_of_nodes, executing_node, num_of_tasks):
        out_data = {}
        area = self.get_area(task[self.const.bounding_box_tag])
        out_data['area'] = area


        if (isinstance(task[self.const.time_tag][self.const.time_start_tag], str)):
            start_date = datetime.strptime(task[self.const.time_tag][self.const.time_start_tag], self.const.date_format)
        else:
            start_date = task[self.const.time_tag][self.const.time_start_tag]
        if (isinstance(task[self.const.time_tag][self.const.time_end_tag], str)):
            end_date = datetime.strptime(task[self.const.time_tag][self.const.time_end_tag], self.const.date_format)
        else:
            end_date = task[self.const.time_tag][self.const.time_end_tag]

        out_data[self.const.time_tag] = self.get_time_delta(start_date, end_date).total_seconds()

        out_data[self.const.parameters_tag] = len(task[self.const.parameters_tag])
        out_data['dataset_size'] = get_size(input_folder_path)
        out_data['execution_time'] = elapsed #'%.3f' % elapsed.total_seconds()
        out_data['execution_date'] = execution_date.strftime(self.const.date_format)
        task = self.convert_dates_to_string(task)
        task = self.uid_to_string(task)
        out_data['configuration'] = json.dumps(task)
        out_data['num_of_nodes'] = num_of_nodes
        out_data['executing_node'] = executing_node
        out_data['num_of_tasks'] = num_of_tasks
        return json.dumps(out_data)    