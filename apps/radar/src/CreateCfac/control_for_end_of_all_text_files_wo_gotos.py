# may not need this file
def control_for_end_of_all_text_files(kdzsurf, kvsurf, kdvinsitu, swdzmsurf_tot, swdzsurf_tot, swdz2surf_tot, swvmsurf_tot, swvsurf_tot,
    swv2surf_tot, swdvminsitu_tot, swdvinsitu_tot, swv2insitu_tot, xv_vpv, x_vpv, xvv_vpv):

#******************************************************************
#**** CONTROL FOR THE END OF THE READING ALL TEXT FILES
#******************************************************************
#
  # end while ifile < nfile
  7   iend=0  # What is the use of iend? boolean? or state? State: 
              # iend = 0 ???
              # iend = 1 for end of sweep
              # iend = 2 for end of considered period.
    if ifile == nfile and islastfile:
         iend=2 # end_of_considered_period = True
         done = True
         print(' ')
         print('**** END OF READING ALL TEXT FILES ****')
    #endif


def control_for_end_of_all_text_files():

#******************************************************************
#**** CONTROL OF CURRENT TIME
#******************************************************************
#
      ih_ray=ih_rdl
      im_ray=im_rdl
      is_ray=is_rdl
      ims_ray=ims_rdl
      ihhmmss=10000*ih_ray+100*im_ray+is_ray
      if(ihhmmss > 0):   # go to 1 # read next file   # END WHILE ihhmmss >= 0
    #
          time_ks=3.6*float(ih_ray)+0.06*float(im_ray)
                  +0.001*float(is_ray)+1.e-6*float(ims_ray)
          if(    time_ks-time_prev < -80.
             .or.time_ks-tmin < -80.):
            time_ks=time_ks+86.4
    	  ihhmmss=ihhmmss+240000
          endif
          time_prev=time_ks
          if time_ks < tmin):
            if ihhmmss/10 > ihms_prev):
    	  print(' HHMMSS:',ihhmmss,' < HHMMSS_min:',ihms_min
    	  ihms_prev=ihhmmss/10
            endif
            if iend .ne. 2) go to 1   # read next file ! only when end of text file not reached
          endif
          if time_ks > tmax):
    	      iend=2
    	      print(' '
    	      print(' HHMMSSms:',100*ihhmmss+ims_rdl
                         ,' > HHMMSSms_max:',100*ihms_max
          endif
          if iend == 2):
              iend_equals_2() # go to 2
          else:
          #
          #******************************************************************
          #**** CONTROL OF LAT, LON, P_ALT AND R_ALT
          #******************************************************************
          #
                if     abs(lat_av) < 0.001
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
          #if(abs(tilt_ray) < 15.):
          #  done = True # go to 1 # read next file
          #elif(abs(tilt_ray) < 30.):
          #  if(tilt_ray < -15.):
          #    iradar_ray=1
          #    iaftfore=-1
          #    swp(iradar_ray)=num_swp
          #  if(tilt_ray > +15.):
          #    iradar_ray=2
          #    iaftfore=+1
          #    swp(iradar_ray)=num_swp
          #else:
    	  #  done = True # go to 1 # read next file
          # move this to inside while more data files loop ... done
          #if abs(tilt_ray) >= 15. and abs(tilt_ray) < 30.:
          #  if(tilt_ray < -15.):
          #    iradar_ray=1
          #    iaftfore=-1
          #    swp(iradar_ray)=num_swp
          #  if(tilt_ray > +15.):
          #    iradar_ray=2
          #    iaftfore=+1
          #    swp(iradar_ray)=num_swp
      #******************************************************************
      #**** CONTROL FOR AN END OF SWEEP
      #******************************************************************
      if not done:
          if(nb_ray(iradar_ray) == 1):
            tandrot=0.
          else
            tandrot=tan(conv*(rota_rdl-rota_prev(iradar_ray)))

          if(     nb_ray(iradar_ray) > 1
              and (    (swp(iradar_ray).ne.swp_prev(iradar_ray))
                   .or.(abs(tandrot) > 0.2)       ) )
            iend=1
       #******************************************************************
       #****    END OF A SWEEP ( IEND = 1 )
       #**** or END OF THE TAPE or END OF CONSIDERED PERIOD ( IEND = 2 )
       #******************************************************************
#   2   continue
      done = iend_ge_1()
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
      dtilt_guess, drota_quess = earth_rel_angles(iaftfore)
#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE NAVIGATION WITHOUT dXXX_GUESS
#------------------------------------------------------------------
      if(isim == 1):
          caze_true,
  	  saze_true,
          celh_true,
          selh_true,
          dcwe_dt_true,
          dcwe_dr_true,
          dcwe_dp_true,
          dcwe_dh_true,
          dcsn_dt_true,
          dcsn_dr_true,
          dcsn_dp_true,
          dcsn_dh_true,
          dcnz_dt_true,
          dcnz_dr_true,
          dcnz_dp_true,
          dcnz_dh_true,
          duacft_dv_true,
          dvacft_dv_true = 
              isim_equals_1()
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
      else:
        side=+1.
        ilr=2
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
      else:
        d_dgate_guess=rdfore_guess
      ngates=nb_portes
#------------------------------------------------------------------
#---- ( IF ISIM=1 ) -> SIMULATED TRUE RANGE GATES WITHOUT dXXX_GUESS
#------------------------------------------------------------------
      if(isim == 1):
        do ig=1,ngates
# CAI-START
#          dgate_true(ig)=d_porte(iradar*MAXPORT+ig)
#                             +corr_dist(iradar+1)
# It seems that the above code is wrong, since iradar has not been assigned values yet,
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
        else:
	  z_acft_true=r_alt_acft
#------------------------------------------------------------------
      x_acft=(xlon_acft-orig_lon)*deg_lon+dxwe_guess
      y_acft=(xlat_acft-orig_lat)*deg_lat+dysn_guess
      if(ipr_alt == 1):
	z_acft=p_alt_acft+dzacft_guess
      else:
	z_acft=r_alt_acft+dzacft_guess

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
        go to 1 # read next file; replace with continue and move inside while loop
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
      if isim == 1:
        proj_wind=wind_we*cwe_true+wind_sn*csn_true+wind_nz*cnz_true
        wa_we_true=wind_we-acftspd_we_true
        wa_sn_true=wind_sn-acftspd_sn_true
      #endif
#----------------------------------------------------------------------
      if(    (abs(wind_we) <= 0. and abs(wind_sn) <= 0.)
         .or.(abs(wind_we) > 100..or.abs(wind_sn) > 100.)):
        print(' !!!! NO_RAY:',nb_ray(iradar_ray),' -> Uwe,Vsn_wind:'
               ,wind_we,wind_sn,' !!!!'
        go to 1 # read next file #  replace with continue and move inside while loop
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
      if abs(selh) < selhinsitu_max:
        ig=1
        while (     ig < MAXPORT
                   and dgate_corr(ig) < dmax_insitu)
           ngates_insitu_max=ig
           ig=ig+1
        #enddo
      # endif
#
#******************************************************************
#**** CHECK THE NCP, SW AND REFLECTIVITY VALUES
#******************************************************************
#
      ngates_max=1
      for ig in range(ngates):
         ref_min=ref_min0+20.*(alog10(dgate_corr(ig))-1.)
         if dgate_corr(ig) < dmin
            or dgate_corr(ig) > dmax
            or ncp(ig) < xncp_min
            or sw(ig) > sw_max
            or ze(ig) < ref_min
            or ze(ig) > ref_max:
             ze(ig)=-999.
             vr(ig)=-999.
	     vs(ig)=-999.	!Olivier
	     vl(ig)=-999.	!Olivier
             vg(ig)=-999.
             vu(ig)=-999.
         else:
	     ngates_max=ig
             nref_ok(iradar_ray)=nref_ok(iradar_ray)+1
         # endif
      # end for
  10  continue
#
#******************************************************************
#**** CHOOSE WHICH DOPPLER VELOCITY WILL BE USED (FOLLOWING ICHOICE_VDOP)
#****   -> 1:RAW(VR), 2:CORRECTED FOR VACFT(VG), 3:UNFOLDED(VU)
#******************************************************************

      for ig in range(ngates_max):

	 vdop_read=-999.
	 vdop_corr(ig)=-999.
	 if ze(ig) > -900.:

            if      ichoice_vdop == 1
               and abs(vr(ig)) > 0. and abs(vr(ig)) < vdop_max
               and proj_acftspd > -900.:
               vdop_read=vr(ig)+proj_acftspd
# CAI-STOP


           if      ichoice_vdop == 2
               and abs(vr(ig)) > 0. and abs(vr(ig)) < vdop_max:
             vdop_read=vr(ig)

           if      ichoice_vdop == 3
               and abs(vu(ig)) > 0. and abs(vu(ig)) < vdop_max:
             vdop_read=vu(ig)

           if vdop_read > -900.:
             ndop_ok(iradar_ray)=ndop_ok(iradar_ray)+1
             vdop_corr(ig)=vdop_read
           #endif

         #endif
      #enddo

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
    if iend==2:
        iend_equals_2(kdzsurf, kvsurf, kdvinsitu, swdzmsurf_tot, swdzsurf_tot, swdz2surf_tot, swvmsurf_tot, swvsurf_tot,
    swv2surf_tot, swdvminsitu_tot, swdvinsitu_tot, swv2insitu_tot, xv_vpv, x_vpv, xvv_vpv)
    return

