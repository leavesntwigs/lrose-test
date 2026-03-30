
def initialize_sweep_beginning(iradar_ray,
    nb_ray,
    stilt,
    stilt2,
    rota_prev,
    rota_start,
    rota_end,
    sxa,
    sya,
    sza,
    sacfthspd,
    stime,
    ssc,
    scc,
    xp_acft,
    su_acft,
    sv_acft,
    sw_acft,
    xp_wind,
    su_wind,
    sv_wind,
    sw_wind,
    n_dvinsitu,
    n_dzsurf,
    n_vsurf,
    ndismiss_vhacft,
    ndismiss_vdopcorr,
    ndismiss_vdopsurf,
    zs_rot,
    zs_el,
    zs_az,
    zs_dsurf,
    zs_dhor,
    zs_zsurf,
    zs_hsurf,
    vs_dhor,
    vs_vdopsurf,
    #vi_dhor,
    #vi_vdop,
    #vi_vinsitu,
    swdzsurf_sweep,
    dzsurfsweep_mean,
    dzsurfsweep_rms,
    swvsurf_sweep,
    vsurfsweep_mean,
    vsurfsweep_rms,
    nsurf_wri,
    swinsitu_sweep,
    dvinsitusweep_mean,
    dvinsitusweep_rms,
    s_vpv,
    sv_vpv,
    svv_vpv,
    ):

    #
    #******************************************************************
    #**** INITIALIZATIONS AT THE BEGINNING OF A SWEEP (if IEND=1)
    #******************************************************************
    #
    # istart_sweep[iradar_ray]=0 # not used
    # xsweeps[iradar_ray]=xsweeps[iradar_ray]+1. # moved to cns_eldo_cai
    nb_ray[iradar_ray]=0
    stilt[iradar_ray]=0.
    stilt2[iradar_ray]=0.
    rota_prev[iradar_ray]=-999.
    rota_start[iradar_ray]=-999.
    rota_end[iradar_ray]=-999.
    sxa[iradar_ray]=0.
    sya[iradar_ray]=0.
    sza[iradar_ray]=0.
    sacfthspd[iradar_ray]=0.
    stime[iradar_ray]=0.
    ssc[iradar_ray]=0.
    scc[iradar_ray]=0.
    xp_acft[iradar_ray]=0.
    su_acft[iradar_ray]=0.
    sv_acft[iradar_ray]=0.
    sw_acft[iradar_ray]=0.
    xp_wind[iradar_ray]=0.
    su_wind[iradar_ray]=0.
    sv_wind[iradar_ray]=0.
    sw_wind[iradar_ray]=0.
    n_dvinsitu[iradar_ray]=0
    n_dzsurf[iradar_ray]=0
    n_vsurf[iradar_ray]=0
    ndismiss_vhacft[iradar_ray]=0
    ndismiss_vdopcorr[iradar_ray]=0
    ndismiss_vdopsurf[iradar_ray]=0
#

    #do n=1,500
    for n in range(500):
        zs_rot[iradar_ray,n]=0.
        zs_el[iradar_ray,n]=0.
        zs_az[iradar_ray,n]=0.
        zs_dsurf[iradar_ray,n]=0.
        zs_dhor[iradar_ray,n]=0.
        zs_zsurf[iradar_ray,n]=0.
        zs_hsurf[iradar_ray,n]=0.
        vs_dhor[iradar_ray,n]=0.
        vs_vdopsurf[iradar_ray,n]=0.
        #vi_dhor[iradar_ray,n]=0.
        #vi_vdop[iradar_ray,n]=0.
        #vi_vinsitu[iradar_ray,n]=0.
    # enddo
#
    swdzsurf_sweep[iradar_ray]=0.
    dzsurfsweep_mean[iradar_ray]=0.
    dzsurfsweep_rms[iradar_ray]=0.
    swvsurf_sweep[iradar_ray]=0.
    vsurfsweep_mean[iradar_ray]=0.
    vsurfsweep_rms[iradar_ray]=0.
    nsurf_wri[iradar_ray]=0
    swinsitu_sweep[iradar_ray]=0.
    dvinsitusweep_mean[iradar_ray]=0.
    dvinsitusweep_rms[iradar_ray]=0.
          # do jgd=1,2
    for jgd in range(2):
        s_vpv[iradar_ray,jgd]=0.
        sv_vpv[iradar_ray,jgd]=0.
        # svv_vpv[iradar_ray,jgd]=0. # causes TypeError: 'NoneType' object does not support item assignment
    # enddo

