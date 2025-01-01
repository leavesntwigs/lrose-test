#******************************************************************
#**** (if IWRISURFILE=1)
#**** WEIGHTED SUM FOR ALT_SURF(x,y)
#**** TO BE WRITTEN ON "SURF_EL_*" FILE #30
#******************************************************************
#
              if(iwrisurfile == 1):
#
	        if(     xsurf_ray > xmin_wrisurf-hxy_wrisurf
                    and xsurf_ray < xmax_wrisurf+hxy_wrisurf
                    and ysurf_ray > ymin_wrisurf-hxy_wrisurf
                    and ysurf_ray < ymax_wrisurf+hxy_wrisurf
                    and hsurf_ray > zsurfrad_min
                    and hsurf_ray < zsurfrad_max):
#
 	          nsurf_wri(iradar_ray)=nsurf_wri(iradar_ray)+1
	          i_wrisurf=(xsurf_ray-xmin_wrisurf)/hxy_wrisurf+1
	          if(xsurf_ray < xmin_wrisurf)i_wrisurf=i_wrisurf-1
	          j_wrisurf=(ysurf_ray-ymin_wrisurf)/hxy_wrisurf+1
	          if(ysurf_ray < ymin_wrisurf)j_wrisurf=j_wrisurf-1
#
	          do ii=max0(i_wrisurf,1)
                        ,min0(i_wrisurf+1,nx_wrisurf)
	             xi=xmin_wrisurf+float(ii-1)*hxy_wrisurf
	             dx=(xsurf_ray-xi)/hxy_wrisurf
	             do jj=max0(j_wrisurf,1)
                           ,min0(j_wrisurf+1,ny_wrisurf)
		        yj=ymin_wrisurf+float(jj-1)*hxy_wrisurf
		        dy=(ysurf_ray-yj)/hxy_wrisurf
		        d2=dx*dx+dy*dy
		        wghtsurf_wri=wghtsurf_ray*((4.-d2)/(4.+d2))
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print('      II,JJ:',ii,jj,' WGTHSURF_ray,wri:'
#!!!!             ,wghtsurf_ray,wghtsurf_wri
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		        swdzsurf_wri(ii,jj)=swdzsurf_wri(ii,jj)
                                           +wghtsurf_wri
	                sw_or_altsurf_wri(ii,jj)
                                          =sw_or_altsurf_wri(ii,jj)
                                           +wghtsurf_wri*hsurf_ray
 	             enddo
	          enddo
#
	        endif
#
	      endif
#
