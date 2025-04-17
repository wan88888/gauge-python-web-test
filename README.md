# Web自动化测试框架

这是一个使用Gauge、Playwright和页面对象模型(POM)设计模式的Web自动化测试框架。

## 先决条件

- Python 3.7+
- Gauge
- Playwright

## 安装

1. 创建并激活虚拟环境:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows上: venv\Scripts\activate
   ```

2. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

3. 安装Playwright浏览器:
   ```
   playwright install
   ```

## 项目结构

- `specs/`: 包含Gauge规范文件
- `step_impl/`: 包含步骤实现
- `pages/`: 包含按POM模式设计的页面对象
- `utils/`: 包含通用工具类和辅助函数
- `test_data/`: 包含测试数据文件
- `env/`: 包含环境配置

## 运行测试

运行所有测试:
```
gauge run specs
```

运行特定规范:
```
gauge run specs/login.spec
```

使用指定的环境变量运行(覆盖默认配置):
```
BROWSER=firefox HEADLESS=true gauge run specs
```

可用的环境变量:
- `BROWSER`: 选择浏览器 (chromium/firefox/webkit)
- `HEADLESS`: 无头模式 (true/false)
- `SLOW_MO`: 慢速模式，单位毫秒(ms)
- `VIEWPORT_WIDTH`/`VIEWPORT_HEIGHT`: 浏览器视窗尺寸
- `TRACE`: 是否启用Playwright跟踪 (true/false)
- `MAXIMIZED`: 是否最大化浏览器窗口 (true/false)

## 持续集成

本项目使用GitHub Actions进行持续集成测试。每当有代码推送到main/master分支或提交Pull Request时，会自动运行测试。

### GitHub Actions工作流程

工作流程文件位于 `.github/workflows/test.yml`，包含以下步骤:

1. 设置Python环境
2. 安装Gauge和相关插件
3. 安装项目依赖
4. 安装Playwright浏览器
5. 以无头模式运行测试
6. 上传测试报告和截图

### 手动触发工作流

您可以在GitHub仓库的"Actions"标签页中手动触发工作流程。

## 框架特性

- 页面对象模型(POM)设计模式提高可维护性
- Playwright提供强大的浏览器自动化能力
- Gauge提供BDD风格的规范和报告
- 灵活的配置使测试可在不同环境中运行
- 自动检测并适配不同操作系统的窗口最大化方法 