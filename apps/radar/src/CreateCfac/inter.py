import numpy as np

# def inter(sp, sz, nx, ny, nxysurfmax):  ! fortran autoconversion
def inter(sp, nx, ny, nxysurfmax):  # BEJ conversion
    nsaut = 5
    nmin = 5
    spmin = 1.0
    nin = 0
    nintx = 0
    ninty = 0
    nout = 0
    sz = np.zeros((nxysurfmax,nxysurfmax), dtype='float', order='F')
    x = np.zeros(1000)
    y = np.zeros(1000)
    s = np.zeros(1000)
    d = np.zeros(1000)

    for j in range(ny):
        for i in range(nx):
            if sp[i, j] > spmin:
                sz[i, j] = sz[i, j] / sp[i, j]
                nin += 1
            else:
                print('sp[i,j]=', sp[i,j], ' setting sz[', i, ',', j, ']=-999')
                sz[i, j] = -999.0

    print('     -> ALONG X')
    for j in range(ny):
        imax = 0
        imin = imax
        iant = 0
        n = 0
        for i in range(imin, nx):
            imax = i
            if sz[i, j] > -900.0:
                if iant != 0 and (i - iant) > nsaut + 1:
                    break
                iant = i
                n += 1
                x[n - 1] = float(i)
                y[n - 1] = sz[i, j]

        if n >= nmin:
            q1 = (y[1] - y[0]) / (x[1] - x[0])
            qn = (y[n - 1] - y[n - 2]) / (x[n - 1] - x[n - 2])
            s = np.zeros(1000)  # Placeholder for spline coefficients
            d = np.zeros(1000)  # Placeholder for spline derivatives
            # spline(x[:n], y[:n], s, d, q1, qn, n) ! fortran autoconversion
            s, d = spline(x[:n], y[:n], q1, qn, n)  # conversion BEJ
            for i in range(imin, imax + 1):
                if sz[i, j] < -900.0:
                    xi = float(i)
                    val = splin(xi, x[:n], y[:n], s, d, q1, qn, n)
                    if val > 0.0:
                        sz[i, j] = val
                        nintx += 1

        if imax <= (nx - nsaut + 1):
            continue

    print('     -> ALONG Y')
    for i in range(nx):
        jmax = 0
        jmin = jmax
        jant = 0
        n = 0
        for j in range(jmin, ny):
            jmax = j
            if sz[i, j] > -900.0:
                if jant != 0 and (j - jant) > nsaut + 1:
                    break
                jant = j
                n += 1
                x[n - 1] = float(j)
                y[n - 1] = sz[i, j]

        if n >= nmin:
            q1 = (y[1] - y[0]) / (x[1] - x[0])
            qn = (y[n - 1] - y[n - 2]) / (x[n - 1] - x[n - 2])
            s = np.zeros(1000)  # Placeholder for spline coefficients
            d = np.zeros(1000)  # Placeholder for spline derivatives
            # spline(x[:n], y[:n], s, d, q1, qn, n) ! fortran autoconversion
            s, d = spline(x[:n], y[:n], q1, qn, n) # conversion BEJ
            for j in range(jmin, jmax + 1):
                if sz[i, j] < -900.0:
                    yj = float(j)
                    val = splin(yj, x[:n], y[:n], s, d, q1, qn, n)
                    if val > 0.0:
                        sz[i, j] = val
                        ninty += 1
                        nput = nout + 1
                else:
                    nout += 1

        if jmax <= (ny - nmin + 1):
            continue

    print('     -> N_in,int_X,int_Y,out :', nin, nintx, ninty, nout)

    return sz


