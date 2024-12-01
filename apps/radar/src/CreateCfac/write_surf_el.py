            print(' '
  	    print(' WRITES THE "SURF_EL_*" FILE #30 :'
              ,directory(1:ndir)//'/'//wrisurfile(1:nsf)
            print(' INTERPOLATION OF THE RADAR-DERIVED SURFACE MAP'
	    call inter(swdzsurf_wri,sw_or_altsurf_wri
                       ,nx_wrisurf,ny_wrisurf,nxysurfmax)
	    nwrisurf_ok=0
	    do j_wrisurf=1,ny_wrisurf
	       do i_wrisurf=1,nx_wrisurf
	  	  if(abs(sw_or_altsurf_wri(i_wrisurf,j_wrisurf))
                      < 10.):
		    ialtsurf_wri(i_wrisurf)
                     =(1000.*sw_or_altsurf_wri(i_wrisurf,j_wrisurf))
		    nwrisurf_ok=nwrisurf_ok+1
		  else
	 	    ialtsurf_wri(i_wrisurf)=-9999
		  endif
	       enddo
	       write(30,222)(ialtsurf_wri(i_wrisurf)
                             ,i_wrisurf=1,nx_wrisurf)
 222           format(500i6)
	    enddo
	    print(' -> NPTS WRITTEN ON THE "SURF_EL_*" FILE #30'
                   ,nwrisurf_ok
	    close(30)
	  endif
