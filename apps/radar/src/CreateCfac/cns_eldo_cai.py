#****
#******************************************************************
#**** THIS PROGRAM CALCULATES NAVIGATIONAL ERRORS:
#****
#****    D_TILT_aft, D_TILT_fore, D_ROLL, D_PITCH, D_HEADING
#****    RANGE_DELAY_aft, RANGE_DELAY_fore, D_Xwe, D_Ysn, D_Z
#****    D_VH_acft
#****
#**** FROM COMPARISONS BETWEEN:
#****
#****    - RADAR-DERIVED SURFACE AND DIGITAL TERRAIN MAP
#****     (or CONSTANT GROUND LEVEL);
#****    - DOPPLER VELOCITY AT SURFACE LEVEL AND ZERO;
#****    - DOPPLER  VELOCITY AT LOW-ELEVATION CLOSE TO THE AIRCRAFT
#****      AND THE PROJECTION OF THE FLIGHT-LEVEL (IN SITU) WIND;
#****
#**** DIFFERENT OPTIONS ARE AVAILABLE (see DATA_cns FILE)
#****
#****
#**** THIS PROGRAM ALSO PRODUCES A "RADAR-DERIVED" SURFACE MAP
#**** (FILE "SURF_EL_*" HAS THE SAME STRUCTURE AS FILE "SURF_DTM_*")
#****
#****
#******************************************************************
#**** Author: Frank ROUX (LA, UPS-CNRS, Toulouse), March 2000  ****
#******************************************************************
#     Modified by Huaqing Cai at NCAR, April, 2010
#******************************************************************
#   Converted to Python by Brenda Javornik at NCAR, November, 2024
#******************************************************************

import numpy as np
import read_input_parameters

def cns_eldo():
    nvar=12
    nxysurfmax=200
#
#       parameter (nvar=12,nxysurfmax=200)
#
#     include '/home/users/rouf/SOURCES/ELDO/mes_parametres'
# CAI-START: Inlcude the parameter file mes_parametres directly below
#      instead of using the include function above
#******************************************************************
#**** FICHIER 'mes_parametres'
#******************************************************************
#

    MAXRAD=2,MAXFREQ=5,MAXPARM=10,MAXPORT=2000
    MAXFREQRAD=MAXFREQ*MAXPARM
    MAXPARAD=MAXRAD*MAXPARM
    MAXPORAD=MAXRAD*MAXPORT
    MAXPARIS=256

# Variable for reading text files

        int ntimes    # Number of times rays were collected --- Number of rays
        int nranges   # Number of range gates per time  --- Number of gates for each ray
        int nsweep    # Sweep number in each netcdf file; Used to identify different sweep

        int*4 counter  # Ray number


        int start_year,start_mon,start_day
        int start_hour,start_min,start_sec


!  Scaler variable for coccrection factors

        float azimuth_correction
        float elevation_correction
        float range_correction
        float longitude_correction
        float latitude_correction
        float pressure_altitude_correction
        float radar_altitude_correction
        float ew_gound_speed_correction
        float ns_ground_speed_correction
        float vertical_velocity_correction
        float heading_correction
        float roll_correction
        float pitch_correction
        float drift_correction
        float rotation_correction
        float tilt_correction

! Variable for cfac files
        float tilt_corr_aft
        float tilt_corr_fore
        float rot_angle_corr_aft
        float rot_angle_corr_fore
        float pitch_corr_cfac
        float drift_corr_cfac
        float range_delay_corr_aft
        float range_delay_corr_fore
        float pressure_alt_corr
        float ew_gndspd_corr

! Scaler variable for each ray

        int sweep_number

        float*8  time
        float azimuth
        float elevation
        float*8 latitude
        float*8 longitude
        float*8 altitude
        float altitude_agl
        float heading
        float roll
        float pitch
        float drift
        float rotation
        float tilt
        float ew_velocity
        float ns_velocity
        float vertical_velocity
        float ew_wind
        float ns_wind
        float vertical_wind

! One dimensional array of DBZ, VR, SW, NCP, etc

        float range(MAXPORT)
        float ZE(MAXPORT),NCP(MAXPORT),VR(MAXPORT),SW(MAXPORT)
        float VS(MAXPORT),VL(MAXPORT),VG(MAXPORT),VU(MAXPORT)

! Variables for input file list
        CHARACTER(len=80) infilename
        int  nfile,ifile,lastfile     ! total number of netcdf text file   file number
        int iopen

# Variables declarations previous in Franks' common block, which has been deleted

# From COMMON /CSPD_OU_CELV/
      integer*4 nb_portes
      float d_porte(MAXPORAD)

# From COMMON /CFAC/
#
      float corr_azest(MAXRAD),corr_elhor(MAXRAD),corr_dist(MAXRAD)
          ,corr_lon(MAXRAD),corr_lat(MAXRAD)
          ,corr_p_alt(MAXRAD),corr_r_alt(MAXRAD)
          ,corr_vwe_av(MAXRAD),corr_vsn_av(MAXRAD)
          ,corr_vnz_av(MAXRAD)
          ,corr_cap(MAXRAD),corr_roul(MAXRAD)
          ,corr_tang(MAXRAD),corr_derv(MAXRAD)
          ,corr_rota(MAXRAD),corr_incl(MAXRAD)

# From COMMON /RYIB/
#
      integer*2 ih_rdl,im_rdl,is_rdl,ims_rdl
      integer*4 num_swp,j_julien,etat_rdl,no_rdl
      float azest_rdl,elhor_rdl,puiscre_em,vit_bal_rdl

# From COMMON /ASIB/ ************************************************
#
      float*8  lon_av,lat_av,p_alt_av,r_alt_av
      float    vwe_av,vsn_av,vnz_av
          ,cap_av,roul_av,tang_av,derv_av
          ,rota_rdl,incl_rdl
          ,vent_we,vent_sn,vent_nz
          ,chg_cap,chg_tang

# CAI-STOP
#
      float*4  dgate_corr(MAXPORT),dgate_true(MAXPORT)
             ,vdop_corr(MAXPORT)
             ,xms(9),xml(9)
             ,rota_start(2),rota_end(2),xp(2)
             ,ssc(2),scc(2)
             ,sxa(2),sya(2),sza(2)
             ,sacfthspd(2),stime(2)
             ,xp_acft(2),su_acft(2),sv_acft(2),sw_acft(2)
             ,su_wind(2),sv_wind(2),sw_wind(2),xp_wind(2)
             ,stilt(2),stilt2(2),xsweeps(2)
             ,rota_prev(2)
             ,swdzsurf_sweep(2),dzsurfsweep_mean(2)
             ,dzsurfsweep_rms(2)
             ,swvsurf_sweep(2),vsurfsweep_mean(2),vsurfsweep_rms(2)
             ,swinsitu_sweep(2),dvinsitusweep_mean(2)
             ,dvinsitusweep_rms(2)
             ,var(nvar),xmat(nvar,nvar),vect(nvar)
             ,xinv(nvar,nvar),res(nvar)
             ,vect_dzsurf(nvar),xmat_dzsurf(nvar,nvar)
             ,vect_vsurf(nvar),xmat_vsurf(nvar,nvar)
             ,vect_dvinsitu(nvar),xmat_dvinsitu(nvar,nvar)
             ,alt_dtm(nxysurfmax,nxysurfmax)
             ,swdzsurf_wri(nxysurfmax,nxysurfmax)
             ,sw_or_altsurf_wri(nxysurfmax,nxysurfmax)
             ,zs_rot(2,500),zs_el(2,500),zs_az(2,500)
             ,zs_dsurf(2,500),zs_dhor(2,500)
             ,zs_zsurf(2,500)
             ,zs_hsurf(2,500)
             ,vs_dhor(2,500),vs_vdopsurf(2,500)
             ,vi_dhor(2,500),vi_vdop(2,500),vi_vinsitu(2,500)
             ,rms_var_zsurf(nvar),rms_var_vsurf(nvar)
             ,rms_var_vinsitu(nvar)
             ,corr_var(nvar,nvar)
             ,s_vpv(2,2),sv_vpv(2,2),svv_vpv(2,2)
             ,x_vpv(2,2),xv_vpv(2,2),xvv_vpv(2,2)
#
      integer*2 iyymmdd(3),ig_dismiss(15)
#
      integer*4 nb_ray(2),nb_sweep(2)
               ,n_dzsurf(2),n_vsurf(2),n_dvinsitu(2)
               ,nsurf_wri(2)
               ,ndismiss_vhacft(2),ndismiss_vdopcorr(2)
               ,ndismiss_vdopsurf(2)
               ,swp(2),swp_prev(2)
               ,ndop_ok(2),nref_ok(2)
               ,istart_sweep(2)
               ,itab(nxysurfmax),ihms_dtm(6),ialtsurf_wri(nxysurfmax)
#
      character path_abs*18,directory*60,dir_read*60
               ,fich_sis*30
               ,dtm_file*50,fich_cornav*30
               ,wrisurfile*50
               ,yymmdd_dtm*12,suff_dtm*20
               ,yymmdd*12,c_hms_min*7,c_hms_max*7
# CAI START   command line arguments
               ,argu*30
# CAI STOP

#
#     include '/home/users/rouf/SOURCES/ELDO/mes_commons'
#
# CAI-START: This is common block for transfering data from tape to this
#      program, and it will be replaced by read in a text file
#      so that this common block is no longer used
#     include '/home/caihq/navigation/roux_nav/SOURCES-ELDO/mes_commons'
# CAI-STOP
      common/cosinang/crr,srr,cti,sti
                     ,chdg,shdg,cdri,sdri,cpit,spit
                     ,caze,saze,celh,selh
#
# CAI-START
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!! THES VALUES ARE CORRECT FOR IPP1/IPP2=4/5 ONLY !!!!
#     data xms/0.,-10.,+20.,+10.,0.,-10.,-20.,+10.,0./
#     data xml/-8.,-16.,+16.,+8.,0.,-8.,-16.,+16.,+8./
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# CAI-STOP: xml and xms are not used anymore for ELDORA
#
#******************************************************************
#**** CONSTANT PARAMETRES
#******************************************************************
#
      path_abs='/d1/navigation/roux_nav/'
      pipi=6.38319
      deg_lon0=111.32
      deg_lat=111.13
      conv=3.14159/180.
      rayter=6370.
      xncp_min=0.25
      sw_max=5.
      vdop_max=200.
      selh_surf=-0.15
      zacftmin_surf=1.5
      igstart_surf=5
      refsurf_min0=20.
      gradrefsurf_min0=50.
      dhsurf_max=999.
      vdopsurf_max=999.
      dmax_insitu=5.
      xpmin_contray=3.
      dvdop_max=10.
      dvdopinsitu_max=999.
      selhinsitu_max=0.1
      ssurfins_min=1.
#
#******************************************************************
#**** READ THE INPUT PARAMETERS ON FILE "DATA_cns"
#******************************************************************
#
# CAI-START ---- read in command line arguments
      CALL GETARG(1, argu)

      read_input_parameters.read_input_parameters('DATA_cns.txt')

      if(no_lect > 900)go to 3 # stop

      if (idtmfile == 1):
         generate_surface_arrays.generate_surface_arrays(directory,
            idtmfile, dtm_file)
      elif(idtmfile == 0):
#
#------------------------------------------------------------------
#---- FROM ZSURF_CST (read in DATA_cns)
#------------------------------------------------------------------
#
        print(' IFIDTM=0 -> ALT_SURF(i,j)=cst'
               ,' (',zsurf_cst,' )')
        xmin_dtm=xmin_wrisurf
        ymin_dtm=ymin_wrisurf
        hx_dtm=hxy_wrisurf
        hy_dtm=hxy_wrisurf
        nx_dtm=nx_wrisurf
        ny_dtm=ny_wrisurf
	xmax_dtm=xmin_dtm+float(nx_dtm-1)*hx_dtm
	ymax_dtm=ymin_dtm+float(ny_dtm-1)*hy_dtm
        do jdtm=1,ny_dtm
	   do idtm=1,nx_dtm
	      alt_dtm(idtm,jdtm)=zsurf_cst
	   enddo
	enddo
        altdtm_mean=zsurf_cst
	altdtm_min=zsurf_cst
	altdtm_max=zsurf_cst
#
#      endif
      print('     -> NPTS:',int(saltdtm)
             ,' ALTSURF_mean,min,max:',altdtm_mean
             ,altdtm_min,altdtm_max)
      zsurfrad_min=altdtm_min-1.
      zsurfrad_max=altdtm_max+1.
      print(' ')
      print(' -> AUTHORIZED ZSURF_RAD_min,max :'
             ,zsurfrad_min,zsurfrad_max)
