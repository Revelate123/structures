"""Contains tests for unreinforced clay masonry in horizontal shear"""

from structures.Masonry.unreinforced_masonry import Clay


class TestHorizontalShear:
    """Tests for the Basic compressive capacity, in accordance with AS3700 Cl 7.3.2"""

    def test_standard_m3_brick(self):
        """
        Think Brick Manual 15 Worked example 7
        4m long x 2.7m high x 110mm thick masonry wall
        loaded with 50 KN/m dead load + 15 KN/m Live load
        fmt = 0.2 MPa
        fms = 1.25 * fmt = 0.25 MPa
        Ad = 110 * 4000 = 440,000 mm2
        V0 = 0.6 * 0.25 * 440,000 = 66 KN
        kv = 0.3
        fd = 0.9 * (50,000) / (110 * 1000) = 0.41 MPa
        V1 = 0.3 * 0.41 * 440,000 = 54.12 KN
        Vd = 66 + 54.12 = 120.12 KN
        """
        wall = Clay(
            length=4000,
            height=2700,
            thickness=110,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
            fmt=0.2,
        )
        cap = wall.horizontal_plane_shear(kv=0.3, interface=True, fd=0.41)
        assert cap["friction"] == 54.12
        assert cap["bond"] == 66

    def test_fd_limited(self):
        """"""
        pass
