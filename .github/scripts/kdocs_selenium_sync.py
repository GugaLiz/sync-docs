#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/kdocs_selenium_sync.py

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

class KDocsSeleniumUpdater:
    def __init__(self):
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # 使用webdriver-manager自动管理ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        self.actions = ActionChains(self.driver)

    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=30):
        """等待元素出现"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, selector))
        )

    def login_to_kdocs(self, username, password):
        """登录金山文档（如果需要）"""
        try:
            # 检查是否需要登录
            login_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='login-button']")
            if login_elements:
                print("需要登录，正在执行登录流程...")
                # 这里需要根据实际登录页面调整
                # 通常需要输入用户名密码
                pass
        except Exception as e:
            print(f"登录检查失败: {e}")

    def update_document_content(self, new_content):
        """更新文档内容"""
        try:
            print("1. 正在打开金山文档...")
            # 打开金山文档
            self.driver.get("https://365.kdocs.cn/l/cjpVZz0ASxGp")
            time.sleep(10)  # 等待页面加载

            print("2. 页面加载完成，寻找编辑区域...")

            # 方法1: 直接通过ID定位内容块
            content_block = self.wait_for_element("#hPxWNIobEgWTpwIS")
            print("找到内容块")

            # 方法2: 通过class定位文本内容区域
            text_content_span = content_block.find_element(By.CSS_SELECTOR, ".otl-paragraph-content")
            print("找到文本内容区域")

            # 双击选中所有文本
            print("3. 选择现有文本...")
            self.actions.double_click(text_content_span).perform()
            time.sleep(2)

            # 清空原有内容并输入新内容
            print("4. 清空并输入新内容...")
            text_content_span.send_keys(Keys.CONTROL + "a")  # 全选
            time.sleep(1)
            text_content_span.send_keys(Keys.DELETE)  # 删除
            time.sleep(1)
            text_content_span.send_keys(new_content)  # 输入新内容
            time.sleep(2)

            # 点击页面其他区域保存（可选）
            print("5. 保存更改...")
            content_block.click()  # 点击内容块外区域
            time.sleep(3)

            # 验证内容是否更新成功
            updated_text = text_content_span.text
            if new_content.strip() in updated_text.strip():
                print("✅ 内容更新成功！")
                print(f"更新前预览: {updated_text[:50]}...")
                return True
            else:
                print("❌ 内容更新可能未成功")
                print(f"期望内容: {new_content[:50]}...")
                print(f"实际内容: {updated_text[:50]}...")
                return False

        except Exception as e:
            print(f"❌ 更新过程中出错: {e}")
            # 保存截图用于调试
            self.driver.save_screenshot("error_screenshot.png")
            print("已保存错误截图: error_screenshot.png")
            return False

    def alternative_update_method(self, new_content):
        """备选更新方法：使用JavaScript直接修改"""
        try:
            print("尝试备选更新方法...")

            # 使用JavaScript直接设置内容
            script = """
            var element = document.querySelector('#hPxWNIobEgWTpwIS .otl-paragraph-content');
            if (element) {
                element.textContent = arguments[0];
                // 触发输入事件以确保保存
                var event = new Event('input', { bubbles: true });
                element.dispatchEvent(event);
                return true;
            }
            return false;
            """

            result = self.driver.execute_script(script, new_content)
            time.sleep(3)

            if result:
                print("✅ 备选方法更新成功！")
                return True
            else:
                print("❌ 备选方法更新失败")
                return False

        except Exception as e:
            print(f"❌ 备选方法出错: {e}")
            return False

    def close(self):
        """关闭浏览器"""
        self.driver.quit()

def main():
    # 检查是否需要登录信息
    kdocs_username = os.getenv('KDOCS_USERNAME', '')
    kdocs_password = os.getenv('KDOCS_PASSWORD', '')

    try:
        # 读取README内容
        print("📖 正在读取README.md文件...")
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"📝 内容长度: {len(content)} 字符")

        if len(content.strip()) == 0:
            print("❌ README内容为空")
            return 1

        # 初始化更新器
        updater = KDocsSeleniumUpdater()

        try:
            # 尝试主要更新方法
            success = updater.update_document_content(content)

            if not success:
                print("主要方法失败，尝试备选方法...")
                success = updater.alternative_update_method(content)

            if success:
                print("🎉 文档同步完成！")
                return 0
            else:
                print("💥 所有更新方法都失败了")
                return 1

        finally:
            updater.close()

    except FileNotFoundError:
        print("❌ README.md 文件未找到")
        return 1
    except Exception as e:
        print(f"💥 发生错误: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
