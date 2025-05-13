import numpy as np

# writes to the CORNAV_EL_* file #10   fich_cornav= "('CORNAV_E_',a6,'_',a6)") c_hms_min(2:7),c_hms_max(2:7)
# send the values that need to be written to the #10 file
def calculate_navigational_errors(directory, fich_cornav,
    yymmdd, rw_dzsurf,rw_vsurf,rw_dvinsitu,
    idtmfile, iwrisurfile, 
    idtiltaft, idtiltfore, idrotaaft, idrotafore, idpitch, idhdg, irdaft, irdfore, idxwe, 
    idysn, idzacft, idvh, 
    swdzsurf_tot, 
    ):
   

    fich_cornav = f"CORNAV_E_{c_hms_min[1:7]}_{c_hms_max[1:7]}"
    fich_sis = f"SIS_E_{c_hms_min[1:7]}_{c_hms_max[1:7]}"

    # writes output to a string
    # write(c_hms_min,"(i7)")1000000+ihms_min
    # write(c_hms_max,"(i7)")1000000+ihms_max
    # write(fich_cornav,"('CORNAV_E_',a6,'_',a6)")
    #      c_hms_min(2:7),c_hms_max(2:7)
    # write(fich_sis,"('SIS_E_',a6,'_',a6)")
    #      c_hms_min(2:7),c_hms_max(2:7)
    #
    #******************************************************************
    #**** OPEN THE OUPUT "CORNAV_EL_*" FILE #10
    #******************************************************************
    #
    path = os.path.join(directory, fich_cornav)
    print(' ')
    print(' OPEN "CORNAV_EL_*" FILE #10 :', path)
    if not os.path.exists(directory):
       os.makedirs(directory)
    with open(path, 'w') as f10:
        #open(10,file=directory(1:ndir)//'/'//fich_cornav
        #       ,form='formatted',status='unknown')
        print("yymmdd: ", yymmdd)
        f10.write(f"{' YYYYMMDD : '}{yymmdd:<12}")
        #f10.write(f"{' HHMMSS_min HHMMSS_max : '}{,a6,3x,a6,/)")
        #     c_hms_min(2:7),c_hms_max(2:7)
        f10.write(f"{ ' FIELDS TAKEN INTO ACCOUNT',/
                   ,'  -> REL.WGHT_dZsurf,Vsurf,dVinsitu : ',3f6.3,/)")
             rw_dzsurf,rw_vsurf,rw_dvinsitu
        f10.write(f"{ ' VARIABLES TAKEN INTO ACCOUNT',/
                   ,'  -> D_TILT_AFT,D_TILT_FORE (1/0) : ',2i2,/
                   ,'  -> D_ROTA_AFT,D_ROTA_FORE (1/0) : ',2i2,/
                   ,'  -> D_PITCH,D_HEADING (1/0) : ',2i2,/
                   ,'  -> RANGE_DELAY_AFT,RANGE_DELAY_FORE (1/0) : '
                   ,2i2,/
                   ,'  -> D_XWE,D_YSN,D_ZACFT (1/0) : ',3i2,/
                   ,'  -> D_VHACFT (1/0) : ',i2)")
             idtiltaft,idtiltfore
            ,idrotaaft,idrotafore
            ,idpitch,idhdg
            ,irdaft,irdfore
            ,idxwe,idysn,idzacft
            ,idvh
        if idtmfile == 1:
          f10.write(f"{' READS THE SURF_DTM_* FILE :',a50)")
               directory(1:ndir)//'/'//dtm_file(1:ndtmfile)
        else:
          f10.write(f"{ ' NO SURF_DTM_* FILE TO READ '
   #                  ,'-> ALT_SURF(x,y)=CST (',f6.3,')')")
               zsurf_cst
        # endif
        if iwrisurfile == 1:
          f10.write(f"{' WRITES THE SURF_EL_* FILE :',a50,//)")
               directory(1:ndir)//'/'//wrisurfile(1:nsf)
        else:
          f10.write(f"{' NO SURF_EL_* FILE TO WRITE ',//)")
 






 
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
# ^^^^ this goes to enough_points.py
    #
    #******************************************************************
    #**** RMS VALUES OF THE NORMALIZED VARIABLES
    #******************************************************************
    #
    print(' ')
    print(' **********************************************')
    print(' *** RMS VALUES OF THE NORMALIZED VARIABLES ***')
    print(' **********************************************')
    print(' ')
    
    if swdzsurf_tot > 1.:
        print(' DZ_surf -> sWGHTs:',swdzsurf_tot
        print('          rms_VAR(dTaft,dTfore:'
               ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=1,2)))
        print('          -------(dRaft,dRfore:'
               ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=3,4))
        print('          -------(dPitch,dHdg:'
               ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=5,6))
        print('          -------(RDaft,RDfore:'
               ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=7,8))
        print('          -------(dXwe,dYsn,dZacft:'
               ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=9,11))
        print('          -------(dVHacft:'
               ,sqrt(rms_var_zsurf(12)/swadzsurf_tot))
    else:
        print(' !!!! DZ_surf -> sWGHTs:',swdzsurf_tot,' !!!!')
    # endif
    #
    if swvsurf_tot > 1.:
        print(' VDOP_surf -> sWGHTs:',swvsurf_tot)
        print('          rms_VAR(dTaft,dTfore:'
               ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=1,2))
        print('          -------(dRaft,dRfore:'
               ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=3,4))
        print('          -------(dPitch,dHdg:'
               ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=5,6))
        print('          -------(RDaft,RDfore:'
               ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=7,8))
        print('          -------(dXwe,dYsn,dZacft:'
               ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=9,11))
        print('          -------(dVHacft:'
               ,sqrt(rms_var_vsurf(12)/swavsurf_tot))
    else:
        print(' !!!! VDOP_surf -> sWGHTs:',swvsurf_tot,' !!!!')
    # endif
    #
    if swdvinsitu_tot > 1.:
        print(' DVDOP_insitu -> sWGHTs:',swdvinsitu_tot)
        print('          rms_VAR(dTaft,dTfore:'
               ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=1,2))
        print('          -------(dRaft,dRfore:'
               ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=3,4))
        print('          -------(dPitch,dHdg:'
               ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=5,6))
        print('          -------(RDaft,RDfore:'
               ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=7,8))
        print('          -------(dXwe,dYsn,dZacft:'
               ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=9,11))
        print('          -------(dVHacft:'
               ,sqrt(rms_var_vinsitu(12)/swadvinsitu_tot))
    else:
        print(' !!!! DVDOP_insitu -> sWGHTs:'
               ,swdvinsitu_tot,' !!!!')
    # endif
    #
    #******************************************************************
    #**** NORMALIZED CORRELATION MATRIX BETWEEN THE NVAR VARIABLES
    #******************************************************************
    #
    print(' ')
    sp_zsvszi=swdzsurf_tot+swvsurf_tot+swdvinsitu_tot
    if sp_zsvszi > 1.:
        print(' **********************************************')
	print(' ******* NORMALIZED CORRELATION MATRIX ********')
	print(' *******            (*1000)            ********')
	print(' *******   BETWEEN THE NVAR VARIABLES  ********')
	print(' **********************************************')
	print(' ')
        print('        dTa-dTf-dRa-dRf-dP-dH-RDa-RDf' ,'-dX-dY-dZ-dV ')
       #do i=1,nvar
        for i in range(nvar):
            match i:
                case 1:
                    print(' dTa  - '
                        ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 2:
                    print(' dTf  - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 3:
                    print(' dRa  - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 4:
                    print(' dRf  - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 5:
                    print(' dP   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 6:
                    print(' dH   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 7:
                    print(' RDa - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 8:
                    print(' RDf - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 9:
                    print(' dX   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 10:
                    print(' dY   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
                case 11:
                    print(' dZ   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case 12:
                    print(' dV   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
                case -:
                    print("something went wrong with dTa - dTf")
        #
                # case / was endif
         # enddo
    else:
         print(' !!!! sw_Zsurf+Vsurf+Vinsitu:',sp_zsvsvi,' !!!!')
    # endif
    print(' ')
    #
    #******************************************************************
    #**** NORMALIZATION OF THE MATRICES AND VECTORS
    #**** FOR DZ_surf, VDOP_surf et DVDOP_insitu
    #**** BY THE SUM OF THE POSITIVE VALUES OF THE OBSERVED ERRORS
    #**** THEN BUILD A UNIQUE MATRICE AND VECTOR BY SUMMING
    #******************************************************************
    #
    print(' ')
    print(' NORMALIZATION OF THE MATRICES AND VECTORS')
    print(' SumPosVal_DZsurf,VDOPsurf,DVDOPinsitu:'
        ,swadzsurf_tot,swavsurf_tot,swadvinsitu_tot)
          
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
    for i in range(1, nvar + 1:
        vect[i - 1] = 0.0
        if kdzsurf == 1 and swadzsurf_tot > 0:
            vect[i - 1] += rw_dzsurf * vect_dzsurf[i - 1] / swadzsurf_tot
        if kvsurf == 1 and swavsurf_tot > 0:
            vect[i - 1] += rw_vsurf * vect_vsurf[i - 1] / swavsurf_tot
        if kdvinsitu == 1 and swadvinsitu_tot > 0:
            vect[i - 1] += rw_dvinsitu * vect_dvinsitu[i - 1] / swadvinsitu_tot
        
        for j in range(1, nvar + 1:
            xmat[i - 1, j - 1] = 0.0
            if kdzsurf == 1 and swadzsurf_tot > 0:
                xmat[i - 1, j - 1] += rw_dzsurf * xmat_dzsurf[i - 1, j - 1] / swadzsurf_tot
            if kvsurf == 1 and swavsurf_tot > 0:
                xmat[i - 1, j - 1] += rw_vsurf * xmat_vsurf[i - 1, j - 1] / swavsurf_tot
            if kdvinsitu == 1 and swadvinsitu_tot > 0:
                xmat[i - 1, j - 1] += rw_dvinsitu * xmat_dvinsitu[i - 1, j - 1] / swadvinsitu_tot
            if abs(xmat[i - 1, j - 1]) > 0:
                itest_xmat = 1
    
        if abs(xmat[i - 1, i - 1]) <= 0:
            for j in range(1, nvar + 1:
                xmat[i - 1, j - 1] = 0.0
                xmat[j - 1, i - 1] = 0.0
            xmat[i - 1, i - 1] = 1.0
            vect[i - 1] = 0.0
    
    
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
        resoud(xmat,xinv,vect,res,nvar)
    else:
        print(' !!!! XMAT=0 !!!!')
    # endif
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!      print(' '
    #!!!!      print(' RESULTING VECTOR'
    #!!!!      do i=1,nvar
    #!!!!         print(' RES(',i,':',res(i)
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
        dtiltaft_res=res(1)
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
        dtiltfore_res=res(2)
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
        drotaaft_res=res(3)
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
        drotafore_res=res(4)
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
        dpitch_res=res(5)
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
        dhdg_res=res(6)
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
        rdaft_res=100.*res(7)
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
        rdfore_res=100.*res(8)
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
        dxwe_res=100.*res(9)
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
        dysn_res=100.*res(10)
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
        dzacft_res=100.*res(11)
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
        dvh_res=res(12)
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

