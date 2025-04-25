import xarray as xr

def read_eldora_data_file(path, nranges):

    tree = xr.open_datatree("/Users/brenda/data/from_isaac/cfrad.19950516_221950.411_to_19950516_221953.219_\
TA-ELDR_AIR.nc")

    counter = 0
    nsweep = tree.dims['sweep']
    NTIMES = tree.dims['time']
    NRANGES = tree.dims['range']
    meta_data = (counter, nsweep, NTIMES, NRANGES, 
                )

    return meta_data, ranges, ZE, NCP, VR, SW

    # with open(path, 'r') as f:

     #    meta_data = f.readline().strip().split()
        

#         counter, nsweep, NTIMES, NRANGES, start_year, start_mon, start_day, start_hour, start_min, start_sec, time, azimuth, elevation, latitude, longitude, altitude, altitude_agl, heading, roll, pitch, drift, rotation, tilt, ew_velocity, ns_velocity, vertical_velocity, ew_wind, ns_wind, vertical_wind, azimuth_correction, elevation_correction, range_correction, longitude_correction, latitude_correction, pressure_altitude_correction, radar_altitude_correction, ew_ground_speed_correction, ns_ground_speed_correction, vertical_velocity_correction, heading_correction, roll_correction, pitch_correction, drift_correction, rotation_correction, tilt_correction = map(float, data)

      #   ranges = np.zeros(nranges)
      #   ZE = np.zeros(nranges)
      #   NCP = np.zeros(nranges)
      #   VR = np.zeros(nranges)
      #   SW = np.zeros(nranges)
 
      #   for J in range(nranges):
      #       data = f.readline().strip().split()
      #       ranges[J], ZE[J], NCP[J], VR[J], SW[J] = map(float, data)

    # return map(float, meta_data), ranges
# , ranges, ZE, NCP, VR, SW
