"""Contains tests for unreinforced clay masonry in horizontal shear"""

import pytest
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

    def test_standard_m3_brick_at_concrete_interface(self):
        """
        Think Brick Manual 15 Worked example 7 (modified)
        4m long x 2.7m high x 110mm thick masonry wall
        loaded with 50 KN/m dead load + 15 KN/m Live load
        fmt = 0 MPa (0 at non masonry interfaces)
        fms = 1.25 * fmt = 0.15 MPa
        Ad = 110 * 4000 = 440,000 mm2
        V0 = 0.6 * 0.15 * 440,000 = 39.6 KN
        kv = 0.3
        fd = 0.9 * (50,000) / (110 * 1000) = 0.41 MPa
        V1 = 0.3 * 0.41 * 440,000 = 54.12 KN
        Vd = 39.6 + 54.12 = 93.72 KN
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
        cap = wall.horizontal_plane_shear(kv=0.3, interface=False, fd=0.41)
        assert cap["friction"] == 54.12
        assert cap["bond"] == 39.6

    def test_fd_limited(self):
        """
        Consider a 3m long x 1m high x 230 thick masonry wall
        with fd = 2.5MPa
        fd limited to max of 2 MPa
        fmt = 0.2 MPa
        fms = 1.25 * fmt = 0.25 MPa
        Ad = 230 * 3000 = 690,000 mm2
        V0 = 0.6 * 0.25 * 690,000 = 103.5 KN
        kv = 0.3
        V1 = 0.3 * 2 * 690,000 = 414 KN
        Vd = 103.5 KN + 414 KN = 517.5
        """
        wall = Clay(
            length=3000,
            height=1000,
            thickness=230,
            fuc=20,
            mortar_class=3,
            bedding_type=True,
        )
        cap = wall.horizontal_plane_shear(kv=0.3, interface=True, fd=2.5)
        assert cap["bond"] == 103.5
        assert cap["friction"] == 414

    def test_kv_small(self):
        """
        Consider a 200mm long x 3000mm high x 90 thick wall at
        an interface with a slip joint 400mm from the base
        fd = 19KN/m3 * (3-0.4) = 0.0494 MPa
        fmt = 0 MPa (at slip joint)
        fms = 1.25 * fmt = 0 MPa but not less than 0.15 MPa
        fms = 0.15 MPa
        Ad = 90 * 200 = 18,000 mm2
        V0 = 0.6 * 0.15 * 18,000 = 1.62 KN
        kv = 0.1
        V1 = 0.1 * 0.0494 * 18,000 = 0.09 KN
        Vd = 1.62 KN + 0.09 KN = 1.71
        """
        wall = Clay(
            length=200,
            height=3000,
            thickness=90,
            fuc=10,
            mortar_class=3,
            bedding_type=True,
        )
        cap = wall.horizontal_plane_shear(
            kv=0.1, interface=False, fd=19 * (3 - 0.4) / 1000
        )
        assert cap["bond"] == 1.62
        assert cap["friction"] == 0.09

    def test_kv_zero(self):
        """
        Consider a 1000mm long x 2400mm high x 100 thick wall at an interface
        with a location not covered by AS3700.
        fd = 19KN/m3 * (2.4) = 0.0456 MPa
        fmt = 0 MPa (at other location)
        fms = 1.25 * fmt = 0 MPa but not less than 0.15 MPa
        fms = 0.15 MPa
        Ad = 100 * 1000 = 100,000 mm2
        V0 = 0.6 * 0.15 * 100,000 = 9 KN
        kv = 0 (At other locations)
        V1 = 0 * 0.0456 * 100,000 = 0 KN
        Vd = 9 KN + 0 KN = 9 KN
        """
        wall = Clay(
            length=1000,
            height=2400,
            thickness=100,
            fuc=10,
            mortar_class=3,
            bedding_type=True,
        )
        cap = wall.horizontal_plane_shear(kv=0, interface=False, fd=19 * (2.4) / 1000)
        assert cap["bond"] == 9
        assert cap["friction"] == 0

    def test_kv_large(self):
        """
        Entering a kv greater than 3 raises an error
        """
        with pytest.raises(ValueError):
            wall = Clay(
                length=1000,
                height=2400,
                thickness=100,
                fuc=10,
                mortar_class=3,
                bedding_type=True,
            )
            wall.horizontal_plane_shear(kv=0.31, interface=False, fd=19 * (2.4) / 1000)
