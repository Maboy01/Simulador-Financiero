import streamlit as st

st.set_page_config(page_title="Simulador Financiero", page_icon="🏦", layout="centered")

st.title("🏦 Simulador Financiero de Préstamos")
st.markdown("*Universidad de Cundinamarca — Análisis de Riesgo Crediticio*")
st.divider()

# ─── DATOS PERSONALES ───
st.subheader("📋 Datos Personales")
col1, col2 = st.columns(2)
with col1:
    nombre = st.text_input("Nombre completo")
    identificacion = st.text_input("Número de identificación")
with col2:
    edad = st.number_input("Edad", min_value=0, max_value=120, value=25)
    residencia = st.text_input("Lugar de residencia")

st.divider()

# ─── DATOS LABORALES ───
st.subheader("💼 Datos Laborales")
col1, col2 = st.columns(2)
with col1:
    profesion = st.text_input("Profesión")
    empresa = st.text_input("Empresa / Actividad económica")
with col2:
    ocupacion = st.text_input("Ocupación actual")
    tipo_contrato = st.selectbox("Tipo de contrato", [
        "Indefinido (35%)",
        "Fijo (30%)",
        "Independiente / Prestación de servicios (25%)"
    ])

st.divider()

# ─── DATOS FINANCIEROS ───
st.subheader("💰 Datos Financieros")
col1, col2 = st.columns(2)
with col1:
    ingresos = st.number_input("Ingresos mensuales ($)", min_value=0.0, step=100000.0, format="%.0f")
    gastos_basicos = st.number_input("Gastos básicos mensuales ($)", min_value=0.0, step=50000.0, format="%.0f")
    otros_gastos = st.number_input("Otros gastos mensuales ($)", min_value=0.0, step=50000.0, format="%.0f")
with col2:
    valor_prestamo = st.number_input("Valor del préstamo solicitado ($)", min_value=0.0, step=500000.0)
    plazo = st.number_input("Plazo (meses)", min_value=1, max_value=360, value=12)
    tasa_interes = st.number_input(
        "Tasa de interés (ej: 0.15 = 15%)",
        min_value=0.0, max_value=1.0,
        value=0.15, step=0.01, format="%.2f"
    )

st.divider()

# ─── BOTÓN ANALIZAR ───
if st.button("📊 Analizar solicitud", use_container_width=True, type="primary"):

    errores = []
    if not nombre:
        errores.append("El nombre es obligatorio.")
    if edad < 18:
        errores.append("El cliente debe ser mayor de 18 años.")
    if ingresos <= 0:
        errores.append("Los ingresos deben ser mayores a cero.")
    if valor_prestamo <= 0:
        errores.append("El valor del préstamo debe ser mayor a cero.")

    if errores:
        for e in errores:
            st.error(e)
    else:
        # ─── CÁLCULOS ───
        total_gastos = gastos_basicos + otros_gastos
        ingreso_disponible = ingresos - total_gastos

        if "Indefinido" in tipo_contrato:
            porcentaje = 0.35
            tipo_label = "Indefinido"
        elif "Fijo" in tipo_contrato:
            porcentaje = 0.30
            tipo_label = "Fijo"
        else:
            porcentaje = 0.25
            tipo_label = "Independiente / PS"

        capacidad_maxima = ingresos * porcentaje
        interes_total = valor_prestamo * tasa_interes
        total_a_pagar = valor_prestamo + interes_total
        cuota_mensual = total_a_pagar / plazo
        monto_maximo = (capacidad_maxima * plazo) / (1 + tasa_interes)

        # ─── DECISIÓN ───
        if ingreso_disponible <= 0:
            decision = "NO APROBADO"
            razon = "El ingreso disponible es negativo o cero. El cliente no puede cubrir sus gastos básicos."
            color = "red"
            icono = "❌"
        elif cuota_mensual <= capacidad_maxima and ingreso_disponible > 0:
            decision = "APROBADO"
            razon = "La cuota mensual está dentro de la capacidad de endeudamiento y el ingreso disponible es positivo."
            color = "green"
            icono = "✅"
        else:
            decision = "APROBADO PARCIALMENTE"
            razon = "El cliente tiene capacidad de pago, pero la cuota supera el límite permitido. Se sugiere un monto menor."
            color = "orange"
            icono = "⚠️"

        # Nivel de riesgo
        relacion_gastos = total_gastos / ingresos if ingresos > 0 else 1
        if relacion_gastos < 0.4:
            nivel_riesgo = "🟢 BAJO"
        elif relacion_gastos < 0.7:
            nivel_riesgo = "🟡 MEDIO"
        else:
            nivel_riesgo = "🔴 ALTO"

        # ─── INDICADORES ───
        st.subheader("📈 Indicadores Financieros")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total gastos mensuales", f"${total_gastos:,.0f}")
        c2.metric("Ingreso disponible", f"${ingreso_disponible:,.0f}")
        c3.metric("Capacidad máx. de pago", f"${capacidad_maxima:,.0f}")

        c4, c5, c6 = st.columns(3)
        c4.metric("Interés total", f"${interes_total:,.0f}")
        c5.metric("Total a pagar", f"${total_a_pagar:,.0f}")
        c6.metric("Cuota mensual estimada", f"${cuota_mensual:,.0f}")

        st.divider()

        # ─── RESULTADO ───
        st.subheader("🏁 Resultado de la Solicitud")

        if color == "green":
            st.success(f"{icono} **{decision}**")
        elif color == "orange":
            st.warning(f"{icono} **{decision}**")
        else:
            st.error(f"{icono} **{decision}**")

        st.markdown(f"**Justificación:** {razon}")
        st.markdown(f"**Nivel de riesgo:** {nivel_riesgo}")
        st.markdown(f"**Tipo de contrato:** {tipo_label} — porcentaje permitido: {int(porcentaje*100)}%")

        if decision == "APROBADO PARCIALMENTE":
            st.info(f"💡 **Monto máximo recomendable:** ${monto_maximo:,.0f}  \n"
                    f"Este es el máximo que el cliente podría asumir sin superar su capacidad de pago.")

        if edad > 70:
            st.warning("⚠️ El cliente tiene más de 70 años. Este caso requiere revisión especial.")

        st.divider()

        # ─── PERFIL DEL CLIENTE ───
        with st.expander("👤 Ver resumen del perfil del cliente"):
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
