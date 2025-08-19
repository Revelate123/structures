import math
import structures.Masonry.unreinforced_masonry as unreinforced_masonry
import Concrete.concrete as concrete

class RetainingWall:
    def __init__(self,  footing_length, footing_depth, heel, wall_thickness, wall_height, soil_density = 18, ka = 0.41, kp = 2.4):

        self.wall = unreinforced_masonry.ReinforcedMasonry(thickness = wall_thickness, height = wall_height, length = 1000)
        self.footing = concrete.ConcreteBeam(length = footing_length, depth = footing_depth)
        self.footing_length = footing_length
        self.footing_toe_incl_wall = footing_length - heel
        self.footing_heel = heel
        self.wall_thickness = wall_thickness
        self.soil_density = soil_density
        self.ka = ka
        self.kp = kp

    def overturning(self, Dimensions, density_concrete, density_soil, surcharge, Additional_moment, Ka,
                values):
        # Unfactored soil force
        PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) ** 2 * 10 ** -6
        # Unfactored surcharge force
        PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) * 10 ** -3

        # 1.25G + 1.5Q
        factored_overturning_moment = 1.25 * PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + 1.5 * PA2 * (
                Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment
        
        restoring_moment = 0

        # Moment from self-weight of wall
        wall_moment = self.wall.self_weight() * (self.footing_toe_incl_wall - self.wall_thickness/2)

        # Moment from self-weight of footing
        restoring_moment += (Dimensions['Ltoe'] + Dimensions['Lheel']) * Dimensions['D'] * density_concrete * ( \
                        Dimensions['Ltoe'] + Dimensions['Lheel']) / 2 * 10 ** -9
        
        # Moment from self-weight of soil over heel
        restoring_moment +=  Dimensions['Lheel'] * Dimensions['H'] * density_soil * ( \
                        Dimensions['Ltoe'] + Dimensions['Lheel'] / 2) * 10 ** -9
        
        # Moment from self weight of shear key
        restoring_moment += Dimensions['SW'] * Dimensions[
                'SD'] * density_concrete * (Dimensions['SKD'] + Dimensions['SW'] / 2) * 10 ** -9

        # Moment from surcharge over heel, magic number 0.4 is probably long term live load factor = 0.4
        restoring_moment += surcharge * Dimensions['Lheel'] * (Dimensions['Ltoe'] + Dimensions['Lheel'] / 2) * 0.4 * 10 ** -6

        # Moment from additional load at top of wall
        restoring_moment += values['Additional_load'] * (Dimensions['Ltoe'] - Dimensions['tw'] / 2) * 10 ** -3
            
        return 0.9 * restoring_moment - factored_overturning_moment

    def bearing(Dimensions, allowable_end_pressure, density_concrete, density_soil, surcharge, Additional_moment, Ka,
                Internal_friction, c, Kp, values, Top_restraint, Restraint_height):
        PA1 = 0.5 * Ka * density_soil * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) ** 2 * 10 ** -6

        PA2 = Ka * surcharge * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) * 10 ** -3

        values['Additional_load'] = float(values['Additional_load'])

        values['Overburden'] = float(values['Overburden'])

        N = density_concrete * Dimensions['H'] * Dimensions['tw'] * 10 ** -6 + (Dimensions['Ltoe']
                                                                                + Dimensions['Lheel']) * Dimensions[
                'D'] * density_concrete * 10 ** -6 \
            + Dimensions['Lheel'] * Dimensions['H'] * density_soil * 10 ** -6 + surcharge * Dimensions['Lheel'] * 10 ** -3 \
            + Dimensions['SW'] * Dimensions['SD'] * density_concrete * 10 ** -6 + values['Additional_load'] + values[
                'Overburden'] * density_soil * (Dimensions['Ltoe'] - Dimensions['tw']) * 10 ** -6

        centroid_N = (density_concrete * Dimensions['H'] * Dimensions['tw'] * 10 ** -6 * (
                Dimensions['Ltoe'] - Dimensions['tw'] / 2) + (Dimensions['Ltoe']
                                                            + Dimensions['Lheel']) * Dimensions[
                        'D'] * density_concrete * 10 ** -6 * (Dimensions['Ltoe'] + Dimensions['Lheel']) / 2
                    + Dimensions['Lheel'] * Dimensions['H'] * density_soil * 10 ** -6 * (
                            Dimensions['Ltoe'] + 0.5 * Dimensions['Lheel']) + surcharge * Dimensions[
                        'Lheel'] * 10 ** -3 * (Dimensions['Ltoe'] + 0.5 * Dimensions['Lheel'])
                    + Dimensions['SW'] * Dimensions['SD'] * density_concrete * 10 ** -6 * (Dimensions['SKD'] / 2)
                    + values['Additional_load'] * (Dimensions['Ltoe'] - Dimensions['tw'] / 2) + values[
                        'Overburden'] * density_soil * (Dimensions['Ltoe'] - Dimensions['tw']) ** 2 / 2 * 10 ** -6) / N

        Moment = PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + PA2 * (
                Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment

        x = Moment / N

        a = 3 * (centroid_N * 10 ** -3 - x)

        if a < (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3 and x < centroid_N * 10 ** -3:
            qmax = 2 * N / a
        elif a > (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3:
            M = -N * (centroid_N - Dimensions['Ltoe'] / 2 - Dimensions['Lheel'] / 2) * 10 ** -3 \
                + Moment
            qmax = N / ((Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) + 6 * M / (
                    (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) ** 2
            a = (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3
        elif x > centroid_N * 10 ** -3:
            qmax = 'INCREASE LENGTH'
        Moment = 1.25 * PA1 * (Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 3 * 10 ** -3 + 1.5 * PA2 * (
                Dimensions['H'] + Dimensions['D'] + Dimensions['h']) / 2 * 10 ** -3 + Additional_moment
        x_ULS = Moment / N
        a_ULS = 3 * (centroid_N * 10 ** -3 - x_ULS)
        if a_ULS < (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3 and x_ULS < centroid_N * 10 ** -3:
            qmax_ULS = 2 * N / a_ULS
        elif a_ULS > (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3:
            M1 = -N * (centroid_N - Dimensions['Ltoe'] / 2 - Dimensions['Lheel'] / 2) * 10 ** -3 \
                + Moment
            qmax_ULS = N / ((Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) + 6 * M1 / (
                    (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3) ** 2
            a_ULS = (Dimensions['Ltoe'] + Dimensions['Lheel']) * 10 ** -3
        elif x_ULS > centroid_N * 10 ** -3:
            qmax_ULS = 10
            a_ULS = 10000

        print('Auls', a_ULS, PA1, PA2, qmax_ULS)

        F = 0.9 * (N * math.tan(
            0.75 * Internal_friction / 180 * math.pi) + c * a_ULS) - 1.25 * PA1 - 1.5 * PA2 + 0.9 * 0.5 * Kp * (
                    Dimensions['D'] + Dimensions['SD'] + values['Overburden']) ** 2 * density_soil * 10 ** -6
        results = {'qmax': qmax, 'F': F, 'a_ULS': a_ULS, 'qmax_ULS': qmax_ULS, 'PA1': PA1, 'PA2': PA2, 'N': N,
                'N_centroid': centroid_N, 'a': a}
        return results



