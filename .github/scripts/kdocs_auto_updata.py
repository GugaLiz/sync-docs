#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# automation/kdocs_auto_update.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class KDocsAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def login_and_update(self, content):
        """通过浏览器自动化更新文档"""
        try:
            # 打开金山文档
            self.driver.get("https://365.kdocs.cn/l/cjpVZz0ASxGp")

            # 等待页面加载
            time.sleep(15)

            # 这里需要根据实际页面结构调整选择器
            # 点击编辑按钮
            edit_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='edit-button']"))
            )
            edit_button.click()

            # 清空原有内容
            content_area = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".text-block-content-container"))
            )
            content_area.clear()

            # 输入新内容
            content_area.send_keys("xin nei ron")

            # 保存
            save_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='save-button']")
            save_button.click()

            return True

        except Exception as e:
            print(f"Automation failed: {e}")
            return False
        finally:
            self.driver.quit()
