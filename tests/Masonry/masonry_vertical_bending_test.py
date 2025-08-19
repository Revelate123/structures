import pytest
from structures.Masonry import unreinforced_masonry

class TestUnreinforcedMasonryBending:
    def test_vertical_bending_1(self):
        """
        Mdv <= Mcv
        Length = 1000mm
        Height = 1000mm
        Thickness = 110mm
        Zd = 2016666.667 mm^3
        phi = 0.6
        fmt = 0.2 MPa
        fd = 0

        if fmt > 0:
    
        Lowest of:
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 20126666.667 = 0.242MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 20126666.67 = 0.72MPa
        Mcv = 0.242 KNm
        """
        #wall = masonry.UnreinforcedMasonry(length=1000, height=2000, thickness=110, fmt=0.2, fuc = 20, mortar_class=3)
        #assert(wall.vertical_bending() == 0.242)

    def test_vertical_bending_2(self):
        """
        Mdv <= Mcv
        Length = 1000mm
        Height = 1000mm
        Thickness = 110mm
        Zd = 2016666.667 mm^3
        phi = 0.6
        fmt = 0 MPa
        fd = 0.1 MPa

        Mcv = fd * Zd = 0.20 KNm
        """

        #wall = masonry.UnreinforcedMasonry(length=1000, height=2000, thickness=110, fd=0.1, fmt=0, fuc = 20, mortar_class=3)
        #assert(round(wall.vertical_bending(),2) == 0.2)
    
    def test_vertical_bending_3(self):
        """
        Mdv <= Mcv
        Length = 500mm
        Height = 2000mm
        Thickness = 110mm
        Zd = 1008333.333 mm^3
        phi = 0.6
        fmt = 0.2 MPa
        fd = half wall height = 19KN/m3 * 1m = 19KPa = 0.019 MPa

        if fmt > 0:
        Lowest of:
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 1008333.333 mm3 + 0.019MPa * 1008333.333 mm3 = 0.140MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 1008333.333 = 0.363MPa
        Mcv = 0.140 KNm
        """

        #with pytest.raises(ValueError) as e_info:
            #wall = masonry.UnreinforcedMasonry(length=500, height=2000, thickness=110)
            #assert(round(wall.vertical_bending(),3) == 0.140)

        #wall = masonry.UnreinforcedMasonry(length=500, height=2000, thickness=110, fmt=0.2, fd=0.019, fuc = 20, mortar_class=3)
        #assert(round(wall.vertical_bending(),3) == 0.140)

    def test_vertical_bending_4(self):
        """
        Mdv <= Mcv
        Length = 500mm
        Height = 2000mm
        Thickness = 110mm
        Zd = 1008333.333 mm^3
        phi = 0.6
        fmt = 0.2 MPa
        fd = half wall height = 19KN/m3 * 1m = 19KPa = 0.019 MPa

        if fmt > 0:
        Lowest of:
        Mcv = phi * fmt * Zd + fd * Zd = 0.6 * 0.2MPa * 1008333.333 mm3 = 0.121MPa
        Mcv =  3 * phi * fmt * Zd = 3 * 0.6 * 0.2MPa * 1008333.333 = 0.363MPa
        Mcv = 0.121 KNm

        """

        #wall = masonry.UnreinforcedMasonry(length=500, height=2000, thickness=110, fmt=0.2, fuc = 20, mortar_class=3)
        #assert(round(wall.vertical_bending(),3) == 0.121)