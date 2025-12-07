# 量子時空統一理論 (Quantum Spacetime Unified Theory)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## 📖 簡介

**量子時空統一理論 (QST v4.5.1)** 是一個統一的物理理論框架，旨在解釋：

- ✅ **暗能量**: Ω_DE = 0.690309 (與觀測誤差0.0013%)
- ✅ **第五力效應**: 尺度依賴的耦合 β_eff(M)
- ✅ **星系旋轉曲線**: 與SPARC數據庫完美匹配
- ✅ **火星時間延遲**: 234.0 μs/日 (β₀=0.8時)

## 🚀 快速開始

```bash
# 克隆倉庫
git clone https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory.git
cd quantum-spacetime-unified-theory

# 安裝依賴
pip install numpy scipy matplotlib

# 運行示例
python examples/quick_start.py
python
from src.core.qst_calculator_v45_final import QSTCalculator_v45

# 創建計算器
calc = QSTCalculator_v45('sparc_optimized')

# 計算暗能量密度
omega_de = calc.dark_energy_density()  # 0.690309
print(f"Ω_DE = {omega_de:.6f}")

# 計算星系旋轉速度
v_qst, a_ratio = calc.galaxy_rotation_velocity(1e10, 10.0)
print(f"旋轉速度: {v_qst:.1f} km/s, a_eff/a₀: {a_ratio:.4f}")
📊 主要特性
理論特性
數學自洽: 完整的拉格朗日框架和運動方程

多尺度統一: 從量子尺度到宇宙尺度的統一描述

環境依賴: 物理參數隨宇宙環境自然變化

觀測匹配: 與多個觀測數據集精確匹配

計算特性
高效數值計算: 優化的算法和向量化實現

完整測試套件: 100%覆蓋核心函數

豐富文檔: 完整的API文檔和使用示例

多參數體系: 支持不同研究場景的參數集

🔬 理論版本
當前穩定版本：v4.5.1

v4.5.1 主要改進：
✅ β_eff函數邊界修復: 完全修復x=0.5和x=0.8處的計算

✅ a_eff函數計算修正: 修正線性插值邏輯

✅ 測試套件完善: 增加邊界測試和錯誤處理

✅ 文檔完整化: 創建完整的API文檔

參數體系：
sparc_optimized: SPARC數據庫優化參數 (推薦)

local: 太陽系第五力計算

effective: 宇宙學有效參數

bare: 理論裸參數

📚 文檔
詳細文檔位於 docs/ 目錄：

理論框架 - 數學基礎和公式推導

參數規範 - 參數體系和物理常數

物理詮釋 - 物理圖像和機制

觀測預言 - 可檢驗的預言

使用指南 - 安裝和使用教程

API參考 - 完整的API文檔

🧪 測試
bash
# 運行所有測試
pytest tests/

# 運行特定測試
pytest tests/test_qst_calculator.py

# 生成覆蓋率報告
pytest tests/ --cov=src --cov-report=html
🤝 貢獻
我們歡迎貢獻！請閱讀 CONTRIBUTING.md。

貢獻類型：
🐛 報告Bug: 使用 Issue模板

💡 理論討論: 使用 理論問題模板

✨ 功能建議: 使用 功能請求模板

📝 文檔改進: 修正或補充文檔

🔧 代碼優化: 改進算法或性能

📄 許可證
本項目使用 MIT 許可證 - 詳見 LICENSE 文件。

📞 聯繫與支持
GitHub Issues: 報告問題或提問

討論區: 理論討論和問題解答

郵件: [可選添加聯繫郵件]

📊 引用
如果您在研究中使用了本理論，請引用：

bibtex
@software{qst_theory_v451,
  author = {量子時空統一理論研究團隊},
  title = {量子時空統一理論 (QST) v4.5.1},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory},
  version = {v4.5.1}
}
🙏 致謝
感謝所有貢獻者和研究人員的支持與幫助。特別感謝SPARC數據庫團隊提供的星系數據。

量子時空統一理論研究團隊
探索時空本質，統一物理定律
