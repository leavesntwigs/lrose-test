import os.path

def write_sisel_file(directory,
    c_hms_min,
    c_hms_max,
    ihms_min,
    ihms_max,
    iyymmdd,
    orig_lon,
    orig_lat,
    ):

    fich_sisel = f"SIS_E_{c_hms_min[1:7]}_{c_hms_max[1:7]}"

    #******************************************************************
    #**** OPEN THE OUPUT "CORNAV_EL_*" FILE #50
    #******************************************************************
    #
    path = os.path.join(directory, fich_sisel)
    print(' ')
    print(' OPEN "SIS_EL_*" FILE #50 :', path)
    if not os.path.exists(directory):
       os.makedirs(directory)
    print(ihms_min)

    iyymmdd[0] = 2008
    iyymmdd[1] = 14 
    iyymmdd[2] = 9
  
    # byte_array = bytearray([int(orig_lon), int(orig_lat), int(ihms_min), int(ihms_max)])
    with open(path, 'wb') as f50:
        f50.write(int(iyymmdd[0]).to_bytes(3))
        f50.write(int(iyymmdd[2]).to_bytes(2))
        f50.write(int(iyymmdd[1]).to_bytes(2))
        f50.write(orig_lon.to_bytes(3))
        f50.write(orig_lat.to_bytes(3))
        f50.write(ihms_min.to_bytes(3))
        f50.write(ihms_max.to_bytes(3))
    
    return path
