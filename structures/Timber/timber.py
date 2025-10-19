"""
Module for calculating timber member capacities in accordance with AS1720.1
"""

import math
import sqlite3
import os
from typing import Callable
from pydantic.dataclasses import dataclass
from structures.util import round_half_up


db_path = os.path.join(os.path.dirname(__file__), "tables.db")


@dataclass
class Properties:
    """Stores properties of timber members. Retrieves values from database"""

    length: float
    depth: float
    breadth: float
    grade: str
    category: int | None = None
    phi_bending: float | None = None
    phi_shear: float | None = None
    phi_compression: float | None = None
    fb: float | None = None
    fs: float | None = None
    fc: float | None = None
    ft_hw: float | None = None
    ft_sw: float | None = None
    elastic_modulus: float | None = None
    rigidity_modulus: float | None = None
    pb: float | None = None
    pc: float | None = 1
    seasoned: bool | None = None
    epsilon: int = 2
    latitude: bool | None = None

    def __post_init__(self):
        self._set_section_properties(verbose=True)
        self._set_pb(verbose=True)
        self._set_phi()

    def _set_section_properties(self, verbose: bool = True) -> None:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM f_grade_properties WHERE grade = ?", (self.grade,)
        )
        row = cursor.fetchone()
        (
            _,
            self.fb,
            self.ft_hw,
            self.ft_sw,
            self.fs,
            self.fc,
            self.elastic_modulus,
            self.rigidity_modulus,
        ) = row
        if "LVL" in self.grade and self.depth > 95:
            self.fb *= (95 / self.depth) ** 0.154
            self.fb = round_half_up(self.fb, self.epsilon)
        if "LVL" in self.grade and self.depth > 300:
            self.fb *= (300 / self.depth) ** 0.167
            self.fb = round_half_up(self.fb, self.epsilon)
        if verbose:
            print(f"fb: {self.fb} MPa")
            print(f"ft: {self.ft_hw} MPa (hardwood)")
            print(f"ft: {self.ft_sw} MPa (softwood)")
            print(f"fs: {self.fs} MPa")
            print(f"fc: {self.fc} MPa")
            print(f"E:  {self.elastic_modulus} MPa")
            print(f"G:  {self.rigidity_modulus} MPa")
        conn.commit()
        conn.close()

    def _set_pb(self, verbose: bool = True) -> None:
        if "LVL" in self.grade:
            self.pb = round_half_up(
                14.71 * (self.elastic_modulus / self.fb) ** (-0.48) * 0.25 ** (-0.061),
                self.epsilon,
            )
        else:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT seasoned, unseasoned FROM table3_1 WHERE grade = ?",
                (self.grade,),
            )
            row = cursor.fetchone()
            self.pb = row[0] if self.seasoned is True else row[1]
            conn.commit()
            conn.close()
        if verbose:
            print(f"pb: {self.pb}")

    def _set_phi(self, verbose: bool = True) -> None:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT grade, category_1, category_2, category_3 FROM table2_1 WHERE grade = ?",
            (self.grade,),
        )
        row = cursor.fetchone()
        self.phi_bending = self.phi_shear = self.phi_compression = row[self.category]

        if verbose:
            print(f"phi_bending: {self.phi_bending}")
            print(f"phi_shear: {self.phi_shear}")
            print(f"phi_compression: {self.phi_compression}")
        conn.commit()
        conn.close()


