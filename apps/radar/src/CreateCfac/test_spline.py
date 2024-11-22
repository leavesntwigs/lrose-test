      
# 
import numpy as np
import spline


def compare_results(result, expected):
    # print('result: ', result, ' expected: ', expected)
    if (result == expected):
        print('PASS')
    else:
        print('FAIL')


# real x(1000),u(1000),s(1000),del(1000)

q1 = 0
qn = 0

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

x = np.array([3., 12., 22., 42., 40.])
u = np.array([9., 8., 7., 6., 5])

# TODO: how to handle these out parameters?  
# **1. create them inside spline as arrays of length n
#   2. pass them in, preallocated.
# dely = np.array([1., 1., 1., 1.])
# s = np.array([1., 1., 1., 1.])

q1 = 0
qn = 0

# NOT A VALID TEST
n = 0
# test: n = 0 
print('')
print('test n=0')
s, dely = spline.spline(x,u,q1,qn,n)
print('dely: ', dely[:10])
print('s: ', s[:10])


# test: n = 1 
print('')
print('test n=1')
n = 1
s, dely = spline.spline(x,u,q1,qn,n)
print('dely: ', dely[:10])
print('s: ', s[:10])
expected = 9

# test: n = 2
print('')
print('test n=2')
n = 2
s, dely = spline.spline(x,u,q1,qn,n)
print('dely: ', dely[:10])
print('s: ', s[:10])
expected = 0

# test: n = 3
print('')
print('test n=3')
n = 3
s, dely = spline.spline(x,u,q1,qn,n)
print('dely: ', dely[:10])
print('s: ', s[:10])
expected = 79 

# test: n = 4
print('')
print('test n=4')
n = 4
s, dely = spline.spline(x,u,q1,qn,n)
print('dely: ', dely[:10])
print('s: ', s[:10])
expected = 79 

