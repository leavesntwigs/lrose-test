      program test_azel

      ! common block is set in the calling function, 
      ! values are changed in the function,
      ! then referenced back in the calling function.
      ! The common block variables are OUT parameters
      ! Subroutine azel sets all of these common block variables.
   
      common/cosinang/crr,srr,cti,sti
     &               ,chdg,shdg,cdri,sdri,cpit,spit
     &               ,caze,saze,celh,selh
 
      ! call azel(swdzsurf_wri,sw_or_altsurf_wri
      ! &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      !
      ! subroutine azel(rotaroll,tilt_ray
      !                ,hdg_acft,drift_acft,pitch_acft
      !                ,azeast_ray,elhor_ray
      !                ,cxa,cya,cza,cwe,csn,cnz)

      real rotaroll,tilt_ray
     &                ,hdg_acft,drift_acft,pitch_acft
     &                ,azeast_ray,elhor_ray
     &                ,cxa,cya,cza,cwe,csn,cnz

      rotaroll = 0.0
      tilt_ray = 0.0
      hdg_acft = 0.0
      drift_acft = 0.0
      pitch_acft = 0.0
      azeast_ray = 0.0
      elhor_ray = 0.0
      cxa = 0.0
      cya = 0.0
      cza = 0.0
      cwe = 0.0
      csn = 0.0
      cnz = 0.0

      print *,'test 0'
      call azel(rotaroll,tilt_ray
     &                ,hdg_acft,drift_acft,pitch_acft
     &                ,azeast_ray,elhor_ray
     &                ,cxa,cya,cza,cwe,csn,cnz)

      print *,crr,srr,cti,sti
     &               ,chdg,shdg,cdri,sdri,cpit,spit
     &               ,caze,saze,celh,selh

      stop 
      end

