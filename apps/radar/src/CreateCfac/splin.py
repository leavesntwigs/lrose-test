def splin(v, x, u, s, del_, q1, qn, n):
    tester = v - x[0]
    print('tester = ', tester)
    if tester < 0:
        return 0.0
    if tester > 0:
        for k in range(1, n):
            tester2 = v - x[k]
            if tester2 <= 0:
                k1 = k - 1
                ff1 = s[k1] * (x[k] - v) ** 3
                ff2 = s[k] * (v - x[k1]) ** 3
                ff3 = 1 / (6 * del_[k])
                f1 = (ff1 + ff2) * ff3
                f2 = (v - x[k1]) * (u[k] / del_[k] - s[k] * del_[k] / 6)
                f3 = (x[k] - v) * (u[k1] / del_[k1] - s[k1] * del_[k1] / 6)
                return f1 + f2 + f3
    
        return 0.0
    else: # tester == 0:
        return u[0]


