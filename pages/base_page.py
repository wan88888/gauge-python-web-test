from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = 10000  # 默认超时时间（毫秒）
        
    def navigate(self, url):
        """Navigate to the given URL"""
        self.page.goto(url, wait_until="networkidle")
        
    def get_text(self, selector):
        """Get text content of an element"""
        try:
            return self.page.text_content(selector, timeout=self.default_timeout)
        except PlaywrightTimeoutError:
            raise Exception(f"Element with selector '{selector}' not found within timeout period")
    
    def is_visible(self, selector):
        """Check if element is visible"""
        try:
            return self.page.is_visible(selector, timeout=self.default_timeout)
        except PlaywrightTimeoutError:
            return False
            
    def wait_for_selector(self, selector, state="visible"):
        """Wait for an element to be in the specified state"""
        try:
            self.page.wait_for_selector(selector, state=state, timeout=self.default_timeout)
            return True
        except PlaywrightTimeoutError:
            return False
            
    def click_element(self, selector):
        """Click on an element after waiting for it"""
        try:
            self.page.click(selector, timeout=self.default_timeout)
        except PlaywrightTimeoutError:
            raise Exception(f"Could not click element with selector '{selector}' within timeout period")
            
    def fill_text(self, selector, text):
        """Fill a text field after waiting for it"""
        try:
            self.page.fill(selector, text, timeout=self.default_timeout)
        except PlaywrightTimeoutError:
            raise Exception(f"Could not fill element with selector '{selector}' within timeout period") 