"""
This module performs engineering calculations in accordance with
AS3700:2018 for unreinforced masonry
"""

from toms_structures._masonry import _Masonry


class Clay(_Masonry):
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

        raking : float
            depth of raking in mm, defaults to 0 mm

        fmt : float
            Characteristic flexural tensile strength of masonry in MPa, defaults to 0.2 MPa

    """

    hu: float = 76
    tj: float = 10
    face_shell_thickness: float = 0
    raking: float = 0
    fmt: float = 0.2
    fut: float = 0.8
    phi_shear: float = 0.6
    phi_bending: float = 0.6
    phi_compression: float = 0.75
    density: float = 19
    grouted: bool = False
    fcg: float = 15

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


class HollowConcrete(_Masonry):
    """Concrete Masonry object

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

    raking : float
        depth of raking in mm, defaults to 0 mm

    fmt : float
        Characteristic flexural tensile strength of masonry in MPa, defaults to 0.2 MPa

    """

    hu: float = 200
    tj: float = 10
    face_shell_thickness: float = 30
    raking: float = 0
    fmt: float = 0.2
    fut: float = 0.8
    phi_shear: float = 0.6
    phi_bending: float = 0.6
    phi_compression: float = 0.75
    density: float = 19
    grouted: bool = False
    fcg: float = 15

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

    def _calc_kc(self) -> float:
        if self.density > 20:
            return 1.4
        else:
            return 1.2
