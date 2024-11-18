import numpy as np

# xmat (in param)
# res  (out param)
# vect (in param)
# nvar (in param)
# ierr (out param)
# 
# chol_inv(xmat, res, vect, nvar, ierr)  called at line 3912; from resoud at line 1682
# chol_inv(   a,   x,    b,    n, ierr)
#            in, out,   in,   in,  out)
def chol_inv(a, b, n):
    x = np.zeros(n, dtype=np.float32)
    # b = np.zeros(n, dtype=np.float32)
    p = np.zeros(100, dtype=np.float32)  # n <= 100
    ierr = 0

    for i in range(n):
        for j in range(n):
            sum_val = a[i, j]
            for k in range(i - 1, -1, -1):
                sum_val -= a[i, k] * a[j, k]
            if i == j:
                if sum_val <= 0.0:
                    ierr = -1
                    print('  Choleski Decomposition Failed')
                    return ierr, x
                else:
                    p[i] = np.sqrt(sum_val)
            else:
                a[j, i] = sum_val / p[i]

    if ierr == 0:  # solve the linear system using forward and back substitution
        # Solve A x = L (LT x) = b
        # First solve L y = b
        for i in range(n):  # solve L y = b, storing y in x
            sum_val = b[i]
            for k in range(i - 1, -1, -1):
                sum_val -= a[i, k] * x[k]
            x[i] = sum_val / p[i]

        # Then solve LT x = y
        for i in range(n - 1, -1, -1):  # solve LT x = y
            sum_val = x[i]
            for k in range(i + 1, n):
                sum_val -= a[k, i] * x[k]
            x[i] = sum_val / p[i]

    return ierr, x


