import json
import os
from typing import Dict, Any

class TestData:
    """测试数据管理类"""
    
    @staticmethod
    def load_json_data(file_path: str) -> Dict[str, Any]:
        """从JSON文件加载测试数据"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"测试数据文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @staticmethod
    def get_login_credentials() -> Dict[str, str]:
        """获取登录凭据
        
        如果存在test_data/credentials.json文件，将从该文件加载
        否则返回默认凭据
        """
        data_file = "test_data/credentials.json"
        
        try:
            return TestData.load_json_data(data_file)
        except FileNotFoundError:
            # 如果文件不存在，则返回默认凭据
            return {
                "valid_user": {
                    "username": "tomsmith",
                    "password": "SuperSecretPassword!"
                },
                "invalid_user": {
                    "username": "invalid",
                    "password": "wrongpassword"
                }
            }
    
    @staticmethod
    def get_test_urls() -> Dict[str, str]:
        """获取测试URL
        
        如果存在test_data/urls.json文件，将从该文件加载
        否则返回默认URL
        """
        data_file = "test_data/urls.json"
        
        try:
            return TestData.load_json_data(data_file)
        except FileNotFoundError:
            # 如果文件不存在，则返回默认URL
            return {
                "base_url": "http://the-internet.herokuapp.com",
                "login_url": "http://the-internet.herokuapp.com/login"
            } 