import pytest
import structures.Masonry.unreinforced_masonry as unreinforced_masonry

class TestCompression:
    def test_compression(self):
        pass

class TestRefinedCompression:
    def test_refined_compression(self):
        """
        Scenario:
        A masonry wall 600W x 2700H x 110Thick is supporting an eccentric load due to an RC slab.

        Fd <= kFo

        Fo = phi * fm * Ab
        fm = 8.9MPa
        phi = 0.75
        Fo = 6.675MPa * Ab
        Ab = 600*110 = 66,000 mm2
        Fo = 440.55 KN
        k = 0.5(1+ e1/e2) * [(1 - 2.082* e1/tw) - (0.025 - 0.037 * e1/tw) * (1.33 * Sr - 8)] + 0.5 * (1 - 0.6 * e1/tw) * (1 - e2/e1) * (1.18 - 0.03Sr)
        k =  1 * [(0.65300) - (0.01883333) * (16.4841)] + 0 = 0.34255
        e1 = tw/6 = 18.3333mm
        e2 = tw/6 = 18.3333mm
        tw = 110mm
        Sr = av * H / (kt * t) = 0.75 * 2700 / (1 * 110) = 18.40909
        kFo = 440.55 KN * 0.34255 = 150.91KN

        """
        wall = unreinforced_masonry.UnreinforcedMasonry(length=600, height=2700, thickness=110, fuc = 20, mortar_class=4)
        capacity = wall.refined_compression(refined_av=0.75, Ab=0, kt=1, W_left=0,W_direct=0,W_right=10,refined_ah=0)
        #assert(capacity['Buckling'] == 150.91)
        #assert(capacity['Crushing'] == 295.16)
    
    def test_refined_compression_2(self):
        """
        Fd <= kFo

        Fo = phi * fm * Ab
        fm = 4.4MPa
        phi = 0.75
        Fo = 3.3MPa * Ab
        Ab = 600*110 = 66,000 mm2
        Fo = 217.8 KN
        k = 0.5(1+ e1/e2) * [(1 - 2.082* e1/tw) - (0.025 - 0.037 * e1/tw) * (1.33 * Sr - 8)] + 0.5 * (1 - 0.6 * e1/tw) * (1 - e2/e1) * (1.18 - 0.03Sr)
        k =  1 * [(0.65300) - (0.01883333) * (16.4841)] + 0 = 0.34255
        e1 = tw/6 = 18.3333mm
        e2 = tw/6 = 18.3333mm
        tw = 110mm
        Sr = av * H / (kt * t) = 0.75 * 2700 / (1 * 110) = 18.40909
        kFo = 217.8 KN * 0.34255 = 74.6KN

        """
        #wall = masonry.UnreinforcedMasonry(length=600, height=2700, thickness=110, av=0.75, kt = 1, Ab = 0 , fuc = 10, mortar_class=3)
        #assert(round(wall.refined_compression()) == 74.6)
    
    def test_refined_compression_3(self):
        """
        Fd <= kFo

        Fo = phi * fm * Ab
        fm = 4.4MPa
        phi = 0.75
        Fo = 3.3MPa * Ab
        Ab = 1500*110 = 165,000 mm2
        Fo = 544.5 KN
        k = 0.5(1+ e1/e2) * [(1 - 2.082* e1/tw) - (0.025 - 0.037 * e1/tw) * (1.33 * Sr - 8)] + 0.5 * (1 - 0.6 * e1/tw) * (1 - e2/e1) * (1.18 - 0.03Sr)
        k =  1 * [(0.65300) - (0.01883333) * (16.4841)] + 0 = 0.34255
        e1 = tw/6 = 18.3333mm
        e2 = tw/6 = 18.3333mm
        tw = 110mm
        Sr = av * H / (kt * t) = 0.75 * 2700 / (1 * 110) = 18.40909
        kFo = 544.5 KN * 0.34255 = 186.5KN

        """
        #wall = masonry.UnreinforcedMasonry(length=1500, height=2700, thickness=110, av=0.75, kt = 1, Ab =0 , fuc=10, mortar_class=3)
        #assert(round(wall.refined_compression(),1) == 186.5)
    
    def test_define_bearing_area(self):
        pass