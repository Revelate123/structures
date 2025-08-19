import math
from dataclasses import dataclass

@dataclass
class Masonry:
    length: float|None = None
    height: float|None = None
    thickness: float|None = None
    fuc: float|None = None
    mortar_class: float|None = None
    fut: float = 0.8 # Cl 3.2 - In absence of test data, fut not to exceed 0.8MPa
    fmt: float = -1

    def __post_init__(self):
            print(
                """Version 0.0.1
    All calculations are based on AS3700:2018
    Units unless specified otherwise, are:
    Pressure: MPa 
    Length: mm
    Forces: KN\n"""
            )
            self.Zd = self.length * self.thickness**2 / 6

            self.Zu = self.Zp = self.Zd
            print(f"Zu = Zp = Zd: {self.Zd}")
            self.Zd_horz = self.height * self.thickness**2 / 6
            self.Zu_horz = self.Zp_horz = self.Zd_horz
            self._set_masonry_properties()

    def _set_masonry_properties(self):
        if self.fuc == -1:
            raise ValueError(
                "fuc undefined, for new structures the value is typically 20 MPa, and for existing 10 to 12MPa"
            )
        if self.mortar_class == -1:
            raise ValueError("mortar_class undefined, typically 3")
        if self.mortar_class == 4:
            self.km = 2
        elif self.mortar_class == 3:
            self.km = 1.4
        elif self.mortar_class == 1:
            self.km = 1.1
        else:
            raise ValueError("Invalid mortar class provided")

        if self.hu != None and self.tj != None:
            self.kh = min(1.3 * (self.hu / (19 * self.tj)) ** 0.29, 1.3)
            print(
                f"kh: {self.kh}, based on a masonry unit height of {self.hu} mm and a joint thickness of {self.tj} mm"
            )
        elif self.hu != None and self.tj == None:
            raise ValueError(
                "Masonry unit height provided but mortar thickness tj not provided"
            )
        elif self.hu == None and self.tj != None:
            raise ValueError(
                "joint thickness tj provided but masonry unit height not provided"
            )
        else:
            print(
                f"kh: {self.kh}, this is not usually changed, however, to calculate a new kh enter the masonry unit height, hu and joint thickness, tj, both in mm"
            )

        print(f"km: {self.km}")
        self.fm = math.sqrt(self.fuc) * self.km
        print("fm: ", self.fm)
        self.fmb = self.kh * self.fm
        print("fmb: ", self.fmb)
        self.fms_horizontal = min(max(1.25 * self.fmt, 0.15), 0.35)