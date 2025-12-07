#!/usr/bin/env python3
"""
量子時空統一理論 - 示例使用腳本

這個腳本展示了如何使用QST計算器進行基本計算。
"""

import sys
sys.path.append('src')

from core.qst_calculator import QSTCalculator

def main():
    """主函數"""
    print("量子時空統一理論 - 示例計算")
    print("=" * 60)
    
    # 1. 宇宙學計算
    print("\n1. 宇宙學計算 (有效參數):")
    calc_eff = QSTCalculator('effective')
    omega_de = calc_eff.dark_energy_density()
    print(f"暗能量密度: Ω_DE = {omega_de:.6f}")
    print(f"目標值: 0.690309")
    print(f"誤差: {abs(omega_de - 0.690309)/0.690309*100:.6f}%")
    
    # 2. 太陽系計算
    print("\n2. 太陽系計算 (局部參數):")
    calc_local = QSTCalculator('local')
    tau_mars = calc_local.mars_time_delay()
    print(f"火星時間延遲: {tau_mars:.1f} μs/日")
    print(f"目標值: 81.6 μs/日")
    print(f"誤差: {abs(tau_mars - 81.6)/81.6*100:.2f}%")
    
    # 3. 尺度依賴性示例
    print("\n3. 尺度依賴性示例:")
    masses = [1.99e30, 5.97e24, 7.35e22, 5e3]  # 太陽、地球、月球、航天器
    names = ['太陽', '地球', '月球', '航天器']
    
    for name, mass in zip(names, masses):
        beta_eff = calc_local.beta_effective(mass)
        print(f"  {name}: M = {mass:.2e} kg, β_eff = {beta_eff:.3f}")
    
    # 4. 星系計算示例
    print("\n4. 星系旋轉速度示例 (v4.2):")
    # 示例星系參數
    galaxies = [
        {'name': 'D631-7', 'M_baryon': 1.2e9, 'R_disk': 2.1, 'sigma': 0.314},
        {'name': 'DDO064', 'M_baryon': 0.8e9, 'R_disk': 2.0, 'sigma': 0.240},
        {'name': 'DDO154', 'M_baryon': 0.9e9, 'R_disk': 1.8, 'sigma': 0.912},
    ]
    
    for galaxy in galaxies:
        v_rot, a_ratio = calc_local.galaxy_rotation_velocity(
            galaxy['M_baryon'], 
            galaxy['R_disk'], 
            galaxy['sigma']
        )
        print(f"  {galaxy['name']}:")
        print(f"    重子質量: {galaxy['M_baryon']:.1e} M_sun")
        print(f"    盤半徑: {galaxy['R_disk']:.1f} kpc")
        print(f"    表面密度: {galaxy['sigma']:.3f}")
        print(f"    預測速度: {v_rot:.1f} km/s")
        print(f"    a_eff/a₀: {a_ratio:.4f}")
    
    print("\n" + "=" * 60)
    print("示例計算完成！")
    print("更多功能請查看文檔和源代碼。")

if __name__ == "__main__":
    main()
