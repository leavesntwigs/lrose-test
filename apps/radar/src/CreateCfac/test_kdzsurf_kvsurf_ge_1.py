
import numpy as np
import azel
import kdzsurf_kvsurf_ge_1

#kdzsurf = 1
#kvsurf = 1
selh_surf = 2
x_acft = 1
y_acft = 1
z_acft = 1
zacftmin_surf = 0
nb_ray = np.zeros(2)
iradar_ray = 0
nb_ray[iradar_ray] = 10 # this will cause the debug to be printed
#ihhmmss = 
n_dzsurf = np.zeros(2, dtype=np.int32)
altdtm_min = 0
hsurf_ray = 0
wghtsurf_ray = 0
xsurf_ray  = 0 # not sure where this is set ???
xmin_dtm  =0  # set in cns_eldo_cai
xmax_dtm  =100  # set in cns_eldo_cai
ymin_dtm  =0  # set in cns_eldo_cai
ymax_dtm  =100  # set in cns_eldo_cai
hx_dtm = 0
hy_dtm = 0
isim = 0


ny_dtm = 10
nx_dtm = 10
zsurf_cst = 30
# altitude from detailed terrain map; we don't have this, so just set the info to a constant zsurf_cst
alt_dtm = np.zeros((ny_dtm, nx_dtm))
alt_dtm + zsurf_cst
#for jdtm in range(int(ny_dtm)):
#    for idtm in range(int(nx_dtm)):
#        alt_dtm[idtm][jdtm]=zsurf_cst
altdtm_mean=zsurf_cst
altdtm_min=zsurf_cst
altdtm_max=zsurf_cst

igstart_surf=1
ngates_max = igstart_surf + 7 # should be greater than igstart_surf
dgate_corr = np.zeros(ngates_max, dtype=np.float32)  # igstart_surf ... ngates_max ; fill in control_for_end_of_all_text_files_wo_gotos.py
dgate_corr += [1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8]
ze = np.zeros(ngates_max, dtype=np.float32) # same dimensions as dgate_corr
ze += 53
ze[6] = 140
ze[7] = 200


rota_ray = 0
drota_guess = 0
roll_acft = 0
rotaroll = rota_ray+drota_guess+roll_acft

tilt_ray = 0
dtilt_guess = 0
tilt_ray = tilt_ray+dtilt_guess

hdg_acft = 0
dhdg_guess = 0
hdg_acft = hdg_acft+dhdg_guess

drift_acft = 0

pitch_acft = 0
dpitch_guess = 0
pitch_acft = pitch_acft+dpitch_guess

#azeast_ray
#elhor_ray
#    azeast_ray=azest_rdl+corr_azest[iradar_ray] # Mod Oliv
#    elhor_ray=elhor_rdl+corr_elhor[iradar_ray] 

cosinang = {}
cxa = 0.0 
cya = 0.0 
cza = 0.0 
cwe = 0.0 
csn = 0.0 
cnz = 0.0 
azeast_ray,elhor_ray,cxa, cya, cza, cwe, csn, cnz, cosinang = azel.azel( rota_ray+drota_guess+roll_acft
      ,tilt_ray+dtilt_guess
      ,hdg_acft+dhdg_guess,drift_acft
      ,pitch_acft+dpitch_guess)
#      ,azeast_ray,elhor_ray
#      ,cxa,cya,cza,cwe,csn,cnz,
#      cosinang) 


selh = cosinang['selh']  # cannot be zero, otherwise, division by zero.
celh = cosinang['celh']
caze = cosinang['caze']
saze = cosinang['saze']

# test n_dzsurf gets incremented by 1, need these conditions to be true:
# if( (kdzsurf+kvsurf) >= 1 and selh < selh_surf and z_acft > zacftmin_surf)
# if(hsurf_ray > -900. and wghtsurf_ray > 0.):    hsurf_ray is local/derived ; wghtsurf_ray is local/derived

#        if (refmax_ray > refsurf_min
#            and gradrefmax_ray > gradrefsurf_min):
#            if(     (d_refmax > d_gradrefmax)
#                and abs(z_refmax-z_gradrefmax) < 1.):
#
#                hsurf_ray=-999.
#                hsurf_ray=z_refmax    <-- follow this path # z_refmax is local and set to z_ig, but is dependent on dgate_corr[ig] <= distmax; dgate_corr is set in control_for_..wo_gotos
#         or
#  X      if (isim == 1)
#  X          hsurf_ray = z_app

#         wghtsurf_ray=0 ...
#         wghtsurf_ray=sqrt(wght_ref*wght_grad)  <== these must be > 0
# if(xsurf_ray > xmin_dtm           xsurf_ray is local/derived ; xmin_dtm is passed in
# if(abs(d_hsurf) < dhsurf_max):  d_hsurf is local/derived ; dhsurf_max is a constant

n_dzsurf, xmat_vsurf, vect_vsurf, corr_var = kdzsurf_kvsurf_ge_1.kdzsurf_kvsurf_ge_1(  # kdzsurf, kvsurf, # NOTE: These are ALWAYS = 1
    selh, selh_surf, x_acft, y_acft, z_acft, zacftmin_surf, nb_ray,
    iradar_ray,
    #ihhmmss,
    n_dzsurf,
    altdtm_min,
    xmin_dtm,
    xmax_dtm,
    ymin_dtm,
    ymax_dtm,
    hx_dtm,
    hy_dtm,
    isim, # set to 1 if using guess input values.
    igstart_surf,
    ngates_max,
    dgate_corr,
    ze,
    celh,
    caze,
    saze,
    alt_dtm,
    )

print('n_dzsurf: ', n_dzsurf)
