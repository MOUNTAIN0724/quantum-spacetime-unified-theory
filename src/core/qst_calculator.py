"""
量子時空統一理論 - 核心計算器

本模塊實現了QST理論的核心計算功能。
"""

import numpy as np
from typing import Dict, Tuple, Optional
from .physics_constants import PhysicalConstants, QSTConstants


class QSTCalculator:
    """量子時空統一理論計算器"""
    
    def __init__(self, param_set: str = 'effective'):
        """
        初始化QST計算器
        
        參數:
            param_set: 參數集選擇
                - 'bare': 理論裸參數
                - 'effective': 宇宙學有效參數
                - 'local': 局部第五力參數
        """
        self.param_set = param_set
        self.constants = PhysicalConstants()
        self.qst_constants = QSTConstants()
        
        # 根據參數集選擇參數
        self._setup_parameters()
        
        # 初始化計算緩存
        self._cache = {}
    
    def _setup_parameters(self):
        """設置參數"""
        if self.param_set == 'bare':
            # 理論裸參數
            self.params = {
                'phi_plus': QSTConstants.PHI_PLUS,
                'phi_minus': QSTConstants.PHI_MINUS,
                'omega': QSTConstants.OMEGA,
                'm_phi': 0.935,  # m_Φ,bare/H₀
                'm_omega': 1.0,  # m_Ω,bare/H₀
                'mu': QSTConstants.MU,
                'lambda1': 2.34e-6,
                'lambda2': 3.78e-7,
                'lambda3': 1.29e-8,
            }
        elif self.param_set == 'effective':
            # 宇宙學有效參數
            self.params = {
                'phi_plus': QSTConstants.PHI_PLUS,
                'phi_minus': QSTConstants.PHI_MINUS,
                'omega': QSTConstants.OMEGA,
                'm_phi': QSTConstants.M_PHI_EFF,
                'm_omega': QSTConstants.M_OMEGA_EFF,
                'mu': QSTConstants.MU,
                'V_const': QSTConstants.V_CONST,
            }
        elif self.param_set == 'local':
            # 局部第五力參數
            self.params = {
                'phi_plus': QSTConstants.PHI_PLUS,
                'phi_minus': QSTConstants.PHI_MINUS,
                'omega': QSTConstants.OMEGA,
                'm_omega_5th': QSTConstants.M_OMEGA_5TH,
                'lambda_5th': QSTConstants.LAMBDA_5TH,
                'beta0': QSTConstants.BETA0,
                'M_th': QSTConstants.M_TH,
            }
        else:
            raise ValueError(f"未知參數集: {self.param_set}")
    
    def dark_energy_density(self) -> float:
        """
        計算暗能量密度 Ω_DE
        
        返回:
            Ω_DE 數值
        """
        if self.param_set != 'effective':
            raise ValueError("此計算需要有效參數集 (param_set='effective')")
        
        # 計算勢能
        phi_plus = self.params['phi_plus']
        phi_minus = self.params['phi_minus']
        omega = self.params['omega']
        m_phi = self.params['m_phi']
        m_omega = self.params['m_omega']
        mu = self.params['mu']
        V_const = self.params['V_const']
        
        # 勢能計算 (歸一化單位)
        V_phi = 0.5 * m_phi**2 * (phi_plus**2 + phi_minus**2)
        V_mix = -mu**2 * phi_plus * phi_minus
        V_omega = 0.5 * m_omega**2 * omega**2
        
        V_total = V_phi + V_mix + V_omega + V_const
        
        # 臨界密度 (歸一化單位: M_pl = H₀ = 1)
        rho_crit = 3.0
        
        # Ω_DE = V_total / ρ_crit
        Omega_DE = V_total / rho_crit
        
        return Omega_DE
    
    def mars_time_delay(self) -> float:
        """
        計算火星時間延遲
        
        返回:
            時間延遲 [μs/日]
        """
        if self.param_set != 'local':
            raise ValueError("此計算需要局部參數集 (param_set='local')")
        
        beta0 = self.params['beta0']
        
        # 火星的引力勢差 (簡化計算)
        # 實際值需要精確軌道計算
        delta_phi_grav = 3.386e-9
        
        # 相對時間延遲
        delta_tau_tau = beta0 * delta_phi_grav
        
        # 轉換為每日微秒數
        seconds_per_day = 86400.0
        microseconds_per_second = 1e6
        
        delta_tau_per_day = delta_tau_tau * seconds_per_day * microseconds_per_second
        
        return delta_tau_per_day
    
    def beta_effective(self, M: float) -> float:
        """
        計算尺度依賴的耦合常數 β_eff(M)
        
        參數:
            M: 質量 [kg]
            
        返回:
            β_eff 數值
        """
        if self.param_set != 'local':
            raise ValueError("此計算需要局部參數集 (param_set='local')")
        
        beta0 = self.params['beta0']
        M_th = self.params['M_th']
        
        x = M / M_th
        
        # 尺度依賴函數
        if x < 1.0:
            f = np.exp(-(1.0 - x))
        else:
            f = 1.0 - np.exp(-(x - 1.0))
        
        beta_eff = beta0 * f
        
        return beta_eff
    
    def fifth_force_range(self) -> Tuple[float, float]:
        """
        計算第五力力程
        
        返回:
            (力程 [m], 力程 [AU])
        """
        if self.param_set != 'local':
            raise ValueError("此計算需要局部參數集 (param_set='local')")
        
        lambda_au = self.params['lambda_5th']
        lambda_m = lambda_au * self.constants.AU
        
        return lambda_m, lambda_au
    
    def effective_a0_ratio(self, sigma: float) -> float:
        """
        計算有效加速度比例 a_eff/a₀ (v4.2新增)
        
        參數:
            sigma: 表面密度 [10^9 M_sun/kpc²]
            
        返回:
            a_eff/a₀ 比值
        """
        # 簡化的分段函數
        if sigma < 0.001:
            return 0.0001
        elif sigma < 0.01:
            return 0.0005
        elif sigma < 0.1:
            return 0.001
        elif sigma < 0.5:
            return 0.01
        elif sigma < 5.0:
            return 0.1
        elif sigma < 50.0:
            return 0.5
        else:
            return 1.0
    
    def galaxy_rotation_velocity(self, M_baryon: float, R_disk: float, 
                                sigma: Optional[float] = None) -> Tuple[float, float]:
        """
        計算星系旋轉速度 (v4.2新增)
        
        參數:
            M_baryon: 重子質量 [M_sun]
            R_disk: 盤半徑 [kpc]
            sigma: 表面密度 [10^9 M_sun/kpc²]，如果為None則計算
            
        返回:
            (旋轉速度 [km/s], a_eff/a₀ 比值)
        """
        # 如果沒有提供sigma，則計算
        if sigma is None:
            # 將重子質量轉換為kg
            M_baryon_kg = M_baryon * self.constants.M_SUN
            
            # 將半徑轉換為米
            R_disk_m = R_disk * self.constants.KPC
            
            # 計算表面密度
            sigma = M_baryon_kg / (np.pi * R_disk_m**2)
            # 轉換為 [10^9 M_sun/kpc²]
            sigma = sigma / (1e9 * self.constants.M_SUN / self.constants.KPC**2)
        
        # 計算a_eff/a₀
        a_ratio = self.effective_a0_ratio(sigma)
        
        # 標準加速度
        a0_standard = 1.2e-10  # m/s²
        
        # 計算旋轉速度 (簡化公式)
        # V_qst^4 = G * M_baryon * a_eff
        M_baryon_kg = M_baryon * self.constants.M_SUN
        a_eff = a0_standard * a_ratio
        
        v4 = self.constants.G * M_baryon_kg * a_eff
        v_qst = v4**0.25
        
        # 轉換為km/s
        v_qst_km_s = v_qst / 1000.0
        
        return v_qst_km_s, a_ratio
    
    def print_summary(self):
        """打印計算摘要"""
        print("=" * 60)
        print("量子時空統一理論 - 計算摘要")
        print("=" * 60)
        print(f"參數集: {self.param_set}")
        print()
        
        if self.param_set == 'effective':
            omega_de = self.dark_energy_density()
            print(f"暗能量密度: Ω_DE = {omega_de:.6f}")
            print(f"  目標值: 0.690309")
            print(f"  誤差: {abs(omega_de - 0.690309)/0.690309*100:.4f}%")
        
        elif self.param_set == 'local':
            tau_mars = self.mars_time_delay()
            print(f"火星時間延遲: {tau_mars:.1f} μs/日")
            print(f"  目標值: 81.6 μs/日")
            print(f"  誤差: {abs(tau_mars - 81.6)/81.6*100:.2f}%")
            
            lambda_m, lambda_au = self.fifth_force_range()
            print(f"第五力力程: {lambda_au:.1f} AU = {lambda_m:.2e} m")
            
            # 示例計算
            masses = [5.97e24, 7.35e22, 5e3]  # 地球、月球、航天器
            names = ['地球', '月球', '航天器']
            
            print("\n尺度依賴耦合示例:")
            for name, mass in zip(names, masses):
                beta_eff = self.beta_effective(mass)
                print(f"  {name}: M = {mass:.2e} kg, β_eff = {beta_eff:.3f}")
        
        print("=" * 60)


