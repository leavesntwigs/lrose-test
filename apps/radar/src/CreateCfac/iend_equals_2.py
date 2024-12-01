	  print(' ')
	  print(' ****************************************************')
	  print('   HHMMSS :',ih_ray,im_ray,is_ray
                 ,'   -> END OF CONSIDERED PERIOD')
	  print('   NB_SWEEPS_READ FOR AFT AND FORE RADARS :'
                 ,nb_sweep)
	  print(' ****************************************************')
	  print(' ')
	  print(' ')
          write(10,"(' NB_SWEEPS FOR THE AFT AND FORE RADARS: '
                     ,2i5,/)")
                    ,int(xsweeps(1)),int(xsweeps(2))
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

import numpy as np

if kdzsurf == 1:
    bias_dzsurf = swdzmsurf_tot / max(1.0, swdzsurf_tot)
    stdv_dzsurf = np.sqrt(swdzsurf_tot * swdz2surf_tot - swdzmsurf_tot * swdzmsurf_tot) / max(1.0, swdzsurf_tot)
    print(' ')
    print(' dZ_surf (km) sum_wghts,mean,stdv :', swdzsurf_tot, bias_dzsurf, stdv_dzsurf)
    print(f' dZ_surf (km) sum_wghts,mean,stdv : {swdzsurf_tot:10.1f} {bias_dzsurf:8.3f} {stdv_dzsurf:8.3f}')

if kvsurf == 1:
    bias_vsurf = swvmsurf_tot / max(1.0, swvsurf_tot)
    stdv_vsurf = np.sqrt(swvsurf_tot * swv2surf_tot - swvmsurf_tot * swvmsurf_tot) / max(1.0, swvsurf_tot)
    print(' ')
    print(' VDOP_surf (m/s) sum_wghts,mean,stdv :', swvsurf_tot, bias_vsurf, stdv_vsurf)
    print(f' VDOP_surf (m/s) sum_wghts,mean,stdv : {swvsurf_tot:10.1f} {bias_vsurf:8.3f} {stdv_vsurf:8.3f}')

if kdvinsitu == 1:
    bias_dvinsitu = swdvminsitu_tot / max(1.0, swdvinsitu_tot)
    stdv_dvinsitu = np.sqrt(swdvinsitu_tot * swv2insitu_tot - swdvminsitu_tot * swdvminsitu_tot) / max(1.0, swdvinsitu_tot)
    print(' ')
    print(' dVDOP_insitu (m/s) sum_wghts,mean,stdv :', swdvinsitu_tot, bias_dvinsitu, stdv_dvinsitu)
    print(f' dVDOP_insitu (m/s) sum_wghts,mean,stdv : {swdvinsitu_tot:10.1f} {bias_dvinsitu:8.3f} {stdv_dvinsitu:8.3f}')
    
    for iradar in range(1, 3):
        print('   IRADAR (AR=1,AV=2) :', iradar)
        bias_dvinsitu_ir_g = xv_vpv[iradar-1][0] / max(1.0, x_vpv[iradar-1][0])
        stdv_dvinsitu_ir_g = np.sqrt(x_vpv[iradar-1][0] * xvv_vpv[iradar-1][0] - xv_vpv[iradar-1][0] * xv_vpv[iradar-1][0]) / max(1.0, x_vpv[iradar-1][0])
        print('     -> VDOP-PROJWIND_LEFT_npts,mean,stdv:', x_vpv[iradar-1][0], bias_dvinsitu_ir_g, stdv_dvinsitu_ir_g)
        print(f'   IRADAR (AR=1,AV=2) : {iradar}    -> VDOP-PROJWIND_LEFT_npts,mean,stdv: {x_vpv[iradar-1][0]:10.1f} {bias_dvinsitu_ir_g:8.3f} {stdv_dvinsitu_ir_g:8.3f}')
        
        bias_dvinsitu_ir_d = xv_vpv[iradar-1][1] / max(1.0, x_vpv[iradar-1][1])
        stdv_dvinsitu_ir_d = np.sqrt(x_vpv[iradar-1][1] * xvv_vpv[iradar-1][1] - xv_vpv[iradar-1][1] * xv_vpv[iradar-1][1]) / max(1.0, x_vpv[iradar-1][1])
        print('     -> VDOP-PROJWIND_RIGHT_npts,mean,stdv:', x_vpv[iradar-1][1], bias_dvinsitu_ir_d, stdv_dvinsitu_ir_d)
        print(f'    -> VDOP-PROJWIND_RIGHT_npts,mean,stdv: {x_vpv[iradar-1][1]:10.1f} {bias_dvinsitu_ir_d:8.3f} {stdv_dvinsitu_ir_d:8.3f}')
    
    print(' ')
    print()



