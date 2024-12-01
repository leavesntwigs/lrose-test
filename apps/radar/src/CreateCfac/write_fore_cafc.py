# Write the fore cafc file

          open(12,file=directory(1:ndir)//'/'//'cfac.fore'
             ,form='formatted',status='unknown')

              write(12,"('azimuth_corr           ='
                         ,f8.3)")0.0

              write(12,"('elevation_corr         ='
                         ,f8.3)")0.0

              write(12,"('range_delay_corr       ='
                         ,f8.3)")range_delay_corr_fore

              write(12,"('longitude_corr         ='
                         ,f8.3)")0.0
              write(12,"('latitude_corr          ='
                         ,f8.3)")0.0
              write(12,"('pressure_alt_corr      ='
                         ,f8.3)")pressure_alt_corr
              write(12,"('radar_alt_corr         ='
                         ,f8.3)")0.0
              write(12,"('ew_gndspd_corr         ='
                         ,f8.3)")ew_gndspd_corr

              write(12,"('ns_gndspd_corr         ='
                         ,f8.3)")0.0
              write(12,"('vert_vel_corr          ='
                         ,f8.3)")0.0
              write(12,"('heading_corr           ='
                         ,f8.3)")0.0
              write(12,"('roll_corr              ='
                         ,f8.3)")0.0
              write(12,"('pitch_corr             ='
                         ,f8.3)")pitch_corr_cfac
              write(12,"('drift_corr             ='
                         ,f8.3)")drift_corr_cfac
              write(12,"('rot_angle_corr         ='
                         ,f8.3)")rot_angle_corr_fore
              write(12,"('tilt_corr              ='
                         ,f8.3)")tilt_corr_fore

              close(12)

