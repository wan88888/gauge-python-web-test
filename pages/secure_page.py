from pages.base_page import BasePage

class SecurePage(BasePage):
    # Locators
    LOGOUT_BUTTON = "a.button[href='/logout']"
    SECURE_AREA_HEADER = "h2"
    
    def is_logged_in(self):
        """Check if user is logged in by verifying the logout button is visible"""
        return self.is_visible(self.LOGOUT_BUTTON)
    
    def get_header_text(self):
        """Get the text of the page header"""
        return self.get_text(self.SECURE_AREA_HEADER) 