# Importamos la librería streamlit, que nos permite crear la página web interactiva
import streamlit as st

# Configuramos la pestaña del navegador: título, ícono y que el contenido quede centrado
st.set_page_config(page_title="Simulador Financiero", page_icon="🏦", layout="centered")

# Mostramos el título principal de la página
st.title("🏦 Simulador Financiero de Préstamos")

# Mostramos un texto secundario en cursiva debajo del título
st.markdown("*Universidad de Cundinamarca — Análisis de Riesgo Crediticio*")

# Dibujamos una línea horizontal para separar secciones visualmente
st.divider()


# ─── SECCIÓN 1: DATOS PERSONALES ───
# Mostramos el subtítulo de esta sección
st.subheader("📋 Datos Personales")

# Dividimos la pantalla en dos columnas para que los campos queden lado a lado
col1, col2 = st.columns(2)

# En la columna izquierda ponemos dos campos de texto
with col1:
    nombre = st.text_input("Nombre completo")                      # El usuario escribe su nombre aquí
    identificacion = st.text_input("Número de identificación")     # Campo para la cédula

# En la columna derecha ponemos otros dos campos
with col2:
    edad = st.number_input("Edad", min_value=0, max_value=120, value=25)  # Solo acepta números entre 0 y 120
    residencia = st.text_input("Lugar de residencia")              # Ciudad o municipio del cliente

st.divider()  # Línea separadora


# ─── SECCIÓN 2: DATOS LABORALES ───
st.subheader("💼 Datos Laborales")

col1, col2 = st.columns(2)  # Volvemos a dividir en dos columnas

with col1:
    profesion = st.text_input("Profesión")                         # Ej: Ingeniero, Contador
    empresa = st.text_input("Empresa / Actividad económica")       # Dónde trabaja el cliente

with col2:
    ocupacion = st.text_input("Ocupación actual")
    sueldo = st.number_input("Sueldo mensual ($)", min_value=0.0, step=100000.0, format="%.0f")  # Salario base del cargo                  # Cargo que desempeña
    # Lista desplegable para elegir el tipo de contrato
    # Cada opción ya incluye el porcentaje máximo de endeudamiento permitido
    tipo_contrato = st.selectbox("Tipo de contrato", [
        "Indefinido (35%)",
        "Fijo (30%)",
        "Independiente / Prestación de servicios (25%)"
    ])

st.divider()


# ─── SECCIÓN 3: DATOS FINANCIEROS ───
st.subheader("💰 Datos Financieros")

col1, col2 = st.columns(2)

with col1:
    # format="%.0f" hace que el número se muestre sin decimales (ej: 2000000 en vez de 2000000.00)
    ingresos = st.number_input("Ingresos mensuales ($)", min_value=0.0, step=100000.0, format="%.0f")
    gastos_basicos = st.number_input("Gastos básicos mensuales ($)", min_value=0.0, step=50000.0, format="%.0f")
    otros_gastos = st.number_input("Otros gastos mensuales ($)", min_value=0.0, step=50000.0, format="%.0f")
    total_gastos_visible = gastos_basicos + otros_gastos  # Se calcula en tiempo real
    st.info(f"📊 Total de gastos mensuales: **${total_gastos_visible:,.0f}**")  # Se muestra al usuario mientras llena el form
with col2:
    valor_prestamo = st.number_input("Valor del préstamo solicitado ($)", min_value=0.0, step=500000.0, format="%.0f")
    plazo = st.number_input("Plazo (meses)", min_value=1, max_value=360, value=12)  # Cuántos meses para pagar
    tasa_interes = st.number_input(
        "Tasa de interés (ej: 0.15 = 15%)",
        min_value=0.0, max_value=1.0,
        value=0.15, step=0.01, format="%.2f"   # Se muestra con 2 decimales
    )

st.divider()

