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

import os.path
import getopt
import numpy as np
# import read_input_parameters
import read_eldora_data_file
import process_ray
import iend_ge_1
import iend_equals_2
import control_for_end_of_all_text_files_wo_gotos
import write_aft_cfac

def enough_points(ssurfins, ssurfins_min):
    return ssurfins > ssurfins_min

# arg is a dictionary of parameters
def cns_eldo(input_parameters):

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

    MAXRAD=2
    MAXFREQ=5
    MAXPARM=10
    MAXPORT=2000
    MAXFREQRAD=MAXFREQ*MAXPARM
    MAXPARAD=MAXRAD*MAXPARM
    MAXPORAD=MAXRAD*MAXPORT
    MAXPARIS=256

    # Variable for reading text files

#    int ntimes    # Number of times rays were collected --- Number of rays
#    int nranges   # Number of range gates per time  --- Number of gates for each ray
#    int nsweep    # Sweep number in each netcdf file; Used to identify different sweep
#
#    np.int32 counter  # Ray number
#
#
#    int start_year,start_mon,start_day
#    int start_hour,start_min,start_sec
#
#
#    !  Scalar variable for correction factors
#
#    float azimuth_correction
#    float elevation_correction
#    float range_correction
#    float longitude_correction
#    float latitude_correction
#    float pressure_altitude_correction
#    float radar_altitude_correction
#    float ew_gound_speed_correction
#    float ns_ground_speed_correction
#    float vertical_velocity_correction
#    float heading_correction
#    float roll_correction
#    float pitch_correction
#    float drift_correction
#    float rotation_correction
#    float tilt_correction

#! Variable for cfac files
#    float tilt_corr_aft
#    float tilt_corr_fore
#    float rot_angle_corr_aft
#    float rot_angle_corr_fore
#    float pitch_corr_cfac
#    float drift_corr_cfac
#    float range_delay_corr_aft
#    float range_delay_corr_fore
#    float pressure_alt_corr
#    float ew_gndspd_corr
    range_delay_corr_aft = 0.0
    pressure_alt_corr = 0.0
    ew_gndspd_corr = 0.0
    pitch_corr_cfac = 0.0
    drift_corr_cfac = 0.0
    rot_angle_corr_aft = 0.0
    tilt_corr_aft = 0.0 
#
#! Scaler variable for each ray
#
#    int sweep_number
#
#    float  time
#    float azimuth
#    float elevation
#    float latitude
#    float longitude
#    float altitude
#    float altitude_agl
#    float heading
#    float roll
#    float pitch
#    float drift
#    float rotation
#    float tilt
#    float ew_velocity
#    float ns_velocity
#    float vertical_velocity
#    float ew_wind
#    float ns_wind
#    float vertical_wind
#
## ! One dimensional array of DBZ, VR, SW, NCP, etc
#
#    float range(MAXPORT)
#    float ZE(MAXPORT),NCP(MAXPORT),VR(MAXPORT),SW(MAXPORT)
#    float VS(MAXPORT),VL(MAXPORT),VG(MAXPORT),VU(MAXPORT)
#
## ! Variables for input file list
##     CHARACTER(len=80) infilename
#    int  nfile,ifile # total number of netcdf text file, current file number
#    islastfile = False
#    int iopen

# Variables declarations previous in Franks' common block, which has been deleted

# From COMMON /CSPD_OU_CELV/
#    np.int32 nb_portes
    # d_porte = np.zeros(MAXPORAD, dtype=np.float16)

# From COMMON /CFAC/
#
    # float corr_azest(MAXRAD),corr_elhor(MAXRAD),corr_dist(MAXRAD)
#    corr_azest = np.zeros(MAXRAD, dtype=np.float16)
#    corr_elhor = np.zeros(MAXRAD, dtype=np.float16)
#    corr_dist = np.zeros(MAXRAD, dtype=np.float16)
#    corr_lon = np.zeros(MAXRAD, dtype=np.float16)
#    corr_lat = np.zeros(MAXRAD, dtype=np.float16)
#    corr_p_alt = np.zeros(MAXRAD, dtype=np.float16)
#    corr_r_alt = np.zeros(MAXRAD, dtype=np.float16)
#    corr_vwe_av = np.zeros(MAXRAD, dtype=np.float16)
#    corr_vsn_av = np.zeros(MAXRAD, dtype=np.float16)
#    corr_vnz_av = np.zeros(MAXRAD, dtype=np.float16)
#    corr_cap = np.zeros(MAXRAD, dtype=np.float16)
#    corr_roul = np.zeros(MAXRAD, dtype=np.float16)
#    corr_tang = np.zeros(MAXRAD, dtype=np.float16)
#    corr_derv = np.zeros(MAXRAD, dtype=np.float16)
#    corr_rota = np.zeros(MAXRAD, dtype=np.float16)
#    corr_incl = np.zeros(MAXRAD, dtype=np.float16)

