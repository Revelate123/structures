"""Contains tests for unreinforced hollow concrete masonry in two way bending"""

from toms_structures.unreinforced_masonry import HollowConcrete


class TestUnreinforcedDiagonalBending:
    """Tests for diagonal bending capacity, in accordance with AS3700:2018 Cl 7.4.3.3"""

    def test_b_greater_t(self):
        pass

    def test_b_less_t(self):
        pass

    def test_hollow(self):
        pass

class TestUnreinforcedMasonryTwoWayBending:
    """Tests"""

    def test_think_brick_example(self):
        """
        Design a wall panel 4 m long and 3 m high with simple supports on all four
        sides for an applied lateral load of 1.0 kPa.
        """
        wall = HollowConcrete(
            length=4000,
            height=3000,
            thickness=110,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        cap = wall.two_way_bending(
            vert_supports=2,
            top_support=True,
            rot_rest_1=0,
            rot_rest_2=0,
            fd=0,
            verbose=True,
        )
        #assert cap == 1.11
