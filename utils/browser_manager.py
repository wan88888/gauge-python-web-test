from playwright.sync_api import sync_playwright
import os
import datetime
import platform

class BrowserManager:
    """浏览器管理器类，负责管理Playwright浏览器实例"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.system = platform.system()  # 获取操作系统类型
    
    def get_env_var(self, var_name, default_value):
        """从环境变量获取配置"""
        return os.environ.get(var_name, default_value)
    
    def start(self):
        """启动浏览器"""
        # 获取浏览器配置
        browser_name = self.get_env_var("BROWSER", "chromium").lower()
        headless = self.get_env_var("HEADLESS", "false").lower() == "true"
        slow_mo = int(self.get_env_var("SLOW_MO", "0"))
        is_maximized = self.get_env_var("MAXIMIZED", "true").lower() == "true"
        
        # 初始化 Playwright
        self.playwright = sync_playwright().start()
        
        # 准备浏览器启动参数
        browser_args = []
        if is_maximized:
            # 添加最大化参数，根据不同系统和浏览器调整
            if self.system == "Darwin":  # macOS
                if browser_name == "chromium":
                    browser_args = ["--start-fullscreen"]
                # macOS上的Firefox和WebKit需要特殊处理
            elif self.system == "Windows":
                if browser_name == "chromium":
                    browser_args = ["--start-maximized"]
                elif browser_name == "firefox":
                    browser_args = ["--kiosk"]
            else:  # Linux和其他系统
                if browser_name == "chromium":
                    browser_args = ["--start-maximized"]
                elif browser_name == "firefox":
                    browser_args = ["--kiosk"]
        
        # 根据配置启动相应的浏览器
        if browser_name == "firefox":
            self.browser = self.playwright.firefox.launch(
                headless=headless,
                slow_mo=slow_mo,
                args=browser_args
            )
        elif browser_name == "webkit":
            self.browser = self.playwright.webkit.launch(
                headless=headless,
                slow_mo=slow_mo
            )
        else:  # 默认使用 chromium
            self.browser = self.playwright.chromium.launch(
                headless=headless,
                slow_mo=slow_mo,
                args=browser_args
            )
        
        print(f"启动浏览器: {browser_name}, 系统: {self.system}, 无头模式: {headless}, 慢速模式: {slow_mo}ms, 最大化: {is_maximized}")
    
    def stop(self):
        """停止浏览器"""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def create_context(self):
        """创建浏览器上下文和页面"""
        # 判断是否需要最大化
        is_maximized = self.get_env_var("MAXIMIZED", "true").lower() == "true"
        
        # 创建上下文
        if is_maximized:
            # 为最大化情况创建上下文
            self.context = self.browser.new_context(
                no_viewport=True,  # 禁用固定视口
                accept_downloads=True
            )
        else:
            # 浏览器设置
            viewport_width = int(self.get_env_var("VIEWPORT_WIDTH", "1280"))
            viewport_height = int(self.get_env_var("VIEWPORT_HEIGHT", "720"))
            
            # 为每个场景创建新的浏览器上下文
            self.context = self.browser.new_context(
                viewport={"width": viewport_width, "height": viewport_height},
                accept_downloads=True
            )
        
        # 创建新页面
        self.page = self.context.new_page()
        
        # 如果是最大化模式，使用多种方法确保窗口最大化
        if is_maximized:
            # 导航到一个页面，有助于最大化命令执行
            self.page.goto("about:blank")
            self._maximize_window()
            # 等待一小段时间让最大化生效
            self.page.wait_for_timeout(1000)
            # 检查窗口尺寸以确认最大化是否成功
            self._check_window_size()
        
        # 开启跟踪日志（可选）
        if self.get_env_var("TRACE", "false").lower() == "true":
            self.context.tracing.start(screenshots=True, snapshots=True)
        
        # 使页面全局可用
        os.environ["playwright_page"] = "initialized"
    
    def _maximize_window(self):
        """使用多种方法尝试最大化窗口"""
        if self.page:
            try:
                # 根据不同系统使用不同的最大化方法
                if self.system == "Darwin":  # macOS
                    self._maximize_mac_window()
                else:
                    self._maximize_standard_window()
                    
                print(f"已尝试在{self.system}系统上最大化浏览器窗口")
            except Exception as e:
                print(f"窗口最大化过程中出现错误: {str(e)}")
    
    def _maximize_mac_window(self):
        """macOS特定的窗口最大化方法"""
        # 1. 尝试使用macOS特定的键盘快捷键模拟
        self.page.keyboard.press("Meta+Control+F")  # macOS全屏快捷键
        
        # 2. 设置视口大小为屏幕大小
        screen_size = self.page.evaluate("""() => {
            return {
                width: window.screen.width,
                height: window.screen.height
            }
        }""")
        
        if screen_size and 'width' in screen_size and 'height' in screen_size:
            self.page.set_viewport_size({
                'width': screen_size['width'],
                'height': screen_size['height'] - 30  # 减去菜单栏高度
            })
        
        # 3. 尝试JavaScript全屏API
        self.page.evaluate("""() => {
            // 尝试标准的全屏API
            const elem = document.documentElement;
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) { /* Safari */
                elem.webkitRequestFullscreen();
            }
            
            // 手动调整窗口大小
            window.moveTo(0, 0);
            window.resizeTo(screen.width, screen.height);
        }""")
    
    def _maximize_standard_window(self):
        """标准窗口最大化方法，适用于Windows和Linux"""
        # 方法1: 使用CDP会话设置窗口最大化(仅适用于Chromium)
        if hasattr(self.page, 'evaluate_handle') and hasattr(self.page, 'set_viewport_size'):
            # 获取窗口尺寸信息
            screen_size = self.page.evaluate("""() => {
                return {
                    width: window.screen.availWidth,
                    height: window.screen.availHeight
                }
            }""")
            
            # 设置为最大可用大小
            if screen_size and 'width' in screen_size and 'height' in screen_size:
                # 设置尺寸稍微小于屏幕尺寸，以避免可能的滚动条
                self.page.set_viewport_size({
                    'width': screen_size['width'],
                    'height': screen_size['height'] - 50  # 减去一点空间给工具栏等
                })
        
        # 方法2: 通用JavaScript方法
        self.page.evaluate("""() => {
            // 尝试标准最大化
            if (window.outerHeight < screen.availHeight || window.outerWidth < screen.availWidth) {
                window.moveTo(0, 0);
                window.resizeTo(screen.availWidth, screen.availHeight);
            }
            
            // 尝试全屏模式
            const elem = document.documentElement;
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
            } else if (elem.webkitRequestFullscreen) { /* Safari */
                elem.webkitRequestFullscreen();
            } else if (elem.msRequestFullscreen) { /* IE11 */
                elem.msRequestFullscreen();
            }
        }""")
    
    def _check_window_size(self):
        """检查并显示当前窗口尺寸"""
        try:
            # 获取完整的窗口尺寸信息
            window_size = self.page.evaluate("""() => {
                return {
                    screen: {
                        width: window.screen.width,
                        height: window.screen.height,
                        availWidth: window.screen.availWidth,
                        availHeight: window.screen.availHeight
                    },
                    window: {
                        innerWidth: window.innerWidth,
                        innerHeight: window.innerHeight,
                        outerWidth: window.outerWidth,
                        outerHeight: window.outerHeight
                    },
                    document: {
                        clientWidth: document.documentElement.clientWidth,
                        clientHeight: document.documentElement.clientHeight,
                        offsetWidth: document.documentElement.offsetWidth,
                        offsetHeight: document.documentElement.offsetHeight
                    }
                }
            }""")
            
            print(f"屏幕尺寸: {window_size['screen']['width']}x{window_size['screen']['height']}")
            print(f"可用屏幕: {window_size['screen']['availWidth']}x{window_size['screen']['availHeight']}")
            print(f"窗口尺寸: {window_size['window']['outerWidth']}x{window_size['window']['outerHeight']}")
            print(f"内容尺寸: {window_size['window']['innerWidth']}x{window_size['window']['innerHeight']}")
            print(f"文档尺寸: {window_size['document']['clientWidth']}x{window_size['document']['clientHeight']}")
            
            # 简单比较判断是否最大化
            screen_area = window_size['screen']['availWidth'] * window_size['screen']['availHeight']
            window_area = window_size['window']['innerWidth'] * window_size['window']['innerHeight']
            ratio = window_area / screen_area if screen_area > 0 else 0
            
            if ratio > 0.9:
                print("确认: 窗口已成功最大化 (窗口面积占屏幕可用面积的90%以上)")
            else:
                print(f"警告: 窗口可能未完全最大化 (窗口面积占屏幕可用面积的{ratio:.1%})")
                
        except Exception as e:
            print(f"检查窗口尺寸时出错: {str(e)}")
    
    def close_context(self):
        """关闭浏览器上下文"""
        # 停止跟踪日志（如果启用）
        if self.get_env_var("TRACE", "false").lower() == "true":
            self.context.tracing.stop(path="trace.zip")
        
        # 每个场景后关闭上下文
        if self.context:
            self.context.close()
    
    def take_screenshot(self):
        """截取当前页面的屏幕截图"""
        if self.page:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_dir = "screenshots"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
            self.page.screenshot(path=screenshot_path, full_page=True)
            return screenshot_path
        return ""
    
    def get_page(self):
        """获取当前页面实例"""
        return self.page 