# From COMMON /RYIB/
#
#    np.int16 ih_rdl,im_rdl,is_rdl,ims_rdl
#    np.int32 num_swp,j_julien,etat_rdl,no_rdl
#    float azest_rdl,elhor_rdl,puiscre_em,vit_bal_rdl
#
## From COMMON /ASIB/ ************************************************
##
#     float  lon_av,lat_av,p_alt_av,r_alt_av
#     float    vwe_av,vsn_av,vnz_av
#          ,cap_av,roul_av,tang_av,derv_av
#          ,rota_rdl,incl_rdl
#          ,vent_we,vent_sn,vent_nz
#          ,chg_cap,chg_tang

# CAI-STOP
#
# float*4 is dtype=np.float32 in python
      # float*4  dgate_corr = np.zeros(MAXPORT, dtype=np.float32)
    dgate_corr = np.zeros(MAXPORT, dtype=np.float32)
    dgate_true = np.zeros(MAXPORT, dtype=np.float32)
    vdop_corr = np.full(MAXPORT, -999, dtype=np.float32)
    xms = np.zeros(9, dtype=np.float32)
    xml = np.zeros(9, dtype=np.float32)
    #rota_start = np.full(2, -999, dtype=np.float32)
    #rota_end = np.full(2, -999, dtype=np.float32)
    xp = np.zeros(2, dtype=np.float32)
    #ssc = np.zeros(2, dtype=np.float32)
    #scc = np.zeros(2, dtype=np.float32)
    #sxa = np.zeros(2, dtype=np.float32)
    #sya = np.zeros(2, dtype=np.float32)
    #sza = np.zeros(2, dtype=np.float32)
    sacfthspd = np.zeros(2, dtype=np.float32)
    # stime = np.zeros(2, dtype=np.float32)
    xp_acft = np.zeros(2, dtype=np.float32)
    su_acft = np.zeros(2, dtype=np.float32)
    sv_acft = np.zeros(2, dtype=np.float32)
    sw_acft = np.zeros(2, dtype=np.float32)
    su_wind = np.zeros(2, dtype=np.float32)
    sv_wind = np.zeros(2, dtype=np.float32)
    sw_wind = np.zeros(2, dtype=np.float32)
    xp_wind = np.zeros(2, dtype=np.float32)
    # stilt = np.zeros(2, dtype=np.float32)
    # stilt2 = np.zeros(2, dtype=np.float32)
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

    xmat_dzsurf = np.zeros((nvar,nvar), dtype=np.float32)
    vect_vsurf = np.zeros((nvar), dtype=np.float32)
    xmat_vsurf = np.zeros((nvar,nvar), dtype=np.float32)
    vect_dvinsitu = np.zeros((nvar), dtype=np.float32)
    xmat_dvinsitu = np.zeros((nvar,nvar), dtype=np.float32)
    alt_dtm = np.zeros((nxysurfmax,nxysurfmax), dtype=np.float32)
    swdzsurf_wri = np.zeros((nxysurfmax,nxysurfmax), dtype=np.float32)
    sw_or_altsurf_wri = np.zeros((nxysurfmax,nxysurfmax), dtype=np.float32)
    zs_rot = np.zeros((2,500), dtype=np.float32)
    zs_el = np.zeros((2,500), dtype=np.float32)
    zs_az = np.zeros((2,500), dtype=np.float32)
    zs_dsurf = np.zeros((2,500), dtype=np.float32)
    zs_dhor = np.zeros((2,500), dtype=np.float32)
    zs_zsurf = np.zeros((2,500), dtype=np.float32)
    zs_hsurf = np.zeros((2,500), dtype=np.float32)
    vs_dhor = np.zeros((2,500), dtype=np.float32)
    vs_vdopsurf = np.zeros((2,500), dtype=np.float32)
    vi_dhor = np.zeros((2,500), dtype=np.float32)
    vi_vdop = np.zeros((2,500), dtype=np.float32)
    vi_vinsitu = np.zeros((2,500), dtype=np.float32)
    
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
#       np.int16 iyymmdd(3),ig_dismiss(15)
    iyymmdd = np.zeros(3, dtype=np.int16)
    ig_dismiss = np.zeros(15, dtype=np.int16)
