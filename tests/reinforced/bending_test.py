"""Contains tests for reinforced HollowConcrete masonry in bending"""

from toms_structures.reinforced_masonry import HollowConcrete


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
        wall = HollowConcrete(
            length=1000,
            height=6000,
            thickness=190,
            mortar_class=3,
            fuc=15,
        )
        assert (
            wall.out_of_plane_vertical_bending(
                d=95, area_tension_steel=113 / 0.4, fsy=500, fd=0, interface=True
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
        wall = HollowConcrete(
            length=1000,
            height=6000,
            thickness=290,
            mortar_class=3,
            fuc=15,
        )
        assert (
            wall.out_of_plane_vertical_bending(
                d=290 - 40 - 15 - 20 / 2,
                area_tension_steel=314 / 0.2,
                fsy=500,
                fd=0,
                interface=True,
            )
            == 95.3
        )

    def test_capacity_less_than_unreinforced(self):
        """As per Cl 8.6(a) Md must exceed 1.2 times the unreinforced capacity
        This is likely to occur for a wide but lighlty reinforced wall with a compressive force applied.
        Consider a 290 wide HollowConcrete wall with 1/N10 every 400mm placed central.

        b = 1000
        d = 290/2 = 145
        fsy = 500 MPa
        Ast = 78.5/0.4 = 196.35 mm2 (N10's at 400 centres)
        fm = sqrt(15) * 1.6 * 1.3 = 8.06 MPa
        Asd = (0.29)*1.3*fm*b*d/fsy
            = (0.29)*1.3*8.06*1000*145/500
            = 881.2 mm2
        Asd = 196.35 mm2
        phi = 0.75
        Md = phi * fsy * Asd * d * (1 - (0.6 * fsy * Asd)/(1.3 * fm * b * d))
        = 0.75 * 500 * 196.35 * 145 * (1 - (0.6 * 500 * 196.35)/(1.3 * 8.06 * 1000 * 145)) * 10^-6
        = 10.26 KNm

        """
        wall = HollowConcrete(
            length=1000,
            height=2000,
            thickness=290,
            mortar_class=3,
            fuc=15,
        )
        assert (
            wall.out_of_plane_vertical_bending(
                d=290 / 2, area_tension_steel=78.5 / 0.4, fsy=500, fd=0, interface=True
            )
            == 10.26
        )
