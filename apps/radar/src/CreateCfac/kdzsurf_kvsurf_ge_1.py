import numpy as np

import variable_indexes

def kdzsurf_kvsurf_ge_1(kdzsurf, kvsurf,
    selh, selh_surf, z_acft, zacftmin_surf,
    nb_ray,  # array (2) of int   nb_ray(iradar_ray) is just the ray number and here it is just for printing debug lines
    iradar_ray,
    n_dzsurf,
    altdtm_min,
    xmin_dtm,
    isim,
    igstart_surf,
    ngates_max,
    dgate_corr,
    ze,
    celh,
    ):

#******************************************************************
#**** ( if     ( KZsurf=1  or  KVsurf=1 )
#****      and  Z_ACFT > Z_ACFTmin
#****      and SIN(ELEV_HOR) < SELH_SURF
#****      and  VFF_AV>0 )
#****  -> DETERMINE ALTITUDE (THEN DOPPLER VELOCITY)
#****     OF THE SURFACE FOR THIS RAY
#******************************************************************
#
    if( (kdzsurf+kvsurf) >= 1 and
        selh < selh_surf and
        z_acft > zacftmin_surf):
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #if( nb_ray[iradar_ray] == 10*(nb_ray[iradar_ray]/10) ):
            #print(' ')
            #print(' ',1000*ihhmmss+ims_ray
            #       ,' IRADAR:',iradar_ray
            #       ,' NO_RAY:',nb_ray(iradar_ray))
            #print('    ROTA,TILT_RAY:',rota_ray,tilt_ray)
            #print('    ROLL,PITCH,HDG,DRIFT_ACFT:',roll_acft
            #       ,pitch_acft,hdg_acft,drift_acft)
            #print('    AZ_EAST:',azeast_ray,' EL_HOR:',elhor_ray)
            #print('    CWE,CSN,CNZ:',cwe,csn,cnz)
            #print('    U,V,W_ACFT:',acftspd_we,acftspd_sn,acftspd_nz
            #       ,' PROJ_VACFT:',proj_acftspd)
            #!!!!        print('    U,V,W_WIND:',wind_we,wind_sn,wind_nz
            #!!!!               ,'    PROJ_WIND:',proj_wind
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
        dsurf_ray=-999.
        dhorsurf_ray=-999.
        hsurf_ray=-999.
        refsurf_ray=0.
        refsurf_min0=20.
        gradrefsurf_min0=50.
        dhsurf_max=999.

        refsurf_min=refsurf_min0*((abs(selh))**0.7)
        gradrefsurf_ray=0.
        gradrefsurf_min=gradrefsurf_min0*((abs(selh))**0.7)
        wghtsurf_ray=0.
  #
        refmax_ray=-999.
        ig_refmax=999		# Olivier (float->entier)
        d_refmax=-999.
        h_refmax=-999.
        z_refmax=-999.
        gradrefmax_ray=-999.
        ig_gradrefmax=999	# Olivier (float->entier)
        d_gradrefmax=-999.
        h_gradrefmax=-999.
        z_gradrefmax=-999.

        rayter=6370.
#
#******************************************************************
#**** DETERMINE REFmax AND dREF/dD|max
#******************************************************************
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
#!!!!        print('    -> REFSURF,GRADREFSURF_min:'
#!!!!               ,refsurf_min,gradrefsurf_min
#!!!!      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        distmax=(z_acft-altdtm_min+1.)/abs(selh)

        dhor_prevgate=0.	# Mod Oliv
        z_prevgate=0.		# Mod Oliv

# autoconverted begin

        for ig in range(igstart_surf, ngates_max):
            if dgate_corr[ig] <= distmax:
                d_ig = dgate_corr[ig]
                dver_ig = d_ig * selh
                dhor_ig = d_ig * celh
                frac1 = 2. * (z_acft + dver_ig) / rayter
                frac2 = (z_acft**2 + d_ig**2 + 2. * z_acft * dver_ig) / (rayter**2)
                z_ig = rayter * (np.sqrt(1. + frac1 + frac2) - 1.)
                theta = np.arctan(dhor_ig / (rayter + z_acft + dver_ig))
                dhor_ig = rayter * theta
                
                if ze[ig] > -900.:
                    if ze[ig] > refmax_ray:
                        refmax_ray = ze[ig]
                        ig_refmax = ig
                        d_refmax = d_ig
                        dhor_refmax = dhor_ig
                        z_refmax = z_ig
                    
                    if ig > 0 and ze[ig - 1] > -900.:
                        gradref = (ze[ig] - ze[ig - 1]) / (d_ig - dgate_corr[ig - 1])
                        if gradref > gradrefmax_ray:
                            gradrefmax_ray = gradref
                            ig_gradrefmax = ig
                            d_gradrefmax = (d_ig + dgate_corr[ig - 1]) / 2.
                            dhor_gradrefmax = (dhor_prevgate + dhor_ig) / 2.
                            z_gradrefmax = (z_prevgate + z_ig) / 2.
                
                z_prevgate = z_ig
                dhor_prevgate = dhor_ig


# autoconverted end
#
#******************************************************************
#**** WEIGHT ASSOCIATED WITH THE OBTAINED SURFACE POINT
#******************************************************************
#
        if (refmax_ray > refsurf_min
            and gradrefmax_ray > gradrefsurf_min):
            if(     (d_refmax > d_gradrefmax)
                and abs(z_refmax-z_gradrefmax) < 1.):
                wght_ref=1.+(refmax_ray-refsurf_min)/refsurf_min
                wght_grad=1.+(gradrefmax_ray-gradrefsurf_min) / (gradrefsurf_min)
                wghtsurf_ray=sqrt(wght_ref*wght_grad)
                dsurf_ray=d_refmax
                hsurf_ray=z_refmax
                dhorsurf_ray=dhor_refmax
                xsurf_ray=x_acft+dhorsurf_ray*caze
                ysurf_ray=y_acft+dhorsurf_ray*saze
            #endif
        #endif
#
#--------------------------------------------------------------
#---- ( IF ISIM=1 ) -> (XYH)SURF_RAY FROM dXXX_GUESS   DTM
#--------------------------------------------------------------
#
        if(isim == 1):
#
#---- *_app -> with dXXX_GUESS ("apparent" navigation)
#---- *_true -> without ("true" navigation)
#
            hsurf_ray=-999.
            wghtsurf_ray=0.
            igsurf_ray=-999

            for ig in range(igstart_surf, ngates_max + 1):
                if dgate_corr[ig] <= distmax:
                    d_app = dgate_corr[ig]
                    dver_app = d_app * selh
                    dhor_app = d_app * celh
                    frac1 = 2. * (z_acft + dver_app) / rayter
                    frac2 = (z_acft**2 + d_app**2 + 2. * z_acft * dver_app) / (rayter**2)
                    z_app = rayter * (np.sqrt(1. + frac1 + frac2) - 1.)
                    theta = np.arctan(dhor_app / (rayter + z_acft + dver_app))
                    dhor_app = rayter * theta
                    x_app = x_acft + dhor_app * caze
                    y_app = y_acft + dhor_app * saze
            
                    d_true = dgate_true[ig]
                    dver_true = d_true * selh_true
                    dhor_true = d_true * celh_true
                    frac1 = 2. * (z_acft_true + dver_true) / rayter
                    frac2 = (z_acft_true**2 + d_true**2 + 2. * z_acft_true * dver_true) / (rayter**2)
                    z_true = rayter * (np.sqrt(1. + frac1 + frac2) - 1.)
                    theta = np.arctan(dhor_true / (rayter + z_acft_true + dver_true))
                    dhor_true = rayter * theta
                    x_true = x_acft_true + dhor_true * caze_true
                    y_true = y_acft_true + dhor_true * saze_true
            
                    if igsurf_ray == -999 and xmin_dtm < x_true < xmax_dtm and ymin_dtm < y_true < ymax_dtm:
                        isurf_true = (x_true - xmin_dtm) / hx_dtm + 1
                        jsurf_true = (y_true - ymin_dtm) / hy_dtm + 1
                        aa = alt_dtm[isurf_true, jsurf_true]
                        bb = (-alt_dtm[isurf_true, jsurf_true] + alt_dtm[isurf_true + 1, jsurf_true]) / hx_dtm
                        cc = (-alt_dtm[isurf_true, jsurf_true] + alt_dtm[isurf_true, jsurf_true + 1]) / hy_dtm
                        dd = (alt_dtm[isurf_true, jsurf_true] - alt_dtm[isurf_true + 1, jsurf_true] - 
                              alt_dtm[isurf_true, jsurf_true + 1] + alt_dtm[isurf_true + 1, jsurf_true + 1]) / (hx_dtm * hy_dtm)
                        x_dtm = xmin_dtm + float(isurf_true - 1) * hx_dtm
                        dx = x_true - x_dtm
                        y_dtm = ymin_dtm + float(jsurf_true - 1) * hy_dtm
                        dy = y_true - y_dtm
                        hsurf_dtm = aa + bb * dx + cc * dy + dd * dx * dy
                        
                        if hsurf_dtm >= z_true:
                            xsurf_true = x_true
                            ysurf_true = y_true
                            hsurf_true = z_true
                            dxh_dtm = bb + dd * dy
                            dyh_dtm = cc + dd * dx
            
                            igsurf_ray = ig
                            dsurf_ray = d_app
                            xsurf_ray = x_app
                            ysurf_ray = y_app
                            hsurf_ray = z_app
                            wghtsurf_ray = 1.0
# autoconverted end
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
                print('     -> X,Y,H_SURF-TRUE:' ,xsurf_true,ysurf_true,hsurf_true)
                print('        I,J_SURF_true :',isurf_true,jsurf_true ,' dxH,dyH :',dxh_dtm,dyh_dtm)
                print('     -> X,Y,H_SURF-RAY:' ,xsurf_ray,ysurf_ray,hsurf_ray)
            #endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
	#endif