#
    nb_ray = np.zeros(2, dtype=np.int32)
    nb_sweep = np.zeros(2, dtype=np.int32)
    n_dzsurf = np.zeros(2, dtype=np.int32)
    n_vsurf = np.zeros(2, dtype=np.int32)
    n_dvinsitu = np.zeros(2, dtype=np.int32)
    nsurf_wri = np.zeros(2, dtype=np.int32)
    ndismiss_vhacft = np.zeros(2, dtype=np.int32)
    ndismiss_vdopcorr = np.zeros(2, dtype=np.int32)
    ndismiss_vdopsurf = np.zeros(2, dtype=np.int32)
    swp = np.zeros(2, dtype=np.int32)
    swp_prev = np.zeros(2, dtype=np.int32)
    ndop_ok = np.zeros(2, dtype=np.int32)
    nref_ok = np.zeros(2, dtype=np.int32)
    istart_sweep = np.zeros(2, dtype=np.int32)
    itab = np.zeros(nxysurfmax, dtype=np.int32)
    ihms_dtm = np.zeros(6, dtype=np.int32)
    # ialtsurf_wri = np.zeros(nxysurfmax, dtype=np.int32)

    iradar_ray = 0
    iaftfore = 0
#

    path_abs = ""  # 18 characters
    directory = ""  # 60 characters
    dir_read = ""  # 60 characters
    fich_sis = ""  # 30 characters
    dtm_file = ""  # 50 characters
    fich_cornav = ""  # 30 characters
    wrisurfile = ""  # 50 characters
    yymmdd_dtm = ""  # 12 characters
    suff_dtm = ""  # 20 characters
    yymmdd = input_parameters["yymmdd"]  # 12 characters
    c_hms_min = ""  # 7 characters
    c_hms_max = ""  # 7 characters
    argu = "" # 30 characters

#
#     include '/home/users/rouf/SOURCES/ELDO/mes_commons'
#
# CAI-START: This is common block for transfering data from tape to this
#      program, and it will be replaced by read in a text file
#      so that this common block is no longer used
#     include '/home/caihq/navigation/roux_nav/SOURCES-ELDO/mes_commons'
# CAI-STOP
# TODO deal with this common block
#      common/cosinang/crr,srr,cti,sti
#                     ,chdg,shdg,cdri,sdri,cpit,spit
#                     ,caze,saze,celh,selh
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
    # deg_lon0=111.32  # used only in control_for...
    # deg_lat=111.13
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
#**** READ THE INPUT PARAMETERS IN FILE "DATA_cns"
#******************************************************************
#
# CAI-START ---- read in command line arguments
    # CALL GETARG(1, argu)  # command line arg is just the name of the input param file. 
    # idtmfile
    # 

    # ndtmfile=len(dtm_file)
    idtmfile = input_parameters['idtmfile']
    zsurf_cst = input_parameters['zsurf_cst']
    dtm_file = input_parameters['dtm_file']
    if(idtmfile == 0):
       print(' NO "SURF_DTM_*" FILE WILL BE READ '
           ,'-> ZSURF_CST (km) =',zsurf_cst)
    if(idtmfile == 1):
       print(' WILL READ "SURF_DTM_*" FILE :'
           ,dtm_file)

    ihms_min = int(input_parameters['ihms_min'])
    ihms_max = int(input_parameters['ihms_max'])
    ih_min=int(ihms_min/10000)
    im_min=int((ihms_min-10000*ih_min)/100)
    is_min=int(ihms_min-10000*ih_min-100*im_min)
    ih_max=int(ihms_max/10000)
    im_max=int((ihms_max-10000*ih_max)/100)
    is_max=int(ihms_max-10000*ih_max-100*im_max)

    nsf=0
    iwrisurfile = int(input_parameters['iwrisurfile'])
    if(iwrisurfile == 1):
       wrisurfile = input_parameters['wrisurfile']
       # while(wrisurfile(nsf+1:nsf+1).ne.' '):
       #     nsf=nsf+1
       nsf = len(wrisurfile)
       print(' WILL WRITE "SURF_EL_*" FILE : '
           ,wrisurfile)
       # tokens = f99.readline().split()
       xywidth_wrisurf = float(input_parameters['xywidth_wrisurf'])
       hxy_wrisurf = float(input_parameters['hxy_wrisurf'])
       xmin_wrisurf=-xywidth_wrisurf/2.
       xmax_wrisurf=+xywidth_wrisurf/2.
       ymin_wrisurf=-xywidth_wrisurf/2.
       ymax_wrisurf=+xywidth_wrisurf/2.
       print(' -> Xmin,max_wrisurf:',xmin_wrisurf,xmax_wrisurf)
       print('    Ymin,max_wrisurf:',ymin_wrisurf,ymax_wrisurf)
       print('    Hx,y_wrisurf:',hxy_wrisurf)
       nx_wrisurf=int((xmax_wrisurf-xmin_wrisurf)/hxy_wrisurf+1.)
       ny_wrisurf=int((ymax_wrisurf-ymin_wrisurf)/hxy_wrisurf+1.)
       print('    Nx,Ny_wrisurf:',nx_wrisurf,ny_wrisurf)
       if(nx_wrisurf > nxysurfmax or ny_wrisurf > nxysurfmax):
          print(' !!!! Nx,Ny_wrisurf :',nx_wrisurf,ny_wrisurf
             ,' > NxySURFmax !!!!')
          print(' !!!! MODIFY l.30 AND RECOMPILE THE PROGRAM !!!!')
          return # go to 3 # stop end
