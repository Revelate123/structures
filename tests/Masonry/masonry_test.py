import pytest
import structures.Masonry.unreinforced_masonry as unreinforced_masonry


class TestBasicCompressiveCapacity:
    def test_basic_compressive_strength(self):
        """
        fuc = 20 MPa
        mortar class = 3
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        fm = kh * fmb = 1 * fmb = 6.261 MPa
        phi = 0.75
        Fo = 0.75 * 6.261 = 4.70 MPa
        """

        wall = unreinforced_masonry.UnreinforcedMasonry(length = 1000, height = 1000, thickness= 110, fuc = 20, mortar_class=3)
        Fo = wall.basic_compressive_capacity(verbose=False)
        assert(Fo == 4.70)

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