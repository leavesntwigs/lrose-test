#
#******************************************************************
#**** GENERATE THE SURFACE ARRAYS
#******************************************************************
#

def generate_surface_arrays(
   directory,
   idtmfile,
   dtm_file
   ):

   print(' '
   print(' GENERATE THE SURFACE ARRAYS'
   print(' '
#
   if(idtmfile == 1):
#
#------------------------------------------------------------------
#---- FROM THE INPUT "SURF_DTM_*" FILE
#------------------------------------------------------------------
#
    print(' IFIDTM=1 -> READ THE "SURF_DTM_*" FILE #20 :'
            ,directory//'/'//dtm_file
    with file.open(directory//'/'//dtm_file, 'w'
        # ,form='formatted',status='unknown'
        ) as f20:
       try:
          data = f20.readline().strip().split()
          yymmdd_dtm,suff_dtm ,iolat_dtm,iolon_dtm ,iha_dtm,ima_dtm,isa_dtm ,iua_dtm,iva_dtm ,ihms_dtm,ixmin_dtm,iymin_dtm,nul1 ,nx_dtm,ny_dtm,nul2,ihx_dtm,ihy_dtm,nul3 = map(float,data)
  # 111format(a12,a4,22i7)

       except EOFError:
          iopen = 0  # jump here on EOF
          if ifile == nfile:
             lastfile = 1
             break
          else:
             ifile += 1
# CAI START
       print('nx_dtm,ny_dtm,ixmin_dtm',nx_dtm,ny_dtm,ixmin_dtm)
# CAI STOP
       olat_dtm=float(iolat_dtm)/1000.
       olon_dtm=float(iolon_dtm)/1000.
       xlatm_surf=(olat_dtm+orig_lat)/2.
       deg_lon=deg_lon0*cos(conv*xlatm_surf)
       dx_dtm=(olon_dtm-orig_lon)*deg_lon
       dy_dtm=(olat_dtm-orig_lat)*deg_lat
       xmin_dtm=float(ixmin_dtm)/1000.+dx_dtm
       ymin_dtm=float(iymin_dtm)/1000.+dy_dtm
       hx_dtm=float(ihx_dtm)/1000.
       hy_dtm=float(ihy_dtm)/1000.
       xmax_dtm=xmin_dtm+float(nx_dtm-1)*hx_dtm
       ymax_dtm=ymin_dtm+float(ny_dtm-1)*hy_dtm
       print(' X_DTM_min,max :',xmin_dtm,xmax_dtm)
       print(' Y_DTM_min,max :',ymin_dtm,ymax_dtm)
       print(' Hx,y_DTM :',hx_dtm,hy_dtm)
       print(' Nx,y_DTM:',nx_dtm,ny_dtm)
       saltdtm=0.
       altdtm_mean=0.
       altdtm_min=+999.
       altdtm_max=-999.
# TODO: figure out this read statement
#        for jdtm in range(1,ny_dtm+1):
# 	  f20.read(333)(itab(idtm),idtm=1,nx_dtm)
 #  # 333   format(500i6)
# 	  for idtm in range(1,nx_dtm+1):
# 	     if(itab(idtm) > -1000):
# 		h_dtm=float(itab(idtm))/1000.
# 		alt_dtm(idtm,jdtm)=h_dtm
# 	        saltdtm=saltdtm+1.
# 	        altdtm_mean=altdtm_mean+h_dtm
# 	        altdtm_min=amin1(altdtm_min,h_dtm)
# 	        altdtm_max=amax1(altdtm_max,h_dtm)
 #             else:
# 		alt_dtm(idtm,jdtm)=-999.
       altdtm_mean=altdtm_mean/amax1(1.,saltdtm)
   return
