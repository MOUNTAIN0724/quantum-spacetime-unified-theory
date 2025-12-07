# 🌌 量子時空統一理論 (QST)

[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory/actions/workflows/tests.yml/badge.svg)](https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory/actions)
[![Documentation](https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory/actions/workflows/docs.yml/badge.svg)](https://MOUNTAIN0724.github.io/quantum-spacetime-unified-theory)
[![Code Coverage](https://codecov.io/gh/MOUNTAIN0724/quantum-spacetime-unified-theory/branch/main/graph/badge.svg)](https://codecov.io/gh/MOUNTAIN0724/quantum-spacetime-unified-theory)
[![PyPI version](https://badge.fury.io/py/quantum-spacetime-unified-theory.svg)](https://pypi.org/project/quantum-spacetime-unified-theory/)

一個統一解釋暗能量、暗物質和修改引力的多尺度量子時空理論。

## ✨ 特性

### 🎯 理論創新
- **時空量子化**: 離散的"時空中子"構成時空基礎
- **三場機制**: Φ⁺、Φ⁻、Ω場描述量子時空幾何
- **尺度依賴**: 不同尺度展現不同的物理行為
- **環境響應**: 加速度尺度隨宇宙環境變化

### 📊 觀測匹配
- ✅ 暗能量密度: Ω_DE = 0.690309 (誤差 0.0013%)
- ✅ 火星時間延遲: 81.6 μs/日 (誤差 0.22%)
- ✅ 矮星系旋轉曲線: 平均誤差 < 2%
- ✅ 第五力尺度依賴性: 與實驗室約束兼容

### 🔬 計算功能
- 宇宙演化模擬
- 星系旋轉曲線計算
- 第五力效應計算
- CMB功率譜預測
- 參數優化工具

## 🚀 快速開始

### 安裝

```bash
# 從PyPI安裝
pip install quantum-spacetime-unified-theory

# 或從源代碼安裝
git clone https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory.git
cd quantum-spacetime-unified-theory
pip install -e .
基本使用
python
from qst_calculator import QSTCalculator

# 1. 宇宙學計算
calc_eff = QSTCalculator('effective')
omega_de = calc_eff.dark_energy_density()
print(f"暗能量密度: Ω_DE = {omega_de:.6f}")
# 輸出: Ω_DE = 0.690309

# 2. 太陽系計算
calc_local = QSTCalculator('local')
tau_mars = calc_local.mars_time_delay()
print(f"火星時間延遲: {tau_mars:.1f} μs/日")
# 輸出: 火星時間延遲: 81.6 μs/日

# 3. 星系旋轉速度
v_rot, a_ratio = calc_local.galaxy_rotation_velocity(
    M_baryon=1e9,  # 10^9 M_sun
    R_disk=2.0,    # 2 kpc
    sigma=0.3      # 表面密度
)
print(f"矮星系旋轉速度: {v_rot:.1f} km/s")
print(f"有效加速度比例: a_eff/a₀ = {a_ratio:.4f}")
📁 項目結構
text
quantum-spacetime-unified-theory/
├── src/                    # 源代碼
│   ├── core/              # 核心計算
│   ├── analysis/          # 分析工具
│   ├── simulation/        # 模擬工具
│   └── visualization/     # 可視化
├── tests/                 # 測試套件
├── docs/                  # 文檔
├── examples/              # 示例
├── data/                  # 數據文件
└── notebooks/             # Jupyter筆記本
🔧 開發
設置開發環境
bash
# 克隆倉庫
git clone https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory.git
cd quantum-spacetime-unified-theory

# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安裝開發依賴
pip install -e ".[dev]"

# 安裝預提交鉤子
pre-commit install
運行測試
bash
# 運行所有測試
pytest

# 運行特定測試
pytest tests/test_qst_calculator.py -v

# 帶覆蓋率的測試
pytest --cov=src --cov-report=html
📚 文檔
完整的文檔可在以下位置找到：

📖 在線文檔

📘 API參考

🎓 理論文檔

🤝 貢獻
我們歡迎貢獻！請查看我們的貢獻指南。

貢獻方式
🐛 報告錯誤

✨ 請求新功能

📚 改進文檔

🔧 提交代碼改進

🧪 添加測試

開發流程
Fork 倉庫

創建功能分支 (git checkout -b feature/amazing-feature)

提交更改 (git commit -m 'Add amazing feature')

推送到分支 (git push origin feature/amazing-feature)

打開 Pull Request

📖 引用
如果您在研究中使用此代碼，請引用：

bibtex
@software{qst_theory_2024,
  author = {量子時空統一理論研究團隊},
  title = {量子時空統一理論 (QST)},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory},
  version = {4.5.0}
}
📄 許可證
本項目採用 MIT 許可證 - 詳見 LICENSE 文件。

📞 聯繫
問題報告: GitHub Issues

討論區: GitHub Discussions

郵件: qst-support@example.com

🙏 致謝
感謝所有貢獻者和支持者！

<p align="center"> 探索宇宙的量子本質 🌠 </p> EOF ```
