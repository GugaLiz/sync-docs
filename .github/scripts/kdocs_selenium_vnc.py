#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/kdocs_selenium_vnc.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os
import sys

class KDocsVisualUpdater:
    def __init__(self):
        # 设置Chrome选项 - 非无头模式，便于调试
        chrome_options = Options()

        # 在GitHub Actions中需要这些参数
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # 如果是本地测试，可以注释掉headless
        # chrome_options.add_argument('--headless')

        # 其他优化参数
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # 使用webdriver-manager
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.actions = ActionChains(self.driver)

        # 修改webdriver属性
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def javascript_update(self, new_content):
        """使用JavaScript直接更新内容"""
        try:
            print("1. 使用JavaScript方法更新内容...")

            # 等待页面加载
            time.sleep(10)

            # 方法1: 直接设置innerHTML
            script1 = """
            var targetElement = document.querySelector('#hPxWNIobEgWTpwIS .otl-paragraph-content');
            if (targetElement) {
                targetElement.innerHTML = arguments[0];
                // 触发各种事件以确保保存
                var inputEvent = new Event('input', { bubbles: true });
                var changeEvent = new Event('change', { bubbles: true });
                targetElement.dispatchEvent(inputEvent);
                targetElement.dispatchEvent(changeEvent);
                return 'success';
            }
            return 'element_not_found';
            """

            result1 = self.driver.execute_script(script1, new_content)
            print(f"JavaScript方法1结果: {result1}")

            if result1 == 'success':
                time.sleep(3)
                return True

            # 方法2: 通过父元素操作
            print("2. 尝试方法2...")
            script2 = """
            // 找到目标元素
            var contentSpan = document.querySelector('#hPxWNIobEgWTpwIS .otl-paragraph-content');
            if (contentSpan) {
                // 聚焦元素
                contentSpan.focus();
                // 选中所有文本
                var range = document.createRange();
                range.selectNodeContents(contentSpan);
                var selection = window.getSelection();
                selection.removeAllRanges();
                selection.addRange(range);

                // 删除选中内容并插入新内容
                document.execCommand('delete', false, null);
                document.execCommand('insertText', false, arguments[0]);

                // 触发事件
                var event = new Event('input', { bubbles: true });
                contentSpan.dispatchEvent(event);
                return 'success';
            }
            return 'element_not_found';
            """

            result2 = self.driver.execute_script(script2, new_content)
            print(f"JavaScript方法2结果: {result2}")

            time.sleep(3)
            return result2 == 'success'

        except Exception as e:
            print(f"JavaScript更新失败: {e}")
            return False

    def simple_click_update(self, new_content):
        """简化点击更新方法"""
        try:
            print("3. 尝试简化点击方法...")

            # 找到元素
            element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#hPxWNIobEgWTpwIS .otl-paragraph-content"))
            )

            print("找到目标元素，准备更新...")

            # 使用Actions链
            self.actions.move_to_element(element).click().perform()
            time.sleep(1)

            # 清空内容
            element.clear()
            time.sleep(1)

            # 输入新内容
            element.send_keys(new_content)
            time.sleep(2)

            # 点击其他地方保存
            body = self.driver.find_element(By.TAG_NAME, 'body')
            body.click()
            time.sleep(3)

            return True

        except Exception as e:
            print(f"简化点击方法失败: {e}")
            return False

    def update_content(self, new_content):
        """主要更新方法"""
        self.driver.get("https://365.kdocs.cn/l/cjpVZz0ASxGp")
        print("页面已打开，等待加载...")

        # 尝试多种方法
        methods = [
            self.javascript_update,
            self.simple_click_update
        ]

        for i, method in enumerate(methods, 1):
            print(f"\n尝试方法 {i}...")
            try:
                if method(new_content):
                    print(f"✅ 方法 {i} 成功！")
                    return True
            except Exception as e:
                print(f"方法 {i} 失败: {e}")
                # 保存截图
                self.driver.save_screenshot(f"method_{i}_error.png")

        return False

    def close(self):
        self.driver.quit()

def main():
    try:
        # 读取内容
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if not content:
            print("❌ README内容为空")
            return 1

        print(f"📝 准备更新 {len(content)} 字符")

        # 初始化更新器
        updater = KDocsVisualUpdater()

        try:
            success = updater.update_content(content)

            if success:
                print("🎉 文档更新成功！")
                return 0
            else:
                print("💥 所有方法都失败了")
                return 1

        finally:
            updater.close()

    except Exception as e:
        print(f"💥 主程序错误: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
