import pytest
import structures.Timber.timber as timber


class TestInPlaneBending:
    def test_slender_beam(self):
        """
        Md =
        """
        beam = timber.Beam(length=1000, depth=240, breadth=90, fb=12, phi_bending=0.7)
        assert (
            beam.in_plane_bending(
                seasoned=True,
                moisture_content=15,
                latitude=False,
                ncom=1,
                nmem=1,
                pb=1,
                restraint_location=1,
                Lay=1000,
            )
            is not None
        )

    def test_stocky_beam(self):
        pass

    def test_width_greater_than_height(self):
        pass

    def test_long_span(self):
        pass

    def test_compression_flange_restraints(self):
        pass

    def test_tension_flange_restraints(self):
        pass

    def test_ncom_5(self):
        pass

    def test_nmem_ncom_4(self):
        pass

    def test_continually_restrained(self):
        pass
