"""
This module performs engineering calculations in accordance with
AS3700:2018 for unreinforced masonry
"""

import math
from dataclasses import dataclass

# ...

def round_half_up(n, decimals=0):
    """
    Rounds positive numbers up, as a human would expect. Requires a 'fudge'
    factor denoted by + 10**-(decimals*2) to account for rounding point errors
    for example, 5.42 * 0.75 = 4.06499999999999, which would round to 
    4.06 incorrectly.
    """
    if n < 0:
        raise ValueError("This function should not be used to round negative numbers")
    multiplier = 10**decimals
    return math.floor(n * multiplier + 0.5 + 10**-(decimals*2)) / multiplier

# pylint: disable=too-many-instance-attributes
@dataclass
class Clay:
    """
    For the design of unreinforced clay brick masonry in accordance with AS3700:2018
    """

    length: float | None = None
    height: float | None = None
    thickness: float | None = None
    fuc: float | None = None
    mortar_class: float | None = None
    bedding_type: bool | None = None
    fm: float | None = None
    fmt: float | None = None
    fut: float = 0.8
    hu: float = 76
    tj: float = 10
    phi_shear: float = 0.6
    phi_bending: float = 0.6
    phi_compression: float = 0.75
    density: float = 19
    epsilon: float = 2

    def basic_compressive_capacity(self, verbose: bool = True) -> float:
        """Computes the Basic Compressive strength to AS3700 Cl 7.3.2(2)
        and returns a value in MPa"""
        km = self._calc_km(verbose=verbose)
        self._calc_fm(km=km, verbose=verbose)

        basic_comp_cap = round_half_up(self.phi_compression * self.fm, self.epsilon)
        if verbose:
            print(f"phi_compression: {self.phi_compression}")
            print(
                f"basic_compressive_capacity = {basic_comp_cap} MPa \
                (Basic Compressive Capacity Cl 7.3.2(2))"
            )
        return basic_comp_cap

    def compression_capacity(
        self,
        simple_av: float | None = None,
        kt: float | None = None,
        compression_load_type: int | None = None,
        verbose: bool = True,
    ) -> float:
        """
        Computes the compression capacity of a masonry wall element using the simplified method,
        described in AS 3700.

        Args:
            loads: List of applied loads in kN.
            simple_av: Coefficient (1 or 2.5) based on lateral support.
            kt: Coefficient for engaged piers (1 if none).
            compression_load_type: Type of compression loading (1, 2, or 3).
            verbose: If True, print internal calculation details.

        Returns:
            A dictionary with crushing and buckling capacity in kN.
        """
        if compression_load_type not in [1, 2, 3]:
            raise ValueError(
                """compression_load_type undefined, refer AS 3700 Cl 7.3.3.3.
                    Options are:
                        1: concrete slab
                        2: other systems as defined in Table 7.1,
                        3: wall with load applied to the face as defined in Table 7.1"""
            )
        if simple_av is None:
            raise ValueError(
                "simple_av undefined, refer AS 3700 Cl 7.3.3.4."
                "Set to 1 if member is laterally supported along top edge, else 2.5"
            )
        if kt is None:
            raise ValueError(
                "kt undefined, refer AS 3700 Cl 7.3.4.2, set to 1 if there are no engaged piers"
            )

        basic_comp_cap = self.basic_compressive_capacity(verbose)

        srs = (simple_av * self.height) / (kt * self.thickness)
        if verbose:
            print("\nBuckling capacity:")
            print(f"Srs = {srs:.2f} (Simplified slenderness ratio Cl 7.3.3.3)")

        if compression_load_type == 1:
            k = min(0.67 - 0.02 * (srs - 14), 0.67)
            if verbose:
                print("Load type: Concrete slab over")
        elif compression_load_type == 2:
            k = min(0.67 - 0.025 * (srs - 10), 0.67)
            if verbose:
                print("Load type: Other systems (Table 7.1)")
        elif compression_load_type == 3:
            k = min(0.067 - 0.002 * (srs - 14), 0.067)
            if verbose:
                print("Load type: Load applied to face of wall (Table 7.1)")
        else:
            raise ValueError("")

        simple_comp_cap = k * basic_comp_cap * self.length * self.thickness * 1e-3
        if verbose:
            print(f"k: {k}")
            print(f"Simple compression capacity kFo: {simple_comp_cap:.2f}")

        return simple_comp_cap

    def refined_compression(
        self,
        refined_av: float | None = None,
        refined_ah: float | None = None,
        kt: float | None = None,
        e1: float | None = None,
        e2: float | None = None,
        dist_to_return: float | None = None,
        effective_length: float | None = None,
        verbose: bool = True,
    ) -> dict:
        """Computes the refined compressive capacity of a masonry wall per AS3700 Cl 7.3.

        Parameters:
            loads (list): Axial loads (kN) to check against capacities.
            refined_av (float): Coefficient for vertical restraint.
            refined_ah (float): Coefficient for horizontal restraint.
            kt (float): Coefficient for engaged piers.
            w_left, w_direct, w_right (float): Applied loads (kN) from left,
                            right and center based on applied slab loading.
                            May be overriden by setting e1, e2.
            e1, e2 (float): End eccentricities (mm).
            dist_to_return (float): Distance to return wall (mm).
            effective_length (float): Length of wall used in calculations (mm).
            verbose (bool): Whether to print outputs.

        Returns:
            dict: {
                'Crushing': crushing_compressive_capacity,
                'Buckling': kFo,
            }
        """

        if effective_length is None:
            effective_length = self.length
        if verbose:
            print(
                f"effective length of wall used in calculation: {effective_length} mm"
            )

        basic_comp_cap = self.basic_compressive_capacity(verbose)

        if e1 is None or e2 is None:
            raise ValueError(
                "e1 and/or e2 is not set. "
                "This is the eccentricity of the applied loads, where" \
                "e1 is the larger eccentricity of the vertical force"
            )
        e1, e2 = self._calc_e1_e2(e1, e2, verbose)

        k_local_crushing = round_half_up(1 - 2 * e1 / self.thickness, self.epsilon)
        crushing_comp_cap = round_half_up(
            basic_comp_cap
            * k_local_crushing
            * effective_length
            * self.thickness
            * 1e-3,
            self.epsilon,
        )
        if verbose:
            print("\nCrushing capacity:")
            print(f"  k (crushing): {k_local_crushing:.3f}")
            print(f"  crushing_compressive_capacity = {crushing_comp_cap} kN")

        sr_vertical, sr_horizontal = self._calc_refined_slenderness(
            refined_ah=refined_ah,
            refined_av=refined_av,
            kt=kt,
            dist_to_return=dist_to_return,
            verbose=verbose,
        )
        if verbose:
            print("Horizontal:")
        k_lateral_horz = self._calc_refined_k_lateral(
            e1=e1, e2=e2, sr=sr_horizontal, verbose=verbose
        )
        if k_lateral_horz > 0.2:
            k_lateral_horz = 0.2
            if verbose:
                print("k_lateral_horz limited to 0.2 by 7.3.4.3(a) requirement of Fd < 0.2Fd")

        if verbose:
            print("Vertical:")
        k_lateral_vert = self._calc_refined_k_lateral(
            e1=e1, e2=e2, sr=sr_vertical, verbose=verbose
        )

        k_lateral = max(k_lateral_horz,k_lateral_vert)

        buckling_comp_cap = round_half_up(
            basic_comp_cap * k_lateral * effective_length * self.thickness * 1e-3,
            self.epsilon,
        )
        if verbose:
            print("\nBuckling capacity:")
            print(f"  k (buckling): {k_lateral}")
            print(f"  Effective length: {effective_length:.1f} mm")
            print(f"  kFo = {buckling_comp_cap} kN")

        return {"Crushing": crushing_comp_cap, "Buckling": buckling_comp_cap}

    def concentrated_load(
        self,
        refined_av: float | None = None,
        refined_ah: float | None = None,
        kt: float | None = None,
        e1: float | None = None,
        e2: float | None = None,
        dist_to_return: float | None = None,
        dist_to_end: float | None = None,
        bearing_width: float | None = None,
        bearing_length: float | None = None,
        verbose: bool = True,
    ) -> dict:
        """Computes the refined compressive capacity of a masonry wall per AS3700 Cl 7.3.

        Parameters:
            refined_av (float): Coefficient for vertical restraint.
            refined_ah (float): Coefficient for horizontal restraint.
            kt (float): Coefficient for engaged piers.
            w_left, w_direct, w_right (float): Applied loads (kN) from left,
                        right and center based on applied slab loading.
                        May be overriden by setting e1, e2.
            e1, e2 (float): End eccentricities (mm).
            dist_to_return (float): Distance to return wall (mm).
            effective_length (float): Length of wall used in calculations (mm).
            verbose (bool): Whether to print outputs.

        Returns:
            dict: {
                "Crushing",
                "Buckling",
                "Bearing"
            }
        """

        basic_comp_cap = self.basic_compressive_capacity(verbose=False)

        effective_length = self._calc_effective_compression_length(
            bearing_length=bearing_length, dist_to_end=dist_to_end, verbose=verbose
        )
        capacity = self.refined_compression(
            refined_av=refined_av,
            refined_ah=refined_ah,
            kt=kt,
            e1=e1,
            e2=e2,
            dist_to_return=dist_to_return,
            effective_length=effective_length,
            verbose=verbose,
        )

        kb = self._calc_kb(
            a1=dist_to_end,
            bearing_area=bearing_length * bearing_width,
            effective_length=effective_length,
            verbose=verbose,
        )
        bearing_comp_cap = kb * basic_comp_cap * bearing_length * bearing_width * 1e-3
        if verbose:
            print(f"kbFo: {bearing_comp_cap} KN")

        capacity["Bearing"] = bearing_comp_cap

        return capacity

    def _calc_effective_compression_length(
        self,
        bearing_length: float | None = None,
        dist_to_end: float | None = None,
        verbose: bool = True,
    ) -> float:
        if bearing_length is None:
            raise ValueError("bearing_length not set")

        if dist_to_end is None:
            raise ValueError(
                "dist_to_end not set. This is defined as the shortest distance "
                "from the edge of the bearing area to "
                "the edge of the wall, refer AS3700 Cl 7.3.5.4."
            )

        effective_length = min(
            self.length,
            min(dist_to_end, self.height / 2)
            + bearing_length
            + min(self.height / 2, self.length - dist_to_end - bearing_length),
        )
        if verbose:
            print(f"effective wall length: {effective_length} mm")

        return effective_length

    def _calc_kb(
        self,
        a1: float | None = None,
        bearing_area: float | None = None,
        effective_length: float | None = None,
        verbose: bool = True,
    ) -> float:
        """Calculates kb in accordance with AS3700:2018 Cl 7.3.5.4"""
        if self.bedding_type is None:
            raise ValueError(
                "bedding_type not set. set to True for Full bedding or False for Face shell bedding"
            )
        elif self.bedding_type is False and self.mortar_class != 3:
            raise ValueError(
                "Face shell bedding_type is only available for mortar class M3. "
                "Change bedding_type or mortar_class"
            )
        elif verbose:
            print(
                f"bedding_type: {"Full" if self.bedding_type is True else "Face shell"}"
            )

        if bearing_area is None:
            raise ValueError(
                "bearing_area not set. This is the bearing area of the concentrated load."
            )
        dispersed_area = effective_length * self.thickness

        if self.bedding_type:
            kb = (
                0.55
                * (1 + 0.5 * a1 / self.length)
                / ((bearing_area / dispersed_area) ** 0.33)
            )
            kb = min(kb, 1.5 + a1 / self.length)
            kb = round_half_up(max(kb, 1), self.epsilon)
        else:
            kb = 1
        if verbose:
            print(f"kb: {kb}")

        return kb

    def horizontal_shear(self, kv:float|None = None):
        if kv is None:
            raise ValueError("kv undefined, select kv from AS3700 T3.3")
        if self.fmt is None:
            raise ValueError(
                "fmt undefined, fms is calculated using fmt, set fmt = 0.2 under wind load, or 0 elsewhere, refer AS3700 Cl 3.3.3"
            )

        self.Ab = self.length * self.thickness
        self.V0 = self.phi_shear * self.fms_horizontal * self.Ab * 1e-3
        print(
            f"V0, the shear bond strength of section: {self.V0} KN. To be taken as 0 at interfaces with DPC/flashings etc."
        )
        self.V1 = self.kv * self.fd * self.Ab * 1e-3
        print(f"V1, the shear friction of the section: {self.V1} KN.")
        self.Vd = self.V0 + self.V1
        print(f"V0 + V1, combined shear strength: {self.Vd}")
        return self.Vd

    def _calc_e1_e2(
        self,
        e1: float | None = None,
        e2: float | None = None,
        verbose: bool = True,
    ) -> tuple[float, float]:
        if e1 < e2:
            raise ValueError("e1 set to a value less than e2")
        if e1 < 0:
            raise ValueError("e1 < 0. e1 should always be positive by defintion"
            "refer AS3700:2018 Cl 7.3.4.5. If e1 and e2 are opposite, e1 should be"
            "positive and e2 negative")

        if abs(e1) < 0.05 * self.thickness:
            e1 = 0.05 * self.thickness if e1 >= 0 else -0.05 * self.thickness
        if abs(e2) < 0.05 * self.thickness:
            e2 = 0.05 * self.thickness if e2 >= 0 else -0.05 * self.thickness
        if verbose:
            print(
                f"End eccentricity, e1: {e1} mm, e2: {e2} mm, refer AS3700 Cl 7.3.4.4"
            )
        return e1, e2

    def _calc_refined_slenderness(
        self,
        refined_av: float | None = None,
        refined_ah: float | None = None,
        kt: float | None = None,
        dist_to_return: float | None = None,
        verbose: bool | None = True,
    ) -> tuple[float, float]:
        if refined_av is None:
            raise ValueError(
                "refined_av undefined, refer AS 3700 Cl 7.3.4.3. \n"
                "0.75 for a wall laterally supported and partially rotationally"
                " restrained at both top and bottom\n"
                "0.85 for a wall laterally supported at top and bottom and "
                "partially rotationally restrained at one end\n"
                "1.0 for a wall laterally supported at both top and bottom\n"
                "1.5 for a wall laterally supported and partially rotationally"
                "restrained at the bottom and partially laterally supported at the top\n"
                "2.5 for freestanding walls"
            )
        if verbose:
            print(f"av: {refined_av}")

        if refined_ah is None:
            raise ValueError(
                "refined_ah undefined, refer AS3700 Cl 7.3.4.3."
                " 1.0 for a wall laterally supported along both vertical edges,"
                " 2.5 for one edge. If no vertical edges supported set as 0"
            )
        if verbose:
            print(f"ah: {refined_ah}")

        if kt is None:
            raise ValueError(
                "kt undefined, refer AS 3700 Cl 7.3.4.2, set to 1 if there are no engaged piers"
            )
        if verbose:
            print(f"kt: {kt}")

        if refined_ah != 0 and dist_to_return is None:
            raise ValueError(
                "dist_to_return undefined. "
                "For one edge restrained, this is the distance to the return wall. "
                "If both edges restrained, it is thedistance between return walls"
            )
        if dist_to_return is not None and verbose:
            print(
                f"distance to return wall or between lateral supports {dist_to_return} mm"
            )

        sr_vertical = round_half_up(
            (refined_av * self.height) / (kt * self.thickness), self.epsilon
        )
        if verbose:
            print(f"Sr (vertical): {sr_vertical}")

        sr_horizontal = float("inf")

        if refined_ah != 0:
            sr_horizontal = round_half_up(
                0.7
                / self.thickness
                * math.sqrt(refined_av * self.height * refined_ah * dist_to_return),
                self.epsilon,
            )
        if verbose:
            print(f"Sr (horizontal) = {sr_horizontal}")

        return sr_vertical, sr_horizontal

    def _calc_refined_k_lateral(
        self,
        e1: float | None = None,
        e2: float | None = None,
        sr: float | None = None,
        verbose=True,
    ) -> float:
        """Calculates k for lateral instability in accordance with AS3700 Cl 7.3.4.5(1)"""

        if sr == float("inf"):
            k_lateral = 0
        else:
            k_lateral = (
                0.5
                * (1 + e2 / e1)
                * (
                    (1 - 2.083 * e1 / self.thickness)
                    - (0.025 - 0.037 * e1 / self.thickness) * (1.33 * sr - 8)
                )
                + 0.5
                * (1 - 0.6 * e1 / self.thickness)
                * (1 - e2 / e1)
                * (1.18 - 0.03 * sr))
        
        k_lateral = round_half_up(max(k_lateral, 0),self.epsilon)
        if verbose:
            print(f"k for lateral instability: {k_lateral}")
        return k_lateral

    def horizontal_bending(self):
        if self.fmt < 0:
            raise ValueError(
                "fmt undefined, fms is calculated using fmt, set fmt = 0.2 under wind load, or 0 elsewhere, refer AS3700 Cl 3.3.3"
            )
        # Cl 4.4
        φ = 0.6
        # Cl 7.4.3.4
        kp = 1
        # Cl 7.4.3.2(2)
        Mch_1 = (
            2 * φ * kp * math.sqrt(self.fmt) * (1 + self.fd / self.fmt) * self.Zd_horz
        )
        # Cl 7.4.3.2(3)
        Mch_2 = 4 * φ * kp * math.sqrt(self.fmt) * self.Zd_horz
        # Cl 7.4.3.2(4)
        Mch_3 = φ * (0.44 * self.fut * self.Zu_horz + 0.56 * self.fmt * self.Zp_horz)
        Mch = min(Mch_1, Mch_2, Mch_3) * 10**-6
        print("Mch:", Mch, " KNm")
        return Mch

    def diagonal_bending(self, hu, tj, lu, tu, Ld, Mch):
        G = 2 * (hu + tj) / (lu + tj)
        Hd = 2900 / 2
        alpha = G * Ld / Hd
        print("alpha", alpha)
        af = alpha / (1 - 1 / (3 * alpha))
        k1 = 0
        k2 = 1 + 1 / G**2
        φ = 0.6
        ft = 2.25 * math.sqrt(self.fmt) + 0.15 * self.fd
        B = (hu + tj) / math.sqrt(1 + G**2)
        if B >= tu:
            Zt = ((2 * B**2 * tu**2) / (3 * B + 1.8 * tu)) / (
                (lu + tj) * math.sqrt(1 + G**2)
            )
        else:
            Zt = ((2 * B**2 * tu**2) / (3 * tu + 1.8 * B)) / (
                (lu + tj) * math.sqrt(1 + G**2)
            )
        Mcd = φ * ft * Zt
        print(Mcd)
        # Cl 7.4.4.2
        w = (2 * af) / (Ld**2) * (k1 * Mch + k2 * Mcd)
        print(w)

    def vertical_bending(self):
        if self.fmt < 0:
            raise ValueError(
                "fmt undefined, fms is calculated using fmt, set fmt = 0.2 under wind load, or 0 elsewhere, refer AS3700 Cl 3.3.3"
            )

        if self.fmt > 0:
            Mcv = min(
                self.phi_bending * self.fmt * self.Zd * 1e-6
                + min(self.fd, 0.36) * self.Zd * 1e-6,
                3 * self.phi_bending * self.fmt * self.Zd * 1e-6,
            )
        else:
            Mcv = self.fd * self.Zd * 1e-6
        print(f"Mcv = {Mcv} for length of {self.length}")
        print(f"Mcv per m = {Mcv/self.length*1e3}")
        return Mcv

    def self_weight(self) -> float:
        """Returns the seld weight of the masonry, exlcuding any applied actions such as Fd."""
        return self.density * self.length * self.height * self.thickness

    def _calc_km(self, verbose: bool = True) -> float:
        if self.fuc is None:
            raise ValueError(
                "fuc undefined, for new structures the value is typically 20 MPa,"
                " and for existing 10 to 12MPa"
            )
        if self.bedding_type is None:
            raise ValueError(
                "bedding_type not set. set to True for Full bedding or False for Face shell bedding"
            )
        elif self.bedding_type is False and self.mortar_class != 3:
            raise ValueError(
                "Face shell bedding_type is only available for mortar class M3."
                " Change bedding_type or mortar_class"
            )
        elif verbose:
            print(
                f"bedding_type: {"Full" if self.bedding_type is True else "Face shell"}"
            )

        if self.mortar_class is None:
            raise ValueError("mortar_class undefined, typically 3")

        if self.bedding_type is False:
            km = 1.6
        elif self.mortar_class == 4:
            km = 2
        elif self.mortar_class == 3:
            km = 1.4
        elif self.mortar_class == 2:
            km = 1.1
        else:
            raise ValueError("Invalid mortar class provided")
        return km

    def _calc_fm(self, km: float | None = None, verbose: bool = True):
        """Computes fm in accordance with AS3700 Cl 3."""

        if km is None:
            raise ValueError("km not set.")
        elif verbose:
            print(f"km: {km}")
        if self.hu is not None and self.tj is None:
            raise ValueError(
                "Masonry unit height provided but mortar thickness tj not provided"
            )
        elif self.hu is None and self.tj is not None:
            raise ValueError(
                "joint thickness tj provided but masonry unit height not provided"
            )

        kh = round_half_up(min(1.3 * (self.hu / (19 * self.tj)) ** 0.29, 1.3), self.epsilon)
        if verbose:
            print(
                f"kh: {kh}, based on a masonry unit height of {self.hu} mm"
                " and a joint thickness of {self.tj} mm"
            )

        fmb = round_half_up(math.sqrt(self.fuc) * km, self.epsilon)
        if verbose:
            print(f"fmb: {fmb} MPa")

        self.fm = round_half_up(kh * fmb, self.epsilon)
        if verbose:
            print(f"fm: {self.fm} MPa")
