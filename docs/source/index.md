# 量子時空統一理論 (QST) 文檔

歡迎來到量子時空統一理論的官方文檔！

## 📚 目錄

### 理論框架
- [參數規範手冊](theory/parameters.md)
- [數學框架](theory/mathematics.md)
- [物理詮釋](theory/physics.md)

### 使用指南
- [安裝指南](guides/installation.md)
- [快速開始](guides/quickstart.md)
- [API參考](api/index.md)

### 示例
- [基礎計算示例](examples/basic.md)
- [星系分析示例](examples/galaxies.md)
- [宇宙學模擬](examples/cosmology.md)

### 開發者文檔
- [貢獻指南](development/contributing.md)
- [代碼風格](development/style.md)
- [測試指南](development/testing.md)

## 🚀 快速開始

```python
from qst_calculator import QSTCalculator

# 宇宙學計算
calc = QSTCalculator('effective')
omega_de = calc.dark_energy_density()
print(f"Ω_DE = {omega_de:.6f}")  # 輸出: Ω_DE = 0.690309

# 太陽系計算
calc_local = QSTCalculator('local')
tau_mars = calc_local.mars_time_delay()
print(f"火星延遲: {tau_mars:.1f} μs/日")  # 輸出: 火星延遲: 81.6 μs/日
🔗 相關資源
GitHub倉庫

論文預印本

在線演示

📞 支持
問題報告: GitHub Issues

討論區: GitHub Discussions

郵件: qst-support@example.com
