"""
QST计算器测试
"""

import pytest
import numpy as np
from src.core.qst_calculator import QSTCalculator


class TestQSTCalculator:
    """测试QST计算器"""
    
    def test_effective_parameters(self):
        """测试有效参数集"""
        calc = QSTCalculator('effective')
        omega_de = calc.dark_energy_density()
        
        # 检查暗能量密度计算
        assert abs(omega_de - 0.690309) < 1e-6, f"Ω_DE计算错误: {omega_de}"
        
        # 检查参数设置
        assert 'phi_plus' in calc.params
        assert 'phi_minus' in calc.params
        assert 'omega' in calc.params
    
    def test_local_parameters(self):
        """测试局部参数集"""
        calc = QSTCalculator('local')
        
        # 测试火星时间延迟
        tau_mars = calc.mars_time_delay()
        assert 75 < tau_mars < 85, f"火星时间延迟异常: {tau_mars} μs/日"
        
        # 测试第五力力程
        lambda_m, lambda_au = calc.fifth_force_range()
        assert 800 < lambda_au < 1000, f"第五力力程异常: {lambda_au} AU"
        
        # 测试尺度依赖函数
        beta_earth = calc.beta_effective(5.97e24)  # 地球质量
        assert 0.27 < beta_earth < 0.29, f"地球β_eff异常: {beta_earth}"
    
    def test_beta_effective_function(self):
        """测试尺度依赖函数"""
        calc = QSTCalculator('local')
        
        # 测试极小质量
        beta_tiny = calc.beta_effective(0.001)  # 1g
        assert beta_tiny == 0.0, f"极小质量β_eff应为0: {beta_tiny}"
        
        # 测试小质量
        beta_small = calc.beta_effective(1.0)  # 1kg
        assert beta_small < 0.03, f"小质量β_eff过大: {beta_small}"
        
        # 测试大质量
        beta_large = calc.beta_effective(1e30)  # 太阳质量级
        assert abs(beta_large - 0.279) < 0.001, f"大质量β_eff异常: {beta_large}"
        
        # 测试质量阈值附近
        beta_threshold = calc.beta_effective(calc.params['M_th'])
        assert 0.25 < beta_threshold < 0.28, f"阈值质量β_eff异常: {beta_threshold}"
    
    def test_effective_a0_ratio(self):
        """测试有效加速度比例"""
        calc = QSTCalculator('local')
        
        # 测试极低表面密度
        a_ratio_low = calc.effective_a0_ratio(0.001)
        assert a_ratio_low < 0.001, f"低σ a_eff异常: {a_ratio_low}"
        
        # 测试中等表面密度
        a_ratio_mid = calc.effective_a0_ratio(1.0)
        assert 0.04 < a_ratio_mid < 0.07, f"中σ a_eff异常: {a_ratio_mid}"
        
        # 测试高表面密度
        a_ratio_high = calc.effective_a0_ratio(100.0)
        assert 0.8 < a_ratio_high <= 1.0, f"高σ a_eff异常: {a_ratio_high}"
        
        # 测试边界情况
        a_ratio_05 = calc.effective_a0_ratio(0.5)
        a_ratio_50 = calc.effective_a0_ratio(50.0)
        assert a_ratio_05 < a_ratio_50, "函数应为单调递增"
    
    def test_galaxy_rotation_velocity(self):
        """测试星系旋转速度计算"""
        calc = QSTCalculator('local')
        
        # 测试矮星系参数
        v_rot, a_ratio = calc.galaxy_rotation_velocity(
            M_baryon=1e9,    # 10^9 M_sun
            R_disk=2.0,      # 2 kpc
            sigma=0.3        # 表面密度
        )
        
        # 检查结果在合理范围
        assert 16 < v_rot < 30, f"矮星系旋转速度异常: {v_rot} km/s"
        assert 0.005 < a_ratio < 0.02, f"矮星系a_eff异常: {a_ratio}"
        
        # 测试计算一致性
        v_rot2, a_ratio2 = calc.galaxy_rotation_velocity(2e9, 2.0, 0.3)
        assert v_rot2 > v_rot, "质量增加速度应增加"
    
    def test_parameter_sets(self):
        """测试不同参数集"""
        # 测试所有参数集都能初始化
        calc_bare = QSTCalculator('bare')
        calc_eff = QSTCalculator('effective')
        calc_local = QSTCalculator('local')
        
        assert calc_bare.param_set == 'bare'
        assert calc_eff.param_set == 'effective'
        assert calc_local.param_set == 'local'
        
        # 测试无效参数集
        with pytest.raises(ValueError):
            QSTCalculator('invalid')
    
    def test_dark_energy_only_effective(self):
        """测试暗能量计算仅在有效参数集"""
        calc_local = QSTCalculator('local')
        calc_bare = QSTCalculator('bare')
        
        # 局部参数集不应支持暗能量计算
        with pytest.raises(ValueError):
            calc_local.dark_energy_density()
        
        # 裸参数集不应支持暗能量计算
        with pytest.raises(ValueError):
            calc_bare.dark_energy_density()
    
    def test_mars_delay_only_local(self):
        """测试火星延迟计算仅在局部参数集"""
        calc_eff = QSTCalculator('effective')
        calc_bare = QSTCalculator('bare')
        
        # 有效参数集不应支持火星延迟计算
        with pytest.raises(ValueError):
            calc_eff.mars_time_delay()
        
        # 裸参数集不应支持火星延迟计算
        with pytest.raises(ValueError):
            calc_bare.mars_time_delay()
    
    def test_consistency(self):
        """测试计算一致性"""
        calc = QSTCalculator('local')
        
        # 测试相同输入得到相同输出
        v1, a1 = calc.galaxy_rotation_velocity(1e9, 2.0, 0.3)
        v2, a2 = calc.galaxy_rotation_velocity(1e9, 2.0, 0.3)
        
        assert abs(v1 - v2) < 1e-10, "计算不一致"
        assert abs(a1 - a2) < 1e-10, "计算不一致"
        
        # 测试不同输入得到不同输出
        v3, a3 = calc.galaxy_rotation_velocity(2e9, 2.0, 0.3)
        assert abs(v3 - v1) > 1e-10, "质量不同但速度相同"


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
