import pytest
import structures.Timber.timber as timber


class TestInPlaneBending:
    def test_slender_beam(self):
        """
        Md =
        """
        beam = timber.Beam()
        assert 1 == 2

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
