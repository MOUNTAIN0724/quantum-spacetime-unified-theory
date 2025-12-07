"""
量子時空統一理論 - 物理常數定義

本模塊定義了QST理論中使用的所有物理常數。
"""

# 基礎物理常數
class PhysicalConstants:
    """物理常數類"""
    
    # 基本常數
    M_PL = 2.176434e-8           # 普朗克質量 [kg]
    M_PL_eV = 2.176434e17        # 普朗克質量 [eV]
    H0 = 2.27e-18                # 哈勃常數 [Hz]
    H0_eV = 1.50e-33             # 哈勃常數 [eV]
    C = 299792458.0              # 光速 [m/s]
    G = 6.67430e-11              # 引力常數 [m³/kg/s²]
    
    # 天文單位
    AU = 1.495978707e11          # 天文單位 [m]
    LY = 9.461e15                # 光年 [m]
    PC = 3.085677581e16          # 秒差距 [m]
    KPC = 3.085677581e19         # 千秒差距 [m]
    MPC = 3.085677581e22         # 百萬秒差距 [m]
    
    # 太陽系相關
    M_SUN = 1.98847e30           # 太陽質量 [kg]
    R_SUN = 6.957e8              # 太陽半徑 [m]
    L_SUN = 3.828e26             # 太陽光度 [W]
    
    # 轉換因子
    KM_PER_S_TO_MPC = 1.0 / (H0 * MPC)  # km/s 到 Mpc 的轉換
    
    @classmethod
    def print_constants(cls):
        """打印所有常數"""
        print("量子時空統一理論 - 物理常數表")
        print("=" * 60)
        print(f"普朗克質量 M_pl = {cls.M_PL:.6e} kg")
        print(f"哈勃常數 H₀ = {cls.H0:.6e} Hz")
        print(f"光速 c = {cls.C:.6e} m/s")
        print(f"引力常數 G = {cls.G:.6e} m³/kg/s²")
        print(f"天文單位 AU = {cls.AU:.6e} m")
        print(f"太陽質量 M_sun = {cls.M_SUN:.6e} kg")
        print("=" * 60)


# QST理論特定常數
class QSTConstants:
    """QST理論特定常數"""
    
    # 場值 (歸一化到M_pl)
    PHI_PLUS = 1.621             # Φ⁺ = φ⁺/M_pl
    PHI_MINUS = 1.459            # Φ⁻ = φ⁻/M_pl
    OMEGA = 1.297                # Ω = ω/M_pl
    
    # 有效質量 (H₀單位)
    M_PHI_EFF = 0.08             # m_Φ,eff/H₀
    M_OMEGA_EFF = 0.06           # m_Ω,eff/H₀
    MU = 0.00306                 # μ/H₀
    
    # 第五力參數
    M_OMEGA_5TH = 1.44e-21       # 第五力質量 [eV]
    LAMBDA_5TH = 915.0           # 第五力力程 [AU]
    BETA0 = 0.279                # 漸近耦合常數
    M_TH = 1.0e22                # 質量閾值 [kg]
    
    # 勢能常數
    V_CONST = 2.0527             # 勢能常數
    
    @classmethod
    def print_qst_constants(cls):
        """打印QST常數"""
        print("QST理論特定常數")
        print("=" * 60)
        print(f"Φ⁺ = {cls.PHI_PLUS:.6f}")
        print(f"Φ⁻ = {cls.PHI_MINUS:.6f}")
        print(f"Ω = {cls.OMEGA:.6f}")
        print(f"m_Φ,eff/H₀ = {cls.M_PHI_EFF:.6f}")
        print(f"m_Ω,eff/H₀ = {cls.M_OMEGA_EFF:.6f}")
        print(f"μ/H₀ = {cls.MU:.6f}")
        print(f"m_Ω5th = {cls.M_OMEGA_5TH:.6e} eV")
        print(f"λ = {cls.LAMBDA_5TH:.1f} AU")
        print(f"β₀ = {cls.BETA0:.6f}")
        print(f"M_th = {cls.M_TH:.6e} kg")
        print("=" * 60)


if __name__ == "__main__":
    # 測試代碼
    PhysicalConstants.print_constants()
    print()
    QSTConstants.print_qst_constants()
