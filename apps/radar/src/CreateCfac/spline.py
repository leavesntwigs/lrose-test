import numpy as np

      # parameters (in/out)
      # x (in)
      # u (in)
      # s (out)
      # del (out)
      # q1 (in)
      # qn (in)
      # n (in)

# TODO: clean up that 1000 magic number!
# TODO: return error? if n<=0, this causes a division by zero error
def spline(x, u, q1, qn, n):
    
    del_ = np.zeros(1000)
    s = np.zeros(1000)
    v = np.zeros(1000)

    del_[1] = x[1] - x[0]
    v[0] = 6. * ((u[1] - u[0]) / del_[1] - q1)
    n1 = n - 1

    for i in range(1, n1):
        print('inside loop 1')
        del_[i + 1] = x[i + 1] - x[i]
        v[i] = ((u[i - 1] / del_[i]) - u[i] * ((1. / del_[i]) + (1. / del_[i + 1])) + (u[i + 1] / del_[i + 1])) * 6.

    # fortran: v[n] = (qn + (u[n1] - u[n]) / del_[n]) * 6. # autoconverted
    v[n-1] = (qn + (u[n1-1] - u[n-1]) / del_[n-1]) * 6.    # BEJ adjusted

    a = np.zeros(1000)
    a[0] = 2. * del_[1]
    a[1] = 1.5 * del_[1] + 2. * del_[2]
    v[1] = v[1] - 0.5 * v[0]

    for i in range(2, n1):
        print('inside loop 2')
        c = del_[i] / a[i - 1]
        a[i] = 2. * (del_[i] + del_[i + 1]) - c * del_[i]
        v[i] = v[i] - c * v[i - 1]

    # if n > 0:   # BEJ added to prevent division by zero in next statement
    # fortran:  c = del_[n] / a[n1]     # autoconverted
    # fortran: a[n] = 2. * del_[n] - c * del_[n] # autoconverted
    # fortran: v[n] = v[n] - c * v[n1] # autoconverted
    # fortran: s[n] = v[n] / a[n] # autoconverted

    c = del_[n-1] / a[n1-1]                 # BEJ adjusted
    a[n-1] = 2. * del_[n-1] - c * del_[n-1]       # BEJ adjusted
    v[n-1] = v[n-1] - c * v[n1-1]                 # BEJ adjusted
    s[n-1] = v[n-1] / a[n-1]                      # BEJ adjusted

    for j in range(n1):
        print('inside loop 3')
        i = n - j - 1
        s[i] = (v[i] - del_[i + 1] * s[i + 1]) / a[i]
    
    return s, del_


