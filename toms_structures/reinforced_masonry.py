"""
This module performs engineering calculations in accordance with
AS3700:2018 for reinforced masonry
"""

from toms_structures._reinforced_masonry import _ReinforcedMasonry


class HollowConcrete(_ReinforcedMasonry):
    """For the design of reinforced block masonry in accordance with AS3700:2018

    Parameters
    ----------

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

    """

    hu: float = 200
    tj: float = 10
    lu: float = 400
    face_shell_thickness: float = 10
    raking: float = 0
    fmt: float = 0.2
    fut: float = 0.8
    phi_shear: float = 0.75
    phi_bending: float = 0.75
    phi_compression: float = 0.75
    density: float = 19
    grouted: bool = False
    fcg: float = 15

    def out_of_plane_vertical_bending(
        self,
        d: float,
        area_tension_steel: float,
        fsy: float,
        fd: float,
        interface: bool,
        verbose: bool = True,
    ) -> float:
        """
        Computes the bending capacity of a reinforced masonry wall element in accordance with
        AS3700:2018 Cl 8.6.

        Parameters
        ----------

        d : float
            Effective depth of the reinforced masonry member from the extreme compressive
            fibre of the masonry to the resultant tensile force in the steel in the tensile
            zone in mm. Typical values are 95 for 190 block walls

        b : float
            Width of the masonry member of solid rectangular cross-section or the effective
            width of a member in accordance with Cl 4.5.2

        area_tension_steel : float
            Cross-sectional area of fully anchored longitudinal reinforcement in the tension
            zone of the cross-section under consideration in mm². Denoted as Ast in AS3700. Note:
            the amount of steel used in calculation is limited to effective_area_tension_steel

        fsy : float
            Design yield strength of reinforcement in MPa (refer Cl 3.6.1), typically 500 MPa

        fd : float
            The minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        verbose : bool
            True to print internal calculations
            False otherwise

        Returns
        -------
            Moment capacity in KN : float
        """
        moment_cap = self._reinforced_bending(
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
        fd: float,
        interface: bool,
        verbose: bool = True,
    ) -> float:
        """
        Computes the bending capacity of a reinforced masonry wall element in accordanc with
        AS 3700 Cl 8.6.

        Parameters
        ----------

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

        fd : float
            The minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        verbose : bool
            True to print internal calculations
            False otherwise

        Returns
        -------
            Moment capacity in KN : float
        """
        moment_cap = self._reinforced_bending(
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
    ) -> float:
        """
        Computes the bending capacity of a reinforced masonry wall element using the methods
        described in AS 3700 Cl 8.6.

        Parameters
        ----------

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

        Returns
        -------
            Moment capacity in KN : float

        """
        moment_cap = self._reinforced_bending(
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

    def _calc_kc(self) -> float:
        if self.density > 20:
            return 1.4
        else:
            return 1.2
