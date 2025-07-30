import streamlit as st
from jinja2 import Template
from weasyprint import HTML
from io import BytesIO
from pathlib import Path
import datetime

st.title("🧾 Generador de Recibo Simple")

# Campos del formulario de recibo
recibi_de   = st.text_input("Recibí de", placeholder="Nombre de la persona")
cantidad_de = st.text_input("La cantidad de", placeholder="Monto en números")
concepto    = st.text_area("Por concepto de", placeholder="Descripción del concepto", height=100)
fecha       = st.date_input("Fecha", value=datetime.date.today())

# Cargar plantilla HTML y renderizar con los datos
tpl = Template(Path("templates/receipt.html").read_text())
html_out = tpl.render(
    recibí_de   = recibi_de.strip()   or "—",
    cantidad_de = cantidad_de.strip() or "—",
    concepto    = concepto.replace("\n", "<br>") or "—",
    fecha       = fecha.strftime("%d/%m/%Y"),
)

# Generar PDF a partir del HTML
pdf_bytes = HTML(string=html_out).write_pdf()

# Botón de descarga del PDF
st.download_button(
    label="⬇️ Generar y descargar PDF",
    data=BytesIO(pdf_bytes),
    file_name=f"recibo_{fecha.strftime('%Y%m%d')}.pdf",
    mime="application/pdf"
)