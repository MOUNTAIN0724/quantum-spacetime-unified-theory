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
        
        # 測試小質量
        beta_small = calc.beta_effective(1.0)  # 1kg
        assert beta_small < 0.01, f"小質量β_eff過大: {beta_small}"
        
        # 測試大質量
        beta_large = calc.beta_effective(1e30)  # 太陽質量級
        assert abs(beta_large - 0.279) < 0.001, f"大質量β_eff異常: {beta_large}"
        
        # 測試質量閾值附近
        beta_threshold = calc.beta_effective(calc.params['M_th'])
        assert 0.1 < beta_threshold < 0.2, f"閾值質量β_eff異常: {beta_threshold}"
    
    def test_effective_a0_ratio(self):
        """測試有效加速度比例"""
        calc = QSTCalculator('local')
        
        # 測試極低表面密度
        a_ratio_low = calc.effective_a0_ratio(0.001)
        assert a_ratio_low < 0.001, f"低σ a_eff異常: {a_ratio_low}"
        
        # 測試中等表面密度
        a_ratio_mid = calc.effective_a0_ratio(1.0)
        assert 0.01 < a_ratio_mid < 0.1, f"中σ a_eff異常: {a_ratio_mid}"
        
        # 測試高表面密度
        a_ratio_high = calc.effective_a0_ratio(100.0)
        assert 0.5 < a_ratio_high <= 1.0, f"高σ a_eff異常: {a_ratio_high}"
    
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
        assert 20 < v_rot < 80, f"矮星系旋轉速度異常: {v_rot} km/s"
        assert 0.001 < a_ratio < 0.01, f"矮星系a_eff異常: {a_ratio}"
    
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


if __name__ == "__main__":
    # 運行測試
    pytest.main([__file__, "-v"])
