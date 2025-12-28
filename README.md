# CreditReportGenerator

Automated tool for generating structured credit analysis reports based on financial data.

## 使用方式
1. 创建并激活虚拟环境（可选）：
   - macOS/Linux: `python -m venv .venv && source .venv/bin/activate`
   - Windows (PowerShell): `python -m venv .venv; .venv\\Scripts\\Activate.ps1`
2. 安装依赖：`pip install -r requirements.txt`
3. 启动服务：`python src/main.py`
4. 浏览器访问 `http://localhost:8000`，填入财务与定性信息即可生成授信报告模版。

## 查看运行效果的小提示
- 表单页面会在顶部展示标题，中央是输入表单，提交后跳转到报告预览页。
- 可以先试填示例数据（如收入 10000000、毛利 4000000、净利润 1500000、资产 8000000、负债 3000000、经营现金流 2000000）。
- 报告页会显示执行摘要、财务概览卡片、核心指标 pill 标签，以及优势/风险与授信建议板块。

## 功能概览
- 表单采集关键财务数据（收入、利润、资产负债、现金流）。
- 自动计算毛利率、净利率、资产负债率等核心指标。
- 生成标准化的执行摘要、财务概览、优势/风险与授信建议版块。
