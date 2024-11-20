      
# 
import numpy as np
import splin

# real x(1000),u(1000),s(1000),del(1000)

s   = np.zeros(3)
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

      #  these are filled in inter, and then passed to splin
      # &         x(1000),
      # &         y(1000),
      # &         s(1000),
      # &         d(1000)

      # calls splin ...
      # val=splin(yj,x,y,s,d,q1,qn,n) 

      # function splin(v,x,u,s,del,q1,qn,n)
      # dimension x(1000),u(1000),s(1000),del(1000)
      #    v, q1, qn, n are all single values

x = np.array([3., 12., 22., 42.])
u = np.array([9., 8., 7., 6.])
dely = np.array([1., 1., 1., 1.])
n = 4
# test: v-x(1) < 0 
v = 1 
result = splin.splin(v,x,u,s,dely,q1,qn,n)
expected = 0
print('result: ', result, ' expected: ', expected)
if (result == expected):
    print('PASS')
else:
    print('FAIL')

# test: v-x(1) == 0 
v = x[0] 
result = splin.splin(v,x,u,s,dely,q1,qn,n)
expected = 9
print('result: ', result, ' expected: ', expected)
if (result == expected):
    print('PASS')
else:
    print('FAIL')

# test: v-x(1) > 0 && v-x(2:n) > 0
v = 50
result = splin.splin(v,x,u,s,dely,q1,qn,n)
expected = 0
print('result: ', result, ' expected: ', expected)
if (result == expected):
    print('PASS')
else:
    print('FAIL')

# test: v-x(1) > 0  && v-x(2:n) <= 0
v = 5 
result = splin.splin(v,x,u,s,dely,q1,qn,n)
expected = 79 
print('result: ', result, ' expected: ', expected)
if (result == expected):
    print('PASS')
else:
    print('FAIL')