@dataclass
class Beam(Properties):
    """Class for designing timber beams in accordance with AS1720.1

    seasoned: True if seasoned timber is used and false otherwise.
    latitude: True if located in coastal Queensland north of latitude 25 degrees south
                                 or 16 degrees south elsewhere, and False otherwise.
    """

    def major_axis_bending(
        self,
        moisture_content: float | None = None,
        ncom: int | None = None,
        nmem: int | None = None,
        spacing: float | None = None,
        span: float | None = None,
        restraint_location: int | None = None,
        lay: float | None = None,
        z: float | None = None,
        verbose=True,
    ) -> float:
        """Interface function which calls self._bending() configured for in-plane capacity"""
        assert self.depth is not None
        assert self.breadth is not None

        return self._bending(
            moisture_content=moisture_content,
            ncom=ncom,
            nmem=nmem,
            spacing=spacing,
            span=span,
            restraint_location=restraint_location,
            lay=lay,
            z=z,
            out_of_plane=self.depth < self.breadth,
            verbose=verbose,
        )

    def minor_axis_bending(
        self,
        moisture_content=None,
        ncom=None,
        nmem=None,
        spacing=None,
        span=None,
        restraint_location: int | None = None,
        lay: float | None = None,
        z: float | None = None,
        verbose=True,
    ) -> float:
        """Interface function which calls self._bending() configured for out-of-plane capacity"""

        assert self.depth is not None
        assert self.breadth is not None

        return self._bending(
            moisture_content=moisture_content,
            ncom=ncom,
            nmem=nmem,
            spacing=spacing,
            span=span,
            restraint_location=restraint_location,
            lay=lay,
            z=z,
            out_of_plane=self.depth > self.breadth,
            verbose=verbose,
        )

    def shear(
        self,
        moisture_content=None,
        verbose=None,
    ):
        """
        Computes the shear capacity of a timber element using the methods
        described in AS 1720 Cl 3.2.5

        Args:
            loads: List of applied loads in kN.
            moisture_content: precentage moisture content, given as whole numbers,
                                 e.g. for 15% set as 15.
            verbose: If True, print internal calculation details.

        Returns:
            A dictionary with bending capacities for different durations related to the factor k1
        """
        k4 = self._calc_k4(moisture_content=moisture_content, verbose=verbose)
        k6 = self._calc_k6(verbose=verbose)

        shear_plane_area = 2 / 3 * (self.breadth * self.depth)
        if verbose:
            print(f"As (shear plane area): {shear_plane_area} mm2")

        vd = self.phi_shear * k4 * k6 * self.fs * shear_plane_area
        if verbose is True:
            print(f"Vd = {vd} KN (Not including k1)")

        k1_shear_cap = {
            "k1 = 1": round_half_up(vd, self.epsilon),
            "5 seconds": round_half_up(vd, self.epsilon),
            "5 minutes": round_half_up(vd, self.epsilon),
            "5 hours": round_half_up(0.97 * vd, self.epsilon),
            "5 days": round_half_up(0.94 * vd, self.epsilon),
            "5 months": round_half_up(0.8 * vd, self.epsilon),
            "50+ years": round_half_up(0.57 * vd, self.epsilon),
        }
        if verbose is True:
            for key, value in k1_shear_cap.items():
                print(f"Md ({key}): {value} KNm")
        return k1_shear_cap

    def _bending(
        self,
        moisture_content: float | None = None,
        ncom: int | None = None,
        nmem: int | None = None,
        spacing: float | None = None,
        span: float | None = None,
        out_of_plane: bool | None = None,
        restraint_location: int | None = None,
        lay: float | None = None,
        z: float | None = None,
        verbose=True,
    ) -> dict:
        """
        Computes the bending capacity of a timber element using the methods
        described in AS 1720 Cl 3.2

        Args:
            loads: List of applied loads in kN.
            seasoned: True if seasoned timber is used and false otherwise.
            moisture_content: precentage moisture content, given as whole numbers,
                                 e.g. for 15% set as 15.
            latitude: True if located in coastal Queensland north of latitude 25
                         degrees south or 16 degrees south elsewhere, and False otherwise.
            verbose: If True, print internal calculation details.

        Returns:
            A dictionary with bending capacities for different durations related to the factor k1
        """
        k4 = self._calc_k4(moisture_content=moisture_content, verbose=verbose)
        k6 = self._calc_k6(verbose=verbose)
        k9 = self._calc_k9(
            ncom=ncom, nmem=nmem, spacing=spacing, span=span, verbose=verbose
        )
        k12 = self._calc_k12(
            restraint_location=restraint_location,
            lay=lay,
            out_of_plane=out_of_plane,
            verbose=verbose,
        )
        z = self._calc_z(out_of_plane=out_of_plane, verbose=verbose)
        print(f"phi_bending = {self.phi_bending}")
        moment_cap = self.phi_bending * k4 * k6 * k9 * k12 * self.fb * z * 1e-6
        k1_moment_cap = {
            "k1 = 1": round_half_up(moment_cap, self.epsilon),
            "5 seconds": round_half_up(moment_cap, self.epsilon),
            "5 minutes": round_half_up(moment_cap, self.epsilon),
            "5 hours": round_half_up(0.97 * moment_cap, self.epsilon),
            "5 days": round_half_up(0.94 * moment_cap, self.epsilon),
            "5 months": round_half_up(0.8 * moment_cap, self.epsilon),
            "50+ years": round_half_up(0.57 * moment_cap, self.epsilon),
        }
        if verbose is True:
            for key, value in k1_moment_cap.items():
                print(f"Md ({key}): {value} KNm")
        return k1_moment_cap

    def _calc_k4(self, moisture_content, verbose):
        """Computes k4 using AS1720.1-2010 Cl 2.4.2.2 & Cl 2.4.2.3"""
        if self.seasoned is None:
            raise ValueError(
                "seasoned not set, set to True if using seasoned timber, and False otherwise"
            )
        elif verbose:
            print(f"seasoned: {self.seasoned}")

        if moisture_content is None:
            raise ValueError(
                "moisture_content not set, set to 15 if inside and 25 if outside. "
                "Note: further investigation needed regarding moisture content values"
            )
        elif verbose:
            print(f"moisture_content: {moisture_content} %")

        least_dim = min(self.length, self.breadth, self.depth)
        if self.seasoned:
            if moisture_content > 15:
                k4 = max(1 - 0.3 * (moisture_content - 15) / 10, 0.7)
            else:
                k4 = 1
        else:
            if least_dim <= 38:
                k4 = 1.15
            elif least_dim < 50:
                k4 = 1.1
            elif least_dim < 75:
                k4 = 1.05
            else:
                k4 = 1
        if verbose:
            print(f"k4: {k4}, refer Table 2.5")
        return k4

    def _calc_k6(self, verbose):
        """Computes k6 using AS1720.1-2010 Cl 2.4.3"""

        if verbose:
            print(f"latitude: {self.latitude}")
        if self.latitude is True:
            k6 = 0.9
        else:
            k6 = 1
        if verbose:
            print(f"k6: {k6}, refer Cl 2.4.3")
        return k6

    def _calc_k9(self, ncom, nmem, spacing, span, verbose):
        """Computes k9 using AS1720.1-2010 Cl 2.4.5.3"""

        if ncom is None:
            raise ValueError(
                "ncom not set, this is the number of elements that"
                " are effectively fastened together to form a single group"
            )
        if verbose:
            print(f"ncom: {ncom}, number of members per group")

        if nmem is None:
            raise ValueError(
                "nmem not set, this is the number of members that"
                " are discretely spaced parallel to each other"
            )
        if verbose:
            print(f"nmem: {nmem}, number of groups of members")

        if nmem > 1 and spacing is None:
            raise ValueError(
                "nmem greater than 1 but spacing between groups not set. This should be in mm."
            )
        if verbose and nmem > 1 and not spacing is None:
            print(f"spacing: {spacing} mm")

        if nmem > 1 and span is None:
            raise ValueError(
                "nmem greater than 1 but span of members not set. This should be in mm."
            )
        if verbose and nmem > 1 and not span is None:
            print(f"span: {span} mm")

        if (nmem == 1 and ncom == 1) or "LVL" in self.grade:
            if verbose:
                print("k9: 1")
            return 1

        table_2_7 = [0, 1, 1.14, 1.2, 1.24, 1.26, 1.28, 1.3, 1.31, 1.32, 1.33]

        g31 = table_2_7[ncom if ncom < 10 else 10]
        if verbose:
            print(f"g31: {g31}")
        g32 = table_2_7[ncom * nmem if ncom * nmem < 10 else 10]
        if verbose:
            print(f"g32: {g32}")
        k9 = g31 + (g32 - g31) * (1 - 2 * spacing / span)
        k9 = max(k9, 1)
        if verbose:
            print(f"k9: {k9}")
        return k9

    def _calc_k12(
        self,
        restraint_location: int | None = None,
        lay: float | None = None,
        fly_brace_spacing: int | None = None,
        out_of_plane: bool | None = None,
        verbose: bool = True,
    ) -> float:
        """Computes k12 using AS1720.1-2010 Cl"""
        if self.pb is None:
            raise ValueError("pb not defined")
        elif verbose:
            print(f"pb: {self.pb}")

        if out_of_plane is None:
            raise ValueError("out_of_plane not set. Set to True if out of plane")
        if out_of_plane is True:
            return 1

        if restraint_location is None or restraint_location not in [1, 2, 3]:
            raise ValueError(
                "restraint_location not set or set incorrectly.\n"
                "set to 1 if restraints are to the compression edge\n"
                "set to 2 if restraints are to the tension edge\n"
                "set to 3 if restraints are to the tension edge and "
                "there is fly-bracing to the compression edge\n"
                "If unsure, setting to 2 is conservative"
            )
        if verbose:
            print(f"restraint_location: {restraint_location}")

        if lay is None:
            raise ValueError(
                "lay not set. This is the distance between restraints in mm.\n"
                "For continuous systems e.g. flooring, set to the nail spacing e.g 300mm\n"
                "For fly-bracing systems it is NOT the distance between fly-braces."
            )
        if verbose:
            print(f"lay: {lay} mm")

        if restraint_location == 3 and fly_brace_spacing is None:
            raise ValueError(
                "restraint_location set to 3 but fly-brace spacing has not been set."
                " This should be the number of members in the group"
                "[L,R), for example, if there are fly braces to every purlin,"
                " then fly_brace_spacing should be set to 1, if they alternate every 2nd purlin,"
                " it should be set to 2, etc."
            )
        elif verbose and restraint_location == 3 and not fly_brace_spacing is None:
            if fly_brace_spacing == 1:
                print("fly braces connected to every restraint")
            elif fly_brace_spacing > 1:
                print(f"fly bracing to every {fly_brace_spacing} restraints")

        cont_restrained = self._cont_restraint(lay=lay, verbose=verbose)
        s1 = self._calc_s1(
            restraint_location=restraint_location,
            lay=lay,
            fly_brace_spacing=fly_brace_spacing,
            cont_restrained=cont_restrained,
            verbose=verbose,
        )

        if self.pb * s1 <= 10:
            k12 = 1
        elif self.pb * s1 <= 20:
            k12 = 1.5 - 0.05 * self.pb * s1
        else:
            k12 = 200 / (self.pb * s1) ** 2
        k12 = round_half_up(k12, self.epsilon)
        if verbose:
            print(f"k12: {k12}")
        return k12

    def _calc_s1(
        self,
        restraint_location: int | None = None,
        lay: float | None = None,
        fly_brace_spacing: int | None = None,
        cont_restrained: bool = False,
        verbose: bool = True,
    ) -> float:
        """Calculates the beam slenderness s1"""
        s1 = float("inf")
        if cont_restrained is True:
            if restraint_location == 1:
                s1 = 0
            if restraint_location == 2:
                s1 = 2.25 * self.depth / self.breadth
            if restraint_location == 3:
                s1 = (1.5 * self.depth / self.breadth) / (
                    (math.pi * self.depth / fly_brace_spacing * lay) ** 2 + 0.4
                ) ** 0.5
        elif cont_restrained is False:
            if restraint_location == 1:
                s1 = 1.25 * self.depth / self.breadth * (lay / self.depth) ** 0.5
            if restraint_location in (2, 3):
                s1 = (self.depth / self.breadth) ** 1.35 * (lay / self.depth) ** 0.25
        s1 = round_half_up(s1, self.epsilon)
        if verbose:
            print(f"s1: {s1}")
        return s1

    def _calc_s2(self):
        pass

    def _cont_restraint(self, lay: float | None = None, verbose: bool = True):
        """Determines if the beam is continuously restrained"""
        cont_restrained = (
            lay / self.depth <= 64 * (self.breadth / (self.pb * self.depth)) ** 2
        )
        if verbose:
            print(f"Continuously restrained: {cont_restrained}")
        return cont_restrained

    def _calc_z(self, out_of_plane: bool | None = None, verbose: bool = True) -> float:
        if out_of_plane is None:
            raise ValueError("out_of_plane not set.")
        if out_of_plane is True:
            z = self.depth * self.breadth**2 / 6
        elif out_of_plane is False:
            z = self.breadth * self.depth**2 / 6
        else:
            raise ValueError("error in _calc_z")

        if verbose:
            print(f"z: {z} mm3")
        return z

    def _calc_k1(self, duration: int | None = None, verbose: bool = True):
        """Calculates k1 in accordance with AS1720.1-2010 Cl 2.4.1.1"""
        if duration is None or duration not in (1, 2, 3, 4, 5, 6):
            raise ValueError(
                "duration not set. This is the duration of loading for strength:\n"
                "1:     5 seconds\n"
                "2:     5 minutes\n"
                "3:     5 hours\n"
                "4:     5 days\n"
                "5:     5 months\n"
                "6:     50+ years"
            )
        if duration == 1:
            k1 = 1
            if verbose:
                print(f"k1: {k1}, duration of loading for strength: 5 seconds")
        elif duration == 2:
            k1 = 1
            if verbose:
                print(f"k1: {k1}, duration of loading for strength: 5 minutes")
        if duration == 3:
            k1 = 0.97
            if verbose:
                print(f"k1: {k1}, duration of loading for strength: 5 hours")
        if duration == 4:
            k1 = 0.94
            if verbose:
                print(f"k1: {k1}, duration of loading for strength: 5 days")
        if duration == 5:
            k1 = 0.8
            if verbose:
                print(f"k1: {k1}, duration of loading for strength: 5 months")
        if duration == 6:
            k1 = 0.57
            if verbose:
                print(f"k1: {k1}, duration of loading for strength: 50+ years")
        return k1

    def __post_init__(self):
        if self.length is None:
            raise ValueError(
                "length is not set. "
                "This is the length of beam being considered between supports in mm."
            )
        if self.depth is None:
            raise ValueError("depth is not set. This is the depth of the beam in mm.")
        if self.breadth is None:
            raise ValueError(
                "breadth is not set. This is the breadth of the beam in mm."
            )
        if self.category is None:
            raise ValueError(
                "self.category not set.\n"
                "Select 1 for houses in which failure is unlikely to affect an"
                " area greater than 25m2\n"
                "\t or secondary members in structures other than houses\n"
                "Select 2 for primary structural members in structues other than houses or\n"
                "\t elements in houses for which failure will affect an area > 25m2\n"
                "Select 3 for primary structural members in structures inteded to fulfull\n"
                "\t an essential service or post disaster function"
            )
        if self.latitude is None:
            raise ValueError(
                "latitude not set, set to True if located in coastal Queensland "
                "north of latitude 25 degrees south or 16 degrees south elsewhere,"
                " and False otherwise."
            )
        super().__post_init__()


