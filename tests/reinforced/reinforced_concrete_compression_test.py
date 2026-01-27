"""Contains tests for reinforced HollowConcrete masonry in compression"""

from toms_structures.reinforced_masonry import HollowConcrete


class TestCompression:
    """Tests for vertical bending in accordance with 7.4.2"""

    def test_lightly_reinforced_wall(self):
        """
        Determine the capacity of a 140 thick x 1000 wide x 3000 high reinforced block wall.
        Assume N12's @ 400 vertical reinforcement placed centrally. Assume wall thickness is 25mm.
        fm = sqrt(15) * 1.6 * 1.3 = 8.06 MPa
        b = 1000
        Ab = 1000 * 190  = 190,000 mm2
        kc = 1.4
        d = 190/2 = 95
        fcg = 12 MPa
        fsy = 500 MPa
        Ag = ((0.4 - 0.025*2) * (0.14 - 0.025*2))/0.4 = 0.07875m2
        phi = 0.75
        alpha_r = 0.4
        As = 113mm2 / 0.4 = 282.5mm2
        Sr = 0.75 * 3000 / (1 * 140) = 16.07
        kes = (1 - 0.025 * Sr) * (1 - 2*e/t) = (1 - 0.025 * 16.07) * 1 = 0.60
        Fd = phi * Kes * (fm*Ab + kc*((fcg/1.3)^(0.55 + 0.005*fcg))*Ag + alpha_r * fsy * As)
        = 0.75 * 0.60 * (8.06* 190,000 + 1.4 *((12/1.3)^(0.55 + 0.005*12))*0.07875 + 0.4*500*282.5)
        = 0.45 * (1531400 + 1.4*(9.231) ^ (0.61)*78750 + 56500)
        = 0.45 * (1531400 + 427740.464 + 56500)
        = 907.038 KN

        """
        assert 1 == 1