# autoconverted end

	  print(' ')
	  print(' **********************************************')
	  print(' ')
	  print(' ')
	  print(' ')
#
#******************************************************************
#****  (IF SUM_WGHTS_surf+insitu > SUM_WGHTS_min)
#****   -> NAVIGATIONAL ERROS CAN BE CALCULATED
#******************************************************************
#
	  if(ssurfins > ssurfins_min):
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
#
            if(swdzsurf_tot > 1.):
              print(' DZ_surf -> sWGHTs:',swdzsurf_tot
              print('          rms_VAR(dTaft,dTfore):')
                     ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=1,2))
              print('          -------(dRaft,dRfore):'
                     ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=3,4))
              print('          -------(dPitch,dHdg):'
                     ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=5,6))
              print('          -------(RDaft,RDfore):'
                     ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=7,8))
              print('          -------(dXwe,dYsn,dZacft):'
                     ,(sqrt(rms_var_zsurf(i)/swadzsurf_tot),i=9,11))
              print('          -------(dVHacft):'
                     ,sqrt(rms_var_zsurf(12)/swadzsurf_tot))
            else
              print(' !!!! DZ_surf -> sWGHTs:',swdzsurf_tot,' !!!!')
            endif
#
            if(swvsurf_tot > 1.):
              print(' VDOP_surf -> sWGHTs:',swvsurf_tot)
              print('          rms_VAR(dTaft,dTfore):'
                     ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=1,2))
              print('          -------(dRaft,dRfore):'
                     ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=3,4))
              print('          -------(dPitch,dHdg):'
                     ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=5,6))
              print('          -------(RDaft,RDfore):'
                     ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=7,8))
              print('          -------(dXwe,dYsn,dZacft):'
                     ,(sqrt(rms_var_vsurf(i)/swavsurf_tot),i=9,11))
              print('          -------(dVHacft):'
                     ,sqrt(rms_var_vsurf(12)/swavsurf_tot))
            else
              print(' !!!! VDOP_surf -> sWGHTs:',swvsurf_tot,' !!!!')
            endif
#
            if(swdvinsitu_tot > 1.):
              print(' DVDOP_insitu -> sWGHTs:',swdvinsitu_tot)
              print('          rms_VAR(dTaft,dTfore):'
                     ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=1,2))
              print('          -------(dRaft,dRfore):'
                     ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=3,4))
              print('          -------(dPitch,dHdg):'
                     ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=5,6))
              print('          -------(RDaft,RDfore):'
                     ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=7,8))
              print('          -------(dXwe,dYsn,dZacft):'
                     ,(sqrt(rms_var_vinsitu(i)/swadvinsitu_tot),i=9,11))
              print('          -------(dVHacft):'
                     ,sqrt(rms_var_vinsitu(12)/swadvinsitu_tot))
            else
              print(' !!!! DVDOP_insitu -> sWGHTs:'
                     ,swdvinsitu_tot,' !!!!')
            endif
#
#******************************************************************
#**** NORMALIZED CORRELATION MATRIX BETWEEN THE NVAR VARIABLES
#******************************************************************
#
            print(' ')
            sp_zsvszi=swdzsurf_tot+swvsurf_tot+swdvinsitu_tot
            if(sp_zsvszi > 1.):
	    print(' **********************************************')
	    print(' ******* NORMALIZED CORRELATION MATRIX ********')
	    print(' *******            (*1000)            ********')
	    print(' *******   BETWEEN THE NVAR VARIABLES  ********')
	    print(' **********************************************')
	    print(' ')
              print('        dTa-dTf-dRa-dRf-dP-dH-RDa-RDf'
                     ,'-dX-dY-dZ-dV ')
              do i=1,nvar
