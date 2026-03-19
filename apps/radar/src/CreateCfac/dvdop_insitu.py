import simulate_dv_dopinsitu_with_guess
import ctrl_contray


# fills xmat_dvinsitu, vect_dvinsitu
#       xmat_vsurf,
#       vi_dhor, vi_vdop, vi_vinsitu
#
def dvdop_insitu(kdvinsit, ngates_insitu_max,
    ictrl_contray,
    dgate_corr, # array
    ze,         # array
    # ichoice_vdop,
    vdop_corr,
    # xpmin_contray,
    proj_wind,
    dmax_insitu,
    # ddg,
    # vnyq,
    # dvdop_max, 
    nb_ray,
    iradar_ray,
    ilr,
    ihhmmss,  # just for debug print lines
    ims_ray,  # just for debug print lines
    rota_ray,tilt_ray,  # just for debug print lines
    roll_acft,pitch_acft,hdg_acft,drift_acft,  # just for debug print lines
    azeast_ray,elhor_ray,  # just for debug print lines
    isim, 
    wa_nz,
    conv,
    # drota_guess,
    # dpitch_guess,
    # dhdg_guess,
    # cwe_true,duacft_dv_true,
    # csn_true,dvacft_dv_true,dvh_guess,
    # proj_wind_true,
    # wa_we_true,dcwe_dt_true,
    # wa_sn_true,dcsn_dt_true,
    # dcnz_dt_true,
    # dtilt_guess,
    # dcwe_dr_true,
    # dcsn_dr_true,
    # dcnz_dr_true,
    # dcwe_dp_true,
    # dcsn_dp_true,
    # dcnz_dp_true,
    # dcwe_dh_true,
    # dcsn_dh_true,
    # dcnz_dh_true,

    ):

#******************************************************************
#**** CASE "DVDOP_insitu"
#**** (if D<DMAX_insitu and ||sin(ELEV_HOR)||<0.1)
#******************************************************************
#
    if(kdvinsitu == 1 and ngates_insitu_max > 1):
#
#******************************************************************
#**** CONTROL CONTINUITY ALONG THE RAY ( if ICTRL_CONTRAY=1 )
#**** DISMISS VDOP IF |VDOP-VDOP_PREV|>dVDOP_MAX AFTER UNFOLDING
#******************************************************************
#
        if(ictrl_contray == 1):    # always set to 0 in code, regardless of input param
            ctrl_contray.ctrl_contray()
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        itest=1
        for ig in range(0,ngates_insitu_max):
            if (ze[ig] > -900.  and vdop_corr[ig] > -900.):
                itest=1
        #enddo
        if (itest == 1 and nb_ray[iradar_ray] == 5*(nb_ray[iradar_ray]/5)):
            print(' ')
            print(' ',1000*ihhmmss+ims_ray
                ,' IRADAR:',iradar_ray
                ,' NO_RAY:',nb_ray[iradar_ray])
            print('    ROTA,TILT_RAY:',rota_ray,tilt_ray)
            print('    ROLL,PITCH,HDG,DRIFT_ACFT:',roll_acft
                ,pitch_acft,hdg_acft,drift_acft)
            print('    AZ_EAST:',azeast_ray,' EL_HOR:',elhor_ray)
        #endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        for ig in range(1,ngates_insitu_max):

            #------------------------------------------------------------------
            #---- ( IF ISIM=1 ) -> SIMULATED dV_dopinsitu WITH dXXX_GUESS
            #------------------------------------------------------------------
            if (ig == 1 and isim == 1):    # SIMULATION is set to 0 in input parameters
                simulate_dv_dopinsitu_with_guess.simulate_dv_dopinsitu_with_guess()

    #------------------------------------------------------------------ finally some code that is accessible ...
            if (ze[ig] > -900. and vdop_corr[ig] > -900.):
                wghtinsitu_ig=1.-0.5*dgate_corr[ig]/dmax_insitu
                dv_dopinsitu=vdop_corr[ig]-proj_wind
                if(abs(dv_dopinsitu) < dvdopinsitu_max):
                    #
                    #******************************************************************
                    #**** ADD WEIGHTS AND DVDOP_insitu
                    #******************************************************************
    
                    n_dvinsitu[iradar_ray] += 1
                    ssurfins += wghtinsitu_ig
                    swinsitu_sweep[iradar_ray] += wghtinsitu_ig
    
                    dvinsitusweep_mean[iradar_ray] += wghtinsitu_ig*dv_dopinsitu
                    dvinsitusweep_rms[iradar_ray] += wghtinsitu_ig*dv_dopinsitu*dv_dopinsitu
    
                    swdvinsitu_tot  += wghtinsitu_ig
                    swdvminsitu_tot += wghtinsitu_ig*dv_dopinsitu
                    swdv2insitu_tot += wghtinsitu_ig *dv_dopinsitu*dv_dopinsitu
                    swadvinsitu_tot += wghtinsitu_ig*abs[dv_dopinsitu]
    
                    s_vpv[iradar_ray,ilr]   += wghtinsitu_ig
                    sv_vpv[iradar_ray,ilr]  += wghtinsitu_ig*dv_dopinsitu
                    svv_vpv[iradar_ray,ilr] += wghtinsitu_ig *dv_dopinsitu*dv_dopinsitu
                    x_vpv[iradar_ray,ilr]   += wghtinsitu_ig
                    xv_vpv[iradar_ray,ilr]  += wghtinsitu_ig*dv_dopinsitu
                    xvv_vpv[iradar_ray,ilr] += wghtinsitu_ig *dv_dopinsitu*dv_dopinsitu
                    #
                    #******************************************************************
                    #**** VALUES OF VAR(1->NVAR) FOR FIELD "DV_insitu"
                    #****  - VAR(1->6) -> [dT_aft,dT_fore,dR_aft,dR_fore,dP,dH] in DEGREES
                    #****  - VAR(7->11) -> [RD_aft,RD_fore,dXwe,dYsn,dZ] in HECTOMETERS
                    #****  - VAR(12) -> [dVH] in METER/SECOND
                    #******************************************************************
                    #
                    if is_aft:                 # (iaftfore == -1):
                        if(idtiltaft == 1):
                            var[1]=( wa_we*dcwe_dt+wa_sn*dcsn_dt +wa_nz*dcnz_dt)*conv
                        else:
                            var[1]=0.
                            xmat_dvinsitu[1,1] += wghtinsitu_ig
                        #endif
                        var[2]=0.
                    else:
                        var[1]=0.
                        if(idtiltfore == 1):
                            var[2]=( wa_we*dcwe_dt+wa_sn*dcsn_dt +wa_nz*dcnz_dt)*conv
                        else:
                            var[2]=0.
                            xmat_dvinsitu[2,2] += wghtinsitu_ig
                        #endif
                    #endif
    
                    if is_aft:                 # (iaftfore == -1):
                        if[idrotaaft == 1]:
                            var[3]=( wa_we*dcwe_dr+wa_sn*dcsn_dr +wa_nz*dcnz_dr)*conv
                        else:
                            var[3]=0.
                            xmat_dvinsitu[3,3] += wghtinsitu_ig
                        #endif
                        var[4]=0.
                    else:
                        var[3]=0.
                        if(idrotafore == 1):
                            var[4]=( wa_we*dcwe_dr+wa_sn*dcsn_dr +wa_nz*dcnz_dr)*conv
                        else:
                            var[4]=0.
                            xmat_dvinsitu[4,4] += wghtinsitu_ig
                        #endif
                    #endif
    
                    if(idpitch == 1):
                        var[5]=( wa_we*dcwe_dp+wa_sn*dcsn_dp +wa_nz*dcnz_dp)*conv
                    else:
                        var[5]=0.
                        xmat_dvinsitu[5,5] += wghtinsitu_ig
                    #endif
    
                    if(idhdg == 1):
                        var[6]=[wa_we*dcwe_dh+wa_sn*dcsn_dh]*conv
                    else:
                        var[6]=0.
                        xmat_dvinsitu[6,6] += wghtinsitu_ig
                    #endif
    
                    var[7]=0.
                    var[8]=0.
                    var[9]=0.
                    var[10]=0.
                    var[11]=0.
    
                    if(idvh == 1):
                        var[12]=-duacft_dv*cwe-dvacft_dv*csn
                    else:
                        var[12]=0.
                        xmat_dvinsitu[12,12] += wghtinsitu_ig
                    #endif
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #!!!!      print['    VAR_DVINSITU[1->12]:',[var[i],i=1,12]
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #
                    #******************************************************************
                    #**** ADD TO XMAT_dvinsitu[1->NVAR,1->NVAR] AND VECT_dvinsitu[1->NVAR]
                    #******************************************************************
                    #
                    for i in range(1,nvar):
                        for j in range(1,nvar):
                            xmat_dvinsitu[[i,j]] += wghtinsitu_ig*var[i]*var[j]
                        #enddo
                        vect_dvinsitu[i] += wghtinsitu_ig*var[i]*dv_dopinsitu
                    #enddo
                    #
                    #******************************************************************
                    #**** ADD TO COVARIANCE MATRIX FOR FIELD "DVDOP_insitu"
                    #******************************************************************
                    #
                    for i in range(1,nvar):
                        rms_var_vinsitu[i] += wghtinsitu_ig*var[i]*var[i]
                        for j in range(1,nvar):
                            corr_var[i,j] += wghtinsitu_ig*var[i]*var[j]
                        #enddo
                    #enddo
                    #
                    #******************************************************************
                    #**** CASE "VDOP_surf" and/or "DVDOP_insitu" ONLY :
                    #**** -> RGE-DLY_aft,RGE-DLY_aft,D_XWE,D_YSN,D_ZACFT CANNOT BE CALCULATED
                    #******************************************************************
                    #
                    if(rw_dzsurf <= 0.):
                        for ij in range(7,11):
                            xmat_vsurf[ij,ij] += wghtinsitu_ig
                        #enddo
                    #endif
                    #
                    #******************************************************************
                    #**** ARRAYS FOR "SIS_EL_*" FILE
                    #******************************************************************
                    #
                    vi_dhor[iradar_ray,n_dvinsitu[iradar_ray]] =side*dgate_corr[ig]*celh
                    vi_vdop[iradar_ray,n_dvinsitu[iradar_ray]]=vdop
                    vi_vinsitu[iradar_ray,n_dvinsitu[iradar_ray]]=proj_wind
    
                 #endif  !!  of  !!  if(abs(dv_dopinsitu] < dvdopinsitu_max)  !!
    
            #endif  !!  of  !!  if(ze[ig] > -900. ... )  !!
        #enddo !!  of  !!  for ig in range(1,ngates_insitu_max)  !!
    
    #endif  !!  of  !!  if(kdvinsitu == 1 and ngates_insitu_max > 1)  !!
    

    return xmat_dvinsitu, vect_dvinsitu, xmat_vsurf, vi_dhor, vi_vdop, vi_vinsitu