#  
#**** OPEN "SURF_EL_*" FILE #30 FOR WRITING (if IWRISURFILE=1)
#
       directory = input_parameters['directory'] 
       wrisurfile = input_parameters['wrisurfile'] 
       orig_lat = float(input_parameters['orig_lat'])
       orig_lon = float(input_parameters['orig_lon'])
       # xmin_wrisurf = float(input_parameters['xmin_wrisurf'])
       # ymin_wrisurf = float(input_parameters['ymin_wrisurf'])
       # hxy_wrisurf = float(input_parameters['hxy_wrisurf'])
       wrisurfile_path = os.path.join(directory, wrisurfile)
       print(' OPEN "SURF_EL_*" FILE #30 FOR WRITING :'
          , wrisurfile_path)
       if not os.path.exists(directory):
          os.makedirs(directory)
       with open(wrisurfile_path, 'w') as f30:
            # ,form='formatted',status='unknown')
          iolat_wrisurf=(1000.*orig_lat)
          iolon_wrisurf=(1000.*orig_lon)
          ixmin_wrisurf=(1000.*xmin_wrisurf)
          iymin_wrisurf=(1000.*ymin_wrisurf)
          ihxy_wrisurf=(1000.*hxy_wrisurf)
          #format(a12,a4,22i7)
          #f30.write(yymmdd,'ELDO'
          #   ,iolat_wrisurf,iolon_wrisurf
          #   ,0,0,0,0,0
          #   ,ih_min,im_min,is_min
          #   ,ih_max,im_max,is_max
          #   ,ixmin_wrisurf,iymin_wrisurf,0
          #   ,nx_wrisurf,ny_wrisurf,1
          #   ,ihxy_wrisurf,ihxy_wrisurf,0)

          print(f'{yymmdd}{"ELDO":4}') # TODO compare to container output, I think the format may be wrong
          #f30.write(f'{yymmdd:12>}{"ELDO":4}')
          f30.write(f'{yymmdd.strftime("%Y%d%m"):>12}{"ELDO"}')
          f30.write(''.join(f"{i:7n}" for i in [
              iolat_wrisurf, iolon_wrisurf, 0, 0, 0, 0, 0,
              ih_min, im_min, is_min,
              ih_max, im_max, is_max,
              ixmin_wrisurf, iymin_wrisurf, 0,
              nx_wrisurf, ny_wrisurf, 1,
              ihxy_wrisurf, ihxy_wrisurf, 0
          ]))
