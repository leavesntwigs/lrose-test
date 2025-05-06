import xarray as xr
import numpy as np

def read_eldora_data_file(path, nranges):

    counter = 0
    nsweep = 0
    NTIMES = 0
    NRANGES = 0
           
    start_year = 0
    start_mon = 0
    start_day = 0
           
    start_hour = 0
    start_min = 0
    start_sec = 0
    time = 0
           
    azimuth = 0
    elevation = 0
    latitude = 0
    longitude = 0
    altitude = 0
    
    altitude_agl = 0
    heading = 0
    roll = 0
    pitch = 0
    drift = 0
           
    rotation = 0
    tilt = 0
    ew_velocity = 0
           
    ns_velocity = 0
    vertical_velocity = 0
    ew_wind = 0
    ns_wind = 0
    vertical_wind = 0
    azimuth_correction = 0
    elevation_correction = 0
    range_correction = 0
    longitude_correction = 0
    latitude_correction = 0
    pressure_altitude_correction = 0
    radar_altitude_correction = 0
    ew_gound_speed_correction = 0
    ns_ground_speed_correction = 0
    vertical_velocity_correction = 0
    heading_correction = 0
    roll_correction = 0
    pitch_correction = 0
    drift_correction = 0
    rotation_correction = 0
    tilt_correction = 0



#    tree = xr.open_datatree("/Users/brenda/data/from_isaac/cfrad.19950516_221950.411_to_19950516_221953.219_\
#TA-ELDR_AIR.nc")
#
#    counter = 0
#    nsweep = tree.dims['sweep']
#    NTIMES = tree.dims['time']
#    NRANGES = tree.dims['range']
#    #date_time = datetime.datetime.
#    #start_year = tree.
## , start_mon, start_day, start_hour, start_min, start_sec,
#    meta_data = (counter, nsweep, NTIMES, NRANGES, 
#                start_year, start_mon, start_day, start_hour, start_min, start_sec,
#                )
#
#
    fmt = '{:10d}' + ' '*2 + ' '*50 + '{:10d}'*3 + '{:5d}' + '{:3d}'*5 + '{:20.8f}' + '{:10.4f}'*2 + '{:20.8f}'*3 + '{:10.4f}'*29
    with open(path, 'r') as f:

     #    meta_data = f.readline().strip().split()

        data = f.readline().strip().split()  
            # (fmt.format(
#            counter
#            ,nsweep,NTIMES,NRANGES
#            ,start_year,start_mon,start_day
#            ,start_hour,start_min,start_sec,time
#            ,azimuth,elevation,latitude,longitude,altitude
#            ,altitude_agl,heading,roll,pitch,drift
#            ,rotation,tilt,ew_velocity
#            ,ns_velocity,vertical_velocity,ew_wind,ns_wind
#            ,vertical_wind,azimuth_correction,elevation_correction
#            ,range_correction,longitude_correction,latitude_correction
#            ,pressure_altitude_correction,radar_altitude_correction
#            ,ew_gound_speed_correction,ns_ground_speed_correction
#            ,vertical_velocity_correction,heading_correction
#            ,roll_correction,pitch_correction,drift_correction
#            ,rotation_correction,tilt_correction
#        ))
            
    
        meta_data = (
            counter, nsweep, NTIMES, NRANGES, start_year, start_mon, start_day, start_hour, start_min, start_sec, time, azimuth, elevation, latitude, longitude, altitude, altitude_agl, heading, roll, pitch, drift, rotation, tilt, ew_velocity, ns_velocity, vertical_velocity, ew_wind, ns_wind, vertical_wind, azimuth_correction, elevation_correction, range_correction, longitude_correction, latitude_correction, pressure_altitude_correction, radar_altitude_correction, ew_ground_speed_correction, ns_ground_speed_correction, vertical_velocity_correction, heading_correction, roll_correction, pitch_correction, drift_correction, rotation_correction, tilt_correction
            ) = tuple(map(float, data))
    
        ranges = np.zeros(nranges)
        ZE = np.zeros(nranges)
        NCP = np.zeros(nranges)
        VR = np.zeros(nranges)
        SW = np.zeros(nranges)
     
          #   for J in range(nranges):
          #       data = f.readline().strip().split()
          #       ranges[J], ZE[J], NCP[J], VR[J], SW[J] = map(float, data)
    
        # return map(float, meta_data), ranges
    # , ranges, ZE, NCP, VR, SW

    return meta_data, ranges, ZE, NCP, VR, SW
