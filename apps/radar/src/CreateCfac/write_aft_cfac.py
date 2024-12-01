# Write the aft cafc file

         open(11,file=directory(1:ndir)//'/'//'cfac.aft'
             ,form='formatted',status='unknown')

              write(11,"('azimuth_corr           ='
                         ,f8.3)")0.0

              write(11,"('elevation_corr         ='
                         ,f8.3)")0.0

              write(11,"('range_delay_corr       ='
                         ,f8.3)")range_delay_corr_aft

              write(11,"('longitude_corr         ='
                         ,f8.3)")0.0
              write(11,"('latitude_corr          ='
                         ,f8.3)")0.0
              write(11,"('pressure_alt_corr      ='
                         ,f8.3)")pressure_alt_corr
              write(11,"('radar_alt_corr         ='
                         ,f8.3)")0.0
              write(11,"('ew_gndspd_corr         ='
                         ,f8.3)")ew_gndspd_corr

              write(11,"('ns_gndspd_corr         ='
                         ,f8.3)")0.0
              write(11,"('vert_vel_corr          ='
                         ,f8.3)")0.0
              write(11,"('heading_corr           ='
                         ,f8.3)")0.0
              write(11,"('roll_corr              ='
                         ,f8.3)")0.0
              write(11,"('pitch_corr             ='
                         ,f8.3)")pitch_corr_cfac
              write(11,"('drift_corr             ='
                         ,f8.3)")drift_corr_cfac
              write(11,"('rot_angle_corr         ='
                         ,f8.3)")rot_angle_corr_aft
              write(11,"('tilt_corr              ='
                         ,f8.3)")tilt_corr_aft

              close(11)