#
    else:
       print(' NO "SURF_EL_*" FILE WILL BE WRITTEN')

    saltdtm=0.

    if idtmfile == 1:
        print("WARNING: code path not tested!")
        # generate_surface_arrays.generate_surface_arrays(directory,
        #   idtmfile, dtm_file)
    elif idtmfile == 0:   # sample param file has idtmfile = 0
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
        #do jdtm=1,ny_dtm
        # do idtm=1,nx_dtm
        #    alt_dtm(idtm,jdtm)=zsurf_cst
        # enddo
        #enddo
        for jdtm in range(int(ny_dtm)):
            for idtm in range(int(nx_dtm)):
                alt_dtm[idtm][jdtm]=zsurf_cst
        altdtm_mean=zsurf_cst
        altdtm_min=zsurf_cst
        altdtm_max=zsurf_cst
    else:
        print("WARNING: No logic for idtmfile not equal 1 or 0")

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
    tmin=3.6*float(ih_min)+0.06*float(im_min) \
        +0.001*float(is_min)
    tmax=3.6*float(ih_max)+0.06*float(im_max) \
        +0.001*float(is_max)

    c_hms_min = f"{1000000 + ihms_min:7d}"
    c_hms_max = f"{1000000 + ihms_max:7d}"

#    fich_cornav = f"CORNAV_E_{c_hms_min[1:7]}_{c_hms_max[1:7]}"
#    fich_sis = f"SIS_E_{c_hms_min[1:7]}_{c_hms_max[1:7]}"
#
#    # writes output to a string
#    # write(c_hms_min,"(i7)")1000000+ihms_min
#    # write(c_hms_max,"(i7)")1000000+ihms_max
#    # write(fich_cornav,"('CORNAV_E_',a6,'_',a6)")
#    #      c_hms_min(2:7),c_hms_max(2:7)
#    # write(fich_sis,"('SIS_E_',a6,'_',a6)")
#    #      c_hms_min(2:7),c_hms_max(2:7)
#    #
#    #******************************************************************
#    #**** OPEN THE OUPUT "CORNAV_EL_*" FILE #10
#    #******************************************************************
#    #
#    path = os.path.join(directory, fich_cornav)
#    print(' ')
#    print(' OPEN "CORNAV_EL_*" FILE #10 :', path)
#    if not os.path.exists(directory):
#       os.makedirs(directory)
#    with open(path, 'w') as f10:
#        #open(10,file=directory(1:ndir)//'/'//fich_cornav
#        #       ,form='formatted',status='unknown')
#        print("yymmdd: ", yymmdd)
#        f10.write(f"{' YYYYMMDD : '}{yymmdd:<12}")
#        #f10.write(f"{' HHMMSS_min HHMMSS_max : '}{,a6,3x,a6,/)")
#        #     c_hms_min(2:7),c_hms_max(2:7)
#        f10.write(f"{ ' FIELDS TAKEN INTO ACCOUNT',/
#                   ,'  -> REL.WGHT_dZsurf,Vsurf,dVinsitu : ',3f6.3,/)")
#             rw_dzsurf,rw_vsurf,rw_dvinsitu
#        f10.write(f"{ ' VARIABLES TAKEN INTO ACCOUNT',/
#                   ,'  -> D_TILT_AFT,D_TILT_FORE (1/0) : ',2i2,/
#                   ,'  -> D_ROTA_AFT,D_ROTA_FORE (1/0) : ',2i2,/
#                   ,'  -> D_PITCH,D_HEADING (1/0) : ',2i2,/
#                   ,'  -> RANGE_DELAY_AFT,RANGE_DELAY_FORE (1/0) : '
#                   ,2i2,/
#                   ,'  -> D_XWE,D_YSN,D_ZACFT (1/0) : ',3i2,/
#                   ,'  -> D_VHACFT (1/0) : ',i2)")
#             idtiltaft,idtiltfore
#            ,idrotaaft,idrotafore
#            ,idpitch,idhdg
#            ,irdaft,irdfore
#            ,idxwe,idysn,idzacft
#            ,idvh
#        if idtmfile == 1:
#          f10.write(f"{' READS THE SURF_DTM_* FILE :',a50)")
#               directory(1:ndir)//'/'//dtm_file(1:ndtmfile)
#        else:
#          f10.write(f"{ ' NO SURF_DTM_* FILE TO READ '
#   #                  ,'-> ALT_SURF(x,y)=CST (',f6.3,')')")
#               zsurf_cst
#        # endif
#        if iwrisurfile == 1:
#          f10.write(f"{' WRITES THE SURF_EL_* FILE :',a50,//)")
#               directory(1:ndir)//'/'//wrisurfile(1:nsf)
#        else:
#          f10.write(f"{' NO SURF_EL_* FILE TO WRITE ',//)")
#    

# open and write OUTPUT "SIS_EL_*" FILE #50

# initializations
    time_prev=-999
    ihms_prev=-999
    iend = 0

