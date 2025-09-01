import pytest
import structures.Masonry.unreinforced_masonry as unreinforced_masonry

class TestCompression:
    def test_compression(self):
        pass

class TestBasicCompressiveCapacity:
    def test_standard_M3_brick(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 6.261 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 6.261 = 4.70 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 100, fuc = 20, mortar_class= 3,bedding_type=True)
        assert(wall.basic_compressive_capacity() == 4.70)

    def test_standard_M4_brick(self):
        """
        km = 2 (For clay Full Bedding M4 mortar class)
        fmb = km * sqrt(fuc) = 2 * sqrt(20) = 8.944 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 8.944 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 8.944 = 6.71 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 100, fuc = 20, mortar_class= 4,bedding_type=True)
        assert(wall.basic_compressive_capacity() == 6.71)
    
    def test_low_compressive_strength_brick(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(5) = 3.130 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 3.130 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 3.130 = 2.35 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 100, fuc = 5, mortar_class= 3,bedding_type=True)
        assert(wall.basic_compressive_capacity() == 2.35)

    def test_high_compressive_strength_brick(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(60) = 10.844 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 10.844 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 10.844 = 8.13 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 100, fuc =60, mortar_class= 3,bedding_type=True)
        assert(wall.basic_compressive_capacity() == 8.13)

    def test_face_shell_bedding_type(self):
        """
        km = 1.6 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.6 * sqrt(20) = 7.155 MPa
        kh = 1.0 (for 76mm brick height with 10mm thick mortar)
        fm = kh * fmb = 7.155 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 7.155 = 5.37 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 100, fuc = 20, mortar_class= 3,bedding_type=False)
        assert(wall.basic_compressive_capacity() == 5.37)

    def test_fails_for_M4_face_shell_bedding_type(self):
        with pytest.raises(ValueError):
            wall = unreinforced_masonry.Clay(length=1000,height=1000,thickness=100,fuc=20,mortar_class=4,bedding_type=False)
            wall.basic_compressive_capacity()

    def test_fails_for_M1_mortar(self):
        with pytest.raises(ValueError):
            wall = unreinforced_masonry.Clay(length=1000,height=1000,thickness=100,fuc=20,mortar_class=1,bedding_type=True)
            wall.basic_compressive_capacity()

    def test_90_brick_10_joint(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.05 (for 90mm brick height with 10mm thick mortar)
        fm = kh * fmb = 1.05 * 6.261 MPa = 6.574 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 6.261 = 4.93 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 90, tj=10, hu=90, fuc = 20, mortar_class= 3,bedding_type=True)
        assert(wall.basic_compressive_capacity() == 4.93)

    def test_150_brick_12_joint(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.3 * (150/(19*12))**0.29 = 1.151
        fm = kh * fmb = 1.151 * 6.261 MPa = 7.206 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 7.206 = 5.40 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 100, tj=12,hu=150,  fuc = 20, mortar_class= 3,bedding_type=True)
        assert(wall.basic_compressive_capacity() == 5.40)

    def test_200_brick_5_joint(self):
        """
        km = 1.4 (For clay Full Bedding M3 mortar class)
        fmb = km * sqrt(fuc) = 1.4 * sqrt(20) = 6.261 MPa
        kh = 1.3 (maximum value)
        fm = kh * fmb = 1.3 * 6.261 MPa = 8.14 MPa
        Phi = 0.75
        Fo = phi * f'm = 0.75 * 8.14 = 6.11 MPa
        """
        wall = unreinforced_masonry.Clay(length=1000, height=1000, thickness = 100, tj=5,hu=200,  fuc = 20, mortar_class= 3,bedding_type=True)
        assert(wall.basic_compressive_capacity() == 6.11)
    

class TestSimplifiedCompression:
    def test(self):
        pass

class TestRefinedCompression:
    
    def test_face_shell_bedding(self):
        pass

    def test_large_eccentricity(self):
        pass

    def test_small_eccentricity(self):
        pass
    
    def test_horz_capacity_limited_by_Fo(self):
        pass

    def test_stocky_wall(self):
        pass

    def test_slender_wall(self):
        pass

    def test_one_return(self):
        pass

    def test_two_returns(self):
        pass

    def test_cantilever_wall(self):
        pass
    
    def test_refined_compression(self):
        """
        Scenario:
        A masonry wall 600W x 2700H x 110 Thick is supporting an eccentric load applied by an RC slab.

        Fd <= kFo

        Fo = phi * fm * Ab
        fm = 8.94MPa
        phi = 0.75
        Fo = 0.75 * 8.94 * Ab = 6.71MPa
        Sr = av * H / (kt * t) = 0.75 * 2700 / (1 * 110) = 18.41
        k = 0.5(1+ e1/e2) * [(1 - 2.082* e1/tw) - (0.025 - 0.037 * e1/tw) * (1.33 * Sr - 8)] + 0.5 * (1 - 0.6 * e1/tw) * (1 - e2/e1) * (1.18 - 0.03Sr)
        k =  1 * [(0.65300) - (0.01883333) * (16.4841)] + 0 = 0.34
        e1 = tw/6 = 18.3333mm
        e2 = tw/6 = 18.3333mm
        tw = 110mm
        Ab = 600*110 = 66,000 mm2
        kFo = 6.71MPa * 66,000mm2 * 0.34 = 150.57KN

        k = 1 - 2*(18.33/110) = 0.67
        Fo = 6.71MPa * 66,000mm2 * 0.67 = 296.72

        """
        wall = unreinforced_masonry.Clay(length=600, height=2700, thickness=110, fuc = 20, mortar_class=4, bedding_type=True)
        capacity = wall.refined_compression(refined_av=0.75, kt=1, W_left=0,W_direct=0,W_right=10,refined_ah=0)
        assert(capacity['Buckling'] == 150.57)
        assert(capacity['Crushing'] == 296.72)
    
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
        wall = unreinforced_masonry.Clay(length=600, height=2700, thickness=110, fuc = 10, mortar_class=3)
        #capacity = wall.refined_compression(refined_av=0.75, refined_ah=0,kt=1)
    
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

class TestConcentratedLoad:
    def test_concetrated_load_1(self):
        """
        
        """
        wall = unreinforced_masonry.Clay(length=1000,height=1000,thickness=100, fuc=20, mortar_class=3,bedding_type=True)
        bearing_cap = wall.concentrated_load(bearing_length=1000,dist_to_end=0,bearing_width=100,W_left=0,W_direct=0,W_right=0,refined_av=0.75,refined_ah=0,kt=1)
        #assert(bearing_cap == 600)