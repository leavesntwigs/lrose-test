

#******************************************************************
#**** DISMISS THE SPECIFIED RANGE GATES
#******************************************************************
#
# ig_dismiss: array of 15; if value > 0, then it is an index in ze/vr/vu to "dismiss", i.e. set to -999


def dismiss_range_gates(ig_dismiss, ze, vr, vu, magic_number=15):
#
    for iig in range(magic_number):
       if (ig_dismiss[iig] > 0):
           ig=ig_dismiss[iig]
           ze[ig]=-999.
           vr[ig]=-999.
           vu[ig]=-999.
    return ze,vr,vu


# original Fortran code; hmmm, why are vg,vl,vs not included above in Python?
#      do iig=1,15
#         if(ig_dismiss(iig).gt.0)then
#           ig=ig_dismiss(iig)
#           ze(ig)=-999.
#           vr(ig)=-999.
#           vs(ig)=-999. !Olivier
#           vl(ig)=-999. !Olivier
#           vg(ig)=-999.
#           vu(ig)=-999.
#         endif
#      enddo
