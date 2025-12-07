"""
QST计算器 - v4.1版本 (兼容层)
此模块提供v4.1参数的兼容性
"""

import numpy as np
from typing import Dict, Tuple, Optional
from .physics_constants import PhysicalConstants


class QSTConstants_v41:
    """QST v4.1 常数定义"""
    
    # 场值 (归一化)
    PHI_PLUS = 1.621
    PHI_MINUS = 1.459
    OMEGA = 1.297
    
    # 基本常数
    MU = 0.00306
    V_CONST = 2.0527
    
    # v4.1参数
    BETA0 = 0.279                      # 第五力耦合常数 (v4.1值)
    M_TH = 1.0e22                     # 质量阈值 [kg]
    
    # 第五力参数
    LAMBDA_5TH = 915.0                # 第五力力程 [AU]
    M_OMEGA_5TH = 1.44e-21            # 第五力质量 [eV]
    
    # 宇宙学参数
    M_PHI_EFF = 0.08                  # m_Φ,eff/H₀
    M_OMEGA_EFF = 0.06                # m_Ω,eff/H₀
    
    # 标准加速度
    A0_STANDARD = 1.2e-10             # m/s²


class QSTCalculator_v41:
    """量子时空统一理论计算器 v4.1"""
    
    def __init__(self, param_set: str = 'effective'):
        """
        初始化QST计算器 v4.1
        
        参数:
            param_set: 参数集选择
                - 'bare': 理论裸参数
                - 'effective': 宇宙学有效参数
                - 'local': 局部第五力参数
        """
        self.param_set = param_set
        self.constants = PhysicalConstants()
        self.qst_constants = QSTConstants_v41()
        
        self._setup_parameters()
    
    def _setup_parameters(self):
        """设置参数"""
        if self.param_set == 'local':
            self.params = {
                'phi_plus': self.qst_constants.PHI_PLUS,
                'phi_minus': self.qst_constants.PHI_MINUS,
                'omega': self.qst_constants.OMEGA,
                'm_omega_5th': self.qst_constants.M_OMEGA_5TH,
                'lambda_5th': self.qst_constants.LAMBDA_5TH,
                'beta0': self.qst_constants.BETA0,
                'M_th': self.qst_constants.M_TH,
            }
        else:
            raise ValueError("v4.1仅支持local参数集")
    
    def mars_time_delay(self) -> float:
        """计算火星时间延迟 - v4.1版本"""
        beta0 = self.params['beta0']
        delta_phi_grav = 3.386e-9
        delta_tau_tau = beta0 * delta_phi_grav
        seconds_per_day = 86400.0
        microseconds_per_second = 1e6
        delta_tau_per_day = delta_tau_tau * seconds_per_day * microseconds_per_second
        return delta_tau_per_day
    
    def beta_effective(self, M: float) -> float:
        """计算尺度依赖的耦合常数 β_eff(M) - v4.1版本"""
        beta0 = self.params['beta0']
        M_th = self.params['M_th']
        x = M / M_th
        
        # v4.1的尺度依赖函数
        if x < 1e-6:
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
            f = 0.7 + 0.1 * (x - 0.8) / 0.2
        elif x < 2.0:
            f = 0.8 + 0.1 * (x - 1.0) / 1.0
        else:
            f = 0.9
        
        beta_eff = beta0 * f
        return beta_eff
    
    def get_parameters(self) -> Dict:
        """获取当前参数集"""
        return self.params.copy()
