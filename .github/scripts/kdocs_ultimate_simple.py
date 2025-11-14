#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/kdocs_ultimate_simple.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import sys

def ultimate_simple_update():
    """终极简化版本"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # 直接使用系统Chrome，避免webdriver-manager问题
    driver = webdriver.Chrome(options=options)

    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read().strip()

        print(f"更新 {len(content)} 字符")

        driver.get("https://365.kdocs.cn/l/cjpVZz0ASxGp")
        time.sleep(15)  # 延长等待时间

        # 直接使用JavaScript
        script = """
        var element = document.querySelector('#hPxWNIobEgWTpwIS .otl-paragraph-content');
        if (element) {
            element.textContent = arguments[0];
            return 'success';
        }
        return 'failed';
        """

        result = driver.execute_script(script, content)
        time.sleep(5)

        if result == 'success':
            print("✅ 更新成功！")
            return True
        else:
            print("❌ 更新失败")
            return False

    except Exception as e:
        print(f"错误: {e}")
        return False
    finally:
        driver.quit()

if __name__ == '__main__':
    success = ultimate_simple_update()
    sys.exit(0 if success else 1)