# read ELDORA data (from text files originally, then move to CfRadial/binary files
    nfile = input_parameters['nfile']
    # for ifile in range(nfile):
    ifile = 1
    while ifile < nfile and iend == 0:
        data_dir = input_parameters['dir_read']
        infilename = os.path.join(data_dir, str(ifile)+".txt")
        print("reading ", infilename)
        # infilename = f"{dir_read[0:ndirr]}/{infile:10d}.txt"
        with open(infilename, 'r') as f:
    
            try:
                data = f.readline().strip().split()
                counter, nsweep, NTIMES, nranges, start_year, start_mon, start_day, start_hour, start_min, start_sec, time, azimuth, elevation, latitude, longitude, altitude, altitude_agl, heading, roll, pitch, drift, rotation, tilt, ew_velocity, ns_velocity, vertical_velocity, ew_wind, ns_wind, vertical_wind, azimuth_correction, elevation_correction, range_correction, longitude_correction, latitude_correction, pressure_altitude_correction, radar_altitude_correction, ew_ground_speed_correction, ns_ground_speed_correction, vertical_velocity_correction, heading_correction, roll_correction, pitch_correction, drift_correction, rotation_correction, tilt_correction = map(float, data)
                nranges = int(nranges)
                ranges = np.zeros(nranges)
                ZE = np.zeros(nranges)
                NCP = np.zeros(nranges)
                VR = np.zeros(nranges)
                SW = np.zeros(nranges) 
    
                # read(55,102,END=5)counter,(range(J),J=1,nranges) 
                # on error, goto 5
                # read counter (format I10), range(1), range(2), ... (format 2000f10.4)
    
                # for J in range(nranges):
                #     data = f.readline().strip().split()
                #     ranges[J], ZE[J], NCP[J], VR[J], SW[J] = map(float, data)
        
                data = f.readline().strip().split()
                # data_iterator = map(float, data)
                counter = int(data[0]) 
                for J in range(nranges):
                    ranges[J] = float(data[J+1])  # map(float, data)
        
                # process ray / sweep  ...
                corr_azest, corr_elhor, corr_dist, corr_lon, corr_lat, corr_p_alt, corr_r_alt, corr_vwe_av, corr_vsn_av, corr_cap, corr_roul, corr_tang, corr_derv, corr_rota, corr_incl, nb_portes, d_porte, ih_rdl,     im_rdl, is_rdl, ims_rdl, ih_rdl1, im_rdl1, is_rdl1, ims_rdl1, azest_rdl, elhor_rdl, lat_av, lon_av, p_alt_av, r_alt_av, cap_av, roul_av, tang_av, derv_av, rota_rdl, incl_rdl, vwe_av, vsn_av, vnz_av, vent_we, vent_sn, vent_nz = process_ray.process_ray(
                    nranges, MAXRAD, MAXPORAD, nsweep, start_hour, start_min, start_sec, time, azimuth, elevation, 
                    latitude, longitude, altitude, altitude_agl, 
                    heading, roll, pitch, drift, rotation, tilt, ew_velocity, ns_velocity, vertical_velocity, ew_wind, ns_wind, vertical_wind, 
                    azimuth_correction, elevation_correction, range_correction, longitude_correction,
                    latitude_correction, pressure_altitude_correction, radar_altitude_correction, 
                    ew_ground_speed_correction, ns_ground_speed_correction, vertical_velocity_correction,
                    heading_correction, roll_correction, pitch_correction, drift_correction,
                    rotation_correction, tilt_correction)

                # ih_rdl, im_rdl, is_rdl, ims_rdl = process_ray(meta_data, ranges)  # , ZE, NCP, VR, SW)
                # TODO: rename this function ...
                # iend = control_for_end_of_all_text_files() # ih_ray= (967) ... to tilt_prev= (3841); calls  iend_equals_2()
                # various check for control flow: time, lat, lon, end of sweep, etc.
                #c******************************************************************
                #c**** CONTROL OF CURRENT TIME 
                #c******************************************************************
                ih_ray=ih_rdl
                im_ray=im_rdl
                is_ray=is_rdl
                ims_ray=ims_rdl
                ihhmmss=10000*ih_ray+100*im_ray+is_ray
                print("ihhmmss= ", ihhmmss, " is_ray= ", is_ray, " im_ray=", im_ray, " ih_ray=", ih_ray)
                if ihhmmss <= 0:    # go to 1 
                    # skip to next file
                    continue
                time_ks=3.6*float(ih_ray)+0.06*float(im_ray)+0.001*float(is_ray)+1.e-6*float(ims_ray)
                if time_ks-time_prev < -80.  or time_ks-tmin < -80.: 
                    time_ks=time_ks+86.4
                    ihhmmss=ihhmmss+240000
                time_prev=time_ks
