@echo off
echo 启动社交媒体数据分析平台...
echo.

REM 检查Python是否已安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python解释器，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否已安装
echo 检查依赖...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动应用
echo 启动应用...
python init.py

pause