#
                 if(i == 1):
                   print(' dTa  - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 2):
                   print(' dTf  - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 3):
                   print(' dRa  - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 4):
                   print(' dRf  - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 5):
                   print(' dP   - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 6):
                   print(' dH   - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 7):
                   print(' RDa - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 8):
                   print(' RDf - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 9):
                   print(' dX   - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 10):
                   print(' dY   - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
                 elif(i == 11):
                   print(' dZ   - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 elif(i == 12):
                   print(' dV   - '
                          ,(int(1000.*corr_var(i,j)
                                /amax1( 0.01
                                       ,sqrt( corr_var(i,i)
                                             *corr_var(j,j))))
                            ,j=1,nvar))
#
                 endif
              enddo
            else
              print(' !!!! sw_Zsurf+Vsurf+Vinsitu:',sp_zsvsvi,' !!!!')
            endif
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
#               if(kdzsurf == 1 and swadzsurf_tot > 0.)
#                 vect(i)=vect(i)+rw_dzsurf*vect_dzsurf(i)
#                                 /swadzsurf_tot
#               if(kvsurf == 1 and swavsurf_tot > 0.)
#                 vect(i)=vect(i)+rw_vsurf*vect_vsurf(i)
#                                 /swavsurf_tot
#               if(kdvinsitu == 1 and swadvinsitu_tot > 0.)
#                 vect(i)=vect(i)+rw_dvinsitu*vect_dvinsitu(i)
#                                 /swadvinsitu_tot
#               do j=1,nvar
#                  xmat(i,j)=0.
#                  if(kdzsurf == 1 and swadzsurf_tot > 0.)
#                    xmat(i,j)=xmat(i,j)+rw_dzsurf*xmat_dzsurf(i,j)
#                                        /swadzsurf_tot
#                  if(kvsurf == 1 and swavsurf_tot > 0.)
#                    xmat(i,j)=xmat(i,j)+rw_vsurf*xmat_vsurf(i,j)
#                                        /swavsurf_tot
#                  if(kdvinsitu == 1 and swadvinsitu_tot > 0.)
#                    xmat(i,j)=xmat(i,j)+rw_dvinsitu*xmat_dvinsitu(i,j)
#                                        /swadvinsitu_tot
#                  if(abs(xmat(i,j)) > 0.)itest_xmat=1
#               enddo
#
#******************************************************************
#**** CHECK THAT NO ELEMENT OF THE MATRIX' MAIN DIAGONAL IS NULL
#******************************************************************
#
#               if(abs(xmat(i,i)) <= 0.):
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
import numpy as np

itest_xmat = 0
for i in range(1, nvar + 1):
    vect[i - 1] = 0.0
    if kdzsurf == 1 and swadzsurf_tot > 0:
        vect[i - 1] += rw_dzsurf * vect_dzsurf[i - 1] / swadzsurf_tot
    if kvsurf == 1 and swavsurf_tot > 0:
        vect[i - 1] += rw_vsurf * vect_vsurf[i - 1] / swavsurf_tot
    if kdvinsitu == 1 and swadvinsitu_tot > 0:
        vect[i - 1] += rw_dvinsitu * vect_dvinsitu[i - 1] / swadvinsitu_tot
    
    for j in range(1, nvar + 1):
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
        for j in range(1, nvar + 1):
            xmat[i - 1, j - 1] = 0.0
            xmat[j - 1, i - 1] = 0.0
        xmat[i - 1, i - 1] = 1.0
        vect[i - 1] = 0.0


# autoconverted end 

            print(' '
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print(' '
#!!!!      print(' NORMALIZED MATRIX AND VECTOR'
#!!!!      do i=1,nvar
#!!!!         print(' i:',i,' XMAT(i,1->nvar)',(xmat(i,j),j=1,nvar)
#!!!!                ,' VECT(i):',vect(i)
#!!!!      enddo
#!!!!      print(' '
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** INVERSION OF THE MATRIX
#**** CALCULATION OF THE RESULTING VECTOR
#******************************************************************
#
            if(itest_xmat == 1):
              call resoud(xmat,xinv,vect,res,nvar)
            else
              print(' !!!! XMAT=0 !!!!'
            endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print(' '
#!!!!      print(' RESULTING VECTOR'
#!!!!      do i=1,nvar
#!!!!         print(' RES(',i,'):',res(i)
#!!!!      enddo
#!!!!      print(' '
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** ASSIGNEMENT OF THE RESULTS
#******************************************************************
#

# CAI START -- add the function to write out cfac files in SOLO format
            print(' '
            print(' '
            print(' '
            print(' /////////////////////////////////////////////'
            print('     CORRECTIONS FOR NAVIGATIONAL ERRORS'
            print(' //////////// (add these values)  ////////////'
            print(' /////////////////////////////////////////////'
            print(' '
            print(' '
#
            write(10
                  ,"(//
                     ,' /////////////////////////////////////////////'
                   ,/,'    CORRECTIONS FOR NAVIGATIONAL ERRORS'
                   ,/,' //////////// (add these values)  ////////////'
                   ,/,' /////////////////////////////////////////////'
                     ,//)")
#
            if(idtiltaft == 1):
              dtiltaft_res=res(1)
              print(' D_TILT_aft (deg) guess,residual,total : '
                     ,dtiltaft_guess,dtiltaft_res
                     ,dtiltaft_guess+dtiltaft_res
              write(10,"(' D_TILT_aft (deg) guess,residual,total : '
                         ,3f7.3,/)")
                   dtiltaft_guess,dtiltaft_res
                  ,dtiltaft_guess+dtiltaft_res
# CAI
              tilt_corr_aft = dtiltaft_guess+dtiltaft_res
            else
              dtiltaft_res=0.
              tilt_corr_aft = 0.0
            endif
#
            if(idtiltfore == 1):
              dtiltfore_res=res(2)
              print(' D_TILT_fore (deg) guess,residual,total : '
                     ,dtiltfore_guess,dtiltfore_res
                     ,dtiltfore_guess+dtiltfore_res
              write(10,"(' D_TILT_fore  (deg) guess,residual,total : '
                         ,3f7.3,/)")
                   dtiltfore_guess,dtiltfore_res
                  ,dtiltfore_guess+dtiltfore_res
# CAI
              tilt_corr_fore = dtiltfore_guess+dtiltfore_res
            else
              dtiltfore_res=0.
              tilt_corr_fore = 0.0
            endif
#
            if(idrotaaft == 1):
              drotaaft_res=res(3)
              print(' D_ROTA_aft (deg) guess,residual,total : '
                     ,drotaaft_guess,drotaaft_res
                     ,drotaaft_guess+drotaaft_res
              write(10,"(' D_dROTA_aft (deg) guess,residual,total : '
                         ,3f7.3,/)")
                   drotaaft_guess,drotaaft_res
                  ,drotaaft_guess+drotaaft_res
# CAI
              rot_angle_corr_aft = drotaaft_guess+drotaaft_res
            else
              drotaaft_res=0.
              rot_angle_corr_aft = 0.0
            endif
#
            if(idrotafore == 1):
              drotafore_res=res(4)
              print(' D_ROTA_fore (deg) guess,residual,total : '
                     ,drotafore_guess,drotafore_res
                     ,drotafore_guess+drotafore_res
              write(10,"(' D_dROTA_fore (deg) guess,residual,total : '
                         ,3f7.3,/)")
                   drotafore_guess,drotafore_res
                  ,drotafore_guess+drotafore_res
# CAI
              rot_angle_corr_fore = drotafore_guess+drotafore_res
            else
              drotafore_res=0.
              rot_angle_corr_fore = 0.0
            endif
#
            if(idpitch == 1):
              dpitch_res=res(5)
              print(' D_PITCH (deg) guess,residual,total : '
                     ,dpitch_guess,dpitch_res,dpitch_guess+dpitch_res
              write(10,"(' D_PITCH (deg) guess,residual,total : '
                         ,3f7.3,/)")
                   dpitch_guess,dpitch_res,dpitch_guess+dpitch_res
# CAI
              pitch_corr_cfac = dpitch_guess+dpitch_res
            else
              dpitch_res=0.
              pitch_corr_cfac = 0.0
            endif
#
            if(idhdg == 1):
              dhdg_res=res(6)
              print(' D_HEADING (deg) guess,residual,total : '
                     ,dhdg_guess,dhdg_res,dhdg_guess+dhdg_res
              write(10,"(' D_HEADING (deg) guess,residual,total : '
                         ,3f7.3,/)")
                   dhdg_guess,dhdg_res,dhdg_guess+dhdg_res
# CAI
              drift_corr_cfac = dhdg_guess+dhdg_res
            else
              dhdg_res=0.
              drift_corr_cfac = 0.0
            endif
#
            if(irdaft == 1):
              rdaft_res=100.*res(7)
              print(' RANGE_DELAY_AFT (m) guess,residual,total : '
                     ,1000.*rdaft_guess,rdaft_res
                     ,1000.*rdaft_guess+rdaft_res
              write(10,"(' RANGE_DELAY_AFT (m) guess,residual,total : '
                         ,3f6.0,/)")
                   1000.*rdaft_guess,rdaft_res
                  ,1000.*rdaft_guess+rdaft_res
# CAI
              range_delay_corr_aft = 1000.*rdaft_guess+rdaft_res
            else
              rdaft_res=0.
              range_delay_corr_aft = 0.0
            endif
#
            if(irdfore == 1):
              rdfore_res=100.*res(8)
              print(' RANGE_DELAY_FORE (m) guess,residual,total : '
                     ,1000.*rdfore_guess,rdfore_res
                     ,1000.*rdfore_guess+rdfore_res
              write(10,"(' RANGE_DELAY_FORE (m) guess,residual,total : '
                         ,3f6.0,/)")
                   1000.*rdfore_guess,rdfore_res
                  ,1000.*rdfore_guess+rdfore_res
# CAI
              range_delay_corr_fore = 1000.*rdfore_guess+rdfore_res
            else
              rdfore_res=0.
              range_delay_corr_fore = 0.0
            endif
#
            if(idxwe == 1):
              dxwe_res=100.*res(9)
              print(' D_XWE (m) guess,residual,total : '
                     ,1000.*dxwe_guess,dxwe_res
                     ,1000.*dxwe_guess+dxwe_res
              write(10,"(' D_XWE (m) guess,residual,total : '
                         ,3f6.0,/)")
                   1000.*dxwe_guess,dxwe_res
                  ,1000.*dxwe_guess+dxwe_res
            else
              dxwe_res=0.
            endif
#
            if(idysn == 1):
              dysn_res=100.*res(10)
              print(' D_YSN (m) guess,residual,total : '
                     ,1000.*dysn_guess,dysn_res
                     ,1000.*dysn_guess+dysn_res
              write(10,"(' D_YSN (m) guess,residual,total : '
                         ,3f6.0,/)")
                   1000.*dysn_guess,dysn_res
                  ,1000.*dysn_guess+dysn_res
            else
              dxwe_res=0.
            endif
#
            if(idzacft == 1):
              dzacft_res=100.*res(11)
              print(' D_ZACFT (m) guess,residual,total : '
                     ,1000.*dzacft_guess,dzacft_res
                     ,1000.*dzacft_guess+dzacft_res
              write(10,"(' D_ZACFT (m) guess,residual,total : '
                         ,3f6.0,/)")
                   1000.*dzacft_guess,dzacft_res
                  ,1000.*dzacft_guess+dzacft_res
# CAI
              pressure_alt_corr = 1000.*dzacft_guess+dzacft_res
            else
              dzacft_res=0.
              pressure_alt_corr = 0.0
            endif
#
            if(idvh == 1):
              dvh_res=res(12)
              print(' D_VHACFT (m/s) guess,residual,total : '
                     ,dvh_guess,dvh_res,dvh_guess+dvh_res
              write(10,"(' D_VHACFT (m/s) guess,residual,total : '
                         ,3f6.2,/)")
                   dvh_guess,dvh_res,dvh_guess+dvh_res
# CAI
              ew_gndspd_corr = dvh_guess+dvh_res
            else
              dvh_res=0.
              ew_gndspd_corr = 0.0
            endif
#
            print(' '
	    print(' '
	    print(' '
	    print(' '
	    print(' //////////////////////////////////////////////////'
	    print(' //////////////////////////////////////////////////'
	    print(' //////////////////////////////////////////////////'
#
            write(10,"(///
                       ,' /////////////////////////////////////////////'
                      )")
#
	  else    !!  of  !!  if(ssurfins > ssurfins_min):  !!
#
            write(10,"(/////
                      ,' /////////////////////////////////////////////'
                    ,/,'    NO CORRECTIONS FOR NAVIGATIONAL ERRORS'
                    ,/,' //////////// (not enough points) ////////////'
                    ,/,' /////////////////////////////////////////////'
                    ,///)")
#
	    print(' '
	    print(' '
	    print(' '
	    print(' /////////////////////////////////////////////'
	    print('    NO CORRECTIONS FOR NAVIGATIONAL ERRORS'
	    print(' //////////// (not enough points) ////////////'
	    print(' /////////////////////////////////////////////'
	    print(' '
#
	  endif    !!  of  !!  if(ssurfins > ssurfins_min):  !!
          print(' '
          print(' END OF "CORNAV_EL_*" FILE #10 :'
                 ,directory(1:ndir)//'/'//fich_cornav
	  close(10)
#
# CAI
#******************************************************************
#             Write the cfac files using SOLO format
#******************************************************************

# Write the aft cafc file
         write_aft_cafc(
             directory,
             range_delay_corr_aft,
             pressure_alt_corr,
             ew_gndspd_corr,
             pitch_corr_cfac,
             drift_corr_cfac,
             rot_angle_corr_aft,
             tilt_corr_aft)

# Write the fore cafc file
          write_fore_cafc(directory, 
              range_delay_corr, 
              pressure_alt_corr, 
              ew_gndspd_corr,
              pitch_corr_cfac,
              drift_corr_cfac,
              rot_angle_corr_fore,
              tilt_corr_fore)

# CAI ******  End of writing the cfac files  ******************



#******************************************************************
#**** WRITES THE "SURF_EL*" FILE #30 (if IWRISURFILE=1)
#******************************************************************
#
          if(iwrisurfile == 1):
            write_surf_el(directory, wrisurfile,
                swdzsurf_wri, sw_or_altsurf_wri
                ,nx_wrisurf,ny_wrisurf,nxysurfmax,
                )

#******************************************************************
#**** END OF "SIS_EL_*" FILE #50
#******************************************************************
#
          print(' '
          print(' END OF "SIS_EL_*" FILE #50 :'
                ,directory(1:ndir)//'/'//fich_sis
          f50.write(999,999
                    ,-999.,-999.,-999.,-999.
                    ,-999.,-999.,-999.
                    ,-999.,-999.,-999.
          f50.write(-999
          f50.write(-999
          f50.write(-999
          close(50)
#
#******************************************************************
#**** END OF PROGRAMM
#******************************************************************
#
          print(' '
          print(' **************************'
          print(' **** END OF PROGRAMM  ****'
          print(' **************************'

	  print('N1,N2,N3,N4,N5,N6,N7,N8= ',nb1,nb2,nb3,nb4,nb5,nb6
                                             ,nb7,nb8
	  print('NSUP=', nsup
	  print('NTOTAL_OK= ',nbtotals
	  print('NBON, NMAUVAIS= ',nbon,nmauvais
#
          go to 3 # stop
#
        endif    !!  of  !! if(iend == 2):  !!
