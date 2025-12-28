from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from flask import Flask, render_template, request

app = Flask(__name__)


@dataclass
class FinancialInputs:
    company_name: str
    fiscal_year: str
    revenue: Optional[float]
    gross_profit: Optional[float]
    operating_income: Optional[float]
    net_income: Optional[float]
    total_assets: Optional[float]
    total_liabilities: Optional[float]
    operating_cash_flow: Optional[float]
    key_strengths: str
    key_risks: str
    recommendation: str


def _to_float(value: str | None) -> Optional[float]:
    try:
        if value is None or value == "":
            return None
        return float(value)
    except ValueError:
        return None


def compute_metrics(inputs: FinancialInputs) -> dict[str, Optional[float]]:
    return {
        "gross_margin": (
            inputs.gross_profit / inputs.revenue if inputs.gross_profit and inputs.revenue else None
        ),
        "operating_margin": (
            inputs.operating_income / inputs.revenue if inputs.operating_income and inputs.revenue else None
        ),
        "net_margin": (inputs.net_income / inputs.revenue if inputs.net_income and inputs.revenue else None),
        "leverage": (
            inputs.total_liabilities / inputs.total_assets
            if inputs.total_liabilities and inputs.total_assets
            else None
        ),
        "cash_flow_coverage": (
            inputs.operating_cash_flow / inputs.total_liabilities
            if inputs.operating_cash_flow and inputs.total_liabilities
            else None
        ),
    }


def format_ratio(value: Optional[float]) -> str:
    if value is None:
        return "N/A"
    return f"{value:0.2%}" if abs(value) < 10 else f"{value:0.2f}x"


def build_report(inputs: FinancialInputs, metrics: dict[str, Optional[float]]) -> dict[str, str]:
    executive_summary = (
        f"{inputs.company_name} {inputs.fiscal_year} 财报显示收入"
        f" {inputs.revenue:,.0f}，净利润 {inputs.net_income:,.0f}。" if inputs.revenue and inputs.net_income else ""
    )

    financial_highlights = [
        f"营业收入：{inputs.revenue:,.0f}" if inputs.revenue is not None else "营业收入：未填", 
        f"毛利：{inputs.gross_profit:,.0f} (毛利率 {format_ratio(metrics['gross_margin'])})"
        if inputs.gross_profit is not None
        else "毛利：未填",
        f"营业利润：{inputs.operating_income:,.0f} (营业利润率 {format_ratio(metrics['operating_margin'])})"
        if inputs.operating_income is not None
        else "营业利润：未填",
        f"净利润：{inputs.net_income:,.0f} (净利率 {format_ratio(metrics['net_margin'])})"
        if inputs.net_income is not None
        else "净利润：未填",
        f"总资产：{inputs.total_assets:,.0f}" if inputs.total_assets is not None else "总资产：未填",
        f"总负债：{inputs.total_liabilities:,.0f} (资产负债率 {format_ratio(metrics['leverage'])})"
        if inputs.total_liabilities is not None
        else "总负债：未填",
        f"经营性现金流：{inputs.operating_cash_flow:,.0f} (债务覆盖率 {format_ratio(metrics['cash_flow_coverage'])})"
        if inputs.operating_cash_flow is not None
        else "经营性现金流：未填",
    ]

    qualitative = {
        "key_strengths": inputs.key_strengths or "暂无",
        "key_risks": inputs.key_risks or "暂无",
        "recommendation": inputs.recommendation or "待补充",
    }

    return {
        "executive_summary": executive_summary or "根据输入生成摘要。",
        "financial_highlights": financial_highlights,
        "qualitative": qualitative,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        inputs = FinancialInputs(
            company_name=request.form.get("company_name", ""),
            fiscal_year=request.form.get("fiscal_year", ""),
            revenue=_to_float(request.form.get("revenue")),
            gross_profit=_to_float(request.form.get("gross_profit")),
            operating_income=_to_float(request.form.get("operating_income")),
            net_income=_to_float(request.form.get("net_income")),
            total_assets=_to_float(request.form.get("total_assets")),
            total_liabilities=_to_float(request.form.get("total_liabilities")),
            operating_cash_flow=_to_float(request.form.get("operating_cash_flow")),
            key_strengths=request.form.get("key_strengths", ""),
            key_risks=request.form.get("key_risks", ""),
            recommendation=request.form.get("recommendation", ""),
        )

        metrics = compute_metrics(inputs)
        report = build_report(inputs, metrics)

        return render_template(
            "report.html",
            inputs=inputs,
            metrics=metrics,
            report=report,
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
