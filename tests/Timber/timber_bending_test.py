import structures.Timber.timber as timber


class TestInPlaneBending:
    """Tests beam bending capacity in accordance with AS 1720.1 Cl 3.2.1"""

    def test_slender_beam(self):
        """
        240 x 45 F17 Beam spanning 2000mm with restraints to compression edge:

        Md = phi * k1 * k4 * k6 * k9 * k12 * fb * Z
        phi = 0.95 (Category I, F17)
        k4 = 1
        k6 = 1 (Located in NSW)
        k9 = 1 (single member)
        S1 = 1.25 * 240/45 * (2000/240)^0.5 = 19.25
        pb = 0.98 (seasoned)
        pb*S1 = 0.98 * 19.25 = 18.87
        k12 = 1.5 - 0.05 * pb*S1 = 0.56
        fb = 42 MPa
        Z = 45 * 240 ^2 /6 = 432,000 mm3
        Md = k1 * 0.95 * 0.56 * 42 MPa * 432,000mm3 = k1 * 9.65 KNm
        """
        beam = timber.Beam(
            length=1000,
            depth=240,
            breadth=45,
            latitude=False,
            seasoned=True,
            grade="F17",
            category=1,
        )
        cap = beam.in_plane_bending(
                moisture_content=15, ncom=1, nmem=1, restraint_location=1, lay=2000
            )
        assert (
            cap["5 seconds"]
            == 9.65
        )

    def test_stocky_beam(self):
        pass

    def test_width_greater_than_height(self):
        pass

    def test_long_span(self):
        pass

    def test_compression_flange_restraints(self):
        pass

    def test_tension_flange_restraints(self):
        pass

    def test_ncom_5(self):
        pass

    def test_nmem_ncom_4(self):
        pass

    def test_continually_restrained(self):
        pass
