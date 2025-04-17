from getgauge.python import step, data_store
from pages.login_page import LoginPage
from pages.secure_page import SecurePage
from step_impl.hooks import get_page

@step("Open the login page")
def open_login_page():
    login_page = LoginPage(get_page())
    login_page.open()
    
    # 将页面对象保存到数据存储中，以便其他步骤使用
    data_store.scenario["login_page"] = login_page

@step("Enter valid username <username>")
def enter_username(username):
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    login_page.enter_username(username)

@step("Enter valid password <password>")
def enter_password(password):
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    login_page.enter_password(password)

@step("Click login button")
def click_login_button():
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    login_page.click_login_button()
    
    # 登录后创建安全页面对象并保存
    secure_page = SecurePage(get_page())
    data_store.scenario["secure_page"] = secure_page

@step("Login with username <username> and password <password>")
def login_with_credentials(username, password):
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    login_page.login(username, password)
    
    # 登录后创建安全页面对象并保存
    secure_page = SecurePage(get_page())
    data_store.scenario["secure_page"] = secure_page

@step("Login as valid user")
def login_as_valid_user():
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    login_page.login_as_valid_user()
    
    # 登录后创建安全页面对象并保存
    secure_page = SecurePage(get_page())
    data_store.scenario["secure_page"] = secure_page

@step("Login as invalid user")
def login_as_invalid_user():
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    login_page.login_as_invalid_user()

@step("Verify successful login message")
def verify_success_message():
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    secure_page = data_store.scenario.get("secure_page") or SecurePage(get_page())
    
    # 验证是否已登录
    assert login_page.is_success_message_visible(), "成功消息不可见"
    assert "You logged into a secure area!" in login_page.get_success_message(), "成功消息文本不匹配"
    assert secure_page.is_logged_in(), "用户未登录 - 未找到注销按钮"
    assert "Secure Area" in secure_page.get_header_text(), "未找到安全区域标题"

@step("Verify error message <expected_message>")
def verify_error_message(expected_message):
    login_page = data_store.scenario.get("login_page") or LoginPage(get_page())
    
    error_message = login_page.get_error_message()
    assert expected_message in error_message, f"错误消息不匹配。预期: '{expected_message}', 实际: '{error_message}'" 