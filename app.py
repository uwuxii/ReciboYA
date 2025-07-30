import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from jinja2 import Template
from pathlib import Path
import datetime

st.title("🧾 Generador de Recibo con ReportLab")

# Form inputs
recibi_de   = st.text_input("Recibí de", placeholder="Nombre de la persona")
cantidad_de = st.text_input("La cantidad de", placeholder="Monto en números")
concepto    = st.text_area("Por concepto de", placeholder="Descripción del concepto", height=100)
fecha       = st.date_input("Fecha", value=datetime.date.today())

# Render Jinja2 just to inject values into an HTML-ish template (optional)
tpl = Template(Path("templates/receipt.html").read_text())
html_out = tpl.render(
    recibí_de   = recibi_de.strip()   or "—",
    cantidad_de = cantidad_de.strip() or "—",
    concepto    = concepto.replace("\n", " "),
    fecha       = fecha.strftime("%d/%m/%Y"),
)

# Generate PDF
buffer = BytesIO()
c = canvas.Canvas(buffer, pagesize=LETTER)
width, height = LETTER

# Simple layout: you can customize fonts, positions, etc.
c.setFont("Helvetica-Bold", 16)
c.drawString(72, height - 72, "Resumen de Recibo")

c.setFont("Helvetica", 12)
c.drawString(72, height - 108, f"Recibí de: {recibi_de or '—'}")
c.drawString(72, height - 128, f"La cantidad de: {cantidad_de or '—'}")
c.drawString(72, height - 148, f"Fecha: {fecha.strftime('%d/%m/%Y')}")

# Multi-line concepto
text = c.beginText(72, height - 188)
for line in concepto.split("\n"):
    text.textLine(line)
c.drawText(text)

c.showPage()
c.save()
buffer.seek(0)

# Download button
st.download_button(
    "⬇️ Generar y descargar PDF",
    data=buffer,
    file_name=f"recibo_{fecha.strftime('%Y%m%d')}.pdf",
    mime="application/pdf"
)
