
def print_past_sweep(
          ihms,
          iradar_ray,
          iaftfore,
          nb_sweep,
          xacft_mean,
          yacft_mean,zacft_mean,
          hdg_mean,
uacft_mean,vacft_mean,wacft_mean,
uwind_mean,vwind_mean,wwind_mean,
nb_ray,
tilt_mean,tilt_rms,
rota_start,
rota_end,
nref_ok,
ndop_ok,
kdzsurf,
swdzsurf_sweep,
...  # think about how to pass this info.
          
          ):
#
#******************************************************************
#**** CONTROL PRINTS FOR THE PAST SWEEP
#******************************************************************
#
 	  print(' ')
	  print(' ')
	  print(' *******************************************')
 	  print(' **** CONTROL PRINTS FOR THE PAST SWEEP ****')
	  print(' *******************************************')
 	  print(' ')
	  print(' HHMMSS :',ihms)
          print(' RADAR(aft=1,fore=2) :',iradar_ray)
          print(' SWEEP(aft=-1,fore=+1) :',iaftfore
                 ,' NO_SWEEP(this program) :',nb_sweep(iradar_ray)
                 ,'      [ on tape :',swp(iradar_ray),' ]')
          print(' X_we/OLON,Y_sn/OLAT,Z_acft :'
                 ,xacft_mean,yacft_mean,zacft_mean)
          print(' HEADING :',hdg_mean)
	  print(' U,V,W_acft :',uacft_mean,vacft_mean,wacft_mean)
	  print(' U,V,W_insitu :',uwind_mean,vwind_mean,wwind_mean)
          print(' -> NB_RAYS_THIS_SWEEP :',nb_ray(iradar_ray))
          print(' -> TILT_mean,rms :',tilt_mean,tilt_rms)
	  print(' -> ROTA_start,end :',rota_start(iradar_ray))
           	                        ,rota_end(iradar_ray))
          print(' ')
          print(' -> NREF_OK:',nref_ok(iradar_ray))
                 ,'    NDOP_OK:',ndop_ok(iradar_ray))
          print(' ')
#
	  if(kdzsurf == 1):
	    if(swdzsurf_sweep(iradar_ray) > 0.):
	      bias_dzsurf=dzsurfsweep_mean(iradar_ray)
                          /swdzsurf_sweep(iradar_ray)
	      stdv_dzsurf=sqrt(  swdzsurf_sweep(iradar_ray)
                                *dzsurfsweep_rms(iradar_ray)
                               - dzsurfsweep_mean(iradar_ray)
                                *dzsurfsweep_mean(iradar_ray))
                          /swdzsurf_sweep(iradar_ray)
	      print(' -> dZHSURF_npts,swghts,mean,stdv :'
                     ,n_dzsurf(iradar_ray),swdzsurf_sweep(iradar_ray)
                     ,bias_dzsurf,stdv_dzsurf)
              if(iwrisurfile == 1)
                print('     [ NPTS_SURF FOR SURF_EL_*:'
                       ,nsurf_wri(iradar_ray),' ]')
            else
	      print(' !!!! NPTS_dZHSURF :',n_dzsurf(iradar_ray),' !!!!')
            endif
          endif
#
	  if(kvsurf == 1):
	    if(swvsurf_sweep(iradar_ray) > 0.):
	      bias_vsurf=vsurfsweep_mean(iradar_ray)
                          /swvsurf_sweep(iradar_ray)
	      stdv_vsurf=sqrt(  swvsurf_sweep(iradar_ray)
                                *vsurfsweep_rms(iradar_ray)
                               - vsurfsweep_mean(iradar_ray)
                                *vsurfsweep_mean(iradar_ray))
                          /swvsurf_sweep(iradar_ray)
	      print(' -> VSURF_npts,swghts,mean,stdv :'
                     ,n_vsurf(iradar_ray),swvsurf_sweep(iradar_ray)
                     ,bias_vsurf,stdv_vsurf)
            else
	      print(' !!!! NPTS_VSURF :',n_vsurf(iradar_ray),' !!!!')
	      print(' !!!! Ndismissed_VACFT,VDOPCORR,VDOPSURF:'
                     ,ndismiss_vhacft(iradar_ray)
                     ,ndismiss_vdopcorr(iradar_ray)
                     ,ndismiss_vdopsurf(iradar_ray),' !!!!')
            endif
          endif
#
	  if(kdvinsitu == 1):
	    if(swinsitu_sweep(iradar_ray) > 0.):
	      bias_dvinsitu=dvinsitusweep_mean(iradar_ray)
                            /swinsitu_sweep(iradar_ray)
	      stdv_dvinsitu=sqrt(  swinsitu_sweep(iradar_ray)
                                  *dvinsitusweep_rms(iradar_ray)
                                 - dvinsitusweep_mean(iradar_ray)
                                  *dvinsitusweep_mean(iradar_ray))
                          /swinsitu_sweep(iradar_ray)
	      print(' -> dVINSITU_npts,swghts,mean,stdv :'
                     ,n_dvinsitu(iradar_ray),swinsitu_sweep(iradar_ray)
                     ,bias_dvinsitu,stdv_dvinsitu)
              print('     -> LEFT_swghts,mean,stdv:'
                     ,s_vpv(iradar_ray,1)
                     ,sv_vpv(iradar_ray,1)
                      /amax1(0.001,s_vpv(iradar_ray,1))
                     ,sqrt( s_vpv(iradar_ray,1)*svv_vpv(iradar_ray,1)
                           -sv_vpv(iradar_ray,1)*sv_vpv(iradar_ray,1))
                      /amax1(0.001,s_vpv(iradar_ray,1)))
              print('     -> RIGHT_swghts,mean,stdv:'
                     ,s_vpv(iradar_ray,2)
                     ,sv_vpv(iradar_ray,2)
                      /amax1(0.001,s_vpv(iradar_ray,2))
                     ,sqrt( s_vpv(iradar_ray,2)*svv_vpv(iradar_ray,2)
                           -sv_vpv(iradar_ray,2)*sv_vpv(iradar_ray,2))
                      /amax1(0.001,s_vpv(iradar_ray,2)))
            else
	      print(' !!!! NPTS_VINSITU :'
                     ,n_dvinsitu(iradar_ray),' !!!!')
            endif
          endif
          print(' ')
	  print(' *******************************************')
 	  print(' ')
 	  print(' ')
#
