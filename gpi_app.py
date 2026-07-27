"""
GPI Learning Lab | Investment Portfolio Management

A Streamlit learning app for conceptual, visual, and interactive understanding of
investment portfolio management. The app is written for students and focuses on
financial intuition, simplified simulations, and decision-oriented interpretation.

Important: every numerical module is a learning model, not a forecast, not
financial advice, and not an empirical asset-pricing model.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="GPI Learning Lab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# STYLE
# =============================================================================

PRIMARY = "#1E3A8A"
PRIMARY_2 = "#2563EB"
TEXT = "#0F172A"
MUTED = "#475569"
BORDER = "#CBD5E1"
BG = "#F8FAFC"
GOOD = "#059669"
WARN = "#D97706"
BAD = "#DC2626"
PURPLE = "#7C3AED"

st.markdown(
    f"""
<style>
    .block-container {{
        padding-top: 1.3rem;
        padding-bottom: 3rem;
    }}
    .main-title {{
        font-size: 2.35rem;
        line-height: 1.10;
        font-weight: 850;
        color: {PRIMARY};
        margin-bottom: 0.20rem;
    }}
    .sub-title {{
        font-size: 1.08rem;
        color: {MUTED};
        margin-bottom: 1.1rem;
    }}
    .kicker {{
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {PRIMARY};
        margin-bottom: 0.2rem;
    }}
    .concept-card {{
        background: #FFFFFF;
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 1rem 1.05rem;
        margin-bottom: 0.80rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    }}
    .anchor-card {{
        background: linear-gradient(90deg, #EFF6FF, #FFFFFF);
        border-left: 5px solid {PRIMARY_2};
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 0.8rem 0 1rem 0;
    }}
    .decision-card {{
        background: #F0FDF4;
        border-left: 5px solid #16A34A;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 0.8rem 0;
    }}
    .warning-card {{
        background: #FFF7ED;
        border-left: 5px solid #EA580C;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 0.8rem 0;
    }}
    .model-card {{
        background: #FAF5FF;
        border-left: 5px solid {PURPLE};
        border-radius: 12px;
        padding: 1rem 1.1rem;
        margin: 0.8rem 0;
    }}
    .quote-card {{
        background: linear-gradient(135deg, #1E293B, #0F172A);
        border-left: 5px solid #F59E0B;
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        margin: 0.8rem 0 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    .quote-text {{
        font-size: 1.02rem;
        font-style: italic;
        line-height: 1.5;
        color: #F8FAFC;
        margin-bottom: 0.45rem;
    }}
    .quote-author {{
        font-size: 0.88rem;
        font-weight: 700;
        color: #38BDF8;
    }}
    .quote-source {{
        font-size: 0.82rem;
        color: #94A3B8;
        font-style: italic;
    }}
    .fact-card {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 3px solid {PRIMARY_2};
        border-radius: 10px;
        padding: 0.9rem 1rem;
        height: 100%;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
    }}
    .fact-title {{
        font-size: 0.88rem;
        font-weight: 700;
        color: {PRIMARY};
        margin-bottom: 0.35rem;
    }}
    .fact-body {{
        font-size: 0.84rem;
        color: #334155;
        line-height: 1.45;
        margin-bottom: 0.45rem;
    }}
    .fact-source {{
        font-size: 0.75rem;
        color: {MUTED};
        font-style: italic;
    }}
    .small-note {{
        color: {MUTED};
        font-size: 0.92rem;
    }}
    .formula {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.35rem 0.5rem;
        display: inline-block;
    }}
    .pill {{
        display: inline-block;
        padding: 0.22rem 0.55rem;
        margin: 0.12rem;
        border-radius: 999px;
        background-color: #E0E7FF;
        color: #3730A3;
        font-size: 0.78rem;
        font-weight: 700;
    }}
    .stMetric {{
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.55rem;
    }}
</style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def money(x: float, decimals: int = 0) -> str:
    return f"US ${x:,.{decimals}f}"


def pct(x: float, decimals: int = 1) -> str:
    return f"{100*x:,.{decimals}f}%"


def pp(x: float, decimals: int = 1) -> str:
    return f"{x:,.{decimals}f}%"


def card(title: str, body: str, kind: str = "concept") -> None:
    cls = {
        "concept": "concept-card",
        "anchor": "anchor-card",
        "decision": "decision-card",
        "warning": "warning-card",
        "model": "model-card",
    }.get(kind, "concept-card")
    st.markdown(f'<div class="{cls}"><div class="kicker">{title}</div>{body}</div>', unsafe_allow_html=True)


def topic_header(title: str, subtitle: str, anchor: str, question: str) -> None:
    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{subtitle}</div>', unsafe_allow_html=True)
    card("Conceptual anchor", f"<strong>{anchor}</strong>", "anchor")
    card("Question to keep in mind", f"<strong>{question}</strong>", "decision")


def topic_cover(
    title: str,
    subtitle: str,
    quote: str,
    author: str,
    source: str,
    facts: List[Tuple[str, str, str]],
    anchor: str,
    question: str,
) -> None:
    """Enhanced header with reflection quotes and financial history highlights."""
    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{subtitle}</div>', unsafe_allow_html=True)

    # Reflection Quote
    st.markdown(
        f"""
        <div class="quote-card">
            <div class="kicker" style="color: #F59E0B; margin-bottom: 0.3rem;">Reflection for this module</div>
            <div class="quote-text">"{quote}"</div>
            <div>
                <span class="quote-author">— {author}</span>, <span class="quote-source">{source}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Historical Trivia / Curious Facts
    if facts:
        with st.expander("💡 Financial History & Literature Highlights (Curious Facts)", expanded=True):
            cols = st.columns(len(facts))
            for col, (f_title, f_body, f_src) in zip(cols, facts):
                with col:
                    st.markdown(
                        f"""
                        <div class="fact-card">
                            <div class="fact-title">📜 {f_title}</div>
                            <div class="fact-body">{f_body}</div>
                            <div class="fact-source">Source: {f_src}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            st.markdown("<div style='margin-bottom: 0.8rem;'></div>", unsafe_allow_html=True)

    card("Conceptual anchor", f"<strong>{anchor}</strong>", "anchor")
    card("Question to keep in mind", f"<strong>{question}</strong>", "decision")


def line_chart(df: pd.DataFrame, x: str, cols: List[str], title: str, y_title: str) -> go.Figure:
    fig = go.Figure()
    for col in cols:
        fig.add_trace(go.Scatter(x=df[x], y=df[col], mode="lines", name=col, hovertemplate="%{y:,.2f}<extra></extra>"))
    fig.update_layout(
        title=title,
        template="plotly_white",
        hovermode="x unified",
        height=430,
        xaxis_title=x,
        yaxis_title=y_title,
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
        margin=dict(l=15, r=15, t=55, b=90),
    )
    return fig


def bar_chart(labels: List[str], values: List[float], title: str, y_title: str, text_suffix: str = "%") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=values, text=[f"{v:,.1f}{text_suffix}" for v in values], textposition="outside"))
    fig.update_layout(
        title=title,
        template="plotly_white",
        height=390,
        yaxis_title=y_title,
        xaxis_title="",
        margin=dict(l=20, r=20, t=55, b=55),
    )
    return fig


def radar_chart(df: pd.DataFrame, label_col: str, dimensions: List[str], title: str) -> go.Figure:
    fig = go.Figure()
    for _, row in df.iterrows():
        values = [row[d] for d in dimensions]
        fig.add_trace(
            go.Scatterpolar(
                r=values + [values[0]],
                theta=dimensions + [dimensions[0]],
                fill="toself",
                name=str(row[label_col]),
            )
        )
    fig.update_layout(
        title=title,
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        template="plotly_white",
        height=470,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        margin=dict(l=20, r=20, t=60, b=90),
    )
    return fig


def scenario_label(value: float, low: float, high: float, low_label: str, mid_label: str, high_label: str) -> str:
    if value <= low:
        return low_label
    if value >= high:
        return high_label
    return mid_label


def safe_div(a: float, b: float) -> float:
    return a / b if abs(b) > 1e-12 else 0.0

# =============================================================================
# GLOSSARY DATA
# =============================================================================

GLOSSARY: List[Dict[str, str]] = [
    # Foundations
    {"Term": "Investment", "Category": "Foundations", "Definition": "A disciplined allocation of capital with a reasoned expectation of creating, preserving, or transferring value over time.", "Why it matters": "The process matters as much as the asset. A stock can be speculative if it is bought without analysis or rules."},
    {"Term": "Speculation", "Category": "Foundations", "Definition": "A position that depends mainly on someone else paying a higher price in the future, often with weak connection to value, horizon, or rules.", "Why it matters": "Speculation is not defined only by the asset. It is defined by the process and the investor's behavior."},
    {"Term": "Investment Policy Statement (IPS)", "Category": "Foundations", "Definition": "A written set of objectives, constraints, risk limits, liquidity needs, time horizon, and behavioral rules that guide investment decisions.", "Why it matters": "An IPS protects your future emotional self from improvising under market pressure."},
    {"Term": "Time horizon", "Category": "Foundations", "Definition": "The length of time capital can remain invested before it is needed for consumption, liquidity, or another objective.", "Why it matters": "A risky asset can be reasonable for a long horizon and unsuitable for a short horizon."},
    {"Term": "Liquidity", "Category": "Foundations", "Definition": "The ability to convert an asset into cash quickly, at a fair price, and with limited transaction cost.", "Why it matters": "Liquidity is valuable precisely when uncertainty rises and investors need flexibility."},
    {"Term": "Expected return", "Category": "Foundations", "Definition": "The return an investor expects to earn on average, conditional on assumptions about growth, income, valuation, risk, and time.", "Why it matters": "Expected return is not a promise. It is an estimate under assumptions."},
    {"Term": "Risk", "Category": "Foundations", "Definition": "The possibility that an investment outcome prevents the investor from meeting objectives. It includes volatility, permanent loss, liquidity failure, inflation erosion, and behavioral failure.", "Why it matters": "Risk is broader than price fluctuation."},
    {"Term": "Opportunity cost", "Category": "Foundations", "Definition": "The value of the best alternative you give up when choosing one option over another.", "Why it matters": "Holding cash, buying a bond, or investing in equities all involve giving up other possibilities."},
    {"Term": "Purchasing power", "Category": "Foundations", "Definition": "The amount of goods and services money can buy after accounting for inflation.", "Why it matters": "A nominal balance can look stable while real purchasing power declines."},
    {"Term": "Optionality", "Category": "Foundations", "Definition": "The ability to make better future choices because you have financial flexibility, liquidity, and resilience.", "Why it matters": "Investing is not only about return; it is also about preserving future choices."},

    # Macro
    {"Term": "Inflation", "Category": "Macroeconomics", "Definition": "A sustained increase in the general price level that reduces the purchasing power of money.", "Why it matters": "Inflation silently penalizes idle capital and changes real returns."},
    {"Term": "Nominal interest rate", "Category": "Macroeconomics", "Definition": "The stated interest rate before adjusting for inflation.", "Why it matters": "A high nominal rate can still be unattractive if inflation and taxes are also high."},
    {"Term": "Real interest rate", "Category": "Macroeconomics", "Definition": "The interest rate after adjusting for inflation, approximated as nominal rate minus inflation.", "Why it matters": "Real rates help evaluate whether savers are truly being compensated."},
    {"Term": "Policy rate", "Category": "Macroeconomics", "Definition": "The short-term interest rate set or influenced by a central bank to guide financial conditions.", "Why it matters": "It affects credit, savings rates, bond yields, currencies, and valuation multiples."},
    {"Term": "Basis point", "Category": "Macroeconomics", "Definition": "One hundredth of one percentage point. A 100 basis point move equals 1.00 percentage point.", "Why it matters": "Interest-rate changes are commonly expressed in basis points."},
    {"Term": "Monetary policy", "Category": "Macroeconomics", "Definition": "Central bank actions that influence interest rates, money, credit, inflation expectations, and financial conditions.", "Why it matters": "Monetary policy changes the discount rate and the opportunity cost of capital."},
    {"Term": "Fiscal policy", "Category": "Macroeconomics", "Definition": "Government decisions on spending, taxation, borrowing, and debt sustainability.", "Why it matters": "Fiscal credibility can affect sovereign yields, currency risk, and country risk premiums."},
    {"Term": "Market expectation", "Category": "Macroeconomics", "Definition": "The consensus view embedded in prices before a data release or policy announcement.", "Why it matters": "Markets often react to surprises, not to the raw data alone."},
    {"Term": "Economic surprise", "Category": "Macroeconomics", "Definition": "The difference between a reported data point and what the market expected.", "Why it matters": "A good economic number can hurt markets if it changes expectations about rates or liquidity."},
    {"Term": "Hawkish", "Category": "Macroeconomics", "Definition": "A policy tone associated with tighter monetary policy, higher rates, or stronger anti-inflation emphasis.", "Why it matters": "Hawkish surprises can pressure bonds and growth-sensitive equities."},
    {"Term": "Dovish", "Category": "Macroeconomics", "Definition": "A policy tone associated with easier monetary policy, lower rates, or greater concern about growth.", "Why it matters": "Dovish surprises can support risk assets if they reduce discount rates."},
    {"Term": "Risk-on", "Category": "Macroeconomics", "Definition": "A market environment where investors prefer riskier assets such as equities, high yield bonds, and emerging markets.", "Why it matters": "Portfolio performance often changes when global risk appetite changes."},
    {"Term": "Risk-off", "Category": "Macroeconomics", "Definition": "A market environment where investors seek safety, liquidity, and lower-risk assets.", "Why it matters": "Risk-off episodes can strengthen safe-haven assets and pressure emerging markets."},
    {"Term": "Country risk", "Category": "Macroeconomics", "Definition": "The additional risk associated with investing in a specific country because of fiscal, political, institutional, currency, or legal conditions.", "Why it matters": "In emerging markets, country risk can dominate asset-level analysis."},
    {"Term": "Currency risk", "Category": "Macroeconomics", "Definition": "The risk that exchange-rate movements change the value of an investment measured in the investor's home currency.", "Why it matters": "International diversification can reduce local risk but introduces currency exposure."},
    {"Term": "Home bias", "Category": "Macroeconomics", "Definition": "The tendency to overinvest in domestic assets because they feel familiar.", "Why it matters": "Familiarity is not the same as diversification."},

    # Markets and intermediaries
    {"Term": "Financial system", "Category": "Markets & Intermediaries", "Definition": "The network of markets, intermediaries, instruments, rules, and institutions that moves money across people, time, risk, and opportunities.", "Why it matters": "Investors rarely interact with 'the market' directly; they use channels and institutions."},
    {"Term": "Money market", "Category": "Markets & Intermediaries", "Definition": "A market for short-term instruments focused on liquidity and near-term funding.", "Why it matters": "It influences cash management, short-term rates, and liquidity choices."},
    {"Term": "Capital market", "Category": "Markets & Intermediaries", "Definition": "A market for long-term financing instruments such as bonds and equities.", "Why it matters": "It connects investors seeking returns with issuers seeking long-term capital."},
    {"Term": "Primary market", "Category": "Markets & Intermediaries", "Definition": "The market where securities are issued for the first time and capital flows to the issuer.", "Why it matters": "IPOs and bond issuances occur in the primary market."},
    {"Term": "Secondary market", "Category": "Markets & Intermediaries", "Definition": "The market where existing securities trade between investors.", "Why it matters": "Liquidity and price discovery mainly occur in secondary markets."},
    {"Term": "Broker", "Category": "Markets & Intermediaries", "Definition": "An intermediary that allows investors to buy and sell securities.", "Why it matters": "Execution quality, fees, access, custody, and regulation depend on the broker."},
    {"Term": "Custody", "Category": "Markets & Intermediaries", "Definition": "The safekeeping and administration of financial assets by a financial institution.", "Why it matters": "Operational safety is part of investment risk."},
    {"Term": "Bid", "Category": "Markets & Intermediaries", "Definition": "The highest price a buyer is currently willing to pay for an asset.", "Why it matters": "If you sell immediately, the bid is often the relevant price."},
    {"Term": "Ask", "Category": "Markets & Intermediaries", "Definition": "The lowest price a seller is currently willing to accept for an asset.", "Why it matters": "If you buy immediately, the ask is often the relevant price."},
    {"Term": "Bid-ask spread", "Category": "Markets & Intermediaries", "Definition": "The difference between the ask price and the bid price.", "Why it matters": "It is an implicit transaction cost and tends to widen in illiquid or stressed markets."},
    {"Term": "Market order", "Category": "Markets & Intermediaries", "Definition": "An order to buy or sell immediately at the best available price.", "Why it matters": "It prioritizes execution certainty over price control."},
    {"Term": "Limit order", "Category": "Markets & Intermediaries", "Definition": "An order to buy or sell only at a specified price or better.", "Why it matters": "It prioritizes price control but may not execute."},

    # Fixed income
    {"Term": "Bond", "Category": "Fixed Income", "Definition": "A debt instrument through which an issuer borrows money and promises payments according to specified terms.", "Why it matters": "Buying a bond means lending money, not becoming an owner."},
    {"Term": "Principal", "Category": "Fixed Income", "Definition": "The amount the bond issuer promises to repay at maturity, also called face value.", "Why it matters": "Principal repayment is central to bond cash flows."},
    {"Term": "Coupon", "Category": "Fixed Income", "Definition": "The periodic interest payment promised by a bond.", "Why it matters": "Coupon size affects cash income and price sensitivity."},
    {"Term": "Maturity", "Category": "Fixed Income", "Definition": "The date when the bond's principal is scheduled to be repaid.", "Why it matters": "Longer maturities usually imply greater sensitivity to interest-rate changes."},
    {"Term": "Yield to maturity (YTM)", "Category": "Fixed Income", "Definition": "The internal rate of return implied by a bond's price, coupon, maturity, and principal, assuming payments occur as scheduled and the bond is held to maturity.", "Why it matters": "YTM is an assumption-based measure, not a guaranteed realized return."},
    {"Term": "Duration", "Category": "Fixed Income", "Definition": "A measure of a bond's sensitivity to interest-rate changes.", "Why it matters": "A bond with higher duration tends to lose more value when yields rise."},
    {"Term": "Yield curve", "Category": "Fixed Income", "Definition": "A line showing yields across maturities for bonds of similar credit quality.", "Why it matters": "Its shape can signal expectations about inflation, growth, and monetary policy."},
    {"Term": "Credit risk", "Category": "Fixed Income", "Definition": "The risk that a borrower fails to make promised payments or suffers financial deterioration.", "Why it matters": "Higher yield can be compensation for higher default risk."},
    {"Term": "Reinvestment risk", "Category": "Fixed Income", "Definition": "The risk that future cash flows must be reinvested at lower rates.", "Why it matters": "A high-yielding short-term product may not be repeatable after it matures."},
    {"Term": "Sovereign bond", "Category": "Fixed Income", "Definition": "A bond issued by a national government.", "Why it matters": "It is tied to fiscal credibility, currency, inflation, and country risk."},
    {"Term": "Corporate bond", "Category": "Fixed Income", "Definition": "A bond issued by a company.", "Why it matters": "It carries business risk, credit risk, liquidity risk, and interest-rate risk."},

    # Equity
    {"Term": "Equity", "Category": "Equity", "Definition": "Ownership interest in a company, usually represented by shares.", "Why it matters": "Equity investors are residual claimants: they participate in upside but absorb business risk."},
    {"Term": "Common stock", "Category": "Equity", "Definition": "A share that typically grants voting rights and residual claim on company value.", "Why it matters": "Common shareholders benefit from growth but rank behind creditors."},
    {"Term": "Preferred stock", "Category": "Equity", "Definition": "An equity-like security with priority over common stock for dividends or liquidation, often with limited upside.", "Why it matters": "It blends equity and income characteristics."},
    {"Term": "ADR", "Category": "Equity", "Definition": "American Depositary Receipt: a U.S.-traded certificate representing shares of a foreign company.", "Why it matters": "It gives foreign exposure but may add currency, custody, and structural considerations."},
    {"Term": "Dividend", "Category": "Equity", "Definition": "A distribution of company earnings to shareholders.", "Why it matters": "Dividends are one component of total return, but high dividends are not automatically attractive."},
    {"Term": "Dividend yield", "Category": "Equity", "Definition": "Annual dividend per share divided by the share price.", "Why it matters": "A very high yield may signal opportunity or a dividend trap."},
    {"Term": "Intrinsic value", "Category": "Equity", "Definition": "An estimate of the present value of future cash flows an asset can generate.", "Why it matters": "Price is observable; value is estimated."},
    {"Term": "Discounted cash flow (DCF)", "Category": "Equity", "Definition": "A valuation method that estimates value by discounting expected future cash flows to the present.", "Why it matters": "DCF forces you to connect value to cash flows, growth, risk, and time."},
    {"Term": "P/E ratio", "Category": "Equity", "Definition": "Price per share divided by earnings per share.", "Why it matters": "It shows how much investors pay for current earnings, but it can mislead when earnings are cyclical or distorted."},
    {"Term": "P/B ratio", "Category": "Equity", "Definition": "Market price divided by book value per share.", "Why it matters": "Useful for some financial or asset-heavy firms, less informative for intangible-heavy businesses."},
    {"Term": "P/S ratio", "Category": "Equity", "Definition": "Market capitalization divided by revenue.", "Why it matters": "It can be useful when earnings are negative, but it ignores profitability."},
    {"Term": "Market capitalization", "Category": "Equity", "Definition": "Share price multiplied by shares outstanding.", "Why it matters": "It measures market value of equity and affects index weights."},
    {"Term": "Value stock", "Category": "Equity", "Definition": "A stock trading at relatively low valuation multiples compared with fundamentals.", "Why it matters": "Cheap can mean undervalued, but it can also mean impaired."},
    {"Term": "Growth stock", "Category": "Equity", "Definition": "A stock whose valuation depends heavily on expected future growth.", "Why it matters": "Growth stocks are often sensitive to interest rates and expectations."},

    # Funds and ETFs
    {"Term": "Index", "Category": "Funds & ETFs", "Definition": "A rules-based representation of a market, sector, asset class, or strategy.", "Why it matters": "An index is a methodology, not the market itself."},
    {"Term": "ETF", "Category": "Funds & ETFs", "Definition": "Exchange-traded fund: an investment vehicle that holds a portfolio and trades on an exchange like a stock.", "Why it matters": "ETFs can provide diversified exposure, but structure, costs, liquidity, domicile, and tax treatment matter."},
    {"Term": "Mutual fund", "Category": "Funds & ETFs", "Definition": "A pooled investment vehicle whose shares are usually bought or redeemed at net asset value after market close.", "Why it matters": "Mutual funds differ from ETFs in pricing, liquidity, cost, and trading mechanics."},
    {"Term": "NAV", "Category": "Funds & ETFs", "Definition": "Net asset value: the value of a fund's assets minus liabilities, divided by shares outstanding.", "Why it matters": "NAV is the economic value reference for funds."},
    {"Term": "Tracking error", "Category": "Funds & ETFs", "Definition": "The volatility of the difference between a fund's return and its benchmark's return.", "Why it matters": "It measures how closely a fund follows its benchmark."},
    {"Term": "Expense ratio", "Category": "Funds & ETFs", "Definition": "The annual operating cost of a fund expressed as a percentage of assets.", "Why it matters": "Costs compound negatively over time."},
    {"Term": "Physical replication", "Category": "Funds & ETFs", "Definition": "A fund replication method that holds the actual underlying securities, fully or by sampling.", "Why it matters": "It affects transparency, costs, and tracking."},
    {"Term": "Synthetic replication", "Category": "Funds & ETFs", "Definition": "A fund replication method using derivatives such as swaps to obtain index exposure.", "Why it matters": "It can improve access or tracking but adds counterparty risk."},
    {"Term": "Benchmark", "Category": "Funds & ETFs", "Definition": "A reference portfolio or index used to evaluate performance and risk.", "Why it matters": "Without the right benchmark, performance evaluation is weak."},
    {"Term": "Active management", "Category": "Funds & ETFs", "Definition": "An investment approach that seeks to outperform a benchmark through selection, timing, or allocation decisions.", "Why it matters": "The challenge is achieving outperformance after costs and taxes."},
    {"Term": "Passive investing", "Category": "Funds & ETFs", "Definition": "An investment approach that seeks to replicate a market or index at low cost.", "Why it matters": "It emphasizes diversification, low fees, and discipline."},

    # Risk and portfolio theory
    {"Term": "Simple return", "Category": "Risk & Portfolio Theory", "Definition": "Percentage change in wealth over a period: ending value divided by beginning value minus one.", "Why it matters": "It is intuitive and directly linked to investor wealth."},
    {"Term": "Log return", "Category": "Risk & Portfolio Theory", "Definition": "The natural logarithm of ending value divided by beginning value.", "Why it matters": "Log returns are additive over time and useful in modeling."},
    {"Term": "Arithmetic mean", "Category": "Risk & Portfolio Theory", "Definition": "The simple average of period returns.", "Why it matters": "It can overstate long-term compound growth when volatility is high."},
    {"Term": "Geometric mean", "Category": "Risk & Portfolio Theory", "Definition": "The compound average growth rate over multiple periods.", "Why it matters": "It better reflects actual long-term wealth growth."},
    {"Term": "Volatility", "Category": "Risk & Portfolio Theory", "Definition": "The standard deviation of returns, commonly used as a measure of price variability.", "Why it matters": "Volatility affects emotional pressure and compounded wealth, but it is not the only kind of risk."},
    {"Term": "Systematic risk", "Category": "Risk & Portfolio Theory", "Definition": "Risk associated with broad market or macro forces that cannot be diversified away easily.", "Why it matters": "Asset pricing theory says investors should be compensated mainly for systematic risk."},
    {"Term": "Idiosyncratic risk", "Category": "Risk & Portfolio Theory", "Definition": "Risk specific to a company, issuer, sector, or security.", "Why it matters": "Diversification can reduce much of this risk."},
    {"Term": "Beta", "Category": "Risk & Portfolio Theory", "Definition": "A measure of an asset's sensitivity to market movements.", "Why it matters": "Beta is about systematic exposure, not total risk."},
    {"Term": "Correlation", "Category": "Risk & Portfolio Theory", "Definition": "A standardized measure of how two assets move together, ranging from -1 to +1.", "Why it matters": "Diversification depends on imperfect correlation."},
    {"Term": "Covariance", "Category": "Risk & Portfolio Theory", "Definition": "A measure of how two asset returns move together in their own units.", "Why it matters": "Portfolio risk depends on covariance among assets."},
    {"Term": "Efficient frontier", "Category": "Risk & Portfolio Theory", "Definition": "The set of portfolios offering the highest expected return for each level of risk, or lowest risk for each level of expected return.", "Why it matters": "It visualizes the trade-off between risk and return."},
    {"Term": "Minimum-variance portfolio", "Category": "Risk & Portfolio Theory", "Definition": "The portfolio with the lowest possible volatility among the available assets.", "Why it matters": "It shows how weights and correlations shape portfolio risk."},
    {"Term": "Sharpe ratio", "Category": "Risk & Portfolio Theory", "Definition": "Excess return over the risk-free rate divided by volatility.", "Why it matters": "It compares return per unit of risk, but it relies on assumptions about volatility."},
    {"Term": "CAPM", "Category": "Risk & Portfolio Theory", "Definition": "Capital Asset Pricing Model: a model linking expected return to the risk-free rate, market risk premium, and beta.", "Why it matters": "It formalizes the idea that only systematic risk should be rewarded."},
    {"Term": "Security Market Line", "Category": "Risk & Portfolio Theory", "Definition": "A line showing the CAPM relationship between beta and expected return.", "Why it matters": "It helps interpret whether expected returns are high or low for a given beta."},
    {"Term": "Factor investing", "Category": "Risk & Portfolio Theory", "Definition": "Investing by targeting systematic characteristics such as value, size, momentum, quality, or low volatility.", "Why it matters": "It connects empirical return patterns with portfolio construction."},
    {"Term": "Value at Risk (VaR)", "Category": "Risk & Portfolio Theory", "Definition": "A statistical estimate of the maximum expected loss over a horizon at a given confidence level under model assumptions.", "Why it matters": "VaR is useful but can hide what happens in the tail."},
    {"Term": "Stress test", "Category": "Risk & Portfolio Theory", "Definition": "An analysis of how a portfolio could behave under severe but plausible scenarios.", "Why it matters": "Stress testing asks what happens when normal assumptions fail."},
    {"Term": "Tail risk", "Category": "Risk & Portfolio Theory", "Definition": "The risk of extreme outcomes that occur more often or more severely than standard models imply.", "Why it matters": "Tail events can dominate long-term investment survival."},
    {"Term": "Drawdown", "Category": "Risk & Portfolio Theory", "Definition": "The decline from a portfolio peak to a subsequent trough.", "Why it matters": "Drawdowns measure the emotional and financial stress of losses."},

    # Performance, behavior, frictions
    {"Term": "Rebalancing", "Category": "Performance, Behavior & Frictions", "Definition": "The process of restoring a portfolio to its target allocation after market movements change the weights.", "Why it matters": "Rebalancing converts discipline into a rule."},
    {"Term": "Asset allocation", "Category": "Performance, Behavior & Frictions", "Definition": "The decision of how to distribute portfolio capital across asset classes such as equities, bonds, cash, and alternatives.", "Why it matters": "Allocation often explains a large share of portfolio outcomes."},
    {"Term": "Security selection", "Category": "Performance, Behavior & Frictions", "Definition": "The choice of specific securities within an asset class.", "Why it matters": "It is different from deciding the broad asset-class mix."},
    {"Term": "Performance attribution", "Category": "Performance, Behavior & Frictions", "Definition": "A method for explaining where portfolio returns came from: allocation, selection, currency, fees, or other effects.", "Why it matters": "It separates luck from decisions more clearly."},
    {"Term": "Gross return", "Category": "Performance, Behavior & Frictions", "Definition": "Return before costs, taxes, and other frictions.", "Why it matters": "Investors do not spend gross returns."},
    {"Term": "Net return", "Category": "Performance, Behavior & Frictions", "Definition": "Return after costs, fees, taxes, spreads, and other frictions.", "Why it matters": "Net return is what actually matters for wealth."},
    {"Term": "Turnover", "Category": "Performance, Behavior & Frictions", "Definition": "The rate at which a portfolio buys and sells holdings over a period.", "Why it matters": "High turnover can increase taxes, spreads, commissions, and behavioral mistakes."},
    {"Term": "Slippage", "Category": "Performance, Behavior & Frictions", "Definition": "The difference between the expected execution price and the actual execution price.", "Why it matters": "It is an often invisible execution cost."},
    {"Term": "Loss aversion", "Category": "Performance, Behavior & Frictions", "Definition": "The tendency for losses to hurt more than equivalent gains feel good.", "Why it matters": "It can trigger panic selling or refusal to realize losses."},
    {"Term": "Disposition effect", "Category": "Performance, Behavior & Frictions", "Definition": "The tendency to sell winners too early and hold losers too long.", "Why it matters": "It is a common investor behavior that weakens portfolio discipline."},
    {"Term": "Overconfidence", "Category": "Performance, Behavior & Frictions", "Definition": "Excessive belief in one's own forecasting ability, knowledge, or control.", "Why it matters": "Overconfidence often increases trading and concentration."},
    {"Term": "Confirmation bias", "Category": "Performance, Behavior & Frictions", "Definition": "The tendency to seek information that confirms existing beliefs.", "Why it matters": "It prevents investors from updating when evidence changes."},
    {"Term": "Herd behavior", "Category": "Performance, Behavior & Frictions", "Definition": "The tendency to follow the crowd rather than independent analysis.", "Why it matters": "Herding can amplify bubbles, crashes, and FOMO."},
    {"Term": "FOMO", "Category": "Performance, Behavior & Frictions", "Definition": "Fear of missing out: anxiety that others are profiting from an opportunity you are not taking.", "Why it matters": "FOMO can turn a portfolio process into impulse chasing."},
    {"Term": "Bubble", "Category": "Performance, Behavior & Frictions", "Definition": "A market episode where prices become strongly disconnected from fundamentals, often supported by narrative, leverage, and social reinforcement.", "Why it matters": "Bubbles teach that price momentum can look like evidence until it breaks."},

    # Alternatives and tech
    {"Term": "Alternative assets", "Category": "Alternatives & Technology", "Definition": "Investments outside traditional public stocks, bonds, and cash, such as real estate, commodities, private equity, hedge funds, or cryptoassets.", "Why it matters": "Alternatives can diversify, but they can also add cost, complexity, illiquidity, and opacity."},
    {"Term": "REIT", "Category": "Alternatives & Technology", "Definition": "Real Estate Investment Trust: a vehicle that owns or finances income-producing real estate and often trades like a stock.", "Why it matters": "It provides real estate exposure without direct property ownership, but still carries market and rate sensitivity."},
    {"Term": "Commodity", "Category": "Alternatives & Technology", "Definition": "A raw material or primary good such as oil, gold, copper, or agricultural products.", "Why it matters": "Commodities can hedge some risks but are volatile and often do not generate cash flows."},
    {"Term": "Cryptoasset", "Category": "Alternatives & Technology", "Definition": "A digital asset recorded on a distributed ledger or blockchain-based system.", "Why it matters": "Its investment role must be assessed critically: liquidity, regulation, custody, narrative risk, and volatility matter."},
    {"Term": "Robo-advisor", "Category": "Alternatives & Technology", "Definition": "A digital platform that automates portfolio recommendations or management based on user information and algorithms.", "Why it matters": "Automation can help discipline but does not eliminate the need for judgment."},
    {"Term": "Overfitting", "Category": "Alternatives & Technology", "Definition": "Building a model that fits historical data too closely but performs poorly out of sample.", "Why it matters": "Many attractive backtests fail because they learned noise instead of robust patterns."},
]

# =============================================================================
# SIDEBAR
# =============================================================================

st.sidebar.markdown("## GPI Learning Lab")
st.sidebar.caption("Interactive concepts for Investment Portfolio Management")

TOPICS = [
    "Why Invest?",
    "Macroeconomic Context & Financial Markets",
    "Financial Glossary",
]

selected_topic = st.sidebar.radio("Select a learning topic", TOPICS)

st.sidebar.divider()
st.sidebar.markdown("### Learning roadmap")
with st.sidebar.expander("Show broader topic map", expanded=False):
    st.markdown(
        """
- Investor mindset and planning
- Macro context and financial markets
- Market structure and real decisions
- Financial assets and portfolio logic
- Fixed income
- Equity markets
- Indexing, passive investing, and market efficiency
- Returns and risk measurement
- Diversification and efficient frontier
- Portfolio optimization and CML
- CAPM and factor models
- Risk management and stress testing
- Rebalancing, benchmarks, and attribution
- Real frictions and behavioral finance
- Alternatives, technology, and AI in investing
"""
    )

st.sidebar.divider()
st.sidebar.info(
    "This app uses simplified educational models. It is designed to build financial intuition, not to forecast markets or provide investment advice."
)

# =============================================================================
# TOPIC 1 — WHY INVEST?
# =============================================================================

if selected_topic == "Why Invest?":
    topic_cover(
        title="Why Invest?",
        subtitle="Personal wealth, future choices, inflation, discipline, and long-term investing.",
        quote="The investor's chief problem — and even his worst enemy — is likely to be himself. Investing isn't about beating others at their game. It's about controlling yourself at your own game.",
        author="Benjamin Graham",
        source="The Intelligent Investor (Ch. 1)",
        facts=[
            (
                "Weimar Republic Hyperinflation (1923)",
                "In 1923 Germany, inflation reached such extreme levels that prices doubled every few days. People used wheelbarrows of banknotes to buy a loaf of bread, and paper money was cheaper than firewood. Holding uninvested cash during inflation is a guaranteed real-loss strategy.",
                "Niall Ferguson, The Ascent of Money (Ch. 2)"
            ),
            (
                "The Origin of 'Bank' and 'Bankrupt'",
                "The word 'bank' comes from the Italian 'banco' (bench), where Renaissance Florentine money changers conducted transactions. When a banker failed to meet his obligations, his bench was physically broken — giving us 'bankrupt' (banca rotta).",
                "Niall Ferguson, The Ascent of Money (Ch. 1)"
            )
        ],
        anchor="The biggest investment risk is not market volatility — it is not having a plan.",
        question="Why should you invest at all — and what happens if you do not?",
    )

    tabs = st.tabs(
        [
            "Big Picture",
            "Inflation Trap",
            "Cost of Waiting",
            "Capital Beyond Money",
            "Trade-Off Map",
            "Investment or Speculation?",
            "IPS Builder",
        ]
    )

    with tabs[0]:
        st.subheader("Investing begins before assets")
        c1, c2 = st.columns([1.2, 1])
        with c1:
            card(
                "Core idea",
                """
                Investing does not begin when you buy a stock, a bond, an ETF, or a fund.
                It begins when you recognize that your money, time, career, emotions,
                inflation exposure, and future choices are already exposed to risk.
                """,
                "concept",
            )
            card(
                "The hidden decision",
                """
                Not investing is not neutral. It usually means holding a concentrated
                position in cash, accepting inflation exposure, postponing compounding,
                and leaving future decisions with less financial flexibility.
                """,
                "warning",
            )
            card(
                "Memorable rule",
                """
                <strong>Investing is not about becoming rich quickly. It is about building future choices.</strong>
                """,
                "decision",
            )
        with c2:
            ideas = pd.DataFrame(
                {
                    "Question": [
                        "What can reduce purchasing power?",
                        "What makes future choices easier?",
                        "What comes before asset selection?",
                        "What destroys discipline?",
                        "What makes an asset suitable?",
                    ],
                    "Concept": [
                        "Inflation",
                        "Optionality",
                        "Rules and constraints",
                        "Emotional improvisation",
                        "Fit with horizon, liquidity, risk, and behavior",
                    ],
                }
            )
            st.dataframe(ideas, use_container_width=True, hide_index=True)
            st.markdown(
                """
                **Use this topic to train a habit:** before asking *what should I buy?*, ask
                *what problem am I trying to solve, under what constraints, and with what rules?*
                """
            )

    with tabs[1]:
        st.subheader("The inflation trap: when safety becomes slow erosion")
        with st.expander("What am I moving in this simulator?", expanded=True):
            st.markdown(
                """
                You are comparing the **real purchasing power** of money under different assumptions.

                - **Initial capital** is the amount you start with.
                - **Annual contribution** is the amount added every year.
                - **Inflation** reduces purchasing power.
                - **Cash/deposit nominal yield** is the return earned by a low-risk cash-like option before inflation.
                - **Disciplined portfolio nominal return** is a simplified long-term expected return assumption.
                - **Annual drag** represents fees, taxes, and other frictions.

                This is **not a forecast**. It is a learning model showing how nominal balances can look acceptable while real purchasing power changes very differently.
                """
            )

        left, right = st.columns([0.95, 1.65])
        with left:
            initial_capital = st.number_input("Initial capital", min_value=100.0, max_value=1_000_000.0, value=10_000.0, step=500.0, help="Amount invested or held at the starting point.")
            annual_contribution = st.number_input("Annual contribution", min_value=0.0, max_value=100_000.0, value=1_200.0, step=100.0, help="Additional amount contributed at the end of each year.")
            years = st.slider("Time horizon", 1, 40, 20, help="Longer horizons magnify the effect of inflation, compounding, and fees.")
            inflation = st.slider("Annual inflation", 0.0, 15.0, 4.0, 0.25, help="Inflation reduces the real purchasing power of money.") / 100
            cash_yield = st.slider("Cash/deposit nominal yield", 0.0, 12.0, 2.0, 0.25, help="Nominal return earned by the low-risk cash-like option.") / 100
            portfolio_return = st.slider("Disciplined portfolio nominal return", 0.0, 18.0, 7.0, 0.25, help="Simplified annual return assumption for a diversified portfolio.") / 100
            annual_drag = st.slider("Annual drag: fees + taxes + frictions", 0.0, 5.0, 0.7, 0.1, help="A simple annual reduction applied to the portfolio return.") / 100

        t = np.arange(0, years + 1)
        cash_nominal = np.zeros_like(t, dtype=float)
        portfolio_nominal = np.zeros_like(t, dtype=float)
        cash_nominal[0] = initial_capital
        portfolio_nominal[0] = initial_capital
        net_portfolio_return = max(portfolio_return - annual_drag, -0.99)

        for i in range(1, years + 1):
            cash_nominal[i] = cash_nominal[i - 1] * (1 + cash_yield) + annual_contribution
            portfolio_nominal[i] = portfolio_nominal[i - 1] * (1 + net_portfolio_return) + annual_contribution

        inflation_index = (1 + inflation) ** t
        cash_real = cash_nominal / inflation_index
        portfolio_real = portfolio_nominal / inflation_index
        contributed_nominal = initial_capital + annual_contribution * t
        contributed_real = contributed_nominal / inflation_index

        df_inflation = pd.DataFrame(
            {
                "Year": t,
                "Cash/deposit — real purchasing power": cash_real,
                "Disciplined portfolio — real purchasing power": portfolio_real,
                "Contributions only — inflation adjusted": contributed_real,
            }
        )
        with right:
            st.plotly_chart(
                line_chart(
                    df_inflation,
                    "Year",
                    ["Cash/deposit — real purchasing power", "Disciplined portfolio — real purchasing power", "Contributions only — inflation adjusted"],
                    "Real purchasing power over time",
                    "Today's dollars",
                ),
                use_container_width=True,
            )

        real_cash_change = cash_real[-1] / initial_capital - 1
        real_port_change = portfolio_real[-1] / initial_capital - 1
        gap = portfolio_real[-1] - cash_real[-1]
        m1, m2, m3 = st.columns(3)
        m1.metric("Final real value — cash/deposit", money(cash_real[-1]), delta=pct(real_cash_change))
        m2.metric("Final real value — portfolio", money(portfolio_real[-1]), delta=pct(real_port_change))
        m3.metric("Real wealth gap", money(gap), help="Final portfolio purchasing power minus final cash/deposit purchasing power.")

        if cash_yield < inflation:
            cash_message = "Your cash-like option has a negative real rate: it earns interest, but inflation grows faster."
        elif cash_yield < inflation + 0.01:
            cash_message = "Your cash-like option is barely protecting purchasing power. The margin of safety is thin."
        else:
            cash_message = "Your cash-like option protects purchasing power better in this scenario, but it may still sacrifice long-term compounding."

        if annual_drag > 0.015:
            drag_message = "The annual drag is high enough to materially reduce compounding. Costs and taxes are not small details."
        else:
            drag_message = "The annual drag is moderate in this scenario, but it still compounds against you over time."

        card(
            "Dynamic reading",
            f"""
            {cash_message}<br><br>
            {drag_message}<br><br>
            Under your assumptions, the disciplined portfolio ends with <strong>{money(gap)}</strong>
            more real purchasing power than the cash/deposit path. The lesson is not that risky assets always win.
            The lesson is that inflation, time, contributions, fees, and discipline interact.
            """,
            "model",
        )

    with tabs[2]:
        st.subheader("The cost of waiting")
        with st.expander("What does this simulator teach?", expanded=True):
            st.markdown(
                """
                This module isolates the impact of **delaying the start** of an investment process.
                You are not changing the final date. You are changing when contributions begin.

                The key idea is that waiting does not only reduce the number of contributions.
                It also removes early contributions from the compounding process.
                """
            )
        left, right = st.columns([0.9, 1.7])
        with left:
            monthly_contribution = st.number_input("Monthly contribution", min_value=10.0, max_value=20_000.0, value=150.0, step=10.0)
            horizon_years = st.slider("Total horizon", 5, 50, 30)
            wait_years = st.slider("Years before starting", 0, min(20, horizon_years - 1), 5)
            nominal_return = st.slider("Expected annual nominal return", 0.0, 15.0, 7.0, 0.25) / 100
            inflation_wait = st.slider("Annual inflation assumption", 0.0, 10.0, 3.0, 0.25) / 100
        months = horizon_years * 12
        wait_months = wait_years * 12
        monthly_r = (1 + nominal_return) ** (1 / 12) - 1
        monthly_i = (1 + inflation_wait) ** (1 / 12) - 1
        now = np.zeros(months + 1)
        later = np.zeros(months + 1)
        for m in range(1, months + 1):
            now[m] = now[m - 1] * (1 + monthly_r) + monthly_contribution
            later[m] = later[m - 1] * (1 + monthly_r) + (monthly_contribution if m > wait_months else 0)
        real_now = now / ((1 + monthly_i) ** np.arange(months + 1))
        real_later = later / ((1 + monthly_i) ** np.arange(months + 1))
        df_wait = pd.DataFrame({"Year": np.arange(months + 1) / 12, "Start now — real value": real_now, "Start later — real value": real_later})
        with right:
            st.plotly_chart(line_chart(df_wait, "Year", ["Start now — real value", "Start later — real value"], "Starting earlier vs. starting later", "Today's dollars"), use_container_width=True)
        lost_real = real_now[-1] - real_later[-1]
        contributions_missed = monthly_contribution * wait_months
        growth_lost = lost_real - contributions_missed / ((1 + inflation_wait) ** horizon_years)
        c1, c2, c3 = st.columns(3)
        c1.metric("Real value if you start now", money(real_now[-1]))
        c2.metric("Real value if you wait", money(real_later[-1]))
        c3.metric("Real cost of waiting", money(lost_real))
        card(
            "Dynamic reading",
            f"""
            Waiting <strong>{wait_years} years</strong> costs approximately <strong>{money(lost_real)}</strong>
            in final real wealth under your assumptions. Part of that comes from missed contributions, but part comes from the lost compounding time of early contributions.
            This is why investing is partly a timing problem, but not in the sense of predicting the market. It is about giving your process enough time to work.
            """,
            "model",
        )

    with tabs[3]:
        st.subheader("Capital is more than money")
        with st.expander("What am I scoring?", expanded=True):
            st.markdown(
                """
                Investing decisions are stronger when you understand your full capital structure.
                You are scoring different forms of capital from 1 to 5.

                These are not moral scores. They are diagnostic inputs: where are you resilient,
                where are you concentrated, and where could financial planning create more optionality?
                """
            )
        dims = ["Financial", "Human", "Time", "Reputational", "Emotional", "Entrepreneurial"]
        explanations = {
            "Financial": "Savings, income, emergency reserves, investable assets.",
            "Human": "Education, skills, employability, career prospects.",
            "Time": "Age, horizon, flexibility, ability to wait.",
            "Reputational": "Trust, relationships, credibility, professional network.",
            "Emotional": "Ability to tolerate uncertainty without breaking your plan.",
            "Entrepreneurial": "Projects, business ideas, risk-taking capacity, opportunity pipeline.",
        }
        left, right = st.columns([0.9, 1.6])
        scores = {}
        with left:
            for d in dims:
                scores[d] = st.slider(d, 1, 5, 3, help=explanations[d])
        df_capital = pd.DataFrame([{"Profile": "Your capital map", **scores}])
        with right:
            st.plotly_chart(radar_chart(df_capital, "Profile", dims, "Personal capital map"), use_container_width=True)
        min_dim = min(scores, key=scores.get)
        max_dim = max(scores, key=scores.get)
        balance = np.mean(list(scores.values())) - np.std(list(scores.values()))
        card(
            "Dynamic reading",
            f"""
            Your strongest capital area is <strong>{max_dim}</strong>; your weakest or most fragile area is <strong>{min_dim}</strong>.
            A disciplined portfolio should not be disconnected from this map. If your income or business risk is concentrated,
            your financial portfolio may need more liquidity, diversification, or behavioral simplicity.
            """,
            "model",
        )
        st.progress(max(0.0, min(1.0, balance / 5)))
        st.caption("Balance indicator: higher values suggest a more even capital structure. This is a learning diagnostic, not a personal assessment.")

    with tabs[4]:
        st.subheader("The trade-off map: no free return")
        with st.expander("How should you read this map?", expanded=True):
            st.markdown(
                """
                Each vehicle is scored from 1 to 5 on five dimensions. A high expected return is not automatically better.
                It may come with higher volatility, lower liquidity, longer horizon, or greater behavioral discipline required.

                The values are educational approximations. They are not product recommendations.
                """
            )
        default_assets = pd.DataFrame(
            {
                "Vehicle": ["Cash", "Short-term deposit", "Broad equity ETF", "Individual cyclical stock", "Speculative narrative asset"],
                "Expected return": [1.0, 2.0, 3.7, 4.2, 5.0],
                "Risk": [0.8, 1.4, 3.3, 4.4, 5.0],
                "Liquidity": [5.0, 2.8, 4.5, 3.8, 3.0],
                "Required horizon": [1.0, 2.0, 4.3, 4.0, 4.8],
                "Required discipline": [1.2, 2.0, 4.0, 4.6, 5.0],
            }
        )
        selected = st.multiselect("Choose vehicles to compare", default_assets["Vehicle"].tolist(), default=["Short-term deposit", "Broad equity ETF", "Speculative narrative asset"])
        df_selected = default_assets[default_assets["Vehicle"].isin(selected)]
        col1, col2 = st.columns([1.25, 1])
        with col1:
            if len(df_selected) > 0:
                st.plotly_chart(radar_chart(df_selected, "Vehicle", ["Expected return", "Risk", "Liquidity", "Required horizon", "Required discipline"], "Investment trade-offs"), use_container_width=True)
            else:
                st.warning("Select at least one vehicle.")
        with col2:
            scatter = px.scatter(
                default_assets,
                x="Risk",
                y="Expected return",
                size="Required discipline",
                color="Liquidity",
                hover_name="Vehicle",
                text="Vehicle",
                range_x=[0, 5.5],
                range_y=[0, 5.5],
                title="Risk-return-discipline view",
                color_continuous_scale="Blues",
            )
            scatter.update_traces(textposition="top center")
            scatter.update_layout(template="plotly_white", height=470, margin=dict(l=20, r=20, t=55, b=40))
            st.plotly_chart(scatter, use_container_width=True)
        card(
            "Interpretation rule",
            """
            If a product seems to offer high return, low risk, high liquidity, low cost, and no discipline requirement,
            do not celebrate first. Ask what risk, restriction, cost, or assumption is missing.
            """,
            "warning",
        )

    with tabs[5]:
        st.subheader("Investment or speculation?")
        with st.expander("What does this diagnostic do?", expanded=True):
            st.markdown(
                """
                The same asset can be approached with different processes.
                This diagnostic does not judge the asset alone. It evaluates the quality of the decision process.

                You will receive a score based on horizon, thesis, valuation discipline, risk limits, liquidity fit, and behavioral trigger.
                """
            )
        left, right = st.columns([1, 1.35])
        with left:
            asset_label = st.text_input("Asset or vehicle you are evaluating", "Global equity ETF")
            horizon = st.selectbox("Primary horizon", ["Less than 3 months", "3–12 months", "1–5 years", "More than 5 years"])
            reason = st.selectbox("Main reason for entering", ["Clear role in my plan", "Valuation or expected cash flows", "Diversification", "Recent price momentum", "Social media or peer pressure", "Fear of missing out"])
            risk_rule = st.selectbox("Risk rule", ["Written rule and position limit", "General idea but not written", "No explicit risk rule"])
            liquidity_fit = st.selectbox("Liquidity fit", ["Matches my need", "Unclear", "Could conflict with my need"])
            understanding = st.selectbox("Understanding of what drives returns", ["Strong", "Partial", "Weak"])
        score = 0
        score += {"Less than 3 months": 0, "3–12 months": 1, "1–5 years": 2, "More than 5 years": 2}[horizon]
        score += {"Clear role in my plan": 3, "Valuation or expected cash flows": 3, "Diversification": 2, "Recent price momentum": 0, "Social media or peer pressure": -1, "Fear of missing out": -2}[reason]
        score += {"Written rule and position limit": 3, "General idea but not written": 1, "No explicit risk rule": -1}[risk_rule]
        score += {"Matches my need": 2, "Unclear": 0, "Could conflict with my need": -2}[liquidity_fit]
        score += {"Strong": 2, "Partial": 1, "Weak": -2}[understanding]
        max_score = 12
        normalized = max(0, min(1, score / max_score))
        if score >= 9:
            label = "Investment-like process"
            color = GOOD
            advice = "The process is relatively disciplined. The next step is to test assumptions and compare alternatives."
        elif score >= 5:
            label = "Borderline decision"
            color = WARN
            advice = "The decision may be reasonable, but the process still has weak points. Clarify rules, liquidity, and evidence."
        else:
            label = "Speculation-like process"
            color = BAD
            advice = "The decision depends too much on price movement, emotion, or weak rules. Slow down before allocating capital."
        with right:
            fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=score, title={"text": label}, gauge={"axis": {"range": [-4, 12]}, "bar": {"color": color}, "steps": [{"range": [-4, 4.9], "color": "#FEE2E2"}, {"range": [5, 8.9], "color": "#FEF3C7"}, {"range": [9, 12], "color": "#DCFCE7"}]}))
            fig_gauge.update_layout(height=330, margin=dict(l=20, r=20, t=45, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            card("Dynamic reading", f"For <strong>{asset_label}</strong>, the process currently looks like: <strong>{label}</strong>.<br><br>{advice}", "model")
        st.markdown("#### Process checklist")
        st.write("Before deciding, complete these sentences:")
        st.markdown(
            """
- I am considering this asset because...
- The risk I am accepting is...
- The alternative I am rejecting is...
- I would change my mind if...
- This position fits my horizon because...
"""
        )

    with tabs[6]:
        st.subheader("IPS Builder: rules before assets")
        with st.expander("What is an IPS?", expanded=True):
            st.markdown(
                """
                An Investment Policy Statement is a set of rules that connects objectives, constraints, risk tolerance,
                liquidity, horizon, and behavior. It should come before asset selection.

                Think of it as a letter from your disciplined self to your emotional future self.
                """
            )
        left, right = st.columns([1, 1.2])
        with left:
            objective = st.selectbox("Primary objective", ["Emergency resilience", "Long-term wealth building", "Future entrepreneurship", "Education or major purchase", "Financial independence"])
            horizon_ips = st.selectbox("Investment horizon", ["Short-term", "Medium-term", "Long-term"])
            liquidity_need = st.selectbox("Liquidity need", ["High", "Moderate", "Low"])
            max_drawdown = st.select_slider("Temporary drawdown you could tolerate without breaking the plan", options=["0%", "-5%", "-10%", "-20%", "-30%", "-40% or more"])
            contribution_rule = st.text_input("Contribution rule", "I will invest a fixed amount every month after covering essential liquidity needs.")
            panic_rule = st.text_input("Market stress rule", "I will not sell only because prices fall; I will first review whether my objective, horizon, or liquidity need changed.")
            exclusion_rule = st.text_input("Exclusion rule", "I will not buy assets I cannot explain in plain language.")
        ips_text = f"""# Draft Investment Policy Statement

## Objective
My primary objective is: {objective}.

## Horizon
My investment horizon is: {horizon_ips}.

## Liquidity
My liquidity need is: {liquidity_need}.

## Risk tolerance
The temporary drawdown I believe I could tolerate without breaking my plan is: {max_drawdown}.

## Contribution rule
{contribution_rule}

## Market stress rule
{panic_rule}

## Exclusion rule
{exclusion_rule}

## Decision principle
I will not start with the question "What should I buy?" I will start with the question "What role should this decision play in my life, under my constraints, and according to my rules?"
"""
        with right:
            st.markdown("#### Draft output")
            st.code(ips_text, language="markdown")
            st.download_button("Download draft IPS", data=ips_text, file_name="draft_ips.md", mime="text/markdown")
        card("Core rule", "A recommendation without a mandate is only an opinion. A recommendation with objectives, constraints, evidence, and rules starts to look like an investment decision.", "decision")

# =============================================================================
# TOPIC 2 — MACROECONOMIC CONTEXT AND FINANCIAL MARKETS
# =============================================================================

elif selected_topic == "Macroeconomic Context & Financial Markets":
    topic_cover(
        title="Macroeconomic Context & Financial Markets",
        subtitle="How inflation, interest rates, expectations, currencies, markets, and intermediaries shape investment decisions.",
        quote="Financial markets do not price past economic data. They price expectations about the future, and asset prices move primarily when reality differs from what was expected.",
        author="Howard Marks",
        source="The Most Important Thing: Uncommon Sense for the Thoughtful Investor",
        facts=[
            (
                "Nathan Rothschild & The Battle of Waterloo (1815)",
                "Nathan Rothschild used a private courier network of carrier pigeons and fast boats to learn of Napoleon's defeat at Waterloo a full day before official British dispatches arrived. Instead of selling in panic, he bought depressed government bonds (Consols), capturing one of history's famous bond market gains.",
                "Niall Ferguson, The Ascent of Money (Ch. 2)"
            ),
            (
                "When 'Good News' is Bad Market News",
                "In inflationary cycles, an extraordinarily strong employment report (positive economic news) often triggers a sharp selloff in stocks and bonds. Markets immediately discount that central banks will raise interest rates aggressively to cool the economy.",
                "Frederic Mishkin, Financial Markets & Institutions"
            )
        ],
        anchor="Markets move not only because of fundamentals, but because of expectations about the future.",
        question="How does the macroeconomic environment affect investment decisions, even for an individual investor?",
    )

    tabs = st.tabs(
        [
            "Macro Map",
            "Transmission Engine",
            "Expectations vs. Surprises",
            "Real Returns",
            "Market Architecture",
            "Emerging Market Lens",
        ]
    )

    with tabs[0]:
        st.subheader("Macro is the environment your portfolio lives in")
        card(
            "Core idea",
            """
            Macroeconomics does not tell you exactly what to buy. It changes the terrain where every investment decision occurs:
            inflation, interest rates, discount rates, credit conditions, currency, liquidity, risk appetite, and valuation.
            """,
            "concept",
        )
        st.markdown("#### The five channels that matter most")
        channels = pd.DataFrame(
            {
                "Macro variable": ["Inflation", "Interest rates", "Growth", "Fiscal credibility", "Global risk appetite"],
                "Investment channel": ["Purchasing power and real returns", "Discount rates, credit, bond prices", "Corporate earnings and employment", "Country risk, sovereign yields, currency", "Flows, liquidity, emerging markets, safe havens"],
                "Common trap": ["Confusing nominal return with real return", "Thinking high rates are simply good or bad", "Treating growth as always bullish", "Ignoring country risk in local assets", "Assuming diversification always works in stress"],
            }
        )
        st.dataframe(channels, hide_index=True, use_container_width=True)
        card(
            "Interpretation rule",
            "Macro matters when it changes cash flows, discount rates, risk premiums, liquidity, or currency.",
            "decision",
        )

    with tabs[1]:
        st.subheader("Macro Transmission Engine")
        with st.expander("What am I moving in this simulator?", expanded=True):
            st.markdown(
                """
                This simulator studies a **hypothetical interest-rate shock**.

                - A **basis point** is 0.01 percentage point. A 100 bps shock means the rate changes by 1.00 percentage point.
                - The **policy-rate shock** represents a central bank decision or a sudden repricing of expected policy rates.
                - The **pass-through to bond yields** says how much of that shock is reflected in market yields. It may be less than 100% if markets had already expected it, or more than 100% if the shock changes the whole yield curve.
                - The **bond impact** uses the traditional duration approximation: price change ≈ -duration × yield change.
                - The **equity impact** uses a simplified valuation sensitivity: higher discount rates reduce the present value of future cash flows, especially for long-duration growth equities.
                - The **currency and liquidity effects** are teaching assumptions, not forecasts.

                The point is not to claim that assets will move by exactly these numbers.
                The point is to see why a rate shock can affect bonds, equities, currency, and liquidity through different mechanisms.
                """
            )
        left, right = st.columns([0.95, 1.65])
        with left:
            initial_policy_rate = st.slider("Initial policy rate", 0.0, 20.0, 8.0, 0.25, help="Starting short-term policy rate before the hypothetical shock.") / 100
            shock_bps = st.slider("Policy-rate shock", -400, 400, 100, 25, help="Positive values represent rate hikes or hawkish repricing. Negative values represent cuts or dovish repricing.")
            pass_through = st.slider("Pass-through to market yields", 0.0, 150.0, 80.0, 5.0, help="How much of the policy shock is reflected in bond yields. 100% means one-for-one pass-through.") / 100
            bond_duration = st.slider("Bond duration", 0.5, 20.0, 6.0, 0.5, help="Higher duration means higher price sensitivity to yield changes.")
            equity_duration = st.selectbox("Equity profile", ["Defensive equity", "Broad equity market", "Long-duration growth equity"], help="Growth equities tend to be more sensitive to discount-rate changes.")
            risk_premium_change_bps = st.slider("Risk premium shock", -200, 300, 50, 25, help="Additional repricing of risk appetite. Positive values mean investors demand more compensation for risk.")
            fx_sensitivity = st.slider("Currency sensitivity", 0.0, 1.5, 0.5, 0.05, help="Teaching assumption: how strongly currency pressure reacts to rate/risk shocks.")

        yield_change = (shock_bps / 10_000) * pass_through
        bond_price_change = -bond_duration * yield_change
        equity_base_sensitivity = {"Defensive equity": 4.0, "Broad equity market": 7.0, "Long-duration growth equity": 11.0}[equity_duration]
        total_discount_shock = yield_change + risk_premium_change_bps / 10_000
        equity_price_change = -equity_base_sensitivity * total_discount_shock
        cash_return_change = shock_bps / 10_000
        currency_pressure = fx_sensitivity * (0.35 * shock_bps + 0.65 * risk_premium_change_bps) / 100
        liquidity_score_change = -0.015 * max(shock_bps, 0) - 0.012 * max(risk_premium_change_bps, 0)

        impacts = pd.DataFrame(
            {
                "Asset / condition": ["Short-term cash yield", f"Bond price (duration {bond_duration:.1f})", equity_duration, "Currency pressure", "Liquidity conditions"],
                "Estimated impact (%)": [cash_return_change * 100, bond_price_change * 100, equity_price_change * 100, currency_pressure, liquidity_score_change],
            }
        )
        with right:
            st.plotly_chart(bar_chart(impacts["Asset / condition"].tolist(), impacts["Estimated impact (%)"].tolist(), "Simplified impact of the macro shock", "Estimated impact (%)"), use_container_width=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("New policy rate", pct(initial_policy_rate + shock_bps / 10_000))
        c2.metric("Yield change used", f"{yield_change*10_000:,.0f} bps")
        c3.metric("Bond price impact", pct(bond_price_change))
        c4.metric("Equity price impact", pct(equity_price_change))

        direction = "tightening" if shock_bps > 0 else "easing" if shock_bps < 0 else "no policy-rate change"
        if shock_bps > 0:
            rate_read = "The rate shock raises the opportunity cost of money and tends to pressure long-duration assets."
        elif shock_bps < 0:
            rate_read = "The rate shock lowers the discount-rate pressure and can support duration-sensitive assets, all else equal."
        else:
            rate_read = "There is no policy-rate shock, so the simulated movement comes mainly from the risk-premium assumption."
        if pass_through < 0.5:
            pass_read = "The pass-through is low, suggesting the market had already priced in much of the policy move or does not expect it to persist."
        elif pass_through <= 1.0:
            pass_read = "The pass-through is moderate to high: market yields move meaningfully, but not more than the policy shock itself."
        else:
            pass_read = "The pass-through is above 100%, meaning the shock is assumed to change broader yield-curve expectations, not only the current policy rate."
        if risk_premium_change_bps > 0:
            rp_read = "The positive risk-premium shock means investors demand more compensation for risk, which adds pressure to equities and risky assets."
        elif risk_premium_change_bps < 0:
            rp_read = "The negative risk-premium shock means risk appetite improves, partly offsetting discount-rate pressure."
        else:
            rp_read = "Risk premiums are unchanged, so the scenario isolates the rate channel."
        card(
            "Dynamic reading",
            f"""
            This is a <strong>{direction}</strong> scenario. {rate_read}<br><br>
            {pass_read}<br><br>
            {rp_read}<br><br>
            The bond result comes from the duration approximation. The equity result is a simplified sensitivity, not an empirical prediction. In real markets, the actual reaction also depends on whether the move was expected, what happens to earnings, liquidity, inflation expectations, and investor positioning.
            """,
            "model",
        )

    with tabs[2]:
        st.subheader("Expectations vs. surprises")
        with st.expander("Why can good news be bad market news?", expanded=True):
            st.markdown(
                """
                Markets often move because a data point changes expectations.
                A strong labor-market or inflation report can be economically positive in one sense,
                but negative for asset prices if it makes investors expect tighter monetary policy.

                The key relationship is:

                **Surprise = Actual data − Expected data**

                The direction of the market reaction depends on what the surprise means for rates, liquidity, earnings, and risk appetite.
                """
            )
        left, right = st.columns([0.9, 1.7])
        with left:
            data_type = st.selectbox("Data release", ["Inflation", "Employment", "GDP growth", "Central bank statement"])
            expected = st.number_input("Expected value", value=4.0, step=0.1, help="Market consensus before the release.")
            actual = st.number_input("Actual value", value=5.0, step=0.1, help="Reported value after release.")
            surprise_sensitivity = st.slider("Market sensitivity to surprise", 0.0, 3.0, 1.0, 0.1, help="Educational parameter: higher values amplify the simulated reaction.")
            prior_rate_cut_probability = st.slider("Prior probability of rate cuts", 0, 100, 55, 5, help="Simplified expectation before the data release.")
        surprise = actual - expected
        hawkish_score = 0.0
        if data_type in ["Inflation", "Employment", "GDP growth"]:
            hawkish_score = surprise * surprise_sensitivity
        else:
            hawkish_score = (actual - expected) * surprise_sensitivity
        new_rate_cut_probability = np.clip(prior_rate_cut_probability - 12 * hawkish_score, 0, 100)
        bond_yield_reaction = 6 * hawkish_score
        equity_reaction = -0.45 * hawkish_score
        currency_reaction = 0.25 * hawkish_score
        times = ["Before release", "Immediate repricing", "Narrative stabilizes"]
        df_surprise = pd.DataFrame(
            {
                "Stage": times,
                "Rate-cut probability (%)": [prior_rate_cut_probability, new_rate_cut_probability, 0.7 * new_rate_cut_probability + 0.3 * prior_rate_cut_probability],
                "Bond yield index": [100, 100 + bond_yield_reaction, 100 + 0.75 * bond_yield_reaction],
                "Equity price index": [100, 100 + equity_reaction, 100 + 0.7 * equity_reaction],
            }
        )
        with right:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_surprise["Stage"], y=df_surprise["Rate-cut probability (%)"], mode="lines+markers", name="Rate-cut probability (%)", yaxis="y1"))
            fig.add_trace(go.Scatter(x=df_surprise["Stage"], y=df_surprise["Bond yield index"], mode="lines+markers", name="Bond yield index", yaxis="y2"))
            fig.add_trace(go.Scatter(x=df_surprise["Stage"], y=df_surprise["Equity price index"], mode="lines+markers", name="Equity price index", yaxis="y2"))
            fig.update_layout(
                title="Simplified repricing after a macro surprise",
                template="plotly_white",
                height=420,
                yaxis=dict(title="Probability (%)"),
                yaxis2=dict(title="Index level", overlaying="y", side="right"),
                hovermode="x unified",
                legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"),
                margin=dict(l=20, r=20, t=55, b=90),
            )
            st.plotly_chart(fig, use_container_width=True)
        if hawkish_score > 0.25:
            surprise_label = "hawkish surprise"
            interpretation = "The actual value is above expectations in a way that may reduce expected rate cuts or increase tightening pressure."
        elif hawkish_score < -0.25:
            surprise_label = "dovish surprise"
            interpretation = "The actual value is below expectations in a way that may increase expected rate cuts or reduce tightening pressure."
        else:
            surprise_label = "limited surprise"
            interpretation = "The release is close enough to expectations that the price reaction may be muted."
        card(
            "Dynamic reading",
            f"""
            The release currently looks like a <strong>{surprise_label}</strong>. {interpretation}<br><br>
            Notice that the same data point can have different market meanings depending on what was already expected.
            That is why investors should ask: <strong>What changed relative to expectations?</strong>
            """,
            "model",
        )

    with tabs[3]:
        st.subheader("Real returns: the return you can actually use")
        with st.expander("What am I calculating?", expanded=True):
            st.markdown(
                """
                This module converts a nominal return into an approximate after-tax, after-fee, inflation-adjusted return.
                It helps you see why two products with the same headline yield can have very different real usefulness.

                Approximation:
                **Net nominal return = nominal return − fees − taxes on income/return**

                **Real return ≈ (1 + net nominal return) / (1 + inflation) − 1**
                """
            )
        left, right = st.columns([0.9, 1.7])
        with left:
            nominal_yield = st.slider("Headline nominal return", 0.0, 25.0, 9.0, 0.25) / 100
            inflation_real = st.slider("Inflation", 0.0, 20.0, 5.0, 0.25) / 100
            fee_drag = st.slider("Annual fees / costs", 0.0, 5.0, 0.5, 0.1) / 100
            tax_rate = st.slider("Tax rate applied to investment income", 0.0, 40.0, 15.0, 1.0) / 100
            alternative_nominal = st.slider("Alternative nominal return", 0.0, 25.0, 6.0, 0.25) / 100
        net_nominal = nominal_yield * (1 - tax_rate) - fee_drag
        real_return = (1 + net_nominal) / (1 + inflation_real) - 1
        alt_net = alternative_nominal * (1 - tax_rate) - fee_drag
        alt_real = (1 + alt_net) / (1 + inflation_real) - 1
        comp_df = pd.DataFrame(
            {
                "Measure": ["Headline return", "After tax and fees", "Real after tax and fees", "Alternative real after tax and fees"],
                "Value (%)": [nominal_yield * 100, net_nominal * 100, real_return * 100, alt_real * 100],
            }
        )
        with right:
            st.plotly_chart(bar_chart(comp_df["Measure"].tolist(), comp_df["Value (%)"].tolist(), "From headline return to usable return", "Return (%)"), use_container_width=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Headline nominal return", pct(nominal_yield))
        m2.metric("Net nominal return", pct(net_nominal))
        m3.metric("Real net return", pct(real_return))
        if real_return < 0:
            rr_msg = "The investment has a negative real net return under your assumptions. The headline yield does not protect purchasing power."
        elif real_return < 0.02:
            rr_msg = "The investment protects purchasing power only modestly. Small changes in inflation, fees, or taxes can change the conclusion."
        else:
            rr_msg = "The investment generates a positive real net return under your assumptions. The next question is whether the risk, liquidity, and horizon are acceptable."
        card("Dynamic reading", rr_msg, "model")

    with tabs[4]:
        st.subheader("Market architecture: where does the investment actually happen?")
        with st.expander("Why this tab exists", expanded=True):
            st.markdown(
                """
                An individual investor does not invest in a vacuum. A decision is implemented through a channel:
                bank, broker, fund manager, platform, exchange, custodian, or regulated vehicle.

                This tab is not a list of institutions. It is a map of **implementation logic**:
                what you want to do, which channel is usually involved, what vehicle may appear, and which frictions you must examine.
                """
            )
        left, right = st.columns([0.9, 1.7])
        with left:
            objective = st.selectbox(
                "Investment intention",
                [
                    "Hold emergency liquidity",
                    "Earn fixed income for a known horizon",
                    "Buy diversified equity exposure",
                    "Buy an individual stock",
                    "Invest internationally",
                ],
            )
            horizon_arch = st.selectbox("Horizon", ["Very short", "Short", "Medium", "Long"])
            need_liquidity_arch = st.selectbox("Need for liquidity", ["High", "Moderate", "Low"])
        architecture = {
            "Hold emergency liquidity": {
                "Channel": "Bank, money market fund, or highly liquid platform",
                "Vehicle": "Cash, savings account, short-term deposit, money market fund",
                "Main frictions": "Inflation, low real return, fees, withdrawal conditions",
                "Key question": "Can you access the money when you need it without destroying value?",
            },
            "Earn fixed income for a known horizon": {
                "Channel": "Bank, broker, fund manager, or authorized platform",
                "Vehicle": "Deposit, bond, bond fund, Treasury exposure",
                "Main frictions": "Duration, credit risk, reinvestment risk, liquidity, taxes",
                "Key question": "Are you compensated for inflation, credit, duration, liquidity, and country risk?",
            },
            "Buy diversified equity exposure": {
                "Channel": "Broker, fund platform, ETF platform, pension/fund administrator",
                "Vehicle": "ETF, mutual fund, index fund, diversified equity fund",
                "Main frictions": "Expense ratio, tracking error, spread, domicile, taxes, currency",
                "Key question": "What exposure are you really buying and at what total cost?",
            },
            "Buy an individual stock": {
                "Channel": "Broker or trading platform",
                "Vehicle": "Common stock, preferred share, ADR",
                "Main frictions": "Spread, liquidity, concentration, corporate governance, FX, information risk",
                "Key question": "Do you understand the business, valuation, risk, and role in the portfolio?",
            },
            "Invest internationally": {
                "Channel": "International broker, local intermediary with global access, global fund platform",
                "Vehicle": "Foreign ETF, ADR, global mutual fund, international bond/equity fund",
                "Main frictions": "FX conversion, custody, tax treatment, regulation, estate rules, currency risk",
                "Key question": "Does international exposure reduce concentration enough to justify the added frictions?",
            },
        }[objective]
        flow_labels = ["Investor", "Intermediary / channel", "Investment vehicle", "Underlying exposure", "Investor outcome"]
        flow_values = [1, 1, 1, 1]
        flow_text = [objective, architecture["Channel"], architecture["Vehicle"], "Assets, issuers, markets, currencies", "Return after risk, costs, taxes, and behavior"]
        fig_flow = go.Figure(
            data=[
                go.Sankey(
                    arrangement="snap",
                    node=dict(label=[f"{flow_labels[i]}<br>{flow_text[i]}" for i in range(len(flow_labels))], pad=18, thickness=20),
                    link=dict(source=[0, 1, 2, 3], target=[1, 2, 3, 4], value=flow_values),
                )
            ]
        )
        fig_flow.update_layout(title="Implementation flow", height=420, font_size=11, margin=dict(l=10, r=10, t=50, b=10))
        with right:
            st.plotly_chart(fig_flow, use_container_width=True)
        details = pd.DataFrame([architecture]).T.reset_index()
        details.columns = ["Dimension", "Reading"]
        st.dataframe(details, use_container_width=True, hide_index=True)
        card(
            "Decision rule",
            f"Before asking what to buy, ask where, how, through whom, at what cost, under what risks, and under what rules. For your selected intention, the key question is: <strong>{architecture['Key question']}</strong>",
            "decision",
        )

    with tabs[5]:
        st.subheader("Emerging market lens: familiarity is not safety")
        with st.expander("What does this simulator show?", expanded=True):
            st.markdown(
                """
                This module compares a portfolio concentrated in a local emerging market with a portfolio that includes global exposure.
                It is not claiming one is always better. It shows the trade-off between local familiarity and broader diversification.

                You control local allocation, local returns, global returns, inflation, currency movement, and a country-risk penalty.
                """
            )
        left, right = st.columns([0.95, 1.65])
        with left:
            local_weight = st.slider("Local-market allocation", 0, 100, 75, 5) / 100
            global_weight = 1 - local_weight
            local_return = st.slider("Expected local nominal return", -10.0, 25.0, 8.0, 0.5) / 100
            global_return = st.slider("Expected global nominal return", -10.0, 20.0, 7.0, 0.5) / 100
            fx_move = st.slider("Home currency depreciation vs. global currency", -15.0, 30.0, 4.0, 0.5) / 100
            local_inflation = st.slider("Local inflation", 0.0, 20.0, 5.5, 0.25) / 100
            country_risk_penalty = st.slider("Country-risk / liquidity penalty", 0.0, 8.0, 1.5, 0.25) / 100
            years_em = st.slider("Horizon", 1, 20, 10)
        t_em = np.arange(0, years_em + 1)
        local_path = 100 * ((1 + local_return - country_risk_penalty) / (1 + local_inflation)) ** t_em
        global_path_local_currency = 100 * ((1 + global_return) * (1 + fx_move) / (1 + local_inflation)) ** t_em
        mixed_path = local_weight * local_path + global_weight * global_path_local_currency
        fully_local = local_path
        balanced_50 = 0.5 * local_path + 0.5 * global_path_local_currency
        df_em = pd.DataFrame({"Year": t_em, "Selected mix — real index": mixed_path, "100% local — real index": fully_local, "50/50 local/global — real index": balanced_50})
        with right:
            st.plotly_chart(line_chart(df_em, "Year", ["Selected mix — real index", "100% local — real index", "50/50 local/global — real index"], "Real wealth index under emerging-market assumptions", "Real index, base 100"), use_container_width=True)
        local_final = fully_local[-1]
        selected_final = mixed_path[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric("Local weight", pct(local_weight))
        c2.metric("Selected final real index", f"{selected_final:,.1f}")
        c3.metric("100% local final real index", f"{local_final:,.1f}")
        if local_weight > 0.8:
            home_bias_msg = "Your portfolio is highly exposed to the local environment. That may feel familiar, but it can concentrate income, currency, political, and liquidity risks."
        elif local_weight < 0.25:
            home_bias_msg = "Your portfolio is strongly global. This may reduce local concentration, but currency, tax, access, and behavioral risks become more important."
        else:
            home_bias_msg = "Your allocation mixes local familiarity with global exposure. The quality of this decision depends on costs, currency, liquidity, and the role each exposure plays."
        card("Dynamic reading", f"{home_bias_msg}<br><br>In this scenario, currency movement is not simply a travel issue. It changes the local-currency value of global assets and the real purchasing power of the portfolio.", "model")

# =============================================================================
# FINANCIAL GLOSSARY
# =============================================================================

elif selected_topic == "Financial Glossary":
    topic_cover(
        title="Financial Glossary",
        subtitle="A searchable and organized glossary of core investment portfolio management concepts.",
        quote="Risk comes from not knowing what you're doing. Never invest in an idea you can't illustrate with a crayon.",
        author="Warren Buffett & Peter Lynch",
        source="Essays of Warren Buffett / One Up On Wall Street",
        facts=[
            (
                "The World's First Public Stock (1602)",
                "The Dutch East India Company (VOC) issued the world's first publicly traded shares on the Amsterdam Stock Exchange in 1602 to share the immense capital risk and financial upside of long-distance spice trade voyages.",
                "Niall Ferguson, The Ascent of Money (Ch. 3)"
            ),
            (
                "Sir Isaac Newton's South Sea Bubble Loss (1720)",
                "Sir Isaac Newton, one of history's greatest mathematical minds, lost his life savings in the South Sea stock bubble. He famously lamented: 'I can calculate the motion of heavenly bodies, but not the madness of people.'",
                "Niall Ferguson, The Ascent of Money (Ch. 3)"
            )
        ],
        anchor="Use the search box to look for a term, concept, risk, asset, or decision.",
        question="Why does financial vocabulary matter? Because precise language shapes how we define risk and evaluate opportunities.",
    )

    glossary_df = pd.DataFrame(GLOSSARY)
    categories = sorted(glossary_df["Category"].unique().tolist())
    col1, col2, col3 = st.columns([1.2, 1.2, 0.8])
    with col1:
        query = st.text_input("Search glossary", placeholder="Try: duration, ETF, beta, inflation, spread...")
    with col2:
        selected_categories = st.multiselect("Filter by category", categories, default=categories)
    with col3:
        sort_by = st.selectbox("Sort by", ["Term", "Category"])
    filtered = glossary_df[glossary_df["Category"].isin(selected_categories)]
    if query.strip():
        q = query.lower().strip()
        mask = (
            filtered["Term"].str.lower().str.contains(q, regex=False)
            | filtered["Definition"].str.lower().str.contains(q, regex=False)
            | filtered["Why it matters"].str.lower().str.contains(q, regex=False)
            | filtered["Category"].str.lower().str.contains(q, regex=False)
        )
        filtered = filtered[mask]
    filtered = filtered.sort_values(sort_by)
    st.metric("Terms shown", len(filtered))
    view_mode = st.radio("View mode", ["Concept cards", "Compact table"], horizontal=True)
    if view_mode == "Compact table":
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download filtered glossary as CSV", data=csv, file_name="financial_glossary_filtered.csv", mime="text/csv")
    else:
        if len(filtered) == 0:
            st.warning("No terms match your current search.")
        for _, row in filtered.iterrows():
            st.markdown(
                f"""
<div class="concept-card">
    <div class="kicker">{row['Category']}</div>
    <h4 style="margin-top:0.1rem; margin-bottom:0.35rem; color:{PRIMARY};">{row['Term']}</h4>
    <p><strong>Definition:</strong> {row['Definition']}</p>
    <p><strong>Why it matters:</strong> {row['Why it matters']}</p>
</div>
""",
                unsafe_allow_html=True,
            )