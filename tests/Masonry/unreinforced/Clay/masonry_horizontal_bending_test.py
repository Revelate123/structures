"""Contains tests for unreinforced clay masonry in horizontal bending"""

from structures.Masonry import unreinforced_masonry


class TestUnreinforcedMasonryHorizontalBending:
    """Tests for horizontal bending in accordance with 7.4.3"""

    def test_horizontal_bending_1(self):
        """
        Mdh < Mch

        Mch = 2 * phi * kp * (math.sqrt(fmt)) * (1 + fd/fmt) * Zd
            = 2 * 0.6 * 1 * 0.447 *1 * 479966.6667 = 0.257KNm
        Mch = 4 * phi * kp * (math.sqrt(fmt)) * Zd
            = 4 * 0.6 * 1 * 0.447 * 479966.6667 = 0.515KNm
        Mch = phi * (0.44 * fut * Zu + 0.56 * fmt * Zp)
            = 0.6 * (0.44 * 0.8MPa * 479966.6667mm3 + 0.56 * 0.2MPa * 479966.6667mm3)
            = 0.134KNm

        phi = 0.6
        lesser of: Cl 7.4.3.4
            kp = Sp/tu = (230/2)/110 = 1.05
            kp = sp/hu = (230/3)/76 = 1.5
            kp = 1
        fmt = 0.2 MPa
        fut = 0.8 MPa Cl 3.2
        fd = 0
        Zd = (3 * 86 - 20) * 110**2 /6 = 479966.6667mm3

        """

        wall = unreinforced_masonry.Clay(
            length=3000,
            height=3 * 86 - 20,
            thickness=110,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        assert wall.horizontal_bending(fd=0, interface=True) == 0.13

    def test_horizontal_bending_2(self):
        """
        Mdh < Mch

        Mch = 2 * phi * kp * (math.sqrt(fmt)) * (1 + fd/fmt) * Zd
            = 2 * 0.6 * 1 * 0.447 *1 * 5,290,000 = 2.84 KNm
        Mch = 4 * phi * kp * (math.sqrt(fmt)) * Zd
            = 4 * 0.6 * 1 * 0.447 * 5,290,000 = 5.68 KNm
        Mch = phi * (0.44 * fut * Zu + 0.56 * fmt * Zp)
            = 0.6 * (0.44 * 0.8MPa * 5,290,000 mm3 + 0.56 * 0.2MPa * 5,290,000 mm3)
            = 1.47 KNm

        phi = 0.6
        lesser of: Cl 7.4.3.4
            kp = Sp/tu = (230/2)/110 = 1.05
            kp = sp/hu = (230/3)/76 = 1.5
            kp = 1
        fmt = 0.2 MPa
        fut = 0.8 MPa Cl 3.2
        fd = 0
        Zd = (600) * 230**2 /6 = 5,290,000 mm3

        """

        wall = unreinforced_masonry.Clay(
            length=2000,
            height=600,
            thickness=230,
            fmt=0.2,
            fuc=20,
            mortar_class=4,
            bedding_type=True,
        )
        assert wall.horizontal_bending(fd=0, interface=True) == 1.47
