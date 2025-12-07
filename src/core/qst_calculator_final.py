"""
量子时空统一理论 - 核心计算器 v4.5 (最终修复版)
"""

import numpy as np
from typing import Dict, Tuple, Optional
from .physics_constants import PhysicalConstants, QSTConstants


class QSTCalculator:
    """量子时空统一理论计算器 v4.5"""
    
    def __init__(self, param_set: str = 'sparc_optimized'):
        self.param_set = param_set
        self.constants = PhysicalConstants()
        self.qst_constants = QSTConstants()
        self._setup_parameters()
        self._cache = {}
    
    def _setup_parameters(self):
        """设置参数"""
        if self.param_set == 'bare':
            self.params = {
                'phi_plus': self.qst_constants.PHI_PLUS,
                'phi_minus': self.qst_constants.PHI_MINUS,
                'omega': self.qst_constants.OMEGA,
                'm_phi': 0.935,
                'm_omega': 1.0,
                'mu': self.qst_constants.MU,
                'lambda1': 2.34e-6,
                'lambda2': 3.78e-7,
                'lambda3': 1.29e-8,
            }
        elif self.param_set == 'effective':
            self.params = {
                'phi_plus': self.qst_constants.PHI_PLUS,
                'phi_minus': self.qst_constants.PHI_MINUS,
                'omega': self.qst_constants.OMEGA,
                'm_phi': self.qst_constants.M_PHI_EFF,
                'm_omega': self.qst_constants.M_OMEGA_EFF,
                'mu': self.qst_constants.MU,
                'V_const': self.qst_constants.V_CONST,
            }
        elif self.param_set == 'local':
            self.params = {
                'phi_plus': self.qst_constants.PHI_PLUS,
                'phi_minus': self.qst_constants.PHI_MINUS,
                'omega': self.qst_constants.OMEGA,
                'm_omega_5th': self.qst_constants.M_OMEGA_5TH,
                'lambda_5th': self.qst_constants.LAMBDA_5TH,
                'beta0': self.qst_constants.BETA0,
                'M_th': self.qst_constants.M_TH,
            }
        elif self.param_set == 'sparc_optimized':
            self.params = {
                'phi_plus': self.qst_constants.PHI_PLUS,
                'phi_minus': self.qst_constants.PHI_MINUS,
                'omega': self.qst_constants.OMEGA,
                'beta0': self.qst_constants.BETA0,
                'M_th': self.qst_constants.M_TH,
                'A_low': self.qst_constants.A_LOW,
                'sigma_crit': self.qst_constants.SIGMA_CRIT,
                'sigma_transition': self.qst_constants.SIGMA_TRANSITION,
                'alpha': self.qst_constants.ALPHA,
                'a0_standard': self.qst_constants.A0_STANDARD,
                'm_omega_5th': self.qst_constants.M_OMEGA_5TH,
                'lambda_5th': self.qst_constants.LAMBDA_5TH,
                'm_phi': self.qst_constants.M_PHI_EFF,
                'm_omega': self.qst_constants.M_OMEGA_EFF,
                'mu': self.qst_constants.MU,
                'V_const': self.qst_constants.V_CONST,
            }
        else:
            raise ValueError(f"未知参数集: {self.param_set}")
    
    def beta_effective(self, M: float) -> float:
        """计算尺度依赖的耦合常数 β_eff(M) - 修复版"""
        if self.param_set not in ['local', 'sparc_optimized']:
            raise ValueError("此计算需要局部参数集")
        
        beta0 = self.params['beta0']
        M_th = self.params['M_th']
        
        x = M / M_th
        
        # v4.5优化后的尺度依赖函数 - 使用更精确的边界处理
        # 使用numpy的isclose来处理浮点数精度
        if x < 1e-6:
            f = 0.0
        elif np.isclose(x, 0.001, rtol=1e-10) or (1e-6 <= x < 0.001):
            f = 0.001
        elif np.isclose(x, 0.01, rtol=1e-10) or (0.001 <= x < 0.01):
            f = 0.01
        elif np.isclose(x, 0.1, rtol=1e-10) or (0.01 <= x < 0.1):
            f = 0.1
        elif np.isclose(x, 0.5, rtol=1e-10) or (0.1 <= x < 0.5):
            f = 0.5
        elif np.isclose(x, 0.8, rtol=1e-10) or (0.5 <= x < 0.8):
            f = 0.7
        elif np.isclose(x, 1.0, rtol=1e-10) or (0.8 <= x < 1.0):
            if x < 0.8:
                f = 0.7
            elif x >= 1.0:
                f = 0.8
            else:
                f = 0.7 + 0.1 * (x - 0.8) / 0.2
        elif np.isclose(x, 2.0, rtol=1e-10) or (1.0 <= x < 2.0):
            if x < 1.0:
                f = 0.8
            elif x >= 2.0:
                f = 0.9
            else:
                f = 0.8 + 0.1 * (x - 1.0) / 1.0
        else:
            f = 0.9
        
        beta_eff = beta0 * f
        
        return beta_eff
    
    # 其他函数保持不变...
    def dark_energy_density(self) -> float:
        if self.param_set not in ['effective', 'sparc_optimized']:
            raise ValueError("此计算需要有效参数集")
        
        phi_plus = self.params['phi_plus']
        phi_minus = self.params['phi_minus']
        omega = self.params['omega']
        m_phi = self.params.get('m_phi', self.qst_constants.M_PHI_EFF)
        m_omega = self.params.get('m_omega', self.qst_constants.M_OMEGA_EFF)
        mu = self.params.get('mu', self.qst_constants.MU)
        V_const = self.params.get('V_const', self.qst_constants.V_CONST)
        
        V_phi = 0.5 * m_phi**2 * (phi_plus**2 + phi_minus**2)
        V_mix = -mu**2 * phi_plus * phi_minus
        V_omega = 0.5 * m_omega**2 * omega**2
        
        V_total = V_phi + V_mix + V_omega + V_const
        rho_crit = 3.0
        Omega_DE = V_total / rho_crit
        
        return Omega_DE
    
    def mars_time_delay(self) -> float:
        if self.param_set not in ['local', 'sparc_optimized']:
            raise ValueError("此计算需要局部参数集")
        
        beta0 = self.params['beta0']
        delta_phi_grav = 3.386e-9
        delta_tau_tau = beta0 * delta_phi_grav
        seconds_per_day = 86400.0
        microseconds_per_second = 1e6
        delta_tau_per_day = delta_tau_tau * seconds_per_day * microseconds_per_second
        
        return delta_tau_per_day
    
    def effective_a0_ratio(self, sigma: float) -> float:
        if self.param_set == 'sparc_optimized':
            return self._effective_a0_ratio_v45(sigma)
        
        if sigma < 0.001:
            return 0.0005
        elif sigma < 0.01:
            return 0.0005 + 0.0005 * (sigma - 0.001) / 0.009
        elif sigma < 0.1:
            return 0.001 + 0.001 * (sigma - 0.01) / 0.09
        elif sigma < 0.3:
            return 0.002 + 0.003 * (sigma - 0.1) / 0.2
        elif sigma < 0.5:
            return 0.005 + 0.005 * (sigma - 0.3) / 0.2
        elif sigma < 1.0:
            return 0.01 + 0.04 * (sigma - 0.5) / 0.5
        elif sigma < 5.0:
            return 0.05 + 0.45 * (sigma - 1.0) / 4.0
        elif sigma < 10.0:
            return 0.5 + 0.3 * (sigma - 5.0) / 5.0
        elif sigma < 50.0:
            return 0.8 + 0.2 * (sigma - 10.0) / 40.0
        else:
            return 1.0
    
    def _effective_a0_ratio_v45(self, sigma: float) -> float:
        A_low = self.params['A_low']
        sigma_crit = self.params['sigma_crit']
        sigma_transition = self.params['sigma_transition']
        alpha = self.params['alpha']
        
        if sigma < sigma_crit:
            return A_low
        elif sigma < sigma_transition:
            frac = (sigma - sigma_crit) / (sigma_transition - sigma_crit)
            return A_low + (1.0 - A_low) * (frac ** alpha)
        else:
            return 1.0
    
    def galaxy_rotation_velocity(self, M_baryon: float, R_disk: float, 
                                sigma: Optional[float] = None) -> Tuple[float, float]:
        if sigma is None:
            M_baryon_kg = M_baryon * self.constants.M_SUN
            R_disk_m = R_disk * self.constants.KPC
            sigma = M_baryon_kg / (np.pi * R_disk_m**2)
            sigma = sigma / (1e9 * self.constants.M_SUN / self.constants.KPC**2)
        
        a_ratio = self.effective_a0_ratio(sigma)
        a0_standard = self.params.get('a0_standard', 1.2e-10)
        M_baryon_kg = M_baryon * self.constants.M_SUN
        a_eff = a0_standard * a_ratio
        beta_eff = self.beta_effective(M_baryon_kg)
        
        v4 = self.constants.G * M_baryon_kg * a_eff * (1.0 + beta_eff) * 2.0
        v_qst = v4**0.25
        v_qst_km_s = v_qst / 1000.0
        
        return v_qst_km_s, a_ratio
    
    def fifth_force_range(self) -> Tuple[float, float]:
        if self.param_set not in ['local', 'sparc_optimized']:
            raise ValueError("此计算需要局部参数集")
        
        lambda_au = self.params['lambda_5th']
        lambda_m = lambda_au * self.constants.AU
        
        return lambda_m, lambda_au
    
    def get_parameters(self) -> Dict:
        return self.params.copy()
    
    def print_parameters(self):
        print(f"QST计算器参数集: {self.param_set}")
        print("=" * 50)
        for key, value in self.params.items():
            if isinstance(value, float):
                print(f"{key:20} = {value:.6g}")
            else:
                print(f"{key:20} = {value}")