# >>>>>> disagreement here on HHMMSSms compared to .f !
                if time_ks < tmin:
                    if ihhmmss/10 > ihms_prev:
                        print(' HHMMSS:',ihhmmss,' < HHMMSS_min:',ihms_min)
                        ihms_prev=ihhmmss/10
                    if iend !=  2: #  go to 1   ! only when end of text file not reached
                        # skip to next file
                        continue
                if time_ks > tmax:
                    iend=2
                    print(' ')
                    print(' HHMMSSms:',100*ihhmmss+ims_rdl
                          ,' > HHMMSSms_max:',100*ihms_max)
                if iend != 2:  
                    #
                    #******************************************************************
                    #**** CONTROL OF LAT, LON, P_ALT AND R_ALT
                    #******************************************************************
                    #
                    if (   abs(lat_av) < 0.001
                        or abs(lon_av) < 0.001
                        or (     abs(p_alt_av) < 0.001
                        and abs(r_alt_av) < 0.001)):  # go to 1 # read next file
                        continue
                    #   print('P_ALT_AV= ',p_alt_av
                    #
     
                    #******************************************************************
                    #**** RADAR IDENTIFICATION THROUGH TILT_RAY (=INCL_RDL)
                    #****  -> AFT : IRADAR_RAY=1, IAFTFORE=-1
                    #****  -> FORE : IRADAR_RAY=2, IAFTFORE=+1
                    #**********************F********************************************
                    #
                    tilt_ray=incl_rdl
                    if abs(tilt_ray) < 15. :
                        continue  # go to 1 # read next file
                    elif abs(tilt_ray) < 30. :
                        if tilt_ray < -15. :
                            iradar_ray=1
                            iaftfore=-1
                            swp[iradar_ray]=num_swp
                        if tilt_ray > +15. :
                            iradar_ray=2
                            iaftfore=+1
                            swp[iradar_ray]=num_swp
                    else:
                        continue  # go to 1 # read next file
                    #******************************************************************
                    #**** CONTROL FOR AN END OF SWEEP
                    #******************************************************************
                    if(nb_ray(iradar_ray) == 1):
                        tandrot=0.
                    else:
                        tandrot=tan(conv*(rota_rdl-rota_prev(iradar_ray)))
              
                    if(     nb_ray(iradar_ray) > 1
                        and (    (swp[iradar_ray].ne.swp_prev(iradar_ray))
                        or (abs(tandrot) > 0.2)       ) ):
                          # iend=1
                          iend_ge_1.iend_ge_1()
                    #******************************************************************
                    #****    END OF A SWEEP ( IEND = 1 )
                    #**** or END OF THE TAPE or END OF CONSIDERED PERIOD ( IEND = 2 )
                    #******************************************************************
                # end_of_sweep_iend_eq_1()

                #
                #******************************************************************
                #**** END OF THE TAPE or END OF CONSIDERED PERIOD ( IEND = 2 )
                #******************************************************************
                #
                if iend == 2:
                    print("end of tape or end of considered period: iend = 2")
                    kdzsurf = int(input_parameters['kdzsurf'])
                    kvsurf = int(input_parameters['kvsurf'])
                    kdvinsitu = int(input_parameters['kdvinsitu'])
                    dtiltaft_guess = float(input_parameters['dtiltaft_guess'])
                    dtiltfore_guess = float(input_parameters['dtiltfore_guess'])
                    drotaaft_guess = float(input_parameters['drotaaft_guess'])
                    drotafore_guess = float(input_parameters['drotafore_guess'])
                    dhdg_guess = float(input_parameters['dhdg_guess'])
                    dpitch_guess = float(input_parameters['dpitch_guess'])
                    rdfore_guess = float(input_parameters['rdfore_guess'])
                    rdaft_guess = float(input_parameters['rdaft_guess'])
                    dxwe_guess = float(input_parameters['dxwe_guess'])
                    dysn_guess = float(input_parameters['dysn_guess'])
                    dzacft_guess = float(input_parameters['dzacft_guess'])
                    isim = int(input_parameters['isim'])
                    ipr_alt = int(input_parameters['ipr_alt'])
                    dmax0 = float(input_parameters['dmax0'])
                    continue_processing = control_for_end_of_all_text_files_wo_gotos.control_for_end_of_all_text_files(
                        kdzsurf, kvsurf, kdvinsitu,
                        iradar_ray, nb_ray,
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
#, kdvinsitu, 
#                        swv2surf_tot, swdvminsitu_tot, swdvinsitu_tot, swv2insitu_tot, xv_vpv, 
#                        x_vpv, xvv_vpv
                        )
                    if continue_processing:
                        swdzmsurf_tot = 0
                        swdzsurf_tot = 0
                        swdz2surf_tot = 0
                        swvmsurf_tot = 0
                        swvsurf_tot = 0
                        swv2surf_tot = 0
                        swdvminsitu_tot = 0
                        swdvinsitu_tot = 0
                        swv2insitu_tot = 0
                        print(' ')
                        print(' ****************************************************')
                        print('   HHMMSS :',ih_ray,im_ray,is_ray
                                  ,'   -> END OF CONSIDERED PERIOD')
                        print('   NB_SWEEPS_READ FOR AFT AND FORE RADARS :'
                                  ,nb_sweep)
                        print(' ****************************************************')
                        print(' ')
                        print(' ')
                        #    xv_vpv, x_vpv, xvv_vpv
                        iend_equals_2.iend_equals_2(
                            kdzsurf, kvsurf, kdvinsitu, swdzmsurf_tot, swdzsurf_tot, 
                            swdz2surf_tot, swvmsurf_tot, swvsurf_tot,
                            swv2surf_tot, swdvminsitu_tot, swdvinsitu_tot, swv2insitu_tot, 
                            xv_vpv, x_vpv, xvv_vpv,
                            iwrisurfile, wrisurfile_path,
                            swdzsurf_wri, sw_or_altsurf_wri,
                            nx_wrisurf,ny_wrisurf,nxysurfmax,
                            )
                #endif    !!  of  !! if(iend == 2):  !!
               
            except EOFError:
                # jump here on EOF
                print("Error reading data file:", ifile)
        ifile += 1

    #
    #    control_for_end_of_all_text_files_wo_gotos()
    # (IF SUM_WGHTS_surf+insitu > SUM_WGHTS_min)
    #    -> NAVIGATIONAL ERROS CAN BE CALCULATED
    if False:   # enough_points(ssurfins, ssurfins_min):
        range_delay_corr_aft,
        pressure_alt_corr,
        ew_gndspd_corr,
        pitch_corr_cfac,
        drift_corr_cfac,
        rot_angle_corr_aft,
        tilt_corr_aft = calculate_navigational_errors()

    else:
        print(' /////////////////////////////////////////////')
        print(' ')
        print(' /////////////////////////////////////////////')
        print('    NO CORRECTIONS FOR NAVIGATIONAL ERRORS')
        print(' //////////// (not enough points) ////////////')
        print(' /////////////////////////////////////////////')
        print(' ')

