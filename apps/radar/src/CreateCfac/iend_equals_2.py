import numpy as np

import write_surf_el
import write_aft_cfac

# test 
# >>> inner = [1,2,3]
# >>> l = [inner, inner]
# >>> result = iend_equals_2.iend_equals_2(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, l, l, l)

def iend_equals_2(kdzsurf, kvsurf, kdvinsitu, swdzmsurf_tot, swdzsurf_tot, swdz2surf_tot, swvmsurf_tot, swvsurf_tot,
    swv2surf_tot, swdvminsitu_tot, swdvinsitu_tot, swv2insitu_tot, xv_vpv, x_vpv, xvv_vpv,
    iwrisurfile, wrisurfile_path,
    swdzsurf_wri, sw_or_altsurf_wri,
    nx_wrisurf,ny_wrisurf,nxysurfmax,
    ):

    #write(10,"(' NB_SWEEPS FOR THE AFT AND FORE RADARS: '
    #            ,2i5,/)")
    #            ,int(xsweeps(1)),int(xsweeps(2))
    #
    #******************************************************************
    #****  SUM OF INDIVIDUAL WEIGHTS, MEAN, RMS VALUES OF
    #****    - DIFFERENCE OF SURFACE ALTITUDE (RADAR-DTM);
    #****    - DOPPLER VELOCITY OF THE GROUND CLUTTER;
    #****    - DIFFERENCE OF DOPPLER VELOCITY (RADAR-FLIGHT_LEVEL);
    #******************************************************************
    #
    print(' ')
    print(' **********************************************')
    print(' ************ MEAN AND RMS ERRORS *************')
    print(' **********************************************')
    print(' ')
    
    # autoconverted begin
    
    if kdzsurf == 1:  # always 1
        bias_dzsurf = swdzmsurf_tot / max(1.0, swdzsurf_tot)
        stdv_dzsurf = np.sqrt(swdzsurf_tot * swdz2surf_tot - swdzmsurf_tot * swdzmsurf_tot) / max(1.0, swdzsurf_tot)
        print(' ')
        print(f' dZ_surf (km) sum_wghts,mean,stdv : {swdzsurf_tot:10.1f} {bias_dzsurf:8.3f} {stdv_dzsurf:8.3f}')
    
    if kvsurf == 1:  # always 1
        bias_vsurf = swvmsurf_tot / max(1.0, swvsurf_tot)
        stdv_vsurf = np.sqrt(swvsurf_tot * swv2surf_tot - swvmsurf_tot * swvmsurf_tot) / max(1.0, swvsurf_tot)
        print(' ')
        print(f' VDOP_surf (m/s) sum_wghts,mean,stdv : {swvsurf_tot:10.1f} {bias_vsurf:8.3f} {stdv_vsurf:8.3f}')
    
    if kdvinsitu == 1:  # always 1
        bias_dvinsitu = swdvminsitu_tot / max(1.0, swdvinsitu_tot)
        stdv_dvinsitu = np.sqrt(swdvinsitu_tot * swv2insitu_tot - swdvminsitu_tot * swdvminsitu_tot) / max(1.0, swdvinsitu_tot)
        print(' ')
        print(f' dVDOP_insitu (m/s) sum_wghts,mean,stdv : {swdvinsitu_tot:10.1f} {bias_dvinsitu:8.3f} {stdv_dvinsitu:8.3f}')
        
        for iradar in range(1, 3):
            print('   IRADAR (AR=1,AV=2) :', iradar)
            bias_dvinsitu_ir_g = xv_vpv[iradar-1][0] / max(1.0, x_vpv[iradar-1][0])
            stdv_dvinsitu_ir_g = np.sqrt(x_vpv[iradar-1][0] * xvv_vpv[iradar-1][0] - xv_vpv[iradar-1][0] * xv_vpv[iradar-1][0]) / max(1.0, x_vpv[iradar-1][0])
            # print('     -> VDOP-PROJWIND_LEFT_npts,mean,stdv:', x_vpv[iradar-1][0], bias_dvinsitu_ir_g, stdv_dvinsitu_ir_g)
            # print(f'   IRADAR (AR=1,AV=2) : {iradar}   
            print(f'     -> VDOP-PROJWIND_LEFT_npts,mean,stdv: {x_vpv[iradar-1][0]:10.1f} {bias_dvinsitu_ir_g:8.3f} {stdv_dvinsitu_ir_g:8.3f}')
            
            bias_dvinsitu_ir_d = xv_vpv[iradar-1][1] / max(1.0, x_vpv[iradar-1][1])
            stdv_dvinsitu_ir_d = np.sqrt(x_vpv[iradar-1][1] * xvv_vpv[iradar-1][1] - xv_vpv[iradar-1][1] * xv_vpv[iradar-1][1]) / max(1.0, x_vpv[iradar-1][1])
            print(f'     -> VDOP-PROJWIND_RIGHT_npts,mean,stdv: {x_vpv[iradar-1][1]:10.1f} {bias_dvinsitu_ir_d:8.3f} {stdv_dvinsitu_ir_d:8.3f}')
        
        print(' ')
        print()
    
    
    
    # autoconverted end
    
