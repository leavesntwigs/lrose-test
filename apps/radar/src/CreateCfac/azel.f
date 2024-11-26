c******************************************************************
c
c**** CALCULATE DIRECTOR COSINES, AZIM_EST ET DE ELEV_HOR
c**** FROM LEE ET AL. (JTech, 1994, 11, 572-578)
c
c******************************************************************
c
      subroutine azel(rotaroll,tilt_ray
     &                ,hdg_acft,drift_acft,pitch_acft
     &                ,azeast_ray,elhor_ray
     &                ,cxa,cya,cza,cwe,csn,cnz)
      common/cosinang/crr,srr,cti,sti
     &               ,chdg,shdg,cdri,sdri,cpit,spit
     &               ,caze,saze,celh,selh
c
      conv=3.14159/180.
c
      crr=cos(conv*rotaroll)
      srr=sin(conv*rotaroll)
      cti=cos(conv*tilt_ray)
      sti=sin(conv*tilt_ray)
      if(srr.gt.0.)then
        side=+1.
      else
        side=-1.
      endif
c
      chdg=cos(conv*hdg_acft)
      shdg=sin(conv*hdg_acft)
      cdri=cos(conv*drift_acft)
      sdri=sin(conv*drift_acft)
      cpit=cos(conv*pitch_acft)
      spit=sin(conv*pitch_acft)
c
      cxa=+srr*cti
      cya=-cti*crr*spit+sti*cpit
      cza=+cti*crr*cpit+sti*spit
c
      cwe=+chdg*cxa+shdg*cya
      csn=-shdg*cxa+chdg*cya
      cnz=+cza
      azeast_ray=atan2(csn,cwe)/conv
      caze=cos(conv*azeast_ray)
      saze=sin(conv*azeast_ray)
      do while (azeast_ray.le.0.)
         azeast_ray=azeast_ray+360.
      enddo
      chor=amax1(0.1,sqrt(cwe*cwe+csn*csn))
      elhor_ray=atan(cnz/chor)/conv
      celh=cos(conv*elhor_ray)
      selh=sin(conv*elhor_ray)
c
      return
      end
c
