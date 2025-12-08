# pylint: disable=too-many-lines
"""
This module performs engineering calculations in accordance with
AS3700:2018 for unreinforced masonry
"""

import math
from abc import ABC, abstractmethod
from structures.Masonry import masonry
from structures.util import round_half_up


# pylint: disable=too-many-instance-attributes
class _Unreinforced(ABC):
    """Abstract Base Class For the design of unreinforced masonry in accordance with AS3700:2018"""

    @abstractmethod
    def __init__(
        self,
        length: float,
        height: float,
        thickness: float,
        fuc: float,
        mortar_class: int,
        bedding_type: bool,
        verbose: bool = True,
        hu: float = 76,
        tj: float = 10,
        face_shell_thickness: float = 30,
        raking: float = 0,
        fmt: float = 0.2,
    ):

        self.length = length
        self.height = height
        self.thickness = thickness
        self.fuc = fuc
        self.mortar_class = mortar_class
        self.bedding_type = bedding_type
        self.hu = hu
        self.tj = tj
        self.fm = None
        self.fmt = fmt
        self.verbose = verbose
        self.fut = 0.8
        self.phi_shear = 0.6
        self.phi_bending = 0.6
        self.phi_compression = 0.75
        self.density = 19
        self.epsilon = 2
        self.grouted = False
        self.face_shell_thickness = face_shell_thickness
        self.raking = raking
        self.fcg = 1
        self.__post_init__()

    def __post_init__(self):

        if self.verbose:
            print(f"length: {self.length} mm")
            print(f"height: {self.height} mm")
            print(f"thickness: {self.thickness} mm")
            print(
                f"bedding_type: {'Full bedding' if
                                    self.bedding_type is True else 'Face shell bedding'}"
            )
            print(f"mortar class: M{self.mortar_class}")
            print(f"fuc: {self.fuc} MPa")
            print(f"fmt: {self.fmt} MPa")
            print(f"Joint thickness tj: {self.tj} mm")
            print(f"Masonry unit height hu: {self.hu} mm")

            km = self._calc_km(verbose=self.verbose)
            masonry.calc_fm(self=self, km=km, verbose=self.verbose)

    def basic_compressive_capacity(self, verbose: bool = True) -> float:
        """Computes the Basic Compressive strength to AS3700 Cl 7.3.2(2)
        and returns the compressive capacity in KN. This does not account for
        wall geometry, including whether it is face-shell bedding.

        Parameters
        ----------
        verbose : bool
            True to print calculations

        Returns
        -------
            basic compressive capacity in KN


        >>> from structures.Masonry.unreinforced_masonry import Clay
        >>> wall = Clay()
        """
        km = self._calc_km(verbose=verbose)
        masonry.calc_fm(self=self, km=km, verbose=verbose)
        bedded_area = self._calc_ab()
        if verbose:
            print(f"bedded area Ab: {bedded_area} mm2")
        grouted_area = self._calc_ag(bedded_area)
        if verbose:
            print(f"grouted area Ag: {grouted_area} mm2")
        kc = self._calc_kc()
        basic_comp_cap = round_half_up(
            self.phi_compression
            * (
                self.fm * bedded_area
                + kc * (self.fcg / 1.3) ** (0.55 + 0.005 * self.fcg) * grouted_area
            )
            * 1e-3,
            self.epsilon,
        )
        if verbose:
            print(f"phi_compression: {self.phi_compression}")
            print(
                f"basic_compressive_capacity = {basic_comp_cap} KN \
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
        Computes the compression capacity of a masonry wall using the simplified method in AS3700.

        Parameters
        ==========

        simple_av : float
            Vertical slenderness coefficient\n
            1 if the member is laterally supported along its top edge\n
            2.5 if the member is not laterally supported along its top edge

        kt : float
            a thickness coefficient derived from Table 7.2\n
            1 - if there are no engaged piers\n
            If the engagement of a pier to the wall does not meet the requirements of\n
            Clause 4.11 for bonding or tying, the value of kt shall be taken as 1.0.

        compression_load_type : int
            Type of compression loading:\n
            1 - concrete slab\n
            2 - other systems (see Table 7.1)\n
            3 - wall with load applied to the face (see Table 7.1)

        verbose : bool
            If True, print internal calculation details.

        Returns:
            A dictionary with crushing and buckling capacity in kN.

        Examples
        ========

        Description

        >>> from structures.unreinforced_masonry import Clay
        >>> wall = Clay()
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
        if srs < 0:
            raise ValueError(
                "Srs is negative, either decrease wall height or increase thickness"
            )
        if verbose:
            print("\nBuckling capacity:")
            print(f"Srs = {simple_av} * {self.height} / {kt} * {self.thickness} ")
            print(f"Srs = {srs:.2f} (Simplified slenderness ratio Cl 7.3.3.3)")

        if compression_load_type == 1:
            k = round_half_up(
                min(0.67 - 0.02 * (srs - 14), 0.67),
                self.epsilon,
            )
            if verbose:
                print("Load type: Concrete slab over")
                print(f"k = min(0.67 - 0.02 * ({srs:.2f} - 14), 0.67)")
        elif compression_load_type == 2:
            k = round_half_up(
                min(
                    0.67 - 0.025 * (srs - 10),
                    0.67,
                ),
                self.epsilon,
            )
            if verbose:
                print("Load type: Other systems (Table 7.1)")
                print(f"k = min(0.67 - 0.025 * ({srs:.2f} - 10), 0.67)")
        elif compression_load_type == 3:
            k = round_half_up(
                min(
                    0.067 - 0.002 * (srs - 14),
                    0.067,
                ),
                self.epsilon + 1,
            )
            if verbose:
                print("Load type: Load applied to face of wall (Table 7.1)")
                print(f"k = min(0.067 - 0.002 * ({srs} - 14), 0.067)")
        else:
            raise ValueError("compression_load_type not in [1,2,3]")

        simple_comp_cap = round_half_up(
            k * basic_comp_cap,
            self.epsilon,
        )
        if verbose:
            print(f"k = {k}")
            print(f"Simple compression capacity kFo: {simple_comp_cap}")

        return {"Simple": simple_comp_cap}

    def refined_compression(
        self,
        refined_av: float,
        refined_ah: float,
        kt: float,
        e1: float,
        e2: float,
        dist_to_return: float | None = None,
        effective_length: float | None = None,
        verbose: bool = True,
    ) -> dict:
        """Computes the refined compressive capacity of a masonry wall per AS3700 Cl 7.3.

        Parameters
        ==========

        refined_av : float
            Vertical slenderness coefficient\n
            0.75 for a wall laterally supported and partially rotationally
            restrained at both top and bottom\n
            0.85 for a wall laterally supported at top and bottom and
            partially rotationally restrained at one end\n
            1.0 for a wall laterally supported at both top and bottom\n
            1.5 for a wall laterally supported and partially rotationally
            restrained at the bottom and partially laterally supported at the top\n
            2.5 for freestanding walls\n
            refer AS 3700 Cl 7.3.4.3.

        refined_ah : float
            Horizontal slenderness coefficient\n
            0 - for a wall with no lateral supports\n
            1 - for a wall laterally supported along both vertical edges (regardless of
            the rotational restraint along these edges)\n
            2.5 - for a wall laterally supported along one vertical edge, and
            unsupported along its other vertical edge\n
            Refer Figure 7.2 AS3700

         kt : float
            A thickness coefficient derived from Table 7.2\n
            1 - if there are no engaged piers\n
            If the engagement of a pier to the wall does not meet the requirements of\n
            Clause 4.11 for bonding or tying, the value of kt shall be taken as 1.0.\n

        e1 : float
            The larger eccentricity of the vertical force, at either top or bottom of the
            member in mm

        e2 : float
            The smaller eccentricity of the vertical force, at the other end of the member,
            not less than el, and negative when the eccentricities are on opposite sides of
            the member, given in mm

        dist_to_return : float
            Distance to return wall in mm. Note, this may be different from the length of
            the wall. For example, if only looking at a section of the wall, or a section
            which extends beyond.

        effective_length : float
            Length of wall used in calculations in mm

        verbose : bool
            Whether to print outputs.

        Returns:
            dict: {
                'Crushing': crushing_compressive_capacity,
                'Buckling': kFo,
            }

        Examples
        ========
        description

        >>> from ...
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
                "This is the eccentricity of the applied loads, where"
                "e1 is the larger eccentricity of the vertical force"
            )
        e1, e2 = self._calc_e1_e2(e1, e2, verbose)
        k_local_crushing = round_half_up(
            1 - 2 * e1 / self.thickness,
            self.epsilon,
        )
        crushing_comp_cap = round_half_up(
            basic_comp_cap * k_local_crushing * (effective_length / self.length),
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
            e1=e1,
            e2=e2,
            sr=sr_horizontal,
            verbose=verbose,
        )
        if k_lateral_horz > 0.2:
            k_lateral_horz = 0.2
            if verbose:
                print(
                    "k_lateral_horz limited to 0.2 by 7.3.4.3(a) requirement of Fd < 0.2Fd"
                )

        if verbose:
            print("Vertical:")
        k_lateral_vert = self._calc_refined_k_lateral(
            e1=e1,
            e2=e2,
            sr=sr_vertical,
            verbose=verbose,
        )

        k_lateral = max(k_lateral_horz, k_lateral_vert)

        buckling_comp_cap = round_half_up(
            basic_comp_cap * k_lateral * (effective_length / self.length),
            self.epsilon,
        )
        if verbose:
            print("\nBuckling capacity:")
            print(f"  k (buckling): {k_lateral}")
            print(f"  Effective length: {effective_length:.1f} mm")
            print(f"  kFo = {buckling_comp_cap} kN")

        return {
            "Crushing": crushing_comp_cap,
            "Buckling": buckling_comp_cap,
        }

    def concentrated_load(
        self,
        simple_av: float | None = None,
        kt: float | None = None,
        compression_load_type: int | None = None,
        dist_to_end: float | None = None,
        bearing_width: float | None = None,
        bearing_length: float | None = None,
        verbose: bool = True,
    ) -> dict:
        """Computes the simplified compression capacity
        of a masonry wall under concentrated loads

        Parameters
        ==========

        simple_av : float
            Vertical slenderness coefficient\n
            1 if the member is laterally supported along its top edge\n
            2.5 if the member is not laterally supported along its top edge

        kt : float
            a thickness coefficient derived from Table 7.2\n
            1 - if there are no engaged piers\n
            If the engagement of a pier to the wall does not meet the requirements of\n
            Clause 4.11 for bonding or tying, the value of kt shall be taken as 1.0.

        compression_load_type : int
            Type of compression loading:\n
            1 - concrete slab\n
            2 - other systems (see Table 7.1)\n
            3 - wall with load applied to the face (see Table 7.1)

        dist_to_end : float
            Defined as the shortest distance
            from the edge of the bearing area to
            the edge of the wall, refer AS3700 Cl 7.3.5.4.

        bearing_width : float
            Width of the bearing area in mm.

        bearing_length : float
            Length of the bearing area in mm.

        verbose : bool
            If True, print internal calculation details.

        Returns:
            A dictionary with crushing and buckling capacity in kN.

        Examples
        ========

        >>> from structures.unreinforced_masonry import Clay
        >>> wall = Clay()
        """
        if bearing_width is None:
            raise ValueError(
                "bearing_width not defined. Often this is the width of the wall."
            )
        if verbose:
            print(f"bearing width: {bearing_width} mm")
        print("WARNING: Test cases incomplete")
        basic_comp_cap = self.basic_compressive_capacity(verbose=False)

        effective_length = self._calc_effective_compression_length(
            bearing_length=bearing_length,
            dist_to_end=dist_to_end,
            verbose=verbose,
        )
        capacity = self.compression_capacity(
            simple_av=simple_av,
            kt=kt,
            compression_load_type=compression_load_type,
            verbose=verbose,
        )

        kb = self._calc_kb(
            a1=dist_to_end,
            bearing_area=bearing_length * bearing_width,
            effective_length=effective_length,
            verbose=verbose,
        )
        bearing_comp_cap = (
            kb
            * basic_comp_cap
            / (self.length * self.thickness)
            * bearing_length
            * bearing_width
            * 1e-3
        )
        if verbose:
            print(f"kbFo: {bearing_comp_cap} KN")

        capacity["Bearing"] = bearing_comp_cap

        return capacity

    def refined_concentrated_load(
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

        Parameters
        ==========

        refined_av : float
            Vertical slenderness coefficient\n
            0.75 for a wall laterally supported and partially rotationally
            restrained at both top and bottom\n
            0.85 for a wall laterally supported at top and bottom and
            partially rotationally restrained at one end\n
            1.0 for a wall laterally supported at both top and bottom\n
            1.5 for a wall laterally supported and partially rotationally
            restrained at the bottom and partially laterally supported at the top\n
            2.5 for freestanding walls\n
            refer AS 3700 Cl 7.3.4.3.

        refined_ah : float
            Horizontal slenderness coefficient\n
            1 - for a wall laterally supported along both vertical edges (regardless of
            the rotational restraint along these edges)\n
            2.5 - for a wall laterally supported along one vertical edge, and
            unsupported along its other vertical edge\n
            Refer Figure 7.2 AS3700

         kt : float
            A thickness coefficient derived from Table 7.2\n
            1 - if there are no engaged piers\n
            If the engagement of a pier to the wall does not meet the requirements of\n
            Clause 4.11 for bonding or tying, the value of kt shall be taken as 1.0.\n

        e1 : float
            The larger eccentricity of the vertical force, at either top or bottom of the
            member

        e2 : float
            The smaller eccentricity of the vertical force, at the other end of the member,
            not less than el, and negative when the eccentricities are on opposite sides of
            the member

        dist_to_return : float
            Distance to return wall (mm).

        effective_length : float
            Length of wall used in calculations (mm).

        dist_to_end : float
            Defined as the shortest distance
            from the edge of the bearing area to
            the edge of the wall, refer AS3700 Cl 7.3.5.4.

        bearing_width : float
            Width of the bearing area in mm.

        bearing _length : float
            Length of the bearing area in mm.

        verbose : bool
            If True, print internal calculation details.

        Returns:
            dict: {
                "Crushing",
                "Buckling",
                "Bearing"
            }

        Examples
        ========

        Description

        >>> from ..
        """
        print("WARNING: Test cases incomplete")
        basic_comp_cap = self.basic_compressive_capacity(verbose=False)

        effective_length = self._calc_effective_compression_length(
            bearing_length=bearing_length,
            dist_to_end=dist_to_end,
            verbose=verbose,
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
        bearing_comp_cap = (
            kb
            * basic_comp_cap
            / (self.length * self.thickness)
            * bearing_length
            * bearing_width
            * 1e-3
        )
        if verbose:
            print(f"kbFo: {bearing_comp_cap} KN")

        capacity["Bearing"] = bearing_comp_cap

        return capacity

    def vertical_bending(
        self,
        fd: float | None = None,
        interface: None | bool = None,
        verbose: bool = True,
    ) -> float:
        """Computes the vertical bending capacity in accordance with AS 3700 Cl 7.4.2

        Parameters
        ==========

        fd : float
            the minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        interface : bool
            True if shear plane is masonry to masonry,
            and False if shear_plane is masonry to other material

        verbose : bool
            Whether to print outputs

        Returns: float

        Examples
        ========

        Description

        >>> from ...
        """
        if fd is None:
            raise ValueError(
                "fd undefined. This is the minimum design compressive stress on the bed joint\n"
                "at the cross section under consideration, in MPa"
            )
        if verbose:
            print(f"fd: {fd} MPa")
        fmt = self._calc_fmt(interface=interface, verbose=verbose)

        zd_vert = round_half_up(
            self.length * self.thickness**2 / 6,
            self.epsilon,
        )
        if verbose:
            print(f"Zd (horizontal plane): {zd_vert} mm3")

        if fmt > 0:
            m_cv_1 = self.phi_bending * fmt * zd_vert + min(fd, 0.36) * zd_vert
            m_cv_2 = 3 * self.phi_bending * fmt * zd_vert
            m_cv = min(m_cv_1, m_cv_2)
            if verbose:
                print(
                    f"Mcv = {self.phi_bending} * {fmt} *"
                    f"{zd_vert} + {min(fd,0.36)} = "
                    f"{round_half_up(m_cv_1* 1e-6,self.epsilon)} KNm (7.4.2(2))"
                )
                print(
                    f"Mcv = 3 * {self.phi_bending} * {fmt} *"
                    f" {zd_vert} = {round_half_up(m_cv_2* 1e-6,self.epsilon)} KNm (7.4.2(3))"
                )
        else:
            m_cv = fd * zd_vert
            if verbose:
                print(
                    f"Mcv = fd Zd = {min(fd,0.36)} * {zd_vert} = {m_cv*1e-6} KNm (7.4.2(4))"
                )
        m_cv = round_half_up(m_cv * 1e-6, self.epsilon)
        if verbose:
            print("\nVertical bending capacity:")
            print(f"Mcv = {m_cv} KNm for length of {self.length} mm")
            print(f"Mcv = {m_cv/self.length*1e3} KNm/m")
        return m_cv

    def horizontal_bending(
        self,
        fd: float | None = None,
        interface: None | bool = None,
        verbose: bool = True,
    ) -> float:
        """Computes the horizontal bending capacity in accordance with AS3700 Cl 7.4.3.2

        Parameters
        ==========

        fd : float
            the minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        interface : bool
            True if shear plane is masonry to masonry,
            and False if shear_plane is masonry to other material

        verbose : bool
            Whether to print outputs

        Returns: float

        Examples
        ========

        Description

        >>> from ..."""
        if self.fmt is None:
            raise ValueError(
                "self.fmt undefined.\n"
                " set fmt = 0.2 under wind load, or 0 elsewhere, refer AS3700 Cl 3.3.3"
            )
        if verbose:
            print(f"fmt: {self.fmt} MPa")

        if fd is None:
            raise ValueError(
                "fd undefined. This is the minimum design compressive stress on the bed joint\n"
                "at the cross section under consideration, in MPa"
            )
        if verbose:
            print(f"fd: {fd} MPa")

        kp = self._calc_kp(verbose=verbose)

        self._calc_fmt(interface=interface, verbose=verbose)

        zd_horz = round_half_up(
            self.height * self.thickness**2 / 6,
            self.epsilon,
        )
        if verbose:
            print(f"Zd (horizontal): {zd_horz} mm3")

        zu_horz = zd_horz
        if verbose:
            print(
                f"Zu (horizontal): {zu_horz} mm3, assumed full perpends with no raking"
            )

        zp_horz = zd_horz
        if verbose:
            print(
                f"Zp (horizontal): {zp_horz} mm3, assumed full perpends with no raking"
            )

        mch_1 = (
            2
            * self.phi_shear
            * kp
            * math.sqrt(self.fmt)
            * (1 + fd / self.fmt)
            * zd_horz
        ) * 10**-6
        if verbose:
            print(f"Mch_1: {mch_1:.2f} KNm Cl 7.4.3.2(2)")

        mch_2 = 4 * self.phi_shear * kp * math.sqrt(self.fmt) * zd_horz * 10**-6
        if verbose:
            print(f"Mch_2: {mch_2:.2f} KNm Cl 7.4.3.2(3)")

        mch_3 = (
            self.phi_shear
            * (0.44 * self.fut * zu_horz + 0.56 * self.fmt * zp_horz)
            * 10**-6
        )
        if verbose:
            print(f"Mch_3: {mch_3:.2f} KNm  # Cl 7.4.3.2(4)")
        mch = round_half_up(min(mch_1, mch_2, mch_3), self.epsilon)
        if verbose:
            print("\nHorizontal bending capacity:")
            print(f"Mch: {mch} KNm for height of {self.height} mm")
            print(f"Mch: {mch/self.height*1e3:.2f} KNm/m")
        return mch

    def horizontal_plane_shear(
        self,
        kv: float,
        interface: float,
        fd: float,
        verbose: bool = True,
    ) -> dict:
        """Calculates the  horizontal shear capacity in accordance with AS3700:2018 Cl 7.5.4.1

        Parameters
        ==========

        kv : float
            shear factor (see AS3700 T3.3). At mortar bed joints or interfaces with concrete = 0.3\n
            At interfaces with steel = 0.2\n
            At slip joints comprising two layers of membrane-type DPC material = 0.1\n
            For other locations see AS3700 T3.3 or assume 0.

        interface : bool
            True if shear plane is masonry to masonry,
            and False if shear_plane is masonry to other material

        fd : float
            the minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        verbose : bool
            Whether to print outputs

        Returns: float

        Examples
        ========

        Description

        >>> from ..."""
        if kv > 0.3:
            raise ValueError("kv > 0.3 is outside the scope of AS3700")
        if verbose:
            print(f"kv: {kv} (AS3700 T3.3)")
        fmt = self._calc_fmt(interface=interface, verbose=verbose)

        bedding_area = self.length * self.thickness
        fms_horizontal = self._calc_fms_horz(fmt=fmt, verbose=verbose)

        v0 = round_half_up(
            self.phi_shear * fms_horizontal * bedding_area * 1e-3, self.epsilon
        )
        if verbose:
            print("\nV0: phi_shear * fms_horizontal * bedding_area")
            print(f"V0: {self.phi_shear} * {fms_horizontal} * {bedding_area * 1e-3}")
            print(f"V0: {v0} KN (bond strength)")
        if verbose:
            print(f"fd: {fd} MPa")
        if fd > 2:
            fd = 2
            if verbose:
                print("fd limited to 2 MPa")
        v1 = round_half_up(kv * fd * bedding_area * 1e-3, self.epsilon)
        if verbose:
            print("\nV1: kv * fd * bedding_area")
            print(f"V1: {kv} * {fd} * {bedding_area * 1e-3}")
            print(f"V1: {v1} KN (shear friction)")
        vd = v0 + v1
        if verbose:
            print(f"V0 + V1: {vd} KN")
            print(f"V0 + V1: {vd/self.length*1e3:.2f} KN/m")
        return {"bond": v0, "friction": v1}

    def vertical_plane_shear(self, verbose: bool = True) -> float:
        """Computes the horizontal shear capacity in accordance with AS3700 Cl 7.5.4.2"""
        print("WARNING: Test cases incomplete")
        fms_vertical = self._calc_fms_vert(verbose=verbose)
        vertical_shear_cap = (
            self.phi_shear * fms_vertical * self.thickness * self.length
        )
        if verbose:
            print(f"Vertical shear capacity: {vertical_shear_cap} KN")
        return vertical_shear_cap

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
            + min(
                self.height / 2,
                self.length - dist_to_end - bearing_length,
            ),
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

        if self.bedding_type is False and self.mortar_class != 3:
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
        if verbose:
            print(f"dispersed area = {dispersed_area} mm2")
        if self.bedding_type:
            kb = (
                0.55
                * (1 + 0.5 * a1 / self.length)
                / ((bearing_area / dispersed_area) ** 0.33)
            )
            kb = min(kb, 1.5 + a1 / self.length)
            kb = round_half_up(max(kb, 1), self.epsilon)
            if verbose:
                print(
                    "kb = 0.55 * (1 + 0.5 * a1 / length) / "
                    "((bearing_area / dispersed_area) ** 0.33)"
                )
                print(
                    f"kb = 0.55 * (1 + 0.5 * {a1} / {self.length}) / "
                    "(({bearing_area} / {dispersed_area}) ** 0.33)"
                )
        else:
            kb = 1
        if verbose:
            print(f"kb: {kb}")

        return kb

    def _calc_e1_e2(
        self,
        e1: float | None = None,
        e2: float | None = None,
        verbose: bool = True,
    ) -> tuple[float, float]:
        if e1 < e2:
            raise ValueError("e1 set to a value less than e2")
        if e1 < 0:
            raise ValueError(
                "e1 < 0. e1 should always be positive by defintion"
                "refer AS3700:2018 Cl 7.3.4.5. If e1 and e2 are opposite, e1 should be"
                "positive and e2 negative"
            )

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
                "refined_ah undefined, refer AS3700 Cl 7.3.4.3.\n"
                " 1.0 for a wall laterally supported along both vertical edges,\n"
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
            (refined_av * self.height) / (kt * self.thickness),
            self.epsilon,
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
            k_lateral = 0.5 * (1 + e2 / e1) * (
                (1 - 2.083 * e1 / self.thickness)
                - (0.025 - 0.037 * e1 / self.thickness) * (1.33 * sr - 8)
            ) + 0.5 * (1 - 0.6 * e1 / self.thickness) * (1 - e2 / e1) * (
                1.18 - 0.03 * sr
            )
        print(
            f"k for lateral instability = 0.5 * (1 + {e2} / {e1}) * ( "
            f" (1 - 2.083 * {e1} / {self.thickness}) "
            f" - (0.025 - 0.037 * {e1} / {self.thickness}) * (1.33 * {sr} - 8) "
            f") + 0.5 * (1 - 0.6 * {e1} / {self.thickness}) * (1 - {e2} / {e1}) * ("
            f"   1.18 - 0.03 * {sr}"
            " )"
        )
        k_lateral = round_half_up(max(k_lateral, 0), self.epsilon)
        if verbose:
            print(f"k for lateral instability: {k_lateral}")
        return k_lateral

    def _calc_kp(self, verbose: bool):
        kp = 1
        if verbose:
            print(f"kp: {kp} Cl 7.4.3.4")
        return kp

    def _diagonal_bending(self, hu, fd, tj, lu, tu, Ld, Mch) -> float:
        """Computes the two bending capacity in accordance with AS3700 Cl 7.4.4"""
        G = 2 * (hu + tj) / (lu + tj)
        Hd = 2900 / 2
        alpha = G * Ld / Hd
        print("alpha", alpha)
        af = alpha / (1 - 1 / (3 * alpha))
        k1 = 0
        k2 = 1 + 1 / G**2
        φ = 0.6
        ft = 2.25 * math.sqrt(self.fmt) + 0.15 * fd
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

    def _self_weight(self) -> float:
        """Returns the seld weight of the masonry, exlcuding any applied actions such as Fd."""
        return self.density * self.length * self.height * self.thickness

    @abstractmethod
    def _calc_km(self, verbose: bool = True) -> float:
        pass

    def _calc_fms_horz(self, fmt: float, verbose: bool = True) -> float:
        fms_horizontal = max(0.15, min(1.25 * fmt, 0.35))
        if verbose:
            print(f"f'ms (horizontal): {fms_horizontal} MPa")
        return fms_horizontal

    def _calc_fms_vert(self, verbose: bool = True) -> float:
        fms_vertical = max(0.15, min(1.25 * self.fm, 0.35))
        if verbose:
            print(f"f'ms (vertical): {fms_vertical} MPa")
        return fms_vertical

    def _calc_fmt(
        self,
        interface: None | bool = None,
        verbose: bool = True,
    ) -> None:
        """Computes fmt in accordance with AS3700 Cl 3.3.3"""
        # 0.2 for clay masonry
        if interface is None:
            raise ValueError(
                "interface not set, set to True if shear plane is masonry to masonry,"
                " and False if shear_plane is masonry to other material"
            )
        if interface is False:
            fmt = 0
        elif interface is True:
            fmt = self.fmt
        else:
            raise ValueError("interface not bool")
        if verbose:
            print(
                f"fmt = {fmt} MPa (at interface with "
                f"{"masonry" if interface else "other materials"})"
            )
        return fmt

    def _calc_ab(self):
        # Fully grouted
        if self.bedding_type is True:
            bedded_area = self.length * (self.thickness - 2 * self.raking)
        elif self.bedding_type is False:
            bedded_area = 2 * self.length * (self.face_shell_thickness - self.raking)
        else:
            raise ValueError("bedding type not bool")
        return bedded_area

    def _calc_ag(self, bedded_area: float) -> float:
        if self.grouted:
            return self.length * (self.thickness - self.raking) - bedded_area
        else:
            return 0

    @abstractmethod
    def _calc_kc(self):
        return 1


class Clay(_Unreinforced):
    """Clay Masonry object

    Parameters
    ----------

        length : float
            length of the wall in mm

        height : float
            height of the wall in mm

        thickness : float
            thickness of the wall in mm

        fuc : float
            unconfined compressive capacity in MPa,
            typically 20 MPa in new structures and 10-12 MPa for existing structures

        mortar_class : float
            Mortar class in accordance with AS3700

        bedding_type : bool
            True if fully grout bedding,
            False if face shell bedding

        verbose : float
            True to print internal calculations
            False otherwise

        hu : float
            masonry unit height in mm, defaults to 76 mm

        tj : float
            grout thickness between masonry units in mm, defaults to 10 mm

        fmt : float
            Characteristic flexural tensile strength of masonry in MPa, defaults to 0.2 MPa

    Examples
    --------

    >>> from structures.Masonry.unreinforced_masonry import Clay
    >>> wall = Clay(
                length=1000,
                height=3000,
                thickness=110,
                fuc=20,
                mortar_class=3,
                bedding_type=True
                )


    """

    def __init__(
        self,
        length: float,
        height: float,
        thickness: float,
        fuc: float,
        mortar_class: int,
        bedding_type: bool,
        verbose: bool = True,
        hu: float = 76,
        tj: float = 10,
        face_shell_thickness: float = 0,
        raking: float = 0,
        fmt: float = 0.2,
    ):

        self.length = length
        self.height = height
        self.thickness = thickness
        self.fuc = fuc
        self.mortar_class = mortar_class
        self.bedding_type = bedding_type
        self.hu = hu
        self.tj = tj
        self.fm = None
        self.fmt = fmt
        self.verbose = verbose
        self.fut = 0.8
        self.phi_shear = 0.6
        self.phi_bending = 0.6
        self.phi_compression = 0.75
        self.density = 19
        self.face_shell_thickness = face_shell_thickness
        self.raking = raking
        self.grouted = False
        self.fcg = 1
        self.epsilon = 2
        self.__post_init__()

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
        if self.bedding_type is False and self.mortar_class != 3:
            raise ValueError(
                "Face shell bedding_type is only available for mortar class M3."
                " Change bedding_type or mortar_class"
            )
        if verbose:
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

    def _calc_kc(self):
        return 1.2


class Concrete(_Unreinforced):
    """Concrete Masonry object

    Parameters
    ==========

    length : float
        length of the wall in mm

    height : float
        height of the wall in mm

    thickness : float
        thickness of the wall in mm

    fuc : float
        unconfined compressive capacity in MPa,
        typically 10 MPa for full bedding and 15 MPa for face shell bedding

    mortar_class : float
        Mortar class in accordance with AS3700, only 3 is defined for concrete masonry in AS3700

    bedding_type : bool
        True if fully grouted bedding,
        False if face shell bedding

    verbose : float
        True to print internal calculations
        False otherwise

    hu : float
        masonry unit height in mm, defaults to 200 mm

    tj : float
        grout thickness between masonry units in mm, defaults to 10 mm

    fmt : float
        Characteristic flexural tensile strength of masonry in MPa, defaults to 0.2 MPa

    Examples
    ========

    >>> from structures.Masonry.unreinforced_masonry import Concrete
    >>> wall = Concrete(
                length=1000,
                height=3000,
                thickness=110,
                fuc=20,
                mortar_class=3,
                bedding_type=True
                )


    """

    def __init__(
        self,
        length: float,
        height: float,
        thickness: float,
        fuc: float,
        mortar_class: int,
        bedding_type: bool,
        grouted: bool = False,
        verbose: bool = True,
        hu: float = 200,
        tj: float = 10,
        face_shell_thickness: float = 30,
        raking: float = 0,
        density: float = 25,
        fcg: float = 15,
        fmt: float = 0.2,
    ):

        self.length = length
        self.height = height
        self.thickness = thickness
        self.fuc = fuc
        self.mortar_class = mortar_class
        self.bedding_type = bedding_type
        self.hu = hu
        self.tj = tj
        self.fm = None
        self.fmt = fmt
        self.verbose = verbose
        self.fut = 0.8
        self.phi_shear = 0.6
        self.phi_bending = 0.6
        self.phi_compression = 0.6 if grouted else 0.5
        self.density = 19
        self.grouted = grouted
        self.face_shell_thickness = face_shell_thickness
        self.raking = raking
        self.density = density
        self.fcg = fcg
        self.epsilon = 2
        self.__post_init__()

    def _calc_km(self, verbose: bool = True) -> float:
        if self.bedding_type is None:
            raise ValueError(
                "bedding_type not set. set to True for Full bedding or False for Face shell bedding"
            )
        if self.bedding_type is False and self.mortar_class != 3:
            raise ValueError(
                "Face shell bedding_type is only available for mortar class M3."
                " Change bedding_type or mortar_class"
            )
        if verbose:
            print(
                f"bedding_type: {"Full" if self.bedding_type is True else "Face shell"}"
            )

        if self.bedding_type is False and self.mortar_class == 3:
            km = 1.6
        elif self.mortar_class == 3:
            km = 1.4
        else:
            raise ValueError("Invalid mortar class provided")
        return km

    def _calc_kc(self):
        if self.density > 20:
            return 1.4
        else:
            return 1.2