#    print(' ')
#    print(' **********************************************')
#    print(' ')
#    print(' ')
#    print(' ')
#    #
#    #******************************************************************
#    #****  (IF SUM_WGHTS_surf+insitu > SUM_WGHTS_min)
#    #****   -> NAVIGATIONAL ERROS CAN BE CALCULATED
#    #******************************************************************
#    #
#    if ssurfins > ssurfins_min:
#    #
#    #******************************************************************
#    #**** RMS VALUES OF THE NORMALIZED VARIABLES
#    #******************************************************************
#    #
#       print(' ')
#       print(' **********************************************')
#       print(' *** RMS VALUES OF THE NORMALIZED VARIABLES ***')
#       print(' **********************************************')
#       print(' ')
#    #
#                if swdzsurf_tot > 1.:
#                  print(' DZ_surf -> sWGHTs:',swdzsurf_tot
#                  print('          rms_VAR(dTaft,dTfore:')
#                         ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=1,2))
#                  print('          -------(dRaft,dRfore:'
#                         ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=3,4))
#                  print('          -------(dPitch,dHdg:'
#                         ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=5,6))
#                  print('          -------(RDaft,RDfore:'
#                         ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=7,8))
#                  print('          -------(dXwe,dYsn,dZacft:'
#                         ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=9,11))
#                  print('          -------(dVHacft:'
#                         ,sqrt(rms_var_zsurf(12)/swadzsurf_tot))
#                else:
#                  print(' !!!! DZ_surf -> sWGHTs:',swdzsurf_tot,' !!!!')
#                # endif
#    #
#                if swvsurf_tot > 1.:
#                  print(' VDOP_surf -> sWGHTs:',swvsurf_tot)
#                  print('          rms_VAR(dTaft,dTfore:'
#                         ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=1,2))
#                  print('          -------(dRaft,dRfore:'
#                         ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=3,4))
#                  print('          -------(dPitch,dHdg:'
#                         ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=5,6))
#                  print('          -------(RDaft,RDfore:'
#                         ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=7,8))
#                  print('          -------(dXwe,dYsn,dZacft:'
#                         ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=9,11))
#                  print('          -------(dVHacft:'
#                         ,sqrt(rms_var_vsurf(12)/swavsurf_tot))
#                else:
#                  print(' !!!! VDOP_surf -> sWGHTs:',swvsurf_tot,' !!!!')
#                # endif
#    #
#                if swdvinsitu_tot > 1.:
#                  print(' DVDOP_insitu -> sWGHTs:',swdvinsitu_tot)
#                  print('          rms_VAR(dTaft,dTfore:'
#                         ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=1,2))
#                  print('          -------(dRaft,dRfore:'
#                         ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=3,4))
#                  print('          -------(dPitch,dHdg:'
#                         ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=5,6))
#                  print('          -------(RDaft,RDfore:'
#                         ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=7,8))
#                  print('          -------(dXwe,dYsn,dZacft:'
#                         ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=9,11))
#                  print('          -------(dVHacft:'
#                         ,sqrt(rms_var_vinsitu(12)/swadvinsitu_tot))
#                else:
#                  print(' !!!! DVDOP_insitu -> sWGHTs:'
#                         ,swdvinsitu_tot,' !!!!')
#                # endif

