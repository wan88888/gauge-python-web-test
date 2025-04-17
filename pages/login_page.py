from pages.base_page import BasePage
from utils.test_data import TestData

class LoginPage(BasePage):
    # 从测试数据获取URL
    URL = TestData.get_test_urls().get("login_url")
    
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    SUCCESS_MESSAGE = "#flash.success"
    ERROR_MESSAGE = "#flash.error"
    
    def open(self):
        """Open the login page"""
        self.navigate(self.URL)
        self.wait_for_selector(self.USERNAME_INPUT)
        
    def enter_username(self, username):
        """Enter username into the username field"""
        self.fill_text(self.USERNAME_INPUT, username)
        
    def enter_password(self, password):
        """Enter password into the password field"""
        self.fill_text(self.PASSWORD_INPUT, password)
        
    def click_login_button(self):
        """Click the login button"""
        self.click_element(self.LOGIN_BUTTON)
        
    def get_success_message(self):
        """Get the success message after successful login"""
        self.wait_for_selector(self.SUCCESS_MESSAGE)
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def get_error_message(self):
        """Get the error message after failed login"""
        self.wait_for_selector(self.ERROR_MESSAGE)
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_success_message_visible(self):
        """Check if success message is visible"""
        return self.is_visible(self.SUCCESS_MESSAGE)
        
    def login(self, username, password):
        """Perform login with given credentials"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
    def login_as_valid_user(self):
        """Login as a valid user using credentials from test data"""
        credentials = TestData.get_login_credentials().get("valid_user")
        self.login(credentials.get("username"), credentials.get("password"))

    def login_as_invalid_user(self):
        """Login as an invalid user using credentials from test data"""
        credentials = TestData.get_login_credentials().get("invalid_user")
        self.login(credentials.get("username"), credentials.get("password")) 