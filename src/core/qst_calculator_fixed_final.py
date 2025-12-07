"""
最终修复版的β_eff函数
"""

def beta_eff_final(x, beta0=0.8):
    """正确的β_eff函数逻辑"""
    if x < 1e-6:
        f = 0.0
    elif x < 0.001:
        f = 0.001
    elif x < 0.01:
        f = 0.01
    elif x < 0.1:
        f = 0.1
    elif x < 0.5:      # 0.1 ≤ x < 0.5
        f = 0.5
    elif x < 0.8:      # 0.5 ≤ x < 0.8 ← x=0.5进入这里！
        f = 0.7
    elif x < 1.0:      # 0.8 ≤ x < 1.0
        # 线性插值: x=0.8时f=0.7, x=1.0时f=0.8
        f = 0.7 + 0.1 * (x - 0.8) / 0.2
    elif x < 2.0:      # 1.0 ≤ x < 2.0
        # 线性插值: x=1.0时f=0.8, x=2.0时f=0.9
        f = 0.8 + 0.1 * (x - 1.0) / 1.0
    else:              # x ≥ 2.0
        f = 0.9
    
    return beta0 * f

# 测试
test_cases = [
    (0.0000001, 0.0),
    (0.0005, 0.0008),
    (0.001, 0.0008),
    (0.005, 0.008),
    (0.05, 0.08),
    (0.1, 0.08),     # x=0.1, f=0.1 → β=0.08
    (0.3, 0.4),      # x=0.3, f=0.5 → β=0.4
    (0.5, 0.56),     # x=0.5, f=0.7 → β=0.56 ✓
    (0.8, 0.56),     # x=0.8, f=0.7 → β=0.56
    (0.9, 0.6),      # 线性插值
    (1.0, 0.64),     # x=1.0, f=0.8 → β=0.64
    (1.5, 0.68),     # 线性插值
    (2.0, 0.72),     # x=2.0, f=0.9 → β=0.72
    (3.0, 0.72),     # x>2.0, f=0.9 → β=0.72
]

print("正确的β_eff函数测试:")
all_correct = True
for x, expected in test_cases:
    beta = beta_eff_final(x)
    f = beta / 0.8
    correct = abs(beta - expected) < 1e-10
    
    status = '✓' if correct else '✗'
    print(f"x={x:.7f}: f={f:.3f}, β={beta:.6f} (期望{expected:.6f}) {status}")
    
    if not correct:
        all_correct = False
        print(f"  错误: 期望f={expected/0.8:.3f}, 实际f={f:.3f}")

if all_correct:
    print("\n✅ 所有测试通过!")
else:
    print("\n❌ 有测试失败!")
