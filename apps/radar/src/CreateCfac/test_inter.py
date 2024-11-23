      
# 
import numpy as np
import inter


def compare_results(result, expected):
    # print('result: ', result, ' expected: ', expected)
    if (result == expected):
        print('PASS')
    else:
        print('FAIL')


# real x(1000),u(1000),s(1000),del(1000)

q1 = 0
qnx_wrisurf = 0

      # INTEGER v, q1, qn, n 

    
      # 	    call inter(swdzsurf_wri,sw_or_altsurf_wri
      # &                 ,nx_wrisurf,ny_wrisurf,nxysurfmax)
      #
      #       subroutine inter(sp,sz,
      #                    nx,ny,nxysurfmax)
      # dimension sp(nxysurfmax,nxysurfmax),
      # &         sz(nxysurfmax,nxysurfmax),
      # end of dimensions for args

      #  these are filled in inter, and then passed to spline
      # &         x(1000),
      # &         y(1000),
      # &         s(1000),
      # &         d(1000)

      # calls spline ...
      # val=spline(yj,x,y,s,d,q1,qn,n) 

      # function spline(x,u,s,del,q1,qn,n)
      # dimension x(1000),u(1000),s(1000),del(1000)
      #    v, q1, qn, n are all single values

nxysurfmax = 10
swdzsurf_wri = np.ndarray((10,10), dtype=float)

swdzsurf_wri[1,1] = 3
swdzsurf_wri[1,2] = 12
swdzsurf_wri[1,3] = 22
swdzsurf_wri[1,4] = 42
swdzsurf_wri[2,1] = 3
swdzsurf_wri[2,2] = 12
swdzsurf_wri[2,3] = 22
swdzsurf_wri[2,4] = 42
swdzsurf_wri[3,1] = 3
swdzsurf_wri[3,2] = 12
swdzsurf_wri[3,3] = 22
swdzsurf_wri[3,4] = 42
swdzsurf_wri[4,1] = 3
swdzsurf_wri[4,2] = 12
swdzsurf_wri[4,3] = 22
swdzsurf_wri[4,4] = 42

q1 = 0
qnx_wrisurf = 0

# NOT A VALID TEST
nx_wrisurf = 0
ny_wrisurf = 0
# test: nx_wrisurf = 0 
print('')
print('test n=0')
sw_or_altsurf_wri = inter.inter(swdzsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
print('sw_or_altsurf_wri: ')
print(sw_or_altsurf_wri[:10,:10])


# test: nx_wrisurf = 1 
print('')
print('test n=1')
nx_wrisurf = 1
ny_wrisurf = 1
sw_or_altsurf_wri = inter.inter(swdzsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
print('sw_or_altsurf_wri: ')
print(sw_or_altsurf_wri[:10,:10])
expected = 9

# test: nx_wrisurf = 2
print('')
print('test n=2')
nx_wrisurf = 2
ny_wrisurf = 2
sw_or_altsurf_wri = inter.inter(swdzsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
print('sw_or_altsurf_wri: ')
print(sw_or_altsurf_wri[:10,:10])
expected = 0

# test: nx_wrisurf = 3
print('')
print('test n=3')
nx_wrisurf = 3
ny_wrisurf = 3
sw_or_altsurf_wri = inter.inter(swdzsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
print('sw_or_altsurf_wri: ')
print(sw_or_altsurf_wri[:10,:10])
expected = 79 

# test: nx_wrisurf = 4
print('')
print('test n=4')
nx_wrisurf = 4
ny_wrisurf = 4
sw_or_altsurf_wri = inter.inter(swdzsurf_wri,nx_wrisurf,ny_wrisurf,nxysurfmax)
print('sw_or_altsurf_wri: ')
print(sw_or_altsurf_wri[:10,:10])
expected = 79 

