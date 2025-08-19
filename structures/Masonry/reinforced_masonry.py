import math
from dataclasses import dataclass
import structures.Masonry.masonry as masonry
from structures import __version__

@dataclass
class ReinforcedMasonry(masonry.Masonry):
    hu: float = 200
    tj: float = 10
    tu: float = 190
    lu: float = 400
    φ_shear: float = 0.75
    φ_bending: float = 0.75
    φ_compression: float = 0.75


    def _bending(self, loads=[], fsy = None, d = None, Ast = None, b = None, verbose = True):
        """
        Computes the bending capacity of a reinforced masonry wall element using the methods
        described in AS 3700 Cl 8.6.

        Args:
            loads: List of applied loads in kN.
            fsy: the design yield strength of reinforcement (refer Cl 3.6.1)
            d: the effective depth of the reinforced masonry member.
            Ast: the cross-sectional area of fully anchored longitudinal reinforcement in the tension zone of the cross-section under consideration.
            verbose: If True, print internal calculation details.

        Returns:
            A dictionary with bending capacity
        """
        if fsy == None:
            raise ValueError("fsy not set, this is the design yield strength of reinforcement (refer Cl 3.6.1) and is typically 500MPa for N grade bars")
        elif verbose:
            print(f"fsy: {fsy:.2f} MPa")

        if d == None:
            raise ValueError("d not set, this is the effective depth of the reinforced masonry member from the extreme compressive fibre of the masonry " \
            "to the resultant tensile force in the steel in the tensile zone, typical values are 95 for 190 block walls")
        elif verbose:
            print(f"d: {d:.2f} mm")

        if Ast == None:
            raise ValueError("Ast not set, this is the quanity of tensile steel. Note: the amount of steel used in calculation is limited to Asd")
        elif verbose:
            print(f"Ast: {Ast:.2f} mm2")

        if b == None:
            raise ValueError("b is not set, this is the breadth of the masonry member used for calculation, and depends on the direction of bending considered.")
        elif verbose:
            print(f"b: {b:.2f} mm")
        
        #Step 1: Calculate Asd
        Asd = min(Ast, (0.29 * 1.3 * self.fm * self.length * d)/fsy)
        if verbose == True:
            print(f"Asd: {Asd:.2f} mm2")

        #Step 2: Calculate Md
        Md = self.φ_bending * fsy * Asd * d * (1 - (0.6 * fsy * Asd)/(1.3*self.fm*self.length*d)) * 1e-6
        if verbose == True:
            print(f"Md: {Md:.2f} KNm")

    def vertical_bending(self, loads=[], fsy = None, d = None, Ast = None, verbose = True):
        Md = self._bending(loads=loads, fsy=fsy, d=d, Ast=Ast, b=self.length, verbose=verbose)
        return Md
    
    def horizontal_bending(self, loads=[], fsy = None, d = None, Ast = None, verbose = True):
        Md = self._bending(loads=loads, fsy=fsy, d=d, Ast=Ast, b=self.height, verbose=verbose)
        return Md