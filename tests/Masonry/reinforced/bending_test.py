"""Contains tests for reinforced block masonry in bending"""

from structures.Masonry.reinforced_masonry import Block


class TestOutOfPlaneVerticalBending:
    """Tests for vertical bending in accordance with 7.4.2"""

    def test_lightly_reinforced_wall(self):
        """
        b = 1000
        d = 190/2 = 95
        fsy = 500 MPa
        Ast = 113/0.4 = 282.5 mm2 (N12's at 400 centres)
        fm = sqrt(15) * 1.6 * 1.3 = 8.06 MPa
        Asd = (0.29)*1.3*fm*b*d/fsy
            = (0.29)*1.3*8.06*1000*95/500
            = 577.3 mm2
        Asd = 282.5 mm2
        phi = 0.75
        Md = phi * fsy * Asd * d * (1 - (0.6 * fsy * Asd)/(1.3 * fm * b * d))
            = 0.75 * 500 * 282.5 * 95 * (1 - (0.6 * 500 * 282.5)/(1.3 * 8.06 * 1000 * 95)) * 10^-6
            = 9.21 KNm
        """
        wall = Block(
            length=1000,
            height=6000,
            thickness=190,
            mortar_class=3,
            fuc=15,
        )
        assert (
            wall.out_of_plane_vertical_bending(
                d=95, area_tension_steel=113 / 0.4, fsy=500
            )
            == 9.21
        )

    def test_heavily_reinforced_wall(self):
        """
        b = 1000
        d = 290-40-15-20/2 = 225
        fsy = 500 MPa
        Ast = 314/0.2 = 1570 mm2 (N20's at 200 centres)
        fm = sqrt(15) * 1.6 * 1.3 = 8.06 MPa
        Asd = (0.29)*1.3*fm*b*d/fsy
            = (0.29)*1.3*8.06*1000*225/500
            = 1367.38 mm2
        Asd = 1367.38 mm2
        phi = 0.75
        Md = phi * fsy * Asd * d * (1 - (0.6 * fsy * Asd)/(1.3 * fm * b * d))
        = 0.75 * 500 * 1367.38 * 225 * (1 - (0.6 * 500 * 1367.38)/(1.3 * 8.06 * 1000 * 225)) * 10^-6
        = 95.30 KNm
        """
        wall = Block(
            length=1000,
            height=6000,
            thickness=290,
            mortar_class=3,
            fuc=15,
        )
        assert (
            wall.out_of_plane_vertical_bending(
                d=290 - 40 - 15 - 20 / 2, area_tension_steel=314 / 0.2, fsy=500
            )
            == 95.3
        )
