# Excerpt, verbatim: IHP-Open-PDK dev 0488153, ihp-sg13g2/libs.tech/klayout/python/
# sg13g2_pycell_lib/ihp/geometry.py lines 813-854 (sg13cmos5l's geometry.py symlinks here)
# Copyright 2023 IHP PDK Authors, Apache License 2.0

def DrawContArray(self, layer, bbox, size, space, over):
    epsilon = self.techparams['epsilon1']

    bbox = bbox.fix()

    x1 = bbox.left
    x2 = bbox.right
    y1 = bbox.bottom
    y2 = bbox.top

    xanz = fix((x2-x1-2*over+space+epsilon)/(size+space))
    yanz = fix((y2-y1-2*over+space+epsilon)/(size+space))

    name = self.tech.name().split()[0]
    if name == 'SG13_dev' :
        cont_layer = 'Cont'
        cont_dist_big = self.techparams['Cnt_b1']
        cont_dist_big_nr = self.techparams['Cnt_b1_nr']

        # now check, if it is cont and more than 4 rows/lines
        if layer.name==cont_layer and xanz>=cont_dist_big_nr and yanz>=cont_dist_big_nr :
            # it has to be bigger space between contacts
            space = cont_dist_big
            # it has to be bigger space between contacts
            xanz = fix((x2-x1-2*over+space+epsilon)/(size+space))
            yanz = fix((y2-y1-2*over+space+epsilon)/(size+space))

    xmin = xanz*(size+space)-space+2*over
    ymin = yanz*(size+space)-space+2*over
    xoff = (x2-x1-xmin)/2
    xoff = GridFix(xoff)
    yoff = (y2-y1-ymin)/2
    yoff = GridFix(yoff)

    for j in range(int(yanz)):
        for i in range(int(xanz)):
            dbCreateRect(self, layer, Box(x1+xoff+over+(size+space)*i, y1+yoff+over+(size+space)*j,
                                          x1+xoff+over+(size+space)*i+size, y1+yoff+over+(size+space)*j+size))

    return Box(x1+xoff+over, y1+yoff+over,
               x1+xoff+over+xanz*size+(xanz-1)*space,
               y1+yoff+over+yanz*size+(yanz-1)*space)
