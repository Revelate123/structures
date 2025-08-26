import math

from dataclasses import dataclass

from sectionproperties.pre.library import rectangular_hollow_section, rectangular_section, i_section
from sectionproperties.pre import Material
steel = Material(
    name="Steel",
    elastic_modulus=200e3,  # N/mm^2 (MPa)
    poissons_ratio=0.3,  # unitless
    density=7.85e-6,  # kg/mm^3
    yield_strength=300,  # N/mm^2 (MPa)
    color="grey",
)

@dataclass
class SteelBeam:
    d:float|None = None
    b:float|None = None
    t_f:float|None = None
    t_w:float|None = None
    r:float|None = None
    n_r:float|None = None
    material:Material = steel

    def __post_init_(self):
        if self.d is None:
            raise ValueError("d not set")
        


    def _calc_section_properties(self):
        pass

    def _calc_section_bending_capacity(self):
        pass

    def _calc_member_bending_capacity(self, Ms:float|None = None, verbose:bool = True):
        """
        Calculates the member bending capacity in accordance with AS 4100:2020 Cl 5.6.1

        Args:
            Ms: Unfactored section moment capacity to AS4100.
            verbose: If True, print internal calculation details.

        Returns:
            Mb: Unfactored section moment capacity to AS4100.
        """
        alpha_m = self._calc_alpha_m()
        alpha_s = self._calc_alpha_s()
        Mb = min(alpha_m * alpha_s * Mb, Mb)
        if verbose:
            print(f"Mb: {Mb} KNm")
        return Mb

    def _calc_alpha_m(self):
        pass

    def _calc_alpha_s(self, Ms:float|None = None, verbose:bool =True):
        Le = self._calc_Le()
        Moa = self._calc_Mo(Le=Le, verbose=verbose)
        alpha_s = 0.6*(math.sqrt((Ms/Moa)**2+3)-(Ms/Moa))

    def _calc_Le(self):
        pass

    def _calc_Mo(self, Le:float|None = None, verbose:bool = True):
        """ Calculates the reference buckling moment for a section with equal flanges according to AS4100:2020 Cl 5.6.1.1(3)"""
        if Le is None:
            raise ValueError("Le not set.")
        left_bracket = (math.pi**2 * self.E * self.Iy)/Le**2
        right_bracket = self.G*self.J + (math.pi**2 * self.E * self.Iw)/Le**2
        Mo = math.sqrt(left_bracket*right_bracket)
        if verbose:
            print(f"Mo: {Mo}")
        return Mo

