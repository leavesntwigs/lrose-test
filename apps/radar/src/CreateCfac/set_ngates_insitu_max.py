
#******************************************************************
#**** RANGE GATES FOR COMPARISONS WITH FLIGHT-LEVEL (IN SITU) DATA
#******************************************************************
#   
def set_ngates_insitu_max(selh, 
    # selhinsitu_max, 
    MAXPORT, dgate_corr, dmax_insitu):

    ngates_insitu_max=-999
    selhinsitu_max=0.1
    if abs(selh) < selhinsitu_max:
        ig=1
        while (ig < MAXPORT and dgate_corr[ig] < dmax_insitu):
            ngates_insitu_max=ig
            ig=ig+1
    return ngates_insitu_max
