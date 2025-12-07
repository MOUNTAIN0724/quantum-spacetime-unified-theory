"""
量子时空统一理论 - 核心计算器 v4.5 (修复版)
"""

import numpy as np
from typing import Dict, Tuple, Optional
from .physics_constants import PhysicalConstants, QSTConstants


class QSTCalculator:
    """量子时空统一理论计算器 v4.5"""
    
    def __init__(self, param_set: str = 'sparc_optimized'):
        """
        初始化QST计算器 v4.5
        
        参数:
            param_set: 参数集选择
                - 'bare': 理论裸参数
                - 'effective': 宇宙学有效参数
                - 'local': 局部第五力参数
                - 'sparc_optimized': SPARC优化参数 (推荐，v4.5)
        """
        self.param_set = param_set
        self.constants = PhysicalConstants()
        self.qst_constants = QSTConstants()
        
        # 根据参数集选择参数
        self._setup_parameters()
        
        # 初始化计算缓存
        self._cache = {}
    
    def _setup_parameters(self):
        """设置参数"""
        if self.param_set == 'bare':
            # 理论裸参数
            self.params = {
                'phi_plus': self.qst_constants.PHI_PLUS,
                'phi_minus': self.qst_constants.PHI_MINUS,
                'omega': self.qst_constants.OMEGA,
                'm_phi': 0.935,  # m_Φ,bare/H₀
                'm_omega': 1.0,  # m_Ω,bare/H₀
                'mu': self.qst_constants.MU,
                'lambda1': 2.34e-6,
                'lambda2': 3.78e-7,
                'lambda3': 1.29e-8,
            }
        elif self.param_set == 'effective':
            # 宇宙学有效参数
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
            # 局部第五力参数
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
            # SPARC优化参数 (v4.5推荐)
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
    
    def effective_a0_ratio(self, sigma: float) -> float:
        """
        计算有效加速度比例 a_eff/a₀ - v4.5优化版本
        
        参数:
            sigma: 表面密度 [10^9 M_sun/kpc²]
            
        返回:
            a_eff/a₀ 比值
        """
        # 如果是sparc_optimized参数集，使用v4.5函数
        if self.param_set == 'sparc_optimized':
            return self._effective_a0_ratio_v45(sigma)
        
        # 否则使用兼容函数
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
        """
        计算有效加速度比例 a_eff/a₀ - v4.5内部实现
        
        参数:
            sigma: 表面密度 [10^9 M_sun/kpc²]
            
        返回:
            a_eff/a₀ 比值
        """
        A_low = self.params['A_low']
        sigma_crit = self.params['sigma_crit']
        sigma_transition = self.params['sigma_transition']
        alpha = self.params['alpha']
        
        # v4.5优化分段函数
        if sigma < sigma_crit:
            return A_low
        elif sigma < sigma_transition:
            # 线性过渡 (alpha=1.0时)
            frac = (sigma - sigma_crit) / (sigma_transition - sigma_crit)
            return A_low + (1.0 - A_low) * (frac ** alpha)
        else:
            return 1.0
    
    # 其他函数保持不变...
    def dark_energy_density(self) -> float:
        """计算暗能量密度 Ω_DE"""
        if self.param_set not in ['effective', 'sparc_optimized']:
            raise ValueError("此计算需要有效参数集")
        
        # 计算势能
        phi_plus = self.params['phi_plus']
        phi_minus = self.params['phi_minus']
        omega = self.params['omega']
        m_phi = self.params.get('m_phi', self.qst_constants.M_PHI_EFF)
        m_omega = self.params.get('m_omega', self.qst_constants.M_OMEGA_EFF)
        mu = self.params.get('mu', self.qst_constants.MU)
        V_const = self.params.get('V_const', self.qst_constants.V_CONST)
        
        # 势能计算 (归一化单位)
        V_phi = 0.5 * m_phi**2 * (phi_plus**2 + phi_minus**2)
        V_mix = -mu**2 * phi_plus * phi_minus
        V_omega = 0.5 * m_omega**2 * omega**2
        
        V_total = V_phi + V_mix + V_omega + V_const
        
        # 临界密度 (归一化单位: M_pl = H₀ = 1)
        rho_crit = 3.0
        
        # Ω_DE = V_total / ρ_crit
        Omega_DE = V_total / rho_crit
        
        return Omega_DE
    
    def mars_time_delay(self) -> float:
        """计算火星时间延迟"""
        if self.param_set not in ['local', 'sparc_optimized']:
            raise ValueError("此计算需要局部参数集")
        
        beta0 = self.params['beta0']
        
        # 火星的引力势差 (简化计算)
        delta_phi_grav = 3.386e-9
        
        # 相对时间延迟
        delta_tau_tau = beta0 * delta_phi_grav
        
        # 转换为每日微秒数
        seconds_per_day = 86400.0
        microseconds_per_second = 1e6
        
        delta_tau_per_day = delta_tau_tau * seconds_per_day * microseconds_per_second
        
        return delta_tau_per_day
    
    def beta_effective(self, M: float) -> float:
        """计算尺度依赖的耦合常数 β_eff(M)"""
        if self.param_set not in ['local', 'sparc_optimized']:
            raise ValueError("此计算需要局部参数集")
        
        beta0 = self.params['beta0']
        M_th = self.params['M_th']
        
        x = M / M_th
        
        # v4.5优化后的尺度依赖函数
        if x < 1e-6:  # 极小质量
            f = 0.0
        elif x < 0.001:
            f = 0.001
        elif x < 0.01:
            f = 0.01
        elif x < 0.1:
            f = 0.1
        elif x < 0.5:
            f = 0.5
        elif x < 0.8:
            f = 0.7
        elif x < 1.0:
            # x=0.8时f=0.7, x=1.0时f=0.8
            f = 0.7 + 0.1 * (x - 0.8) / 0.2
        elif x < 2.0:
            # x=1.0时f=0.8, x=2.0时f=0.9
            f = 0.8 + 0.1 * (x - 1.0) / 1.0
        else:
            f = 0.9
        
        beta_eff = beta0 * f
        
        return beta_eff
    
    def galaxy_rotation_velocity(self, M_baryon: float, R_disk: float, 
                                sigma: Optional[float] = None) -> Tuple[float, float]:
        """计算星系旋转速度"""
        # 如果没有提供sigma，则计算
        if sigma is None:
            # 将重子质量转换为kg
            M_baryon_kg = M_baryon * self.constants.M_SUN
            
            # 将半径转换为米
            R_disk_m = R_disk * self.constants.KPC
            
            # 计算表面密度
            sigma = M_baryon_kg / (np.pi * R_disk_m**2)
            # 转换为 [10^9 M_sun/kpc²]
            sigma = sigma / (1e9 * self.constants.M_SUN / self.constants.KPC**2)
        
        # 计算a_eff/a₀
        a_ratio = self.effective_a0_ratio(sigma)
        
        # 标准加速度
        a0_standard = self.params.get('a0_standard', 1.2e-10)
        
        # 改进的旋转速度公式
        M_baryon_kg = M_baryon * self.constants.M_SUN
        a_eff = a0_standard * a_ratio
        
        # 计算β_eff（使用星系质量）
        beta_eff = self.beta_effective(M_baryon_kg)
        
        # QST速度公式：V_qst^4 = G * M_baryon * a_eff * (1 + β_eff) * k
        k = 2.0  # 调整因子
        
        v4 = self.constants.G * M_baryon_kg * a_eff * (1.0 + beta_eff) * k
        v_qst = v4**0.25
        
        # 转换为km/s
        v_qst_km_s = v_qst / 1000.0
        
        return v_qst_km_s, a_ratio
    
    def fifth_force_range(self) -> Tuple[float, float]:
        """计算第五力力程"""
        if self.param_set not in ['local', 'sparc_optimized']:
            raise ValueError("此计算需要局部参数集")
        
        lambda_au = self.params['lambda_5th']
        lambda_m = lambda_au * self.constants.AU
        
        return lambda_m, lambda_au
    
    def get_parameters(self) -> Dict:
        """获取当前参数集"""
        return self.params.copy()
    
    def print_parameters(self):
        """打印当前参数"""
        print(f"QST计算器参数集: {self.param_set}")
        print("=" * 50)
        for key, value in self.params.items():
            if isinstance(value, float):
                print(f"{key:20} = {value:.6g}")
            else:
                print(f"{key:20} = {value}")
