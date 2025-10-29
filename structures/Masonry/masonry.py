"""Contains methods for inheritance"""

import math
from structures.util import round_half_up


def calc_fm(
    self,
    km: float | None = None,
    verbose: bool = True,
):
    """Computes fm in accordance with AS3700 Cl 3."""

    if km is None:
        raise ValueError("km not set.")
    elif verbose:
        print(f"km: {km}")
    if self.hu is not None and self.tj is None:
        raise ValueError(
            "Masonry unit height provided but mortar thickness tj not provided"
        )
    elif self.hu is None and self.tj is not None:
        raise ValueError(
            "joint thickness tj provided but masonry unit height not provided"
        )

    kh = round_half_up(
        min(
            1.3 * (self.hu / (19 * self.tj)) ** 0.29,
            1.3,
        ),
        self.epsilon,
    )
    if verbose:
        print(
            f"kh: {kh}, based on a masonry unit height of {self.hu} mm"
            f" and a joint thickness of {self.tj} mm"
        )

    fmb = round_half_up(math.sqrt(self.fuc) * km, self.epsilon)
    if verbose:
        print(f"fmb: {fmb} MPa")

    self.fm = round_half_up(kh * fmb, self.epsilon)
    if verbose:
        print(f"fm: {self.fm} MPa")
