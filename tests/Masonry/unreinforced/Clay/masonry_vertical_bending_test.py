"""Contains tests for unreinforced clay masonry in vertical bending"""

from structures.Masonry import unreinforced_masonry


class TestUnreinforcedMasonryBending:
    """Tests for vertical bending in accordance with 7.4.2"""

    def test_tall_wall(self):
        """
        Length = 3000
        Height = 6000
        thickness = 110
        Zd = 3000 * 110^2/6 = 6,050,000mm3
        fmt = 0.2MPa
        fd = 0.8MPa (limited to 0.36MPa)
        Lowest of
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 6,050,000 + 0.36 * 6,050,000 = 2.94MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 6,050,000 = 2.178 MPa
        Mcv = 2.178 KNm
        """
        wall = unreinforced_masonry.Clay(
            length=3000,
            height=6000,
            thickness=110,
            mortar_class=3,
            fuc=20,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=0.8, interface=True) == 2.18

    def test_short_wall(self):
        """
        Length = 3000
        Height = 1000
        thickness = 110
        Zd = 3000 * 110^2/6 = 6,050,000mm3
        fmt = 0.2MPa
        fd = 0.8MPa (limited to 0.36MPa)
        Lowest of
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 6,050,000 + 0.36 * 6,050,000 = 2.94MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 6,050,000 = 2.178 MPa
        Mcv = 2.178 KNm
        """
        wall = unreinforced_masonry.Clay(
            length=3000,
            height=1000,
            thickness=110,
            mortar_class=3,
            fuc=20,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=0.8, interface=True) == 2.18

    def test_thick_wall(self):
        """
        Length = 3000
        Height = 1000
        thickness = 230
        Zd = 3000 * 230^2/6 = 26,450,000 mm3
        fmt = 0.2MPa
        fd = 0.8MPa (limited to 0.36MPa)
        Lowest of
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 26,450,000 + 0.36 * 26,450,000 = 12.696 MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 26,450,000 = 9.522 MPa
        Mcv = 9.52 KNm
        """
        wall = unreinforced_masonry.Clay(
            length=3000,
            height=1000,
            thickness=230,
            mortar_class=3,
            fuc=20,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=0.8, interface=True) == 9.52

    def test_large_fd(self):
        """
        Length = 1000
        Height = 1000
        thickness = 90
        Zd = 1000 * 90^2/6 = 1,350,000 mm3
        fmt = 0.2MPa
        fd = 2MPa (limited to 0.36MPa)
        Lowest of
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 1,350,000 + 0.36 * 1,350,000 = 0.648 MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 1,350,000 = 0.486 MPa
        Mcv = 0.49 KNm
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=90,
            mortar_class=3,
            fuc=20,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=2, interface=True) == 0.49

    def test_fd_0(self):
        """
        Length = 1000
        Height = 1000
        thickness = 100
        Zd = 1000*100^2/6 = 1,666,666.6667 mm3
        fmt = 0.2 MPa
        fd = 0
        Lowest of:
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 1,666,666.6667 = 0.2MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 1,666,666.6667 = 0.6MPa
        Mcv = 0.2 KNm
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=1000,
            thickness=100,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=0, interface=True) == 0.2

    def test_vertical_bending_1(self):
        """
        Mdv <= Mcv
        Length = 1000mm
        Height = 1000mm
        Thickness = 110mm
        Zd = 2016666.667 mm^3
        phi = 0.6
        fmt = 0.2 MPa
        fd = 0

        if fmt > 0:

        Lowest of:
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 20126666.667 = 0.242MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 20126666.67 = 0.72MPa
        Mcv = 0.24 KNm
        """
        wall = unreinforced_masonry.Clay(
            length=1000,
            height=2000,
            thickness=110,
            fmt=0.2,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=0, interface=True) == 0.24

    def test_fmt_0(self):
        """
        Mdv <= Mcv
        Length = 1000mm
        Height = 1000mm
        Thickness = 110mm
        Zd = 2016666.667 mm^3
        phi = 0.6
        fmt = 0 MPa
        fd = 0.1 MPa

        Mcv = fd * Zd = 0.20 KNm
        """

        wall = unreinforced_masonry.Clay(
            length=1000,
            height=2000,
            thickness=110,
            fmt=0,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=0.1, interface=True) == 0.2

    def test_vertical_bending_3(self):
        """
        Mdv <= Mcv
        Length = 500mm
        Height = 2000mm
        Thickness = 110mm
        Zd = 1008333.333 mm^3
        phi = 0.6
        fmt = 0.2 MPa
        fd = half wall height = 19KN/m3 * 1m = 19KPa = 0.019 MPa

        if fmt > 0:
        Lowest of:
        Mcv = phi * fmt * Zd + fd * Zd
            = 0.6 * 0.2MPa * 1008333.333 mm3 + 0.019MPa * 1008333.333 mm3 = 0.140MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 1008333.333 = 0.363MPa
        Mcv = 0.140 KNm
        """

        wall = unreinforced_masonry.Clay(
            length=500,
            height=2000,
            thickness=110,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.vertical_bending(fd=0.019, interface=True) == 0.140
