# -*- coding: utf-8 -*-
import pya

# FEOL contact row (minimal PCell example)
#
# A single row/column of contacts with an M1 landing bar.
# l and h are in nm (integers = DBU at dbu=0.001 µm).

class feol_contact(pya.PCellDeclarationHelper):
    def __init__(self):
        super().__init__()
        # Parameters
        self.param("l", self.TypeInt, "contact length (nm)", default=260)
        self.param("h", self.TypeInt, "contact height (nm)", default=160)
        self.param("ly_co",     self.TypeLayer, "Contact (CO)",            default=pya.LayerInfo(6, 0))
        self.param("ly_m1",     self.TypeLayer, "Metal1 (M1)",             default=pya.LayerInfo(8, 0))

    def display_text_impl(self):
        return f"feol_contact(l={self.l}nm, h={self.h}nm)"

    def coerce_parameters_impl(self):
        # Keep parameters valid; add rules as needed
        # minimum contact size 160, minimum endcap 50, grid 5
        self.l = max(260, self.l // 5 * 5)
        self.h = max(160, self.h // 5 * 5)

    def produce_impl(self):
        # Resolve layers
        ly_co = self.layout.layer(self.ly_co)
        ly_m1 = self.layout.layer(self.ly_m1)

        contact_size    = 160
        contact_distance= 180
        contact_pitch   = contact_size + contact_distance
        metal1endcap    =  50   # metal 1 end cap
        l = self.l
        h = self.h
        n_cuts_x = max(0, (l + contact_distance - 2 * metal1endcap) // contact_pitch)
        n_cuts_y = max(0, (h + contact_distance)                     // contact_pitch)
        xext = n_cuts_x * contact_pitch - contact_distance
        yext = n_cuts_y * contact_pitch - contact_distance
        start_x = (l - xext) // 10 * 5
        start_y = (h - yext) // 10 * 5

        for row in range(n_cuts_y):
            for col in range(n_cuts_x):
                xl = start_x + col * contact_pitch
                yb = start_y + row * contact_pitch
                self.cell.shapes(ly_co).insert(
                    pya.Box(xl, yb, xl + contact_size, yb + contact_size))
        # M1 landing bar that covers the row of contacts
        self.cell.shapes(ly_m1).insert(pya.Box(0, 0, l, h))

# Register library
class BasicsLib(pya.Library):
    def __init__(self):
        super().__init__()  # important
        self.description = "A very basic pcell library"
        # Register PCells
        self.layout().register_pcell("FEOL contacts", feol_contact())
        # Register the library by name
        self.register("BasicsLib")

def load_libraries():
    BasicsLib()

load_libraries()

