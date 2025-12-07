#!/usr/bin/env python3
"""量子時空統一理論快速入門腳本"""

import numpy as np
import matplotlib.pyplot as plt

def main():
    """主函數"""
    print("=" * 60)
    print("量子時空統一理論 (QST) v4.5 - 快速開始")
    print("=" * 60)
    
    # 顯示基本參數
    print("\n基本參數:")
    print(f"暗能量密度: Ω_DE = 0.690309")
    print(f"火星時間延遲: 81.6 μs/日")
    print(f"第五力力程: λ = 915 AU")
    print(f"質量閾值: M_th = 1.0e22 kg")
    
    # 創建簡單的示例圖
    print("\n創建示例圖...")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 示例數據：表面密度 vs 加速度比例
    sigma = np.logspace(-3, 1, 100)
    a_ratio = 0.001 * (sigma / 0.1)**1.5
    a_ratio[sigma >= 1.0] = 1.0
    
    ax.plot(sigma, a_ratio, 'b-', linewidth=2)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('表面密度 σ [10^9 M_sun/kpc²]')
    ax.set_ylabel('a_eff / a_0')
    ax.set_title('QST v4.5: σ-a_eff 關係')
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    plt.savefig('qst_quick_start.png', dpi=150)
    plt.show()
    
    print(f"\n示例圖已保存為: qst_quick_start.png")
    print("快速開始完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
