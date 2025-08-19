import math

import dataclasses

@dataclasses
class TimberBeam:
    length: float|None = None
    depth: float|None = None
    breadth: float|None = None
    φ_shear: float = 0.1
    φ_bending: float = 0.1
    φ_compression: float = 0.1
    fb: float| None = None
    

    

    def _bending(self, loads=[],seasoned=None, moisture_content=None,latitude = None, ncom=None, nmem = None, verbose=True):
        """
        Computes the bending capacity of a timber element using the methods
        described in AS 1720 Cl 3.2

        Args:
            loads: List of applied loads in kN.
            seasoned: True if seasoned timber is used and false otherwise.
            moisture_content: precentage moisture content, given as whole numbers, e.g. for 15% set as 15.
            latitude: True if located in coastal Queensland north of latitude 25 degrees south or 16 degrees south elsewhere, and False otherwise.
            verbose: If True, print internal calculation details.

        Returns:
            A dictionary with bending capacities for different durations related to the factor k1
        """

        k4 = self._calc_k4(seasoned=seasoned,moisture_content=moisture_content,verbose=verbose)
        k6 = self._calc_k6(latitude=latitude,verbose=verbose)
        k9 = 1
        k12 = 1
        Z = 1

        Md = self.φ_bending * k4 * k6 * k9 * k12 * fb * Z

    def in_plane_bending(self):
        pass

    def out_of_plane_bending(self):
        pass

    def _calc_k4(self,seasoned, moisture_content, verbose):
        """Computes k4 using AS1720.1-2010 Cl 2.4.2.2 & Cl 2.4.2.3"""
        if not seasoned:
            raise ValueError("seasoned not set, set to True if using seasoned timber, and False otherwise")
        elif verbose:
            print(f"seasoned: {seasoned}")
        
        if not moisture_content:
            raise ValueError("moisture_content not set, set to 15 if inside and 25 if outside. " \
            "Note: further investigation needed regarding moisture content values")
        elif verbose:
            print(f"moisture_content: {moisture_content} %")
        
        least_dim = min(self.length,self.breadth,self.depth)
        if seasoned:
            if moisture_content > 15:
                k4 = max(1-0.3 * (moisture_content - 15)/10, 0.7)
            else:
                k4 = 1
        else:
            if least_dim <= 38:
                k4 = 1.15
            elif least_dim < 50:
                k4 = 1.1
            elif least_dim < 75:
                k4 = 1.05
            else:
                k4 = 1
        if verbose:
            print(f"k4: {k4}, refer Table 2.5")
        return k4
    
    def _calc_k6(self, latitude, verbose):
        """Computes k6 using AS1720.1-2010 Cl 2.4.3"""
        if not latitude:
            raise ValueError("latitude not set, set to True if located in coastal Queensland " \
            "north of latitude 25 degrees south or 16 degrees south elsewhere, and False otherwise.")
        elif verbose:
            print(f"latitude: {latitude}")
        if latitude == True:
            k6 = 0.9
        elif latitude == False:
            k6 = 1
        if verbose:
            print(f"k6: {k6}, refer Cl 2.4.3")
        return k6

    def _calc_k9(self,ncom,nmem,verbose):
        """Computes k9 using AS1720.1-2010 Cl 2.4.5.3"""

        if not ncom:
            raise ValueError("")
        
        if not nmem:
            raise ValueError("")
        
        k9 = g31 + (g32 - g31)* (1 - 2*s/L)
        k9 = max(k9, 1)
        return k9