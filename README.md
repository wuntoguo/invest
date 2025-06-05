# 投资策略回测

本仓库提供一个示例脚本，用于对美国大盘 ETF（如 QQQ、VOO 等）进行定投策略的回测。

## 环境准备

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 运行回测：
   ```bash
   python dca_backtest.py
   ```

回测脚本会从 Yahoo Finance 下载历史数据，并比较不同定投策略的表现。
