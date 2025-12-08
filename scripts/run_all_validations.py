#!/usr/bin/env python3
"""
運行所有理論驗證腳本
用於本地開發和CI/CD中的全面驗證
"""

import subprocess
import sys
import os
from pathlib import Path

def run_validation(script_name, description):
    """運行單個驗證腳本"""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}")
    
    # 查找腳本路徑
    script_dir = Path(__file__).parent / "validation"
    script_path = script_dir / script_name
    
    if not script_path.exists():
        print(f"✗ 腳本不存在: {script_path}")
        return False
    
    try:
        # 設置Python路徑
        env = os.environ.copy()
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        # 運行腳本
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=300,  # 5分鐘超時
            env=env,
            cwd=project_root  # 設置工作目錄
        )
        
        # 打印輸出
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"✓ {description} 完成")
            return True
        else:
            print(f"✗ {description} 失敗 (退出碼: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"✗ {description} 超時")
        return False
    except Exception as e:
        print(f"✗ {description} 異常: {e}")
        return False

def main():
    """主函數"""
    print("="*70)
    print("量子時空統一理論 v4.5.1 全面驗證套件")
    print("="*70)
    
    validations = [
        ("validate_parameter_boundaries.py", "參數邊界條件驗證"),
        ("validate_theoretical_consistency.py", "理論自洽性驗證"),
        ("validate_observational_matches.py", "觀測匹配驗證"),
        ("validate_numerical_stability.py", "數值穩定性驗證"),
    ]
    
    results = []
    for script, description in validations:
        success = run_validation(script, description)
        results.append((description, success))
    
    # 總結
    print("\n" + "="*70)
    print("全面驗證總結")
    print("="*70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✓ 通過" if success else "✗ 失敗"
        print(f"{description:<25} {status}")
    
    print(f"\n總計: {passed}/{total} 項通過")
    
    if passed == total:
        print("\n🎉 所有驗證通過！理論框架穩健可靠")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 項驗證失敗")
        print("請檢查失敗的驗證項目")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n驗證被用戶中斷")
        sys.exit(130)
