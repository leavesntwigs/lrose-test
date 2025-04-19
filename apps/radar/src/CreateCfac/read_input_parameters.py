#  read Data_cns_Cai (file 99) parameters
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
import datetime

# return a dictionary of the input parameters
def read_input_parameters(file_name):
   nvar=12
   nxysurfmax=200
#
#    parameter (nvar=12,nxysurfmax=200)
#
#  include '/home/users/rouf/SOURCES/ELDO/mes_parametres'
# CAI-START: Inlcude the parameter file mes_parametres directly below
#   instead of using the include function above
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

#
#******************************************************************
#**** READ THE INPUT PARAMETERS ON FILE "DATA_cns"
#******************************************************************
#
   input_parameters = {}

   with open(file_name, 'r') as f99:
      print(' ')
      aline = f99.readline().replace('\'', ' ')
      tokens = aline.split() # comments are !
      #print('tokens: ', aline)
      directory = tokens[0].strip()
      ndir=len(directory) # ndir-1
      print(' DIRECTORY FOR THE OUTPUT FILES :',directory)
      input_parameters['directory'] = directory

      print(' ')
      #aline = f99.readline().replace('\'', ' ')
      #tokens = aline.split()
      dir_read = f99.readline().split()[0].strip()
      input_parameters['dir_read'] = dir_read 
      #ndirr=len(dir_read) # ndirr-1
      print(' DIRECTORY FOR READ FILES :',dir_read)
      input_parameters['dir_read'] = dir_read

      print(' ')
      nfile = f99.readline().strip()
      print(' Total Number of Sweep Files :',nfile)
      input_parameters['nfile'] = nfile 

      tokens = f99.readline().split()
      yymmdd = datetime.date(int(tokens[2]), int(tokens[0]), int(tokens[1]))
    
      # iyymmdd = f99.readline().split()
# convert date format to string
#      write(yymmdd,"(i12)")10000*iyymmdd(3)+100*iyymmdd(2)+iyymmdd(1)
      print(' YYYYMMDD :',yymmdd.isoformat())
      input_parameters['yymmdd'] = yymmdd
#
      tokens = f99.readline().split()
      ihms_min = tokens[0]
      ihms_max = tokens[1]
      print(' HHMMSS (min,max) :',ihms_min,ihms_max)
      #ih_min=ihms_min/10000
      #im_min=(ihms_min-10000*ih_min)/100
      #is_min=ihms_min-10000*ih_min-100*im_min
      #ih_max=ihms_max/10000
      #im_max=(ihms_max-10000*ih_max)/100
      #is_max=ihms_max-10000*ih_max-100*im_max
      input_parameters['ihms_min'] = ihms_min
      input_parameters['ihms_max'] = ihms_max
#
      tokens = f99.readline().split()
      orig_lat = tokens[0]
      orig_lon = tokens[1]
      print(' ORIGIN_LATITUDE,_LONGITUDE :',orig_lat,orig_lon)
      input_parameters['orig_lat'] = orig_lat
      input_parameters['orig_lon'] = orig_lon
#
      print(' ')
      ig_dismiss = f99.readline()
      print(' 15 GATES TO DISMISS (0 if not) :',ig_dismiss)
      input_parameters['ig_dismiss'] = ig_dismiss
#
      print(' ')
      tokens = f99.readline().split()
      dmin0 = tokens[0]
      dmax0 = tokens[1]
      print(' DMIN,DMAX FROM RADAR [km]:',dmin0,dmax0)
      input_parameters['ig_dismiss'] = ig_dismiss
#
      print(' ')
      ipr_alt = f99.readline().split()[0]
      print(' ALTITUDE (1:pressure,2:radar) :',ipr_alt)
      input_parameters['ig_dismiss'] = ig_dismiss
#
      print(' ')
      tokens = f99.readline().split()
      ref_min0 = tokens[0]
      ref_max = tokens[1]
      print(' REF_min(at 10km),REF_max [dBZ]:',ref_min0,ref_max)
      input_parameters['ig_dismiss'] = ig_dismiss
#
      print(' ')
      ichoice_vdop = f99.readline().split()[0]
      print(' WHICH VDOP (1:VR,2:VG,3:VU) :'
         ,ichoice_vdop)
      if(ichoice_vdop == 1 or ichoice_vdop == 2):
         ictrl_contray=0
         print(' -> WILL NOT CONTROL CONTINUITY ALONG THE RAY !!!!')
      else:
         ictrl_contray=0
