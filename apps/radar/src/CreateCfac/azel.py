#******************************************************************
#
#**** CALCULATE DIRECTOR COSINES, AZIM_EST ET DE ELEV_HOR
#**** FROM LEE ET AL. (JTech, 1994, 11, 572-578)
#
#******************************************************************
#
# rotaroll (in param)
# tilt_ray (in param)
# hdg_acft (in param)
# drift_acft, (in param)
# pitch_acft (in param)
# azeast_ray (out param)
# elhor_ray (out param)
# cxa, cya, cza, cwe, csn, cnz (out params)
#

import math
import numpy as np

def azel(rotaroll,tilt_ray
      ,hdg_acft,drift_acft,pitch_acft
      ,azeast_ray,elhor_ray
      ,cxa,cya,cza,cwe,csn,cnz,
#
# CAUTION!!!
# these common block variables could be in/out parameters
# 
#       common/cosinang/
      cosinang
      ):
#
      conv=3.14159/180.
#
      cosinang['crr']=math.cos(conv*rotaroll)
      cosinang['srr']=math.sin(conv*rotaroll)
      cosinang['cti']=math.cos(conv*tilt_ray)
      cosinang['sti']=math.sin(conv*tilt_ray)
      if(cosinang['srr'] > 0.):
            side=+1.
      else:
            side=-1.
#
      cosinang['chdg']=math.cos(conv*hdg_acft)
      cosinang['shdg']=math.sin(conv*hdg_acft)
      cosinang['cdri']=math.cos(conv*drift_acft)
      cosinang['sdri']=math.sin(conv*drift_acft)
      cosinang['cpit']=math.cos(conv*pitch_acft)
      cosinang['spit']=math.sin(conv*pitch_acft)
#
      cxa=+cosinang['srr']*cosinang['cti']
      cya=-cosinang['cti']*cosinang['crr']*cosinang['spit']+cosinang['sti']*cosinang['cpit']
      cza=+cosinang['cti']*cosinang['crr']*cosinang['cpit']+cosinang['sti']*cosinang['spit']
#
      cwe=+cosinang['chdg']*cxa+cosinang['shdg']*cya
      csn=-cosinang['shdg']*cxa+cosinang['chdg']*cya
      cnz=+cza
      azeast_ray=math.atan2(csn,cwe)/conv
      cosinang['caze']=math.cos(conv*azeast_ray)
      cosinang['saze']=math.sin(conv*azeast_ray)
      while (azeast_ray <= 0.):
            azeast_ray=azeast_ray+360.
      chor=max(0.1,np.sqrt(cwe*cwe+csn*csn))
      elhor_ray=math.atan(cnz/chor)/conv
      cosinang['celh']=math.cos(conv*elhor_ray)
      cosinang['selh']=math.sin(conv*elhor_ray)
#
      return azeast_ray,elhor_ray,cxa, cya, cza, cwe, csn, cnz, cosinang



