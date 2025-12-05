"""
This module performs engineering calculations in accordance with
AS3700:2018 for reinforced masonry
"""

from structures.util import round_half_up
from structures.Masonry import masonry


class Block:
    """For the design of reinforced clay brick masonry in accordance with AS3700:2018"""

    def __init__(
        self,
        length: float,
        height: float,
        thickness: float,
        fuc: float,
        mortar_class: float,
        verbose: bool = True,
        hu: float = 200,
        tj: float = 10,
        lu: float = 400,
        fmt: float = 0.2,
    ):
        """Initialises the masonry element

        Parameters
        ==========

        length : float
            length of the wall in mm

        height : float
            height of the wall in mm

        thickness : float
            thickness of the masonry unit in mm

        fuc : float
            unconfined compressive capacity in MPa, AS3700 requires not less than 15 MPa

        mortar_class : float
            Mortar class in accordance with AS3700

        verbose : bool
            True to print internal calculations
            False otherwise

        hu : float
            masonry unit height in mm, defaults to 200 mm

        tj : float
            grout thickness between masonry units in mm, defaults to 10 mm

        lu : float
            length of the masonry unit in mm, defaults to 400 mm

        fmt : float
            Characteristic flexural tensile strength of masonry in MPa, defaults to 0.2 MPa

        Examples
        ========

        >>> from structures.Masonry.reinforced_masonry import ReinforcedBlock
        >>> wall = ReinforcedBlock(
                    length=1000,
                    height=3000,
                    thickness=110,
                    fuc=20,
                    mortar_class=3,
                    bedding_type=True
                    )


        """
        self.length = length
        self.height = height
        self.thickness = thickness
        self.fuc = fuc
        self.mortar_class = mortar_class
        self.hu = hu
        self.tj = tj
        self.lu = lu
        self.fmt = fmt
        self.verbose = verbose

        self.fm = 0
        self.phi_shear = 0.75
        self.phi_bending = 0.75
        self.phi_compression = 0.75
        self.fut = 0.8
        self.epsilon = 2

        if self.mortar_class != 3:
            raise ValueError(
                "Concrete masonry units undefined for mortar class M4, adopt M3"
            )
        if fuc < 15:
            print("Note: fuc less than minimum required by AS3700 of 15 MPa")
        self.zd = self.length * self.thickness**2 / 6
        self.zu = self.zp = self.zd
        self.zd_horz = self.height * self.thickness**2 / 6
        self.zu_horz = self.zp_horz = self.zd_horz

        km = self._calc_km(verbose=verbose)
        masonry.calc_fm(self=self, km=km, verbose=verbose)

    def _bending(
        self,
        d: float,
        b: float,
        area_tension_steel: float,
        fsy: float,
        verbose: bool = True,
    ):

        if verbose:
            print(f"fsy: {fsy:.2f} MPa")

        if verbose:
            print(f"d: {d:.2f} mm")

        if verbose:
            print(f"area_tension_steel: {area_tension_steel:.2f} mm2")

        if verbose:
            print(f"b: {b:.2f} mm")

        # Step 1: Calculate effective_area_tension_steel
        effective_area_tension_steel = min(
            area_tension_steel, (0.29 * 1.3 * self.fm * self.length * d) / fsy
        )
        if verbose is True:
            print(
                f"effective_area_tension_steel: {effective_area_tension_steel:.2f} mm2"
            )

        # Step 2: Calculate moment_cap
        moment_cap = round_half_up(
            self.phi_bending
            * fsy
            * effective_area_tension_steel
            * d
            * (
                1
                - (0.6 * fsy * effective_area_tension_steel)
                / (1.3 * self.fm * self.length * d)
            )
            * 1e-6,
            self.epsilon,
        )
        if verbose is True:
            print(f"moment_cap: {moment_cap:.2f} KNm")
        return moment_cap

    def out_of_plane_vertical_bending(
        self,
        d: float,
        area_tension_steel: float,
        fsy: float,
        verbose: bool = True,
    ):
        """
        Computes the bending capacity of a reinforced masonry wall element using the methods
        described in AS 3700 Cl 8.6.

        Parameters
        ==========

        d : float
            Effective depth of the reinforced masonry member from the extreme compressive
            fibre of the masonry to the resultant tensile force in the steel in the tensile
            zone in mm. Typical values are 95 for 190 block walls

        area_tension_steel : float
            Cross-sectional area of fully anchored longitudinal reinforcement in the tension
            zone of the cross-section under consideration in mm². Denoted as Ast in AS3700. Note:
            the amount of steel used in calculation is limited to effective_area_tension_steel

        fsy : float
            Design yield strength of reinforcement in MPa (refer Cl 3.6.1), typically 500 MPa

        verbose : bool
            True to print internal calculations
            False otherwise

        Examples
        ========

        >>> from ..
        """
        moment_cap = self._bending(
            fsy=fsy,
            d=d,
            area_tension_steel=area_tension_steel,
            b=self.length,
            verbose=verbose,
        )
        return moment_cap

    def out_of_plane_horizontal_bending(
        self,
        d: float,
        area_tension_steel: float,
        fsy: float,
        verbose: bool = True,
    ):
        """
        Computes the bending capacity of a reinforced masonry wall element using the methods
        described in AS 3700 Cl 8.6.

        Parameters
        ==========

        d : float
            Effective depth of the reinforced masonry member from the extreme compressive
            fibre of the masonry to the resultant tensile force in the steel in the tensile
            zone in mm. Typical values are 95 for 190 block walls

        area_tension_steel : float
            Cross-sectional area of fully anchored longitudinal reinforcement in the tension
            zone of the cross-section under consideration in mm². Denoted as Ast in AS3700. Note:
            the amount of steel used in calculation is limited to effective_area_tension_steel

        fsy : float
            Design yield strength of reinforcement in MPa (refer Cl 3.6.1), typically 500 MPa

        verbose : bool
            True to print internal calculations
            False otherwise

        Examples
        ========

        >>> from ..
        """
        moment_cap = self._bending(
            fsy=fsy,
            d=d,
            area_tension_steel=area_tension_steel,
            b=self.height,
            verbose=verbose,
        )
        return moment_cap

    def in_plane_vertical_bending(
        self,
        d: float,
        area_tension_steel: float,
        fsy: float,
        verbose: bool = True,
    ):
        """
        Computes the bending capacity of a reinforced masonry wall element using the methods
        described in AS 3700 Cl 8.6.

        Parameters
        ==========

        d : float
            Effective depth of the reinforced masonry member from the extreme compressive
            fibre of the masonry to the resultant tensile force in the steel in the tensile
            zone in mm. Typical values are 95 for 190 block walls

        area_tension_steel : float
            Cross-sectional area of fully anchored longitudinal reinforcement in the tension
            zone of the cross-section under consideration in mm². Denoted as Ast in AS3700. Note:
            the amount of steel used in calculation is limited to effective_area_tension_steel

        fsy : float
            Design yield strength of reinforcement in MPa (refer Cl 3.6.1), typically 500 MPa

        verbose : bool
            True to print internal calculations
            False otherwise

        Examples
        ========

        >>> from ..
        """
        moment_cap = self._bending(
            fsy=fsy,
            d=d,
            area_tension_steel=area_tension_steel,
            b=self.thickness,
            verbose=verbose,
        )
        return moment_cap

    def _calc_km(self, verbose: bool = True) -> float:
        km = 1.6
        if verbose:
            print("Mortar class M3")
            print("Bedding type: Face shell")
            print(f"km: {km}")
        return km
