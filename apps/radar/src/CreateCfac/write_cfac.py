# Write the aft or fore cafc file

import os.path

# extension is either 'aft' or 'fore'

def write_cfac(directory, extension, range_delay_corr,
    pressure_alt_corr, ew_gndspd_corr, 
    pitch_corr_cfac, drift_corr_cfac,
    rot_angle_corr, tilt_corr):
    file_name = 'cfac.' + extension
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as f11:

        f11.write(f'{"azimuth_corr           ="}{0.0:8.3f}\n')

        f11.write(f'{"elevation_corr         ="}{0.0:8.3f}\n')

        f11.write(f'{"range_delay_corr       ="}{range_delay_corr:8.3f}\n')

        f11.write(f'{"longitude_corr         ="}{0.0:8.3f}\n')
        f11.write(f'{"latitude_corr          ="}{0.0:8.3f}\n')
        f11.write(f'{"pressure_alt_corr      ="}{pressure_alt_corr:8.3f}\n')
        f11.write(f'{"radar_alt_corr         ="}{0.0:8.3f}\n')
        f11.write(f'{"ew_gndspd_corr         ="}{ew_gndspd_corr:8.3f}\n')

        f11.write(f'{"ns_gndspd_corr         ="}{0.0:8.3f}\n')
        f11.write(f'{"vert_vel_corr          ="}{0.0:8.3f}\n')
        f11.write(f'{"heading_corr           ="}{0.0:8.3f}\n')
        f11.write(f'{"roll_corr              ="}{0.0:8.3f}\n')
        f11.write(f'{"pitch_corr             ="}{pitch_corr_cfac:8.3f}\n')
        f11.write(f'{"drift_corr             ="}{drift_corr_cfac:8.3f}\n')
        f11.write(f'{"rot_angle_corr         ="}{rot_angle_corr:8.3f}\n')
        f11.write(f'{"tilt_corr              ="}{tilt_corr:8.3f}\n')


