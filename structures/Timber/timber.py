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

    def _bending(self,
                  loads=[],
                  seasoned=None,
                    moisture_content=None,
                    latitude = None,
                      ncom=None,
                        nmem = None,
                          spacing = None,
                            span = None,
                              out_of_plane:bool|None = None,
                              pb:float|None =None,
                              restraint_location:int|None = None,
                              Lay:float|None = None,
                                Z:float|None = None,
                                verbose=True):
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
        k12 = self._calc_k12(pb=pb,restraint_location=restraint_location,Lay=Lay,out_of_plane=out_of_plane,verbose=verbose) 
        Z = self._calc_Z(out_of_plane=out_of_plane)

        Md = self.φ_bending * k4 * k6 * k9 * k12 * self.fb * Z
        if verbose == True:
            print(f"Md: {Md} KNm")
        return Md

    def in_plane_bending(self,
                  loads=[],
                  seasoned=None,
                    moisture_content=None,
                    latitude = None,
                      ncom=None,
                        nmem = None,
                          spacing = None,
                            span = None,
                              out_of_plane:bool|None = None,
                              pb:float|None =None,
                              restraint_location:int|None = None,
                              Lay:float|None = None,
                                Z:float|None = None,
                                verbose=True):
        return self._bending(loads=loads,seasoned=seasoned,moisture_content=moisture_content,latitude=latitude,ncom=ncom,nmem=nmem,spacing=spacing,span=span,
                             pb=pb, restraint_location=restraint_location,Lay=Lay,Z=Z,
                             out_of_plane=False if self.depth > self.breadth else True,
                             verbose=verbose)

    def out_of_plane_bending(self,
                  loads=[],
                  seasoned=None,
                    moisture_content=None,
                    latitude = None,
                      ncom=None,
                        nmem = None,
                          spacing = None,
                            span = None,
                              out_of_plane:bool|None = None,
                              pb:float|None =None,
                              restraint_location:int|None = None,
                              Lay:float|None = None,
                                Z:float|None = None,
                                verbose=True):

        return self._bending(loads=loads,seasoned=seasoned,moisture_content=moisture_content,latitude=latitude,ncom=ncom,nmem=nmem,spacing=spacing,span=span,
                             pb=pb, restraint_location=restraint_location,Lay=Lay,Z=Z,
                             out_of_plane=True if self.depth > self.breadth else False,
                             verbose=verbose)

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
    
    def _calc_k12(self, pb:float|None = None, restraint_location:int|None=None, Lay:float|None = None, fly_brace_spacing:int|None = None,out_of_plane:bool|None = None, verbose:bool = True):
        """Computes k12 using AS1720.1-2010 Cl """
        if not pb:
            raise ValueError("pb not defined")
        elif verbose:
            print(f"pb: {pb}")
        
        if out_of_plane is None:
            raise ValueError("out_of_plane not set. Set to True if out of plane")
        elif out_of_plane == True:
            return 1

        if restraint_location is None or restraint_location not in [1,2,3]:
            raise ValueError("restraint_location not set or set incorrectly.\n" \
            "set to 1 if restraints are to the compression edge\n" \
            "set to 2 if restraints are to the tension edge\n" \
            "set to 3 if restraints are to the tension edge and there is fly-bracing to the compression edge\n"
            "If unsure, setting to 2 is conservative") #TODO confirm
        elif verbose:
            print(f"restraint_location: {restraint_location}")
        
        if Lay is None:
            raise ValueError("Lay not set. This is the distance between restraints.\n" \
            "For continuous systems e.g. flooring, set to the nail spacing e.g 300mm\n" \
            "For fly-bracing systems it is NOT the distance between fly-braces.")
        elif verbose:
            print(f"Lay: {Lay} mm")
        
        if restraint_location == 3 and fly_brace_spacing is None:
            raise ValueError("restraint_location set to 3 but fly-brace spacing has not been set. This should be the number of members in the group"
            "[L,R), for example, if there are fly braces to every purlin," \
            " then fly_brace_spacing should be set to 1, if they alternate every 2nd purlin, it should be set to 2, etc.")
        elif verbose:
            if fly_brace_spacing == 1:
                print("fly braces connected to every restraint")
            elif fly_brace_spacing > 1:
                print(f"fly bracing to every {fly_brace_spacing} restraints")
            
        cont_restrained = self._cont_restraint(pb=pb,Lay=Lay,verbose=verbose)
        return self._calc_S1(pb=pb,restraint_location=restraint_location,Lay=Lay,fly_brace_spacing=fly_brace_spacing,cont_restrained=cont_restrained,verbose=verbose)
        

    def _calc_S1(self,pb:float|None = None, restraint_location:int|None=None, Lay:float|None = None, fly_brace_spacing:int|None = None,cont_restrained:bool = False, verbose:bool = True):
        """ Calculates the beam slenderness S1 """
        if cont_restrained == True:
            if restraint_location == 1:
                return 0
            if restraint_location == 2:
                return 2.25*self.depth/self.breadth
            if restraint_location == 3:
                return (1.5 * self.depth/self.breadth) / ((math.pi*self.depth/fly_brace_spacing*Lay)**2+0.4)**0.5
        else:
            if restraint_location == 1:
                return 1.25*self.depth/self.breadth*(Lay/self.d)**0.5
            if restraint_location == 2 or restraint_location == 3:
                return (self.depth/self.breadth)**1.35 * (Lay/self.depth)**0.25
        raise ValueError("_calc_S1 did not find a matching restraint case")
        

    def _cont_restraint(self,pb:float|None = None,  Lay:float|None = None, verbose:bool = True):
        """ Determines if the beam is continuously restrained """
        cont_restrained = Lay/self.depth <= 64*(self.breadth/(pb*self.depth))**2
        if verbose:
            print(f"Continuously restrained: {cont_restrained}")
        return cont_restrained

        
    def _calc_Z(self, out_of_plane):
        if out_of_plane is None:
            raise ValueError("out_of_plane not set.")
        if out_of_plane == True:
            return self.depth*self.breadth**2/6
        elif out_of_plane == False:
            return self.breadth*self.depth**2/6
        else:
            raise ValueError("error in _calc_Z")
