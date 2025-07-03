import numpy as np
import print_rms_normalized_variables
import chol_inv
import variable_indexes

# writes to the CORNAV_EL_* file #10   fich_cornav= "('CORNAV_E_',a6,'_',a6)") c_hms_min(2:7),c_hms_max(2:7)
# send the values that need to be written to the #10 file
# from Fortran original code:  parameter (nvar=12,nxysurfmax=200), so nvar=12
# 
def calculate_navigational_errors(directory, fich_cornav,
    yymmdd, rw_dzsurf,rw_vsurf,rw_dvinsitu,
    idtmfile, iwrisurfile, 
    idtiltaft, idtiltfore, idrotaaft, idrotafore, idpitch, idhdg, irdaft, irdfore, idxwe, 
    idysn, idzacft, idvh, 
    swdzsurf_tot,
    nvar,
    vect_dzsurf,
    ):

    write_cornav_file()

    print_rms_normalized_variables.print_rms_normalized_variables()
 
    #            itest_xmat=0
    #            do i=1,nvar
    #               vect(i)=0.
    #               if kdzsurf == 1 and swadzsurf_tot > 0.)
    #                 vect(i)=vect(i)+rw_dzsurf*vect_dzsurf(i)
    #                                 /swadzsurf_tot
    #               if kvsurf == 1 and swavsurf_tot > 0.)
    #                 vect(i)=vect(i)+rw_vsurf*vect_vsurf(i)
    #                                 /swavsurf_tot
    #               if kdvinsitu == 1 and swadvinsitu_tot > 0.)
    #                 vect(i)=vect(i)+rw_dvinsitu*vect_dvinsitu(i)
    #                                 /swadvinsitu_tot
    #               do j=1,nvar
    #                  xmat(i,j)=0.
    #                  if kdzsurf == 1 and swadzsurf_tot > 0.)
    #                    xmat(i,j)=xmat(i,j)+rw_dzsurf*xmat_dzsurf(i,j)
    #                                        /swadzsurf_tot
    #                  if kvsurf == 1 and swavsurf_tot > 0.)
    #                    xmat(i,j)=xmat(i,j)+rw_vsurf*xmat_vsurf(i,j)
    #                                        /swavsurf_tot
    #                  if kdvinsitu == 1 and swadvinsitu_tot > 0.)
    #                    xmat(i,j)=xmat(i,j)+rw_dvinsitu*xmat_dvinsitu(i,j)
    #                                        /swadvinsitu_tot
    #                  if abs(xmat(i,j)) > 0.)itest_xmat=1
    #               enddo
    #
    #******************************************************************
    #**** CHECK THAT NO ELEMENT OF THE MATRIX' MAIN DIAGONAL IS NULL
    #******************************************************************
    #
    #               if abs(xmat(i,i)) <= 0.:
    #                 do j=1,nvar
    #                    xmat(i,j)=0.
    #                    xmat(j,i)=0.
    #                 enddo
    #                 xmat(i,i)=1.
    #                 vect(i)=0.
    #               endif
    #
    #            enddo
    
    # autoconverted begin
    itest_xmat = 0
    for i in range(nvar):
        vect[i] = 0.0
        if kdzsurf == 1 and swadzsurf_tot > 0:
            vect[i] += rw_dzsurf * vect_dzsurf[i] / swadzsurf_tot
        if kvsurf == 1 and swavsurf_tot > 0:
            vect[i] += rw_vsurf * vect_vsurf[i] / swavsurf_tot
        if kdvinsitu == 1 and swadvinsitu_tot > 0:
            vect[i] += rw_dvinsitu * vect_dvinsitu[i] / swadvinsitu_tot
        
        for j in range(nvar):
            xmat[i, j] = 0.0
            if kdzsurf == 1 and swadzsurf_tot > 0:
                xmat[i, j] += rw_dzsurf * xmat_dzsurf[i, j] / swadzsurf_tot
            if kvsurf == 1 and swavsurf_tot > 0:
                xmat[i, j] += rw_vsurf * xmat_vsurf[i, j] / swavsurf_tot
            if kdvinsitu == 1 and swadvinsitu_tot > 0:
                xmat[i, j] += rw_dvinsitu * xmat_dvinsitu[i, j] / swadvinsitu_tot
            if abs(xmat[i, j]) > 0:
                itest_xmat = 1
    
        if abs(xmat[i, i]) <= 0:
            for j in range(nvar):
                xmat[i, j] = 0.0
                xmat[j, i] = 0.0
            xmat[i, i] = 1.0
            vect[i] = 0.0
    
    
    # autoconverted end 
    
    print(' ')
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!      print(' '
    #!!!!      print(' NORMALIZED MATRIX AND VECTOR'
    #!!!!      do i=1,nvar
    #!!!!         print(' i:',i,' XMAT(i,1->nvar)',(xmat(i,j),j=1,nvar)
    #!!!!                ,' VECT(i:',vect(i)
    #!!!!      enddo
    #!!!!      print(' '
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #******************************************************************
    #**** INVERSION OF THE MATRIX
    #**** CALCULATION OF THE RESULTING VECTOR
    #******************************************************************
    #
    if itest_xmat == 1:
        # resoud(xmat,xinv,vect,res,nvar)
        ierr, res = chol_inv.chol_inv(xmat, vect, nvar)
    else:
        print(' !!!! XMAT=0 !!!!')
    # endif
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!      print(' '
    #!!!!      print(' RESULTING VECTOR'
    #!!!!      do i=1,nvar
    #!!!!         print(' RES(',i,':',res[i)
    #!!!!      enddo
    #!!!!      print(' '
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #******************************************************************
    #**** ASSIGNEMENT OF THE RESULTS
    #******************************************************************
    #
    
    # CAI START -- add the function to write out cfac files in SOLO format
    print(' ')
    print(' ')
    print(' ')
    print(' /////////////////////////////////////////////')
    print('     CORRECTIONS FOR NAVIGATIONAL ERRORS')
    print(' //////////// (add these values)  ////////////')
    print(' /////////////////////////////////////////////')
    print(' ')
    print(' ')
    #
    with open(fich_x_path, 'w') as f10:

    write(10
          ,"(//
             ,' /////////////////////////////////////////////'
           ,/,'    CORRECTIONS FOR NAVIGATIONAL ERRORS'
           ,/,' //////////// (add these values)  ////////////'
           ,/,' /////////////////////////////////////////////'
             ,//)")
    #
    if idtiltaft:
        dtiltaft_res=res[variable_indexes.tilt_aft]
        print(' D_TILT_aft (deg) guess,residual,total : '
               ,dtiltaft_guess,dtiltaft_res
               ,dtiltaft_guess+dtiltaft_res)
        f10.write("(' D_TILT_aft (deg) guess,residual,total : '
                   ,3f7.3,/)")
             dtiltaft_guess,dtiltaft_res
            ,dtiltaft_guess+dtiltaft_res
    # CAI
        tilt_corr_aft = dtiltaft_guess+dtiltaft_res
    else:
        dtiltaft_res=0.
        tilt_corr_aft = 0.0
    #endif
    #
    if idtiltfore:
        dtiltfore_res=res[variable_indexes.tilt_fore]
        print(' D_TILT_fore (deg) guess,residual,total : '
             ,dtiltfore_guess,dtiltfore_res
             ,dtiltfore_guess+dtiltfore_res)
        f10.write("(' D_TILT_fore  (deg) guess,residual,total : '
                 ,3f7.3,/)")
             dtiltfore_guess,dtiltfore_res
            ,dtiltfore_guess+dtiltfore_res
    # CAI
        tilt_corr_fore = dtiltfore_guess+dtiltfore_res
    else:
        dtiltfore_res=0.
        tilt_corr_fore = 0.0
    # endif
    #
    if idrotaaft:
        drotaaft_res=res[variable_indexes.rot_aft]
        print(' D_ROTA_aft (deg) guess,residual,total : '
             ,drotaaft_guess,drotaaft_res
             ,drotaaft_guess+drotaaft_res
        f10.write("(' D_dROTA_aft (deg) guess,residual,total : '
                 ,3f7.3,/)")
           drotaaft_guess,drotaaft_res
          ,drotaaft_guess+drotaaft_res
    # CAI
        rot_angle_corr_aft = drotaaft_guess+drotaaft_res
    else:
        drotaaft_res=0.
        rot_angle_corr_aft = 0.0
    # endif
    #
    if idrotafore:
        drotafore_res=res[variable_indexes.rot_fore]
        print(' D_ROTA_fore (deg) guess,residual,total : '
             ,drotafore_guess,drotafore_res
             ,drotafore_guess+drotafore_res
        f10.write("(' D_dROTA_fore (deg) guess,residual,total : '
                 ,3f7.3,/)")
           drotafore_guess,drotafore_res
          ,drotafore_guess+drotafore_res
    # CAI
        rot_angle_corr_fore = drotafore_guess+drotafore_res
    else:
        drotafore_res=0.
        rot_angle_corr_fore = 0.0
    # endif
    #
    if idpitch:
        dpitch_res=res[variable_indexes.pitch]
        print(' D_PITCH (deg) guess,residual,total : '
               ,dpitch_guess,dpitch_res,dpitch_guess+dpitch_res
        f10.write("(' D_PITCH (deg) guess,residual,total : '
                 ,3f7.3,/)")
             dpitch_guess,dpitch_res,dpitch_guess+dpitch_res
    # CAI
        pitch_corr_cfac = dpitch_guess+dpitch_res
    else:
        dpitch_res=0.
        pitch_corr_cfac = 0.0
    # endif
    #
    if idhdg:
        dhdg_res=res[variable_indexes.dhdg]
        print(' D_HEADING (deg) guess,residual,total : '
             ,dhdg_guess,dhdg_res,dhdg_guess+dhdg_res
        f10.write("(' D_HEADING (deg) guess,residual,total : '
                 ,3f7.3,/)")
           dhdg_guess,dhdg_res,dhdg_guess+dhdg_res
    # CAI
        drift_corr_cfac = dhdg_guess+dhdg_res
    else:
        dhdg_res=0.
        drift_corr_cfac = 0.0
    # endif
    #
    if irdaft:
        rdaft_res=100.*res[variable_indexes.rdaft]
        print(' RANGE_DELAY_AFT (m) guess,residual,total : '
             ,1000.*rdaft_guess,rdaft_res
             ,1000.*rdaft_guess+rdaft_res
        f10.write("(' RANGE_DELAY_AFT (m) guess,residual,total : '
                 ,3f6.0,/)")
           1000.*rdaft_guess,rdaft_res
          ,1000.*rdaft_guess+rdaft_res
    # CAI
        range_delay_corr_aft = 1000.*rdaft_guess+rdaft_res
    else:
        rdaft_res=0.
        range_delay_corr_aft = 0.0
    # endif
    #
    if irdfore:
        rdfore_res=100.*res[variable_indexes.rdfore]
        print(' RANGE_DELAY_FORE (m) guess,residual,total : '
             ,1000.*rdfore_guess,rdfore_res
             ,1000.*rdfore_guess+rdfore_res
        f10.write("(' RANGE_DELAY_FORE (m) guess,residual,total : '
                 ,3f6.0,/)")
           1000.*rdfore_guess,rdfore_res
          ,1000.*rdfore_guess+rdfore_res
    # CAI
        range_delay_corr_fore = 1000.*rdfore_guess+rdfore_res
    else:
        rdfore_res=0.
        range_delay_corr_fore = 0.0
    # endif
    #
    if idxwe:
        dxwe_res=100.*res[variable_indexes.dxwe]
        print(' D_XWE (m) guess,residual,total : '
             ,1000.*dxwe_guess,dxwe_res
             ,1000.*dxwe_guess+dxwe_res
        f10.write("(' D_XWE (m) guess,residual,total : '
                 ,3f6.0,/)")
           1000.*dxwe_guess,dxwe_res
          ,1000.*dxwe_guess+dxwe_res
    else:
        dxwe_res=0.
    # endif
    #
    if idysn:
        dysn_res=100.*res[variable_indexes.dysn]
        print(' D_YSN (m) guess,residual,total : '
             ,1000.*dysn_guess,dysn_res
             ,1000.*dysn_guess+dysn_res
        f10.write("(' D_YSN (m) guess,residual,total : '
                 ,3f6.0,/)")
           1000.*dysn_guess,dysn_res
          ,1000.*dysn_guess+dysn_res
    else:
        dxwe_res=0.
    # endif
    #
    if idzacft:
        dzacft_res=100.*res[variable_indexes.dzacft]
        print(' D_ZACFT (m) guess,residual,total : '
             ,1000.*dzacft_guess,dzacft_res
             ,1000.*dzacft_guess+dzacft_res
        f10.write("(' D_ZACFT (m) guess,residual,total : '
                 ,3f6.0,/)")
           1000.*dzacft_guess,dzacft_res
          ,1000.*dzacft_guess+dzacft_res
    # CAI
        pressure_alt_corr = 1000.*dzacft_guess+dzacft_res
    else:
        dzacft_res=0.
        pressure_alt_corr = 0.0
    # endif
    #
    if idvh:
        dvh_res=res[variable_indexes.dvh]
        print(' D_VHACFT (m/s) guess,residual,total : '
             ,dvh_guess,dvh_res,dvh_guess+dvh_res
        f10.write("(' D_VHACFT (m/s) guess,residual,total : '
                 ,3f6.2,/)")
           dvh_guess,dvh_res,dvh_guess+dvh_res
    # CAI
        ew_gndspd_corr = dvh_guess+dvh_res
    else:
        dvh_res=0.
        ew_gndspd_corr = 0.0
    # endif
    #
    print(' ')
    	    print(' ')
    	    print(' ')
    	    print(' ')
    	    print(' //////////////////////////////////////////////////')
    	    print(' //////////////////////////////////////////////////')
    	    print(' //////////////////////////////////////////////////')
    #
    f10.write("(///
               ,' /////////////////////////////////////////////'
              )")
    #


    return range_delay_corr_aft,
        pressure_alt_corr,
        ew_gndspd_corr,
        pitch_corr_cfac,
        drift_corr_cfac,
        rot_angle_corr_aft,
        tilt_corr_aft
