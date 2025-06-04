
import ze_actions
import azel
import numpy as np

# may not need this file
def control_for_end_of_all_text_files(kdzsurf, kvsurf, kdvinsitu, iradar_ray, nb_ray,
iaftfore, isim, ipr_alt,
    time_ks,
corr_azest, corr_elhor, corr_dist, corr_lon, corr_lat, corr_p_alt, corr_r_alt, corr_vwe_av, corr_vsn_av, corr_cap, corr_roul, corr_tang, corr_derv, corr_rota, corr_incl, nb_portes, d_porte, ih_rdl,     im_rdl, is_rdl, ims_rdl, ih_rdl1, im_rdl1, is_rdl1, ims_rdl1, azest_rdl, elhor_rdl, lat_av, lon_av, p_alt_av, r_alt_av, cap_av, roul_av, tang_av, derv_av, rota_rdl, incl_rdl, vwe_av, vsn_av, vnz_av, vent_we, vent_sn, vent_nz,
    dtiltaft_guess,
    drotaaft_guess,
    dtiltfore_guess,
    drotafore_guess,
    dhdg_guess,
    dpitch_guess,
    rdfore_guess,
    rdaft_guess, 
    dxwe_guess,
    dysn_guess,
    dzacft_guess,
    orig_lat, orig_lon,
    dmax0,
    nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins,
):

    continue_processing = True
    # TODO these are constants, they should not be repeated here, figure out a better way to get this info here.
    conv=3.14159/180.
    MAXPORT=2000
    deg_lon0=111.32
    deg_lat=111.13


    dgate_corr = np.zeros(MAXPORT, dtype=np.float32)
    dgate_true = np.zeros(MAXPORT, dtype=np.float32)
    stilt = np.zeros(2, dtype=np.float32)
    stilt2 = np.zeros(2, dtype=np.float32)
    rota_start = np.full(2, -999, dtype=np.float32)
    rota_end = np.full(2, -999, dtype=np.float32)
    sxa = np.zeros(2, dtype=np.float32)
    sya = np.zeros(2, dtype=np.float32)
    sza = np.zeros(2, dtype=np.float32)
    stime = np.zeros(2, dtype=np.float32)
    ssc = np.zeros(2, dtype=np.float32)
    scc = np.zeros(2, dtype=np.float32)

#
#************************************************************************
#**** NEW RAY
#************************************************************************
#
    nb_ray[iradar_ray]=nb_ray[iradar_ray]+1
#
#******************************************************************
#**** FRENCH->ENGLISH TRANSLATIONS
#**** CONSTANT CORRECTIONS READ ON THE TAPE
#******************************************************************
#
    azeast_ray=azest_rdl+corr_azest[iradar_ray]	# Mod Oliv
    elhor_ray=elhor_rdl+corr_elhor[iradar_ray]	#
    xlon_acft=lon_av+corr_lon[iradar_ray]		#
    xlat_acft=lat_av+corr_lat[iradar_ray]		#
    p_alt_acft=p_alt_av+corr_p_alt[iradar_ray]	#
    r_alt_acft=r_alt_av+corr_r_alt[iradar_ray]	#
    roll_acft=roul_av+corr_roul[iradar_ray]		#
    pitch_acft=tang_av+corr_tang[iradar_ray]		#
    hdg_acft=cap_av+corr_cap[iradar_ray]		#
    drift_acft=derv_av+corr_derv[iradar_ray]		#
    rota_ray=rota_rdl+corr_rota[iradar_ray]		#
    tilt_ray=incl_rdl+corr_incl[iradar_ray]		#
    wind_we=vent_we
    wind_sn=vent_sn
    wind_nz=vent_nz
    acftspd_we=vwe_av
    acftspd_sn=vsn_av
    acftspd_nz=vnz_av
