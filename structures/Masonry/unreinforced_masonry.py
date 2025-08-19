import math
from dataclasses import dataclass
import structures.Masonry.masonry as masonry

@dataclass
class UnreinforcedMasonry(masonry.Masonry):
    length: float
    height: float
    thickness: float
    fmt: float = -1
    fd: float = 0
    fuc: float = -1
    fm: float = -1
    fmb: float = -1
    # Cl 3.2 - In absence of test data, fut not to exceed 0.8MPa
    fut: float = 0.8
    kv: float = -1  # T3.3 default for interface with DPC/flashing
    km: float = 1.4  # T3.1 default for
    hu: float = 76
    tj: float = 10
    tu: float = 110
    lu: float = 230
    Ld: float = 3000
    φ_shear: float = 0.6
    φ_bending: float = 0.6
    φ_compression: float = 0.75
    density: float = 19  # KN/m3
    ah: float = -1
    dist_to_return: float | None = None

    mortar_class: int = -1
    kh: float = 1
    hu: float | None = None
    tj: float | None = None

    def basic_compressive_capacity(self,verbose):
        """ Computes the Basic Compressive strength to AS3700 Cl 7.3.2(2)"""
        Fo = round(self.φ_compression * self.fmb,2)
        if verbose:
            print("Simplified Compression capacity")
            print("Fo = ", round(Fo, 2), "MPa", "(Basic Compressive Capacity Cl 7.3.2(2))")
        return Fo

    def horizontal_shear(self):
        if self.kv < 0:
            raise ValueError("kv undefined, select kv from AS3700 T3.3")
        if self.fmt < 0:
            raise ValueError(
                "fmt undefined, fms is calculated using fmt, set fmt = 0.2 under wind load, or 0 elsewhere, refer AS3700 Cl 3.3.3"
            )

        self.Ab = self.length * self.thickness
        self.V0 = self.φ_shear * self.fms_horizontal * self.Ab * 1e-3
        print(
            f"V0, the shear bond strength of section: {self.V0} KN. To be taken as 0 at interfaces with DPC/flashings etc."
        )
        self.V1 = self.kv * self.fd * self.Ab * 1e-3
        print(f"V1, the shear friction of the section: {self.V1} KN.")
        self.Vd = self.V0 + self.V1
        print(f"V0 + V1, combined shear strength: {self.Vd}")
        return self.Vd

    def compression_capacity(
        self, loads=[], simple_av=None, kt=None, Ab=None, compression_load_type=None, verbose=False
    ):
        """
        Computes the compression capacity of a masonry wall element using the simplified method,
        described in AS 3700.

        Args:
            loads: List of applied loads in kN.
            simple_av: Coefficient (1 or 2.5) based on lateral support.
            kt: Coefficient for engaged piers (1 if none).
            Ab: Bearing area in mm². If 0, full wall bearing is assumed.
            compression_load_type: Type of compression loading (1, 2, or 3).
            verbose: If True, print internal calculation details.

        Returns:
            A dictionary with crushing and buckling capacity in kN.
        """
        if compression_load_type not in [1, 2, 3]:
            raise ValueError(
                """compression_load_type undefined, refer AS 3700 Cl 7.3.3.3.
                              Options are  1: concrete slab, 2: other systems as defined in Table 7.1,
                              3: wall with load applied to the face as defined in Table 7.1"""
            )
        if simple_av == None:
            raise ValueError(
                "simple_av undefined, refer AS 3700 Cl 7.3.3.4, set to 1 if member is laterally supported along top edge, else 2.5"
            )
        if kt == None:
            raise ValueError(
                "kt undefined, refer AS 3700 Cl 7.3.4.2, set to 1 if there are no engaged piers"
            )
        if Ab == None:
            raise ValueError(
                "Bearing area Ab is not defined, refer AS 3700, set to 0 to use entire wall"
            )
        
        if Ab == 0:
            Ab = self.length * self.thickness
            kb = 1
            effective_length = self.length
            if verbose: print("Note: Assumed bearing area is entire length of wall\n")
        else:
            raise ValueError("Ab not implemented")

        Fo = self.basic_compressive_capacity(verbose)
        
        # Crushing capacity
        kbFo = kb * Fo * Ab * 1e-3
        if verbose:
            print("\nCrushing capacity:")
            print(f"kb: {kb}")
            print(f"Ab: {Ab} mm2")
            print(f"kbFo = {kbFo} KN (Load capacity under a concentrated load Cl 7.3.5.3)")

        # Wall slenderness
        Srs = (simple_av * self.height) / (kt * self.thickness)
        if verbose:
            print("\nBuckling capacity:")
            print(f"Srs = {Srs:.2f} (Simplified slenderness ratio Cl 7.3.3.3)")

        if compression_load_type == 1:
            k = min(0.67 - 0.02 * (Srs - 14), 0.67)
            if verbose: print("Load type: Concrete slab over")
        elif compression_load_type == 2:
            k = min(0.67 - 0.025 * (Srs - 10), 0.67)
            if verbose: print("Load type: Other systems (Table 7.1)")
        elif compression_load_type == 3:
            k = min(0.067 - 0.002 * (Srs - 14), 0.067)
            if verbose: print("Load type: Load applied to face of wall (Table 7.1)")

        # Buckling capacity
        kFo = k * Fo * effective_length * self.thickness * 1e-3
        if verbose:
            print(f"k: {k}")
            print(f"Effective length of wall: {effective_length} mm")
            print(f"Simple compression capacity kFo: {kFo:.2f}")

        for N in loads:
            if N > kbFo or N > kFo:
                print(f"FAIL: {N} KN > {kbFo} KN or {kFo} KN")
        return {"Crushing": kbFo, "Buckling": kFo}
    

    def calc_e1_e2(self, e1, e2, W_left, W_direct, W_right):
        if e1 and e2:
            return
        e1 = max(
            (-W_left * self.thickness / 6 + W_right * self.thickness / 6)
            / (W_left + W_direct + W_right),
            0.05 * self.thickness,
        )
        e2 = e1
        return e1, e2

    def refined_compression(
        self,
        loads=[],
        refined_av=None,
        refined_ah=None,
        kt=None,
        Ab=None,
        W_left=None,
        W_direct=None,
        W_right=None,
        e1=None,
        e2=None,
        dist_to_return=None,
        dist_to_bearing=None,
        bearing_length=None,
        verbose=True
    ):
        """Computes the refined compressive capacity of a masonry wall per AS3700 Cl 7.3.

    Parameters:
        loads (list): Axial loads (kN) to check against capacities.
        refined_av (float): Coefficient for vertical restraint.
        refined_ah (float): Coefficient for horizontal restraint.
        kt (float): Coefficient for engaged piers.
        Ab (float): Bearing area (mm²).
        W_left, W_direct, W_right (float): Applied loads (kN) from left, right and center based on applied slab loading. May be overriden by setting e1, e2.
        e1, e2 (float): End eccentricities (mm).
        dist_to_return (float): Distance to return wall (mm).
        dist_to_bearing (float): Distance from edge of bearing area to wall edge (mm).
        bearing_length (float): Length of bearing (mm). Use 0 to auto-compute.
        verbose (bool): Whether to print outputs.

    Returns:
        dict: {
            'Fo': φ * f'm,
            'Sr': refined slenderness ratio,
            'e1': end eccentricity e1,
            'e2': end eccentricity e2,
            'Crushing Capacity (kbFo)': kbFo,
            'Buckling Capacity (kFo)': kFo,
            'Results': {N: 'PASS'/'FAIL' for N in loads}
        }
    """
        
        if refined_av == None:
            raise ValueError(
                "refined_av undefined, refer AS 3700 Cl 7.3.4.3, \n0.75 for a wall laterally supported and partially rotationally restrained at both top and bottom"
                "0.85 for a wall laterally supported at top and bottom and partially rotationally restrained at one end\n"
                "1.0 for a wall laterally supported at both top and bottom\n"
                "1.5 for a wall laterally supported and partially rotationally restrained at the bottom and partially laterally supported at the top\n"
                "2.5 for freestanding walls"
            )
        if kt == None:
            raise ValueError(
                "kt undefined, refer AS 3700 Cl 7.3.4.2, set to 1 if there are no engaged piers"
            )
        if Ab == None:
            raise ValueError(
                "Bearing area Ab is not defined, refer AS 3700, set to 0 to use entire wall"
            )
        if (
            W_direct == None
            or W_left == None
            or W_right == None
        ) and (e1 == None and e2 == None):
            raise ValueError(
                "W_direct, W_left, W_right undefined, refer AS 3700 Cl 7.3.4.4. Where W_direct is load applied with eccentricity of 0"
                " W_left and W_right is load applied with eccentricity of 1/3 bearing area of the depth of the bearing area, assuming bearing is across the full "
                "thickness of the wall. Alternatively, provide values of e1 and e2"
            )
        elif not (e1 == None and e2 == None):
            raise ValueError("e1 or e2 defined but not the other")
        elif not (
            W_direct == None
            and W_left == None
            and W_right == None
        ) and not (e1 == None and e2 == None):
            raise ValueError(
                "W_direct/W_left/W_right and e1/e2 defined, use only one system"
            )
        if refined_ah == None:
            raise ValueError(
                "refined_ah undefined, refer AS3700 Cl 7.3.4.3, 1.0 for a wall laterally supported along both vertical edges, 2.5 for one edge. If no vertical edges supported set as 0"
            )
        elif refined_ah != 0 and dist_to_return == None:
            raise ValueError(
                "dist_to_return undefined, for one edge restrained, this is the distance to the return wall. If both edges restrained, it is the"
                " distance between return walls"
            )


        #Step 1: Handle bearing geometry
        if bearing_length == 0 and Ab == None:
            raise ValueError("bearing_length set to 0 but Ab not defined")
        elif bearing_length == 0:
            bearing_length = Ab / self.thickness

        if Ab == 0:
            Ab = self.length * self.thickness
            effective_length = self.length
        elif dist_to_bearing == None:
            raise ValueError(
                "Ab non-zero but dist_to_bearing has not been set. This is defined as the shortest distance from the edge of the bearing area to "
                "the edge of the wall, refer AS3700 Cl 7.3.5.4."
            )
        elif bearing_length == None:
            raise ValueError(
                "Ab non-zero but bearing_length has not been set. This is required to deterine the effective wall length. To calculate "
                "based on provided Ab and given wall thickness, enter 0"
            )
        else:
            effective_length = min(
                self.length,
                min(dist_to_bearing, self.height / 2)
                + bearing_length
                + min(self.height / 2, self.length - dist_to_bearing - bearing_length),
            )

        # Step 2: Basic compressive capacity
        Fo = self.basic_compressive_capacity(verbose)

        #Step 3: Slenderness ratio
        Sr_vertical = (refined_av * self.height) / (kt * self.thickness)
        Sr_horizontal = (
            0.7
            / self.thickness
            * math.sqrt(refined_av * self.height * refined_ah * dist_to_return)
            if refined_ah
            else float("inf")
        )
        Sr = min(Sr_vertical, Sr_horizontal)
        if verbose:
            print("Srs =", Sr, "(Refined slenderness ratio Cl 7.3.4.3)")

        e1, e2 = self.calc_e1_e2(e1, e2, W_left, W_direct, W_right)
        if verbose:
            print(f"End eccentricity, e1: {e1} mm, e2: {e2} mm, refer AS3700 Cl 7.3.4.4")

        # Step 5: Crushing capacity
        k_local_crushing = 1 - 2 * e1 / self.thickness
        kbFo = round(Fo * k_local_crushing * Ab * 1e-3, 2)
        if verbose:
            print("\nCrushing capacity:")
            print(f"  k (crushing): {k_local_crushing:.3f}")
            print(f"  kbFo = {kbFo} kN")

        # Step 6: Buckling capacity
        k_lateral = 0.5 * (1 + e2 / e1) * (
            (1 - 2.083 * e1 / self.thickness)
            - (0.025 - 0.037 * e1 / self.thickness) * (1.33 * Sr - 8)
        ) + 0.5 * (1 - 0.6 * e1 / self.thickness) * (1 - e2 / e1) * (1.18 - 0.03 * Sr)
        kFo = round(Fo * k_lateral * effective_length * self.thickness * 1e-3, 2)
        if verbose:
            print("\nBuckling capacity:")
            print(f"  k (buckling): {k_lateral:.3f}")
            print(f"  Effective length: {effective_length:.1f} mm")
            print(f"  kFo = {kFo} kN")

        # Step 7: Load checks
        for N in loads:
            if N > kbFo or N > kFo:
                print(f"FAIL: {N} KN > {kbFo} KN or {kFo} KN")
            else:
                print(f"PASS: {N} KN < {kbFo} KN and {kFo} KN")
        return {"Crushing": kbFo, "Buckling": kFo}

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

    def diagonal_bending(self,hu, tj, lu, tu, Ld, Mch):
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
                self.φ_bending * self.fmt * self.Zd * 1e-6
                + min(self.fd, 0.36) * self.Zd * 1e-6,
                3 * self.φ_bending * self.fmt * self.Zd * 1e-6,
            )
        else:
            Mcv = self.fd * self.Zd * 1e-6
        print(f"Mcv = {Mcv} for length of {self.length}")
        print(f"Mcv per m = {Mcv/self.length*1e3}")
        return Mcv

    def self_weight_masonry(self):
        return self.density * self.length * self.height * self.thickness



class ReinforcedMasonry(UnreinforcedMasonry):
    pass


if __name__ == "__main__":
    wall = UnreinforcedMasonry(
        length=3000, height=3 * 86 - 20, thickness=110, fmt=0.2, fuc=20, mortar_class=3
    )
    wall.horizontal_bending()