#
      print(' ')
      print(' CORRECTION OF NAVIGATIONAL ERRORS')
      print(' ')
      print(' FIELDS TAKEN INTO ACCOUNT:')
      kdzsurf=1
      kvsurf=1
      kdvinsitu=1
      f99.readline() # ignore ---- line
      tokens = f99.readline().split()
      rw_dzsurf = tokens[0] 
      rw_vsurf = tokens[1] 
      rw_dvinsitu = tokens[2] 
      print('   -> REL.WGHT_dZsurf,Vsurf,dVinsitu (1/0) :'
             ,rw_dzsurf,rw_vsurf,rw_dvinsitu)
      input_parameters['kdzsurf'] = kdzsurf
      input_parameters['kvsurf'] = kvsurf
      input_parameters['kdvinsitu'] = kdvinsitu
      input_parameters['rw_dzsurf'] = rw_dzsurf
      input_parameters['rw_vsurf'] = rw_vsurf
      input_parameters['rw_dvinsitu'] = rw_dvinsitu
#
      print(' ')
      print(' CORRECTIONS TO CALCULATE:')
      f99.readline() # ignore ---- line
      tokens = f99.readline().split()
      idtiltaft = tokens[0]
      idtiltfore = tokens[1]
      print('   -> D_TILT_AFT,D_TILT_FORE (1/0) :'
             ,idtiltaft,idtiltfore)
      tokens = f99.readline().split()
      idrotaaft = tokens[0]
      idrotafore = tokens[1]
      print('   -> D_ROTA_AFT,D_ROTA_FORE (1/0) :'
             ,idrotaaft,idrotafore)
      tokens = f99.readline().split()
      idpitch = tokens[0]
      idhdg = tokens[1]
      print('   -> D_PITCH,D_HEADING (1/0) :'
         ,idpitch,idhdg)
      tokens = f99.readline().split()
      irdaft = tokens[0]
      irdfore = tokens[1]
      print('   -> RANGE_DELAY_AFT,RANGE_DELAY_FORE (1/0) :'
         ,irdaft,irdfore)
      tokens = f99.readline().split()
      idxwe = tokens[0]
      idysn = tokens[1]
      idzacft = tokens[2]
      print('   -> D_XWE,D_YSN,D_ZACFT (1/0) :'
         ,idxwe,idysn,idzacft)
      idvh = f99.readline().split()[0]
      print('   -> D_VHACFT (1/0) :',idvh)
#
      print(' ')
      f99.readline()
      isim = f99.readline().split()[0]
      print(' SIMULATION AVEC +dXXX_GUESS INITIAUX (1/0) :',isim)
#
      print(' ')
      f99.readline()
      tokens = f99.readline().split()
      dtiltaft_guess = tokens[0]
      dtiltfore_guess = tokens[1]
      print(' D_TILT_AFT,D_TILT_FORE (deg) guess :'
         ,dtiltaft_guess,dtiltfore_guess)
      tokens = f99.readline().split()
      drotaaft_guess = tokens[0]
      drotafore_guess = tokens[1]
      print(' D_ROTA_AFT,D_ROTA_FORE (deg) guess :'
         ,drotaaft_guess,drotafore_guess)
      tokens = f99.readline().split()
      dpitch_guess = tokens[0]
      dhdg_guess = tokens[1]
      print(' D_PITCH,D_HEADING (deg) guess :',
         # ,droll_guess,  # not used ???
         dpitch_guess,dhdg_guess)
      tokens = f99.readline().split()
      rdaft_guess = tokens[0]
      rdfore_guess = tokens[1]
      print(' RANGE_DELAY_AFT,RANGE_DELAY_FORE (km) guess :'
         ,rdaft_guess,rdfore_guess)
      tokens = f99.readline().split()
      dxwe_guess = tokens[0]
      dysn_guess = tokens[1]
      dzacft_guess = tokens[2]
      print(' D_XWE,D_YSN,D_ZACFT (km) guess :'
         ,dxwe_guess,dysn_guess,dzacft_guess)
      dvh_guess = f99.readline().split()[0]
      print(' D_VHACFT (m/s) guess :',dvh_guess)
      f99.readline()
