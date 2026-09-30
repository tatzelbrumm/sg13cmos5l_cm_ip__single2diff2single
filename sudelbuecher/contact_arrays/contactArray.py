# Excerpt, verbatim: IHP-Open-PDK dev 0488153, ihp-sg13g2/libs.tech/klayout/python/
# sg13g2_pycell_lib/ihp/geometry.py lines 859-914 (sg13cmos5l's geometry.py symlinks here)
# Copyright 2023 IHP PDK Authors, Apache License 2.0

def contactArray(self, pathLayer, contLayer, xl, yl, xh, yh, ox, oy, ws, ds):
    eps = self.tech.getTechParams()['epsilon1']

    w = xh-xl
    h = yh-yl

    mlist = list()

    nx = floor((w-ox*2+ds)/(ws+ds)+eps)
    if (nx <= 0) :
        return mlist

    dsx = 0
    if (nx == 1) :
        dsx = 0
    else :
        dsx = (w-ox*2-ws*nx)/(nx-1)

    ny = floor((h-oy*2+ds)/(ws+ds)+eps)
    if (ny <= 0) :
        return mlist

    dsy = 0
    if (ny == 1) :
        dsy = 0
    else :
        dsy = (h-oy*2-ws*ny)/(ny-1)

    x = 0
    if (nx == 1) :
        x = (w-ws)/2
    else :
        x = ox

    if pathLayer :
        mlist.append(dbCreateRect(self, pathLayer, Box(xl, yl, xh, yh)))

    for i in range(int(nx)) :
    #for(i=1; i<=nx; i++) {
        y = 0
        if ny == 1 :
            y = (h-ws)/2
        else :
            y = oy

        for j in range(int(ny)) :
        #for(j=1; j<=ny; j++) {
            mlist.append(dbCreateRect(self, contLayer, Box(xl+tog(x), yl+tog(y), xl+tog(x+ws), yl+tog(y+ws))))
            y = y+ws+dsy

        x = x+ws+dsx

    if pathLayer :
        mlist.append(dbCreateRect(self, pathLayer, Box(xl, yl, xh, yh)))

    return mlist
