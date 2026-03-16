

def ze_actions(
    iradar_ray,
    ze, vr, vu,
    ichoice_vdop,
    dgate_corr,
    proj_acftspd,
    ngates,
    dmin, dmax,
    xncp_min,
    sw_max,
    ref_mmin, ref_max,
    vdop_max = 200.,
    ):

#
#******************************************************************
#**** CHECK THE NCP, SW AND REFLECTIVITY VALUES
#******************************************************************
#
    ngates_max=1
    for ig in range(ngates):
         ref_min=ref_min0+20.*(alog10(dgate_corr[ig])-1.)
         if (dgate_corr[ig] < dmin
            or dgate_corr[ig] > dmax
            or ncp[ig] < xncp_min
            or sw[ig] > sw_max
            or ze[ig] < ref_min
            or ze[ig] > ref_max):
             ze[ig]=-999.
             vr[ig]=-999.
             # vs[ig]=-999.	#Olivier # not used
             # vl[ig]=-999.	#Olivier # not used
             # vg[ig]=-999.       # not used
             vu[ig]=-999.
         else:
             ngates_max=ig
             nref_ok[iradar_ray]=nref_ok[iradar_ray]+1
       # endif
    # end for
# 10  continue
#
#******************************************************************
#**** CHOOSE WHICH DOPPLER VELOCITY WILL BE USED (FOLLOWING ICHOICE_VDOP)
#**** -> 1:RAW(VR), 2:CORRECTED FOR VACFT(VG), 3:UNFOLDED(VU)
#******************************************************************

    for ig in range(ngates_max):
         vdop_read=-999.
         vdop_corr[ig]=-999.
         if ze[ig] > -900.:
             if (ichoice_vdop == 1
                  and abs(vr[ig]) > 0. and abs(vr[ig]) < vdop_max
                  and proj_acftspd > -900.):
                  vdop_read=vr[ig]+proj_acftspd
             if (ichoice_vdop == 2
                 and abs(vr[ig]) > 0. and abs(vr[ig]) < vdop_max):
                 vdop_read=vr[ig]
             if (ichoice_vdop == 3
                 and abs(vu[ig]) > 0. and abs(vu[ig]) < vdop_max):
                 vdop_read=vu[ig]

             if vdop_read > -900.:
                 ndop_ok[iradar_ray]=ndop_ok[iradar_ray]+1
                 vdop_corr[ig]=vdop_read


    return vdop_read, vdop_corr, ndop_ok, ze, vr, vu