with st.expander("🧪 Ver casos de prueba sugeridos"):
    st.markdown("""
| | Caso A — Viable | Caso B — Ajuste | Caso C — No viable |
|---|---|---|---|
| Ingresos | $4.000.000 | $3.000.000 | $1.500.000 |
| Gastos básicos | $800.000 | $900.000 | $1.200.000 |
| Otros gastos | $400.000 | $500.000 | $400.000 |
| Préstamo | $5.000.000 | $8.000.000 | $6.000.000 |
| Plazo | 24 meses | 24 meses | 12 meses |
| Tasa | 15% | 15% | 15% |
| Contrato | Indefinido | Fijo | Independiente |
| **Resultado esperado** | **Aprobado** | **Aprobado parcialmente** | **No aprobado** |
""")
    
# ─── BOTÓN PRINCIPAL ───
# Cuando el usuario haga clic en este botón, se ejecuta todo el análisis
if st.button("📊 Analizar solicitud", use_container_width=True, type="primary"):

    # ── VALIDACIONES ──
    # Antes de calcular, verificamos que los datos ingresados tengan sentido
    errores = []  # Lista vacía donde guardaremos los errores que encontremos

    if not nombre:          # Si el nombre está vacío
        errores.append("El nombre es obligatorio.")
    if edad < 18:           # Menores de edad no pueden solicitar préstamos
        errores.append("El cliente debe ser mayor de 18 años.")
    if ingresos <= 0:       # No se puede analizar sin ingresos
        errores.append("Los ingresos deben ser mayores a cero.")
    if valor_prestamo <= 0: # El préstamo debe tener un valor
        errores.append("El valor del préstamo debe ser mayor a cero.")

    # Si encontramos algún error, lo mostramos en pantalla y no seguimos
    if errores:
        for e in errores:
            st.error(e)  # Muestra cada error en un cuadro rojo

    else:
        # ── CÁLCULOS FINANCIEROS ──
        # Solo llegamos aquí si todos los datos son válidos

        # Sumamos todos los gastos del cliente
        total_gastos = gastos_basicos + otros_gastos

        # Calculamos cuánto dinero le queda al cliente después de pagar sus gastos
        ingreso_disponible = ingresos - total_gastos

        # Según el tipo de contrato, el banco permite endeudarse hasta cierto porcentaje del ingreso
        if "Indefinido" in tipo_contrato:
            porcentaje = 0.35       # Contrato indefinido = más estabilidad = más confianza del banco
            tipo_label = "Indefinido"
        elif "Fijo" in tipo_contrato:
            porcentaje = 0.30       # Contrato fijo = estabilidad media
            tipo_label = "Fijo"
        else:
            porcentaje = 0.25       # Independiente = más riesgo = menos porcentaje permitido
            tipo_label = "Independiente / PS"

        # Cuánto puede pagar como máximo al mes sin superar el límite del banco
        capacidad_maxima = ingresos * porcentaje

        # Cuánto dinero extra pagará el cliente por los intereses
        interes_total = valor_prestamo * tasa_interes

        # Suma del préstamo más los intereses = lo que realmente pagará en total
        total_a_pagar = valor_prestamo + interes_total

        # Dividimos el total entre los meses para saber cuánto paga cada mes
        cuota_mensual = total_a_pagar / plazo

        # Si el cliente no puede pagar el monto solicitado, calculamos cuánto sí podría pagar
        monto_maximo = (capacidad_maxima * plazo) / (1 + tasa_interes)


        # ── LÓGICA DE DECISIÓN ──
        # Comparamos los indicadores para decidir si se aprueba o no el préstamo

        if ingreso_disponible <= 0:
            # Si el cliente ya gasta más de lo que gana, no puede asumir ninguna deuda
            decision = "NO APROBADO"
            razon = "El ingreso disponible es negativo o cero. El cliente no puede cubrir sus gastos básicos."
            color = "red"
            icono = "❌"

        elif cuota_mensual <= capacidad_maxima and ingreso_disponible > 0:
            # La cuota cabe dentro del límite permitido y le queda dinero disponible
            decision = "APROBADO"
            razon = "La cuota mensual está dentro de la capacidad de endeudamiento y el ingreso disponible es positivo."
            color = "green"
            icono = "✅"

        else:
            # Tiene capacidad de pago, pero no alcanza para el monto completo solicitado
            decision = "APROBADO PARCIALMENTE"
            razon = "El cliente tiene capacidad de pago, pero la cuota supera el límite permitido. Se sugiere un monto menor."
            color = "orange"
            icono = "⚠️"

        # ── NIVEL DE RIESGO ──
        # Calculamos qué porcentaje del ingreso se va en gastos
        relacion_gastos = total_gastos / ingresos if ingresos > 0 else 1

        if relacion_gastos < 0.4:
            nivel_riesgo = "🟢 BAJO"    # Menos del 40% del ingreso en gastos = poco riesgo
        elif relacion_gastos < 0.7:
            nivel_riesgo = "🟡 MEDIO"   # Entre 40% y 70% = riesgo moderado
        else:
            nivel_riesgo = "🔴 ALTO"    # Más del 70% en gastos = riesgo elevado


        # ── MOSTRAR INDICADORES EN PANTALLA ──
        st.subheader("📈 Indicadores Financieros")

        # Primera fila de métricas
        c1, c2, c3 = st.columns(3)
        c1.metric("Total gastos mensuales", f"${total_gastos:,.0f}")        # :,.0f = formato con comas y sin decimales
        c2.metric("Ingreso disponible", f"${ingreso_disponible:,.0f}")
        c3.metric("Capacidad máx. de pago", f"${capacidad_maxima:,.0f}")

        # Segunda fila de métricas
        c4, c5, c6 = st.columns(3)
        c4.metric("Interés total", f"${interes_total:,.0f}")
        c5.metric("Total a pagar", f"${total_a_pagar:,.0f}")
        c6.metric("Cuota mensual estimada", f"${cuota_mensual:,.0f}")

        st.divider()

        # ── MOSTRAR RESULTADO FINAL ──
        st.subheader("🏁 Resultado de la Solicitud")

        # Mostramos el resultado con el color correspondiente
        if color == "green":
            st.success(f"{icono} **{decision}**")   # Cuadro verde
        elif color == "orange":
            st.warning(f"{icono} **{decision}**")   # Cuadro amarillo
        else:
            st.error(f"{icono} **{decision}**")     # Cuadro rojo

        # Explicamos por qué se tomó esa decisión
        st.markdown(f"**Justificación:** {razon}")
        st.markdown(f"**Nivel de riesgo:** {nivel_riesgo}")
        st.markdown(f"**Tipo de contrato:** {tipo_label} — porcentaje permitido: {int(porcentaje*100)}%")

        # Si fue aprobado parcialmente, mostramos el monto alternativo sugerido
        if decision == "APROBADO PARCIALMENTE":
            st.info(f"💡 **Monto máximo recomendable:** ${monto_maximo:,.0f}  \n"
                    f"Este es el máximo que el cliente podría asumir sin superar su capacidad de pago.")

        # Advertencia especial para clientes mayores de 70 años
        if edad > 70:
            st.warning("⚠️ El cliente tiene más de 70 años. Este caso requiere revisión especial.")

        st.divider()

        # ── RESUMEN DEL CLIENTE ──
        # Bloque que se puede expandir o colapsar con un clic
        with st.expander("👤 Ver resumen del perfil del cliente"):
            # Mostramos todos los datos en formato de tabla
            st.markdown(f"""
| Campo | Valor |
|---|---|
| Nombre | {nombre} |
| Identificación | {identificacion} |
| Edad | {int(edad)} años |
| Residencia | {residencia} |
| Profesión | {profesion} |
| Empresa | {empresa} |
| Tipo de contrato | {tipo_label} |
| Ingresos mensuales | ${ingresos:,.0f} |
| Gastos totales | ${total_gastos:,.0f} |
| Préstamo solicitado | ${valor_prestamo:,.0f} |
| Plazo | {int(plazo)} meses |
| Tasa de interés | {tasa_interes*100:.0f}% |
""")
