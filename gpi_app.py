import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# 1. CONFIGURACIÓN INICIAL Y ESTILOS DE LA APLICACIÓN
# ==============================================================================
st.set_page_config(
    page_title="Investment Portfolio Management Lab | EVAfin & ACP",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para tarjetas, portadas e indicadores
st.markdown("""
<style>
    /* Estilos generales */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
    }
    
    /* Contenedor de encabezado general */
    .main-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border-bottom: 2px solid #38BDF8;
        padding: 20px 25px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    
    /* Tarjetas de métricas personalizadas */
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #38BDF8;
        margin: 5px 0;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Callout conceptual */
    .concept-box {
        background-color: #1E293B;
        border-left: 4px solid #F59E0B;
        padding: 15px 18px;
        border-radius: 0 8px 8px 0;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. FUNCIÓN COMPONENTE: PORTADA DE MÓDULO (COVER HEADER)
# ==============================================================================
def render_module_header(module_num, title, subtitle, quote, author, source, facts):
    """
    Renderiza una portada ejecutiva visualmente atractiva con frase de reflexión
    y datos curiosos/históricos financieros.
    """
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); 
                border-left: 6px solid #38BDF8; 
                padding: 24px 28px; 
                border-radius: 12px; 
                margin-bottom: 20px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="background-color: #0284C7; color: #FFFFFF; font-size: 0.8rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;">
                MÓDULO 0{module_num}
            </span>
            <span style="color: #94A3B8; font-size: 0.85rem; font-weight: 500;">Aurea Capital Partners — Learning Lab</span>
        </div>
        <h2 style="color: #F8FAFC; margin: 0 0 6px 0; font-weight: 700; font-size: 1.75rem;">{title}</h2>
        <p style="color: #38BDF8; font-size: 1.05rem; font-weight: 500; margin: 0 0 18px 0; line-height: 1.4;">{subtitle}</p>
        
        <div style="background: rgba(15, 23, 42, 0.6); border-left: 4px solid #F59E0B; padding: 14px 18px; border-radius: 0 8px 8px 0; margin-top: 10px;">
            <p style="color: #E2E8F0; font-size: 0.98rem; font-style: italic; margin: 0 0 6px 0; line-height: 1.5;">
                "{quote}"
            </p>
            <p style="color: #94A3B8; font-size: 0.82rem; margin: 0; font-weight: 500;">
                — <strong style="color: #CBD5E1;">{author}</strong>, <em style="color: #64748B;">{source}</em>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if facts:
        with st.expander("💡 **Pausa de Reflexión e Historia Financiera (Datos Curiosos de Literatura)**", expanded=True):
            cols = st.columns(len(facts))
            for col, (fact_title, fact_desc, fact_src) in zip(cols, facts):
                with col:
                    st.markdown(f"""
                    <div style="background-color: #1E293B; padding: 16px; border-radius: 10px; border: 1px solid #334155; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                                <span style="font-size: 1.1rem;">📜</span>
                                <h4 style="color: #F59E0B; font-size: 0.92rem; font-weight: 700; margin: 0;">{fact_title}</h4>
                            </div>
                            <p style="color: #CBD5E1; font-size: 0.86rem; line-height: 1.45; margin: 0 0 10px 0;">{fact_desc}</p>
                        </div>
                        <div style="border-top: 1px solid #334155; padding-top: 8px; margin-top: 8px;">
                            <p style="color: #64748B; font-size: 0.78rem; font-style: italic; margin: 0;">Fuente: {fact_src}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 3. ENCABEZADO Y NAVEGACIÓN EN BARRA LATERAL
# ==============================================================================
st.sidebar.image("https://img.icons8.com/fluency/96/chart-comb.png", width=64)
st.sidebar.title("EVAfin Suite")
st.sidebar.caption("Gestión de Portafolios de Inversión")

selected_module = st.sidebar.radio(
    "Selecciona el Módulo:",
    [
        "1. Mentalidad del Inversionista & Valor Real",
        "2. Contexto Macroeconómico & Mercados",
        "3. Precios, Ejecución & Disciplina",
        "4. Asignación de Activos & Frontera Eficiente"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Aurea Capital Partners (ACP)** Simulador pedagógico de toma de decisiones de inversión bajo incertidumbre.
""")

# ==============================================================================
# MÓDULO 1: MENTALIDAD DEL INVERSIONISTA Y VALOR REAL
# ==============================================================================
if selected_module.startswith("1"):
    
    render_module_header(
        module_num=1,
        title="The Investor Mindset & Real Capital Protection",
        subtitle="De la ilusión nominal a la preservación real del poder adquisitivo bajo inflación y fricciones",
        quote="El principal problema del inversor —e incluso su peor enemigo— es probablemente él mismo. Invertir no es vencer a los demás en su propio juego, sino controlar tus emociones en el tuyo.",
        author="Benjamin Graham",
        source="El inversor inteligente (Cap. 1)",
        facts=[
            (
                "La Hiperinflación de Weimar (1923)",
                "En la Alemania de Weimar, la inflación fue tan extrema que un café costaba 5.000 marcas al pedirlo y 8.000 marcas al terminarlo. La gente usaba billetes como papel de estufa porque el efectivo valía menos que la leña. Quedarse quieto en efectivo es aceptar una pérdida real garantizada.",
                "Niall Ferguson, El triunfo del dinero (Cap. 2)"
            ),
            (
                "El Origen de la Palabra 'Dinero'",
                "Proviene del latín 'denarius' (moneda romana). Sin embargo, la palabra 'moneda' nació en el templo de la diosa Juno Moneta en Roma, donde se acuñaba el metal para advertir ('monere') a los ciudadanos contra la devaluación del imperio.",
                "Niall Ferguson, El triunfo del dinero (Cap. 1)"
            )
        ]
    )
    
    tab1, tab2, tab3 = st.tabs([
        "📊 Calculadora de Erosión Patrimonial (Tasa Real)",
        "📈 Interés Compuesto vs Ahorro Pasivo",
        "⚙️ Matriz de Fricciones Retail (ACP)"
    ])
    
    with tab1:
        st.subheader("Análisis de Rentabilidad Real Neto de Impuestos e Inflación")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            cap_inicial = st.number_input("Capital Inicial ($)", value=10_000_000, step=1_000_000)
            tasa_nominal = st.slider("Tasa Nominal Anual (%)", 0.0, 20.0, 10.0, 0.25) / 100
            inflacion = st.slider("Inflación Anual (%)", 0.0, 15.0, 5.0, 0.25) / 100
            impuesto = st.slider("Impuesto / Retención a la Renta (%)", 0.0, 35.0, 7.0, 1.0) / 100
            anios = st.slider("Horizonte de Tiempo (Años)", 1, 30, 10)
            
        with col2:
            # Cálculos
            cap_nominal_bruto = cap_inicial * ((1 + tasa_nominal) ** anios)
            ganancia_nominal = cap_nominal_bruto - cap_inicial
            impuestos_totales = ganancia_nominal * impuesto
            cap_nominal_neto = cap_nominal_bruto - impuestos_totales
            
            # Valor real deflactado
            cap_real_neto = cap_nominal_neto / ((1 + inflacion) ** anios)
            
            # Tasa real exacta de Fisher
            tasa_nominal_neta = tasa_nominal * (1 - impuesto)
            tasa_real_fisher = ((1 + tasa_nominal_neta) / (1 + inflacion)) - 1
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Valor Nominal Neto", f"${cap_nominal_neto:,.0f}")
            c2.metric("Poder Adquisitivo Real", f"${cap_real_neto:,.0f}", delta=f"{((cap_real_neto/cap_inicial)-1)*100:.1f}% Real")
            c3.metric("Tasa Real Neta (Fisher)", f"{tasa_real_fisher*100:.2f}% e.a.")
            
            # Gráfico de proyección
            timeline = list(range(0, anios + 1))
            nom_vals = [cap_inicial * ((1 + tasa_nominal_neta) ** t) for t in timeline]
            real_vals = [nom_vals[t] / ((1 + inflacion) ** t) for t in timeline]
            
            df_proj = pd.DataFrame({"Año": timeline, "Valor Nominal Neto": nom_vals, "Poder Adquisitivo Real": real_vals})
            fig = px.line(df_proj, x="Año", y=["Valor Nominal Neto", "Poder Adquisitivo Real"], 
                          title="Erosión del Poder Adquisitivo en el Tiempo",
                          labels={"value": "Monto ($)", "variable": "Concepto"},
                          template="plotly_dark", color_discrete_sequence=["#38BDF8", "#EF4444"])
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f"""
            <div class="concept-box">
            <strong>Lectura de Criterio Financiero:</strong><br>
            Observa que una rentabilidad nominal del <strong>{tasa_nominal*100:.1f}%</strong> se reduce a un retorno real efectivo de solo <strong>{tasa_real_fisher*100:.2f}%</strong> al descontar la retención y la inflación. Tu verdadero crecimiento patrimonial depende únicamente de la tasa real.
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.subheader("Simulador de Comprensión del Interés Compuesto")
        col_a, col_b = st.columns([1, 2])
        with col_a:
            aporte_mensual = st.number_input("Aporte Mensual ($)", value=500_000, step=50_000)
            ret_anual = st.slider("Retorno Esperado Anual (%)", 1.0, 18.0, 8.0) / 100
            inf_anual = st.slider("Inflación Esperada Anual (%)", 1.0, 12.0, 4.0) / 100
            horizonte = st.slider("Plazo en Años", 5, 40, 20)
            
        with col_b:
            meses = horizonte * 12
            r_mensual = (1 + ret_anual)**(1/12) - 1
            inf_mensual = (1 + inf_anual)**(1/12) - 1
            
            mes_list = list(range(0, meses + 1))
            inv_acum = [aporte_mensual * m for m in mes_list]
            
            comp_nom = [0]
            for m in range(1, meses + 1):
                comp_nom.append((comp_nom[-1] + aporte_mensual) * (1 + r_mensual))
                
            comp_real = [comp_nom[m] / ((1 + inf_mensual)**m) for m in mes_list]
            
            df_comp = pd.DataFrame({"Mes": mes_list, "Capital Invertido": inv_acum, "Acumulado Nominal": comp_nom, "Poder Adquisitivo Real": comp_real})
            
            fig_comp = px.area(df_comp, x="Mes", y=["Capital Invertido", "Acumulado Nominal", "Poder Adquisitivo Real"],
                               title="Curva de Acumulación Compuesta vs. Capital Aportado",
                               template="plotly_dark", color_discrete_sequence=["#64748B", "#10B981", "#38BDF8"])
            st.plotly_chart(fig_comp, use_container_width=True)

    with tab3:
        st.subheader("Fricciones en Vehículos Retail (ACP Reality Check)")
        st.write("Analiza cómo las capas de costos (comisiones, spreads cambiarios, retenciones) afectan el retorno final:")
        
        vehiculos = pd.DataFrame({
            "Vehículo / Canal": ["CDT Bancario Local", "Fondo de Inversión Colectiva (FIC)", "ETF Global (Broker Internacional)", "Acción Local (Comisionista)"],
            "Comisión Admin. Anual": ["0.0%", "1.8%", "0.07%", "0.0%"],
            "Spread Cambiario (FX)": ["0.0%", "0.0%", "1.2%", "0.0%"],
            "Comisión por Transacción": ["$0", "$0", "$2 USD", "0.2% + IVA"],
            "Fricción Clave ACP": ["Liquidez fija / Retención en la fuente", "Comisión de gestión constante", "Costo de giro e impuesto internacional", "Iliquidez y pocos emisores"]
        })
        st.dataframe(vehiculos, use_container_width=True)

# ==============================================================================
# MÓDULO 2: CONTEXTO MACROECONÓMICO Y MERCADOS
# ==============================================================================
elif selected_module.startswith("2"):
    
    render_module_header(
        module_num=2,
        title="Macroeconomic Context & Financial Markets",
        subtitle="Cómo el entorno macroeconómico, la política monetaria y las sorpresas ajustan las valoraciones",
        quote="Los mercados financieros no cotizan los datos económicos del pasado, sino las expectativas sobre el futuro y el grado de sorpresa frente al consenso.",
        author="Howard Marks",
        source="Lo más importante (Cap. 8)",
        facts=[
            (
                "Nathan Rothschild y los Bonos de Waterloo (1815)",
                "Nathan Rothschild usó palomas mensajeras para enterarse de la victoria británica en Waterloo antes que el propio gobierno de Londres. En lugar de entrar en pánico como el público, compró masivamente bonos británicos, consolidando el mercado de deuda más poderoso del siglo XIX.",
                "Niall Ferguson, El triunfo del dinero (Cap. 2)"
            ),
            (
                "El Fenómeno 'Buenas Noticias = Malas Noticias'",
                "En periodos de alta inflación, un reporte de empleo extraordinariamente fuerte (buena noticia económica) desploma las bolsas. El mercado descuenta que el Banco Central subirá las tasas agresivamente para enfriar la economía.",
                "Frederic Mishkin, Financial Markets & Institutions"
            )
        ]
    )
    
    tab1, tab2, tab3 = st.tabs([
        "🔄 Transmisión de Política Monetaria",
        "🎯 Datos vs. Consenso ('Priced In')",
        "🇨🇴 El 'Colombia Factor' & Riesgo País"
    ])
    
    with tab1:
        st.subheader("Mecanismo de Transmisión e Impacto en Activos")
        escenario = st.selectbox(
            "Selecciona la decisión del Banco Central (BanRep / FED):",
            ["Subida Agresiva de Tasa de Interés (Hawkish)", "Corte de Tasa para Estimulo (Dovish)", "Choque Inflacionario (Stagflation)"]
        )
        
        col1, col2, col3, col4 = st.columns(4)
        if "Hawkish" in escenario:
            col1.metric("TES / Bonos Larga Duración", "Caída Fuerte", "- Precio ⬇️ Yield ⬆️", delta_color="inverse")
            col2.metric("Acciones de Crecimiento", "Presión Bajista", "Múltiplos se comprimen", delta_color="inverse")
            col3.metric("Tasa de Cambio (Moneda Local)", "Apreciación Promedio", "Flujo de carry trade", delta_color="normal")
            col4.metric("Costo del Crédito / Liquidez", "Encarecimiento", "Demanda se frena", delta_color="inverse")
        elif "Dovish" in escenario:
            col1.metric("TES / Bonos Larga Duración", "Valorización", "- Precio ⬆️ Yield ⬇️", delta_color="normal")
            col2.metric("Acciones / Renta Variable", "Apetito por Riesgo", "Costo de capital cae", delta_color="normal")
            col3.metric("Tasa de Cambio (Moneda Local)", "Presión a Devaluación", "Salida de flujos cortos", delta_color="inverse")
            col4.metric("Costo del Crédito / Liquidez", "Flexibilización", "Mayor liquidez", delta_color="normal")
        else:
            col1.metric("TES / Bonos Larga Duración", "Desvalorización", "Prima de riesgo sube", delta_color="inverse")
            col2.metric("Acciones / Renta Variable", "Alta Volatilidad", "Margen empresarial cae", delta_color="inverse")
            col3.metric("Tasa de Cambio (Moneda Local)", "Volátil / Depreciación", "Aversión global", delta_color="inverse")
            col4.metric("Costo del Crédito / Liquidez", "Restringido", "Incertidumbre alta", delta_color="inverse")

        st.subheader("Sensibilidad de Bonos a Tasas (Duration Aprox.)")
        duration = st.slider("Duration Modificada del Bono (Años)", 1.0, 15.0, 6.0)
        delta_rate = st.slider("Cambio en Tasa de Interés (Puntos Básicos - bps)", -300, 300, 100, 25) / 10000
        
        impacto_precio = -duration * delta_rate
        st.info(f"💡 **Impacto Estimado en Precio:** Un movimiento de **{delta_rate*10000:.0f} bps** en tasas genera una variación aproximada de **{impacto_precio*100:.2f}%** en el precio del bono.")

    with tab2:
        st.subheader("Simulador de Sorpresa de Mercado vs. Expectativas")
        c_exp, c_real = st.columns(2)
        dato_esperado = c_exp.number_input("Dato Esperado por Consenso (IPC %)", value=6.0, step=0.1)
        dato_observado = c_real.number_input("Dato Real Publicado (IPC %)", value=6.5, step=0.1)
        
        sorpresa = dato_observado - dato_esperado
        
        if sorpresa > 0:
            st.error(f"🚨 **Sorpresa Inflacionaria Positiva (+{sorpresa:.2f}%):** El dato salió peor de lo esperado. El mercado descontará tasas más altas por más tiempo.")
        elif sorpresa < 0:
            st.success(f"🎉 **Sorpresa Inflacionaria Negativa ({sorpresa:.2f}%):** La inflación cayó más de lo esperado. Posible rally en renta fija y variable.")
        else:
            st.info("⚖️ **En Línea con el Consenso:** El dato ya estaba 'priced in'. La reacción del mercado será contenida.")

    with tab3:
        st.subheader("Colombia Factor: Prima de Riesgo & Home Bias")
        col_col1, col_col2 = st.columns(2)
        with col_col1:
            embi = st.slider("Riesgo País / EMBI Colombia (bps)", 150, 600, 320)
            usd_cop = st.slider("Tasa de Cambio TRM (USD/COP)", 3500, 5200, 4100)
        with col_col2:
            st.write("**Riesgos de Concentración Doméstica (Home Bias):**")
            st.markdown("""
            - **Mercado de Renta Variable Pequeño:** Pocos emisores líquidos.
            - **Riesgo Cambiario Estructural:** Vulnerabilidad ante precios de commodities (petróleo).
            - **Conclusión ACP:** Mantener 100% del patrimonio en la moneda e historia local no es patriotismo, es un riesgo de concentración no diversificado.
            """)

# ==============================================================================
# MÓDULO 3: PRECIOS, EJECUCIÓN Y DISCIPLINA
# ==============================================================================
elif selected_module.startswith("3"):
    
    render_module_header(
        module_num=3,
        title="Prices, Execution & Investor Discipline",
        subtitle="De la actividad compulsiva de mercado a las decisiones con reglas, liquidez y control conductual",
        quote="El mercado es un manicomio conducido por Mr. Market. Todos los días te ofrece un precio: no está ahí para darte instrucciones, sino para estar a tu servicio cuando sus emociones abren una oportunidad.",
        author="Benjamin Graham",
        source="El inversor inteligente (Cap. 8)",
        facts=[
            (
                "La Ruina de Sir Isaac Newton (1720)",
                "Isaac Newton, una de las mentes más brillantes de la historia, perdió más de £20.000 (millones actuales) en la burbuja de los Mares del Sur. Tras quebrar escribió: 'Puedo calcular el movimiento de los astros celestes, pero no la locura de los hombres'.",
                "Niall Ferguson, El triunfo del dinero (Cap. 3)"
            ),
            (
                "La Primera Acción de la Historia (VOC, 1602)",
                "La Compañía Holandesa de las Indias Orientales emitió en Ámsterdam las primeras acciones negociables del mundo para compartir el riesgo de expediciones navales, dando nacimiento a la primera bolsa formal de valores.",
                "Niall Ferguson, El triunfo del dinero (Cap. 3)"
            )
        ]
    )
    
    tab1, tab2, tab3 = st.tabs([
        "📖 Libro de Órdenes & Slippage",
        "🔄 Dollar Cost Averaging (DCA) vs Lump-Sum",
        "🛡️ Mr. Market & Reglas IPS"
    ])
    
    with tab1:
        st.subheader("Simulador de Ejecución: Bid, Ask & Spreads")
        
        col_ord1, col_ord2 = st.columns([1, 2])
        with col_ord1:
            tipo_orden = st.radio("Tipo de Orden:", ["Market Order (Mercado)", "Limit Order (Límite)"])
            monto_acciones = st.number_input("Cantidad de Acciones a Comprar", value=500, step=50)
            
        with col_ord2:
            # Simulación de Libro de Órdenes
            bids = pd.DataFrame({"Precio Bid (Compra)": [99.8, 99.5, 99.0], "Volumen": [200, 500, 1000]})
            asks = pd.DataFrame({"Precio Ask (Venta)": [100.2, 100.6, 101.5], "Volumen": [150, 300, 600]})
            
            c_b, c_a = st.columns(2)
            c_b.write("**Compradores (Bids)**")
            c_b.dataframe(bids)
            c_a.write("**Vendedores (Asks)**")
            c_a.dataframe(asks)
            
            spread = 100.2 - 99.8
            st.caption(f"Spread Bid-Ask Actual: **${spread:.2f}** ({spread/100.2*100:.2f}%)")
            
            if "Market" in tipo_orden:
                # Cálculo de precio promedio por barrido de libro
                if monto_acciones <= 150:
                    px_prom = 100.2
                elif monto_acciones <= 450:
                    px_prom = (150*100.2 + (monto_acciones-150)*100.6) / monto_acciones
                else:
                    px_prom = (150*100.2 + 300*100.6 + (monto_acciones-450)*101.5) / monto_acciones
                
                slippage = (px_prom - 100.2) / 100.2 * 100
                st.warning(f"⚡ **Ejecución Inmediata.** Precio Promedio Ejecutado: **${px_prom:.2f}** | Slippage: **{slippage:.2f}%**")
            else:
                st.info("🔒 **Orden Límite enviada.** Garantizas precio máximo pero asumes riesgo de no ejecución si el mercado sube.")

    with tab2:
        st.subheader("Simulación Conductual: DCA vs Inversión De Una Vez (Lump-Sum)")
        regimen = st.selectbox("Escenario de Mercado:", ["Volátil con Caída y Recuperación", "Mercado Alcista Constante", "Mercado Bajista Prolongado"])
        
        meses = 12
        if "Caída" in regimen:
            precios = [100, 90, 75, 60, 55, 65, 75, 85, 95, 100, 110, 115]
        elif "Alcista" in regimen:
            precios = [100, 102, 105, 108, 112, 115, 120, 122, 128, 130, 135, 140]
        else:
            precios = [100, 95, 88, 80, 75, 70, 65, 60, 58, 55, 52, 50]
            
        monto_total = 12000
        aporte_m = monto_total / meses
        
        # Lump Sum
        acciones_ls = monto_total / precios[0]
        val_ls = [acciones_ls * p for p in precios]
        
        # DCA
        acciones_dca = 0
        val_dca = []
        for p in precios:
            acciones_dca += aporte_m / p
            val_dca.append(acciones_dca * p)
            
        df_dca = pd.DataFrame({"Mes": list(range(1, 13)), "Precio Activo": precios, "Valor Lump-Sum": val_ls, "Valor DCA": val_dca})
        
        fig_dca = px.line(df_dca, x="Mes", y=["Valor Lump-Sum", "Valor DCA"], title="Evolución Patrimonial: DCA vs. Lump-Sum",
                          template="plotly_dark", color_discrete_sequence=["#EF4444", "#10B981"])
        st.plotly_chart(fig_dca, use_container_width=True)
        
        st.success(f"Final Mes 12 ➔ **Lump-Sum:** ${val_ls[-1]:,.0f} | **DCA:** ${val_dca[-1]:,.0f}. Recuerda: DCA no es para predecir, es para mitigar el pánico conductual.")

    with tab3:
        st.subheader("Perfil del Inversionista y Reglas IPS (Investment Policy Statement)")
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("#### Inversor Defensivo")
            st.write("- Foco en simplicidad, diversificación y bajo mantenimiento.")
            st.write("- Menos margen para errores conductuales.")
            st.write("- Portafolios basados en ETFs indexados globales.")
            
        with col_p2:
            st.markdown("#### Inversor Emprendedor (Enterprising)")
            st.write("- Requiere tiempo, disciplina analítica y estómago emocional.")
            st.write("- Análisis fundamental activo de emisores.")
            st.write("- Riesgo de sobre-operar si confunde actividad con criterio.")

# ==============================================================================
# MÓDULO 4: ASIGNACIÓN DE ACTIVOS Y FRONTERA EFICIENTE
# ==============================================================================
elif selected_module.startswith("4"):
    
    render_module_header(
        module_num=4,
        title="Portfolio Construction & Efficient Allocation",
        subtitle="Construcción de portafolios, correlación, frontera eficiente y gestión de riesgo tail",
        quote="La diversificación es el único 'almuerzo gratis' en las finanzas. No busca maximizar el retorno en el mejor escenario imaginable, sino asegurar la supervivencia de tu patrimonio ante lo impredecible.",
        author="Harry Markowitz",
        source="Premio Nobel de Economía & Creador de la MPT",
        facts=[
            (
                "La Paradoja de Harry Markowitz",
                "Cuando Harry Markowitz ganó el Premio Nobel por formular matemáticamente la optimización de portafolios, le preguntaron cómo había asignado su propia pensión personal. Confesó que usó un simple 50% en acciones y 50% en bonos por tranquilidad emocional.",
                "Camilo Romero, La Teoría Moderna de Portafolios"
            ),
            (
                "El Sesgo de Disposición (Prospect Theory)",
                "Los inversionistas tienden a vender sus activos ganadores demasiado rápido para sentir satisfacción inmediata y mantienen sus activos perdedores durante años esperando 'recuperarse', destruyendo la tasa de retorno compuesto.",
                "Peter Bevelin, Seeking Wisdom / Kahneman & Tversky"
            )
        ]
    )
    
    tab1, tab2, tab3 = st.tabs([
        "🔗 Correlación & 'Free Lunch'",
        "🎯 Monte Carlo & Frontera Eficiente",
        "📉 Stress Testing & Drawdowns"
    ])
    
    with tab1:
        st.subheader("El Efecto Matemático de la Diversificación")
        col_c1, col_c2 = st.columns([1, 2])
        
        with col_c1:
            r1 = st.slider("Retorno Activo A (%)", 0.0, 20.0, 10.0) / 100
            s1 = st.slider("Volatilidad Activo A (%)", 1.0, 30.0, 15.0) / 100
            r2 = st.slider("Retorno Activo B (%)", 0.0, 20.0, 6.0) / 100
            s2 = st.slider("Volatilidad Activo B (%)", 1.0, 30.0, 8.0) / 100
            corr = st.slider("Correlación (Rho AB)", -1.0, 1.0, 0.1, 0.05)
            
        with col_c2:
            w1 = np.linspace(0, 1, 100)
            w2 = 1 - w1
            
            port_returns = w1 * r1 + w2 * r2
            port_vol = np.sqrt((w1**2)*(s1**2) + (w2**2)*(s2**2) + 2*w1*w2*s1*s2*corr)
            
            df_mpt = pd.DataFrame({"Pesos Activo A": w1, "Retorno Portafolio": port_returns, "Riesgo (Volatilidad)": port_vol})
            
            fig_mpt = px.line(df_mpt, x="Riesgo (Volatilidad)", y="Retorno Portafolio",
                              title="Curva de Riesgo-Retorno según Correlación",
                              template="plotly_dark", color_discrete_sequence=["#38BDF8"])
            st.plotly_chart(fig_mpt, use_container_width=True)
            
            st.success("💡 **Observación Clave:** Si la correlación es menor a 1.0, la curva se dobla hacia la izquierda: puedes reducir el riesgo del portafolio por debajo de la volatilidad del activo individual más seguro.")

    with tab2:
        st.subheader("Simulación Monte Carlo de Portafolios (Frontera Eficiente)")
        
        num_portafolios = 800
        np.random.seed(42)
        
        # 3 Activos: Acciones Globales, TES/Bonos, Oro
        means = np.array([0.09, 0.05, 0.04])
        covs = np.array([
            [0.0225, 0.0015, 0.0005],
            [0.0015, 0.0064, -0.0008],
            [0.0005, -0.0008, 0.0196]
        ])
        
        results = np.zeros((3, num_portafolios))
        for i in range(num_portafolios):
            weights = np.random.random(3)
            weights /= np.sum(weights)
            
            p_ret = np.sum(weights * means)
            p_std = np.sqrt(np.dot(weights.T, np.dot(covs, weights)))
            p_sharpe = p_ret / p_std
            
            results[0,i] = p_std
            results[1,i] = p_ret
            results[2,i] = p_sharpe
            
        df_mc = pd.DataFrame({"Volatilidad": results[0], "Retorno Esperado": results[1], "Sharpe Ratio": results[2]})
        
        fig_mc = px.scatter(df_mc, x="Volatilidad", y="Retorno Esperado", color="Sharpe Ratio",
                            title=f"Nube de {num_portafolios} Portafolios Simulados",
                            template="plotly_dark", color_continuous_scale="Viridis")
        st.plotly_chart(fig_mc, use_container_width=True)

    with tab3:
        st.subheader("Stress Testing & Caídas Máximas (Drawdown)")
        st.write("Prueba la resistencia histórica de tu portafolio ante eventos tail (Cisnes Negros):")
        
        crisis = st.selectbox("Selecciona la Crisis Histórica de Referencia:", ["Crisis Financiera Global (2008)", "Crash COVID-19 (2020)", "Choque de Inflación y Tasas (2022)"])
        
        if "2008" in crisis:
            st.error("📉 **Caída Máxima Renta Variable:** -55% | **Tiempo de Recuperación:** 48 Meses")
        elif "2020" in crisis:
            st.warning("📉 **Caída Máxima Renta Variable:** -34% | **Tiempo de Recuperación:** 5 Meses (Rally V-Shape)")
        else:
            st.info("📉 **Caída Simultánea Acciones + Bonos:** -20% Acciones / -16% Bonos (Ruptura temporal de la correlación de cobertura)")

# ==============================================================================
# PIE DE PÁGINA AUREA CAPITAL PARTNERS
# ==============================================================================
st.markdown("---")
st.caption("Aurea Capital Partners (ACP) — Learning Lab | Diseñado para la Asignación de Gestión de Portafolios de Inversión.")