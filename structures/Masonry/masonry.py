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
                """
All calculations are based on AS3700:2018
Units unless specified otherwise, are:
Pressure: MPa 
Length: mm
Forces: KN\n"""
            )
            self.Zd = self.length * self.thickness**2 / 6
            self.Zu = self.Zp = self.Zd
            self.Zd_horz = self.height * self.thickness**2 / 6
            self.Zu_horz = self.Zp_horz = self.Zd_horz