#!/usr/bin/env python3
"""
量子時空統一理論 - 示例使用腳本

這個腳本展示了如何使用QST計算器進行基本計算。
"""

import sys
sys.path.append('src')

import numpy as np
import matplotlib.pyplot as plt
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
    masses = [1.99e30, 5.97e24, 7.35e22, 5e3, 0.001]  # 太陽、地球、月球、航天器、1g
    names = ['太陽', '地球', '月球', '航天器', '1g物體']
    
    for name, mass in zip(names, masses):
        beta_eff = calc_local.beta_effective(mass)
        print(f"  {name}: M = {mass:.2e} kg, β_eff = {beta_eff:.3f}")
    
    # 4. 星系計算示例
    print("\n4. 星系旋轉速度示例 (v4.2):")
    # 示例星系參數（來自SPARC數據）
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
    
    # 5. 繪製函數圖形
    print("\n5. 生成函數圖形...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 5.1 尺度依賴函數
    ax1 = axes[0, 0]
    masses_plot = np.logspace(-3, 30, 200)
    beta_eff_plot = [calc_local.beta_effective(m) for m in masses_plot]
    
    ax1.plot(masses_plot, beta_eff_plot, 'b-', linewidth=2)
    ax1.axvline(x=calc_local.params['M_th'], color='r', linestyle='--', 
               label=f'M_th = {calc_local.params["M_th"]:.1e} kg')
    ax1.set_xscale('log')
    ax1.set_xlabel('質量 [kg]', fontsize=12)
    ax1.set_ylabel('β_eff', fontsize=12)
    ax1.set_title('尺度依賴耦合函數 β_eff(M)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 5.2 表面密度-加速度關係
    ax2 = axes[0, 1]
    sigma_plot = np.logspace(-3, 2, 200)
    a_ratio_plot = [calc_local.effective_a0_ratio(s) for s in sigma_plot]
    
    ax2.plot(sigma_plot, a_ratio_plot, 'g-', linewidth=2)
    ax2.axvline(x=0.1, color='r', linestyle='--', label='σ_crit = 0.1')
    ax2.axvline(x=10.0, color='orange', linestyle='--', label='σ_trans = 10.0')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('表面密度 σ [10^9 M_sun/kpc²]', fontsize=12)
    ax2.set_ylabel('a_eff / a₀', fontsize=12)
    ax2.set_title('表面密度-加速度尺度關係 (QST v4.2)', fontsize=14)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend()
    
    # 5.3 星系旋轉速度示例
    ax3 = axes[1, 0]
    M_range = np.logspace(7, 11, 50)  # 10^7 到 10^11 M_sun
    v_rot_plot = []
    
    for M in M_range:
        v, _ = calc_local.galaxy_rotation_velocity(M, 2.0, None)
        v_rot_plot.append(v)
    
    ax3.plot(M_range, v_rot_plot, 'r-', linewidth=2)
    ax3.set_xscale('log')
    ax3.set_xlabel('重子質量 [M_sun]', fontsize=12)
    ax3.set_ylabel('旋轉速度 [km/s]', fontsize=12)
    ax3.set_title('星系旋轉速度 vs 重子質量', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # 5.4 誤差分析
    ax4 = axes[1, 1]
    # 實際觀測值（來自SPARC）
    obs_data = {
        'D631-7': 57.7,
        'DDO064': 46.1,
        'DDO154': 47.0,
        'DDO161': 66.3,
        'DDO168': 53.4
    }
    
    pred_speeds = []
    obs_speeds = []
    names = []
    
    for name, obs_v in obs_data.items():
        # 使用近似參數
        if name == 'D631-7':
            v_pred, _ = calc_local.galaxy_rotation_velocity(1.2e9, 2.1, 0.314)
        elif name == 'DDO064':
            v_pred, _ = calc_local.galaxy_rotation_velocity(0.8e9, 2.0, 0.240)
        elif name == 'DDO154':
            v_pred, _ = calc_local.galaxy_rotation_velocity(0.9e9, 1.8, 0.912)
        elif name == 'DDO161':
            v_pred, _ = calc_local.galaxy_rotation_velocity(1.1e9, 2.0, 0.451)
        else:  # DDO168
            v_pred, _ = calc_local.galaxy_rotation_velocity(0.7e9, 1.5, 0.197)
        
        pred_speeds.append(v_pred)
        obs_speeds.append(obs_v)
        names.append(name)
    
    x_pos = np.arange(len(names))
    width = 0.35
    
    ax4.bar(x_pos - width/2, pred_speeds, width, label='QST預測', alpha=0.7)
    ax4.bar(x_pos + width/2, obs_speeds, width, label='觀測值', alpha=0.7)
    ax4.set_xlabel('星系', fontsize=12)
    ax4.set_ylabel('旋轉速度 [km/s]', fontsize=12)
    ax4.set_title('QST預測 vs 觀測值 (矮星系)', fontsize=14)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(names, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('qst_example_plots.png', dpi=150, bbox_inches='tight')
    
    print(f"\n圖形已保存為: qst_example_plots.png")
    print("\n" + "=" * 60)
    print("示例計算完成！")
    print("更多功能請查看文檔和源代碼。")

if __name__ == "__main__":
    main()
