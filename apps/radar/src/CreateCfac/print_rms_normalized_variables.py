import numpy as np


# 
def print_rms_normalized_variables(directory, fich_cornav,
    yymmdd, rw_dzsurf,rw_vsurf,rw_dvinsitu,
    idtmfile, iwrisurfile, 
    idtiltaft, idtiltfore, idrotaaft, idrotafore, idpitch, idhdg, irdaft, irdfore, idxwe, 
    idysn, idzacft, idvh, 
    swdzsurf_tot,
    nvar,
    ):

    # constants to reference the array contents with names
    index_tilt_aft  = 0
    index_tilt_fore = 1
    index_rot_aft   = 2
    index_rot_fore  = 3
    index_pitch     = 4
    index_dhdg      = 5
    index_rdaft     = 6
    index_rdfore    = 7
    index_dxwe      = 8
    index_dysn      = 9
    index_dzacft    = 10
    index_dvh       = 11
   
    write_cornav_file()

 
#    print(' ')
#    print(' **********************************************')
#    print(' ')
#    print(' ')
#    print(' ')
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
                case index_tilt_aft:
                    print(' dTa  - '
                        ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_tilt_fore:
                    print(' dTf  - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_rot_aft:
                    print(' dRa  - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_rot_fore:
                    print(' dRf  - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_pitch:
                    print(' dP   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_dhdg:
                    print(' dH   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_rdaft:
                    print(' RDa - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_rdfore:
                    print(' RDf - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_dxwe:
                    print(' dX   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_dysn:
                    print(' dY   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
                case index_dzacft:
                    print(' dZ   - '
                           ,(int(1000.*corr_var(i,j)
                                 /amax1( 0.01
                                        ,sqrt( corr_var(i,i)
                                              *corr_var(j,j))))
                             ,j=1,nvar))
        #
                case index_dvh:
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



