from io import BytesIO
from datetime import datetime
from typing import Optional, Dict, Any

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def _dibujar_pie_pagina(canvas, doc):
	canvas.saveState()
	canvas.setFont("Helvetica", 8)
	canvas.setFillColor(colors.grey)
	canvas.drawString(
		doc.leftMargin,
		12,
		"Estos resultados de ensayado son creados gratuitamente por el software ConcreLab Free; los resultados expresados no tienen relación alguna con la empresa.",
	)
	canvas.restoreState()


def compresion_cilindros_pdf(
    df_resultados: pd.DataFrame,
    encabezado: Optional[Dict[str, Any]] = None
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=24,
        rightMargin=24,
        topMargin=24,
        bottomMargin=24,
    )
    estilos = getSampleStyleSheet()
    elementos = []

    datos_hdr = {
        "ciudad": "Bogotá D.C.",
        "fecha_generacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "obra": "Proyecto Torre Norte - Etapa I",
        "desarrollado_por": "Equipo Técnico Lab Concreto",
    }
    if encabezado:
        datos_hdr.update({
            "ciudad": encabezado.get("ciudad", datos_hdr["ciudad"]),
            "fecha_generacion": encabezado.get("fecha_generacion", datos_hdr["fecha_generacion"]),
            "obra": encabezado.get("obra", datos_hdr["obra"]),
            "desarrollado_por": encabezado.get("desarrollado_por", datos_hdr["desarrollado_por"]),
        })

    tabla_encabezado = Table(
        [
            ["Ciudad:", str(datos_hdr["ciudad"])],
            ["Fecha de generación:", str(datos_hdr["fecha_generacion"])],
            ["Obra:", str(datos_hdr["obra"])],
            ["Desarrollado por:", str(datos_hdr["desarrollado_por"])],
        ],
        colWidths=[140, 360],
        hAlign="LEFT",  # <- alinea la tabla a la izquierda
    )
    tabla_encabezado.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(1, 12))
    elementos.append(Paragraph("<b>Ensayo de compresión de cilindros (NTC 673)</b>", estilos["Title"]))

    #centra el texto normal debajo del título
    
    estilo_texto_centrado = ParagraphStyle(
        "TextoCentrado",
        parent=estilos["Normal"],
        alignment=1,  # CENTER
    )

    elementos.append(Spacer(1, 12))

    columnas = [
        "Muestra",
        "Fecha",
        "Edad(d)",
        "Diámetro(mm)",
        "Altura(mm)",
        "Densidad(kg/m3)",
        "Carga Máxima(kN)",
        "Resistencia(MPa)",
        "Evolución(%)",
        "Tipo Falla",
    ]

    tabla_datos = [columnas]
    for _, fila in df_resultados.iterrows():
        tabla_datos.append([
            str(fila["Muestra"]),
            str(fila["Fecha"]),
            str(fila["Edad(d)"]),
            f"{fila['Diámetro(mm)']:.1f}",
            f"{fila['Altura(mm)']:.1f}",
            f"{fila['Densidad(kg/m3)']:.2f}",
            f"{fila['Carga Máxima(kN)']:.2f}",
            f"{fila['Resistencia(MPa)']:.2f}",
            f"{fila['Evolución(%)']:.2f}",
            str(fila["Tipo Falla"]),
        ])

    tabla = Table(
        tabla_datos,
        repeatRows=1,
        colWidths=[65, 55, 45, 68, 60, 78, 78, 72, 58, 60],
    )
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    elementos.append(tabla)
    doc.build(elementos, onFirstPage=_dibujar_pie_pagina, onLaterPages=_dibujar_pie_pagina)
    buffer.seek(0)
    return buffer.getvalue()


def generarar_pdf(
    df_resultados: pd.DataFrame,
    encabezado: Optional[Dict[str, Any]] = None
) -> bytes:
    return compresion_cilindros_pdf(df_resultados, encabezado)
