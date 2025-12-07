# 貢獻指南

## 🤝 歡迎貢獻！

量子時空統一理論是一個開源科學項目，我們歡迎各種形式的貢獻，包括但不限於：

### 貢獻類型
1. **理論發展**
   - 數學推導改進
   - 物理詮釋完善
   - 新預言提出

2. **數值實現**
   - 代碼優化和重構
   - 新模擬模塊開發
   - 性能提升

3. **數據分析**
   - 新觀測數據分析
   - 統計方法改進
   - 可視化工具

4. **文檔完善**
   - 理論文檔撰寫
   - 代碼文檔編寫
   - 示例和教程

5. **測試和驗證**
   - 單元測試
   - 集成測試
   - 與觀測數據對比

## 📋 貢獻流程

### 1. 報告問題
- 使用 [GitHub Issues](https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory/issues)
- 清晰描述問題
- 提供重現步驟（如果適用）
- 標記適當的標籤（bug, enhancement, question等）

### 2. 提出新功能
- 在 Issues 中討論新想法
- 描述動機和預期結果
- 如果可能，提供初步設計

### 3. 提交代碼更改
1. **Fork 倉庫**
   ```bash
   # Fork到您的GitHub賬戶
   # 然後克隆到本地
   git clone git@github.com:YOUR_USERNAME/quantum-spacetime-unified-theory.git
   cd quantum-spacetime-unified-theory
創建功能分支

bash
git checkout -b feature/your-feature-name
進行更改並提交

bash
# 進行您的更改
git add .
git commit -m "描述您的更改"

# 遵循提交信息規範：
# feat: 新功能
# fix: 修復bug
# docs: 文檔更新
# test: 測試相關
# refactor: 重構
# style: 代碼風格
# chore: 維護任務
推送並創建Pull Request

bash
git push origin feature/your-feature-name
# 然後在GitHub創建Pull Request
4. Pull Request要求
標題: 簡潔描述更改

描述: 詳細說明更改內容、動機、測試結果

關聯Issue: 如果有，關聯對應的Issue

代碼質量: 通過所有測試，符合代碼規範

🧪 開發環境設置
1. 環境準備
bash
# 克隆倉庫
git clone https://github.com/MOUNTAIN0724/quantum-spacetime-unified-theory.git
cd quantum-spacetime-unified-theory

# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安裝依賴
pip install -r requirements.txt
pip install -e .  # 可編輯模式安裝
2. 開發工具
bash
# 代碼格式化
pip install black
black src/

# 代碼檢查
pip install flake8
flake8 src/

# 類型檢查
pip install mypy
mypy src/

# 測試
pip install pytest
pytest tests/
📝 代碼規範
1. Python代碼風格
遵循 PEP 8 規範

使用 Black 自動格式化

最大行長度: 88字符

使用類型提示（Type Hints）

2. 文檔規範
所有公共函數和類都必須有文檔字符串

使用Google風格的文檔字符串

包含參數、返回值和示例

3. 測試規範
重要功能必須有單元測試

測試覆蓋率目標: >80%

使用pytest框架

4. 提交信息規範
text
類型(範圍): 簡短描述

詳細描述（可選）

相關Issue: #123
類型包括:

feat: 新功能

fix: bug修復

docs: 文檔更新

style: 代碼風格

refactor: 重構

test: 測試相關

chore: 維護任務

🔬 理論貢獻指南
1. 理論推導
保持數學嚴謹性

提供清晰的物理圖像

與現有框架兼容

2. 新預言提出
基於現有理論框架

提供具體的數值預言

說明檢驗方法和預期結果

3. 與觀測對比
使用公開的觀測數據

使用標準的統計方法

提供不確定性分析

📚 文檔貢獻
1. 理論文檔
使用Markdown格式

包含必要的數學公式（LaTeX格式）

提供清晰的圖表和示例

2. 代碼文檔
使用Sphinx生成API文檔

包含使用示例

解釋算法和實現細節

3. 教程和示例
創建Jupyter筆記本

提供逐步指南

包含可運行的代碼示例

🧪 測試指南
1. 單元測試
python
# tests/test_qst_calculator.py
import pytest
from src.core.qst_calculator import QSTCalculator

def test_dark_energy_density():
    """測試暗能量密度計算"""
    calc = QSTCalculator('effective')
    omega_de = calc.dark_energy_density()
    assert abs(omega_de - 0.690309) < 1e-6
2. 集成測試
python
# tests/test_integration.py
def test_cosmic_evolution():
    """測試宇宙演化模擬"""
    from src.simulation.cosmic_evolution import CosmicEvolver
    evolver = CosmicEvolver()
    results = evolver.evolve()
    assert results['success'] == True
3. 性能測試
python
# tests/test_performance.py
def test_simulation_speed():
    """測試模擬速度"""
    import time
    start = time.time()
    # 運行模擬
    elapsed = time.time() - start
    assert elapsed < 10.0  # 10秒內完成
🤔 常見問題
Q: 如何開始貢獻？
A: 從以下幾點開始：

閱讀現有文檔

嘗試運行現有示例

修復簡單的bug或文檔錯誤

提出改進建議

Q: 需要什麼背景知識？
A: 根據貢獻類型：

理論貢獻: 理論物理、宇宙學、廣義相對論

數值貢獻: Python編程、數值方法、科學計算

文檔貢獻: 寫作能力、Markdown、LaTeX

Q: 如何獲得幫助？
A:

查看現有文檔和示例

在GitHub Issues中提問

在GitHub Discussions中討論

聯繫核心團隊成員

Q: 貢獻會被接受嗎？
A: 只要符合以下條件就會被考慮：

符合項目目標

代碼質量合格

通過所有測試

有清晰的描述

🙏 致謝
所有貢獻者都將被列在項目的貢獻者列表中。重大貢獻者可能被邀請成為核心團隊成員。

感謝您的貢獻！

最後更新: 2024年12月
維護者: QST研究團隊
