#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# .github/scripts/kdocs_pyppeteer.py

import asyncio
import os
import sys
from pyppeteer import launch

async def update_kdocs_with_pyppeteer():
    """使用Pyppeteer更新金山文档"""
    try:
        # 启动浏览器
        browser = await launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--window-size=1920,1080'
            ]
        )

        page = await browser.newPage()
        await page.setViewport({'width': 1920, 'height': 1080})

        # 读取内容
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read().strip()

        print(f"📝 更新 {len(content)} 字符")

        # 打开页面
        await page.goto('https://365.kdocs.cn/l/cjpVZz0ASxGp', {'waitUntil': 'networkidle2'})
        await asyncio.sleep(10)

        # 方法1: 使用JavaScript直接更新
        update_script = """
        () => {
            const target = document.querySelector('#hPxWNIobEgWTpwIS .otl-paragraph-content');
            if (target) {
                target.textContent = arguments[0];

                // 触发事件
                const event = new Event('input', { bubbles: true });
                target.dispatchEvent(event);

                return true;
            }
            return false;
        }
        """

        result = await page.evaluate(update_script, content)

        if result:
            print("✅ 更新成功！")
            await asyncio.sleep(3)
            await browser.close()
            return True
        else:
            print("❌ 元素未找到")
            await browser.close()
            return False

    except Exception as e:
        print(f"💥 错误: {e}")
        if 'browser' in locals():
            await browser.close()
        return False

def main():
    # Pyppeteer需要异步运行
    success = asyncio.get_event_loop().run_until_complete(
        update_kdocs_with_pyppeteer()
    )
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
