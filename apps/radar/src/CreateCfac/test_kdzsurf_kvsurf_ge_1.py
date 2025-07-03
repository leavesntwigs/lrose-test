
import numpy as np
import kdzsurf_kvsurf_ge_1

kdzsurf = 1
kvsurf = 1
selh = 1  # cannot be zero, otherwise, division by zero.
selh_surf = 2
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
isim = 0

igstart_surf=5
ngates_max = igstart_surf + 3 # should be greater than igstart_surf
dgate_corr = np.zeros(ngates_max, dtype=np.float32)  # igstart_surf ... ngates_max ; fill in control_for_end_of_all_text_files_wo_gotos.py
dgate_corr += [1,2,3,4,5,6,7,8]
ze = np.zeros(ngates_max, dtype=np.float32) # same dimensions as dgate_corr

celh = 0

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

n_dzsurf = kdzsurf_kvsurf_ge_1.kdzsurf_kvsurf_ge_1(kdzsurf, kvsurf,
    selh, selh_surf, z_acft, zacftmin_surf, nb_ray,
    iradar_ray,
    #ihhmmss,
    n_dzsurf,
    altdtm_min,
    xmin_dtm,
    isim, # set to 1 if using guess input values.
    igstart_surf,
    ngates_max,
    dgate_corr,
    ze,
    celh,
    )

print('n_dzsurf: ', n_dzsurf)
