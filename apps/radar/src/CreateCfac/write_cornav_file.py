import os.path

def write_cornav_file(directory,
    c_hms_min,
    c_hms_max,
    # ihms_min,
    yymmdd,
    rw_dzsurf,
    rw_vsurf,
    rw_dvinsitu,
    idtiltaft,idtiltfore,
    idrotaaft,idrotafore,
    idpitch,idhdg,
    irdaft,irdfore,
    idxwe,idysn,idzacft,
    idvh,
    idtmfile,
    dtm_file,
    zsurf_cst,
    iwrisurfile,
    wrisurfile,
    ):

    fich_cornav = f"CORNAV_E_{c_hms_min[1:7]}_{c_hms_max[1:7]}"
    # fich_sis = f"SIS_E_{c_hms_min[1:7]}_{c_hms_max[1:7]}"

    # writes output to a string
    # write(c_hms_min,"(i7)")1000000+ihms_min
    # write(c_hms_max,"(i7)")1000000+ihms_max
    # write(fich_cornav,"('CORNAV_E_',a6,'_',a6)")
    #      c_hms_min(2:7),c_hms_max(2:7)
    # write(fich_sis,"('SIS_E_',a6,'_',a6)")
    #      c_hms_min(2:7),c_hms_max(2:7)
    #
    #******************************************************************
    #**** OPEN THE OUPUT "CORNAV_EL_*" FILE #10
    #******************************************************************
    #
    path = os.path.join(directory, fich_cornav)
    print(' ')
    print(' OPEN "CORNAV_EL_*" FILE #10 :', path)
    if not os.path.exists(directory):
       os.makedirs(directory)
    with open(path, 'w') as f10:
        #open(10,file=directory(1:ndir)//'/'//fich_cornav
        #       ,form='formatted',status='unknown')
        print("yymmdd: ", yymmdd)
        f10.write(f"{' YYYYMMDD : '}{yymmdd.strftime("%Y%d%m"):>12}\n") # yymmdd:<12}\n")
        #f10.write(f'{"' HHMMSS_min HHMMSS_max : '}{,a6,3x,a6,/)")
        #     c_hms_min(2:7),c_hms_max(2:7)
        f10.write(f'{" FIELDS TAKEN INTO ACCOUNT\n"}')
        f10.write(f'{"  -> REL.WGHT_dZsurf,Vsurf,dVinsitu : "}{rw_dzsurf:6.3f}{rw_vsurf:6.3f}{rw_dvinsitu:6.3f}\n')
        f10.write(" VARIABLES TAKEN INTO ACCOUNT\n")
        f10.write(f'{"  -> D_TILT_AFT,D_TILT_FORE (1/0) : "}{idtiltaft:2n}{idtiltfore:2n}\n')
        f10.write(f'{"  -> D_ROTA_AFT,D_ROTA_FORE (1/0) : "}{idrotaaft:2n}{idrotafore:2n}\n')
        f10.write(f'{"  -> D_PITCH,D_HEADING (1/0) : "}{idpitch:2n}{idhdg:2n}\n')
        f10.write(f'{"  -> RANGE_DELAY_AFT,RANGE_DELAY_FORE (1/0) : "}{irdaft:2n}{irdfore:2n}\n')
        f10.write(f'{"  -> D_XWE,D_YSN,D_ZACFT (1/0) : "}{idxwe:2n}{idysn:2n}{idzacft:2n}\n')
        f10.write(f'{"  -> D_VHACFT (1/0) : "}{idvh:2n}\n')
        if idtmfile == 1:
          f10.write(f'{" READS THE SURF_DTM_* FILE :"}{os.path.join(directory, dtm_file)}\n')
               # directory(1:ndir)//'/'//dtm_file(1:ndtmfile)
        else:
          f10.write(f'{" NO SURF_DTM_* FILE TO READ "}')
          f10.write(f'{"-> ALT_SURF(x,y)=CST ("}{zsurf_cst:6.3f}{")"}\n')
          # f10.write(f'{   '-> ALT_SURF(x,y)=CST (',f6.3,')')")
               # zsurf_cst
        # endif
        if iwrisurfile == 1:
          f10.write(f'{" WRITES THE SURF_EL_* FILE :                 "}{ os.path.join(directory, wrisurfile)}\n') 
               # directory(1:ndir)//'/'//wrisurfile(1:nsf)
        else:
          f10.write(f'{" NO SURF_EL_* FILE TO WRITE "}')
    

