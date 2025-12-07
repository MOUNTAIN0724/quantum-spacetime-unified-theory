"""
QST计算器测试 - v4.5版本
基于SPARC优化的最终版本
"""

import pytest
import numpy as np
from src.core.qst_calculator import QSTCalculator


def calculate_expected_a_ratio(sigma, A_low=0.015, sigma_crit=0.4, sigma_transition=2.5):
    """计算a_eff/a₀的期望值"""
    if sigma < sigma_crit:
        return A_low
    elif sigma < sigma_transition:
        frac = (sigma - sigma_crit) / (sigma_transition - sigma_crit)
        return A_low + (1.0 - A_low) * frac
    else:
        return 1.0


class TestQSTCalculator_v45:
    """测试QST计算器 v4.5"""
    
    def test_effective_parameters(self):
        """测试有效参数集"""
        calc = QSTCalculator('effective')
        omega_de = calc.dark_energy_density()
        assert abs(omega_de - 0.690309) < 1e-6, f"Ω_DE计算错误: {omega_de}"
        print("✅ test_effective_parameters: 通过")
    
    def test_local_parameters_v45(self):
        """测试局部参数集 - v4.5版本"""
        calc = QSTCalculator('local')
        
        # 火星时间延迟
        tau_mars = calc.mars_time_delay()
        expected = 0.8 * 3.386e-9 * 86400 * 1e6
        assert abs(tau_mars - expected) < 0.1, f"火星时间延迟异常: {tau_mars} μs/日"
        
        # 第五力力程
        lambda_m, lambda_au = calc.fifth_force_range()
        assert 800 < lambda_au < 1000, f"第五力力程异常: {lambda_au} AU"
        
        # 地球β_eff
        beta_earth = calc.beta_effective(5.97e24)
        assert abs(beta_earth - 0.72) < 1e-10, f"地球β_eff异常: {beta_earth}"
        
        print("✅ test_local_parameters_v45: 通过")
    
    def test_sparc_optimized_parameters(self):
        """测试SPARC优化参数集"""
        calc = QSTCalculator('sparc_optimized')
        params = calc.get_parameters()
        
        # 检查关键v4.5参数
        assert abs(params['beta0'] - 0.8) < 1e-6, f"β₀应该是0.8: {params['beta0']}"
        assert abs(params['A_low'] - 0.015) < 1e-6, f"A_low应该是0.015: {params['A_low']}"
        assert abs(params['sigma_crit'] - 0.4) < 1e-6, f"sigma_crit应该是0.4: {params['sigma_crit']}"
        assert abs(params['sigma_transition'] - 2.5) < 1e-6, f"sigma_transition应该是2.5: {params['sigma_transition']}"
        assert abs(params['alpha'] - 1.0) < 1e-6, f"alpha应该是1.0: {params['alpha']}"
        
        print("\n✅ v4.5参数验证通过")
        for key in ['beta0', 'A_low', 'sigma_crit', 'sigma_transition', 'alpha']:
            print(f"  {key}: {params[key]}")
    
    def test_beta_effective_function_v45(self):
        """测试尺度依赖函数 - v4.5版本"""
        calc = QSTCalculator('sparc_optimized')
        
        beta0 = calc.params['beta0']
        M_th = calc.params['M_th']
        
        # 测试具体x值
        test_cases = [
            (0.0000001, 0.0),   # x < 1e-6
            (0.0005, 0.0008),    # 0.000001 ≤ x < 0.001, f=0.001
            (0.001, 0.0008),     # x = 0.001, f=0.001
            (0.005, 0.008),      # 0.001 ≤ x < 0.01, f=0.01
            (0.05, 0.08),        # 0.01 ≤ x < 0.1, f=0.1
            (0.5, 0.56),         # 0.8×0.7=0.56
            (0.8, 0.56),       # 0.8×0.7=0.56  
            (1.0, 0.64),       # 0.8×0.8=0.64
            (2.0, 0.72),       # 0.8×0.9=0.72
        ]
        
        print("\nβ_eff函数测试:")
        for x, expected in test_cases:
            M = x * M_th
            beta = calc.beta_effective(M)
            assert abs(beta - expected) < 1e-10, f"x={x}: β_eff={beta} (期望{expected})"
            f = beta / beta0
            print(f"  x={x:.3f}: f={f:.3f}, β_eff={beta:.4f} ✓")
        
        print("✅ test_beta_effective_function_v45: 通过")
    
    def test_effective_a0_ratio_v45(self):
        """测试有效加速度比例 - v4.5版本"""
        calc = QSTCalculator('sparc_optimized')
        
        # 测试分段函数 - 使用动态计算的正确期望值
        test_sigmas = [0.001, 0.1, 0.4, 0.5, 1.0, 2.0, 2.5, 3.0, 10.0]
        
        print("\na_eff/a₀函数测试:")
        all_passed = True
        
        for sigma in test_sigmas:
            # 计算正确的期望值
            expected = calculate_expected_a_ratio(sigma)
            
            # 获取实际值
            ratio = calc.effective_a0_ratio(sigma)
            diff = abs(ratio - expected)
            passed = diff < 1e-4
            
            if not passed:
                all_passed = False
                print(f"  σ={sigma}: {ratio:.6f} (期望{expected:.6f}) ✗ 误差={diff:.6f}")
            else:
                # 计算frac用于显示
                if 0.4 <= sigma < 2.5:
                    frac = (sigma - 0.4) / (2.5 - 0.4)
                    print(f"  σ={sigma:.3f}: {ratio:.6f} (frac={frac:.4f}) ✓")
                else:
                    print(f"  σ={sigma:.3f}: {ratio:.6f} ✓")
        
        assert all_passed, "a_eff/a₀函数测试失败"
        print("✅ test_effective_a0_ratio_v45: 通过")
    
    def test_galaxy_rotation_velocity_v45(self):
        """测试星系旋转速度计算 - v4.5版本"""
        calc = QSTCalculator('sparc_optimized')
        
        # 测试矮星系参数 (σ=0.4)
        v_rot, a_ratio = calc.galaxy_rotation_velocity(
            M_baryon=1e9,    # 10^9 M_sun
            R_disk=2.0,      # 2 kpc
            sigma=0.4        # 表面密度
        )
        
        # 验证a_eff比例
        assert abs(a_ratio - 0.015) < 1e-6, f"矮星系a_eff异常: {a_ratio} (期望0.015)"
        
        # 检查速度在合理范围
        assert 25 < v_rot < 35, f"矮星系旋转速度异常: {v_rot} km/s"
        
        # 测试计算一致性
        v_rot2, a_ratio2 = calc.galaxy_rotation_velocity(2e9, 2.0, 0.4)
        assert v_rot2 > v_rot, "质量增加速度应增加"
        
        print(f"\n矮星系测试:")
        print(f"  M=1e9 M_sun, R=2 kpc, σ=0.4")
        print(f"  V={v_rot:.1f} km/s, a_eff/a₀={a_ratio:.4f} ✓")
        print("✅ test_galaxy_rotation_velocity_v45: 通过")
    
    def test_parameter_sets(self):
        """测试不同参数集"""
        # 测试所有参数集都能初始化
        calc_bare = QSTCalculator('bare')
        calc_eff = QSTCalculator('effective')
        calc_local = QSTCalculator('local')
        calc_sparc = QSTCalculator('sparc_optimized')
        
        assert calc_bare.param_set == 'bare'
        assert calc_eff.param_set == 'effective'
        assert calc_local.param_set == 'local'
        assert calc_sparc.param_set == 'sparc_optimized'
        
        # 测试无效参数集
        with pytest.raises(ValueError):
            QSTCalculator('invalid')
        
        print("\n✅ 所有参数集初始化成功")
        print("✅ test_parameter_sets: 通过")
    
    def test_dark_energy_only_effective(self):
        """测试暗能量计算仅在有效参数集"""
        calc_local = QSTCalculator('local')
        calc_bare = QSTCalculator('bare')
        calc_sparc = QSTCalculator('sparc_optimized')
        
        # 局部参数集不应支持暗能量计算
        with pytest.raises(ValueError):
            calc_local.dark_energy_density()
        
        # 裸参数集不应支持暗能量计算
        with pytest.raises(ValueError):
            calc_bare.dark_energy_density()
        
        # sparc_optimized参数集应支持暗能量计算
        omega_de = calc_sparc.dark_energy_density()
        assert abs(omega_de - 0.690309) < 1e-6
        
        print("\n✅ 暗能量计算权限验证通过")
        print("✅ test_dark_energy_only_effective: 通过")
    
    def test_mars_delay_only_local(self):
        """测试火星延迟计算仅在局部参数集"""
        calc_eff = QSTCalculator('effective')
        calc_bare = QSTCalculator('bare')
        calc_sparc = QSTCalculator('sparc_optimized')
        
        # 有效参数集不应支持火星延迟计算
        with pytest.raises(ValueError):
            calc_eff.mars_time_delay()
        
        # 裸参数集不应支持火星延迟计算
        with pytest.raises(ValueError):
            calc_bare.mars_time_delay()
        
        # sparc_optimized参数集应支持火星延迟计算
        tau_mars = calc_sparc.mars_time_delay()
        expected = 0.8 * 3.386e-9 * 86400 * 1e6
        assert abs(tau_mars - expected) < 0.1
        
        print("\n✅ 火星延迟计算权限验证通过")
        print(f"  火星时间延迟: {tau_mars:.1f} μs/日")
        print("✅ test_mars_delay_only_local: 通过")
    
    def test_consistency(self):
        """测试计算一致性"""
        calc = QSTCalculator('sparc_optimized')
        
        # 测试相同输入得到相同输出
        v1, a1 = calc.galaxy_rotation_velocity(1e9, 2.0, 0.4)
        v2, a2 = calc.galaxy_rotation_velocity(1e9, 2.0, 0.4)
        
        assert abs(v1 - v2) < 1e-10, "计算不一致"
        assert abs(a1 - a2) < 1e-10, "计算不一致"
        
        # 测试不同输入得到不同输出
        v3, a3 = calc.galaxy_rotation_velocity(2e9, 2.0, 0.4)
        assert abs(v3 - v1) > 1e-10, "质量不同但速度相同"
        
        print("\n✅ 计算一致性验证通过")
        print("✅ test_consistency: 通过")


if __name__ == "__main__":
    print("=" * 60)
    print("QST v4.5 完整测试套件")
    print("=" * 60)
    
    # 运行测试
    pytest.main([__file__, "-v", "--tb=short"])
