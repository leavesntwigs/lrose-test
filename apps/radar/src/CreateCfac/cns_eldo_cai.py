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
        int  nfile,ifile # total number of netcdf text file, current file number
        islastfile = False
        int iopen

# Variables declarations previous in Franks' common block, which has been deleted

# From COMMON /CSPD_OU_CELV/
      integer*4 nb_portes
d_porte = np.zeros(MAXPORAD, dtype=np.float16)

# From COMMON /CFAC/
#
      # float corr_azest(MAXRAD),corr_elhor(MAXRAD),corr_dist(MAXRAD)
corr_azest = np.zeros(MAXRAD, dtype=np.float16)
corr_elhor = np.zeros(MAXRAD, dtype=np.float16)
corr_dist = np.zeros(MAXRAD, dtype=np.float16)
corr_lon = np.zeros(MAXRAD, dtype=np.float16)
corr_lat = np.zeros(MAXRAD, dtype=np.float16)
corr_p_alt = np.zeros(MAXRAD, dtype=np.float16)
corr_r_alt = np.zeros(MAXRAD, dtype=np.float16)
corr_vwe_av = np.zeros(MAXRAD, dtype=np.float16)
corr_vsn_av = np.zeros(MAXRAD, dtype=np.float16)
corr_vnz_av = np.zeros(MAXRAD, dtype=np.float16)
corr_cap = np.zeros(MAXRAD, dtype=np.float16)
corr_roul = np.zeros(MAXRAD, dtype=np.float16)
corr_tang = np.zeros(MAXRAD, dtype=np.float16)
corr_derv = np.zeros(MAXRAD, dtype=np.float16)
corr_rota = np.zeros(MAXRAD, dtype=np.float16)
corr_incl = np.zeros(MAXRAD, dtype=np.float16)

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
# float*4 is dtype=np.float32 in python
      # float*4  dgate_corr = np.zeros(MAXPORT, dtype=np.float32)
dgate_corr = np.zeros(MAXPORT, dtype=np.float32)
dgate_true = np.zeros(MAXPORT, dtype=np.float32)
vdop_corr = np.full(MAXPORT, -999, dtype=np.float32)
xms = np.zeros(9, dtype=np.float32)
xml = np.zeros(9, dtype=np.float32)
rota_start = np.full(2, -999, dtype=np.float32)
rota_end = np.full(2, -999, dtype=np.float32)
xp = np.zeros(2, dtype=np.float32)
ssc = np.zeros(2, dtype=np.float32)
scc = np.zeros(2, dtype=np.float32)
sxa = np.zeros(2, dtype=np.float32)
sya = np.zeros(2, dtype=np.float32)
sza = np.zeros(2, dtype=np.float32)
sacfthspd = np.zeros(2, dtype=np.float32)
stime = np.zeros(2, dtype=np.float32)
xp_acft = np.zeros(2, dtype=np.float32)
su_acft = np.zeros(2, dtype=np.float32)
sv_acft = np.zeros(2, dtype=np.float32)
sw_acft = np.zeros(2, dtype=np.float32)
su_wind = np.zeros(2, dtype=np.float32)
sv_wind = np.zeros(2, dtype=np.float32)
sw_wind = np.zeros(2, dtype=np.float32)
xp_wind = np.zeros(2, dtype=np.float32)
stilt = np.zeros(2, dtype=np.float32)
stilt2 = np.zeros(2, dtype=np.float32)
xsweeps = np.zeros(2, dtype=np.float32)
# rota_prev(iradar)=-999
rota_prev = np.full(2, -999, dtype=np.float32)
swdzsurf_sweep = np.zeros(2, dtype=np.float32)
dzsurfsweep_mean = np.zeros(2, dtype=np.float32)
dzsurfsweep_rms = np.zeros(2, dtype=np.float32)
swvsurf_sweep = np.zeros(2, dtype=np.float32)
vsurfsweep_mean = np.zeros(2, dtype=np.float32)
vsurfsweep_rms = np.zeros(2, dtype=np.float32)
swinsitu_sweep = np.zeros(2, dtype=np.float32)
dvinsitusweep_mean = np.zeros(2, dtype=np.float32)
dvinsitusweep_rms = np.zeros(2, dtype=np.float32)
var = np.zeros(nvar, dtype=np.float32)
xmat = np.zeros((nvar,nvar), dtype=np.float32)
vect = np.zeros(nvar, dtype=np.float32)
xinv = np.zeros((nvar,nvar), dtype=np.float32)
res = np.zeros(nvar, dtype=np.float32)
vect_dzsurf = np.zeros(nvar, dtype=np.float32)

