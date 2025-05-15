
# I10
nranges = 5
# 2x
start_range = 200
ZE = 11
NCP = 21
VR = 31
SW = 41


counter = 0
nsweep = 1
NTIMES = 1
NRANGES = nranges
       
start_year = 1999 
start_mon = 1
start_day = 1
       
start_hour = 0
start_min = 1
start_sec = 1
time = 0
       
azimuth = 0
elevation = 0
latitude = 0
longitude = 0
altitude = 0

# 29f10.4       

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

# >>> fmt = '{:5d} '*5
# >>> fmt
# '{:5d} {:5d} {:5d} {:5d} {:5d} '
# >>> print(fmt.format(1,2,3,4,5))

#  101  format(I10,2x,50x,3I10,I5,5I3,d20.8,2f10.4,3d20.8,29f10.4)
fmt = '{:10d}' + ' '*2 + ' '*50 + '{:10d}'*3 + '{:5d}' + '{:3d}'*5 + '{:20.8f}' + '{:10.4f}'*2 + '{:20.8f}'*3 + '{:10.4f}'*29
#print(fmt)
print(fmt.format(
    counter
    ,nsweep,NTIMES,NRANGES
    ,start_year,start_mon,start_day
    ,start_hour,start_min,start_sec,time
    ,azimuth,elevation,latitude,longitude,altitude
    ,altitude_agl,heading,roll,pitch,drift
    ,rotation,tilt,ew_velocity
    ,ns_velocity,vertical_velocity,ew_wind,ns_wind
    ,vertical_wind,azimuth_correction,elevation_correction
    ,range_correction,longitude_correction,latitude_correction
    ,pressure_altitude_correction,radar_altitude_correction
    ,ew_gound_speed_correction,ns_ground_speed_correction
    ,vertical_velocity_correction,heading_correction
    ,roll_correction,pitch_correction,drift_correction
    ,rotation_correction,tilt_correction
))

#meta_data = [i for i in range(50)]
#meta_data_str = " ".join(str(x) for x in meta_data)
#print(meta_data_str)
for i in range(1):  # ranges, ZE, NCP, VR, SW
    # format(I10,2000f10.4)
    zero = 0.0
    message = " ".join([f"{zero:10.4f}" for k in range(nranges)])
    print(f'{start_range*i:10d}', message)
    #print(start_range*i, ZE+i, NCP+i, VR+i, SW+i)
for i in range(1):  # ranges, ZE, NCP, VR, SW
    # format(I10,2000f10.4)
    zero = 0.0
    message = " ".join([f"{ZE:10.4f}" for k in range(nranges)])
    print(f'{start_range*i:10d}', message)

for i in range(1):  # ranges, ZE, NCP, VR, SW
    # format(I10,2000f10.4)
    zero = 0.0
    message = " ".join([f"{NCP:10.4f}" for k in range(nranges)])
    print(f'{start_range*i:10d}', message)

for i in range(1):  # ranges, ZE, NCP, VR, SW
    # format(I10,2000f10.4)
    zero = 0.0
    message = " ".join([f"{VR:10.4f}" for k in range(nranges)])
    print(f'{start_range*i:10d}', message)

for i in range(1):  # ranges, ZE, NCP, VR, SW
    # format(I10,2000f10.4)
    zero = 0.0
    message = " ".join([f"{SW:10.4f}" for k in range(nranges)])
    print(f'{start_range*i:10d}', message)
