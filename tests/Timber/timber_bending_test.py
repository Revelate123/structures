"""Test cases for Timber bending capacities"""

from structures.Timber import timber


class TestInPlaneBending:
    """Tests beam bending capacity in accordance with AS 1720.1 Cl 3.2.1"""

    def test_slender_beam(self):
        """
        240 x 45 F17 Beam spanning 2000mm with restraints to compression edge at each end:

        Md = phi * k1 * k4 * k6 * k9 * k12 * fb * Z
        phi = 0.95 (Category 1, F17)
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
            length="1000",
            depth=240,
            breadth=45,
            latitude=False,
            seasoned=True,
            grade="F17",
            category=1,
        )
        cap = beam.major_axis_bending(
            moisture_content=15, ncom=1, nmem=1, restraint_location=1, lay=2000
        )
        assert cap["k1 = 1"] == 9.65

    def test_stocky_beam(self):
        """
        120 x 90 F7 Beam spanning 2000mm with restraints to tension edge:

        Md = phi * k1 * k4 * k6 * k9 * k12 * fb * Z
        phi = 0.7 (Category 2, F17)
        k4 = 1
        k6 = 1 (Located in NSW)
        k9 = 1 (single member)
        S1 = (d/b)^1.35 * (Lay/d)^0.25 = (120/90)^1.35 * (2000/120)^0.25
        S1 = 1.47457 * 2.020516 = 2.97940 = 2.98
        pb = 0.86 (seasoned)
        pb*S1 = 0.86 * 2.98 = 2.56
        k12 = 1
        fb = 18 MPa
        Z = 90 * 120 ^2 /6 = 216,000 mm3
        Md = k1 * 0.7 * 1 * 18 MPa * 216,000mm3 = k1 * 2.72 KNm
        """
        beam = timber.Beam(
            length=2000,
            depth=120,
            breadth=90,
            latitude=False,
            seasoned=True,
            grade="F7",
            category=2,
        )
        cap = beam.major_axis_bending(
            moisture_content=15, ncom=1, nmem=1, restraint_location=2, lay=2000
        )
        assert cap["k1 = 1"] == 2.72

    def test_slender_beam_minor_axis(self):
        """
        45 x 240 F17 Beam spanning 2000mm with restraints to compression edge at each end:

        Md = phi * k1 * k4 * k6 * k9 * k12 * fb * Z
        phi = 0.95 (Category 1, F17)
        k4 = 1
        k6 = 1 (Located in NSW)
        k9 = 1 (single member)
        S1 = 1.25 * 45/240 * (2000/45)^0.5 = 1.5625
        pb = 0.98 (seasoned)
        pb*S1 = 0.98 * 1.5625 = 1.53
        k12 = 1
        fb = 42 MPa
        Z = 240 * 45 ^2 /6 = 81,000 mm3
        Md = k1 * 0.95 * 1 * 42 MPa * 81,000 mm3 = k1 * 3.23 KNm
        """
        beam = timber.Beam(
            length="1000",
            depth=45,
            breadth=240,
            latitude=False,
            seasoned=True,
            grade="F17",
            category=1,
        )
        cap = beam.minor_axis_bending(
            moisture_content=15, ncom=1, nmem=1, restraint_location=1, lay=2000
        )
        assert cap["k1 = 1"] == 3.23

    def test_long_span_lvl(self):
        """
        360 x 90 LVL13 Beam spanning 6000mm:

        Md = phi * k1 * k4 * k6 * k9 * k12 * fb * Z
        phi = 0.9 (Category 2, F17)
        k4 = 1
        k6 = 1 (Located in NSW)
        k9 = 1 (single member)
        S1 = (d/b)^1.35 * (Lay/d)^0.25
        S1 = (360/90)^1.35 * (6000/360)^0.25
        S1 = 13.13

        pb = 14.71 * (E/fb)^-0.48 * r^-0.061 (Worst case assume r=0.25)
        pb = 14.71 * (13200/33.18)^-0.48 * (0.25)^-0.061
        pb = 14.71 * 0.0565125 * 1.088242
        pb = 0.90
        pb*S1 = 0.90 * 13.13 = 11.82
        k12 = 1.5 - 0.05*11.82 = 0.91
        fb = 42 * (95/360)^0.154 * (300/360)^0.167 = 33.18 MPa
        Z = 90 * 360 ^2 /6 = 1,944,000 mm3
        Md = k1 * 0.9 * 0.91 * 33.18 MPa * 1,944,000 mm3 = k1 * 52.83 KNm
        """
        beam = timber.Beam(
            length=6000,
            depth=360,
            breadth=90,
            latitude=False,
            seasoned=True,
            grade="LVL13",
            category=2,
        )
        cap = beam.major_axis_bending(
            moisture_content=15, ncom=1, nmem=1, restraint_location=2, lay=6000
        )
        assert cap["k1 = 1"] == 52.83

    def test_compression_flange_restraints(self):
        pass

    def test_tension_flange_restraints(self):
        pass

    def test_ncom_5(self):
        pass

    def test_nmem_2_ncom_4(self):
        pass

    def test_continually_restrained(self):
        pass
