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

        """
        return self._basic_compressive_capacity(verbose=verbose)

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
        ----------

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

        Returns
        -------
            A dictionary with crushing and buckling capacity in kN.
        """
        return self._compression_capacity(
            simple_av=simple_av,
            kt=kt,
            compression_load_type=compression_load_type,
            verbose=verbose,
        )

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
        ----------

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

        Returns
        -------
            dict: {
                'Crushing': crushing_compressive_capacity,
                'Buckling': kFo,
            }

        """
        return self._refined_compression(
            refined_av=refined_av,
            refined_ah=refined_ah,
            kt=kt,
            e1=e1,
            e2=e2,
            dist_to_return=dist_to_return,
            effective_length=effective_length,
            verbose=verbose,
        )

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
        ----------

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

        Returns
        -------
            A dictionary with crushing and buckling capacity in kN.

        """
        return self._concentrated_load(
            simple_av=simple_av,
            kt=kt,
            compression_load_type=compression_load_type,
            dist_to_end=dist_to_end,
            bearing_width=bearing_width,
            bearing_length=bearing_length,
            verbose=verbose,
        )

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
        ----------

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

        Returns
        -------
            dict: {
                "Crushing",
                "Buckling",
                "Bearing"
            }
        """
        return self._refined_concentrated_load(
            refined_av=refined_av,
            refined_ah=refined_ah,
            kt=kt,
            e1=e1,
            e2=e2,
            dist_to_return=dist_to_return,
            dist_to_end=dist_to_end,
            bearing_width=bearing_width,
            bearing_length=bearing_length,
            verbose=verbose,
        )

    def vertical_bending(
        self,
        fd: float | None = None,
        interface: None | bool = None,
        verbose: bool = True,
    ) -> float:
        """Computes the vertical bending capacity in accordance with AS 3700 Cl 7.4.2

        Parameters
        ----------

        fd : float
            The minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        interface : bool
            True if shear plane is masonry to masonry,
            and False if shear_plane is masonry to other material

        verbose : bool
            Whether to print outputs

        Returns
        -------
            m_cv : float
        """
        return self._vertical_bending(
            fd=fd,
            interface=interface,
            verbose=verbose,
        )

    def horizontal_bending(
        self,
        fd: float | None = None,
        interface: None | bool = None,
        verbose: bool = True,
    ) -> float:
        """Computes the horizontal bending capacity in accordance with AS3700 Cl 7.4.3.2

        Parameters
        ----------

        fd : float
            The minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        interface : bool
            True if shear plane is masonry to masonry,
            and False if shear_plane is masonry to other material

        verbose : bool
            Whether to print outputs

        Returns
        -------
            Horizontal bending capacity in KN : float
        """
        return self._horizontal_bending(
            fd=fd,
            interface=interface,
            verbose=verbose,
        )

    def horizontal_plane_shear(
        self,
        kv: float,
        interface: float,
        fd: float,
        verbose: bool = True,
    ) -> dict:
        """Calculates the  horizontal shear capacity in accordance with AS3700:2018 Cl 7.5.4.1

        Parameters
        ----------

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

        Returns
        -------
            Horizontal shear capacity in KN : float
        """
        return self._horizontal_plane_shear(
            kv=kv,
            interface=interface,
            fd=fd,
            verbose=verbose,
        )

    def vertical_plane_shear(self, verbose: bool = True) -> float:
        """Computes the horizontal shear capacity in accordance with AS3700 Cl 7.5.4.2"""
        return self._vertical_plane_shear(verbose=verbose)

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

        """
        return self._basic_compressive_capacity(verbose=verbose)

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
        ----------

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

        Returns
        -------
            A dictionary with crushing and buckling capacity in kN.
        """
        return self._compression_capacity(
            simple_av=simple_av,
            kt=kt,
            compression_load_type=compression_load_type,
            verbose=verbose,
        )

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
        ----------

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

        Returns
        -------
            dict: {
                'Crushing': crushing_compressive_capacity,
                'Buckling': kFo,
            }

        """
        return self._refined_compression(
            refined_av=refined_av,
            refined_ah=refined_ah,
            kt=kt,
            e1=e1,
            e2=e2,
            dist_to_return=dist_to_return,
            effective_length=effective_length,
            verbose=verbose,
        )

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
        ----------

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

        Returns
        -------
            A dictionary with crushing and buckling capacity in kN.

        """
        return self._concentrated_load(
            simple_av=simple_av,
            kt=kt,
            compression_load_type=compression_load_type,
            dist_to_end=dist_to_end,
            bearing_width=bearing_width,
            bearing_length=bearing_length,
            verbose=verbose,
        )

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
        ----------

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

        Returns
        -------
            dict: {
                "Crushing",
                "Buckling",
                "Bearing"
            }
        """
        return self._refined_concentrated_load(
            refined_av=refined_av,
            refined_ah=refined_ah,
            kt=kt,
            e1=e1,
            e2=e2,
            dist_to_return=dist_to_return,
            dist_to_end=dist_to_end,
            bearing_width=bearing_width,
            bearing_length=bearing_length,
            verbose=verbose,
        )

    def vertical_bending(
        self,
        fd: float | None = None,
        interface: None | bool = None,
        verbose: bool = True,
    ) -> float:
        """Computes the vertical bending capacity in accordance with AS 3700 Cl 7.4.2

        Parameters
        ----------

        fd : float
            The minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        interface : bool
            True if shear plane is masonry to masonry,
            and False if shear_plane is masonry to other material

        verbose : bool
            Whether to print outputs

        Returns
        -------
            m_cv : float
        """
        return self._vertical_bending(
            fd=fd,
            interface=interface,
            verbose=verbose,
        )

    def horizontal_bending(
        self,
        fd: float | None = None,
        interface: None | bool = None,
        verbose: bool = True,
    ) -> float:
        """Computes the horizontal bending capacity in accordance with AS3700 Cl 7.4.3.2

        Parameters
        ----------

        fd : float
            The minimum design compressive stress on the bed joint at the
            cross-section under consideration (see Clause 7.4.3.3), in MPa

        interface : bool
            True if shear plane is masonry to masonry,
            and False if shear_plane is masonry to other material

        verbose : bool
            Whether to print outputs

        Returns
        -------
            Horizontal bending capacity in KN : float
        """
        return self._horizontal_bending(
            fd=fd,
            interface=interface,
            verbose=verbose,
        )

    def horizontal_plane_shear(
        self,
        kv: float,
        interface: float,
        fd: float,
        verbose: bool = True,
    ) -> dict:
        """Calculates the  horizontal shear capacity in accordance with AS3700:2018 Cl 7.5.4.1

        Parameters
        ----------

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

        Returns
        -------
            Horizontal shear capacity in KN : float
        """
        return self._horizontal_plane_shear(
            kv=kv,
            interface=interface,
            fd=fd,
            verbose=verbose,
        )

    def vertical_plane_shear(self, verbose: bool = True) -> float:
        """Computes the horizontal shear capacity in accordance with AS3700 Cl 7.5.4.2"""
        return self._vertical_plane_shear(verbose=verbose)

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
