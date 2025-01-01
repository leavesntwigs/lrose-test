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