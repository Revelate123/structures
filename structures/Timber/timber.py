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
    

    def __post_init__(self):
        self.Zxx = self.breadth*self.depth**2/6
        self.Zyy = self.depth*self.breadth**2/6

    def _bending(self, loads=[],seasoned=None, moisture_content=None,latitude = None, ncom=None, nmem = None, spacing = None, span = None, verbose=True):
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
        k9 = self._calc_k9(ncom=ncom, nmem=nmem,spacing=spacing,span=span)
        k12 = 1
        Z = 1

        Md = self.φ_bending * k4 * k6 * k9 * k12 * self.fb * Z
        if verbose == True:
            print(f"Md: {Md} KNm")
        return Md

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

    def _calc_k9(self,ncom,nmem,spacing,span,verbose):
        """Computes k9 using AS1720.1-2010 Cl 2.4.5.3"""

        if not ncom:
            raise ValueError("ncom not set, this is the number of elements that are effectively fastened together to form a single group")
        elif verbose:
            print(f"ncom: {ncom}, number of members per group")
        
        if not nmem:
            raise ValueError("nmem not set, this is the number of members that are discretely spaced parallel to each other")
        elif verbose:
            print(f"nmem: {nmem}, number of groups of members")
        
        if nmem > 1 and not spacing:
            raise ValueError("nmem greater than 1 but spacing between groups not set. This should be in mm.")
        elif verbose:
            print(f"spacing: {spacing} mm")
        
        if nmem > 1 and not span:
            raise ValueError("nmem greater than 1 but span of members not set. This should be in mm.")
        elif verbose:
            print(f"span: {span} mm")

        table_2_7 = [0,1,1.14,1.2,1.24,1.26,1.28,1.3,1.31,1.32,1.33]

        g31 = table_2_7[ncom if ncom < 10 else 10]
        if verbose:
            print(f"g31: {g31}")
        g32 = table_2_7[ncom*nmem if ncom*nmem < 10 else 10]
        if verbose:
            print(f"g32: {g32}")
        k9 = g31 + (g32 - g31)* (1 - 2*spacing/span)
        k9 = max(k9, 1)
        if verbose:
            print(f"k9: {k9}")
        return k9
    
    def _calc_k12(self, pb:float|None = None, verbose:bool = True):
        """Computes k12 using AS1720.1-2010 Cl """
        if not pb:
            raise ValueError("pb not defined")
        elif verbose:
            print(f"pb: {pb}")

        S1
