# 登录功能测试

这个规范文件测试Heroku应用测试站点的登录功能。

## 使用数据驱动成功登录

* Open the login page
* Login with username "tomsmith" and password "SuperSecretPassword!"
* Verify successful login message

## 使用分步方式成功登录

* Open the login page
* Enter valid username "tomsmith"
* Enter valid password "SuperSecretPassword!"
* Click login button
* Verify successful login message

## 使用测试数据成功登录

* Open the login page
* Login as valid user
* Verify successful login message

## 尝试用无效凭据登录

* Open the login page
* Login as invalid user
* Verify error message "Your username is invalid!" 