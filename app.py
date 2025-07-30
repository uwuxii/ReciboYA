import streamlit as st
from jinja2 import Template
from io import BytesIO
from xhtml2pdf import pisa
from pathlib import Path
import datetime

st.title("🧾 Generador de Recibo Simple")

# Campos del formulario de recibo
recibi_de   = st.text_input("Recibí de", placeholder="Nombre de la persona")
cantidad_de = st.text_input("La cantidad de", placeholder="Monto en números")
concepto    = st.text_area("Por concepto de", placeholder="Descripción del concepto", height=100)
fecha       = st.date_input("Fecha", value=datetime.date.today())

# Cargar y renderizar plantilla
tpl = Template(Path("templates/receipt.html").read_text())
html_out = tpl.render(
    recibí_de   = recibi_de.strip()   or "—",
    cantidad_de = cantidad_de.strip() or "—",
    concepto    = concepto.replace("\n", "<br>") or "—",
    fecha       = fecha.strftime("%d/%m/%Y"),
)

# Convertir HTML a PDF con xhtml2pdf (pisa)
pdf_buffer = BytesIO()
pisa_status = pisa.CreatePDF(src=html_out, dest=pdf_buffer)
pdf_buffer.seek(0)

if pisa_status.err:
    st.error("❌ Ocurrió un error generando el PDF.")
else:
    st.download_button(
        label="⬇️ Generar y descargar PDF",
        data=pdf_buffer,
        file_name=f"recibo_{fecha.strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
