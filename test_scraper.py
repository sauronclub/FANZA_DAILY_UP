#!/usr/bin/env python3
"""
测试脚本 - 验证爬虫基本功能
"""

import os
import sys
import logging
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试模块导入"""
    print("测试模块导入...")
    try:
        from config import ID_PAYLOAD, FANZA_API_URL
        from HEADERS import headers
        print("✅ 配置模块导入成功")
        print(f"   - ID_PAYLOAD结构正常: {type(ID_PAYLOAD)}")
        print(f"   - API URL: {FANZA_API_URL}")
        print(f"   - Headers已生成: {len(headers)} 个字段")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_directory_structure():
    """测试目录结构"""
    print("\n测试目录结构...")
    try:
        output_dir = os.getenv('OUTPUT_DIR', './output')
        subdirs = ['HTML', 'DATE', 'H1', 'CID', 'logs']
        
        for subdir in subdirs:
            path = Path(output_dir) / subdir
            print(f"   - 检查目录: {path}")
            path.mkdir(parents=True, exist_ok=True)
        
        print("✅ 目录结构创建成功")
        return True
    except Exception as e:
        print(f"❌ 目录创建失败: {e}")
        return False

def test_headers():
    """测试headers生成"""
    print("\n测试Headers生成...")
    try:
        from HEADERS import headers
        
        # 检查必要的header字段（注意大小写）
        required_fields = ['user-agent', 'X-Forwarded-For', 'accept-language']
        for field in required_fields:
            if field not in headers:
                print(f"❌ 缺少必要header字段: {field}")
                return False
            print(f"   - {field}: {headers[field][:50]}...")
        
        print("✅ Headers生成正常")
        return True
    except Exception as e:
        print(f"❌ Headers测试失败: {e}")
        return False

def test_payload():
    """测试ID_PAYLOAD结构"""
    print("\n测试ID_PAYLOAD结构...")
    try:
        from config import ID_PAYLOAD
        
        # 检查必要的payload字段
        required_keys = ['operationName', 'query', 'variables']
        for key in required_keys:
            if key not in ID_PAYLOAD:
                print(f"❌ 缺少必要payload字段: {key}")
                return False
        
        # 检查variables结构
        variables = ID_PAYLOAD['variables']
        if 'id' not in variables:
            print("❌ variables中缺少id字段")
            return False
            
        print("✅ ID_PAYLOAD结构正常")
        print(f"   - Operation: {ID_PAYLOAD['operationName']}")
        print(f"   - Query长度: {len(ID_PAYLOAD['query'])} 字符")
        print(f"   - Variables: {list(variables.keys())}")
        return True
    except Exception as e:
        print(f"❌ ID_PAYLOAD测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print(" FANZA爬虫测试程序")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_directory_structure,
        test_headers,
        test_payload
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✅ 所有测试通过！代码结构正常，可以部署到GitHub Actions")
        return 0
    else:
        print("❌ 部分测试失败，请检查代码配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())