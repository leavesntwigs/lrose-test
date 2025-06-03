# end of sweep
import numpy as np

def iend_ge_1(iradar_ray,
    rota_prev,
    nb_ray,
    ):

    rota_end = np.full(2, -999, dtype=np.float32)

    rota_end[iradar_ray]=rota_prev[iradar_ray]
    #
    #******************************************************************
    #**** MEAN VALUES FOR THE PAST SWEEP
    #******************************************************************
    #
    if nb_ray[iradar_ray] > 1 :
        xp[iradar_ray]=float(nb_ray[iradar_ray])
  #
        tilt_mean=stilt[iradar_ray]/xp[iradar_ray]
        tilt_rms=sqrt(amax1(0.,(xp[iradar_ray]*stilt2[iradar_ray]
                     -stilt[iradar_ray]*stilt[iradar_ray])
                      /(xp[iradar_ray]*(xp[iradar_ray]-1))))
  #
        nb_sweep[iradar_ray]=nb_sweep[iradar_ray]+1
        xacft_mean=sxa[iradar_ray]/xp[iradar_ray]
        yacft_mean=sya[iradar_ray]/xp[iradar_ray]
        zacft_mean=sza[iradar_ray]/xp[iradar_ray]
        acfthspd_mean=sacfthspd[iradar_ray]/xp[iradar_ray]
        time_ks_mean=stime[iradar_ray]/xp[iradar_ray]
        ihmean=time_ks_mean/3.6
        immean=(time_ks_mean-3.6*float(ihmean))/0.06
        ismean=(time_ks_mean-3.6*float(ihmean)
    	         -0.06*float(immean))/0.001
        ihms=10000*ihmean+100*immean+ismean
        hdg_mean=atan2( ssc[iradar_ray]/xp[iradar_ray]
                       ,scc[iradar_ray]/xp[iradar_ray])/conv
        uacft_mean=su_acft[iradar_ray]/xp_acft[iradar_ray]
        vacft_mean=sv_acft[iradar_ray]/xp_acft[iradar_ray]
        wacft_mean=sw_acft[iradar_ray]/xp_acft[iradar_ray]
        uwind_mean=su_wind[iradar_ray]/xp_wind[iradar_ray]
        vwind_mean=sv_wind[iradar_ray]/xp_wind[iradar_ray]
        wwind_mean=sw_wind[iradar_ray]/xp_wind[iradar_ray]
        #
        #******************************************************************
        #**** CONTROL PRINTS FOR THE PAST SWEEP
        #******************************************************************
        #
        print_past_sweep()
        #
        #******************************************************************
        #**** WRITE THE RESULTS FOR THE PAST SWEEP
        #**** ON THE "SIS_EL_*" FILE #50
        #******************************************************************
        #
        #**** SWEEP HEADER
        #
        f50.write(iaftfore,nb_sweep[iradar_ray]
                 ,xacft_mean,yacft_mean,zacft_mean
                 ,time_ks_mean,hdg_mean
                 ,u_mean,v_mean,w_mean)
        #
        #******************************************************************
        #**** SWEEP DATA: DZ_surf
        #******************************************************************
        #
        print(' ')
        if (kdzsurf == 1 and n_dzsurf[iradar_ray] > 0 ):
            f50.write(n_dzsurf[iradar_ray])
            n=1
            f50.write(zs_rot[iradar_ray,n],
                    zs_el[iradar_ray,n],zs_az[iradar_ray,n],
                    zs_dsurf[iradar_ray,n],zs_dhor[iradar_ray,n],
                    zs_zsurf[iradar_ray,n],zs_hsurf[iradar_ray,n],
                    n_dzsurf[iradar_ray])
      #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      #!!!!      print(' ')
      #!!!!      print(' SIS_* -> NPTS_Zsurf:',n_dzsurf[iradar_ray])
      #!!!!      print(' [ ROT - DH - Z_surf - H_surf ]')
      #!!!!      do n=1,n_dzsurf[iradar_ray]
      #!!!!         print(zs_rot[iradar_ray,n],zs_dhor[iradar_ray,n]
      #!!!!                ,zs_zsurf[iradar_ray,n],zs_hsurf[iradar_ray,n])
      #!!!!      enddo
      #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            f50.write(0)
        #
        #******************************************************************
        #**** SWEEP DATA: VDOP_surf
        #******************************************************************
        #
        if(kvsurf == 1 and n_vsurf[iradar_ray] > 0):
            f50.write(n_vsurf[iradar_ray])
            n=1
            f50.write((vs_dhor[iradar_ray,n],vs_vdopsurf[iradar_ray,n]
                    ,n_vsurf[iradar_ray]))
  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  #!!!!  print(' '
  #!!!!  print(' SIS_* -> NPTS_VDOP_surf:',n_vsurf[iradar_ray]
  #!!!!  print(' [ DH - VDOP_surf ]'
  #!!!!  do n=1,n_vsurf[iradar_ray]
  #!!!!     print(vs_dhor[iradar_ray,n],vs_vdopsurf[iradar_ray,n]
  #!!!!  enddo
  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            f50.write(0)
        #
        #******************************************************************
        #**** SWEEP DATA: DVDOP_insitu
        #******************************************************************
        #
        if(kdvinsitu == 1 and n_dvinsitu[iradar_ray] > 0):
            f50.write(n_dvinsitu[iradar_ray])
            n=1
            f50.write(( vi_dhor[iradar_ray,n]
                    ,vi_vdop[iradar_ray,n],vi_vinsitu[iradar_ray,n]
                    ,n_dvinsitu[iradar_ray]))
  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  #!!!!  print(' '
  #!!!!  print(' NPTS_Vinsitu:',n_dvinsitu[iradar_ray]
  #!!!!  print(' DH - Vdop - Vinsitu'
  #!!!!  do n=1,n_dvinsitu[iradar_ray]
  #!!!!     print(vi_dhor[iradar_ray,n]
  #!!!!            ,vi_vdop[iradar_ray,n],vi_vinsitu[iradar_ray,n]
  #!!!!  enddo
  #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            f50.write(0)
  #
      #endif    !!  of  !! if(nb_ray[iradar_ray] > 1):  !!

    return rota_end
