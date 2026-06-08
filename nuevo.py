import streamlit as st

# Configuración de página optimizada para pantallas móviles
st.set_page_config(
    page_title="Mi Calculadora de Insulina",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS específicos para pantallas táctiles y diseño limpio
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    h1 { color: #1e3a8a; font-size: 1.8rem; text-align: center; margin-bottom: 0px; }
    .stSelectbox label, .stNumberInput label { font-size: 0.95rem; font-weight: 600; color: #1e293b; }
    div[data-testid="stMetricValue"] { color: #2563eb; font-size: 2.8rem; font-weight: bold; text-align: center; }
    div[data-testid="stMetricLabel"] { text-align: center; }
    .block-container { padding-top: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 Mi Control de Insulina")
st.markdown("<p style='text-align: center; color: #64748b;'>Hospital Regional de Arica</p>", unsafe_allow_html=True)
st.markdown("---")

# --- MATRIZ CLÍNICA CORREGIDA (Cruce exacto del PDF de Dosis) ---
RANGOS_GLICEMIA = [
    (70, 100), (100, 120), (121, 165), (166, 210), (211, 255),
    (256, 300), (301, 345), (346, 390), (391, 435), (436, 480), (481, 525)
]
CHO_COLUMNAS = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
MATRIZ_DOSIS = [
    [0, -1, 0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7],     # 70 - 100
    [0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8],      # 100 - 120
    [1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9],      # 121 - 165
    [2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 10],     # 166 - 210
    [3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9, 10, 11],    # 211 - 255
    [4, 4, 5, 6, 6, 7, 8, 8, 9, 10, 10, 11, 12],  # 256 - 300
    [5, 5, 6, 7, 7, 8, 9, 9, 10, 11, 11, 12, 13],  # 301 - 345
    [6, 6, 7, 8, 8, 9, 10, 10, 11, 12, 12, 13, 14], # 346 - 390
    [7, 7, 8, 9, 9, 10, 11, 11, 12, 13, 13, 14, 15], # 391 - 435
    [8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16], # 436 - 480
    [9, 9, 10, 11, 11, 12, 13, 13, 14, 15, 15, 16, 17]  # 481 - 525
]

# --- BASE DE DATOS ESTRATIFICADA SEGÚN EL MANUAL DE CONTEO (Libro conteo CHO 2022) ---
# Estructura: Alimento: (Gramos de CHO por porción, Nombre de la Porción)
ALIMENTOS_POR_GRUPO = {
    "🍉 Frutas": {
        "Plátano": (15.0, "1/2 unidad"),
        "Naranja": (15.0, "1 unidad regular"),
        "Manzana": (15.0, "1 unidad pequeña"),
        "Frutillas": (15.0, "1 taza"),
        "Mora": (15.0, "½ taza"),
        "Sandia": (15.0, "1 taza"),
        "Melón": (15.0, "1 taza"),
        "Durazno": (15.0, "1 unidad pequeña"),
        "Cerezas": (15.0, "15 unidades"),
        "Chirimoya": (11.0, "1/4 de unidad"),
        "Pera": (15.0, "1 unidad pequeña"),
        "Piña": (15.0, "3/4 de taza"),
        "Kiwi": (15.0, "2 unidades pequeñas"),
        "Frambuesa": (15.0, "1 taza"),
        "Ciruelas": (15.0, "3 unidades"),
        "Uvas": (15.0, "10 unidades"),
        "Pasas": (16.0, "20 unidades"),
        "Huesillo": (15.0, "2 unidades")
    },
    "🌾 Cereales, Papas y Leguminosas": {
        "Arroz": (30.0, "3/4 taza"),
        "Arroz integral": (30.0, "3/4 taza"),
        "Fideos": (30.0, "3/4 taza"),
        "Cabritas (Popcorn)": (30.0, "1 1/2 taza"),
        "Mote": (30.0, "3/4 taza"),
        "Pan marraqueta/hallulla": (30.0, "1/2 unidad"),
        "Pan de molde": (30.0, "3 rebanadas"),
        "Pan de molde integral": (30.0, "3 rebanadas"),
        "Pan de molde high low": (11.9, "2 rebanadas"),
        "Galletas de soda integrales": (20.0, "6 rebanadas"),
        "Mermelada Regimel": (1.1, "1 cucharada"),
        "Pan amasado": (30.0, "1/4 unidad"),
        "Galletas de agua": (30.0, "8 unidades"),
        "Galletas champaña": (30.0, "5 unidades"),
        "Arvejas": (30.0, "1 1/2 taza"),
        "Camote": (30.0, "1/2 taza"),
        "Choclo": (40.0, "1 taza"),
        "Habas": (30.0, "1 taza"),
        "Papa": (30.0, "1 unidad regular"),
        "Porotos granados": (25.0, "3/4 taza"),
        "Avena": (30.0, "6 cucharadas o 1/2 taza"),
        "Avena Integral": (17.2, "2 cucharadas"),
        "Chia": (6.0, "1 cucharada"),
        "Chuño": (32.0, "4 cucharadas"),
        "Harina Tostada": (30.0, "4 cucharadas"),
        "Maicena": (30.0, "3 cucharadas"),
        "Quinoa": (25.0, "4 cucharadas"),
        "Sémola": (30.0, "3 cucharadas")
    },
    "🥦 Verduras": {
        "Acelga cocida": (5.0, "1/2 taza"),
        "Alcachofa": (6.0, "1 unidad pequeña"),
        "Beterraga": (5.0, "1/2 taza"),
        "Berenjena": (7.0, "1 1/2 taza"),
        "Brócoli": (5.0, "1 taza"),
        "Champiñones": (5.0, "3/4 taza"),
        "Coliflor": (5.0, "1 taza"),
        "Espárrago": (5.0, "5 unidades"),
        "Porotos verdes": (6.0, "3/4 taza"),
        "Espinaca": (5.0, "1/2 taza"),
        "Salsa de tomate": (6.0, "2 cucharadas"),
        "Zanahoria": (5.0, "1 taza"),
        "Zapallo italiano": (6.0, "1 taza"),
        "Zapallo": (5.0, "1/2 taza"),
        "Ajo": (3.0, "8 dientes"),
        "Apio": (3.0, "1 taza"),
        "Cochayuyo": (3.0, "2 ramas"),
        "Lechuga": (2.0, "1 taza"),
        "Pepino": (3.0, "1 taza"),
        "Pimentón": (4.0, "1/2 taza"),
        "Repollo": (3.0, "1 taza")
    },
    "🥛 Lácteos": {
        "Leche descremada": (10.0, "1 taza"),
        "Leche entera": (10.0, "1 taza"),
        "Yogurt": (10.0, "1 unidad"),
        "Huevos": (0.6, "1 unidad"),
        "Quesillo": (0.0, "1 rebanada 3 cm (libre)")
    },
    "🥑 Aceite y Grasas": {
        "Crema de leche": (3.0, "4 cucharaditas"),
        "Crema ácida": (4.0, "1/2 taza"),
        "Crema chantilly": (1.5, "4 cucharadas"),
        "Crema Svelty": (4.0, "1/2 taza"),
        "Almendras": (5.0, "26 unidades"),
        "Avellanas": (7.0, "50 unidades"),
        "Maní": (5.0, "20 unidades"),
        "Nuez": (3.0, "5 unidades"),
        "Pistacho": (7.0, "40 unidades"),
        "Aceitunas": (2.0, "11 unidades"),
        "Palta": (7.0, "3 cucharadas")
    },
    "🍭 Azúcar": {
        "Miel de abeja": (5.0, "1 cucharadita"),
        "Miel de palma": (3.0, "1 cucharadita"),
        "Mergelada promedio": (5.0, "1 cucharadita"),
        "Manjar": (6.0, "1 cucharadita"),
        "Jalea": (4.0, "1 porción regular"),
        "Jugo en polvo": (5.0, "1 cucharadita"),
        "Bebida promedio": (5.0, "1/4 taza"),
        "Jugo néctar promedio": (6.0, "1/4 taza")
    }
}

COMIDAS = ["Desayuno", "Almuerzo", "Once", "Cena"]

# Inicializar listas por cada comida si no existen en el session_state
for c in COMIDAS:
    if f"items_{c}" not in st.session_state:
        # Iniciamos con un ítem vacío por defecto que usa el primer grupo y su primer alimento
        primer_grupo = list(ALIMENTOS_POR_GRUPO.keys())[0]
        primer_alimento = list(ALIMENTOS_POR_GRUPO[primer_grupo].keys())[0]
        st.session_state[f"items_{c}"] = [{"grupo": primer_grupo, "alimento": primer_alimento, "cantidad": 0.0}]

# --- FORMULARIO DE ENTRADA ---
glicemia_input = st.number_input("🔴 Ingresa tu Glicemia actual (mg/dL):", min_value=0, max_value=600, value=110, step=1)

st.markdown("### 🥗 ¿Qué comida vas a calcular ahora?")
comida_seleccionada = st.selectbox("Selecciona el momento del día:", COMIDAS, key="selector_comida")

st.markdown(f"**Alimentos para el {comida_seleccionada}:**")

items_comida = st.session_state[f"items_{comida_seleccionada}"]
filas_a_eliminar = []
cho_comida_actual = 0.0

# Renderizar alimentos dinámicamente según grupo y alimento seleccionados
for i, item in enumerate(items_comida):
    col_grupo, col_alimento, col_cantidad, col_btn = st.columns([1.2, 1.5, 1.0, 0.3])
    
    with col_grupo:
        # Selector de Grupo
        nuevo_grupo = st.selectbox(
            "Grupo", 
            list(ALIMENTOS_POR_GRUPO.keys()), 
            index=list(ALIMENTOS_POR_GRUPO.keys()).index(item["grupo"]),
            key=f"{comida_seleccionada}_grp_{i}"
        )
        # Si el usuario cambia el grupo en pantalla, reajustamos el alimento por defecto del nuevo grupo
        if nuevo_grupo != item["grupo"]:
            item["grupo"] = nuevo_grupo
            item["alimento"] = list(ALIMENTOS_POR_GRUPO[nuevo_grupo].keys())[0]
            st.rerun()

    with col_alimento:
        # Selector de Alimento (filtrado por el grupo actual)
        lista_alimentos = list(ALIMENTOS_POR_GRUPO[item["grupo"]].keys())
        # Resguardo por si el índice quedó desajustado temporalmente
        idx_alimento = lista_alimentos.index(item["alimento"]) if item["alimento"] in lista_alimentos else 0
        
        item["alimento"] = st.selectbox(
            "Alimento",
            lista_alimentos,
            index=idx_alimento,
            key=f"{comida_seleccionada}_ali_{i}"
        )
        
    with col_cantidad:
        # Buscar la porción de texto fija del PDF
        unidad_texto = ALIMENTOS_POR_GRUPO[item["grupo"]][item["alimento"]][1]
        item["cantidad"] = st.number_input(
            f"N° Porciones ({unidad_texto})",
            min_value=0.0,
            max_value=100.0,
            value=float(item["cantidad"]),
            step=0.5,
            key=f"{comida_seleccionada}_cant_{i}"
        )
        
    with col_btn:
        st.write("") # Espaciador para alinear el botón con los inputs
        if st.button("❌", key=f"{comida_seleccionada}_del_{i}"):
            filas_a_eliminar.append(i)
            
    # Calcular carbohidratos sumando: (cantidad de porciones introducidas * carbohidratos de la porción base)
    cho_base = ALIMENTOS_POR_GRUPO[item["grupo"]][item["alimento"]][0]
    cho_comida_actual += item["cantidad"] * cho_base

# Eliminar ítems si se presionó la cruz
if filas_a_eliminar:
    for index in reversed(filas_a_eliminar):
        st.session_state[f"items_{comida_seleccionada}"].pop(index)
    st.rerun()

# Botón para añadir un nuevo alimento a la tabla del momento actual
if st.button("➕ Añadir Alimento", key=f"{comida_seleccionada}_add"):
    p_grupo = list(ALIMENTOS_POR_GRUPO.keys())[0]
    p_alimento = list(ALIMENTOS_POR_GRUPO[p_grupo].keys())[0]
    st.session_state[f"items_{comida_seleccionada}"].append({"grupo": p_grupo, "alimento": p_alimento, "cantidad": 0.0})
    st.rerun()

st.markdown("---")

# --- PROCESAMIENTO MATEMÁTICO ---
if glicemia_input < 70:
    st.error("🚨 **ALERTA DE HIPOGLICEMIA**")
    st.warning("🥤 **Toma ya:** 1 vaso de agua con 3 cucharadas de azúcar.") 
else:
    fila_idx = None
    for idx, (inf, sup) in enumerate(RANGOS_GLICEMIA):
        if inf <= glicemia_input <= sup:
            fila_idx = idx
            break
            
    if glicemia_input > 525: 
        fila_idx = len(RANGOS_GLICEMIA) - 1
    
    # Redondear de forma estricta al bloque de carbohidratos de 10 en 10 más cercano en la matriz
    cho_redondeado = min(CHO_COLUMNAS, key=lambda x: abs(x - cho_comida_actual))
    col_idx = CHO_COLUMNAS.index(cho_redondeado)
    
    if fila_idx is not None:
        dosis_sugerida = MATRIZ_DOSIS[fila_idx][col_idx]
        dosis_final = max(0, dosis_sugerida) # Si el ajuste es -1, la dosis final es 0 UI
        
        st.metric(label="DOSIS DE INSULINA SUGERIDA", value=f"{dosis_final} UI")
        st.markdown(
            f"<p style='text-align: center;'>Carbohidratos totales para {comida_seleccionada}: <b>{round(cho_comida_actual, 1)}g</b><br>"
            f"<span style='color: #64748b; font-size: 0.9rem;'>Evaluado en la columna de {cho_redondeado}g de la matriz</span></p>", 
            unsafe_allow_html=True
        )