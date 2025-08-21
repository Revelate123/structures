import math
import dataclasses

@dataclasses
class Surface:
    length: float|None = None
    width: float|None = None


class AttachedAwning(Surface):
    """For wind calculation of attached canopies, awnings, and carports based on AS1170.2 Cl B.4"""
    def __init__(self, base_pressure:dict|None = None, slope:float|None = None, roof_height:float|None = None, awning_height:float|None = None, verbose:bool = True):
        if base_pressure == None:
            raise ValueError("base_pressure not provided, this should be provided in the form {\"N\":0.8,\"NE\":0.65...} where values are in KPa")
        elif verbose:
            print(f"base_pressure: {base_pressure}, in KPa")

        if slope == None:
            raise ValueError("slope not set, this should be provided in degrees and is the angle from horizontal")
        elif slope > 10 or slope < 0:
            raise ValueError("slope outside of range 0 - 10 degrees. For an awning outside of this range, a different AS1170.2 clause must be used.")
        elif verbose:
            print(f"slope: {slope} degrees")
        
        if roof_height == None:
            raise ValueError("roof_height not set, this is the average roof height of the structure the awning is attached to in metres")
        elif verbose:
            print(f"roof height: {roof_height} m")
        
        if awning_height == None:
            raise ValueError("awning_height not set, this is the average height of the awning in metres")
        elif verbose:
            print(f"awning height: {awning_height} m")
        
        if awning_height > roof_height:
            raise ValueError("awning_height cannot be greater than roof_height")
        
        



    def calculate(self):
        """ 
        Calculates all wind pressures acting on the awning
     
        Args:
            
            verbose: If True, print internal calculation details.

        Returns:
            void
        """



