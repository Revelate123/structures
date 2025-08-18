import pytest
import structures.Masonry.masonry as masonry


class TestUnreinforcedMasonry:

    #def test_default_masonry_properties(self):
       # """
        
       # """
        #wall = masonry.UnreinforcedMasonry()
       # assert(wall.fmb == 4.4)
       # assert(wall.fm == 4.4)
        
     
    

    

    
    

    

    

    def test_horizontal_shear_1(self):
        """
        Vd <= V0 + V1 = 16.5 KN + 0KN = 16.5KN

        V0 = phi * fmt * Ad = 0.6 * 0.25 MPa * 110,000 mm2 = 16.5 KN
        phi = 0.6
        fms = 0.25MPa Cl 3.3.4
        Ad = 1000 * 110 = 110,000 mm2

        V1 = kv * fd * Ad = 0
        kv = 0.2 for interface with steel
        fd = 0
        """

       # wall = masonry.UnreinforcedMasonry(length=1000, height=2000, thickness=110, kv = 0.2, fmt=0.2, fuc = 20, mortar_class=3)
       # assert(wall.horizontal_shear() == 16.5)
    
    

  #  def test_horizontal_shear_raises_error(self):
       # with pytest.raises(ValueError) as e_info:
           # wall = masonry.UnreinforcedMasonry(length=1000, thickness=110)
           # wall.horizontal_shear()