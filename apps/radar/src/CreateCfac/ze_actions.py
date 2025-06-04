def ze_actions(nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins):
#
#******************************************************************
#**** DISMISS THE SPECIFIED RANGE GATES
#******************************************************************
#
    for iig in range(15): 
       iig += 1
       if (ig_dismiss[iig] > 0):
           ig=ig_dismiss[iig]
           ze[ig]=-999.
           vr[ig]=-999.
           vs[ig]=-999.	#Olivier
           vl[ig]=-999.	#Olivier
           vg[ig]=-999.
           vu[ig]=-999.
#
#******************************************************************
#**** RANGE GATES FOR COMPARISONS WITH FLIGHT-LEVEL (IN SITU) DATA
#******************************************************************
#
    ngates_insitu_max=-999
    if abs(selh) < selhinsitu_max:
        ig=1
        while (     ig < MAXPORT
                 and dgate_corr[ig] < dmax_insitu):
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
         ref_min=ref_min0+20.*(alog10(dgate_corr[ig])-1.)
         if (dgate_corr[ig] < dmin
            or dgate_corr[ig] > dmax
            or ncp[ig] < xncp_min
            or sw[ig] > sw_max
            or ze[ig] < ref_min
            or ze[ig] > ref_max):
             ze[ig]=-999.
             vr[ig]=-999.
             vs[ig]=-999.	#Olivier
             vl[ig]=-999.	#Olivier
             vg[ig]=-999.
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
         #endif

       #endif
    #enddo

    nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins = kdzsurf_kvsurf_ge_1.kdzsurf_kvsurf_ge_1(
        kdzsurf, kvsurf,
        nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins) #  needs ze ...
#
#******************************************************************
#**** CASE "DVDOP_insitu"
#**** (if D<DMAX_insitu and ||sin(ELEV_HOR)||<0.1)
#******************************************************************
#
    ssurfins = dvdop_insitu(ssurfins)  # needs ze ...

    return nb1,nb2,nb3,nb4,nb5,nb6,nb7,nb8,nsup,nbtotals,nbon,nmauvais,ssurfins
