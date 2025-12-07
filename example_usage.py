#!/usr/bin/env python3
"""
量子时空统一理论 - 示例使用脚本

这个脚本展示了如何使用QST计算器进行基本计算。
"""

import sys
sys.path.append('src')

import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（确保系统安装了中文字体）
try:
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'WenQuanYi Micro Hei', 'SimHei']
    plt.rcParams['axes.unicode_minus'] = False
except:
    print("注意：中文字体可能无法正确显示")

from core.qst_calculator import QSTCalculator

def main():
    """主函数"""
    print("量子时空统一理论 - 示例计算")
    print("=" * 60)
    
    # 1. 宇宙学计算
    print("\n1. 宇宙学计算 (有效参数):")
    calc_eff = QSTCalculator('effective')
    omega_de = calc_eff.dark_energy_density()
    print(f"暗能量密度: Ω_DE = {omega_de:.6f}")
    print(f"目标值: 0.690309")
    print(f"误差: {abs(omega_de - 0.690309)/0.690309*100:.6f}%")
    
    # 2. 太阳系计算
    print("\n2. 太阳系计算 (局部参数):")
    calc_local = QSTCalculator('local')
    tau_mars = calc_local.mars_time_delay()
    print(f"火星时间延迟: {tau_mars:.1f} μs/日")
    print(f"目标值: 81.6 μs/日")
    print(f"误差: {abs(tau_mars - 81.6)/81.6*100:.2f}%")
    
    # 3. 尺度依赖性示例
    print("\n3. 尺度依赖性示例:")
    masses = [1.99e30, 5.97e24, 7.35e22, 5e3, 0.001]  # 太阳、地球、月球、航天器、1g
    names = ['Sun', 'Earth', 'Moon', 'Spacecraft', '1g object']
    
    for name, mass in zip(names, masses):
        beta_eff = calc_local.beta_effective(mass)
        print(f"  {name}: M = {mass:.2e} kg, β_eff = {beta_eff:.4f}")
    
    # 4. 星系计算示例
    print("\n4. 星系旋转速度示例 (v4.2):")
    # 示例星系参数（来自SPARC数据）
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
        print(f"    Baryon mass: {galaxy['M_baryon']:.1e} M_sun")
        print(f"    Disk radius: {galaxy['R_disk']:.1f} kpc")
        print(f"    Surface density: {galaxy['sigma']:.3f}")
        print(f"    Predicted velocity: {v_rot:.1f} km/s")
        print(f"    a_eff/a₀: {a_ratio:.4f}")
    
    # 5. 绘制函数图形
    print("\n5. 生成函数图形...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 5.1 尺度依赖函数
    ax1 = axes[0, 0]
    masses_plot = np.logspace(-3, 30, 200)
    beta_eff_plot = [calc_local.beta_effective(m) for m in masses_plot]
    
    ax1.plot(masses_plot, beta_eff_plot, 'b-', linewidth=2)
    ax1.axvline(x=calc_local.params['M_th'], color='r', linestyle='--', 
               label=f'M_th = {calc_local.params["M_th"]:.1e} kg')
    ax1.set_xscale('log')
    ax1.set_xlabel('Mass [kg]', fontsize=12)
    ax1.set_ylabel('β_eff', fontsize=12)
    ax1.set_title('Scale-dependent coupling β_eff(M)', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 5.2 表面密度-加速度关系
    ax2 = axes[0, 1]
    sigma_plot = np.logspace(-3, 2, 200)
    a_ratio_plot = [calc_local.effective_a0_ratio(s) for s in sigma_plot]
    
    ax2.plot(sigma_plot, a_ratio_plot, 'g-', linewidth=2)
    ax2.axvline(x=0.1, color='r', linestyle='--', label='σ_crit = 0.1')
    ax2.axvline(x=10.0, color='orange', linestyle='--', label='σ_trans = 10.0')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('Surface density σ [10^9 M_sun/kpc²]', fontsize=12)
    ax2.set_ylabel('a_eff / a₀', fontsize=12)
    ax2.set_title('σ-a_eff relation (QST v4.2)', fontsize=14)
    ax2.grid(True, alpha=0.3, which='both')
    ax2.legend()
    
    # 5.3 星系旋转速度示例
    ax3 = axes[1, 0]
    M_range = np.logspace(7, 11, 50)  # 10^7 到 10^11 M_sun
    v_rot_plot = []
    
    for M in M_range:
        v, _ = calc_local.galaxy_rotation_velocity(M, 2.0, None)
        v_rot_plot.append(v)
    
    ax3.plot(M_range, v_rot_plot, 'r-', linewidth=2)
    ax3.set_xscale('log')
    ax3.set_xlabel('Baryon mass [M_sun]', fontsize=12)
    ax3.set_ylabel('Rotation velocity [km/s]', fontsize=12)
    ax3.set_title('Galaxy rotation velocity vs baryon mass', fontsize=14)
    ax3.grid(True, alpha=0.3)
    
    # 5.4 误差分析
    ax4 = axes[1, 1]
    # 实际观测值（来自SPARC）
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
        # 使用近似参数
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
    
    ax4.bar(x_pos - width/2, pred_speeds, width, label='QST prediction', alpha=0.7)
    ax4.bar(x_pos + width/2, obs_speeds, width, label='Observed', alpha=0.7)
    ax4.set_xlabel('Galaxy', fontsize=12)
    ax4.set_ylabel('Rotation velocity [km/s]', fontsize=12)
    ax4.set_title('QST prediction vs observed (dwarf galaxies)', fontsize=14)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(names, rotation=45)
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('qst_example_plots.png', dpi=150, bbox_inches='tight')
    
    print(f"\n图形已保存为: qst_example_plots.png")
    print("\n" + "=" * 60)
    print("示例计算完成！")
    print("更多功能请查看文档和源代码。")

if __name__ == "__main__":
    main()
