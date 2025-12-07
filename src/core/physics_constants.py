"""
量子时空统一理论 - 物理常数定义
v4.5版本 - 基于SPARC优化
"""

class PhysicalConstants:
    """物理常数"""
    
    # 基本常数
    C = 299792458.0                    # 光速 [m/s]
    G = 6.67430e-11                    # 引力常数 [m³/kg/s²]
    H0 = 2.27e-18                      # 哈勃常数 [Hz]
    H0_km_s_Mpc = 67.36                # 哈勃常数 [km/s/Mpc]
    
    # 天文单位
    M_SUN = 1.98847e30                 # 太阳质量 [kg]
    M_EARTH = 5.9722e24                # 地球质量 [kg]
    M_MARS = 6.4171e23                 # 火星质量 [kg]
    AU = 1.495978707e11                # 天文单位 [m]
    KPC = 3.085677581e19               # 千秒差距 [m]
    MPC = 3.085677581e22               # 百万秒差距 [m]
    LY = 9.461e15                      # 光年 [m]
    
    # 时间单位
    YEAR = 31556926.0                  # 年 [秒]
    
    # 其他常数
    M_PL = 2.176434e-8                 # 普朗克质量 [kg]
    M_PL_EV = 2.176434e17              # 普朗克质量 [eV]


class QSTConstants:
    """量子时空统一理论常数 v4.5"""
    
    # 场值 (归一化)
    PHI_PLUS = 1.621
    PHI_MINUS = 1.459
    OMEGA = 1.297
    
    # 基本常数
    MU = 0.00306
    V_CONST = 2.0527
    
    # v4.5优化参数 (SPARC优化报告)
    BETA0 = 0.800                      # 第五力耦合常数 (优化值)
    M_TH = 1.0e22                      # 质量阈值 [kg]
    A_LOW = 0.0150                     # 矮星系a_eff比例
    SIGMA_CRIT = 0.4                   # 临界表面密度 [10^9 M_sun/kpc²]
    SIGMA_TRANSITION = 2.5             # 过渡表面密度 [10^9 M_sun/kpc²]
    ALPHA = 1.0                        # 幂律指数 (线性过渡)
    
    # 第五力参数
    LAMBDA_5TH = 915.0                 # 第五力力程 [AU]
    M_OMEGA_5TH = 1.44e-21             # 第五力质量 [eV]
    
    # 宇宙学参数
    M_PHI_EFF = 0.08                   # m_Φ,eff/H₀
    M_OMEGA_EFF = 0.06                 # m_Ω,eff/H₀
    
    # 标准加速度
    A0_STANDARD = 1.2e-10              # m/s²
