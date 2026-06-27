import streamlit as st
import numpy as np

st.set_page_config(layout="wide", page_title="Cálculo P80 Planta PukaMani")

# TÍTULO GRANDE ARRIBA
st.title("⚒️ Cálculo P80 Planta PukaMani")

# CSS: 72px LETRA EN 50px CUADRO. SIN BORDE
st.markdown("""
<style>
div.stButton > button {
    height: 50px; /* LOS 3 BOTONES 50px */
    width: 100%;
    border-radius: 8px;
    padding: 0;
    margin: 0;
    box-sizing: border-box;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* CORTA LO QUE SOBRA DE 72px */
}
div.stButton > button[kind="primary"] { /* Rojo Calcular */
    background-color: #C0392B; 
    color: white;
    border: none;
    font-size: 16px; 
}
div.stButton > button[kind="secondary"] { /* Verde Limpiar */
    background-color: #229954; 
    color: white;
    border: none;
    font-size: 16px; 
}
div.stButton > button[kind="tertiary"] { /* P80 */
    background-color: #EBF5FB; /* Celeste como tu foto */
    color: #1A5276; /* AZUL FUERTE */
    border: none; /* SIN BORDE */
    font-size: 72px; /* GIGANTE */
    font-weight: 800;
    line-height: 50px; /* Centra lo que entra */
}
div.stButton > button[kind="tertiary"]:disabled {opacity: 1; cursor: default;}
</style>
""", unsafe_allow_html=True)

MALLAS_UM = np.array([297, 210, 149, 105, 74, 44, 37, 0])
NOMBRES = ["50 | 297 µm", "70 | 210 µm", "100 | 149 µm", "140 | 105 µm", "200 | 74 µm", "325 | 44 µm", "400 | 37 µm", "Base | < 37 µm"]

if 'masas' not in st.session_state: st.session_state.masas = [0.0] * 7 
if 'mtotal' not in st.session_state: st.session_state.mtotal = 0.0 
if 'p80_val' not in st.session_state: st.session_state.p80_val = "— µm"

st.number_input("MASA TOTAL [g]", key="mtotal", format="%.2f")

col1, col2 = st.columns(2)
with col1:
    st.session_state.masas[0] = st.number_input(NOMBRES[0], key="g50", format="%.1f")
    st.session_state.masas[2] = st.number_input(NOMBRES[2], key="g100", format="%.1f")
    st.session_state.masas[4] = st.number_input(NOMBRES[4], key="g200", format="%.1f")
    st.session_state.masas[6] = st.number_input(NOMBRES[6], key="g400", format="%.1f")
with col2:
    st.session_state.masas[1] = st.number_input(NOMBRES[1], key="g70", format="%.1f")
    st.session_state.masas[3] = st.number_input(NOMBRES[3], key="g140", format="%.1f")
    st.session_state.masas[5] = st.number_input(NOMBRES[5], key="g325", format="%.1f")
    base_calculado = st.session_state.mtotal - sum(st.session_state.masas)
    st.number_input(NOMBRES[7], value=float(base_calculado), disabled=True, format="%.1f")

col1, col2, col3 = st.columns(3)
with col1: calc = st.button("⚡ Calculadora P80", type="primary", use_container_width=True)
with col2: st.button(f"P80 = {st.session_state.p80_val}", type="tertiary", use_container_width=True, disabled=True) # <- 72px
with col3: clean = st.button("🧹 Limpiar", type="secondary", use_container_width=True)

if clean:
    st.session_state.masas = [0.0] * 7; st.session_state.mtotal = 0.0; st.session_state.p80_val = "— µm"; st.rerun()

if calc:
    if st.session_state.mtotal <= 0: st.error("MASA TOTAL > 0"); st.stop()
    if base_calculado < 0: st.error("Suma mallas > MASA TOTAL"); st.stop()
    
    masas = np.append(st.session_state.masas, base_calculado)
    acum = np.cumsum(masas); pct = 100 * (1 - acum / st.session_state.mtotal)
    idx = MALLAS_UM > 0
    p80 = 10**np.interp(np.log10(80), np.log10(np.clip(pct[idx], 1e-6, 100))[::-1], np.log10(MALLAS_UM[idx])[::-1])
    st.session_state.p80_val = f"{p80:.2f} µm".replace(".", ",")
    st.rerun()