class Column(Beam):
    """Class for designing timber columns in accordance with AS 1720.1"""

    def minor_axis_compression(self):
        pass

    def major_axis_compression(self):
        pass

    def compression(self):
        pass

    def _compression(
        self,
        moisture_content=None,
        slenderness: Callable | None = None,
        g13=None,
        la=None,
        out_of_plane=None,
        verbose=None,
    ):
        """
        Computes the compressive strength of a Timber column parallel
          to grain in accordance with AS1720.1 Cl 3.3.1

        Args:
            loads: List of applied loads in kN.
            seasoned: True if seasoned timber is used and false otherwise.
            moisture_content: precentage moisture content, given as whole numbers,
                                 e.g. for 15% set as 15.
            latitude: True if located in coastal Queensland north of latitude 25 degrees
                         south or 16 degrees south elsewhere, and False otherwise.
            verbose: If True, print internal calculation details.

        Returns:
            A dictionary with bending capacities for different durations related to the factor k1
        """
        k4 = self._calc_k4(moisture_content=moisture_content, verbose=verbose)
        k6 = self._calc_k6(verbose=verbose)
        k12 = self._calc_k12_compression(
            g13=g13,
            la=la,
            verbose=verbose,
        )
        Ac = self.breadth * self.depth
        Ndc = self.phi_compression * k4 * k6 * k12 * self.fc * Ac
        if verbose:
            print(f"Ndc: {Ndc} KNm")
        return Ndc

    def _calc_k12_compression(
        self,
        g13: float | None = None,
        la: float | None = None,
        verbose: bool = True,
    ):
        """Computes k12 using AS1720.1-2010 Cl 3.3.2.2"""
        if self.pc is None:
            raise ValueError("pc not defined")
        elif verbose:
            print(f"pc: {self.pc}")

        if g13 is None:
            raise ValueError(
                "g13 not set. This should be selected from table 3.2. and relates to the end restraint of the column."
                "Flat ends 0.7\n"
                "Restrained at both ends in position and direction 0.7\n"
                "Each end held by two bolts (substantially restrained) 0.75\n"
                "One end fixed in position and direction, the other restrained in position only 0.85\n"
                "Studs in light framing 0.9\n"
                "Restrained at both ends in position only 1.0\n"
                "Restrained at one end in position and direction and at the other end partially \n"
                "restrained in direction but not in position 1.5\n"
                "Restrained at one end in position and direction but not restrained in either \n"
                "position or direction at other end 2.0\n"
            )

        s = max(self._calc_s3(g13, la), self._calc_s4(g13, la))

        if self.pc * s <= 10:
            k12 = 1
        elif self.pc * s <= 20:
            k12 = 1.5 - 0.05 * self.pc * s
        else:
            k12 = 200 / (self.pc * s) ** 2
        if verbose:
            print(f"k12: {k12}")
        return k12

    def _calc_s3(
        self, g13: float | None = None, lax: float | None = None, verbose: bool = True
    ):
        if lax is None:
            raise ValueError("Lax not set. This is the distance between restraints...")
        if verbose:
            print(f"Lax: {lax} mm")

        s3 = min(lax / self.depth, g13 * self.length / self.depth)
        if verbose:
            print(f"S3: {s3}")
        return s3

    def _calc_s4(
        self, g13: float | None = None, lay: float | None = None, verbose: bool = True
    ):
        """Computes Column slenderness for compression buckling using AS1720.1 Cl 3.3.2.2"""
        if lay is None:
            raise ValueError("lay not set. This is the distance between restraints...")
        elif verbose:
            print(f"lay: {lay} mm")

        s4 = min(lay / self.breadth, g13 * self.length / self.breadth)
        if verbose:
            print(f"S4: {s4}")
        return s4
