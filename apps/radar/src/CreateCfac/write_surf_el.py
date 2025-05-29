import inter

import numpy as np

def write_surf_el(
    wrisurfile_path,
    swdzsurf_wri, sw_or_altsurf_wri,
    nx_wrisurf,ny_wrisurf,nxysurfmax):

    print('nx_wrisurf,ny_wrisurf: ', nx_wrisurf,ny_wrisurf)
    print(' ')
    print(' WRITES THE "SURF_EL_*" FILE #30 :' , wrisurfile_path)
             # directory(1:ndir)//'/'//wrisurfile(1:nsf)
    print(' INTERPOLATION OF THE RADAR-DERIVED SURFACE MAP')
    sw_or_altsurf_wri = inter.inter(swdzsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
    nwrisurf_ok=0
    ialtsurf_wri = np.zeros(nxysurfmax, dtype=np.int32)
    with open(wrisurfile_path, 'a') as f30:
        f30.write("\n")
        for j_wrisurf in range(0,ny_wrisurf):
            for i_wrisurf in range(0,nx_wrisurf):
                if(abs(sw_or_altsurf_wri[i_wrisurf,j_wrisurf]) < 10.):
                    ialtsurf_wri[i_wrisurf]=(1000.*sw_or_altsurf_wri[i_wrisurf,j_wrisurf])
                    nwrisurf_ok=nwrisurf_ok+1
                else:
                    ialtsurf_wri[i_wrisurf]=-9999
                #if (i_wrisurf == 0):
                #    print("i_wrisurf[0] = ", ialtsurf_wri[i_wrisurf])
                #if (i_wrisurf == nx_wrisurf-1):
                #    print("i_wrisurf[last] = ", ialtsurf_wri[i_wrisurf])
                # print(ialtsurf_wri)


            # Write the array elements using the implied do loop equivalent
            data_to_write = []
            for i_wrisurf in range(0, nx_wrisurf):
                data_to_write.append(ialtsurf_wri[i_wrisurf])  
            
            # Format each integer with 6 characters width (format 500i6)
            formatted_line = ''.join(f'{value:6d}' for value in data_to_write)
            
            # Write to file unit 30
            f30.write(formatted_line + '\n')




            # for i_wrisurf in 1,nx_wrisurf: 
            #     f30.write(f'{ialtsurf_wri[i_wrisurf]:6n}')
     # 222   format(500i6)
        print(' -> NPTS WRITTEN ON THE "SURF_EL_*" FILE #30' ,nwrisurf_ok)