#
#******************************************************************
#**** MIN AND MAX TIMES
#******************************************************************
#
      tmin=3.6*float(ih_min)+0.06*float(im_min)
           +0.001*float(is_min)
      tmax=3.6*float(ih_max)+0.06*float(im_max)
           +0.001*float(is_max)
      write(c_hms_min,"(i7)")1000000+ihms_min
      write(c_hms_max,"(i7)")1000000+ihms_max
      write(fich_cornav,"('CORNAV_E_',a6,'_',a6)")
           c_hms_min(2:7),c_hms_max(2:7)
      write(fich_sis,"('SIS_E_',a6,'_',a6)")
           c_hms_min(2:7),c_hms_max(2:7)
#
#******************************************************************
#**** OPEN THE OUPUT "CORNAV_EL_*" FILE #10
#******************************************************************
#
      print(' '
      print(' OPEN "CORNAV_EL_*" FILE #10 :'
               ,directory(1:ndir)//'/'//fich_cornav
      open(10,file=directory(1:ndir)//'/'//fich_cornav
             ,form='formatted',status='unknown')
      write(10,"(' YYYYMMDD : ',a12)")yymmdd
      write(10,"(' HHMMSS_min HHMMSS_max : ',a6,3x,a6,/)")
           c_hms_min(2:7),c_hms_max(2:7)
      write(10,"( ' FIELDS TAKEN INTO ACCOUNT',/
                 ,'  -> REL.WGHT_dZsurf,Vsurf,dVinsitu : ',3f6.3,/)")
           rw_dzsurf,rw_vsurf,rw_dvinsitu
      write(10,"( ' VARIABLES TAKEN INTO ACCOUNT',/
                 ,'  -> D_TILT_AFT,D_TILT_FORE (1/0) : ',2i2,/
                 ,'  -> D_ROTA_AFT,D_ROTA_FORE (1/0) : ',2i2,/
                 ,'  -> D_PITCH,D_HEADING (1/0) : ',2i2,/
                 ,'  -> RANGE_DELAY_AFT,RANGE_DELAY_FORE (1/0) : '
                 ,2i2,/
                 ,'  -> D_XWE,D_YSN,D_ZACFT (1/0) : ',3i2,/
                 ,'  -> D_VHACFT (1/0) : ',i2)")
           idtiltaft,idtiltfore
          ,idrotaaft,idrotafore
          ,idpitch,idhdg
          ,irdaft,irdfore
          ,idxwe,idysn,idzacft
          ,idvh
      if(idtmfile == 1):
        write(10,"(' READS THE SURF_DTM_* FILE :',a50)")
             directory(1:ndir)//'/'//dtm_file(1:ndtmfile)
      else
        write(10,"( ' NO SURF_DTM_* FILE TO READ '
                   ,'-> ALT_SURF(x,y)=CST (',f6.3,')')")
             zsurf_cst
      endif
      if(iwrisurfile == 1):
        write(10,"(' WRITES THE SURF_EL_* FILE :',a50,//)")
             directory(1:ndir)//'/'//wrisurfile(1:nsf)
      else
        write(10,"(' NO SURF_EL_* FILE TO WRITE ',//)")
      endif
#
#******************************************************************
#**** OPEN THE OUTPUT "SIS_EL_*" FILE #50
#******************************************************************
#
      print(' '
      print(' OPEN "SIS_EL_*" FILE #50 :'
             ,directory(1:ndir)//'/'//fich_sis
      open(50,file=directory(1:ndir)//'/'//fich_sis
             ,form='unformatted',status='unknown')
      f50.write(iyymmdd,orig_lon,orig_lat,ihms_min,ihms_max
#
#******************************************************************
#**** INITIALIZATIONS
#******************************************************************
#
      time_prev=-999
      ihms_prev=-999
      do iradar=1,2
         istart_sweep(iradar)=0
         rota_prev(iradar)=-999.
         nb_ray(iradar)=0
         stilt(iradar)=0.
         stilt2(iradar)=0.
         rota_start(iradar)=-999.
         rota_end(iradar)=-999.
         sxa(iradar)=0.
         sya(iradar)=0.
         sza(iradar)=0.
         sacfthspd(iradar)=0.
         stime(iradar)=0.
         ssc(iradar)=0.
         scc(iradar)=0.
         xp_acft(iradar)=0.
         su_acft(iradar)=0.
         sv_acft(iradar)=0.
         sw_acft(iradar)=0.
         xp_wind(iradar)=0.
         su_wind(iradar)=0.
         sv_wind(iradar)=0.
         sw_wind(iradar)=0.
         xsweeps(iradar)=0.
         n_dvinsitu(iradar)=0
         n_dzsurf(iradar)=0
         n_vsurf(iradar)=0
         ndismiss_vhacft(iradar)=0
         ndismiss_vdopcorr(iradar)=0
         ndismiss_vdopsurf(iradar)=0
         swdzsurf_sweep(iradar)=0.
         dzsurfsweep_mean(iradar)=0.
         dzsurfsweep_rms(iradar)=0.
         swvsurf_sweep(iradar)=0.
         vsurfsweep_mean(iradar)=0.
         vsurfsweep_rms(iradar)=0.
         swinsitu_sweep(iradar)=0.
         dvinsitusweep_mean(iradar)=0.
         dvinsitusweep_rms(iradar)=0.
         nsurf_wri(iradar)=0
         nb_sweep(iradar)=0
	 do jgd=1,2
	    s_vpv(iradar,jgd)=0.
	    sv_vpv(iradar,jgd)=0.
	    svv_vpv(iradar,jgd)=0.
	    x_vpv(iradar,jgd)=0.
	    xv_vpv(iradar,jgd)=0.
	    xvv_vpv(iradar,jgd)=0.
	 enddo
      enddo
      ssurfins=0.	! Olivier (r�el)
      swdzsurf_tot=0.
      swdzmsurf_tot=0.
      swdz2surf_tot=0.
      swadzsurf_tot=0.
      do i=1,nvar
        rms_var_zsurf(i)=0.
      enddo
      swvsurf_tot=0.
      swvmsurf_tot=0.
      swv2surf_tot=0.
      swavsurf_tot=0.
      do i=1,nvar
        rms_var_vsurf(i)=0.
      enddo
      swdvinsitu_tot=0.
      swdvminsitu_tot=0.
      swdv2insitu_tot=0.
      swadvinsitu_tot=0.
      do i=1,nvar
        rms_var_vinsitu(i)=0.
      enddo
      do i=1,nvar
        do j=1,nvar
           corr_var(i,j)=0.
        enddo
      enddo
      do i=1,nvar
	 var(i)=0.
	 do j=1,nvar
	    xmat_dzsurf(i,j)=0.
	    xmat_vsurf(i,j)=0.
	    xmat_dvinsitu(i,j)=0.
	    xmat(i,j)=0.
	 enddo
	 vect_dzsurf(i)=0.
	 vect_vsurf(i)=0.
	 vect_dvinsitu(i)=0.
	 vect(i)=0.
	 res(i)=0.
      enddo
      do i_wrisurf=1,nxysurfmax
 	 do j_wrisurf=1,nxysurfmax
	    swdzsurf_wri(i_wrisurf,j_wrisurf)=0.
	    sw_or_altsurf_wri(i_wrisurf,j_wrisurf)=0.
	 enddo
      enddo
      do ig=1,MAXPORT
	 vdop_corr(ig)=-999.
      enddo
      do i=1,2
         do n=1,500
            zs_rot(i,n)=0.
            zs_el(i,n)=0.
            zs_az(i,n)=0.
            zs_dsurf(i,n)=0.
            zs_dhor(i,n)=0.
            zs_zsurf(i,n)=0.
            zs_hsurf(i,n)=0.
            vs_dhor(i,n)=0.
            vs_vdopsurf(i,n)=0.
            vi_dhor(i,n)=0.
            vi_vdop(i,n)=0.
            vi_vinsitu(i,n)=0.
         enddo
      enddo


	nb1=0
	nb2=0
	nb3=0
	nb4=0
	nb5=0
	nb6=0
	nb7=0
	nb8=0
	nsup=0
	nbtotals=0	! Olivier
	nbon=0		! Olivier
	nmauvais=0	! Olivier
#
      if(no_lect == 999)go to 3 # stop
#
#******************************************************************
#*** READ THE ELDORA DATA FROM TEXT FILES CREATED BY ANOTHER PROGRAM
#******************************************************************
#
      print(' '
      print('**************************************'
      print(' READ THE ELDORA DATA FROM TEXT FILES'
      print('**************************************'
      print(' '
# 1   call lit_eldo_2()
# CAI-START
#******************************************************************
#    The subroutine lit_eldo_2() is replaced by the following lines
#    of code, which read in a number of text files ray by ray
#******************************************************************
#      iopen = 0
#      ifile = 1
#      lastfile = 0
#   #  while (ifile < nfile):
#  1   if(iopen  ==  0) : 
#
#        write(infilename,'(i10)') ifile
#        infilename = dir_read(1:ndirr) // '/'
#        // TRIM(ADJUSTL(infilename)) // '.txt'
#        open(55,file=infilename, status='old')
#        iopen = 1
#      endif
#      read(55,101,END=5)counter
#        ,nsweep,NTIMES,NRANGES
#        ,start_year,start_mon,start_day
#        ,start_hour,start_min,start_sec,time
#        ,azimuth,elevation,latitude,longitude,altitude
#        ,altitude_agl,heading,roll,pitch,drift
#        ,rotation,tilt,ew_velocity
#        ,ns_velocity,vertical_velocity,ew_wind,ns_wind
#        ,vertical_wind,azimuth_correction,elevation_correction
#        ,range_correction,longitude_correction,latitude_correction
#        ,pressure_altitude_correction,radar_altitude_correction
#        ,ew_gound_speed_correction,ns_ground_speed_correction
#        ,vertical_velocity_correction,heading_correction
#        ,roll_correction,pitch_correction,drift_correction
#        ,rotation_correction,tilt_correction
#
#      read(55,102,END=5)counter,(range(J),J=1,nranges)
#      read(55,102,END=5)counter,(ZE(J),J=1,nranges)
#      read(55,102,END=5)counter,(NCP(J),J=1,nranges)
#      read(55,102,END=5)counter,(VR(J),J=1,nranges)
#      read(55,102,END=5)counter,(SW(J),J=1,nranges)
# 101  format(I10,2x,50x,3I10,I5,5I3,d20.8,2f10.4,3d20.8,29f10.4)
# 102  format(I10,2000f10.4)
## after successful read
#        goto 6
## When end of file reached
#
#  5     iopen = 0  # jump here on EOF
#        close(55)
#        if(ifile  ==  nfile) :
#           lastfile=1
#           goto 7
#        else
#           ifile = ifile +1
#           goto 1
#        endif
#
#  6     continue

# autoconverted begin 
import numpy as np

iopen = 0
ifile = 1
lastfile = 0

while ifile < nfile:
    if iopen == 0:
        infilename = f"{dir_read[0:ndirr]}/{infile:10d}.txt"
        with open(infilename, 'r') as f:
            iopen = 1

    try:
        data = f.readline().strip().split()
        counter, nsweep, NTIMES, NRANGES, start_year, start_mon, start_day, start_hour, start_min, start_sec, time, azimuth, elevation, latitude, longitude, altitude, altitude_agl, heading, roll, pitch, drift, rotation, tilt, ew_velocity, ns_velocity, vertical_velocity, ew_wind, ns_wind, vertical_wind, azimuth_correction, elevation_correction, range_correction, longitude_correction, latitude_correction, pressure_altitude_correction, radar_altitude_correction, ew_ground_speed_correction, ns_ground_speed_correction, vertical_velocity_correction, heading_correction, roll_correction, pitch_correction, drift_correction, rotation_correction, tilt_correction = map(float, data)

        ranges = np.zeros(nranges)
        ZE = np.zeros(nranges)
        NCP = np.zeros(nranges)
        VR = np.zeros(nranges)
        SW = np.zeros(nranges)

        for J in range(nranges):
            data = f.readline().strip().split()
            ranges[J], ZE[J], NCP[J], VR[J], SW[J] = map(float, data)

    except EOFError:
        iopen = 0  # jump here on EOF
        if ifile == nfile:
            lastfile = 1
            break
        else:
            ifile += 1

# end autoconverted

process ray ...

# ************ Get the ray time *************
        ih_rdl1 = start_hour
        im_rdl1 = start_min
        is_rdl1 = start_sec
        ims_rdl1 = (time-INT(time))*1000

# add to the start seconds by time, which is the elpased time after start time
        is_rdl1 = is_rdl1+INT(time)
# adjusting hh,mm,ss for passing 60 mark, assign to Frank's ray time variables
        ims_rdl = ims_rdl1
        is_rdl = MOD(is_rdl1,60)
        im_rdl1 = im_rdl1+is_rdl1/60
        im_rdl = MOD(im_rdl1, 60)
        ih_rdl1 = ih_rdl1+im_rdl1/60
        ih_rdl = MOD(ih_rdl1, 60)

# Assign the aircraft position/angles to Frank's variables
        azest_rdl = azimuth
        elhor_rdl = elevation
        lat_av = latitude
        lon_av = longitude
        p_alt_av = altitude
        r_alt_av = altitude_agl
        cap_av = heading
        roul_av = roll
        tang_av = pitch
        derv_av = drift
        rota_rdl = rotation
        incl_rdl = tilt
        vwe_av = ew_velocity
        vsn_av = ns_velocity
        vnz_av = vertical_velocity
        vent_we = ew_wind
        vent_sn = ns_wind
        vent_nz = vertical_wind

# Assign  the total number of gates and range of each gates,
#  The aft/fore radar are different
        nb_portes = nranges
        if (tilt  <  0) : !AFT,iradar_ray=1,iaftfore= -1
           do ig = 1, nranges
              d_porte(ig) = range(ig)
           enddo
        elif(tilt  >  0) : #FORE,iradar_ray=2,iaftfore= +1
           do ig = 1, nranges
              d_porte(MAXPORT+ig) = range(ig)  # This change fixed icorrupted infilename
           enddo
        endif
# Assign the swp number read from text file to num_swp
       num_swp = nsweep

# Assign the correction factors to Frank's variable
# NOTE: Here the correction factors are arrays with two elements
# This is different from any other variables

        if (tilt  <  0) :   # AFT, iradar_ray=1,iaftfore= -1
           corr_azest(1) = azimuth_correction
           corr_elhor(1) = elevation_correction
           corr_dist(1) = range_correction
           corr_lon(1) = longitude_correction
           corr_lat(1) = latitude_correction
           corr_p_alt(1) = pressure_altitude_correction
           corr_r_alt(1) = radar_altitude_correction
           corr_vwe_av(1) = ew_gound_speed_correction
           corr_vsn_av(1) = ns_ground_speed_correction
           corr_vnz_av(1) = vertical_velocity_correction
           corr_cap(1) = heading_correction
           corr_roul(1) = roll_correction
           corr_tang(1) = pitch_correction
           corr_derv(1) = drift_correction
           corr_rota(1) = rotation_correction
           corr_incl(1) = tilt_correction
        elif(tilt  >  0) :   ! FORE, iradar_ray=2,iaftfore= +1
           corr_azest(2) = azimuth_correction
           corr_elhor(2) = elevation_correction
           corr_dist(2) = range_correction
           corr_lon(2) = longitude_correction
           corr_lat(2) = latitude_correction
           corr_p_alt(2) = pressure_altitude_correction
           corr_r_alt(2) = radar_altitude_correction
           corr_vwe_av(2) = ew_gound_speed_correction
           corr_vsn_av(2) = ns_ground_speed_correction
           corr_vnz_av(2) = vertical_velocity_correction
           corr_cap(2) = heading_correction
           corr_roul(2) = roll_correction
           corr_tang(2) = pitch_correction
           corr_derv(2) = drift_correction
           corr_rota(2) = rotation_correction
           corr_incl(2) = tilt_correction
        endif
#


# TEST reading of text files
#       print*,'File:',infilename,' Ray:', counter
#           ,' HHMMSS:',ih_rdl,im_rdl,is_rdl,' EL:',elhor_rdl
# TEST-END

#******************************************************************
#**** CONTROL FOR THE END OF THE READING ALL TEXT FILES
#******************************************************************
#
  7   iend=0
      if(ifile == nfile  and  lastfile  == 1):
          iend=2
          print(' '
          print('**** END OF READING ALL TEXT FILES ****'
      endif

# CAI-STOP


#******************************************************************
#**** CONTROL OF CURRENT TIME
#******************************************************************
#
      ih_ray=ih_rdl
      im_ray=im_rdl
      is_ray=is_rdl
      ims_ray=ims_rdl
      ihhmmss=10000*ih_ray+100*im_ray+is_ray
      if(ihhmmss <= 0)go to 1
#
      time_ks=3.6*float(ih_ray)+0.06*float(im_ray)
              +0.001*float(is_ray)+1.e-6*float(ims_ray)
      if(    time_ks-time_prev < -80.
         .or.time_ks-tmin < -80.):
        time_ks=time_ks+86.4
	ihhmmss=ihhmmss+240000
      endif
      time_prev=time_ks
      if(time_ks < tmin):
        if(ihhmmss/10 > ihms_prev):
	  print(' HHMMSS:',ihhmmss,' < HHMMSS_min:',ihms_min
	  ihms_prev=ihhmmss/10
        endif
# CAI-START
        if(iend .ne. 2) go to 1   ! only when end of text file not reached
# CAI-STOP
      endif
      if(time_ks > tmax):
	iend=2
	print(' '
	print(' HHMMSSms:',100*ihhmmss+ims_rdl
               ,' > HHMMSSms_max:',100*ihms_max
      endif
      if(iend == 2)go to 2
#
#******************************************************************
#**** CONTROL OF LAT, LON, P_ALT AND R_ALT
#******************************************************************
#
      if(    abs(lat_av) < 0.001
         .or.abs(lon_av) < 0.001
         .or.(     abs(p_alt_av) < 0.001
               and abs(r_alt_av) < 0.001))go to 1

#	print('P_ALT_AV= ',p_alt_av
#
#******************************************************************
#**** RADAR IDENTIFICATION THROUGH TILT_RAY (=INCL_RDL)
#****  -> AFT : IRADAR_RAY=1, IAFTFORE=-1
#****  -> FORE : IRADAR_RAY=2, IAFTFORE=+1
#**********************F********************************************
#
      tilt_ray=incl_rdl
      if(abs(tilt_ray) < 15.):
        go to 1
      elif(abs(tilt_ray) < 30.):
        if(tilt_ray < -15.):
          iradar_ray=1
          iaftfore=-1
          swp(iradar_ray)=num_swp
        endif
        if(tilt_ray > +15.):
          iradar_ray=2
          iaftfore=+1
          swp(iradar_ray)=num_swp
        endif
      else
	go to 1
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print(' /////////////////////////////////////////////////'
#!!!!      print(' '
#!!!!      print(' /////////////////////////////////////////////////'
#!!!!      print('HHMMSSms:',1000*ihhmmss+ims_rdl
#!!!!             ,'   -  ROTA,INCL_rdl:',rota_rdl,incl_rdl
#!!!!      print('NUM_SWP,RAY :',num_swp,no_rdl
#!!!!      print('AZE,ELH_rdl:',azest_rdl,elhor_rdl
#!!!!      print('LON,LAT,ALT_av:',lon_av,lat_av,p_alt_av
#!!!!             ,' CAP_av:',cap_av
#!!!!      print('VENT_we,sn,nz:',vent_we,vent_sn,vent_nz
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** NYQUIST VELOCITY
#******************************************************************
# CAI-START----- Oliver's modification is for P3, for ELDORA, we don't
#                need these NYQUIST velocity stuff!!!!
# CAI-STOP
#
#     vnyq=vit_nonamb(iradar_ray)	! Mod Oliv
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!! THIS VALUE IS CORRECT FOR IPP1/IPP2=4/5 ONLY !!!!
#      vnyq_el=vnyq/20.
#      vnyq_s=5.*vnyq_el	!Olivier
#      vnyq_l=4.*vnyq_el	!Olivier
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** CONTROL FOR AN END OF SWEEP
#******************************************************************
#
      if(nb_ray(iradar_ray) == 1):
        tandrot=0.
      else
        tandrot=tan(conv*(rota_rdl-rota_prev(iradar_ray)))
      endif

      if(     nb_ray(iradar_ray) > 1
          and (    (swp(iradar_ray).ne.swp_prev(iradar_ray))
               .or.(abs(tandrot) > 0.2)       ) )
        iend=1
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      if(iend >= 1):
#!!!!        print(' '
#!!!!        print('NB_RAY(iradar_ray)=',nb_ray(iradar_ray)
#!!!!	print('SWP(iradar_ray),SWP_PREV(iradar_ray)='
#!!!!               ,swp(iradar_ray),swp_prev(iradar_ray)
#!!!!        print('ROTA_RDL,PREV=',rota_rdl,rota_prev(iradar_ray)
#!!!!               ,' -> TANDROT=',tandrot
#!!!!        print('=>IEND=',iend,' NUM_SWP=',swp(iradar_ray)
#!!!!      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#****    END OF A SWEEP ( IEND = 1 )
#**** or END OF THE TAPE or END OF CONSIDERED PERIOD ( IEND = 2 )
#******************************************************************
#
  2   continue
      if(iend >= 1):
	rota_end(iradar_ray)=rota_prev(iradar_ray)
#
#******************************************************************
#**** MEAN VALUES FOR THE PAST SWEEP
#******************************************************************
#
        if(nb_ray(iradar_ray) > 1):
          xp(iradar_ray)=float(nb_ray(iradar_ray))
#
          tilt_mean=stilt(iradar_ray)/xp(iradar_ray)
	  tilt_rms=sqrt(amax1(0.,(xp(iradar_ray)*stilt2(iradar_ray)
                       -stilt(iradar_ray)*stilt(iradar_ray))
                        /(xp(iradar_ray)*(xp(iradar_ray)-1))))
#
          nb_sweep(iradar_ray)=nb_sweep(iradar_ray)+1
          xacft_mean=sxa(iradar_ray)/xp(iradar_ray)
          yacft_mean=sya(iradar_ray)/xp(iradar_ray)
          zacft_mean=sza(iradar_ray)/xp(iradar_ray)
  	  acfthspd_mean=sacfthspd(iradar_ray)/xp(iradar_ray)
          time_ks_mean=stime(iradar_ray)/xp(iradar_ray)
	  ihmean=time_ks_mean/3.6
	  immean=(time_ks_mean-3.6*float(ihmean))/0.06
	  ismean=(time_ks_mean-3.6*float(ihmean)
      	         -0.06*float(immean))/0.001
	  ihms=10000*ihmean+100*immean+ismean
          hdg_mean=atan2( ssc(iradar_ray)/xp(iradar_ray)
                         ,scc(iradar_ray)/xp(iradar_ray))/conv
	  uacft_mean=su_acft(iradar_ray)/xp_acft(iradar_ray)
	  vacft_mean=sv_acft(iradar_ray)/xp_acft(iradar_ray)
          wacft_mean=sw_acft(iradar_ray)/xp_acft(iradar_ray)
	  uwind_mean=su_wind(iradar_ray)/xp_wind(iradar_ray)
	  vwind_mean=sv_wind(iradar_ray)/xp_wind(iradar_ray)
          wwind_mean=sw_wind(iradar_ray)/xp_wind(iradar_ray)
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
#******************************************************************
#**** WRITE THE RESULTS FOR THE PAST SWEEP
#**** ON THE "SIS_EL_*" FILE #50
#******************************************************************
#
#**** SWEEP HEADER
#
          f50.write(iaftfore,nb_sweep(iradar_ray)
                   ,xacft_mean,yacft_mean,zacft_mean
                   ,time_ks_mean,hdg_mean
                   ,u_mean,v_mean,w_mean)
#
#******************************************************************
#**** SWEEP DATA: DZ_surf
#******************************************************************
#
          print(' ')
          if(kdzsurf == 1 and n_dzsurf(iradar_ray) > 0):
            f50.write(n_dzsurf(iradar_ray))
            f50.write(( zs_rot(iradar_ray,n)
                      ,zs_el(iradar_ray,n),zs_az(iradar_ray,n)
                      ,zs_dsurf(iradar_ray,n),zs_dhor(iradar_ray,n)
                      ,zs_zsurf(iradar_ray,n),zs_hsurf(iradar_ray,n)
                      ,n=1,n_dzsurf(iradar_ray))
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print(' ')
#!!!!      print(' SIS_* -> NPTS_Zsurf:',n_dzsurf(iradar_ray))
#!!!!      print(' [ ROT - DH - Z_surf - H_surf ]')
#!!!!      do n=1,n_dzsurf(iradar_ray)
#!!!!         print(zs_rot(iradar_ray,n),zs_dhor(iradar_ray,n)
#!!!!                ,zs_zsurf(iradar_ray,n),zs_hsurf(iradar_ray,n))
#!!!!      enddo
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          else
            f50.write(0)
          endif
#
#******************************************************************
#**** SWEEP DATA: VDOP_surf
#******************************************************************
#
          if(kvsurf == 1 and n_vsurf(iradar_ray) > 0):
            f50.write(n_vsurf(iradar_ray))
            f50.write((vs_dhor(iradar_ray,n),vs_vdopsurf(iradar_ray,n)
                      ,n=1,n_vsurf(iradar_ray)))
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print(' '
#!!!!      print(' SIS_* -> NPTS_VDOP_surf:',n_vsurf(iradar_ray)
#!!!!      print(' [ DH - VDOP_surf ]'
#!!!!      do n=1,n_vsurf(iradar_ray)
#!!!!         print(vs_dhor(iradar_ray,n),vs_vdopsurf(iradar_ray,n)
#!!!!      enddo
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          else
            f50.write(0)
          endif
#
#******************************************************************
#**** SWEEP DATA: DVDOP_insitu
#******************************************************************
#
          if(kdvinsitu == 1 and n_dvinsitu(iradar_ray) > 0):
            f50.write(n_dvinsitu(iradar_ray))
            f50.write(( vi_dhor(iradar_ray,n)
                      ,vi_vdop(iradar_ray,n),vi_vinsitu(iradar_ray,n)
                      ,n=1,n_dvinsitu(iradar_ray)))
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print(' '
#!!!!      print(' NPTS_Vinsitu:',n_dvinsitu(iradar_ray)
#!!!!      print(' DH - Vdop - Vinsitu'
#!!!!      do n=1,n_dvinsitu(iradar_ray)
#!!!!         print(vi_dhor(iradar_ray,n)
#!!!!                ,vi_vdop(iradar_ray,n),vi_vinsitu(iradar_ray,n)
#!!!!      enddo
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          else
            f50.write(0)
          endif
#
        endif    !!  of  !! if(nb_ray(iradar_ray) > 1):  !!
#
#******************************************************************
#**** END OF THE TAPE or END OF CONSIDERED PERIOD ( IEND = 2 )
#******************************************************************
#
        if(iend == 2):
          iend_equals_2()
          # calculate and write cfac then exit?
        endif    !!  of  !! if(iend == 2):  !!



#
#******************************************************************
#**** INITIALIZATIONS AT THE BEGINNING OF A SWEEP (if IEND=1)
#******************************************************************
#
        istart_sweep(iradar_ray)=0
        xsweeps(iradar_ray)=xsweeps(iradar_ray)+1.
        nb_ray(iradar_ray)=0
        stilt(iradar_ray)=0.
	stilt2(iradar_ray)=0.
	rota_prev(iradar_ray)=-999.
	rota_start(iradar_ray)=-999.
	rota_end(iradar_ray)=-999.
	sxa(iradar_ray)=0.
	sya(iradar_ray)=0.
	sza(iradar_ray)=0.
	sacfthspd(iradar_ray)=0.
	stime(iradar_ray)=0.
	ssc(iradar_ray)=0.
	scc(iradar_ray)=0.
	xp_acft(iradar_ray)=0.
	su_acft(iradar_ray)=0.
	sv_acft(iradar_ray)=0.
	sw_acft(iradar_ray)=0.
	xp_wind(iradar_ray)=0.
	su_wind(iradar_ray)=0.
	sv_wind(iradar_ray)=0.
	sw_wind(iradar_ray)=0.
        n_dvinsitu(iradar_ray)=0
        n_dzsurf(iradar_ray)=0
        n_vsurf(iradar_ray)=0
        ndismiss_vhacft(iradar_ray)=0
        ndismiss_vdopcorr(iradar_ray)=0
        ndismiss_vdopsurf(iradar_ray)=0
#
        do n=1,500
           zs_rot(iradar_ray,n)=0.
           zs_el(iradar_ray,n)=0.
           zs_az(iradar_ray,n)=0.
           zs_dsurf(iradar_ray,n)=0.
           zs_dhor(iradar_ray,n)=0.
           zs_zsurf(iradar_ray,n)=0.
           zs_hsurf(iradar_ray,n)=0.
           vs_dhor(iradar_ray,n)=0.
           vs_vdopsurf(iradar_ray,n)=0.
           vi_dhor(iradar_ray,n)=0.
           vi_vdop(iradar_ray,n)=0.
           vi_vinsitu(iradar_ray,n)=0.
        enddo
#
        swdzsurf_sweep(iradar_ray)=0.
        dzsurfsweep_mean(iradar_ray)=0.
        dzsurfsweep_rms(iradar_ray)=0.
        swvsurf_sweep(iradar_ray)=0.
        vsurfsweep_mean(iradar_ray)=0.
        vsurfsweep_rms(iradar_ray)=0.
        nsurf_wri(iradar_ray)=0
        swinsitu_sweep(iradar_ray)=0.
        dvinsitusweep_mean(iradar_ray)=0.
        dvinsitusweep_rms(iradar_ray)=0.
	do jgd=1,2
	   s_vpv(iradar_ray,jgd)=0.
	   sv_vpv(iradar_ray,jgd)=0.
	   svv_vpv(iradar_ray,jgd)=0.
	enddo
#
      endif  !!  of  !! if(iend >= 1):
#
#************************************************************************
#**** NEW RAY
#************************************************************************
#
      nb_ray(iradar_ray)=nb_ray(iradar_ray)+1
#
#******************************************************************
#**** FRENCH->ENGLISH TRANSLATIONS
#**** CONSTANT CORRECTIONS READ ON THE TAPE
#******************************************************************
#
      azeast_ray=azest_rdl+corr_azest(iradar_ray)	! Mod Oliv
      elhor_ray=elhor_rdl+corr_elhor(iradar_ray)	!
      xlon_acft=lon_av+corr_lon(iradar_ray)		!
      xlat_acft=lat_av+corr_lat(iradar_ray)		!
      p_alt_acft=p_alt_av+corr_p_alt(iradar_ray)	!
      r_alt_acft=r_alt_av+corr_r_alt(iradar_ray)	!
      roll_acft=roul_av+corr_roul(iradar_ray)		!
      pitch_acft=tang_av+corr_tang(iradar_ray)		!
      hdg_acft=cap_av+corr_cap(iradar_ray)		!
      drift_acft=derv_av+corr_derv(iradar_ray)		!
      rota_ray=rota_rdl+corr_rota(iradar_ray)		!
      tilt_ray=incl_rdl+corr_incl(iradar_ray)		!
      wind_we=vent_we
      wind_sn=vent_sn
      wind_nz=vent_nz
      acftspd_we=vwe_av
      acftspd_sn=vsn_av
      acftspd_nz=vnz_av
#	print('IRADAR_RAY= ',iradar_ray
#	print('AZ,EL,Xlon,Xlat,Palt,Roll,Pitch,Hdg,Drift,Rota
#               ,Tilt= ',corr_azest(iradar_ray), corr_elhor(iradar_ray)
#               , corr_lon(iradar_ray),corr_lat(iradar_ray)
#               ,corr_p_alt(iradar_ray),corr_roul(iradar_ray)
#               ,corr_tang(iradar_ray),corr_cap(iradar_ray)
#               ,corr_derv(iradar_ray),corr_rota(iradar_ray)
#               , corr_incl(iradar_ray)
#
#******************************************************************
#**** EARTH-RELATIVE ANGLES AND
#**** PARAMETERS FOR THE ANALYSIS
#******************************************************************
#
      if(iaftfore == -1):
        dtilt_guess=dtiltaft_guess
        drota_guess=drotaaft_guess
      else
        dtilt_guess=dtiltfore_guess
        drota_guess=drotafore_guess
      endif
#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE NAVIGATION WITHOUT dXXX_GUESS
#------------------------------------------------------------------
      if(isim == 1):
#
        call azel( rota_ray+roll_acft
                  ,tilt_ray
                  ,hdg_acft,drift_acft
                  ,pitch_acft
                  ,azeast_ray_true,elhor_ray_true
                  ,cxa_true,cya_true,cza_true
                  ,cwe_true,csn_true,cnz_true)
        caze_true=caze
	saze_true=saze
	celh_true=celh
	selh_true=selh

#
        dcwe_dt_true=+crr*sti*spit*shdg-srr*sti*chdg+cti*cpit*shdg
        dcwe_dr_true=+srr*cti*spit*shdg+crr*cti*chdg
        dcwe_dp_true=-crr*cti*cpit*shdg-sti*spit*shdg
        dcwe_dh_true=-crr*cti*spit*chdg-srr*cti*shdg+sti*cpit*chdg
#
        dcsn_dt_true=+crr*sti*spit*chdg+srr*sti*shdg+cti*cpit*chdg
        dcsn_dr_true=+srr*cti*spit*chdg-crr*cti*shdg
        dcsn_dp_true=-crr*cti*cpit*chdg-sti*spit*chdg
        dcsn_dh_true=+crr*cti*spit*shdg-srr*cti*chdg-sti*cpit*shdg
#
        dcnz_dt_true=-crr*sti*cpit+cti*spit
        dcnz_dr_true=-srr*cti*cpit
        dcnz_dp_true=-crr*cti*spit+sti*cpit
        dcnz_dh_true=0.
#
        duacft_dv_true=+shdg*cdri+chdg*sdri
        dvacft_dv_true=+chdg*cdri-shdg*sdri
#
      endif
#------------------------------------------------------------------
      call azel( rota_ray+drota_guess+roll_acft
                ,tilt_ray+dtilt_guess
                ,hdg_acft+dhdg_guess,drift_acft
                ,pitch_acft+dpitch_guess
                ,azeast_ray,elhor_ray
                ,cxa,cya,cza,cwe,csn,cnz)
      if(sin(conv*(rota_ray+drota_guess+roll_acft)) < 0.):
        side=-1.
        ilr=1
      else
        side=+1.
        ilr=2
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      if(      iradar_ray == 1
#!!!!           and nb_ray(iradar_ray)
#!!!!                == 10*(nb_ray(iradar_ray)/10) ):
#!!!!        print(' '
#!!!!        print('NO_RAY:',nb_ray(iradar_ray)
#!!!!               ,' ROTA_RAY:',rota_ray+roll_acft
#!!!!               ,' EL_RAY:',elhor_ray
#!!!!      endif
#!!!!        print('IRADAR_RAY:',iradar_ray
#!!!!               ,' NO_RAY:',nb_ray(iradar_ray)
#!!!!      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
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
      else
        d_dgate_guess=rdfore_guess
      endif
      ngates=nb_portes
#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE RANGE GATES WITHOUT dXXX_GUESS
#------------------------------------------------------------------
      if(isim == 1):
        do ig=1,ngates
# CAI-START
#          dgate_true(ig)=d_porte(iradar*MAXPORT+ig)
#                             +corr_dist(iradar+1)
# It seems that the above code if wrong, since iradar has not been assigned values yet,
# therefore, following are the new code:
           dgate_true(ig)=d_porte((iradar_ray-1)*MAXPORT+ig)
                              +corr_dist(iradar_ray)
        enddo
      endif
#------------------------------------------------------------------
      do ig=1,ngates
         dgate_corr(ig)=d_porte((iradar_ray-1)*MAXPORT+ig)   ! Mod Oliv
                        +corr_dist(iradar_ray)+d_dgate_guess
      enddo
      ddg=dgate_corr(2)-dgate_corr(1)
#
#******************************************************************
#**** AIRCRAFT POSITION, (PRESSURE OR RADAR) ALTITUDE AND HEADING
#******************************************************************
#
      ylat=(xlat_acft+orig_lat)/2.
      deg_lon=deg_lon0*cos(conv*ylat)
#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE AIRCRAFT POSITION WITHOUT dXXX_GUESS
#------------------------------------------------------------------
      if(isim == 1):
        x_acft_true=(xlon_acft-orig_lon)*deg_lon
        y_acft_true=(xlat_acft-orig_lat)*deg_lat
        if(ipr_alt == 1):
	  z_acft_true=p_alt_acft
        else
	  z_acft_true=r_alt_acft
        endif
      endif
#------------------------------------------------------------------
      x_acft=(xlon_acft-orig_lon)*deg_lon+dxwe_guess
      y_acft=(xlat_acft-orig_lat)*deg_lat+dysn_guess
      if(ipr_alt == 1):
	z_acft=p_alt_acft+dzacft_guess
      else
	z_acft=r_alt_acft+dzacft_guess
      endif

#	print('Z_ACFT,P_ALT,D_GUESS= ',z_acft,p_alt_acft,dzacft_guess
#
#******************************************************************
#**** ADD TO THE MEAN PARAMETERS FOR THE CURRENT SWEEP
#******************************************************************
#
      stilt(iradar_ray)=stilt(iradar_ray)+tilt_ray
      stilt2(iradar_ray)=stilt2(iradar_ray)+tilt_ray*tilt_ray
      if(nb_ray(iradar_ray) == 1)rota_start(iradar_ray)=rota_ray
      sxa(iradar_ray)=sxa(iradar_ray)+x_acft
      sya(iradar_ray)=sya(iradar_ray)+y_acft
      sza(iradar_ray)=sza(iradar_ray)+z_acft
      stime(iradar_ray)=stime(iradar_ray)+time_ks
      ssc(iradar_ray)=ssc(iradar_ray)+shdg
      scc(iradar_ray)=scc(iradar_ray)+chdg
      dmax=amin1(dmax0,dgate_corr(ngates))
#
#******************************************************************
#**** AIRCRAFT SPEED
#******************************************************************
#
      if(    (abs(acftspd_we) < 10. and abs(acftspd_sn) < 10.)
         .or.(abs(acftspd_we) > 200..or.abs(acftspd_sn) > 200.) ):
        print(' !!!! NO_RAY:',nb_ray
               ,' -> U,V,W_acft:',acftspd_we,acftspd_sn,acftspd_nz
               ,' !!!!'
        go to 1
      endif
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
      sacfthspd(iradar_ray)=sacfthspd(iradar_ray)+acftspd_hor
      xp_acft(iradar_ray)=xp_acft(iradar_ray)+1.
      su_acft(iradar_ray)=su_acft(iradar_ray)+acftspd_we
      sv_acft(iradar_ray)=sv_acft(iradar_ray)+acftspd_sn
      sw_acft(iradar_ray)=sw_acft(iradar_ray)+acftspd_nz
      proj_acftspd=acftspd_we*cwe+acftspd_sn*csn+acftspd_nz*cnz
#
#******************************************************************
#**** FLIGHT-LEVEL WIND
#******************************************************************
#
#----------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE AIRCRAFT SPEED WITHOUT dXXX_GUESS
#----------------------------------------------------------------------
      if(isim == 1):
        proj_wind=wind_we*cwe_true+wind_sn*csn_true+wind_nz*cnz_true
        wa_we_true=wind_we-acftspd_we_true
        wa_sn_true=wind_sn-acftspd_sn_true
      endif
#----------------------------------------------------------------------
      if(    (abs(wind_we) <= 0. and abs(wind_sn) <= 0.)
         .or.(abs(wind_we) > 100..or.abs(wind_sn) > 100.)):
        print(' !!!! NO_RAY:',nb_ray(iradar_ray),' -> Uwe,Vsn_wind:'
               ,wind_we,wind_sn,' !!!!'
        go to 1
      endif
      if(abs(wind_nz) <= 0..or.abs(wind_nz) > 50.)wind_nz=0.
      xp_wind(iradar_ray)=xp_wind(iradar_ray)+1.
      su_wind(iradar_ray)=su_wind(iradar_ray)+wind_we
      sv_wind(iradar_ray)=sv_wind(iradar_ray)+wind_sn
      sw_wind(iradar_ray)=sw_wind(iradar_ray)+wind_nz
      proj_wind=wind_we*cwe+wind_sn*csn+wind_nz*cnz
      wa_we=wind_we-acftspd_we
      wa_sn=wind_sn-acftspd_sn
      wa_nz=wind_nz-acftspd_nz
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!! ELIMINATION OF GATES CONTAMINATED WITH GROUND-CLUTTER
#!!!! ONLY FOR TOGA-COARE DATA !!!!
#!!!!  -> aft_SWEEP : dROTA=+6 deg
#!!!!  -> fore_SWEEP : dROTA=+3 deg)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!
#!!!!     if(tilt_ray < -15.):
#!!!!       rota_sidelobe=rota_ray+roll_acft+6.
#!!!!     elif(tilt_ray > 15.):
#!!!!       rota_sidelobe=rota_ray+roll_acft+3.
#!!!!     endif
#!!!!      if(a_don <= 1993 and cos(conv*rota_sidelobe) < 0.):
#!!!!       dmax_sidelobe=(z_min-z_acft)/cos(conv*rota_sidelobe)
#!!!!       dmax=amin1(dmax0,dmax_sidelobe)
#!!!!     else
#!!!!       dmax=dmax0
#!!!!     endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** DISMISS THE SPECIFIED RANGE GATES
#******************************************************************
#
      do iig=1,15
         if(ig_dismiss(iig) > 0):
           ig=ig_dismiss(iig)
           ze(ig)=-999.
           vr(ig)=-999.
	   vs(ig)=-999.	!Olivier
	   vl(ig)=-999.	!Olivier
           vg(ig)=-999.
           vu(ig)=-999.
         endif
      enddo
#
#******************************************************************
#**** RANGE GATES FOR COMPARISONS WITH FLIGHT-LEVEL (IN SITU) DATA
#******************************************************************
#
      ngates_insitu_max=-999
      if(abs(selh) < selhinsitu_max):
        ig=1
        do while (     ig < MAXPORT
                   and dgate_corr(ig) < dmax_insitu)
           ngates_insitu_max=ig
           ig=ig+1
        enddo
      endif
#
#******************************************************************
#**** CHECK THE NCP, SW AND REFLECTIVITY VALUES
#******************************************************************
#
      ngates_max=1
      do ig=1,ngates
         ref_min=ref_min0+20.*(alog10(dgate_corr(ig))-1.)
         if(    dgate_corr(ig) < dmin
            .or.dgate_corr(ig) > dmax
            .or.ncp(ig) < xncp_min
            .or.sw(ig) > sw_max
            .or.ze(ig) < ref_min
            .or.ze(ig) > ref_max):
           ze(ig)=-999.
           vr(ig)=-999.
	   vs(ig)=-999.	!Olivier
	   vl(ig)=-999.	!Olivier
           vg(ig)=-999.
           vu(ig)=-999.
         else
	   ngates_max=ig
           nref_ok(iradar_ray)=nref_ok(iradar_ray)+1
         endif
      enddo
  10  continue
#
#******************************************************************
#**** CHOOSE WHICH DOPPLER VELOCITY WILL BE USED (FOLLOWING ICHOICE_VDOP)
#****   -> 1:RAW(VR), 2:CORRECTED FOR VACFT(VG), 3:UNFOLDED(VU)
#******************************************************************

      do ig=1,ngates_max

	 vdop_read=-999.
	 vdop_corr(ig)=-999.
	 if(ze(ig) > -900.):

            if(     ichoice_vdop == 1
               and abs(vr(ig)) > 0. and abs(vr(ig)) < vdop_max
               and proj_acftspd > -900.)
               vdop_read=vr(ig)+proj_acftspd
# CAI-STOP


           if(     ichoice_vdop == 2
               and abs(vr(ig)) > 0. and abs(vr(ig)) < vdop_max)
             vdop_read=vr(ig)

           if(     ichoice_vdop == 3
               and abs(vu(ig)) > 0. and abs(vu(ig)) < vdop_max)
             vdop_read=vu(ig)

           if(vdop_read > -900.):
             ndop_ok(iradar_ray)=ndop_ok(iradar_ray)+1
             vdop_corr(ig)=vdop_read
           endif

         endif
      enddo

#******************************************************************
#**** ( if     ( KZsurf=1  or  KVsurf=1 )
#****      and  Z_ACFT > Z_ACFTmin
#****      and SIN(ELEV_HOR) < SELH_SURF
#****      and  VFF_AV>0 )
#****  -> DETERMINE ALTITUDE (THEN DOPPLER VELOCITY)
#****     OF THE SURFACE FOR THIS RAY
#******************************************************************
#
      if(     (kdzsurf+kvsurf) >= 1
          and selh < selh_surf
          and z_acft > zacftmin_surf):
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
        print(' '
        print(' ',1000*ihhmmss+ims_ray
               ,' IRADAR:',iradar_ray
               ,' NO_RAY:',nb_ray(iradar_ray)
        print('    ROTA,TILT_RAY:',rota_ray,tilt_ray
        print('    ROLL,PITCH,HDG,DRIFT_ACFT:',roll_acft
               ,pitch_acft,hdg_acft,drift_acft
        print('    AZ_EAST:',azeast_ray,' EL_HOR:',elhor_ray
        print('    CWE,CSN,CNZ:',cwe,csn,cnz
        print('    U,V,W_ACFT:',acftspd_we,acftspd_sn,acftspd_nz
               ,' PROJ_VACFT:',proj_acftspd
#!!!!        print('    U,V,W_WIND:',wind_we,wind_sn,wind_nz
#!!!!               ,'    PROJ_WIND:',proj_wind
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
        dsurf_ray=-999.
        dhorsurf_ray=-999.
        hsurf_ray=-999.
        refsurf_ray=0.
        refsurf_min=refsurf_min0*((abs(selh))**0.7)
        gradrefsurf_ray=0.
        gradrefsurf_min=gradrefsurf_min0*((abs(selh))**0.7)
        wghtsurf_ray=0.
#
        refmax_ray=-999.
        ig_refmax=999		! Olivier (float->entier)
        d_refmax=-999.
        h_refmax=-999.
        z_refmax=-999.
        gradrefmax_ray=-999.
        ig_gradrefmax=999	! Olivier (float->entier)
        d_gradrefmax=-999.
        h_gradrefmax=-999.
        z_gradrefmax=-999.
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

	dhor_prevgate=0.	! Mod Oliv
	z_prevgate=0.		! Mod Oliv

# autoconverted begin
import numpy as np

for ig in range(igstart_surf, ngates_max + 1):
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
            
            if ig > 1 and ze[ig - 1] > -900.:
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
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
#!!!!        print('     REF(1->IGmax+5) :'
#!!!!               ,(int(ze(ig)),ig=1,ig_refmax+5)
#!!!!         print('    -> IG_RefMAX:',ig_refmax,' -> REF: max,d,z:'
#!!!!               ,refmax_ray,d_refmax,z_refmax
#!!!!         print('    -> IG_GradMAX:',ig_gradrefmax,' -> GRAD: max,d,z:'
#!!!!                ,gradrefmax_ray,d_gradrefmax,z_gradrefmax
#!!!!      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** WEIGHT ASSOCIATED WITH THE OBTAINED SURFACE POINT
#******************************************************************
#
        if refmax_ray > refsurf_min
            and gradrefmax_ray > gradrefsurf_min):
          if(     (d_refmax > d_gradrefmax)
              and abs(z_refmax-z_gradrefmax) < 1.):
            wght_ref=1.+(refmax_ray-refsurf_min)/refsurf_min
            wght_grad=1.+(gradrefmax_ray-gradrefsurf_min)
                        /(gradrefsurf_min)
            wghtsurf_ray=sqrt(wght_ref*wght_grad)
            dsurf_ray=d_refmax
            hsurf_ray=z_refmax
            dhorsurf_ray=dhor_refmax
            xsurf_ray=x_acft+dhorsurf_ray*caze
            ysurf_ray=y_acft+dhorsurf_ray*saze
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
#!!!!        print('     -> SURF: d,dhor,z:'
#!!!!               ,dsurf_ray,dhorsurf_ray,hsurf_ray
#!!!!        print('     -> X,Y,H_SURF:',xsurf_ray,ysurf_ray,hsurf_ray
#!!!!        print('        WGHTSURF_ray :',wghtsurf_ray
#!!!!      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!          else
#!!!!      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) )
#!!!!        print('    !!!! VALUES OK, BUT PB ON d_REF AND/OR d_GRAD !!!'
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!        else
#!!!!      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) )
#!!!!        print('    !!!! PB ON REF AND/OR GRAD VALUES !!!'
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        endif
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
	  do ig=igstart_surf,ngates_max
	     if(dgate_corr(ig) <= distmax):
#
	       d_app=dgate_corr(ig)
  	       dver_app=d_app*selh
	       dhor_app=d_app*celh
	       frac1=2.*(z_acft+dver_app)/rayter
	       frac2=(z_acft*z_acft+d_app*d_app
                      +2.*z_acft*dver_app)/(rayter*rayter)
               z_app=rayter*(sqrt(1.+frac1+frac2)-1.)
               theta=atan(dhor_app/(rayter+z_acft+dver_app))
               dhor_app=rayter*theta
               x_app=x_acft+dhor_app*caze
               y_app=y_acft+dhor_app*saze
#
	       d_true=dgate_true(ig)
  	       dver_true=d_true*selh_true
	       dhor_true=d_true*celh_true
	       frac1=2.*(z_acft_true+dver_true)/rayter
	       frac2=(z_acft_true*z_acft_true+d_true*d_true
                      +2.*z_acft_true*dver_true)/(rayter*rayter)
               z_true=rayter*(sqrt(1.+frac1+frac2)-1.)
               theta=atan(dhor_true/(rayter+z_acft_true+dver_true))
               dhor_true=rayter*theta
               x_true=x_acft_true+dhor_true*caze_true
               y_true=y_acft_true+dhor_true*saze_true
#
	       if(     igsurf_ray == -999
                   and x_true > xmin_dtm
                   and x_true < xmax_dtm
                   and y_true > ymin_dtm
                   and y_true < ymax_dtm):
                 isurf_true=(x_true-xmin_dtm)/hx_dtm+1
	         jsurf_true=(y_true-ymin_dtm)/hy_dtm+1
	         aa=alt_dtm(isurf_true,jsurf_true)
	         bb=(-alt_dtm(isurf_true,jsurf_true)
                     +alt_dtm(isurf_true+1,jsurf_true))/hx_dtm
	         cc=(-alt_dtm(isurf_true,jsurf_true)
                     +alt_dtm(isurf_true,jsurf_true+1))/hy_dtm
                 dd=(+alt_dtm(isurf_true,jsurf_true)
                     -alt_dtm(isurf_true+1,jsurf_true)
                     -alt_dtm(isurf_true,jsurf_true+1)
                     +alt_dtm(isurf_true+1,jsurf_true+1))
                     /(hx_dtm*hy_dtm)
	         x_dtm=xmin_dtm+float(isurf_true-1)*hx_dtm
	         dx=x_true-x_dtm
	         y_dtm=ymin_dtm+float(jsurf_true-1)*hy_dtm
	         dy=y_true-y_dtm
                 hsurf_dtm=aa+bb*dx+cc*dy+dd*dx*dy
#
		 if(hsurf_dtm >= z_true):
#
		   xsurf_true=x_true
		   ysurf_true=y_true
		   hsurf_true=z_true
	           dxh_dtm=bb+dd*dy
	           dyh_dtm=cc+dd*dx
#
		   igsurf_ray=ig
		   dsurf_ray=d_app
		   xsurf_ray=x_app
		   ysurf_ray=y_app
		   hsurf_ray=z_app
		   wghtsurf_ray=1.
#
		 endif
#
	       endif
	     endif
	  enddo
#
# autoconverted begin
import numpy as np

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
        print('     -> X,Y,H_SURF-TRUE:'
               ,xsurf_true,ysurf_true,hsurf_true
        print('        I,J_SURF_true :',isurf_true,jsurf_true
               ,' dxH,dyH :',dxh_dtm,dyh_dtm
        print('     -> X,Y,H_SURF-RAY:'
               ,xsurf_ray,ysurf_ray,hsurf_ray
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
	endif
#--------------------------------------------------------------
#
#******************************************************************
#**** IF THIS SURFACE POINT IS CORRECT (if WGHTSURF_ray > 0)
#**** THEN COMPARE WITH THE SURFACE POINT DERIVED FROM THE DTM
#******************************************************************
#
        if(hsurf_ray > -900. and wghtsurf_ray > 0.):
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
        print('    -> X,Y,H_SURF-RAY:',xsurf_ray,ysurf_ray,hsurf_ray
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** INTERPOLATION OF ALT_DTM(x,y) [READ ON SURF_DTM_* OR CONSTANT]
#******************************************************************
#
	  if(     xsurf_ray > xmin_dtm
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
            dd=(+alt_dtm(isurf_ray,jsurf_ray)
                -alt_dtm(isurf_ray+1,jsurf_ray)
                -alt_dtm(isurf_ray,jsurf_ray+1)
                +alt_dtm(isurf_ray+1,jsurf_ray+1))
                /(hx_dtm*hy_dtm)
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
        print('        I,J_SURF_ray :',isurf_ray,jsurf_ray
               ,' dxH,dyH :',dxh_dtm,dyh_dtm
        print('     -> H_SURF-DTM:',hsurf_dtm
               ,'  =>> D_HSURF :',d_hsurf
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** IF ( ABS(HSURF_RADAR-HSURF_DTM) < DHSURF_MAX ) THEN
#**** !!!! DHSURF_MAX=999. !!!! -> NOT IN USE !!!!
#******************************************************************
#
            if(abs(d_hsurf) < dhsurf_max):
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
            d_hsurf_dxxx=-dsurf_ray
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
                         +dzacft_guess
#!!!!            d_hsurf=d_hsurf_dxxx
	  endif
#----------------------------------------------------------------------
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
        print('     -> D_HSURF_dXXX :',d_hsurf_dxxx
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** ADD WEIGHTS AND DZ_surf
#******************************************************************
#
                n_dzsurf(iradar_ray)=n_dzsurf(iradar_ray)+1
                swdzsurf_sweep(iradar_ray)
                 =swdzsurf_sweep(iradar_ray)+wghtsurf_ray
#
	        dzsurfsweep_mean(iradar_ray)
                 =dzsurfsweep_mean(iradar_ray)
                  +wghtsurf_ray*d_hsurf
	        dzsurfsweep_rms(iradar_ray)
                 =dzsurfsweep_rms(iradar_ray)
                  +wghtsurf_ray*d_hsurf*d_hsurf
#
                swdzsurf_tot=swdzsurf_tot+wghtsurf_ray
 	        swdzmsurf_tot=swdzmsurf_tot
                             +wghtsurf_ray*d_hsurf
	        swdz2surf_tot=swdz2surf_tot
                             +wghtsurf_ray*d_hsurf*d_hsurf
                swadzsurf_tot=swadzsurf_tot
                              +wghtsurf_ray*abs(d_hsurf)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print('    -> WGHTSURF_RAY:',wghtsurf_ray,' DZSURF:',d_hsurf
#!!!!      print('       N_DZSURF:',n_dzsurf(iradar_ray)
#!!!!             ,' SWDZ,SDZ,SDZ2:',swdzsurf_sweep(iradar_ray)
#!!!!             ,dzsurfsweep_mean(iradar_ray),dzsurfsweep_rms(iradar_ray)
#!!!!      print('       !!!! VR,PROJ_ACFTSPD,VCORR_SURF:'
#!!!!             ,vr(ig_refmax),proj_acftspd,vdop_corr(ig_refmax),' !!!!'
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** VALUES OF VAR(1->NVAR) FOR FIELD "DZ_surf"
#****  - VAR(1->6) -> [dT_aft,dT_fore,dR_aft,dR_fore,dP,dH] in DEGREES
#****  - VAR(7->11) -> [RD_aft,RD_fore,dXwe,dYsn,dZ] in HECTOMETERS
#****  - VAR(12) -> [dVH] in METER/SECOND
#******************************************************************
#
                if(iaftfore == -1):
                  if(idtiltaft == 1):
                    var(1)=dsurf_ray
                           *(-dcnz_dt+dxh_dtm*dcwe_dt+dyh_dtm*dcsn_dt)
                           *conv
                  else
                    var(1)=0.
                    xmat_dzsurf(1,1)=xmat_dzsurf(1,1)+wghtsurf_ray
                  endif
                  var(2)=0.
                else
                  var(1)=0.
                  if(idtiltfore == 1):
                     var(2)=dsurf_ray
                            *(-dcnz_dt+dxh_dtm*dcwe_dt+dyh_dtm*dcsn_dt)
                            *conv
                  else
                    var(2)=0.
                    xmat_dzsurf(2,2)=xmat_dzsurf(2,2)+wghtsurf_ray
                  endif
                endif
#
                if(iaftfore == -1):
                  if(idrotaaft == 1):
                    var(3)=dsurf_ray
                           *(-dcnz_dr+dxh_dtm*dcwe_dr+dyh_dtm*dcsn_dr)
                           *conv
                  else
                    var(3)=0.
                    xmat_dzsurf(3,3)=xmat_dzsurf(3,3)+wghtsurf_ray
                  endif
                  var(4)=0.
                else
                  var(3)=0.
                  if(idrotafore == 1):
                    var(4)=dsurf_ray
                           *(-dcnz_dr+dxh_dtm*dcwe_dr+dyh_dtm*dcsn_dr)
                           *conv
                  else
                    var(4)=0.
                    xmat_dzsurf(4,4)=xmat_dzsurf(2,2)+wghtsurf_ray
                  endif
                endif
#
                if(idpitch == 1):
                  var(5)=dsurf_ray
                         *(-dcnz_dp+dxh_dtm*dcwe_dp+dyh_dtm*dcsn_dp)
                         *conv
                else
                  var(5)=0.
                  xmat_dzsurf(5,5)=xmat_dzsurf(4,4)+wghtsurf_ray
                endif
#
                if(idhdg == 1):
                  var(6)=dsurf_ray
                         *(+dxh_dtm*dcwe_dh+dyh_dtm*dcsn_dh)
                         *conv
                else
                  var(6)=0.
                  xmat_dzsurf(6,6)=xmat_dzsurf(5,5)+wghtsurf_ray
                endif
#
                if(iaftfore == -1):
                   if(irdaft == 1):
                     var(7)=(-cnz+dxh_dtm*cwe+dyh_dtm*csn)
                            *0.1
                   else
                     var(7)=0.
                     xmat_dzsurf(7,7)=xmat_dzsurf(6,6)+wghtsurf_ray
                   endif
                   var(8)=0.
                else
                   var(7)=0.
                   if(irdfore == 1):
                     var(8)=(-cnz+dxh_dtm*cwe+dyh_dtm*csn)
                            *0.1
                   else
                     var(8)=0.
                     xmat_dzsurf(8,8)=xmat_dzsurf(8,8)+wghtsurf_ray
                   endif
                endif
#
                if(idxwe == 1):
                  var(9)=dxh_dtm*0.1
                else
                  var(9)=0.
                  xmat_dzsurf(9,9)=xmat_dzsurf(9,9)+wghtsurf_ray
                endif
#
                if(idysn == 1):
                  var(10)=dyh_dtm*0.1
                else
                  var(10)=0.
                  xmat_dzsurf(10,10)=xmat_dzsurf(10,10)+wghtsurf_ray
                endif
#
                if(idzacft == 1):
                  var(11)=-0.1
                else
                  var(11)=0.
                  xmat_dzsurf(11,11)=xmat_dzsurf(11,11)+wghtsurf_ray
                endif
#
                var(12)=0.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print('    VAR_DZSURF(1->12):',(var(i),i=1,12)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** ADD TO XMAT_dzsurf(1->NVAR,1->NVAR) AND VECT_dzsurf(1->NVAR)
#******************************************************************
#
                do i=1,nvar
                   do j=1,nvar
 	            xmat_dzsurf(i,j)=xmat_dzsurf(i,j)
                	            +wghtsurf_ray*var(i)*var(j)
                   enddo
                   vect_dzsurf(i)=vect_dzsurf(i)
                                  +wghtsurf_ray*var(i)*d_hsurf
                enddo
#
#******************************************************************
#**** ADD TO COVARIANCE MATRIX FOR FIELD "DZ_surf"
#******************************************************************
#
                do i=1,nvar
                   rms_var_zsurf(i)=rms_var_zsurf(i)
                                    +wghtsurf_ray*var(i)*var(i)
                   do j=1,nvar
                      corr_var(i,j)=corr_var(i,j)
                                    +wghtsurf_ray*var(i)*var(j)
                   enddo
                enddo
#
#******************************************************************
#**** CASE "DZ_surf" ONLY -> D_VH CANNOT BE CALCULATED
#******************************************************************
#
                if(rw_vsurf+rw_dvinsitu <= 0.):
                  xmat_vsurf(12,12)=xmat_vsurf(12,12)+wghtsurf_ray
#
#******************************************************************
#**** CASE "FLAT SURFACE" -> D_HEADING,D_XWE,D_YSN CANNOT BE OBTAINED
#******************************************************************
#
                  if(altdtm_min >= altdtm_max):
                    xmat_vsurf(6,6)=xmat_vsurf(6,6)+wghtsurf_ray
                    xmat_vsurf(9,9)=xmat_vsurf(9,9)+wghtsurf_ray
                    xmat_vsurf(10,10)=xmat_vsurf(10,10)+wghtsurf_ray
                  endif
#
                endif
#
#******************************************************************
#**** ARRAYS FOR "SIS_EL_*" FILE #50
#******************************************************************
#
                zs_rot(iradar_ray,n_dzsurf(iradar_ray))=rota_ray
                zs_el(iradar_ray,n_dzsurf(iradar_ray))=elhor_ray
                zs_az(iradar_ray,n_dzsurf(iradar_ray))=azeast_ray
                zs_dsurf(iradar_ray,n_dzsurf(iradar_ray))=dsurf_ray
                zs_dhor(iradar_ray,n_dzsurf(iradar_ray))
                       =side*dsurf_ray*celh
                zs_zsurf(iradar_ray,n_dzsurf(iradar_ray))=hsurf_ray
                zs_hsurf(iradar_ray,n_dzsurf(iradar_ray))=hsurf_dtm
#
	      endif     !!  of !! if(kdzsurf == 1):
#
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
#******************************************************************
#**** CASE "VDOP_surf"
#******************************************************************
#
  	      if(kvsurf == 1 and acftspd_hor > 0.):
#
                if(vdop_corr(ig_refmax) > -900..or.isim == 1):
                  vdopsurf_ray=vdop_corr(ig_refmax)
	if(abs(vdopsurf_ray) <= 1.)nb1=nb1+1
	if(abs(vdopsurf_ray) <= 2. and abs(vdopsurf_ray) > 1.)nb2=nb2+1
	if(abs(vdopsurf_ray) <= 3. and abs(vdopsurf_ray) > 2.)nb3=nb3+1
	if(abs(vdopsurf_ray) <= 4. and abs(vdopsurf_ray) > 3.)nb4=nb4+1
	if(abs(vdopsurf_ray) <= 5. and abs(vdopsurf_ray) > 4.)nb5=nb5+1
	if(abs(vdopsurf_ray) <= 6. and abs(vdopsurf_ray) > 5.)nb6=nb6+1
	if(abs(vdopsurf_ray) <= 7. and abs(vdopsurf_ray) > 6.)nb7=nb7+1
	if(abs(vdopsurf_ray) <= 8. and abs(vdopsurf_ray) > 7.)nb8=nb8+1
	if(abs(vdopsurf_ray) > 8.)nsup=nsup+1
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
#	if(ig_refmax.ne.-999):	! Olivier
#
#	v_ctrl=-999.				! Olivier
#
#	d_vs_vl=vs(ig_refmax)-vl(ig_refmax)	! Olivier
#	kvsl=ifix((d_vs_vl/vnyq_el)*0.5)+5	! Olivier
#        print('    d_VS_VL :',d_vs_vl,' -> KVSL :',kvsl
#	if(kvsl >= 1 and kvsl <= 9):		! Olivier
#	  vs_depl=vs(ig_refmax)+xms(kvsl)*vnyq_el	! Olivier
#	  vl_depl=vl(ig_refmax)+xml(kvsl)*vnyq_el	! Olivier
#c	  vsl_depl=(vs_depl+vl_depl)/2.		! Olivier
#
#	  if(    abs(vs_depl-vl_depl) < vnyq_el/2.
#      	     and abs(vr(ig_refmax)-vsl_depl) < vnyq_el/2.): ! Oliv
#		print('IG_REFMAX= ',ig_refmax
#		print('VR= ',vr(ig_refmax)
#		print('VS, VL= ', vs(ig_refmax),vl(ig_refmax)
#		print('VS_depl,VL_depl= ',vs_depl,vl_depl
#		print('VSL_depl= ',vsl_depl
#	          v_ctrl=vr(ig_refmax)			! Olivier
#		print('VDOP_CTRL= ',v_ctrl
#
#	      if(proj_acftspd > -900.):
#		v_corr=v_ctrl+proj_acftspd
#		print(' VDOP_CORR= ',v_corr
#	      endif
#
#	  endif
#
#	endif
#
#	endif
#      endif

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#--------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED VDOPSURF_RAY FROM dXXX_GUESS
#--------------------------------------------------------------
#
                  if(isim == 1):
                    vdopsurf_ray=-(-acftspd_we_true*dcwe_dt_true
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
                                   -csn_true*dvacft_dv_true)*dvh_guess
	          endif
#--------------------------------------------------------------
#
#                  if(abs(vdopsurf_ray) < vdopsurf_max):

#TEST CAI
                   print('vdopsurf_ray =',vdopsurf_ray
#TEST END

		   if(abs(vdopsurf_ray) < 6.):
#
#******************************************************************
#**** ADD WEIGHTS AND VDOP_surf
#******************************************************************
#
                    n_vsurf(iradar_ray)=n_vsurf(iradar_ray)+1
                    swvsurf_sweep(iradar_ray)
                     =swvsurf_sweep(iradar_ray)+wghtsurf_ray
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
        print('     -> VDOPSURF_RAY :',vdopsurf_ray
#!!!!        print('        SWVSURF_SWEEP(',iradar_ray,') :'
#!!!!               ,swvsurf_sweep(iradar_ray)
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
 	            vsurfsweep_mean(iradar_ray)
                     =vsurfsweep_mean(iradar_ray)
                      +wghtsurf_ray*vdopsurf_ray
	            vsurfsweep_rms(iradar_ray)
                     =vsurfsweep_rms(iradar_ray)
                      +wghtsurf_ray*vdopsurf_ray*vdopsurf_ray
#
                    swvsurf_tot=swvsurf_tot+wghtsurf_ray
  	            swvmsurf_tot=swvmsurf_tot
                                 +wghtsurf_ray*vdopsurf_ray
	            swv2surf_tot=swv2surf_tot
                                 +wghtsurf_ray*vdopsurf_ray*vdopsurf_ray
                    swavsurf_tot=swavsurf_tot
                                 +wghtsurf_ray*abs(vdopsurf_ray)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print('    -> WGHTSURF_RAY:',wghtsurf_ray,' VSURF:',vdopsurf_ray
#!!!!      print('        N_VSURF:',n_vsurf(iradar_ray)
#!!!!             ,' SWV,SV,SV2:',swvsurf_sweep(iradar_ray)
#!!!!             ,vsurfsweep_mean(iradar_ray),vsurfsweep_rms(iradar_ray)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** VALUES OF VAR(1->NVAR) FOR FIELD "V_surf"
#****  - VAR(1->6) -> [dT_aft,dT_fore,dR_aft,dR_fore,dP,dH] in DEGREES
#****  - VAR(7->11) -> [RD_aft,RD_fore,dXwe,dYsn,dZ] in HECTOMETERS
#****  - VAR(12) -> [dVH] in METER/SECOND
#******************************************************************
#
                    if(iaftfore == -1):
                      if(idtiltaft == 1):
                        var(1)=(-acftspd_we*dcwe_dt-acftspd_sn*dcsn_dt
                                -acftspd_nz*dcnz_dt)
                               *conv
                      else
                        var(1)=0.
                        xmat_vsurf(1,1)=xmat_vsurf(1,1)+wghtsurf_ray
                      endif
                      var(2)=0.
                    else
                      var(1)=0.
                      if(idtiltfore == 1):
                        var(2)=(-acftspd_we*dcwe_dt-acftspd_sn*dcsn_dt
                                -acftspd_nz*dcnz_dt)
                               *conv
                      else
                        var(2)=0.
                        xmat_vsurf(2,2)=xmat_vsurf(2,2)+wghtsurf_ray
                      endif
                    endif
#
                    if(iaftfore == -1):
                      if(idrotaaft == 1):
                        var(3)=(-acftspd_we*dcwe_dr-acftspd_sn*dcsn_dr
                                -acftspd_nz*dcnz_dr)
                               *conv
                      else
                        var(3)=0.
                        xmat_vsurf(3,3)=xmat_vsurf(3,3)+wghtsurf_ray
                      endif
                      var(4)=0.
                    else
                      var(3)=0.
                      if(idrotafore == 1):
                        var(4)=(-acftspd_we*dcwe_dr-acftspd_sn*dcsn_dr
                                -acftspd_nz*dcnz_dr)
                               *conv
                      else
                        var(4)=0.
                        xmat_vsurf(4,4)=xmat_vsurf(4,4)+wghtsurf_ray
                      endif
                    endif
#
                    if(idpitch == 1):
                      var(5)=(-acftspd_we*dcwe_dp-acftspd_sn*dcsn_dp
                              -acftspd_nz*dcnz_dp)
                             *conv
                    else
                      var(5)=0.
                      xmat_vsurf(5,5)=xmat_vsurf(5,5)+wghtsurf_ray
                    endif
#
                    if(idhdg == 1):
                      var(6)=(-acftspd_we*dcwe_dh
                              -acftspd_sn*dcsn_dh)
                             *conv
                    else
                      var(6)=0.
                      xmat_vsurf(6,6)=xmat_vsurf(6,6)+wghtsurf_ray
                    endif
#
                    var(7)=0.
                    var(8)=0.
                    var(9)=0.
                    var(10)=0.
                    var(11)=0.
#
                    if(idvh == 1):
                      var(12)=-duacft_dv*cwe-dvacft_dv*csn
                    else
                      var(12)=0.
                      xmat_vsurf(12,12)=xmat_vsurf(12,12)+wghtsurf_ray
                    endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print('    VAR_VSURF(1->12):',(var(i),i=1,12)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** ADD TO XMAT_vsurf(1->NVAR,1->NVAR) AND VECT_vsurf(1->NVAR)
#******************************************************************
#
                    do i=1,nvar
                       do j=1,nvar
    	                  xmat_vsurf(i,j)=xmat_vsurf(i,j)
                      	                  +wghtsurf_ray*var(i)*var(j)
                       enddo
                       vect_vsurf(i)=vect_vsurf(i)
                                     +wghtsurf_ray*var(i)*vdopsurf_ray
                    enddo
#
#******************************************************************
#**** ADD TO COVARIANCE MATRIX FOR FIELD "VDOP_surf"
#******************************************************************
#
                    do i=1,nvar
                       rms_var_vsurf(i)=rms_var_vsurf(i)
                                        +wghtsurf_ray*var(i)*var(i)
                       do j=1,nvar
                          corr_var(i,j)=corr_var(i,j)
                                        +wghtsurf_ray*var(i)*var(j)
                       enddo
                    enddo
#
#******************************************************************
#**** CASE "VDOP_surf" and/or "DVDOP_insitu" ONLY :
#**** -> RGE-DLY_aft,RGE-DLY_aft,D_XWE,D_YSN,D_ZACFT CANNOT BE CALCULATED
#******************************************************************
#
                    if(rw_dzsurf <= 0.):
                      do ij=7,11
                         xmat_vsurf(ij,ij)=xmat_vsurf(ij,ij)
                                           +wghtsurf_ray
                      enddo
                    endif
#
#******************************************************************
#**** ARRAYS FOR "SIS_EL_*" FILE #50
#******************************************************************
#
                    vs_dhor(iradar_ray,n_vsurf(iradar_ray))
                           =side*dsurf_ray*celh
                    vs_vdopsurf(iradar_ray,n_vsurf(iradar_ray))
                           =vdopsurf_ray
#
	          else  !!  of  !! if(abs(vdopsurf_ray) < vdopsurf_max) !!
	            ndismiss_vdopsurf(iradar_ray)
                     =ndismiss_vdopsurf(iradar_ray)+1
	          endif  !! of !! if(abs(vdopsurf_ray) < vdopsurf_max) !!
#
	        else  !!  of  !!  if(vdop_corr(ig_refmax) > -900.) !!
	          ndismiss_vdopcorr(iradar_ray)
                   =ndismiss_vdopcorr(iradar_ray)+1
	        endif  !!  of  !!  if(vdop_corr(ig_refmax) > -900.) !!
#
	      else  !!  of  !! if(kvsurf == 1 and acftspd_hor > 0.)  !!
	        if(acftspd_hor <= 0.)ndismiss_vhacft(iradar_ray)
                                 =ndismiss_vhacft(iradar_ray)+1
	      endif  !!  of  !! if(kvsurf == 1 and acftspd_hor > 0.)  !!
#
            endif  !!  of  !! if(abs(d_hsurf) < dhsurf_max)  !!
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!          else !!  of  !!  if(xsurf_ray > xmin_dtm ... )  !!
#!!!!            if( nb_ray(iradar_ray) == 10*(nb_ray(iradar_ray)/10) ):
#!!!!              print('     !!!! OUT OF DTM LIMITS !!!!'
#!!!!              print('     !!!! X_ray :',xsurf_ray
#!!!!                     ,' XDTM_min,max :',xmin_dtm,xmax_dtm,' !!!!'
#!!!!              print('     !!!! Y_ray :',ysurf_ray
#!!!!                     ,' YDTM_min,max :',ymin_dtm,ymax_dtm,' !!!!'
#!!!!            endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          endif  !!  of  !!  if(xsurf_ray > xmin_dtm ... )  !!
        endif  !!  of  !!  if(hsurf_ray > -999. and wghtsurf_ray > 0.)  !!
      endif  !!  of  !!  if(kdzsurf+kvsurf >= 1 ... )  !!
#
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
        if(ictrl_contray == 1):
#
          init=0
          do ig=1,ngates_insitu_max
	     d_ig=dgate_corr(ig)
	     if(     ze(ig) > -900.
                 and vdop_corr(ig) > -900.):
#
	       xis=0.
	       svis=0.
	       xrad=0.
	       svrad=0.
               if(init == 0):
                 init=1
                 xis=xpmin_contray+1.
	         svis=xis*proj_wind
	       else
	         init=2
                 if(d_ig < dmax_insitu):
                   xis=(dmax_insitu-d_ig)/ddg
                   svis=xis*proj_wind
                   igmin=1
                 else
                   igmin=((d_ig-dmax_insitu)/ddg)
                 endif
                 do jg=igmin,max0(1,ig-1)
                    if(abs(vdop_corr(jg)) < vdop_max):
	              xrad=xrad+1.
	              svrad=svrad+vdop_corr(jg)
                    endif
	         enddo
               endif
               xctrl=xis+xrad
	       if(xctrl >= xpmin_contray):
                 vctrl=(svis+svrad)/xctrl
                 dv=vdop_corr(ig)-vctrl
	         idepl=0
	         if(ichoice_vdop == 1.or.ichoice_vdop == 2):
                   if(abs(dv) > vnyq):
		     idepl=1
		     do while (dv > +vnyq)
  		        vdop_corr(ig)=vdop_corr(ig)-2.*vnyq
                        dv=vdop_corr(ig)-vctrl
                     enddo
		     do while (dv < -vnyq)
		        vdop_corr(ig)=vdop_corr(ig)+2.*vnyq
                        dv=vdop_corr(ig)-vctrl
                     enddo
                   endif
                 endif
                 if(abs(dv) > dvdop_max):
                   vdop_corr(ig)=-999.
	           if(init == 1)init=0
                 endif
	       endif
#
	     endif
          enddo
#
        endif    !!!!  OF if(ictrl_contray == 1)
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      itest=1
      do ig=1,ngates_insitu_max
         if(     ze(ig) > -900.
               and vdop_corr(ig) > -900.)itest=1
      enddo
      if(     itest == 1
          and nb_ray(iradar_ray) == 5*(nb_ray(iradar_ray)/5)):
        print(' '
        print(' ',1000*ihhmmss+ims_ray
               ,' IRADAR:',iradar_ray
               ,' NO_RAY:',nb_ray(iradar_ray)
        print('    ROTA,TILT_RAY:',rota_ray,tilt_ray
        print('    ROLL,PITCH,HDG,DRIFT_ACFT:',roll_acft
               ,pitch_acft,hdg_acft,drift_acft
        print('    AZ_EAST:',azeast_ray,' EL_HOR:',elhor_ray
      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        do ig=1,ngates_insitu_max

#	if(     ze(ig) > 10.
#            and abs(vr(ig)) > 0.
#            and abs(vr(ig)) < vdop_max
#            and abs(vs(ig)) > 0.
#            and abs(vs(ig)) < vdop_max
#            and abs(vl(ig)) > 0.
#            and abs(vl(ig)) < vdop_max
#            and proj_acftspd > -900.
#            and dgate_corr(ig) < 10.
#            and elhor_ray < 5.
#            and elhor_ray > -5.     ):	! 111111
#
#       d_vs_vl=vs(ig)-vl(ig)     ! Olivier
#       kvsl=ifix((d_vs_vl/vnyq_el)*0.5)+5      ! Olivier
#       if(kvsl >= 1 and kvsl <= 9):         ! Olivier
#         vs_depl=vs(ig)+xms(kvsl)*vnyq_el       ! Olivier
#         vl_depl=vl(ig)+xml(kvsl)*vnyq_el       ! Olivier
#         vsl_depl=(vs_depl+vl_depl)/2.         ! Olivier
#
#         if(     abs(vs_depl-vl_depl) < vnyq_el/2.
# c            and abs(vr(ig)-vsl_depl) < vnyq_el/2.     ): ! 112 Oliv
#		print('IG= ',ig
#		print('VR= ',vr(ig)
#		print('VS,VL= ',vs(ig),vl(ig)
#		print('VS_depl,VL_depl= ',vs_depl,vl_depl
#		print('VSL_depl= ',vsl_depl
#
#	    if(proj_acftspd > -900.):
#	      v_corr=vr(ig)+proj_acftspd                ! Olivier
#	      vdop_corr(ig)=v_corr
#              print('    -> VDOP_CORR :',v_corr       ! Olivier
#	    endif
#
#         endif
#
#       endif
#	endif                               ! Olivier

#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED dV_dopinsitu WITH dXXX_GUESS
#------------------------------------------------------------------
      if(ig == 1 and isim == 1):
        ze(1)=999.
        dv_dopinsitu=-( wa_we_true*dcwe_dt_true
                       +wa_sn_true*dcsn_dt_true
                       +wa_nz*dcnz_dt_true)
                      *dtilt_guess*conv
                     -( wa_we_true*dcwe_dr_true
                       +wa_sn_true*dcsn_dr_true
                       +wa_nz*dcnz_dr_true)
                      *drota_guess*conv
                     -( wa_we_true*dcwe_dp_true
                       +wa_sn_true*dcsn_dp_true
                       +wa_nz*dcnz_dp_true)
                      *dpitch_guess*conv
                     -( wa_we_true*dcwe_dh_true
                       +wa_sn_true*dcsn_dh_true
                       +wa_nz*dcnz_dh_true)
                      *dhdg_guess*conv
                     -(-cwe_true*duacft_dv_true
                       -csn_true*dvacft_dv_true)*dvh_guess
	vdop_corr(1)=dv_dopinsitu+proj_wind_true
	do iig=2,ngates_insitu_max
	   ze(iig)=-999.
	   vdop_corr(iig)=-999.
	enddo
      endif
#------------------------------------------------------------------
           if(     ze(ig) > -900.
               and vdop_corr(ig) > -900.):
#
             wghtinsitu_ig=1.-0.5*dgate_corr(ig)/dmax_insitu
#
             dv_dopinsitu=vdop_corr(ig)-proj_wind
#
             if(abs(dv_dopinsitu) < dvdopinsitu_max):
#
#******************************************************************
#**** ADD WEIGHTS AND DVDOP_insitu
#******************************************************************
#
               n_dvinsitu(iradar_ray)=n_dvinsitu(iradar_ray)+1
               ssurfins=ssurfins+wghtinsitu_ig
	       swinsitu_sweep(iradar_ray)
                =swinsitu_sweep(iradar_ray)+wghtinsitu_ig
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      if( nb_ray(iradar_ray) == 5*(nb_ray(iradar_ray)/5) ):
#!!!!        print('    IG=',ig,' -> DVDOPINSITU_RAY :',dv_dopinsitu
#!!!!        print('       SWVSURF_SWEEP(',iradar_ray,') :'
#!!!!               ,swvsurf_sweep(iradar_ray)
#!!!!      endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
	       dvinsitusweep_mean(iradar_ray)
                =dvinsitusweep_mean(iradar_ray)
                 +wghtinsitu_ig*dv_dopinsitu
	       dvinsitusweep_rms(iradar_ray)
                =dvinsitusweep_rms(iradar_ray)
                 +wghtinsitu_ig*dv_dopinsitu*dv_dopinsitu
#
               swdvinsitu_tot=swdvinsitu_tot+wghtinsitu_ig
	       swdvminsitu_tot=swdvminsitu_tot
                               +wghtinsitu_ig*dv_dopinsitu
	       swdv2insitu_tot=swdv2insitu_tot
                               +wghtinsitu_ig
                                *dv_dopinsitu*dv_dopinsitu
               swadvinsitu_tot=swadvinsitu_tot
                               +wghtinsitu_ig*abs(dv_dopinsitu)
#
               s_vpv(iradar_ray,ilr)=s_vpv(iradar_ray,ilr)
                                     +wghtinsitu_ig
               sv_vpv(iradar_ray,ilr)=sv_vpv(iradar_ray,ilr)
                                      +wghtinsitu_ig*dv_dopinsitu
               svv_vpv(iradar_ray,ilr)=svv_vpv(iradar_ray,ilr)
                                       +wghtinsitu_ig
                                        *dv_dopinsitu*dv_dopinsitu
               x_vpv(iradar_ray,ilr)=x_vpv(iradar_ray,ilr)
                                     +wghtinsitu_ig
               xv_vpv(iradar_ray,ilr)=xv_vpv(iradar_ray,ilr)
                                      +wghtinsitu_ig*dv_dopinsitu
               xvv_vpv(iradar_ray,ilr)=xvv_vpv(iradar_ray,ilr)
                                       +wghtinsitu_ig
                                        *dv_dopinsitu*dv_dopinsitu
#
#******************************************************************
#**** VALUES OF VAR(1->NVAR) FOR FIELD "DV_insitu"
#****  - VAR(1->6) -> [dT_aft,dT_fore,dR_aft,dR_fore,dP,dH] in DEGREES
#****  - VAR(7->11) -> [RD_aft,RD_fore,dXwe,dYsn,dZ] in HECTOMETERS
#****  - VAR(12) -> [dVH] in METER/SECOND
#******************************************************************
#
               if(iaftfore == -1):
                 if(idtiltaft == 1):
                   var(1)=( wa_we*dcwe_dt+wa_sn*dcsn_dt
                           +wa_nz*dcnz_dt)*conv
                 else
                   var(1)=0.
                   xmat_dvinsitu(1,1)=xmat_dvinsitu(1,1)
                                      +wghtinsitu_ig
                 endif
                 var(2)=0.
               else
                 var(1)=0.
                 if(idtiltfore == 1):
                   var(2)=( wa_we*dcwe_dt+wa_sn*dcsn_dt
                           +wa_nz*dcnz_dt)*conv
                 else
                   var(2)=0.
                   xmat_dvinsitu(2,2)=xmat_dvinsitu(2,2)
                                      +wghtinsitu_ig
                 endif
               endif
#
               if(iaftfore == -1):
                 if(idrotaaft == 1):
                   var(3)=( wa_we*dcwe_dr+wa_sn*dcsn_dr
                           +wa_nz*dcnz_dr)*conv
                 else
                   var(3)=0.
                   xmat_dvinsitu(3,3)=xmat_dvinsitu(3,3)
                                      +wghtinsitu_ig
                 endif
                 var(4)=0.
               else
                 var(3)=0.
                 if(idrotafore == 1):
                   var(4)=( wa_we*dcwe_dr+wa_sn*dcsn_dr
                           +wa_nz*dcnz_dr)*conv
                 else
                   var(4)=0.
                   xmat_dvinsitu(4,4)=xmat_dvinsitu(4,4)
                                      +wghtinsitu_ig
                 endif
               endif
#
               if(idpitch == 1):
                 var(5)=( wa_we*dcwe_dp+wa_sn*dcsn_dp
                         +wa_nz*dcnz_dp)*conv
               else
                 var(5)=0.
                 xmat_dvinsitu(5,5)=xmat_dvinsitu(5,5)
                                    +wghtinsitu_ig
               endif
#
               if(idhdg == 1):
                 var(6)=(wa_we*dcwe_dh+wa_sn*dcsn_dh)*conv
               else
                 var(6)=0.
                 xmat_dvinsitu(6,6)=xmat_dvinsitu(6,6)
                                    +wghtinsitu_ig
               endif
#
               var(7)=0.
               var(8)=0.
               var(9)=0.
               var(10)=0.
               var(11)=0.
#
               if(idvh == 1):
                 var(12)=-duacft_dv*cwe-dvacft_dv*csn
               else
                 var(12)=0.
                 xmat_dvinsitu(12,12)=xmat_dvinsitu(12,12)
                                      +wghtinsitu_ig
               endif
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#!!!!      print('    VAR_DVINSITU(1->12):',(var(i),i=1,12)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#******************************************************************
#**** ADD TO XMAT_dvinsitu(1->NVAR,1->NVAR) AND VECT_dvinsitu(1->NVAR)
#******************************************************************
#
               do i=1,nvar
   	          do j=1,nvar
 	             xmat_dvinsitu(i,j)=xmat_dvinsitu(i,j)
                                        +wghtinsitu_ig*var(i)*var(j)
 	          enddo
 	          vect_dvinsitu(i)=vect_dvinsitu(i)
                                   +wghtinsitu_ig*var(i)*dv_dopinsitu
               enddo
#
#******************************************************************
#**** ADD TO COVARIANCE MATRIX FOR FIELD "DVDOP_insitu"
#******************************************************************
#
               do i=1,nvar
                  rms_var_vinsitu(i)=rms_var_vinsitu(i)
                                     +wghtinsitu_ig*var(i)*var(i)
                  do j=1,nvar
                     corr_var(i,j)=corr_var(i,j)
                                   +wghtinsitu_ig*var(i)*var(j)
                  enddo
               enddo
#
#******************************************************************
#**** CASE "VDOP_surf" and/or "DVDOP_insitu" ONLY :
#**** -> RGE-DLY_aft,RGE-DLY_aft,D_XWE,D_YSN,D_ZACFT CANNOT BE CALCULATED
#******************************************************************
#
               if(rw_dzsurf <= 0.):
                 do ij=7,11
                    xmat_vsurf(ij,ij)=xmat_vsurf(ij,ij)
                                      +wghtinsitu_ig
                 enddo
               endif
#
#******************************************************************
#**** ARRAYS FOR "SIS_EL_*" FILE
#******************************************************************
#
               vi_dhor(iradar_ray,n_dvinsitu(iradar_ray))
                       =side*dgate_corr(ig)*celh
               vi_vdop(iradar_ray,n_dvinsitu(iradar_ray))=vdop
               vi_vinsitu(iradar_ray,n_dvinsitu(iradar_ray))=proj_wind
#
             endif  !!  of  !!  if(abs(dv_dopinsitu) < dvdopinsitu_max)  !!
#
           endif  !!  of  !!  if(ze(ig) > -900. ... )  !!
        enddo !!  of  !!  do ig=1,ngates_insitu_max  !!
#
      endif  !!  of  !!  if(kdvinsitu == 1 and ngates_insitu_max > 1)  !!
#
#******************************************************************
#**** STORE FOR NEXT RAY
#******************************************************************
#
      istart_sweep(iradar_ray)=1
      swp_prev(iradar_ray)=swp(iradar_ray)
      vnyq_prev=vnyq
      rota_prev(iradar_ray)=rota_ray
      tilt_prev=tilt_ray
#
      go to 1
#
  3   stop
      end

