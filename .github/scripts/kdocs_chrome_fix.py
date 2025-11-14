#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/kdocs_chrome_fix.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import subprocess
import os

def check_chrome_installation():
    """检查Chrome安装"""
    try:
        # 检查Chrome是否安装
        result = subprocess.run(['which', 'google-chrome'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Chrome已安装: {result.stdout.strip()}")
            return True
        else:
            print("❌ Chrome未安装")
            return False
    except Exception as e:
        print(f"检查Chrome安装时出错: {e}")
        return False

def setup_chrome_driver():
    """设置Chrome驱动"""
    options = Options()

    # 基本参数
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    # 无头模式参数优化
    options.add_argument('--headless=new')  # 使用新的headless模式
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-features=VizDisplayCompositor')

    # 用户代理
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    # 实验性选项
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    try:
        # 方法1: 尝试使用系统Chrome
        print("尝试使用系统Chrome...")
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"系统Chrome失败: {e}")

        try:
            # 方法2: 使用chromedriver-autoinstaller
            print("尝试使用chromedriver-autoinstaller...")
            import chromedriver_autoinstaller
            chromedriver_autoinstaller.install()
            driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e2:
            print(f"chromedriver-autoinstaller失败: {e2}")

            try:
                # 方法3: 指定chromedriver路径
                print("尝试指定chromedriver路径...")
                from selenium.webdriver.chrome.service import Service
                service = Service('/usr/bin/chromedriver')
                driver = webdriver.Chrome(service=service, options=options)
                return driver
            except Exception as e3:
                print(f"指定路径失败: {e3}")
                return None

def update_with_js(driver, content):
    """使用JavaScript更新内容"""
    try:
        print("正在打开文档页面...")
        driver.get("https://365.kdocs.cn/l/cjpVZz0ASxGp")

        # 等待更长时间
        time.sleep(15)
        print("页面加载完成")

        # 多次尝试查找元素
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"尝试查找元素 (尝试 {attempt + 1}/{max_retries})...")

                # 使用JavaScript查找元素
                element_script = """
                return document.querySelector('#hPxWNIobEgWTpwIS .otl-paragraph-content');
                """
                element = driver.execute_script(element_script)

                if element:
                    print("✅ 找到目标元素")

                    # 更新内容
                    update_script = """
                    var element = arguments[0];
                    var newContent = arguments[1];
                    element.textContent = newContent;

                    // 触发事件
                    var inputEvent = new Event('input', { bubbles: true });
                    var changeEvent = new Event('change', { bubbles: true });
                    element.dispatchEvent(inputEvent);
                    element.dispatchEvent(changeEvent);

                    return 'success';
                    """

                    result = driver.execute_script(update_script, element, content)
                    time.sleep(5)

                    if result == 'success':
                        print("✅ 内容更新成功")
                        return True
                    else:
                        print("❌ JavaScript更新失败")

                else:
                    print("❌ 未找到目标元素")
                    # 保存页面源码用于调试
                    with open('page_source.html', 'w', encoding='utf-8') as f:
                        f.write(driver.page_source)
                    print("已保存页面源码到 page_source.html")

            except Exception as e:
                print(f"尝试 {attempt + 1} 失败: {e}")
                time.sleep(5)

        return False

    except Exception as e:
        print(f"更新过程中出错: {e}")
        return False

def main():
    print("🚀 开始金山文档同步...")

    # 检查Chrome安装
    if not check_chrome_installation():
        print("请确保Chrome已安装")
        return 1

    # 读取内容
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            print("❌ README内容为空")
            return 1

        print(f"📝 准备更新 {len(content)} 字符")

    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return 1

    # 设置Chrome驱动
    driver = setup_chrome_driver()
    if not driver:
        print("❌ 无法启动Chrome驱动")
        return 1

    try:
        # 更新内容
        success = update_with_js(driver, content)

        if success:
            print("🎉 同步完成！")
            return 0
        else:
            print("💥 同步失败")
            return 1

    except Exception as e:
        print(f"💥 主程序错误: {e}")
        return 1
    finally:
        driver.quit()

if __name__ == '__main__':
    sys.exit(main())