# 測試函數
def test_qst_calculator():
    """測試QST計算器"""
    print("測試量子時空統一理論計算器")
    print("=" * 60)
    
    # 測試有效參數集
    print("\n1. 宇宙學有效參數測試:")
    calc_eff = QSTCalculator('effective')
    calc_eff.print_summary()
    
    # 測試局部參數集
    print("\n2. 局部第五力參數測試:")
    calc_local = QSTCalculator('local')
    calc_local.print_summary()
    
    # 測試星系旋轉速度計算
    print("\n3. 星系旋轉速度測試 (示例):")
    # 示例: 一個典型的矮星系
    M_baryon = 1e9  # 10^9 M_sun
    R_disk = 2.0    # 2 kpc
    sigma = 0.2     # 表面密度
    
    v_rot, a_ratio = calc_local.galaxy_rotation_velocity(M_baryon, R_disk, sigma)
    print(f"重子質量: {M_baryon:.2e} M_sun")
    print(f"盤半徑: {R_disk:.1f} kpc")
    print(f"表面密度: {sigma:.3f}")
    print(f"預測旋轉速度: {v_rot:.1f} km/s")
    print(f"a_eff/a₀: {a_ratio:.4f}")


if __name__ == "__main__":
    # 運行測試
    test_qst_calculator()
