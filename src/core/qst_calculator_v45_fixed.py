"""
量子时空统一理论 - v4.5修复版本
"""

import numpy as np
from typing import Dict, Tuple, Optional


class QSTCalculator_v45:
    """QST v4.5正确修复版本"""
    
    def __init__(self, param_set='sparc_optimized'):
        self.param_set = param_set
        self._setup_parameters()
    
    def _setup_parameters(self):
        """设置v4.5优化参数"""
        if self.param_set == 'sparc_optimized':
            # v4.5优化参数
            self.params = {
                'phi_plus': 1.621,
                'phi_minus': 1.459,
                'omega': 1.297,
                'beta0': 0.8000,           # 第五力修正系数
                'M_th': 1.0e22,            # 质量阈值 [kg]
                'A_low': 0.0150,           # 矮星系的a_eff/a₀
                'sigma_crit': 0.4000,      # 临界表面密度
                'sigma_transition': 2.5000, # 过渡表面密度
                'alpha': 1.0000,           # 幂律指数
                'a0_standard': 1.2e-10,    # 标准加速度尺度
                'm_omega_5th': 1.44e-21,   # 第五力质量 [eV]
                'lambda_5th': 915.0,       # 第五力力程 [AU]
                'm_phi': 0.08,             # Φ场有效质量
                'm_omega': 0.06,           # Ω场有效质量
                'mu': 0.00306,             # 混合参数
                'V_const': 2.0527,         # 势能常数
            }
        else:
            raise ValueError(f"未知参数集: {self.param_set}")
    
    def beta_effective(self, M: float) -> float:
        """v4.5正确版本的β_eff函数"""
        if self.param_set != 'sparc_optimized':
            raise ValueError("此计算需要sparc_optimized参数集")
        
        beta0 = self.params['beta0']
        M_th = self.params['M_th']
        x = M / M_th
        
        # v4.5的尺度依赖函数 - 完全明确的区间判断
        if x < 0.001:
            f = 0.001
        elif x < 0.01:      # 0.001 ≤ x < 0.01
            f = 0.01
        elif x < 0.1:       # 0.01 ≤ x < 0.1
            f = 0.1
        elif x < 0.5:       # 0.1 ≤ x < 0.5
            f = 0.5
        elif x < 0.8:       # 0.5 ≤ x < 0.8  ← 关键区间
            f = 0.7
        elif x < 1.0:       # 0.8 ≤ x < 1.0
            # 线性插值：x=0.8时f=0.7, x=1.0时f=0.8
            f = 0.7 + 0.1 * (x - 0.8) / 0.2
        elif x < 2.0:       # 1.0 ≤ x < 2.0
            # 线性插值：x=1.0时f=0.8, x=2.0时f=0.9
            f = 0.8 + 0.1 * (x - 1.0) / 1.0
        else:               # x ≥ 2.0
            f = 0.9
        
        beta_eff = beta0 * f
        return beta_eff
    
    def effective_a0_ratio(self, sigma: float) -> float:
        """v4.5的a_eff函数"""
        A_low = self.params['A_low']
        sigma_crit = self.params['sigma_crit']
        sigma_transition = self.params['sigma_transition']
        
        if sigma < sigma_crit:
            return A_low
        elif sigma < sigma_transition:
            # 线性插值
            frac = (sigma - sigma_crit) / (sigma_transition - sigma_crit)
            return A_low + (1.0 - A_low) * frac
        else:
            return 1.0
    
    def dark_energy_density(self) -> float:
        """计算暗能量密度"""
        phi_plus = self.params['phi_plus']
        phi_minus = self.params['phi_minus']
        omega = self.params['omega']
        m_phi = self.params['m_phi']
        m_omega = self.params['m_omega']
        mu = self.params['mu']
        V_const = self.params['V_const']
        
        V_phi = 0.5 * m_phi**2 * (phi_plus**2 + phi_minus**2)
        V_mix = -mu**2 * phi_plus * phi_minus
        V_omega = 0.5 * m_omega**2 * omega**2
        
        V_total = V_phi + V_mix + V_omega + V_const
        rho_crit = 3.0  # 归一化单位
        Omega_DE = V_total / rho_crit
        
        return Omega_DE
    
    def mars_time_delay(self) -> float:
        """计算火星时间延迟"""
        beta0 = self.params['beta0']
        delta_phi_grav = 3.386e-9
        delta_tau_tau = beta0 * delta_phi_grav
        seconds_per_day = 86400.0
        microseconds_per_second = 1e6
        delta_tau_per_day = delta_tau_tau * seconds_per_day * microseconds_per_second
        
        return delta_tau_per_day
    
    def galaxy_rotation_velocity(self, M_baryon: float, R_disk: float, 
                                sigma: Optional[float] = None) -> Tuple[float, float]:
        """计算星系旋转速度"""
        # 物理常数
        G = 6.67430e-11     # 引力常数 [m³/kg/s²]
        M_SUN = 1.989e30    # 太阳质量 [kg]
        KPC = 3.086e19      # 千秒差距 [m]
        
        if sigma is None:
            M_baryon_kg = M_baryon * M_SUN
            R_disk_m = R_disk * KPC
            sigma = M_baryon_kg / (np.pi * R_disk_m**2)
            sigma = sigma / (1e9 * M_SUN / KPC**2)
        
        a_ratio = self.effective_a0_ratio(sigma)
        a0_standard = self.params['a0_standard']
        M_baryon_kg = M_baryon * M_SUN
        a_eff = a0_standard * a_ratio
        beta_eff = self.beta_effective(M_baryon_kg)
        
        v4 = G * M_baryon_kg * a_eff * (1.0 + beta_eff) * 2.0
        v_qst = v4**0.25
        v_qst_km_s = v_qst / 1000.0
        
        return v_qst_km_s, a_ratio
    
    def fifth_force_range(self) -> Tuple[float, float]:
        """计算第五力力程"""
        lambda_au = self.params['lambda_5th']
        AU = 1.495978707e11  # 天文单位 [m]
        lambda_m = lambda_au * AU
        
        return lambda_m, lambda_au
    
    def get_parameters(self) -> Dict:
        """获取参数"""
        return self.params.copy()
    
    def print_parameters(self):
        """打印参数"""
        print(f"QST v4.5计算器参数集: {self.param_set}")
        print("=" * 50)
        for key, value in self.params.items():
            if isinstance(value, float):
                print(f"{key:20} = {value:.6g}")
            else:
                print(f"{key:20} = {value}")
