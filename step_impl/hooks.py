from getgauge.python import before_suite, after_suite, before_scenario, after_scenario, screenshot
from utils.browser_manager import BrowserManager
import os
import datetime

# 浏览器管理器实例
browser_manager = BrowserManager()

@before_suite
def before_suite():
    browser_manager.start()

@after_suite
def after_suite():
    browser_manager.stop()

@before_scenario
def before_scenario():
    browser_manager.create_context()

@after_scenario
def after_scenario():
    browser_manager.close_context()

# 注册截图函数
@screenshot
def capture_screenshot():
    return browser_manager.take_screenshot()

# 获取当前页面实例的函数 - 暴露给其他步骤使用
def get_page():
    return browser_manager.get_page() 