
def process_ray(meta_data, ranges):  # , ZE, NCP, VR, SW):
            (counter, nsweep, NTIMES, NRANGES, 
            start_year, start_mon, start_day, start_hour, start_min, start_sec, 
            time, azimuth, elevation, 
            latitude, longitude, altitude, altitude_agl, 
            heading, roll, pitch, drift, rotation, tilt, ew_velocity, ns_velocity, vertical_velocity, ew_wind, ns_wind, vertical_wind, 
            azimuth_correction, elevation_correction, range_correction, longitude_correction, latitude_correction, pressure_altitude_correction, radar_altitude_correction, ew_ground_speed_correction, ns_ground_speed_correction, vertical_velocity_correction, heading_correction, roll_correction, pitch_correction, drift_correction, rotation_correction, tilt_correction) = meta_data

#            # sanity check the ray data have the expected dimensions    
#            ranges = np.zeros(nranges)
#            ZE = np.zeros(nranges)
#            NCP = np.zeros(nranges)
#            VR = np.zeros(nranges)
#            SW = np.zeros(nranges)
#    
#            for J in range(nranges):
#                data = f.readline().strip().split()
#                ranges[J], ZE[J], NCP[J], VR[J], SW[J] = map(float, data)
#    
#    # process ray ...

     # ************ Get the ray time *************
            ih_rdl1 = start_hour
            im_rdl1 = start_min
            is_rdl1 = start_sec
            ims_rdl1 = (time-INT(time))*1000
    
    # add to the start seconds by time, which is the elpased time after start time
            is_rdl1 = is_rdl1+INT(time)
    # adjusting hh,mm,ss for passing 60 mark, assign to Frank's ray time variables
            ims_rdl = ims_rdl1
            is_rdl = MOD(is_rdl1,60)
            im_rdl1 = im_rdl1+is_rdl1/60
            im_rdl = MOD(im_rdl1, 60)
            ih_rdl1 = ih_rdl1+im_rdl1/60
            ih_rdl = MOD(ih_rdl1, 60)
    
    # Assign the aircraft position/angles to Frank's variables
            azest_rdl = azimuth
            elhor_rdl = elevation
            lat_av = latitude
            lon_av = longitude
            p_alt_av = altitude
            r_alt_av = altitude_agl
            cap_av = heading
            roul_av = roll
            tang_av = pitch
            derv_av = drift
            rota_rdl = rotation
            incl_rdl = tilt
            vwe_av = ew_velocity
            vsn_av = ns_velocity
            vnz_av = vertical_velocity
            vent_we = ew_wind
            vent_sn = ns_wind
            vent_nz = vertical_wind
    
    # Assign  the total number of gates and range of each gates,
    #  The aft/fore radar are different
            nb_portes = nranges
            if (tilt  <  0): # AFT,iradar_ray=1,iaftfore= -1
               # do ig = 1, nranges
               #    d_porte(ig) = range(ig)
               # enddo 
               # ig is a loop variable!  
               for ig in range(0, nranges):
                   d_porte[ig] = range[ig]
            elif tilt  >  0: # FORE,iradar_ray=2,iaftfore= +1
               # do ig = 1, nranges
               #    d_porte(MAXPORT+ig) = range(ig)  # This change fixed icorrupted infilename
               # enddo
               for ig in range(0, nranges):
                   d_porte[MAXPORT+ig] = range[ig]
            # endif
    # Assign the swp number read from text file to num_swp
            num_swp = nsweep
    
    # Assign the correction factors to Frank's variable
    # NOTE: Here the correction factors are arrays with two elements
    # This is different from any other variables
    
            if tilt  <  0:   # AFT, iradar_ray=1,iaftfore= -1
               corr_azest[0] = azimuth_correction
               corr_elhor[0] = elevation_correction
               corr_dist[0] = range_correction
               corr_lon[0] = longitude_correction
               corr_lat[0] = latitude_correction
               corr_p_alt[0] = pressure_altitude_correction
               corr_r_alt[0] = radar_altitude_correction
               corr_vwe_av[0] = ew_gound_speed_correction
               corr_vsn_av[0] = ns_ground_speed_correction
               corr_vnz_av[0] = vertical_velocity_correction
               corr_cap[0] = heading_correction
               corr_roul[0] = roll_correction
               corr_tang[0] = pitch_correction
               corr_derv[0] = drift_correction
               corr_rota[0] = rotation_correction
               corr_incl[0] = tilt_correction
            elif tilt  >  0:   # FORE, iradar_ray=2,iaftfore= +1
               corr_azest[1] = azimuth_correction
               corr_elhor[1] = elevation_correction
               corr_dist[1] = range_correction
               corr_lon[1] = longitude_correction
               corr_lat[1] = latitude_correction
               corr_p_alt[1] = pressure_altitude_correction
               corr_r_alt[1] = radar_altitude_correction
               corr_vwe_av[1] = ew_gound_speed_correction
               corr_vsn_av[1] = ns_ground_speed_correction
               corr_vnz_av[1] = vertical_velocity_correction
               corr_cap[1] = heading_correction
               corr_roul[1] = roll_correction
               corr_tang[1] = pitch_correction
               corr_derv[1] = drift_correction
               corr_rota[1] = rotation_correction
               corr_incl[1] = tilt_correction
            # endif
    #
    
    
    # TEST reading of text files
    #       print*,'File:',infilename,' Ray:', counter
    #           ,' HHMMSS:',ih_rdl,im_rdl,is_rdl,' EL:',elhor_rdl
    # TEST-END
    
            return
