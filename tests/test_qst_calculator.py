"""
QST計算器測試
"""

import pytest
import numpy as np
from src.core.qst_calculator import QSTCalculator


class TestQSTCalculator:
    """測試QST計算器"""
    
    def test_effective_parameters(self):
        """測試有效參數集"""
        calc = QSTCalculator('effective')
        omega_de = calc.dark_energy_density()
        
        # 檢查暗能量密度計算
        assert abs(omega_de - 0.690309) < 1e-6, f"Ω_DE計算錯誤: {omega_de}"
        
        # 檢查參數設置
        assert 'phi_plus' in calc.params
        assert 'phi_minus' in calc.params
        assert 'omega' in calc.params
    
    def test_local_parameters(self):
        """測試局部參數集"""
        calc = QSTCalculator('local')
        
        # 測試火星時間延遲
        tau_mars = calc.mars_time_delay()
        assert 75 < tau_mars < 85, f"火星時間延遲異常: {tau_mars} μs/日"
        
        # 測試第五力力程
        lambda_m, lambda_au = calc.fifth_force_range()
        assert 800 < lambda_au < 1000, f"第五力力程異常: {lambda_au} AU"
        
        # 測試尺度依賴函數
        beta_earth = calc.beta_effective(5.97e24)  # 地球質量
        assert 0.27 < beta_earth < 0.29, f"地球β_eff異常: {beta_earth}"
    
    def test_beta_effective_function(self):
        """測試尺度依賴函數"""
        calc = QSTCalculator('local')
        
        # 測試極小質量
        beta_tiny = calc.beta_effective(0.001)  # 1g
        assert beta_tiny == 0.0, f"極小質量β_eff應為0: {beta_tiny}"
        
        # 測試小質量
        beta_small = calc.beta_effective(1.0)  # 1kg
        assert beta_small < 0.02, f"小質量β_eff過大: {beta_small}"
        
        # 測試大質量
        beta_large = calc.beta_effective(1e30)  # 太陽質量級
        assert abs(beta_large - 0.279) < 0.001, f"大質量β_eff異常: {beta_large}"
        
        # 測試質量閾值附近
        beta_threshold = calc.beta_effective(calc.params['M_th'])
        assert 0.25 < beta_threshold < 0.28, f"閾值質量β_eff異常: {beta_threshold}"
    
    def test_effective_a0_ratio(self):
        """測試有效加速度比例"""
        calc = QSTCalculator('local')
        
        # 測試極低表面密度
        a_ratio_low = calc.effective_a0_ratio(0.001)
        assert a_ratio_low < 0.001, f"低σ a_eff異常: {a_ratio_low}"
        
        # 測試中等表面密度
        a_ratio_mid = calc.effective_a0_ratio(1.0)
        assert 0.04 < a_ratio_mid < 0.06, f"中σ a_eff異常: {a_ratio_mid}"
        
        # 測試高表面密度
        a_ratio_high = calc.effective_a0_ratio(100.0)
        assert 0.5 < a_ratio_high <= 1.0, f"高σ a_eff異常: {a_ratio_high}"
        
        # 測試邊界情況
        a_ratio_05 = calc.effective_a0_ratio(0.5)
        a_ratio_50 = calc.effective_a0_ratio(50.0)
        assert a_ratio_05 < a_ratio_50, "函數應為單調遞增"
    
    def test_galaxy_rotation_velocity(self):
        """測試星系旋轉速度計算"""
        calc = QSTCalculator('local')
        
        # 測試矮星系參數
        v_rot, a_ratio = calc.galaxy_rotation_velocity(
            M_baryon=1e9,    # 10^9 M_sun
            R_disk=2.0,      # 2 kpc
            sigma=0.3        # 表面密度
        )
        
        # 檢查結果在合理範圍
        assert 15 < v_rot < 30, f"矮星系旋轉速度異常: {v_rot} km/s"
        assert 0.005 < a_ratio < 0.02, f"矮星系a_eff異常: {a_ratio}"
        
        # 測試計算一致性
        v_rot2, a_ratio2 = calc.galaxy_rotation_velocity(2e9, 2.0, 0.3)
        assert v_rot2 > v_rot, "質量增加速度應增加"
    
    def test_parameter_sets(self):
        """測試不同參數集"""
        # 測試所有參數集都能初始化
        calc_bare = QSTCalculator('bare')
        calc_eff = QSTCalculator('effective')
        calc_local = QSTCalculator('local')
        
        assert calc_bare.param_set == 'bare'
        assert calc_eff.param_set == 'effective'
        assert calc_local.param_set == 'local'
        
        # 測試無效參數集
        with pytest.raises(ValueError):
            QSTCalculator('invalid')
    
    def test_dark_energy_only_effective(self):
        """測試暗能量計算僅在有效參數集"""
        calc_local = QSTCalculator('local')
        calc_bare = QSTCalculator('bare')
        
        # 局部參數集不應支持暗能量計算
        with pytest.raises(ValueError):
            calc_local.dark_energy_density()
        
        # 裸參數集不應支持暗能量計算
        with pytest.raises(ValueError):
            calc_bare.dark_energy_density()
    
    def test_mars_delay_only_local(self):
        """測試火星延遲計算僅在局部參數集"""
        calc_eff = QSTCalculator('effective')
        calc_bare = QSTCalculator('bare')
        
        # 有效參數集不應支持火星延遲計算
        with pytest.raises(ValueError):
            calc_eff.mars_time_delay()
        
        # 裸參數集不應支持火星延遲計算
        with pytest.raises(ValueError):
            calc_bare.mars_time_delay()
    
    def test_consistency(self):
        """測試計算一致性"""
        calc = QSTCalculator('local')
        
        # 測試相同輸入得到相同輸出
        v1, a1 = calc.galaxy_rotation_velocity(1e9, 2.0, 0.3)
        v2, a2 = calc.galaxy_rotation_velocity(1e9, 2.0, 0.3)
        
        assert abs(v1 - v2) < 1e-10, "計算不一致"
        assert abs(a1 - a2) < 1e-10, "計算不一致"
        
        # 測試不同輸入得到不同輸出
        v3, a3 = calc.galaxy_rotation_velocity(2e9, 2.0, 0.3)
        assert abs(v3 - v1) > 1e-10, "質量不同但速度相同"


if __name__ == "__main__":
    # 運行測試
    pytest.main([__file__, "-v"])
