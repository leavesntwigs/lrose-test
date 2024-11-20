import numpy as np

      # parameters (in/out)
      # x (in)
      # u (in)
      # s (out)
      # del (out)
      # q1 (in)
      # qn (in)
      # n (in)

def spline(x, u, s, del_, q1, qn, n):
    del_[1] = x[1] - x[0]
    v = np.zeros(1000)
    v[0] = 6. * ((u[1] - u[0]) / del_[1] - q1)
    n1 = n - 1
    
    for i in range(1, n1):
        del_[i + 1] = x[i + 1] - x[i]
        v[i] = ((u[i - 1] / del_[i]) - u[i] * ((1. / del_[i]) + (1. / del_[i + 1])) + (u[i + 1] / del_[i + 1])) * 6.
    
    v[n] = (qn + (u[n1] - u[n]) / del_[n]) * 6.
    
    a = np.zeros(1000)
    a[0] = 2. * del_[1]
    a[1] = 1.5 * del_[1] + 2. * del_[2]
    v[1] = v[1] - 0.5 * v[0]
    
    for i in range(2, n1):
        c = del_[i] / a[i - 1]
        a[i] = 2. * (del_[i] + del_[i + 1]) - c * del_[i]
        v[i] = v[i] - c * v[i - 1]
    
    c = del_[n] / a[n1]
    a[n] = 2. * del_[n] - c * del_[n]
    v[n] = v[n] - c * v[n1]
    
    s[n] = v[n] / a[n]
    for j in range(n1):
        i = n - j - 1
        s[i] = (v[i] - del_[i + 1] * s[i + 1]) / a[i]
    
    return s, del_


