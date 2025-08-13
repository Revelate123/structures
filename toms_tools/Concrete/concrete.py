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

class ConcreteBeam2:
    def __init__(self,fc):
        self.design_code = AS3600()
        self.concrete = self.design_code.create_concrete_material(compressive_strength=fc)
        self.steel = self.design_code.create_steel_material()
        print(self.concrete. name)
        print(f"Density = {self.concrete. density} kg/mm^3")
        self.concrete. stress_strain_profile.plot_stress_strain(
            title="Service Profile", eng=True, units=si_n_mm
        )
        self.concrete. ultimate_stress_strain_profile.plot_stress_strain(
            title="Ultimate Profile", eng=True, units=si_n_mm
        )
        print(
            f"Concrete Flexural Tensile Strength: {self.concrete. flexural_tensile_strength:.2f} MPa"
        )

@dataclass
class ConcreteBeam:
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

    def display_Table():
        width = 80
        print("+","-"*(width-2),"+",sep="")
        print('|',f"{'Surface of members in contact with the ground': <{width-2}}",'|',sep= '')
        print("+","-"*9,"+","-"*(width-12),"+",sep="")
        print('|','{0: ^9}'.format("0"),'|',f'{"Members protected by a damp-proof membrane": ^{width-12}}','|', sep= '')
        print("+","-"*9,"+","-"*(width-12),"+",sep="")
        print('|','{0: ^9}'.format("1"),'|',f'{"Residential footings in non-aggressive soils": ^{width-12}}','|', sep= '')
        print("+","-"*9,"+","-"*(width-12),"+",sep="")
        print('|','{0: ^9}'.format("2"),'|',f'{"Other members in non-aggressive soils": ^{width-12}}','|', sep= '')
        print("+","-"*9,"+","-"*(width-12),"+",sep="")


    def durability():
        member = {}
        T4_3 = ["A1","A1", "A2", "Table 4.8.1", "U", "U", "Table 4.8.2","A1", "A2", "B1", "A1", "A2", "B1", "B1", "B1", "B2", "B1", "U", "B2", "C1", "C2", "U"]
        while True:

            classification = input("Input the index of the member classification from the table above:")
            if classification.isdigit():
                #add from the table
                #member["fc"] = 
                pass
            else:
                    pass

    def intro_durability():
        #User will input each type of member and it will generate a table of the cover requirements
        display_Table()
        members = []
        while True:
            cur_member = input("Input name of member type or type a number to overwrite an existing row:")
            if cur_member.isdigit():
                if int(cur_member) > len(members):
                    print("Index does not exist")
                else:
                    #Overwrite
                    members[int(cur_member)] 
            elif cur_member != "":
                #logic to determine cover and fc etc.
                members += durability()
            else:
                #proceed to next step
                break


if __name__ == "__main__":
    beam = ConcreteBeam()
    Mn, dn = beam.unfactored_moment() 
    print("Mn", 0.6*Mn, "dn",dn)
    #print(shear(fc,b,d[1],d[1]+cover+6,Ast[0],Ec,18,36,0))
    #intro_durability()