#
      print('  ')
      tokens = f99.readline().replace('\'', ' ').split()
      idtmfile = int(tokens[0])
      dtm_file = tokens[1]
      zsurf_cst = float(tokens[2])
      input_parameters['idtmfile'] = idtmfile
      input_parameters['dtm_file'] = dtm_file.strip()
      input_parameters['zsurf_cst'] = zsurf_cst

      ndtmfile=len(dtm_file)

#      if(idtmfile == 0):
#         print(' NO "SURF_DTM_*" FILE WILL BE READ '
#             ,'-> ZSURF_CST (km) =',zsurf_cst)
#      if(idtmfile == 1):
#         print(' WILL READ "SURF_DTM_*" FILE :'
#             ,dtm_file)
#
      tokens = f99.readline().replace('\'', ' ').split()
      iwrisurfile = int(tokens[0])
      wrisurfile = tokens[1]
      input_parameters['iwrisurfile'] = iwrisurfile
      print(type(iwrisurfile), iwrisurfile)
      input_parameters['wrisurfile'] = wrisurfile.strip()
#      nsf=0
      if(iwrisurfile == 1):
          print("*************")
#         # while(wrisurfile(nsf+1:nsf+1).ne.' '):
#         #     nsf=nsf+1
#         print(' WILL WRITE "SURF_EL_*" FILE : '
#             ,wrisurfile)
          tokens = f99.readline().split()
          xywidth_wrisurf = tokens[0]
          hxy_wrisurf = tokens[1]
          input_parameters['xywidth_wrisurf'] = xywidth_wrisurf
          input_parameters['hxy_wrisurf'] = hxy_wrisurf
          print("just inserted xywidth_wrisurf and hxy_wrisurf")

#         xmin_wrisurf=-xywidth_wrisurf/2.
#         xmax_wrisurf=+xywidth_wrisurf/2.
#         ymin_wrisurf=-xywidth_wrisurf/2.
#         ymax_wrisurf=+xywidth_wrisurf/2.
#         print(' -> Xmin,max_wrisurf:',xmin_wrisurf,xmax_wrisurf)
#         print('    Ymin,max_wrisurf:',ymin_wrisurf,ymax_wrisurf)
#         print('    Hx,y_wrisurf:',hxy_wrisurf)
#         nx_wrisurf=((xmax_wrisurf-xmin_wrisurf)/hxy_wrisurf+1.)
#         ny_wrisurf=((ymax_wrisurf-ymin_wrisurf)/hxy_wrisurf+1.)
#         print('    Nx,Ny_wrisurf:',nx_wrisurf,ny_wrisurf)
#         if(nx_wrisurf > nxysurfmax or ny_wrisurf > nxysurfmax):
#            print(' !!!! Nx,Ny_wrisurf :',nx_wrisurf,ny_wrisurf
#               ,' > NxySURFmax !!!!')
#            print(' !!!! MODIFY l.30 AND RECOMPILE THE PROGRAM !!!!')
#   #   go to 3 # stop end 
#            return
#  # endif
##
##**** OPEN "SURF_EL_*" FILE #30 FOR WRITING (if IWRISURFILE=1)
##
#         print(' OPEN "SURF_EL_*" FILE #30 FOR WRITING :'
#            ,directory//'/'//wrisurfile)
#         with open(directory//'/'//wrisurfile, 'w') as f30:
#              # ,form='formatted',status='unknown')
#            iolat_wrisurf=(1000.*orig_lat)
#            iolon_wrisurf=(1000.*orig_lon)
#            ixmin_wrisurf=(1000.*xmin_wrisurf)
#            iymin_wrisurf=(1000.*ymin_wrisurf)
#            ihxy_wrisurf=(1000.*hxy_wrisurf)
#            f30.write(yymmdd,'ELDO'
#               ,iolat_wrisurf,iolon_wrisurf
#               ,0,0,0,0,0
#               ,ih_min,im_min,is_min
#               ,ih_max,im_max,is_max
#               ,ixmin_wrisurf,iymin_wrisurf,0
#               ,nx_wrisurf,ny_wrisurf,1
#               ,ihxy_wrisurf,ihxy_wrisurf,0)
##
#      else:
#         print(' NO "SURF_EL_*" FILE WILL BE WRITTEN')
    
   return input_parameters

