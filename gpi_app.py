"""
GPI Learning Lab | Aurea Capital Partners
Streamlit app for Investment Portfolio Management — Classes 1 and 2.

This app is designed as a pedagogical companion for undergraduate students.
It uses simplified simulations to develop investment judgment, not to provide
personal financial advice or market forecasts.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="GPI Learning Lab | Aurea Capital Partners",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# STYLE
# ==============================================================================

PRIMARY = "#1E3A8A"
PRIMARY_LIGHT = "#EFF6FF"
TEXT = "#0F172A"
MUTED = "#475569"
BORDER = "#CBD5E1"
GOOD = "#059669"
WARN = "#D97706"
BAD = "#DC2626"
BG = "#F8FAFC"

st.markdown(
    f"""
<style>
    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}
    .main-title {{
        font-size: 2.35rem;
        line-height: 1.15;
        font-weight: 800;
        color: {PRIMARY};
        margin-bottom: 0.20rem;
    }}
    .sub-title {{
        font-size: 1.07rem;
        color: {MUTED};
        margin-bottom: 1.15rem;
    }}
    .section-kicker {{
        font-size: 0.82rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {PRIMARY};
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
    }}
    .quote-box {{
        background: linear-gradient(90deg, #EFF6FF, #FFFFFF);
        border-left: 5px solid #2563EB;
        padding: 1rem 1.1rem;
        border-radius: 10px;
        margin: 0.75rem 0 1rem 0;
        color: {TEXT};
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    }}
    .decision-box {{
        background-color: #F0FDF4;
        border-left: 5px solid #16A34A;
        padding: 1rem 1.1rem;
        border-radius: 10px;
        margin: 0.75rem 0;
    }}
    .trap-box {{
        background-color: #FFF7ED;
        border-left: 5px solid #EA580C;
        padding: 1rem 1.1rem;
        border-radius: 10px;
        margin: 0.75rem 0;
    }}
    .reality-box {{
        background-color: #FDF2F8;
        border-left: 5px solid #DB2777;
        padding: 1rem 1.1rem;
        border-radius: 10px;
        margin: 0.75rem 0;
    }}
    .soft-card {{
        background-color: #FFFFFF;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.7rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    }}
    .small-note {{
        font-size: 0.90rem;
        color: {MUTED};
    }}
    .pill {{
        display: inline-block;
        padding: 0.22rem 0.55rem;
        margin: 0.1rem;
        border-radius: 999px;
        background-color: #E0E7FF;
        color: #3730A3;
        font-size: 0.78rem;
        font-weight: 700;
    }}
    .stMetric {{
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.55rem;
    }}
</style>
""",
    unsafe_allow_html=True,
)

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def pct(x: float, decimals: int = 1) -> str:
    return f"{x * 100:,.{decimals}f}%"


def pct_points(x: float, decimals: int = 1) -> str:
    return f"{x:,.{decimals}f}%"


def cop(x: float, decimals: int = 0) -> str:
    return f"COP ${x:,.{decimals}f}"


def usd(x: float, decimals: int = 0) -> str:
    return f"US ${x:,.{decimals}f}"


def base100(values: np.ndarray) -> np.ndarray:
    return 100 * values / values[0]


def header(title: str, subtitle: str, anchor: str, decision_question: str) -> None:
    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="quote-box">
            <div class="section-kicker">Conceptual anchor</div>
            <strong>{anchor}</strong>
        </div>
        <div class="decision-box">
            <div class="section-kicker">Decision question</div>
            <strong>{decision_question}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str, kind: str = "soft") -> None:
    cls = {
        "soft": "soft-card",
        "trap": "trap-box",
        "decision": "decision-box",
        "reality": "reality-box",
        "quote": "quote-box",
    }.get(kind, "soft-card")
    st.markdown(f'<div class="{cls}"><strong>{title}</strong><br>{body}</div>', unsafe_allow_html=True)


def diagnostic_badge(value: float, good_threshold: float, warn_threshold: float, higher_is_better: bool = True) -> Tuple[str, str]:
    if higher_is_better:
        if value >= good_threshold:
            return "Sólido", GOOD
        if value >= warn_threshold:
            return "Vulnerable", WARN
        return "Crítico", BAD
    if value <= good_threshold:
        return "Sólido", GOOD
    if value <= warn_threshold:
        return "Vulnerable", WARN
    return "Crítico", BAD


def make_line_chart(df: pd.DataFrame, x: str, y_cols: List[str], title: str, y_title: str) -> go.Figure:
    fig = go.Figure()
    for col in y_cols:
        fig.add_trace(go.Scatter(x=df[x], y=df[col], mode="lines+markers", name=col))
    fig.update_layout(
        title=title,
        template="plotly_white",
        hovermode="x unified",
        height=430,
        xaxis_title=x,
        yaxis_title=y_title,
        legend=dict(orientation="h", yanchor="bottom", y=-0.28, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=60, b=90),
    )
    return fig


def make_radar(labels: List[str], series: Dict[str, List[float]], title: str = "") -> go.Figure:
    fig = go.Figure()
    theta = labels + [labels[0]]
    for name, values in series.items():
        r = values + [values[0]]
        fig.add_trace(go.Scatterpolar(r=r, theta=theta, fill="toself", name=name))
    fig.update_layout(
        title=title,
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True,
        height=440,
        template="plotly_white",
        margin=dict(l=30, r=30, t=55, b=30),
    )
    return fig


def download_text_button(label: str, text: str, file_name: str) -> None:
    st.download_button(
        label=label,
        data=text.encode("utf-8"),
        file_name=file_name,
        mime="text/plain",
        use_container_width=True,
    )


def annual_compound_with_contributions(
    initial: float,
    annual_contribution: float,
    annual_return: float,
    years: int,
) -> np.ndarray:
    values = [initial]
    current = initial
    for _ in range(years):
        current = current * (1 + annual_return) + annual_contribution
        values.append(current)
    return np.array(values)


def suitability_score(asset: pd.Series, profile: Dict[str, float]) -> float:
    # Score 0-100. This is pedagogical, not a recommendation engine.
    risk_gap = abs(asset["Risk"] - profile["Risk Capacity"])
    horizon_gap = max(0, asset["Horizon Required"] - profile["Horizon"])
    liquidity_gap = max(0, profile["Liquidity Need"] - asset["Liquidity"])
    discipline_gap = max(0, asset["Discipline Required"] - profile["Discipline"])
    return max(0.0, 100 - 13 * risk_gap - 14 * horizon_gap - 15 * liquidity_gap - 12 * discipline_gap)


# ==============================================================================
# DATA
# ==============================================================================

ASSET_DATA = pd.DataFrame(
    [
        {
            "Vehicle": "Cash / cuenta transaccional",
            "Expected Return": 1.0,
            "Risk": 0.8,
            "Liquidity": 5.0,
            "Horizon Required": 1.0,
            "Discipline Required": 1.0,
            "Main Hidden Risk": "inflación y costo de oportunidad",
            "Role": "liquidez inmediata",
        },
        {
            "Vehicle": "CDT local",
            "Expected Return": 2.6,
            "Risk": 1.7,
            "Liquidity": 2.2,
            "Horizon Required": 2.0,
            "Discipline Required": 1.8,
            "Main Hidden Risk": "reinversión, inflación e impuestos",
            "Role": "estabilidad e ingreso nominal",
        },
        {
            "Vehicle": "TES / fondo de deuda local",
            "Expected Return": 3.0,
            "Risk": 2.5,
            "Liquidity": 3.0,
            "Horizon Required": 2.8,
            "Discipline Required": 2.8,
            "Main Hidden Risk": "duration, tasas y riesgo país",
            "Role": "renta fija con sensibilidad macro",
        },
        {
            "Vehicle": "ETF acciones globales",
            "Expected Return": 4.0,
            "Risk": 3.4,
            "Liquidity": 4.5,
            "Horizon Required": 4.3,
            "Discipline Required": 4.0,
            "Main Hidden Risk": "volatilidad, FX y comportamiento",
            "Role": "crecimiento diversificado",
        },
        {
            "Vehicle": "Acción individual cíclica",
            "Expected Return": 4.4,
            "Risk": 4.4,
            "Liquidity": 3.9,
            "Horizon Required": 4.1,
            "Discipline Required": 4.5,
            "Main Hidden Risk": "tesis equivocada, concentración y ciclo",
            "Role": "crecimiento concentrado",
        },
        {
            "Vehicle": "Cripto / narrativa de moda",
            "Expected Return": 4.8,
            "Risk": 5.0,
            "Liquidity": 3.4,
            "Horizon Required": 4.8,
            "Discipline Required": 5.0,
            "Main Hidden Risk": "narrativa, custodia, regulación y FOMO",
            "Role": "exposición especulativa / alternativa",
        },
    ]
)

PROFILE_DATA = {
    "Reserva de emergencia": {
        "Risk Capacity": 1.0,
        "Horizon": 1.0,
        "Liquidity Need": 5.0,
        "Discipline": 2.0,
        "Description": "Necesitas disponibilidad y preservación. El objetivo no es maximizar retorno.",
    },
    "Construcción patrimonial largo plazo": {
        "Risk Capacity": 3.7,
        "Horizon": 4.7,
        "Liquidity Need": 2.0,
        "Discipline": 4.0,
        "Description": "Puedes aceptar volatilidad si el proceso, los costos y el horizonte son coherentes.",
    },
    "Emprendedor con ingresos volátiles": {
        "Risk Capacity": 2.4,
        "Horizon": 3.2,
        "Liquidity Need": 4.0,
        "Discipline": 3.6,
        "Description": "Tu portafolio debe compensar la concentración vital en tu proyecto, no duplicarla.",
    },
    "Inversionista curioso pero principiante": {
        "Risk Capacity": 2.2,
        "Horizon": 3.0,
        "Liquidity Need": 3.0,
        "Discipline": 2.6,
        "Description": "La simplicidad y las reglas importan más que buscar sofisticación prematura.",
    },
}

DESK_DATA = {
    "Colombia & LatAm Equity Desk": ["COLCAP", "acciones locales", "ADRs LatAm", "USD/COP", "liquidez"],
    "U.S. Equity Desk": ["S&P 500", "Nasdaq", "earnings", "Treasury yields", "AI narrative"],
    "Global Developed Markets Equity Desk": ["Europe", "Japan", "MSCI World ex-USA", "EUR/USD", "sector composition"],
    "Colombia Fixed Income Desk": ["TES", "CDTs", "BanRep", "inflación", "curva local"],
    "Global Fixed Income & Rates Desk": ["US 2Y", "US 10Y", "Fed", "real yields", "credit spreads"],
    "FX, Commodities & Macro Risk Desk": ["USD/COP", "DXY", "oil", "gold", "risk-on/risk-off"],
    "Alternatives, Innovation & Digital Assets Desk": ["crypto", "REITs", "thematic ETFs", "robo-advisors", "AI tools"],
}

# ==============================================================================
# SIDEBAR
# ==============================================================================

with st.sidebar:
    st.markdown("## 📈 GPI Learning Lab")
    st.caption("Aurea Capital Partners | Investment Portfolio Management")

    page = st.radio(
        "Selecciona el módulo",
        [
            "Inicio — Mapa de aprendizaje",
            "Clase 1 — Why Invest?",
            "Clase 2 — Macro & Markets",
        ],
    )

    st.divider()
    st.markdown("### Cómo usar la app")
    st.markdown(
        """
        1. Ajusta los supuestos.
        2. Observa cómo cambia la gráfica.
        3. Lee el diagnóstico automático.
        4. Cierra con una regla para tu IPS o para tu división ACP.
        """
    )

    st.divider()
    st.info(
        "No estás intentando adivinar el mercado. Estás construyendo un proceso de inversión que pueda sobrevivir a incertidumbre, emociones y errores normales del mercado."
    )
    st.caption("Herramienta pedagógica. No constituye asesoría financiera personalizada.")

# ==============================================================================
# HOME PAGE
# ==============================================================================

if page == "Inicio — Mapa de aprendizaje":
    header(
        "GPI Learning Lab",
        "Simuladores conceptuales para las primeras dos clases de Gestión de Portafolios de Inversión",
        "A weak investor reacts to noise. A disciplined investor builds a process.",
        "¿Qué regla de inversión puedes construir antes de elegir activos?",
    )

    st.markdown("### Mapa de experiencia")
    c1, c2, c3 = st.columns(3)
    with c1:
        card(
            "Clase 1 — Why Invest?",
            "Explora inflación, inacción, opcionalidad futura, capital personal, trade-offs, inversión vs. especulación e IPS.",
            "soft",
        )
    with c2:
        card(
            "Clase 2 — Macro & Markets",
            "Traduce inflación, tasas, expectativas, sorpresas, intermediarios, Colombia Factor y FX en decisiones de portafolio.",
            "soft",
        )
    with c3:
        card(
            "Aurea Capital Partners",
            "Usa las simulaciones para convertir observaciones de mercado en señales, riesgos, decisiones y reglas operativas.",
            "soft",
        )

    st.markdown("### Lo que debes producir")
    output_df = pd.DataFrame(
        {
            "Momento": ["Antes de invertir", "Al mirar el mercado", "Al cerrar cada módulo"],
            "Producto intelectual": [
                "Una regla de IPS",
                "Una interpretación de señal, no una lista de noticias",
                "Una decisión defendible con riesgos, restricciones y alternativa descartada",
            ],
            "Pregunta de control": [
                "¿Qué nunca deberías hacer aunque el mercado te provoque?",
                "¿Qué cambió: dato, expectativa, liquidez, tasa, moneda o narrativa?",
                "¿La recomendación responde a un mandato o solo a una opinión?",
            ],
        }
    )
    st.dataframe(output_df, use_container_width=True, hide_index=True)

    st.markdown("### Rasgos Xperience integrados")
    st.markdown(
        """
        <span class="pill">Cointeligencia</span>
        <span class="pill">Actitud humanizadora</span>
        <span class="pill">Conexión global</span>
        <span class="pill">Conexión con el entorno</span>
        <span class="pill">Reality Check ACP</span>
        <span class="pill">Aula invertida aplicada</span>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# CLASS 1
# ==============================================================================

elif page == "Clase 1 — Why Invest?":
    header(
        "Clase 1 — Why Invest?",
        "Personal Wealth, Future Choices, and the Discipline of Long-Term Investing",
        "The biggest investment risk is not market volatility — it is not having a plan.",
        "Why should you invest at all — and what happens if you don’t?",
    )

    tabs = st.tabs(
        [
            "1. Inacción e inflación",
            "2. Costo de esperar",
            "3. Tu capital total",
            "4. Trade-offs",
            "5. IPS & decisión",
        ]
    )

    # ------------------------------------------------------------------
    # TAB 1.1 Inaction and inflation
    # ------------------------------------------------------------------
    with tabs[0]:
        st.markdown("### La trampa de no invertir")
        st.write(
            "Observa cómo una decisión aparentemente segura puede destruir poder adquisitivo. "
            "No invertir no elimina el riesgo: lo transforma en inflación, costo de oportunidad y fragilidad futura."
        )

        left, right = st.columns([0.95, 2.05])
        with left:
            st.markdown("#### Configura el escenario")
            initial = st.number_input("Capital inicial", 1_000_000, 500_000_000, 10_000_000, 1_000_000, format="%d")
            annual_contribution = st.number_input("Aporte anual adicional", 0, 100_000_000, 2_400_000, 100_000, format="%d")
            years = st.slider("Horizonte", 1, 40, 15)
            inflation = st.slider("Inflación anual esperada", 0.0, 20.0, 6.0, 0.25) / 100
            cash_rate = st.slider("Rendimiento nominal de cuenta / efectivo", 0.0, 18.0, 2.0, 0.25) / 100
            portfolio_nominal = st.slider("Retorno nominal esperado del portafolio", 0.0, 25.0, 10.0, 0.25) / 100
            tax_drag = st.slider("Impuestos / costos aproximados sobre rendimientos", 0.0, 40.0, 10.0, 1.0) / 100

            cash_after_cost = cash_rate * (1 - tax_drag)
            portfolio_after_cost = portfolio_nominal * (1 - tax_drag)
            real_portfolio_rate = (1 + portfolio_after_cost) / (1 + inflation) - 1
            real_cash_rate = (1 + cash_after_cost) / (1 + inflation) - 1

        with right:
            t = np.arange(years + 1)
            cash_nom = annual_compound_with_contributions(initial, annual_contribution, cash_after_cost, years)
            port_nom = annual_compound_with_contributions(initial, annual_contribution, portfolio_after_cost, years)
            deflator = (1 + inflation) ** t
            cash_real = cash_nom / deflator
            port_real = port_nom / deflator
            contributions_real = (initial + annual_contribution * t) / deflator

            df = pd.DataFrame(
                {
                    "Año": t,
                    "Efectivo / cuenta — valor real": cash_real,
                    "Portafolio disciplinado — valor real": port_real,
                    "Aportes sin rendimiento — valor real": contributions_real,
                }
            )
            fig = make_line_chart(
                df,
                "Año",
                ["Efectivo / cuenta — valor real", "Portafolio disciplinado — valor real", "Aportes sin rendimiento — valor real"],
                "Poder adquisitivo real bajo distintos comportamientos",
                "COP constantes",
            )
            st.plotly_chart(fig, use_container_width=True)

        gap = port_real[-1] - cash_real[-1]
        loss_cash = (cash_real[-1] / (initial + annual_contribution * years) - 1) if (initial + annual_contribution * years) > 0 else 0
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tasa real cuenta", pct(real_cash_rate, 2))
        m2.metric("Tasa real portafolio", pct(real_portfolio_rate, 2))
        m3.metric("Valor real final en cuenta", cop(cash_real[-1]))
        m4.metric("Brecha vs portafolio", cop(gap), delta=cop(gap))

        if real_cash_rate < 0:
            msg = "Tu cuenta conserva nominalmente dinero, pero pierde capacidad de compra. Esa pérdida suele ser silenciosa."
            kind = "trap"
        else:
            msg = "La cuenta supera la inflación en este escenario, pero aún debes evaluar impuestos, liquidez, horizonte y costo de oportunidad."
            kind = "decision"
        card("Lectura de criterio", msg, kind)
        card(
            "Regla IPS que podrías construir",
            "Define cuánto efectivo mantendrás por liquidez y cuánto capital debe trabajar para objetivos de largo plazo. No confundas reserva de emergencia con estrategia patrimonial completa.",
            "decision",
        )

    # ------------------------------------------------------------------
    # TAB 1.2 Delay cost
    # ------------------------------------------------------------------
    with tabs[1]:
        st.markdown("### El costo de esperar")
        st.write(
            "Analiza qué ocurre cuando pospones la inversión. El problema no es solo perder rendimientos; "
            "también pierdes tiempo de capitalización y opcionalidad futura."
        )

        col_a, col_b = st.columns([1, 2])
        with col_a:
            monthly = st.number_input("Aporte mensual", 50_000, 10_000_000, 500_000, 50_000, format="%d")
            years_total = st.slider("Horizonte total", 5, 45, 25)
            wait_years = st.slider("Años que decides esperar", 1, min(15, years_total - 1), 5)
            expected_nominal = st.slider("Retorno nominal anual esperado", 0.0, 20.0, 9.0, 0.25) / 100
            expected_inflation = st.slider("Inflación anual", 0.0, 15.0, 4.0, 0.25) / 100

        with col_b:
            monthly_r = (1 + expected_nominal) ** (1 / 12) - 1
            months = years_total * 12
            wait_months = wait_years * 12
            path_now = []
            path_late = []
            current_now = 0.0
            current_late = 0.0
            for m in range(months + 1):
                if m > 0:
                    current_now = current_now * (1 + monthly_r) + monthly
                    if m > wait_months:
                        current_late = current_late * (1 + monthly_r) + monthly
                path_now.append(current_now / ((1 + expected_inflation) ** (m / 12)))
                path_late.append(current_late / ((1 + expected_inflation) ** (m / 12)))

            df_delay = pd.DataFrame(
                {
                    "Año": np.arange(months + 1) / 12,
                    "Empiezas hoy": path_now,
                    f"Esperas {wait_years} años": path_late,
                }
            )
            fig_delay = make_line_chart(
                df_delay,
                "Año",
                ["Empiezas hoy", f"Esperas {wait_years} años"],
                "Costo real de posponer el proceso de inversión",
                "Valor real acumulado",
            )
            st.plotly_chart(fig_delay, use_container_width=True)

        delay_gap = path_now[-1] - path_late[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric("Valor real si empiezas hoy", cop(path_now[-1]))
        c2.metric(f"Valor real si esperas {wait_years} años", cop(path_late[-1]))
        c3.metric("Costo real de esperar", cop(delay_gap), delta=f"-{cop(delay_gap)}")

        card(
            "Pregunta ACP",
            "¿Qué decisión parece más prudente: esperar hasta sentirte listo o empezar con una regla simple y pequeña? Justifica qué riesgo estás aceptando en cada alternativa.",
            "decision",
        )
        card(
            "Trampa conceptual",
            "Creer que esperar no cuesta. Esperar puede ser racional si necesitas liquidez o educación financiera, pero no es una decisión gratuita.",
            "trap",
        )

    # ------------------------------------------------------------------
    # TAB 1.3 Capital map
    # ------------------------------------------------------------------
    with tabs[2]:
        st.markdown("### Tu portafolio empieza antes del dinero")
        st.write(
            "Califica tus distintas formas de capital. La inversión personal no comienza con un ticker; comienza cuando ordenas tus recursos, restricciones y riesgos."
        )

        c_left, c_right = st.columns([1.1, 1.9])
        with c_left:
            st.markdown("#### Autoevaluación 1–5")
            financial_capital = st.slider("Capital financiero", 1, 5, 2)
            human_capital = st.slider("Capital humano", 1, 5, 4)
            time_capital = st.slider("Capital temporal / horizonte", 1, 5, 5)
            reputation_capital = st.slider("Capital reputacional", 1, 5, 3)
            emotional_capital = st.slider("Capital emocional ante incertidumbre", 1, 5, 3)
            entrepreneurial_capital = st.slider("Capital emprendedor", 1, 5, 3)

        with c_right:
            labels = [
                "Financiero",
                "Humano",
                "Temporal",
                "Reputacional",
                "Emocional",
                "Emprendedor",
            ]
            values = [
                financial_capital,
                human_capital,
                time_capital,
                reputation_capital,
                emotional_capital,
                entrepreneurial_capital,
            ]
            fig_cap = make_radar(labels, {"Tu mapa de capital": values}, "Mapa de capital personal")
            st.plotly_chart(fig_cap, use_container_width=True)

        concentration = max(values) - min(values)
        avg_score = np.mean(values)
        diagnosis, color = diagnostic_badge(avg_score, 3.7, 2.6, True)
        st.markdown(
            f"""
            <div class="soft-card">
                <strong>Diagnóstico de coherencia:</strong> <span style="color:{color}; font-weight:800;">{diagnosis}</span><br>
                Tu puntaje promedio es <strong>{avg_score:.1f}/5</strong> y la brecha entre tu capital más fuerte y tu capital más débil es <strong>{concentration:.1f}</strong> puntos.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if emotional_capital <= 2:
            card(
                "Advertencia conductual",
                "Una estrategia muy volátil puede ser técnicamente razonable y emocionalmente imposible de sostener. Tu IPS debe protegerte de vender bajo presión.",
                "trap",
            )
        if financial_capital <= 2 and time_capital >= 4:
            card(
                "Ventaja silenciosa",
                "Aunque tu capital financiero inicial sea bajo, tu horizonte puede ser una ventaja poderosa si construyes disciplina temprano.",
                "decision",
            )
        if entrepreneurial_capital >= 4:
            card(
                "Conexión emprendedora",
                "Si tu vida ya concentra riesgo en un proyecto, tu portafolio financiero no debería replicar esa fragilidad. Debe funcionar como infraestructura de estabilidad.",
                "decision",
            )

    # ------------------------------------------------------------------
    # TAB 1.4 Trade-offs
    # ------------------------------------------------------------------
    with tabs[3]:
        st.markdown("### El mapa de trade-offs")
        st.write(
            "Compara vehículos desde cinco dimensiones. Un activo no es bueno o malo en abstracto: "
            "su calidad depende del mandato, el horizonte, la liquidez, el riesgo y la disciplina requerida."
        )

        col_1, col_2 = st.columns([1, 2])
        with col_1:
            profile_name = st.selectbox("Perfil / mandato ACP", list(PROFILE_DATA.keys()))
            selected_assets = st.multiselect(
                "Vehículos para comparar",
                ASSET_DATA["Vehicle"].tolist(),
                default=["CDT local", "ETF acciones globales", "Cripto / narrativa de moda"],
            )
            st.caption(PROFILE_DATA[profile_name]["Description"])

        with col_2:
            filtered = ASSET_DATA[ASSET_DATA["Vehicle"].isin(selected_assets)]
            labels = ["Retorno", "Riesgo", "Liquidez", "Horizonte", "Disciplina"]
            series = {}
            for _, row in filtered.iterrows():
                series[row["Vehicle"]] = [
                    row["Expected Return"],
                    row["Risk"],
                    row["Liquidity"],
                    row["Horizon Required"],
                    row["Discipline Required"],
                ]
            if series:
                st.plotly_chart(make_radar(labels, series, "Perfil comparado de vehículos"), use_container_width=True)
            else:
                st.warning("Selecciona al menos un vehículo.")

        profile = PROFILE_DATA[profile_name]
        score_df = ASSET_DATA.copy()
        score_df["Suitability Score"] = score_df.apply(lambda r: suitability_score(r, profile), axis=1)
        score_df = score_df.sort_values("Suitability Score", ascending=False)

        fig_scatter = px.scatter(
            ASSET_DATA,
            x="Risk",
            y="Expected Return",
            size="Liquidity",
            color="Horizon Required",
            hover_name="Vehicle",
            hover_data=["Main Hidden Risk", "Role"],
            title="Retorno esperado, riesgo, liquidez y horizonte requerido",
            labels={
                "Risk": "Riesgo / volatilidad percibida",
                "Expected Return": "Retorno esperado",
                "Liquidity": "Liquidez",
                "Horizon Required": "Horizonte requerido",
            },
        )
        fig_scatter.update_layout(template="plotly_white", height=420)
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.markdown("#### Ranking pedagógico de coherencia con el mandato")
        st.dataframe(
            score_df[["Vehicle", "Suitability Score", "Role", "Main Hidden Risk"]],
            use_container_width=True,
            hide_index=True,
        )

        card(
            "Regla de oro",
            "Si un producto promete alto retorno, bajo riesgo y liquidez perfecta, no has encontrado magia financiera: falta identificar el costo, la restricción o el riesgo escondido.",
            "trap",
        )

    # ------------------------------------------------------------------
    # TAB 1.5 IPS & decision
    # ------------------------------------------------------------------
    with tabs[4]:
        st.markdown("### IPS Builder: de opinión a mandato")
        st.write(
            "Construye un borrador mínimo de IPS. No estás escogiendo activos todavía; estás definiendo las reglas que deberán gobernar tus decisiones futuras."
        )

        st.markdown("#### Filtro inversión vs. especulación")
        f1, f2, f3 = st.columns(3)
        with f1:
            analysis = st.slider("Análisis del activo", 0, 5, 3)
            horizon = st.slider("Horizonte definido", 0, 5, 4)
        with f2:
            value_link = st.slider("Conexión con valor / flujos / función", 0, 5, 3)
            risk_limits = st.slider("Límites de riesgo", 0, 5, 3)
        with f3:
            rules = st.slider("Reglas previas", 0, 5, 2)
            fomo = st.slider("Influencia de FOMO / moda", 0, 5, 2)

        discipline_score = (analysis + horizon + value_link + risk_limits + rules + (5 - fomo)) / 30 * 100
        diagnosis, color = diagnostic_badge(discipline_score, 75, 50, True)
        st.markdown(
            f"""
            <div class="soft-card">
            <strong>Puntaje de disciplina de la decisión:</strong>
            <span style="color:{color}; font-weight:800;">{discipline_score:.0f}/100 — {diagnosis}</span><br>
            Una decisión se parece más a inversión cuando existe análisis, horizonte, vínculo con valor, límites de riesgo y reglas. Se parece más a especulación cuando depende principalmente de que alguien pague más después.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()
        c_ips1, c_ips2 = st.columns(2)
        with c_ips1:
            st.markdown("#### Mandato")
            goal = st.selectbox(
                "Objetivo principal del capital",
                [
                    "Reserva de estabilidad",
                    "Construcción patrimonial de largo plazo",
                    "Fondo para emprendimiento futuro",
                    "Educación / proyecto personal",
                ],
            )
            ips_horizon = st.selectbox("Horizonte indiscutible", ["Menos de 1 año", "1 a 3 años", "3 a 5 años", "Más de 5 años"])
            liquidity = st.selectbox("Necesidad de liquidez", ["Muy alta", "Alta", "Media", "Baja"])
            max_drawdown = st.selectbox("Caída temporal tolerable sin vender por pánico", ["0%", "-5%", "-15%", "-30%", "Más de -30%"])
        with c_ips2:
            st.markdown("#### Reglas operativas")
            contribution_rule = st.text_input("Regla de aporte", "Invertiré un monto fijo con periodicidad definida, salvo que cambie mi liquidez personal.")
            exclusion_rule = st.text_input("Regla de exclusión", "No compraré activos que no entienda o cuya tesis dependa solo de moda/FOMO.")
            crisis_rule = st.text_input("Regla de crisis", "Ante una caída fuerte, revisaré tesis, horizonte y liquidez antes de vender.")
            review_rule = st.text_input("Regla de revisión", "Revisaré mi IPS periódicamente, no cada vez que cambie el precio.")

        ips_text = f"""AUREA CAPITAL PARTNERS — BORRADOR MÍNIMO DE IPS

Objetivo principal: {goal}
Horizonte: {ips_horizon}
Necesidad de liquidez: {liquidity}
Caída temporal tolerable: {max_drawdown}

Reglas operativas:
1. Aporte y disciplina: {contribution_rule}
2. Exclusiones: {exclusion_rule}
3. Protocolo de crisis: {crisis_rule}
4. Revisión: {review_rule}

Principio rector:
No intento adivinar el mercado. Estoy construyendo un proceso de inversión que pueda sobrevivir a incertidumbre, emociones y errores normales del mercado.
"""
        st.code(ips_text, language="text")
        download_text_button("Descargar borrador IPS", ips_text, "borrador_ips_acp.txt")

        card(
            "Cierre de Clase 1",
            "Una recomendación sin mandato es solo una opinión. Una recomendación con mandato, evidencia y reglas empieza a parecerse a una decisión profesional.",
            "quote",
        )

# ==============================================================================
# CLASS 2
# ==============================================================================

elif page == "Clase 2 — Macro & Markets":
    header(
        "Clase 2 — Macroeconomic Context and Financial Markets",
        "How the Economy Shapes Investment Opportunities & Retail Realities",
        "Markets move not only because of fundamentals, but because of expectations about the future.",
        "How does the macroeconomic environment affect your investment decisions — even if you are a retail investor?",
    )

    tabs2 = st.tabs(
        [
            "1. Motor macro",
            "2. Expectativas y sorpresas",
            "3. Sistema financiero real",
            "4. Colombia Factor",
            "5. ACP Market Brief",
        ]
    )

    # ------------------------------------------------------------------
    # TAB 2.1 Macro engine
    # ------------------------------------------------------------------
    with tabs2[0]:
        st.markdown("### Macro Transmission Engine")
        st.write(
            "Mueve los choques macro y observa cómo se transmiten a bonos, acciones, liquidez, moneda y crédito. "
            "La macro no te dice exactamente qué comprar, pero cambia el terreno sobre el que vive tu portafolio."
        )

        left, right = st.columns([1, 2])
        with left:
            st.markdown("#### Choques")
            rate_shock_bps = st.slider("Choque de tasas de política", -300, 300, 100, 25)
            inflation_shock_pp = st.slider("Sorpresa de inflación", -3.0, 3.0, 0.8, 0.1)
            growth_shock_pp = st.slider("Sorpresa de crecimiento", -4.0, 4.0, -1.0, 0.25)
            risk_premium_bps = st.slider("Cambio en prima de riesgo país / mercado", -300, 500, 100, 25)
            bond_duration = st.slider("Duración bono soberano", 1.0, 15.0, 6.0, 0.5)
            equity_duration = st.slider("Sensibilidad equity growth a tasa", 3.0, 25.0, 12.0, 0.5)

        with right:
            delta_y = (rate_shock_bps + 0.35 * risk_premium_bps + 50 * inflation_shock_pp) / 10000
            bond_impact = -bond_duration * delta_y * 100
            growth_equity_impact = -equity_duration * delta_y * 100 + 1.0 * growth_shock_pp
            value_equity_impact = -0.45 * equity_duration * delta_y * 100 + 0.8 * growth_shock_pp
            cash_cdt_impact = max(rate_shock_bps / 100, -2.0)
            fx_impact = 0.40 * (rate_shock_bps / 100) + 0.55 * (risk_premium_bps / 100) + 0.35 * inflation_shock_pp - 0.25 * growth_shock_pp
            liquidity_impact = -0.25 * (rate_shock_bps / 100) - 0.35 * (risk_premium_bps / 100)

            impacts = pd.DataFrame(
                {
                    "Activo / variable": [
                        "Bono soberano largo",
                        "Acciones growth",
                        "Acciones value / defensivas",
                        "CDT nuevo",
                        "USD/COP",
                        "Liquidez de mercado",
                    ],
                    "Impacto estimado (%)": [
                        bond_impact,
                        growth_equity_impact,
                        value_equity_impact,
                        cash_cdt_impact,
                        fx_impact,
                        liquidity_impact,
                    ],
                }
            )
            fig_bar = px.bar(
                impacts,
                x="Activo / variable",
                y="Impacto estimado (%)",
                title="Impacto pedagógico estimado del escenario macro",
                text_auto=".1f",
            )
            fig_bar.update_layout(template="plotly_white", height=430, xaxis_tickangle=-20)
            st.plotly_chart(fig_bar, use_container_width=True)

        card(
            "Regla causal",
            "Macro matters when it changes cash flows, discount rates, risk premiums, liquidity, or currency.",
            "quote",
        )

        chain_cols = st.columns(5)
        chain = [
            ("Dato", "inflación, empleo, crecimiento"),
            ("Expectativa", "consenso y narrativa previa"),
            ("Sorpresa", "diferencia frente a lo esperado"),
            ("Canal", "tasas, moneda, liquidez, primas"),
            ("Portafolio", "bonos, acciones, FX, efectivo"),
        ]
        for col, (title, body) in zip(chain_cols, chain):
            with col:
                card(title, body, "soft")

        if bond_impact < -5:
            card(
                "Trampa conceptual",
                "Una subida de tasas puede mejorar el rendimiento de nuevos instrumentos, pero destruir precio de bonos que ya estaban en el portafolio. No confundas tasa de entrada con mark-to-market.",
                "trap",
            )

    # ------------------------------------------------------------------
    # TAB 2.2 Expectations vs surprises
    # ------------------------------------------------------------------
    with tabs2[1]:
        st.markdown("### Expectations vs. Surprises")
        st.write(
            "Los mercados no reaccionan solo al dato publicado. Reaccionan a la diferencia entre el dato, la expectativa y lo que ese cambio implica para tasas, liquidez y valoración."
        )

        col_x, col_y = st.columns([1, 2])
        with col_x:
            indicator = st.selectbox("Indicador macro", ["Inflación", "Empleo", "Tasa de política", "Crecimiento"])
            expected = st.number_input("Expectativa del consenso", value=5.0, step=0.1)
            actual = st.number_input("Dato publicado", value=6.0, step=0.1)
            market_position = st.selectbox("Narrativa previa del mercado", ["Esperaba recortes de tasas", "Esperaba tasas estables", "Esperaba endurecimiento monetario"])

        surprise = actual - expected
        hawkish_score = 0.0
        if indicator in ["Inflación", "Empleo", "Crecimiento"]:
            hawkish_score = surprise
        elif indicator == "Tasa de política":
            hawkish_score = surprise * 1.4
        if market_position == "Esperaba recortes de tasas":
            hawkish_score += 0.8
        elif market_position == "Esperaba endurecimiento monetario":
            hawkish_score -= 0.4

        if hawkish_score > 0.4:
            reading = "hawkish"
            narrative = "El mercado puede anticipar tasas más altas por más tiempo. Bonos de duración larga y acciones growth tienden a sufrir."
            rate_move = [0, 0.10, 0.16, 0.18, 0.20]
            equity_move = [0, -0.8, -1.5, -2.0, -2.4]
        elif hawkish_score < -0.4:
            reading = "dovish"
            narrative = "El mercado puede anticipar menor presión de tasas. Bonos y activos de riesgo pueden recibir apoyo si no hay miedo de recesión severa."
            rate_move = [0, -0.08, -0.13, -0.16, -0.18]
            equity_move = [0, 0.7, 1.3, 1.8, 2.1]
        else:
            reading = "mostly priced in"
            narrative = "El dato no altera mucho la narrativa previa. El mercado puede moverse poco o buscar otra señal."
            rate_move = [0, 0.01, 0.00, 0.01, 0.00]
            equity_move = [0, 0.05, -0.02, 0.04, 0.00]

        with col_y:
            times = ["Antes", "Publicación", "+5 min", "+30 min", "Cierre"]
            df_news = pd.DataFrame(
                {
                    "Momento": times,
                    "Cambio tasa 10Y (p.p.)": rate_move,
                    "Cambio equity (%)": equity_move,
                }
            )
            fig_news = go.Figure()
            fig_news.add_trace(go.Scatter(x=times, y=df_news["Cambio tasa 10Y (p.p.)"], name="Tasa 10Y", mode="lines+markers", yaxis="y1"))
            fig_news.add_trace(go.Scatter(x=times, y=df_news["Cambio equity (%)"], name="Equity", mode="lines+markers", yaxis="y2"))
            fig_news.update_layout(
                title="Reacción pedagógica intradía ante la sorpresa",
                yaxis=dict(title="Cambio tasa 10Y (p.p.)"),
                yaxis2=dict(title="Cambio equity (%)", overlaying="y", side="right"),
                template="plotly_white",
                height=430,
                hovermode="x unified",
            )
            st.plotly_chart(fig_news, use_container_width=True)

        m1, m2, m3 = st.columns(3)
        m1.metric("Sorpresa", f"{surprise:+.2f}")
        m2.metric("Lectura dominante", reading.upper())
        m3.metric("Pregunta clave", "¿Qué cambia en tasas?")
        card("Lectura de mercado", narrative, "decision")
        card(
            "Trampa conceptual",
            "Un buen dato económico puede ser mala noticia para algunos activos si implica tasas más altas, menor liquidez o menor probabilidad de recortes.",
            "trap",
        )

    # ------------------------------------------------------------------
    # TAB 2.3 Financial system map
    # ------------------------------------------------------------------
    with tabs2[2]:
        st.markdown("### Reality Check ACP: ¿dónde ocurre realmente la inversión?")
        st.write(
            "Antes de preguntar qué comprar, pregunta dónde, cómo, con quién, a qué costo, bajo qué reglas y con qué riesgos operativos puedes invertir."
        )

        st.markdown("#### Mapa del sistema financiero")
        labels = [
            "Hogares con excedentes",
            "Empresas",
            "Gobierno",
            "Bancos",
            "Comisionistas",
            "Fiduciarias / FIC",
            "Mercado monetario",
            "Mercado de capitales",
            "CDT",
            "TES",
            "Acciones",
            "Fondos / ETFs",
            "Inversionista retail",
        ]
        source = [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 7, 7, 8, 9, 10, 11]
        target = [3, 4, 5, 7, 7, 8, 7, 11, 8, 9, 10, 11, 12, 12, 12, 12]
        value = [8, 5, 4, 5, 4, 4, 4, 6, 3, 4, 4, 5, 4, 4, 3, 5]
        fig_sankey = go.Figure(
            data=[
                go.Sankey(
                    node=dict(label=labels, pad=15, thickness=15),
                    link=dict(source=source, target=target, value=value),
                )
            ]
        )
        fig_sankey.update_layout(title="De excedentes y necesidades a productos reales", height=520)
        st.plotly_chart(fig_sankey, use_container_width=True)

        st.markdown("#### Checklist de implementación")
        product = st.selectbox("Selecciona una decisión retail", ["Abrir un CDT", "Comprar TES", "Invertir en fondo de deuda", "Comprar acción local", "Comprar ETF global", "Usar broker internacional"])
        checklist = {
            "Abrir un CDT": ["Banco o plataforma", "Tasa efectiva anual", "Plazo", "Penalidad/liquidez", "Seguro de depósito", "Impuestos sobre rendimientos"],
            "Comprar TES": ["Comisionista/plataforma autorizada", "Precio limpio/sucio", "YTM", "Duración", "Liquidez secundaria", "Riesgo país y tasas"],
            "Invertir en fondo de deuda": ["Fiduciaria/administradora", "Reglamento", "Comisión", "Perfil de duración", "Calidad crediticia", "Liquidez de rescate"],
            "Comprar acción local": ["Comisionista", "Spread", "Volumen", "Gobierno corporativo", "Dividendos", "Riesgo de concentración local"],
            "Comprar ETF global": ["Broker", "Expense ratio", "Domicilio", "Réplica", "Tracking error", "FX e impuestos"],
            "Usar broker internacional": ["Jurisdicción", "Custodia", "Comisiones", "FX", "Impuestos", "Protección al inversionista"],
        }
        st.dataframe(pd.DataFrame({"Aspecto que debes verificar": checklist[product]}), use_container_width=True, hide_index=True)

        recommendation = st.text_area("Recomendación concreta ACP", "Recomendaría esta vía solo si...")
        discarded = st.text_area("Alternativa descartada y razón", "Descartaría... porque...")
        rule = st.text_input("Regla operativa para IPS / portafolio", "Antes de invertir, verificaré costos, liquidez, regulación y coherencia con mi horizonte.")

        rc_text = f"""REALITY CHECK ACP — IMPLEMENTACIÓN REAL

Decisión analizada: {product}

Recomendación concreta:
{recommendation}

Alternativa descartada:
{discarded}

Regla operativa:
{rule}
"""
        st.code(rc_text, language="text")
        download_text_button("Descargar Reality Check ACP", rc_text, "reality_check_acp.txt")

    # ------------------------------------------------------------------
    # TAB 2.4 Colombia Factor
    # ------------------------------------------------------------------
    with tabs2[3]:
        st.markdown("### Colombia Factor: familiaridad no es seguridad")
        st.write(
            "Simula cómo concentración local, inflación, devaluación, riesgo país y activos globales pueden cambiar el resultado de un portafolio medido desde Colombia."
        )

        col_cf1, col_cf2 = st.columns([1, 2])
        with col_cf1:
            home_bias = st.slider("Asignación en activos Colombia", 0, 100, 80, 5) / 100
            years_cf = st.slider("Horizonte del escenario", 1, 15, 5)
            local_return = st.slider("Retorno nominal local esperado", 0.0, 25.0, 10.0, 0.5) / 100
            global_usd_return = st.slider("Retorno global esperado en USD", -10.0, 20.0, 7.0, 0.5) / 100
            cop_devaluation = st.slider("Devaluación anual COP/USD", -10.0, 25.0, 5.0, 0.5) / 100
            local_inflation = st.slider("Inflación local", 0.0, 20.0, 6.0, 0.5) / 100
            country_risk_drag = st.slider("Arrastre por riesgo país / liquidez", 0.0, 8.0, 1.5, 0.25) / 100

        with col_cf2:
            t_cf = np.arange(years_cf + 1)
            global_cop_return = (1 + global_usd_return) * (1 + cop_devaluation) - 1
            local_net = max(local_return - country_risk_drag, -0.95)
            combined_nominal = home_bias * local_net + (1 - home_bias) * global_cop_return

            local_path = 100 * ((1 + local_net) ** t_cf) / ((1 + local_inflation) ** t_cf)
            global_path = 100 * ((1 + global_cop_return) ** t_cf) / ((1 + local_inflation) ** t_cf)
            combined_path = 100 * ((1 + combined_nominal) ** t_cf) / ((1 + local_inflation) ** t_cf)

            df_cf = pd.DataFrame(
                {
                    "Año": t_cf,
                    "100% Colombia — real COP": local_path,
                    "100% global — real COP": global_path,
                    "Portafolio combinado — real COP": combined_path,
                }
            )
            fig_cf = make_line_chart(
                df_cf,
                "Año",
                ["100% Colombia — real COP", "100% global — real COP", "Portafolio combinado — real COP"],
                "Base 100: desempeño real medido desde Colombia",
                "Índice real base 100",
            )
            st.plotly_chart(fig_cf, use_container_width=True)

        home_bias_score = home_bias * 100
        if home_bias_score >= 80:
            card(
                "Advertencia de concentración",
                "Tu portafolio está altamente expuesto al mismo país donde probablemente están tu empleo, tus ingresos, tu familia, tus gastos y buena parte de tu patrimonio no financiero.",
                "trap",
            )
        elif home_bias_score <= 30:
            card(
                "Advertencia de implementación",
                "Baja concentración local puede reducir riesgo país, pero introduce FX, jurisdicción, costos, impuestos y riesgo operativo. Diversificar afuera no elimina el riesgo: lo transforma.",
                "trap",
            )
        else:
            card(
                "Lectura balanceada",
                "Existe una combinación más razonable entre familiaridad local y exposición global. El punto no es abandonar Colombia; es evitar que la familiaridad sustituya el análisis.",
                "decision",
            )

        card("Frase clave", "Home bias feels familiar, but familiarity is not the same as safety.", "quote")

    # ------------------------------------------------------------------
    # TAB 2.5 ACP Market Brief
    # ------------------------------------------------------------------
    with tabs2[4]:
        st.markdown("### ACP Market Opening Brief Builder")
        st.write(
            "Convierte una noticia o movimiento semanal en una señal de inversión. No reportes titulares: interpreta qué cambió, por qué podría importar y qué debe monitorear un inversionista."
        )

        desk = st.selectbox("División ACP", list(DESK_DATA.keys()))
        st.markdown("**Señales sugeridas para monitorear:** " + ", ".join(DESK_DATA[desk]))

        b1, b2 = st.columns(2)
        with b1:
            movement = st.text_area("1. Movimiento clave observado", "Ej.: El rendimiento del Treasury 10Y subió durante la semana...")
            catalyst = st.text_area("2. Posible catalizador", "Ej.: El dato de inflación sorprendió al alza frente al consenso...")
            signal = st.text_area("3. Señal a monitorear", "Ej.: Próximo dato de inflación / reunión de banco central / spread...")
        with b2:
            implication = st.text_area("4. Implicación general para portafolio", "Ej.: Revisar duración, exposición a growth, liquidez y moneda...")
            risk = st.text_area("5. Riesgo o trampa conceptual", "Ej.: No confundir buena noticia económica con buena noticia para precios...")
            conclusion = st.text_area("6. Mini-conclusión ejecutiva", "Ej.: No recomendamos cambiar la estrategia por ruido semanal, pero sí monitorear...")

        brief_text = f"""ACP MARKET OPENING BRIEF

Desk: {desk}

1. Key weekly movement:
{movement}

2. Probable catalyst:
{catalyst}

3. Signal to monitor next:
{signal}

4. Portfolio implication:
{implication}

5. Risk / conceptual trap:
{risk}

6. Executive mini-conclusion:
{conclusion}

Standard: What changed? Why might it matter? What risk does it reveal? What should an investor monitor next?
"""
        st.code(brief_text, language="text")
        download_text_button("Descargar ACP Market Brief", brief_text, "acp_market_brief.txt")

        st.markdown("#### Checklist de calidad")
        check_df = pd.DataFrame(
            {
                "Criterio": [
                    "No es una lista de titulares",
                    "Identifica catalizador probable",
                    "Conecta con mecanismo financiero",
                    "Explica implicación para portafolio",
                    "Incluye riesgo o trampa conceptual",
                    "Cierra con mini-conclusión ejecutiva",
                ],
                "Pregunta de verificación": [
                    "¿Dices qué cambió?",
                    "¿Dices por qué pudo cambiar?",
                    "¿Mencionas tasas, flujos, liquidez, moneda, valoración, riesgo o expectativas?",
                    "¿Afecta duración, equity, FX, liquidez, costos o benchmark?",
                    "¿Evitas conclusiones demasiado seguras?",
                    "¿Puede decirse en menos de 60 segundos?",
                ],
            }
        )
        st.dataframe(check_df, use_container_width=True, hide_index=True)

        card(
            "Cierre de Clase 2",
            "No necesitas predecir la economía. Pero sí debes entender el ambiente donde vive tu portafolio.",
            "quote",
        )