#	print('IRADAR_RAY= ',iradar_ray
#	print('AZ,EL,Xlon,Xlat,Palt,Roll,Pitch,Hdg,Drift,Rota
#             ,Tilt= ',corr_azest[iradar_ray], corr_elhor[iradar_ray]
#             , corr_lon[iradar_ray],corr_lat[iradar_ray]
#             ,corr_p_alt[iradar_ray],corr_roul[iradar_ray]
#             ,corr_tang[iradar_ray],corr_cap[iradar_ray]
#             ,corr_derv[iradar_ray],corr_rota[iradar_ray]
#             , corr_incl[iradar_ray]
#
    # dtilt_guess, drota_quess = earth_rel_angles(iaftfore)
    #******************************************************************
    #**** EARTH-RELATIVE ANGLES AND
    #**** PARAMETERS FOR THE ANALYSIS
    #******************************************************************
    #
    if(iaftfore == -1):
        dtilt_guess=dtiltaft_guess
        drota_guess=drotaaft_guess
    else:
        dtilt_guess=dtiltfore_guess
        drota_guess=drotafore_guess

#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE NAVIGATION WITHOUT dXXX_GUESS
#------------------------------------------------------------------
    if isim == 1:
        caze_true,
        saze_true,
        celh_true,
        selh_true,
        dcwe_dt_true,
        dcwe_dr_true,
        dcwe_dp_true,
        dcwe_dh_true,
        dcsn_dt_true,
        dcsn_dr_true,
        dcsn_dp_true,
        dcsn_dh_true,
        dcnz_dt_true,
        dcnz_dr_true,
        dcnz_dp_true,
        dcnz_dh_true,
        duacft_dv_true,
        dvacft_dv_true = isim_equals_1()
#------------------------------------------------------------------
    cosinang = {}
    cxa = 0.0 
    cya = 0.0 
    cza = 0.0 
    cwe = 0.0 
    csn = 0.0 
    cnz = 0.0 
    azeast_ray,elhor_ray,cxa, cya, cza, cwe, csn, cnz, cosinang = azel.azel( rota_ray+drota_guess+roll_acft
              ,tilt_ray+dtilt_guess
              ,hdg_acft+dhdg_guess,drift_acft
              ,pitch_acft+dpitch_guess
              ,azeast_ray,elhor_ray
              ,cxa,cya,cza,cwe,csn,cnz,
              cosinang)
    if(np.sin(conv*(rota_ray+drota_guess+roll_acft)) < 0.):
        side=-1.
        ilr=1
    else:
        side=+1.
        ilr=2
#
    crr = cosinang['crr']
    srr = cosinang['srr']
    cti = cosinang['cti']
    sti = cosinang['sti']
    chdg = cosinang['chdg']
    shdg = cosinang['shdg']
    cdri = cosinang['cdri']
    sdri = cosinang['sdri']
    cpit = cosinang['cpit']
    spit = cosinang['spit']
    caze = cosinang['caze']
    saze = cosinang['saze']
    celh = cosinang['celh']
    selh = cosinang['selh']
    dcwe_dt=+crr*sti*spit*shdg-srr*sti*chdg+cti*cpit*shdg
    dcwe_dr=+srr*cti*spit*shdg+crr*cti*chdg
    dcwe_dp=-crr*cti*cpit*shdg-sti*spit*shdg
    dcwe_dh=-crr*cti*spit*chdg-srr*cti*shdg+sti*cpit*chdg
#
    dcsn_dt=+crr*sti*spit*chdg+srr*sti*shdg+cti*cpit*chdg
    dcsn_dr=+srr*cti*spit*chdg-crr*cti*shdg
    dcsn_dp=-crr*cti*cpit*chdg-sti*spit*chdg
    dcsn_dh=+crr*cti*spit*shdg-srr*cti*chdg-sti*cpit*shdg
#
    dcnz_dt=-crr*sti*cpit+cti*spit
    dcnz_dr=-srr*cti*cpit
    dcnz_dp=-crr*cti*spit+sti*cpit
    dcnz_dh=0.
#
    duacft_dv=+shdg*cdri+chdg*sdri
    dvacft_dv=+chdg*cdri-shdg*sdri
