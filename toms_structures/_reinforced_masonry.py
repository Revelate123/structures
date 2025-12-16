# pylint: disable=too-many-lines
"""Contains methods for inheritance"""

from toms_structures._masonry import _Masonry
from toms_structures._util import round_half_up


class _ReinforcedMasonry(_Masonry):
    bedding_type = False

    def _reinforced_bending(
        self,
        d: float,
        b: float,
        area_tension_steel: float,
        fsy: float,
        verbose: bool = True,
    ):
        if verbose:
            print("Bending capacity, refer Cl 8.6 AS3700")
            print("=====================================")
        km = self._calc_km(verbose=verbose)
        self._calc_fm(km=km, verbose=verbose)
        if verbose:
            print(f"fsy: {fsy:.2f} MPa")

        if verbose:
            print(f"d: {d:.2f} mm")

        if verbose:
            print(f"area_tension_steel: {area_tension_steel:.2f} mm2")
            print(
                f"Minimum quantity of secondary reinforcement: {0.00035*d * b:.2f} mm2, Cl 8.4.3"
            )

        if verbose:
            print(f"b: {b:.2f} mm")

        # Step 1: Calculate effective_area_tension_steel
        effective_area_tension_steel = min(
            area_tension_steel, (0.29 * 1.3 * self.fm * self.length * d) / fsy
        )
        if verbose is True:
            print(
                f"effective_area_tension_steel: {effective_area_tension_steel:.2f} mm2"
            )

        # Step 2: Calculate moment_cap
        moment_cap = round_half_up(
            self.phi_bending
            * fsy
            * effective_area_tension_steel
            * d
            * (
                1
                - (0.6 * fsy * effective_area_tension_steel)
                / (1.3 * self.fm * self.length * d)
            )
            * 1e-6,
            self.epsilon,
        )
        if verbose is True:
            print(f"moment_cap: {moment_cap:.2f} KNm")
        return moment_cap