xmat_dzsurf = np.zeros((nvar,nvar), dtype)=np.float32)
vect_vsurf = np.zeros((nvar), dtype)=np.float32)
xmat_vsurf = np.zeros((nvar,nvar), dtype)=np.float32)
vect_dvinsitu = np.zeros((nvar), dtype)=np.float32)
xmat_dvinsitu = np.zeros((nvar,nvar), dtype)=np.float32)
alt_dtm = np.zeros((nxysurfmax,nxysurfmax), dtype)=np.float32)
swdzsurf_wri = np.zeros((nxysurfmax,nxysurfmax), dtype)=np.float32)
sw_or_altsurf_wri = np.zeros((nxysurfmax,nxysurfmax), dtype)=np.float32)
zs_rot = np.zeros((2,500), dtype)=np.float32)
zs_el = np.zeros((2,500), dtype)=np.float32)
zs_az = np.zeros((2,500), dtype)=np.float32)
zs_dsurf = np.zeros((2,500), dtype)=np.float32)
zs_dhor = np.zeros((2,500), dtype)=np.float32)
zs_zsurf = np.zeros((2,500), dtype)=np.float32)
zs_hsurf = np.zeros((2,500), dtype)=np.float32)
vs_dhor = np.zeros((2,500), dtype)=np.float32)
vs_vdopsurf = np.zeros((2,500), dtype)=np.float32)
vi_dhor = np.zeros((2,500), dtype)=np.float32)
vi_vdop = np.zeros((2,500), dtype)=np.float32)
vi_vinsitu = np.zeros((2,500), dtype)=np.float32)

rms_var_zsurf = np.zeros(nvar, dtype=np.float32)
rms_var_vsurf = np.zeros(nvar, dtype=np.float32)
rms_var_vinsitu = np.zeros(nvar, dtype=np.float32)
corr_var = np.zeros((nvar,nvar), dtype=np.float32)
s_vpv = np.zeros((2,2), dtype=np.float32)
sv_vpv = np.zeros((2,2), dtype=np.float32)
svv_vpv = np.zeros((2,2), dtype=np.float32)
x_vpv = np.zeros((2,2), dtype=np.float32)
xv_vpv = np.zeros((2,2), dtype=np.float32)
xvv_vpv = np.zeros((2,2), dtype=np.float32)
#
#       integer*2 iyymmdd(3),ig_dismiss(15)
    iyymmdd = np.zeros(3, dtype=np.int16)
    ig_dismiss = np.zeros(15, dtype=np.int16)
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
# done at np.zeros, and np.full
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
#      islastfile = False 
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
#           islastfile=1
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
islastfile = False 

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
            islastfile = True 
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

    ifile += 1
    if ifile == nfile:
        islastfile = True 

    except EOFError:
        iopen = 0  # jump here on EOF

#******************************************************************
#**** CONTROL FOR THE END OF THE READING ALL TEXT FILES
#******************************************************************
#
  # end while ifile < nfile
  7   iend=0  # What is the use of iend? boolean? or state? State: iend = 1 for end of sweep
              # iend = 2 for end of considered period.
if(ifile == nfile  and  islastfile  == True):
     iend=2 # end_of_considered_period = True
     print(' '
     print('**** END OF READING ALL TEXT FILES ****'
#endif

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
      if(ihhmmss <= 0)go to 1 # read next file
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
        if(iend .ne. 2) go to 1   # read next file ! only when end of text file not reached
# CAI-STOP
      endif
      if(time_ks > tmax):
	iend=2
	print(' '
	print(' HHMMSSms:',100*ihhmmss+ims_rdl
               ,' > HHMMSSms_max:',100*ihms_max
      endif
      if(iend == 2)go to 2
      # if end_of_considered_period
#
#******************************************************************
#**** CONTROL OF LAT, LON, P_ALT AND R_ALT
#******************************************************************
#
      if(    abs(lat_av) < 0.001
         .or.abs(lon_av) < 0.001
         .or.(     abs(p_alt_av) < 0.001
               and abs(r_alt_av) < 0.001))go to 1 # read next file

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
        go to 1 # read next file
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
	go to 1 # read next file
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
      iend_ge_1()
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
        go to 1 # read next file
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
        go to 1 # read next file
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

      kdzsurf_kvsurf_ge_1()
#
#******************************************************************
#**** CASE "DVDOP_insitu"
#**** (if D<DMAX_insitu and ||sin(ELEV_HOR)||<0.1)
#******************************************************************
#
      dvdop_insitu()
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
      go to 1 # read next file
#
  3   stop
      end

