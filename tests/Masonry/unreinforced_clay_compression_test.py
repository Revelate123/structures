"""Contains tests for unreinforced clay masonry in compression"""

import pytest
import structures.Masonry.unreinforced_masonry as unreinforced_masonry


class TestBasicCompressiveCapacity:
    """Tests for the Basic compressive capacity, in accordance with AS3700 Cl 7.3.2"""

    def test_standard_m3_brick(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 6.261 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 6.261 = 4.70 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.basic_compressive_capacity() == 4.70

    def test_standard_m4_brick(self):
        """
        km = 2 (For clay Full Bedding M4 mortar class)
        fmb = km * sqrt(fuc) = 2 * sqrt(20) = 8.944 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 8.944 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 8.944 = 6.71 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=20,
            mortar_class=4,
            bedding_type=True,
        )
        assert wall.basic_compressive_capacity() == 6.71

    def test_low_compressive_strength_brick(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(5) = 3.130 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 3.130 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 3.130 = 2.35 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=5,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.basic_compressive_capacity() == 2.35

    def test_high_compressive_strength_brick(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(60) = 10.844 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 10.844 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 10.844 = 8.13 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=60,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.basic_compressive_capacity() == 8.13

    def test_face_shell_bedding_type(self):
        """
        km = 1.6 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.6 * sqrt(20) = 7.155 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 7.155 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 7.155 = 5.37 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=20,
            mortar_class=3,
            bedding_type=False,
        )
        assert wall.basic_compressive_capacity() == 5.37

    def test_fails_for_m4_face_shell_bedding_type(self):
        """AS3700 does not provide values for mortar class M4 and face shell bedding"""
        with pytest.raises(ValueError):
            wall = unreinforced_masonry.Clay(
                length=1000,
                height=1000,
                thickness=100,
                fuc=20,
                mortar_class=4,
                bedding_type=False,
            )
            wall.basic_compressive_capacity()

    def test_fails_for_m1_mortar(self):
        """AS3700 does not provide values for mortar class M1"""
        with pytest.raises(ValueError):
            wall = unreinforced_masonry.Clay(
                length=1000,
                height=1000,
                thickness=100,
                fuc=20,
                mortar_class=1,
                bedding_type=True,
            )
            wall.basic_compressive_capacity()

    def test_90_brick_10_joint(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.05 (for 90mm brick height with 10mm thick mortar)
        fm = kh * fmb = 1.05 * 6.261 MPa = 6.574 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 6.261 = 4.93 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=90,
            tj=10,
            hu=90,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.basic_compressive_capacity() == 4.93

    def test_150_brick_12_joint(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.3 * (150/(19*12))**0.29 = 1.151
        fm = kh * fmb = 1.151 * 6.261 MPa = 7.206 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 7.206 = 5.40 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            tj=12,
            hu=150,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.basic_compressive_capacity() == 5.40

    def test_200_brick_5_joint(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.3 (maximum value)
        fm = kh * fmb = 1.3 * 6.261 MPa = 8.14 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 8.14 = 6.11 MPa
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            tj=5,
            hu=200,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.basic_compressive_capacity() == 6.11


class TestSimplifiedCompression:
    """Tests wall compressive capacity based on the simplified method given in AS3700 Cl 7.3.3"""

    def test_slender_concrete_slab_over(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa

        Srs = 1 * 3000 / (1 * 110) = 27.27

        k = 0.67 - 0.02 * (27.27 - 14) = 0.40

        kFo = 0.4 * 4.07 MPa * 1000mm * 110mm = 179.08 KN

        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=3000,
            thickness=110,
            mortar_class=3,
            fuc=15,
            bedding_type=True,
        )
        assert (
            wall.compression_capacity(compression_load_type=1, simple_av=1, kt=1)
            == {"Simple":179.08}
        )

    def test_stocky_concrete_slab_over(self):
        """
        fm = 10.844 MPa
        Fo = phi * f'm = 0.75 * 10.844 = 8.13 MPa

        Srs = 1 * 1200/(1*100) = 12

        k = 0.67 - 0.02 * (12 - 14) = 0.71
        k = min(0.67, 0.71) = 0.67

        kFo = 0.67 * 8.13 MPa * 1000mm * 100mm = 544.71 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=60,
            mortar_class=3,
            bedding_type=True,
        )
        assert (
            wall.compression_capacity(compression_load_type=1, simple_av=1, kt=1)
            == {"Simple":544.71}
        )

    def test_slender_other_system_over(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa

        Srs = 2.5 * 1500 / (1 * 110) = 34.09

        k = 0.67 - 0.025 * (34.09 - 10) = 0.07

        kFo = 0.07 * 4.07 MPa * 1000mm * 110mm = 31.34 KN

        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1500,
            thickness=110,
            mortar_class=3,
            fuc=15,
            bedding_type=True,
        )
        assert (
            wall.compression_capacity(compression_load_type=2, simple_av=2.5, kt=1)
            == {"Simple":31.34}
        )

    def test_stocky_other_system_over(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa

        Srs = 1 * 1500 / (1 * 110) = 13.64

        k = 0.67 - 0.025 * (13.64 - 10) = 0.58

        kFo = 0.58 * 4.07 MPa * 1000mm * 110mm = 259.67 KN

        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1500,
            thickness=110,
            mortar_class=3,
            fuc=15,
            bedding_type=True,
        )
        assert (
            wall.compression_capacity(compression_load_type=2, simple_av=1, kt=1)
            == {"Simple":259.67}
        )

    def test_slender_face_loading(self):
        """
        fm = 10.844 MPa
        Fo = phi * f'm = 0.75 * 10.844 = 8.13 MPa

        Srs = 1 * 3000/(1*100) = 30

        k = 0.067 - 0.002 * (30 - 14) = 0.035
        k = min(0.067, 0.035) = 0.035

        kFo = 0.035 * 8.13 MPa * 1000mm * 100mm = 28.46 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=3000,
            thickness=100,
            fuc=60,
            mortar_class=3,
            bedding_type=True,
        )
        assert (
            wall.compression_capacity(compression_load_type=3, simple_av=1, kt=1)
            == {"Simple":28.46}
        )

    def test_stocky_face_loading(self):
        """
        fm = 10.844 MPa
        Fo = phi * f'm = 0.75 * 10.844 = 8.13 MPa

        Srs = 1 * 1500/(1*100) = 15

        k = 0.067 - 0.002 * (15 - 14) = 0.065
        k = min(0.067, 0.035) = 0.065

        kFo = 0.065 * 8.13 MPa * 1000mm * 100mm = 52.85 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1500,
            thickness=100,
            fuc=60,
            mortar_class=3,
            bedding_type=True,
        )
        assert (
            wall.compression_capacity(compression_load_type=3, simple_av=1, kt=1)
            == {"Simple":52.85}
        )


class TestRefinedCompression:
    """Tests wall compressive capacity based on the refined method given in AS3700 Cl 7.3.4"""

    def test_face_shell_bedding(self):
        """
        pass
        """

    def test_equal_large_positive_eccentricity(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa
        Sr = 1 * 3000 / (1* 100) = 30
        e1 = e2 = 30mm

        Lateral stability:
        k = 0.5 * (1 + e2 / e1) * [(1 - 2.083 * e1/tw) - (0.025 - 0.037 * e1/tw)*(1.33*Sr - 8)]
            + 0.5(1 - 0.6*e1/tw)*(1 - e2/e1)*(1.18 - 0.03*Sr)

        =   0.5 * (1 + 30 / 30) * [(1 - 2.083 * 30/100) - (0.025 - 0.037 * 30/100)*(1.33*30 - 8)]
            + 0.5(1 - 0.6*30/100)*(1 - 30/30)*(1.18 - 0.03*30)

        =   1 * [(0.3751) - (0.0139)*(31.9)]
            + 0.5(0.82)*(0)*(-0.32)

        =   1 * [-0.06831]
            + 0

        = -0.07
        k cannot be less than 0
        k = 0.00
        Buckling capacity = 0KN

        Local Crushing
        k = 1 - 2*e1/tw
        = 1 - 2*30/100
        = 0.4
        Crushing capacity = 0.4 * 4.07 MPa * 100mm * 1000mm = 162.8 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=3000,
            thickness=100,
            fuc=15,
            mortar_class=3,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            e1=30, e2=30, refined_av=1, refined_ah=0, kt=1
        )
        assert capacity == {"Crushing": 162.8, "Buckling": 0}

    def test_opposite_large_eccentricity(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa
        Sr = 1 * 3000 / (1* 100) = 30
        e1 = 30mm
        e2 = -30mm

        Lateral stability:
        k = 0.5 * (1 + e2 / e1) * [(1 - 2.083 * e1/tw) - (0.025 - 0.037 * e1/tw)*(1.33*Sr - 8)]
            + 0.5(1 - 0.6*e1/tw)*(1 - e2/e1)*(1.18 - 0.03*Sr)

        = 0.5 * (1 + -30 / 30) * [(1 - 2.083 * 30/100) - (0.025 - 0.037 * 30/100)*(1.33*30 - 8)]
            + 0.5(1 - 0.6*30/100)*(1 - -30/30)*(1.18 - 0.03*30)

        = 0.5 * (0) * [(1 - 2.083 * 30/100) - (0.025 - 0.037 * 30/100)*(1.33*30 - 8)]
            + 0.5(0.82)*(2)*(0.28)

        = 0
            + 0.5(0.82)*(2)*(0.28)

        k = 0.2296 = 0.23
        Buckling capacity = 0.23 * 4.07 MPa * 100mm * 1000mm = 93.61KN

        Local Crushing
        k = 1 - 2*e1/tw
        = 1 - 2*30/100
        = 0.4
        Crushing capacity = 0.4 * 4.07 MPa * 100mm * 1000mm = 162.8 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=3000,
            thickness=100,
            fuc=15,
            mortar_class=3,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            e1=30, e2=-30, refined_av=1, refined_ah=0, kt=1
        )
        assert capacity == {"Crushing": 162.8, "Buckling": 93.61}

    def test_zero_eccentricity(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa
        Sr = 0.75 * 2700 / (1* 100) = 20.25
        e1 = 0.05 * 100mm = 5mm
        e2 = 0.05 * 100mm = 5mm

        Lateral stability:
        k = 0.5 * (1 + e2 / e1) * [(1 - 2.083 * e1/tw) - (0.025 - 0.037 * e1/tw)*(1.33*Sr - 8)]
            + 0.5(1 - 0.6*e1/tw)*(1 - e2/e1)*(1.18 - 0.03*Sr)

        = 0.5 * (1 + 5 / 5) * [(1 - 2.083 * 5/100) - (0.025 - 0.037 * 5/100)*(1.33*20.25 - 8)]
            + 0.5(1 - 0.6*5/100)*(1 - 5/5)*(1.18 - 0.03*20.25)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(18.9325)]
            + 0.5(1 - 0.6*5/100)*(0)*(1.18 - 0.03*20.25)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(18.9325)]
            + 0

        k = 0.457562625 = 0.46
        Buckling capacity = 0.46 * 4.07 MPa * 100mm * 1000mm = 187.22KN

        Local Crushing
        k = 1 - 2*e1/tw
        = 1 - 2*5/100
        = 0.9
        Crushing capacity = 0.9 * 4.07 MPa * 100mm * 1000mm = 366.3 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=2700,
            thickness=100,
            fuc=15,
            mortar_class=3,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            e1=0, e2=0, refined_av=0.75, refined_ah=0, kt=1
        )
        assert capacity == {"Crushing": 366.3, "Buckling": 187.22}

    def test_e2_exceeds_e1(self):
        """raises ValueError when e1 > e2"""
        with pytest.raises(ValueError):
            wall = unreinforced_masonry.Clay(
                length=1000,
                height=2700,
                thickness=100,
                fuc=15,
                mortar_class=3,
                bedding_type=True,
            )
            wall.refined_compression(e1=5, e2=10, refined_av=0.75, refined_ah=0, kt=1)

    def test_kt_not_1(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa
        kt = 1.7
        Sr = 0.75 * 2700 / (1.7* 100) = 11.91
        e1 = 0.05 * 100mm = 5mm
        e2 = 0.05 * 100mm = 5mm

        Lateral stability:
        k = 0.5 * (1 + e2 / e1) * [(1 - 2.083 * e1/tw) - (0.025 - 0.037 * e1/tw)*(1.33*Sr - 8)]
            + 0.5(1 - 0.6*e1/tw)*(1 - e2/e1)*(1.18 - 0.03*Sr)

        = 0.5 * (1 + 5 / 5) * [(1 - 2.083 * 5/100) - (0.025 - 0.037 * 5/100)*(1.33*11.91 - 8)]
            + 0.5(1 - 0.6*5/100)*(1 - 5/5)*(1.18 - 0.03*11.91)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(7.8403)]
            + 0.5(1 - 0.6*5/100)*(0)*(1.18 - 0.03*11.91)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(7.8403)]
            + 0

        k = 0.714347... = 0.71
        Buckling capacity = 0.71 * 4.07 MPa * 100mm * 1000mm = 288.97KN

        Local Crushing
        k = 1 - 2*e1/tw
        = 1 - 2*5/100
        = 0.9
        Crushing capacity = 0.9 * 4.07 MPa * 100mm * 1000mm = 366.3 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=2700,
            thickness=100,
            fuc=15,
            mortar_class=3,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            e1=0, e2=0, refined_av=0.75, refined_ah=0, kt=1.7
        )
        assert capacity == {"Crushing": 366.3, "Buckling": 288.97}

    def test_cantilever_wall(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa
        Sr = 2.5 * 1000 / (1* 100) = 25
        e1 = 0.05 * 100mm = 5mm
        e2 = 0.05 * 100mm = 5mm

        Lateral stability:
        k = 0.5 * (1 + e2 / e1) * [(1 - 2.083 * e1/tw) - (0.025 - 0.037 * e1/tw)*(1.33*Sr - 8)]
            + 0.5(1 - 0.6*e1/tw)*(1 - e2/e1)*(1.18 - 0.03*Sr)

        = 0.5 * (1 + 5 / 5) * [(1 - 2.083 * 5/100) - (0.025 - 0.037 * 5/100)*(1.33*25 - 8)]
            + 0.5(1 - 0.6*5/100)*(1 - 5/5)*(1.18 - 0.03*25)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(25.25)]
            + 0.5(1 - 0.6*5/100)*(0)*(1.18 - 0.03*25)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(25.25)]
            + 0

        k = 0.3113125 = 0.31
        Buckling capacity = 0.31 * 4.07 MPa * 100mm * 1000mm = 126.17 KN

        Local Crushing
        k = 1 - 2*e1/tw
        = 1 - 2*5/100
        = 0.9
        Crushing capacity = 0.9 * 4.07 MPa * 100mm * 1000mm = 366.3 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=15,
            mortar_class=3,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            e1=0, e2=0, refined_av=2.5, refined_ah=0, kt=1
        )
        assert capacity == {"Crushing": 366.3, "Buckling": 126.17}

    def test_horz_capacity_limited_by_Fo(self):
        """
        fm = 5.42 MPa
        Fo = 0.75 * 5.42 MPa = 4.07 MPa
        Sr = 2.5 * 1000 / (1* 100) = 25
        e1 = 0.05 * 100mm = 5mm
        e2 = 0.05 * 100mm = 5mm

        Lateral stability:
        k = 0.5 * (1 + e2 / e1) * [(1 - 2.083 * e1/tw) - (0.025 - 0.037 * e1/tw)*(1.33*Sr - 8)]
            + 0.5(1 - 0.6*e1/tw)*(1 - e2/e1)*(1.18 - 0.03*Sr)

        = 0.5 * (1 + 5 / 5) * [(1 - 2.083 * 5/100) - (0.025 - 0.037 * 5/100)*(1.33*25 - 8)]
            + 0.5(1 - 0.6*5/100)*(1 - 5/5)*(1.18 - 0.03*25)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(25.25)]
            + 0.5(1 - 0.6*5/100)*(0)*(1.18 - 0.03*25)

        = 0.5 * (2) * [(0.89585) - (0.02315)*(25.25)]
            + 0

        k = 0.3113125 = 0.31
        Buckling capacity = 0.31 * 4.07 MPa * 100mm * 1000mm = 126.17 KN

        Local Crushing
        k = 1 - 2*e1/tw
        = 1 - 2*5/100
        = 0.9
        Crushing capacity = 0.9 * 4.07 MPa * 100mm * 1000mm = 366.3 KN
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=15,
            mortar_class=3,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            e1=0, e2=0, refined_av=2.5, refined_ah=1, kt=1,dist_to_return=0
        )
        assert capacity == {"Crushing": 366.3, "Buckling": 126.17}

    def test_stocky_wall(self):
        pass

    def test_stocky_wall_two_returns(self):
        pass

    def test_slender_wall_one_return_nearby(self):
        pass

    def test_slender_wall_two_returns_large_spacing(self):
        pass

    def test_slender_wall_one_return_large_spacing(self):
        pass

    def test_two_returns(self):
        pass

    def test_refined_compression(self):
        """
        Scenario:
        A masonry wall 600W x 2700H x 110 Thick is supporting an eccentric load applied by an RC slab.

        Fd <= kFo

        Fo = phi * fm * Ab
        fm = 8.94MPa
        phi = 0.75
        Fo = 0.75 * 8.94 * Ab = 6.71MPa
        Sr = av * H / (kt * t) = 0.75 * 2700 / (1 * 110) = 18.41
        k = 0.5(1+ e1/e2) * [(1 - 2.082* e1/tw) - (0.025 - 0.037 * e1/tw) * (1.33 * Sr - 8)] + 0.5 * (1 - 0.6 * e1/tw) * (1 - e2/e1) * (1.18 - 0.03Sr)
        k =  1 * [(0.65300) - (0.01883333) * (16.4841)] + 0 = 0.34
        e1 = tw/6 = 18.3333mm
        e2 = tw/6 = 18.3333mm
        tw = 110mm
        Ab = 600*110 = 66,000 mm2
        kFo = 6.71MPa * 66,000mm2 * 0.34 = 150.57KN

        k = 1 - 2*(18.33/110) = 0.67
        Fo = 6.71MPa * 66,000mm2 * 0.67 = 296.72

        """
        wall = unreinforced_masonry.Clay(
            length=600,
            height=2700,
            thickness=110,
            fuc=20,
            mortar_class=4,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            refined_av=0.75, kt=1, e1=110 / 6, e2=110 / 6, refined_ah=0
        )
        assert capacity["Buckling"] == 150.57
        assert capacity["Crushing"] == 296.72

    def test_refined_compression_2(self):
        """
        Fd <= kFo

        Fo = phi * fm * Ab
        fm = 4.43MPa
        phi = 0.75
        Fo = 3.32MPa

        k = 0.5(1+ e1/e2) * [(1 - 2.082* e1/tw) - (0.025 - 0.037 * e1/tw) * (1.33 * Sr - 8)] 
        + 0.5 * (1 - 0.6 * e1/tw) * (1 - e2/e1) * (1.18 - 0.03Sr)

        k =  1 * [(0.65300) - (0.01883333) * (16.4841)] + 0 = 0.34

        e1 = tw/6 = 18.3333mm
        e2 = tw/6 = 18.3333mm
        tw = 110mm
        Sr = av * H / (kt * t) = 0.75 * 2700 / (1 * 110) = 18.41
        kFo = 3.32 MPa * 600 * 110 * 0.34 = 74.50KN

        k = 1 - 2*(18.33/110) = 0.67
        Fo = 3.32 MPa * 600 * 110 * 0.67 = 146.81
        """
        wall = unreinforced_masonry.Clay(
            length=600,
            height=2700,
            thickness=110,
            fuc=10,
            mortar_class=3,
            bedding_type=True,
        )
        capacity = wall.refined_compression(
            refined_av=0.75, e1=110 / 6, e2=110 / 6, refined_ah=0, kt=1
        )

        assert capacity["Buckling"] == 74.50
        assert capacity["Crushing"] == 146.81

    def test_refined_compression_3(self):
        """
        Fd <= kFo

        Fo = phi * fm * Ab
        fm = 4.4MPa
        phi = 0.75
        Fo = 3.3MPa * Ab
        Ab = 1500*110 = 165,000 mm2
        Fo = 544.5 KN
        k = 0.5(1+ e1/e2) * [(1 - 2.082* e1/tw) - (0.025 - 0.037 * e1/tw) * (1.33 * Sr - 8)]
          + 0.5 * (1 - 0.6 * e1/tw) * (1 - e2/e1) * (1.18 - 0.03Sr)
        k =  1 * [(0.65300) - (0.01883333) * (16.4841)] + 0 = 0.34255
        e1 = tw/6 = 18.3333mm
        e2 = tw/6 = 18.3333mm
        tw = 110mm
        Sr = av * H / (kt * t) = 0.75 * 2700 / (1 * 110) = 18.40909
        kFo = 544.5 KN * 0.34255 = 186.5KN

        """
        # wall = masonry.UnreinforcedMasonry(length=1500, height=2700, thickness=110, av=0.75, kt = 1, Ab =0 , fuc=10, mortar_class=3)
        # assert(round(wall.refined_compression(),1) == 186.5)

    def test_define_bearing_area(self):
        pass


class TestConcentratedLoad:
    """ Tests concentrated bearing load in accordance with AS3700 Cl 7.3.5 """
    def test_concetrated_load_1(self):
        """ """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )

        assert wall

    def test_short_wall(self):
        pass

    def test_long_wall(self):
        pass

    def test_large_bearing_area(self):
        pass

    def test_small_bearing_area(self):
        pass

    def test_crushing_governs(self):
        pass

    def test_buckling_governs(self):
        pass

    def test_bearing_governs(self):
        pass
