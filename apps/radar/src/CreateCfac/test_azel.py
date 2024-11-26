# program test_azel
import numpy as np
import azel

# common block is set in the calling function, 
# values are changed in the function,
# then referenced back in the calling function.
# The common block variables are OUT parameters
# Subroutine azel sets all of these common block variables.
   
#common/cosinang/crr,srr,cti,sti
              #,chdg,shdg,cdri,sdri,cpit,spit
              #,caze,saze,celh,selh
 
cosinang = {
   'crr': 0,
   'srr': 0,
   'cti': 0,
   'sti': 0,
   'chdg': 0,
   'shdg': 0,
   'cdri': 0,
   'sdri': 0,
   'cpit': 0,
   'spit': 0,
   'caze': 0,
   'saze': 0,
   'celh': 0,
   'selh': 0
}
 
# call azel(swdzsurf_wri,sw_or_altsurf_wri
#                  ,nx_wrisurf,ny_wrisurf,nxysurfmax)
#
# subroutine azel(rotaroll,tilt_ray
#                ,hdg_acft,drift_acft,pitch_acft
#                ,azeast_ray,elhor_ray
#                ,cxa,cya,cza,cwe,csn,cnz)

#real rotaroll,tilt_ray
               #,hdg_acft,drift_acft,pitch_acft
               #,azeast_ray,elhor_ray
               #,cxa,cya,cza,cwe,csn,cnz

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

print('test 0')
# TODO: should this be a dictionary that is returned?

azeast_ray,
elhor_ray,
cxa, cya, cza, cwe, csn, cnz,
cosinang = azel.azel(rotaroll,tilt_ray
      ,hdg_acft,drift_acft,pitch_acft
      ,azeast_ray,elhor_ray
      ,cxa,cya,cza,cwe,csn,cnz, cosinang)
print(azeast_ray,elhor_ray,cxa, cya, cza, cwe, csn, cnz)
print(cosinang)


