#import sympy
import math
from dataclasses import dataclass

from sectionproperties.pre.library import concrete_rectangular_section
from concreteproperties import (
    BilinearStressStrain,
    ConcreteSection,
    EurocodeParabolicUltimate,
    RectangularStressBlock,
)
from concreteproperties.design_codes import AS3600
from concreteproperties.post import si_kn_m, si_n_mm
from concreteproperties.results import BiaxialBendingResults, MomentInteractionResults

@dataclass
class ConcreteBeam:
    fc:float = 32
        
@dataclass
class OneWaySlab(ConcreteBeam):
    """
    Constructs an object used for calculating one way slab properties

    Args:
        Lx: 
        Ly:
     
    """
    Lx:float|None = None
    Ly:float|None = None


@dataclass
class ConcreteBeam_depracated:
    fc:float = 32
    b:float = 1000
    cover:float = 65
    fy:float = 500
    Ec:float = 30*10**9
    length:float = 1000
    depth:float = 0
    Ast = [12**2/4*math.pi/0.15]
    d = [100/2]
    def unfactored_moment(self):
        """This function calculates the unfactored moment capacity of a rectangular concrete section. It Assumes the maximum strain of 0.003 is reached by the extreme compressive edge.
        fc in MPa
        breadth, b in mm
        depth, d is a list of reinforcement depths in mm
        Ast is a list of reinforcement quantities in mm2 corresponding to each depth, d.
        fy in MPa"""
        alpha_2 = max(0.67, 0.85 - 0.0015*self.fc)
        print(f"\u0391_2 = {alpha_2}")
        gamma = max(0.67, 0.97 - 0.0025*self.fc)
        print(f"\u0393 = {gamma}")
        dn = 0.85*max(self.d)
        Cc = alpha_2*self.fc*self.b*gamma*dn
        steel_strains = [0 for i in self.Ast]
        force_equilibrium = Cc - sum([self.Ast[i]*steel_strains[i]*200*10**3 for i in range(len(self.Ast))])
        #Repeat calculation until force equilibrium satisfied for given nuetral axis depth, dn
        while round(force_equilibrium) != 0:
            for i in range(len(self.Ast)):
                steel_strains[i] = min(max(-self.fy/(200*10**3),(dn - self.d[i])*0.003/(dn)),self.fy/(200*10**3))
            if force_equilibrium > 0:
                #increase dn
                dn *=0.99
            else:
                #decrease dn
                dn *=1.01
            Cc = alpha_2*self.fc*self.b*gamma*dn
            force_equilibrium = Cc + sum([self.Ast[i]*steel_strains[i]*200*10**3 for i in range(len(self.Ast))])

        if (dn - max(self.d))*0.003/dn > -self.fy/(200*10**3):
            print("steel not yielding")
        print(dn,"mm")
        Mu = Cc *(dn - 0.5*gamma*dn)*10**-6 + sum([abs(self.Ast[i]*steel_strains[i]*200*10**-3*(self.d[i] - dn)) for i in range(len(self.Ast))])
        return Mu, dn 

    def shear(fc,bv,d, D,Ast,Ec,M,V,N):
        dv = max(0.9*d, 0.72*D)
        dg = 20
        kdg = (32/(16+dg))
        ex = min((abs(M/dv)*10**6 + abs(V)*10**3 + 0.5*N*10**3)/(2*200*10**9*Ast*10**-6),3*10**-3)
        kv = (0.4/(1 + 1500*ex))*(1300/(1000 + kdg*dv))
        Vuc = kv * math.sqrt(fc) * bv * dv
        return Vuc*10**-3

if __name__ == "__main__":
    beam = ConcreteBeam()
    Mn, dn = beam.unfactored_moment() 
    print("Mn", 0.6*Mn, "dn",dn)
    #print(shear(fc,b,d[1],d[1]+cover+6,Ast[0],Ec,18,36,0))
    #intro_durability()