#    # autoconverted begin
#    import numpy as np
#    
#    itest_xmat = 0
#    for i in range(1, nvar + 1:
#        vect[i - 1] = 0.0
#        if kdzsurf == 1 and swadzsurf_tot > 0:
#            vect[i - 1] += rw_dzsurf * vect_dzsurf[i - 1] / swadzsurf_tot
#        if kvsurf == 1 and swavsurf_tot > 0:
#            vect[i - 1] += rw_vsurf * vect_vsurf[i - 1] / swavsurf_tot
#        if kdvinsitu == 1 and swadvinsitu_tot > 0:
#            vect[i - 1] += rw_dvinsitu * vect_dvinsitu[i - 1] / swadvinsitu_tot
#        
#        for j in range(1, nvar + 1:
#            xmat[i - 1, j - 1] = 0.0
#            if kdzsurf == 1 and swadzsurf_tot > 0:
#                xmat[i - 1, j - 1] += rw_dzsurf * xmat_dzsurf[i - 1, j - 1] / swadzsurf_tot
#            if kvsurf == 1 and swavsurf_tot > 0:
#                xmat[i - 1, j - 1] += rw_vsurf * xmat_vsurf[i - 1, j - 1] / swavsurf_tot
#            if kdvinsitu == 1 and swadvinsitu_tot > 0:
#                xmat[i - 1, j - 1] += rw_dvinsitu * xmat_dvinsitu[i - 1, j - 1] / swadvinsitu_tot
#            if abs(xmat[i - 1, j - 1]) > 0:
#                itest_xmat = 1
#    
#        if abs(xmat[i - 1, i - 1]) <= 0:
#            for j in range(1, nvar + 1:
#                xmat[i - 1, j - 1] = 0.0
#                xmat[j - 1, i - 1] = 0.0
#            xmat[i - 1, i - 1] = 1.0
#            vect[i - 1] = 0.0
#    
#    
#    # autoconverted end 

#    #******************************************************************
#    #             Write the cfac files using SOLO format
#    #******************************************************************
#    
#    # Write the aft cafc file
#         write_aft_cfac.write_aft_cafc(
#                 directory,
#                 range_delay_corr_aft,
#                 pressure_alt_corr,
#                 ew_gndspd_corr,
#                 pitch_corr_cfac,
#                 drift_corr_cfac,
#                 rot_angle_corr_aft,
#                 tilt_corr_aft)
#    
#    # Write the fore cafc file
#              write_fore_cafc(directory, 
#                  range_delay_corr, 
#                  pressure_alt_corr, 
#                  ew_gndspd_corr,
#                  pitch_corr_cfac,
#                  drift_corr_cfac,
#                  rot_angle_corr_fore,
#                  tilt_corr_fore)
#    
#    # CAI ******  End of writing the cfac files  ******************
#    
#    
#    
#    #******************************************************************
#    #**** WRITES THE "SURF_EL*" FILE #30 (if IWRISURFILE=1)
#    #******************************************************************
#    #
        if iwrisurfile == 1:
            write_surf_el.write_surf_el(
                wrisurfile_path,
                swdzsurf_wri, sw_or_altsurf_wri,
                nx_wrisurf,ny_wrisurf,nxysurfmax,
                )
    
#    #******************************************************************
#    #**** END OF "SIS_EL_*" FILE #50
#    #******************************************************************
#    #
#              print(' ')
#              print(' END OF "SIS_EL_*" FILE #50 :'
#                    ,directory(1:ndir)//'/'//fich_sis)
#              f50.write(999,999
#                        ,-999.,-999.,-999.,-999.
#                        ,-999.,-999.,-999.
#                        ,-999.,-999.,-999.)
#              f50.write(-999)
#              f50.write(-999)
#              f50.write(-999)
#              close(50)
#    #
#    #******************************************************************
#    #**** END OF PROGRAM
#    #******************************************************************
#    #
#              print(' ')
#              print(' **************************')
#              print(' **** END OF PROGRAM  ****')
#              print(' **************************')
#    
#    	  print('N1,N2,N3,N4,N5,N6,N7,N8= ',nb1,nb2,nb3,nb4,nb5,nb6
#                                                 ,nb7,nb8)
#    	  print('NSUP=', nsup)
#    	  print('NTOTAL_OK= ',nbtotals)
#    	  print('NBON, NMAUVAIS= ',nbon,nmauvais)
#    #
#          go to 3 # stop
#    #
#    # endif    !!  of  !! if iend == 2:  !!