#        range_delay_corr_aft = 0.0
#        pressure_alt_corr = 0.0
#        ew_gndspd_corr = 0.0
#        pitch_corr_cfac = 0.0
#        drift_corr_cfac = 0.0
#        rot_angle_corr_aft = 0.0
#        tilt_corr_aft = 0.0 
    #
    #    if iend==2: 
    #        iend_equals_2(kdzsurf, kvsurf, kdvinsitu, swdzmsurf_tot, swdzsurf_tot, swdz2surf_tot, swvmsurf_tot, swvsurf_tot,
    #    swv2surf_tot, swdvminsitu_tot, swdvinsitu_tot, swv2insitu_tot, xv_vpv, x_vpv, xvv_vpv)


#    #******************************************************************
#    #             Write the cfac files using SOLO format
#    #******************************************************************
#    
#    # Write the aft cafc file
    write_aft_cfac.write_aft_cfac(
        directory,
        range_delay_corr_aft,
        pressure_alt_corr,
        ew_gndspd_corr,
        pitch_corr_cfac,
        drift_corr_cfac,
        rot_angle_corr_aft,
        tilt_corr_aft)
     
#    # Write the fore cafc file
#              write_fore_cafc(directory,
#                  range_delay_corr,
#                  pressure_alt_corr,
#                  ew_gndspd_corr,
#                  pitch_corr_cfac,
#                  drift_corr_cfac,
#                  rot_angle_corr_fore,
#                  tilt_corr_fore)
#   
#    # CAI ******  End of writing the cfac files  ******************    