#
#******************************************************************
#**** DISTANCE OF THE RANGE GATES
#******************************************************************
#
    if(iaftfore == -1):
        d_dgate_guess=rdaft_guess
    else:
        d_dgate_guess=rdfore_guess
    ngates=nb_portes
#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE RANGE GATES WITHOUT dXXX_GUESS
#------------------------------------------------------------------
    if(isim == 1):
        for ig in range(ngates):
# CAI-START
#        dgate_true[ig]=d_porte(iradar*MAXPORT+ig)
#                           +corr_dist(iradar+1)
# It seems that the above code is wrong, since iradar has not been assigned values yet,
# therefore, following are the new code:
             dgate_true[ig]=d_porte[(iradar_ray-1)*MAXPORT+ig]+corr_dist[iradar_ray]
#------------------------------------------------------------------
    for ig in range(ngates):
        dgate_corr[ig]=d_porte[(iradar_ray-1)*MAXPORT+ig]+corr_dist[iradar_ray]+d_dgate_guess
    ddg=dgate_corr[1]-dgate_corr[0]
#
#******************************************************************
#**** AIRCRAFT POSITION, (PRESSURE OR RADAR) ALTITUDE AND HEADING
#******************************************************************
#
    ylat=(xlat_acft+orig_lat)/2.
    deg_lon=deg_lon0*np.cos(conv*ylat)
#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE AIRCRAFT POSITION WITHOUT dXXX_GUESS
#------------------------------------------------------------------
    if(isim == 1):
        x_acft_true=(xlon_acft-orig_lon)*deg_lon
        y_acft_true=(xlat_acft-orig_lat)*deg_lat
        if(ipr_alt == 1):
            z_acft_true=p_alt_acft
        else:
            z_acft_true=r_alt_acft
#------------------------------------------------------------------
    x_acft=(xlon_acft-orig_lon)*deg_lon+dxwe_guess
    y_acft=(xlat_acft-orig_lat)*deg_lat+dysn_guess
    if(ipr_alt == 1):
        z_acft=p_alt_acft+dzacft_guess
    else:
        z_acft=r_alt_acft+dzacft_guess

    #******************************************************************
    #**** ADD TO THE MEAN PARAMETERS FOR THE CURRENT SWEEP
    #******************************************************************
    #
    stilt[iradar_ray]=stilt[iradar_ray]+tilt_ray
    stilt2[iradar_ray]=stilt2[iradar_ray]+tilt_ray*tilt_ray
    if(nb_ray[iradar_ray] == 1): 
        rota_start[iradar_ray]=rota_ray
    sxa[iradar_ray]=sxa[iradar_ray]+x_acft
    sya[iradar_ray]=sya[iradar_ray]+y_acft
    sza[iradar_ray]=sza[iradar_ray]+z_acft
    stime[iradar_ray]=stime[iradar_ray]+time_ks
    ssc[iradar_ray]=ssc[iradar_ray]+shdg
    scc[iradar_ray]=scc[iradar_ray]+chdg
    dmax=np.min((dmax0,dgate_corr[ngates])) # substitute for fortran amin1
#
#******************************************************************
#**** AIRCRAFT SPEED
#******************************************************************
#
    if(    (abs(acftspd_we) < 10. and abs(acftspd_sn) < 10.)
       or (abs(acftspd_we) > 200. or abs(acftspd_sn) > 200.) ):
        print(" #!!! NO_RAY:", nb_ray, " -> U,V,W_acft:", acftspd_we, acftspd_sn, acftspd_nz, " #!!!")
        # go to 1 # read next file; replace with continue and move inside while loop
        continue_processing = False
        return continue_processing, # swdzmsurf_tot
    # endif
#----------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE AIRCRAFT SPEED WITHOUT dXXX_GUESS
#----------------------------------------------------------------------
    if(isim == 1):
      acftspd_we_true=acftspd_we
      acftspd_sn_true=acftspd_sn
    endif