#--------------------------------------------------------------
#
#******************************************************************
#**** IF THIS SURFACE POINT IS CORRECT (if WGHTSURF_ray > 0)
#**** THEN COMPARE WITH THE SURFACE POINT DERIVED FROM THE DTM
#******************************************************************
#
        if(hsurf_ray > -900. and wghtsurf_ray > 0.):                    # B
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
      #!!!!      print(' '
      #!!!!      print(' ',1000*ihhmmss+ims_ray
      #!!!!             ,' NO_RADAR:',iradar_ray,' FORE/AFT:',iaftfore
      #!!!!             ,' NO_RAY:',nb_ray(iradar_ray)
      #!!!!      print('    ROTA_RAY:',rota_ray+roll_acft
      #!!!!             ,' EL_HOR:',elhor_ray,' AZ_EAST:',azeast_ray
      #!!!!       print('    DISTMAX:',distmax
      #!!!!       print('    IG_RefMAX:',ig_refmax,' -> REF: max,d,z:'
      #!!!!             ,refmax_ray,d_refmax,z_refmax
      #!!!!       print('    IG_GradMAX:',ig_gradrefmax,' -> GRAD: max,d,z:'
      #!!!!              ,gradrefmax_ray,d_gradrefmax,z_gradrefmax
                print('    -> X,Y,H_SURF-RAY:',xsurf_ray,ysurf_ray,hsurf_ray)
            #endif
      #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      #
      #******************************************************************
      #**** INTERPOLATION OF ALT_DTM(x,y) [READ ON SURF_DTM_* OR CONSTANT]
      #******************************************************************
      #
            if(xsurf_ray > xmin_dtm                                     # C
                and xsurf_ray < xmax_dtm
                and ysurf_ray > ymin_dtm
                and ysurf_ray < ymax_dtm):
                isurf_ray=(xsurf_ray-xmin_dtm)/hx_dtm+1
                jsurf_ray=(ysurf_ray-ymin_dtm)/hy_dtm+1
                aa=alt_dtm(isurf_ray,jsurf_ray)
                bb=(-alt_dtm(isurf_ray,jsurf_ray)
                    +alt_dtm(isurf_ray+1,jsurf_ray))/hx_dtm
                cc=(-alt_dtm(isurf_ray,jsurf_ray)
                    +alt_dtm(isurf_ray,jsurf_ray+1))/hy_dtm
                dd=((+alt_dtm(isurf_ray,jsurf_ray)
                    -alt_dtm(isurf_ray+1,jsurf_ray)
                    -alt_dtm(isurf_ray,jsurf_ray+1)
                    +alt_dtm(isurf_ray+1,jsurf_ray+1))/
                    (hx_dtm*hy_dtm))
                x_dtm=xmin_dtm+float(isurf_ray-1)*hx_dtm
                dx=xsurf_ray-x_dtm
                y_dtm=ymin_dtm+float(jsurf_ray-1)*hy_dtm
                dy=ysurf_ray-y_dtm
                hsurf_dtm=aa+bb*dx+cc*dy+dd*dx*dy
                d_hsurf=hsurf_ray-hsurf_dtm
                dxh_dtm=bb+dd*dy
                dyh_dtm=cc+dd*dx
      #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
                    print('        I,J_SURF_ray :',isurf_ray,jsurf_ray ,' dxH,dyH :',dxh_dtm,dyh_dtm)
                    print('     -> H_SURF-DTM:',hsurf_dtm ,'  =>> D_HSURF :',d_hsurf)
                #endif
      #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      #
      #******************************************************************
      #**** IF ( ABS(HSURF_RADAR-HSURF_DTM) < DHSURF_MAX ) THEN
      #**** !!!! DHSURF_MAX=999. !!!! -> NOT IN USE !!!!
      #******************************************************************
      #
                if(abs(d_hsurf) < dhsurf_max):                         # D
                    ssurfins=ssurfins+wghtsurf_ray
      #
      #******************************************************************
      #**** CASE "DZ_surf"
      #******************************************************************
      #
                    if(kdzsurf == 1):
      #
      #----------------------------------------------------------------------
      #---- ( IF ISIM=1 ) -> SIMULATED DZ_surf FROM dXXX_GUESS
      #----------------------------------------------------------------------
                        if(isim == 1):
                            d_hsurf_dxxx=(-dsurf_ray
                                *(-dcnz_dt+dxh_dtm*dcwe_dt+dyh_dtm*dcsn_dt)
                                 *dtilt_guess*conv
                               -dsurf_ray
                                *(-dcnz_dr+dxh_dtm*dcwe_dr+dyh_dtm*dcsn_dr)
                                 *drota_guess*conv
                               -dsurf_ray
                                *(-dcnz_dp+dxh_dtm*dcwe_dp+dyh_dtm*dcsn_dp)
                                 *dpitch_guess*conv
                               -dsurf_ray
                                *(-dcnz_dh+dxh_dtm*dcwe_dh+dyh_dtm*dcsn_dh)
                                 *dhdg_guess*conv
                               -(-cnz+dxh_dtm*cwe+dyh_dtm*csn)
                                *d_dgate_guess
                               -dxh_dtm*dxwe_guess
                               -dyh_dtm*dysn_guess
                               +dzacft_guess)
            #!!!!            d_hsurf=d_hsurf_dxxx
			#endif
            #----------------------------------------------------------------------
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
                            print('     -> D_HSURF_dXXX :',d_hsurf_dxxx)
                        #endif
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #
            #******************************************************************
            #**** ADD WEIGHTS AND DZ_surf
            #******************************************************************
            #
                        n_dzsurf[iradar_ray]=n_dzsurf[iradar_ray]+1
                        swdzsurf_sweep[iradar_ray] =swdzsurf_sweep[iradar_ray]+wghtsurf_ray
            #
                        dzsurfsweep_mean[iradar_ray] =dzsurfsweep_mean[iradar_ray] +wghtsurf_ray*d_hsurf
                        dzsurfsweep_rms[iradar_ray] =dzsurfsweep_rms[iradar_ray] +wghtsurf_ray*d_hsurf*d_hsurf
            #
                        swdzsurf_tot=swdzsurf_tot+wghtsurf_ray
                        swdzmsurf_tot=swdzmsurf_tot +wghtsurf_ray*d_hsurf
                        swdz2surf_tot=swdz2surf_tot +wghtsurf_ray*d_hsurf*d_hsurf
                        swadzsurf_tot=swadzsurf_tot +wghtsurf_ray*abs(d_hsurf)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #!!!!      print('    -> WGHTSURF_RAY:',wghtsurf_ray,' DZSURF:',d_hsurf
            #!!!!      print('       N_DZSURF:',n_dzsurf(iradar_ray)
            #!!!!             ,' SWDZ,SDZ,SDZvariable_indexes.tilt_fore:',swdzsurf_sweep(iradar_ray)
            #!!!!             ,dzsurfsweep_mean(iradar_ray),dzsurfsweep_rms(iradar_ray)
            #!!!!      print('       !!!! VR,PROJ_ACFTSPD,VCORR_SURF:'
            #!!!!             ,vr(ig_refmax),proj_acftspd,vdop_corr(ig_refmax),' !!!!'
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #
            #******************************************************************
            #**** VALUES OF VAR(1->NVAR) FOR FIELD "DZ_surf"
            #****  - VAR(1->variable_indexes.dhdg) -> [dT_aft,dT_fore,dR_aft,dR_fore,dP,dH] in DEGREES
            #****  - VAR(variable_indexes.rdaft->11) -> [RD_aft,RD_fore,dXwe,dYsn,dZ] in HECTOMETERS
            #****  - VAR(12) -> [dVH] in METER/SECOND
            #******************************************************************
            #
                        if(iaftfore == -1):
                            if(idtiltaft == 1):
                                var[variable_indexes.tilt_aft]=dsurf_ray *(-dcnz_dt+dxh_dtm*dcwe_dt+dyh_dtm*dcsn_dt) *conv
                            else:
                                var[variable_indexes.tilt_aft1]=0.
                                xmat_dzsurf[variable_indexes.tilt_aft,variable_indexes.tilt_aft]=xmat_dzsurf[variable_indexes.tilt_aft,variable_indexes.tilt_aft]+wghtsurf_ray
                            var[variable_indexes.tilt_fore]=0.
                        else:
                            var[variable_indexes.tilt_aft]=0.
                            if(idtiltfore == 1):
                                 var[variable_indexes.tilt_fore]=dsurf_ray *(-dcnz_dt+dxh_dtm*dcwe_dt+dyh_dtm*dcsn_dt) *conv
                            else:
                                 var[variable_indexes.tilt_fore]=0.
                                 xmat_dzsurf[variable_indexes.tilt_fore,variable_indexes.tilt_fore]=xmat_dzsurf[variable_indexes.tilt_fore,variable_indexes.tilt_fore]+wghtsurf_ray
            #
                        if(iaftfore == -1):
                            if(idrotaaft == 1):
                                var[variable_indexes.rot_aft]=dsurf_ray *(-dcnz_dr+dxh_dtm*dcwe_dr+dyh_dtm*dcsn_dr) *conv
                            else:
                                var[variable_indexes.rot_aft]=0.
                                xmat_dzsurf[variable_indexes.rot_aft,variable_indexes.rot_aft]=xmat_dzsurf[variable_indexes.rot_aft,variable_indexes.rot_aft]+wghtsurf_ray
                            var[variable_indexes.rot_fore]=0.
                        else:
                            var[variable_indexes.rot_aft]=0.
                            if(idrotafore == 1):
                                var[variable_indexes.rot_fore]=dsurf_ray *(-dcnz_dr+dxh_dtm*dcwe_dr+dyh_dtm*dcsn_dr) *conv
                            else:
                                var[variable_indexes.rot_fore]=0.
                                xmat_dzsurf[variable_indexes.rot_fore,variable_indexes.rot_fore]=xmat_dzsurf[variable_indexes.tilt_fore,variable_indexes.tilt_fore]+wghtsurf_ray
            #
                        if(idpitch == 1):
                            var[variable_indexes.pitch]=dsurf_ray *(-dcnz_dp+dxh_dtm*dcwe_dp+dyh_dtm*dcsn_dp) *conv
                        else:
                            var[variable_indexes.pitch]=0.
                            xmat_dzsurf[variable_indexes.pitch,variable_indexes.pitch]=xmat_dzsurf[variable_indexes.rot_fore,variable_indexes.rot_fore]+wghtsurf_ray
            #
                        if(idhdg == 1):
                            var[variable_indexes.dhdg]=dsurf_ray *(+dxh_dtm*dcwe_dh+dyh_dtm*dcsn_dh) *conv 
                        else:
                            var[variable_indexes.dhdg]=0.
                            xmat_dzsurf[variable_indexes.dhdg,variable_indexes.dhdg]=xmat_dzsurf[variable_indexes.pitch,variable_indexes.pitch]+wghtsurf_ray
            #
                        if(iaftfore == -1):
                            if(irdaft == 1):
                                 var[variable_indexes.rdaft]=(-cnz+dxh_dtm*cwe+dyh_dtm*csn) *0.1
                            else:
                                 var[variable_indexes.rdaft]=0.
                                 xmat_dzsurf[variable_indexes.rdaft,variable_indexes.rdaft]=xmat_dzsurf[variable_indexes.dhdg,variable_indexes.dhdg]+wghtsurf_ray
                            var[variable_indexes.rdfore]=0.
                        else:
                            var[variable_indexes.rdaft]=0.
                            if(irdfore == 1):
                                var[variable_indexes.rdfore]=(-cnz+dxh_dtm*cwe+dyh_dtm*csn) *0.1
                            else:
                                var[variable_indexes.rdfore]=0.
                                xmat_dzsurf[variable_indexes.rdfore,variable_indexes.rdfore]=xmat_dzsurf[variable_indexes.rdfore,variable_indexes.rdfore]+wghtsurf_ray
            #
                        if(idxwe == 1):
                            var[variable_indexes.dxwe]=dxh_dtm*0.1
                        else:
                            var[variable_indexes.dxwe]=0.
                            xmat_dzsurf[variable_indexes.dxwe,variable_indexes.dxwe]=xmat_dzsurf[variable_indexes.dxwe,variable_indexes.dxwe]+wghtsurf_ray
            #
                        if(idysn == 1):
                            var[variable_indexes.dysn]=dyh_dtm*0.1
                        else:
                            var[variable_indexes.dysn]=0.
                            xmat_dzsurf[variable_indexes.dysn,variable_indexes.index_dysn]=xmat_dzsurf[variable_indexes.index_dysn,variable_indexes.index_dysn]+wghtsurf_ray
            #
                        if(idzacft == 1):
                            var[variable_indexes.dzacft]=-0.1
                        else:
                            var[variable_indexes.dzacft]=0.
                            xmat_dzsurf[variable_indexes.dzacft,variable_indexes.index_dzacft]=xmat_dzsurf[variable_indexes.index_dzacft,variable_indexes.index_dzacft]+wghtsurf_ray
            #
                        var[variable_indexes.index_dvh]=0.
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #!!!!      print('    VAR_DZSURF(1->12):',(var(i),i=1,12)
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #
            #******************************************************************
            #**** ADD TO XMAT_dzsurf(1->NVAR,1->NVAR) AND VECT_dzsurf(1->NVAR)
            #******************************************************************
            #
                        for i in range(nvar):
                            for j in range(nvar):
                                xmat_dzsurf[i,j]=xmat_dzsurf[i,j] +wghtsurf_ray*var[i]*var[j]
                                vect_dzsurf[i]=vect_dzsurf[i] +wghtsurf_ray*var[i]*d_hsurf
            #
            #******************************************************************
            #**** ADD TO COVARIANCE MATRIX FOR FIELD "DZ_surf"
            #******************************************************************
            #
                        for i in range(nvar):
                            rms_var_zsurf[i]=rms_var_zsurf[i] +wghtsurf_ray*var[i]*var[i]
                            for j in range(nvar):
                               corr_var[i,j]=corr_var[i,j] +wghtsurf_ray*var[i]*var[j]
            #
            #******************************************************************
            #**** CASE "DZ_surf" ONLY -> D_VH CANNOT BE CALCULATED
            #******************************************************************
            #
                        if(rw_vsurf+rw_dvinsitu <= 0.):
                            xmat_vsurf[variable_indexes.dvh,variable_indexes.dvh]=xmat_vsurf[variable_indexes.dvh,variable_indexes.dvh]+wghtsurf_ray
            #
            #******************************************************************
            #**** CASE "FLAT SURFACE" -> D_HEADING,D_XWE,D_YSN CANNOT BE OBTAINED
            #******************************************************************
            #
                            if(altdtm_min >= altdtm_max):
                                    xmat_vsurf[variable_indexes.dhdg,variable_indexes.dhdg]=xmat_vsurf[variable_indexes.dhdg,variable_indexes.dhdg]+wghtsurf_ray
                                    xmat_vsurf[variable_indexes.dxwe,variable_indexes.dxwe]=xmat_vsurf[variable_indexes.dxwe,variable_indexes.dxwe]+wghtsurf_ray
                                    xmat_vsurf[variable_indexes.dysn,variable_indexes.dysn]=xmat_vsurf[variable_indexes.dysn,variable_indexes.dysn]+wghtsurf_ray
                            #endif
                        #endif
            #
            #******************************************************************
            #**** ARRAYS FOR "SIS_EL_*" FILE #variable_indexes.pitch0
            #******************************************************************
            #
                        #zs_rot[iradar_ray,n_dzsurf[iradar_ray]]=rota_ray
                        #zs_el[iradar_ray,n_dzsurf[iradar_ray]]=elhor_ray
                        #zs_az[iradar_ray,n_dzsurf[iradar_ray]]=azeast_ray
                        #zs_dsurf[iradar_ray,n_dzsurf[iradar_ray]]=dsurf_ray
                        #zs_dhor[iradar_ray,n_dzsurf[iradar_ray]] =side*dsurf_ray*celh
                        #zs_zsurf[iradar_ray,n_dzsurf[iradar_ray]]=hsurf_ray
                        #zs_hsurf[iradar_ray,n_dzsurf[iradar_ray]]=hsurf_dtm
            #
		    #endif     !!  of !! if(kdzsurf == 1):
      #
      #******************************************************************
      #**** (if IWRISURFILE=1)
      #**** WEIGHTED SUM FOR ALT_SURF(x,y)
      #**** TO BE WRITTEN ON "SURF_EL_*" FILE #variable_indexes.rot_aft0
      #******************************************************************
      #
                    if(iwrisurfile == 1):
                        iwrisurfile1()
      #
      #******************************************************************
      #**** CASE "VDOP_surf"
      #******************************************************************
      #
                    if(kvsurf == 1 and acftspd_hor > 0.):                       # E
      #
                        if(vdop_corr[ig_refmax] > -900. or isim == 1):
                            vdopsurf_ray=vdop_corr[ig_refmax]
                            if(abs(vdopsurf_ray) <= 1.):
                                nb1=nb1+1
                            if(abs(vdopsurf_ray) <= 2. and abs(vdopsurf_ray) > 1.):
                                nb2=nb2+1
                            if(abs(vdopsurf_ray) <= 3. and abs(vdopsurf_ray) > 2.):
                                nb3=nb3+1
                            if(abs(vdopsurf_ray) <= 4. and abs(vdopsurf_ray) > 3.):
                                nb4=nb4+1
                            if(abs(vdopsurf_ray) <= 5. and abs(vdopsurf_ray) > 4.):
                                nb5=nb5+1
                            if(abs(vdopsurf_ray) <= 6. and abs(vdopsurf_ray) > 5.):
                                nb6=nb6+1
                            if(abs(vdopsurf_ray) <= 7. and abs(vdopsurf_ray) > 6.):
                                nb7=nb7+1
                            if(abs(vdopsurf_ray) <= 8. and abs(vdopsurf_ray) > 7.):
                                nb8=nb8+1
                            if(abs(vdopsurf_ray) > 8.):
                                nsup=nsup+1
      
      #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      #
      #--------------------------------------------------------------
      #---- ( IF ISIM=1 ) -> SIMULATED VDOPSURF_RAY FROM dXXX_GUESS
      #--------------------------------------------------------------
      #
                            if(isim == 1):
                                vdopsurf_ray=(-(-acftspd_we_true*dcwe_dt_true
                                    -acftspd_sn_true*dcsn_dt_true
                                    -acftspd_nz*dcnz_dt_true)
                                    *dtilt_guess*conv
                                    -(-acftspd_we_true*dcwe_dr_true
                                    -acftspd_sn_true*dcsn_dr_true
                                    -acftspd_nz*dcnz_dr_true)
                                    *drota_guess*conv
                                    -(-acftspd_we_true*dcwe_dp_true
                                    -acftspd_sn_true*dcsn_dp_true
                                    -acftspd_nz*dcnz_dp_true)
                                    *dpitch_guess*conv
                                    -(-acftspd_we_true*dcwe_dh_true
                                    -acftspd_sn_true*dcsn_dh_true
                                    -acftspd_nz*dcnz_dh_true)
                                    *dhdg_guess*conv
                                    -(-cwe_true*duacft_dv_true
                                    -csn_true*dvacft_dv_true)*dvh_guess)
                            #endif
      #--------------------------------------------------------------
      #
      #                     if(abs(vdopsurf_ray) < vdopsurf_max):
                                print('vdopsurf_ray =',vdopsurf_ray)
                                if(abs(vdopsurf_ray) < 6.):
                  #
                  #******************************************************************
                  #**** ADD WEIGHTS AND VDOP_surf
                  #******************************************************************
                  #
                                    n_vsurf[iradar_ray]=n_vsurf[iradar_ray]+1
                                    swvsurf_sweep[iradar_ray] =swvsurf_sweep[iradar_ray]+wghtsurf_ray
                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                    if( nb_ray[iradar_ray] == 10*(nb_ray[iradar_ray]/10) ):
                                        print('     -> VDOPSURF_RAY :',vdopsurf_ray)
                  #!!!!                 print('        SWVSURF_SWEEP(',iradar_ray,') :',swvsurf_sweep[iradar_ray)
                                    #endif
                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  #
                                    vsurfsweep_mean[iradar_ray] =vsurfsweep_mean[iradar_ray] +wghtsurf_ray*vdopsurf_ray
                                    vsurfsweep_rms[iradar_ray] =vsurfsweep_rms[iradar_ray] +wghtsurf_ray*vdopsurf_ray*vdopsurf_ray
                  #
                                    swvsurf_tot=swvsurf_tot+wghtsurf_ray
                                    swvmsurf_tot=swvmsurf_tot +wghtsurf_ray*vdopsurf_ray
                                    swv2surf_tot=swv2surf_tot +wghtsurf_ray*vdopsurf_ray*vdopsurf_ray
                                    swavsurf_tot=swavsurf_tot +wghtsurf_ray*abs(vdopsurf_ray)
                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  #!!!!      print('    -> WGHTSURF_RAY:',wghtsurf_ray,' VSURF:',vdopsurf_ray
                  #!!!!      print('        N_VSURF:',n_vsurf(iradar_ray)
                  #!!!!             ,' SWV,SV,SVvariable_indexes.tilt_fore:',swvsurf_sweep(iradar_ray)
                  #!!!!             ,vsurfsweep_mean(iradar_ray),vsurfsweep_rms(iradar_ray)
                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  #
                  #******************************************************************
                  #**** VALUES OF VAR(1->NVAR) FOR FIELD "V_surf"
                  #****  - VAR(1->variable_indexes.dhdg) -> [dT_aft,dT_fore,dR_aft,dR_fore,dP,dH] in DEGREES
                  #****  - VAR(variable_indexes.rdaft->11) -> [RD_aft,RD_fore,dXwe,dYsn,dZ] in HECTOMETERS
                  #****  - VAR(12) -> [dVH] in METER/SECOND
                  #******************************************************************
                  #
                                    if(iaftfore == -1):
                                        if(idtiltaft == 1):
                                            var[1]=(-acftspd_we*dcwe_dt-acftspd_sn*dcsn_dt -acftspd_nz*dcnz_dt) *conv
                                        else:
                                            var[1]=0.
                                            xmat_vsurf[1,1]=xmat_vsurf[1,1]+wghtsurf_ray
                                        #endif
                                        var[variable_indexes.tilt_fore]=0.
                                    else:
                                        var[1]=0.
                                        if(idtiltfore == 1):
                                            var[variable_indexes.tilt_fore]=(-acftspd_we*dcwe_dt-acftspd_sn*dcsn_dt -acftspd_nz*dcnz_dt) *conv
                                        else:
                                            var[variable_indexes.tilt_fore]=0.
                                            xmat_vsurf[variable_indexes.tilt_fore,variable_indexes.tilt_fore]=xmat_vsurf[variable_indexes.tilt_fore,variable_indexes.tilt_fore]+wghtsurf_ray
                                        #endif
                                    #endif
                  #
                                    if(iaftfore == -1):
                                        if(idrotaaft == 1):
                                            var[variable_indexes.rot_aft]=(-acftspd_we*dcwe_dr-acftspd_sn*dcsn_dr -acftspd_nz*dcnz_dr) *conv
                                        else:
                                            var[variable_indexes.rot_aft]=0.
                                            xmat_vsurf[variable_indexes.rot_aft,variable_indexes.rot_aft]=xmat_vsurf[variable_indexes.rot_aft,variable_indexes.rot_aft]+wghtsurf_ray
                                        #endif
                                        var[variable_indexes.rot_fore]=0.
                                    else:
                                        var[variable_indexes.rot_aft]=0.
                                        if(idrotafore == 1):
                                            var[variable_indexes.rot_fore]=(-acftspd_we*dcwe_dr-acftspd_sn*dcsn_dr -acftspd_nz*dcnz_dr) *conv
                                        else:
                                            var[variable_indexes.rot_fore]=0.
                                            xmat_vsurf[variable_indexes.rot_fore,variable_indexes.rot_fore]=xmat_vsurf[variable_indexes.rot_fore,variable_indexes.rot_fore]+wghtsurf_ray
                                        #endif
                                    #endif
                  #
                                    if(idpitch == 1):
                                        var[variable_indexes.pitch]=(-acftspd_we*dcwe_dp-acftspd_sn*dcsn_dp -acftspd_nz*dcnz_dp) *conv
                                    else:
                                        var[variable_indexes.pitch]=0.
                                        xmat_vsurf[variable_indexes.pitch,variable_indexes.pitch]=xmat_vsurf[variable_indexes.pitch,variable_indexes.pitch]+wghtsurf_ray
                                    #endif
                  #
                                    if(idhdg == 1):
                                        var[variable_indexes.dhdg]=(-acftspd_we*dcwe_dh -acftspd_sn*dcsn_dh) *conv
                                    else:
                                        var[variable_indexes.dhdg]=0.
                                        xmat_vsurf[variable_indexes.dhdg,variable_indexes.dhdg]=xmat_vsurf[variable_indexes.dhdg,variable_indexes.dhdg]+wghtsurf_ray
                                    #endif
                  #
                                    var[variable_indexes.rdaft]=0.
                                    var[variable_indexes.rdfore]=0.
                                    var[variable_indexes.dxwe]=0.
                                    var[variable_indexes.dysn]=0.
                                    var[variable_indexes.dzacft]=0.
                #
                                    if(idvh == 1):
                                        var[variable_indexes.dvh]=-duacft_dv*cwe-dvacft_dv*csn
                                    else:
                                        var[variable_indexes.dvh]=0.
                                        xmat_vsurf[variable_indexes.dvh,variable_indexes.dvh]=xmat_vsurf[variable_indexes.dvh,variable_indexes.dvh]+wghtsurf_ray
                                    #endif
                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  #!!!!      print('    VAR_VSURF(1->12):',(var(i),i=1,12)
                  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                  #
                  #******************************************************************
                  #**** ADD TO XMAT_vsurf(1->NVAR,1->NVAR) AND VECT_vsurf(1->NVAR)
                  #******************************************************************
                  #
                                    for i in range(nvar):
                                        for j in range(nvar):
                                            xmat_vsurf[i,j]=xmat_vsurf[i,j] +wghtsurf_ray*var[i]*var[j]
                                            vect_vsurf[i]=vect_vsurf[i] +wghtsurf_ray*var[i]*vdopsurf_ray
                                    #enddo
                  #
                  #******************************************************************
                  #**** ADD TO COVARIANCE MATRIX FOR FIELD "VDOP_surf"
                  #******************************************************************
                  #
                                    for i in range(nvar):
                                       rms_var_vsurf[i]=rms_var_vsurf[i] +wghtsurf_ray*var[i]*var[i]
                                       for j in range(nvar):
                                          corr_var[i,j]=corr_var[i,j] +wghtsurf_ray*var[i]*var[j]
                                    #enddo
                  #
                  #******************************************************************
                  #**** CASE "VDOP_surf" and/or "DVDOP_insitu" ONLY :
                  #**** -> RGE-DLY_aft,RGE-DLY_aft,D_XWE,D_YSN,D_ZACFT CANNOT BE CALCULATED
                  #******************************************************************
                  #
                                    if(rw_dzsurf <= 0.):
                                        for ij in range(variable_indexes.rdaft,11):  # NOTE! these indexes are Fortran base 1; TODO convert to base 0
                                            xmat_vsurf[ij,ij]=xmat_vsurf[ij,ij] +wghtsurf_ray
                                    #endif
                  #
                  #******************************************************************
                  #**** ARRAYS FOR "SIS_EL_*" FILE #variable_indexes.pitch0
                  #******************************************************************
                  #
                                    vs_dhor[iradar_ray,n_vsurf[iradar_ray]] =side*dsurf_ray*celh
                                    vs_vdopsurf[iradar_ray,n_vsurf[iradar_ray]] =vdopsurf_ray
                                else:  #!!  of  !! if(abs(vdopsurf_ray) < vdopsurf_max) !!
                                    ndismiss_vdopsurf[iradar_ray] =ndismiss_vdopsurf[iradar_ray]+1
                                #endif  !! of !! if(abs(vdopsurf_ray) < vdopsurf_max) !!
                            else:  #!!  of  !!  if(vdop_corr(ig_refmax) > -900.) !!
                                ndismiss_vdopcorr[iradar_ray] =ndismiss_vdopcorr[iradar_ray]+1
                            #endif  !!  of  !!  if(vdop_corr(ig_refmax) > -900.) !!
                        else:  #!!  of  !! if(kvsurf == 1 and acftspd_hor > 0.)  !!    E
                            if(acftspd_hor <= 0.):
                                ndismiss_vhacft[iradar_ray] =ndismiss_vhacft[iradar_ray]+1
                        #endif  !!  of  !! if(kvsurf == 1 and acftspd_hor > 0.)  !!    E
                #endif  !!  of  !! if(abs(d_hsurf) < dhsurf_max)  !!  GOOD INDENT  D
            #endif  !!  of  !!  if(xsurf_ray > xmin_dtm ... )  !!           C
        #endif  !!  of  !!  if(hsurf_ray > -999. and wghtsurf_ray > 0.)  !! B
    #endif  !!  of  !!  if(kdzsurf+kvsurf >= 1 ... )  !! A 
#
    return n_dzsurf 