#----------------------------------------------------------------------
    acftspd_we=acftspd_we+duacft_dv*dvh_guess
    acftspd_sn=acftspd_sn+dvacft_dv*dvh_guess
    acftspd_hor=sqrt(acftspd_we*acftspd_we+acftspd_sn*acftspd_sn)
    sacfthspd[iradar_ray]=sacfthspd[iradar_ray]+acftspd_hor
    xp_acft[iradar_ray]=xp_acft[iradar_ray]+1.
    su_acft[iradar_ray]=su_acft[iradar_ray]+acftspd_we
    sv_acft[iradar_ray]=sv_acft[iradar_ray]+acftspd_sn
    sw_acft[iradar_ray]=sw_acft[iradar_ray]+acftspd_nz
    proj_acftspd=acftspd_we*cwe+acftspd_sn*csn+acftspd_nz*cnz
#
#******************************************************************
#**** FLIGHT-LEVEL WIND
#******************************************************************
#
#----------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE AIRCRAFT SPEED WITHOUT dXXX_GUESS
#----------------------------------------------------------------------
    if isim == 1:
      proj_wind=wind_we*cwe_true+wind_sn*csn_true+wind_nz*cnz_true
      wa_we_true=wind_we-acftspd_we_true
      wa_sn_true=wind_sn-acftspd_sn_true
    #endif
#----------------------------------------------------------------------
    if(    (abs(wind_we) <= 0. and abs(wind_sn) <= 0.)
        or (abs(wind_we) > 100. or abs(wind_sn) > 100.)):
      print(' #!!! NO_RAY:',nb_ray[iradar_ray],' -> Uwe,Vsn_wind:'
             ,wind_we,wind_sn,' #!!!')
      # go to 1 # read next file #  replace with continue and move inside while loop
      continue_processing = False
      return continue_processing, # swdzmsurf_tot
    # endif
    if(abs(wind_nz) <= 0. or abs(wind_nz) > 50.):
      wind_nz=0.
    xp_wind[iradar_ray]=xp_wind[iradar_ray]+1.
    su_wind[iradar_ray]=su_wind[iradar_ray]+wind_we
    sv_wind[iradar_ray]=sv_wind[iradar_ray]+wind_sn
    sw_wind[iradar_ray]=sw_wind[iradar_ray]+wind_nz
    proj_wind=wind_we*cwe+wind_sn*csn+wind_nz*cnz
    wa_we=wind_we-acftspd_we
    wa_sn=wind_sn-acftspd_sn
    wa_nz=wind_nz-acftspd_nz
#
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##!!! ELIMINATION OF GATES CONTAMINATED WITH GROUND-CLUTTER
##!!! ONLY FOR TOGA-COARE DATA !!!!
##!!!-> aft_SWEEP : dROTA=+6 deg
##!!!-> fore_SWEEP : dROTA=+3 deg)
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
##!!!
##!!!   if(tilt_ray < -15.):
##!!!     rota_sidelobe=rota_ray+roll_acft+6.
##!!!   elif(tilt_ray > 15.):
##!!!     rota_sidelobe=rota_ray+roll_acft+3.
##!!!   endif
##!!!    if(a_don <= 1993 and cos(conv*rota_sidelobe) < 0.):
##!!!     dmax_sidelobe=(z_min-z_acft)/cos(conv*rota_sidelobe)
##!!!     dmax=amin1(dmax0,dmax_sidelobe)
##!!!   else
##!!!     dmax=dmax0
##!!!   endif
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins = ze_actions.ze_actions(
        nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins)

#
#******************************************************************
#**** STORE FOR NEXT RAY
#******************************************************************
#
    istart_sweep[iradar_ray]=1
    swp_prev[iradar_ray]=swp[iradar_ray]
    vnyq_prev=vnyq
    rota_prev[iradar_ray]=rota_ray
    tilt_prev=tilt_ray
#
    # return continue_processing, # swdzmsurf_tot
    return nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins

