from io import BytesIO
from datetime import datetime
from typing import Any, Dict, Optional

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def _dibujar_pie_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(
        doc.leftMargin,
        12,
        "Estos resultados de ensayado son creados gratuitamente por el software Laboratorio Concreto Test; los resultados expresados no tienen relación alguna con la empresa.",
    )
    canvas.restoreState()


def granulometria_pdf(
    muestra: str,
    tipo_agregado: str,
    df_resultados: pd.DataFrame,
    fig,
    encabezado: Optional[Dict[str, Any]] = None,
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
        datos_hdr.update(
            {
                "ciudad": encabezado.get("ciudad", datos_hdr["ciudad"]),
                "fecha_generacion": encabezado.get("fecha_generacion", datos_hdr["fecha_generacion"]),
                "obra": encabezado.get("obra", datos_hdr["obra"]),
                "desarrollado_por": encabezado.get("desarrollado_por", datos_hdr["desarrollado_por"]),
            }
        )

    tabla_encabezado = Table(
        [
            ["Ciudad:", str(datos_hdr["ciudad"])],
            ["Fecha de generación:", str(datos_hdr["fecha_generacion"])],
            ["Obra:", str(datos_hdr["obra"])],
            ["Desarrollado por:", str(datos_hdr["desarrollado_por"])],
        ],
        colWidths=[140, 360],
        hAlign="LEFT",
    )
    tabla_encabezado.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(1, 12))
    elementos.extend(
        [
            Paragraph("<b>Análisis Granulométrico (NTC 174)</b>", estilos["Title"]),
            Spacer(1, 6),
            Paragraph(f"<b>Muestra:</b> {muestra or 'Muestra de ensayo'}", estilos["Normal"]),
            Paragraph(f"<b>Tipo de agregado:</b> {tipo_agregado}", estilos["Normal"]),
            Spacer(1, 10),
        ]
    )

    columnas = ["Tamiz (mm)", "% Retenido", "% Retenido Acumulado", "% Pasante"]
    tabla_datos = [columnas]

    for _, fila in df_resultados.iterrows():
        tabla_datos.append(
            [
                str(fila["Tamiz (mm)"]),
                f"{float(fila['% Retenido']):.2f}",
                f"{float(fila['% Retenido Acumulado']):.2f}",
                f"{float(fila['% Pasante']):.2f}",
            ]
        )

    tabla = Table(tabla_datos, repeatRows=1, colWidths=[110, 140, 170, 120])
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    elementos.append(tabla)
    elementos.append(Spacer(1, 12))

    imagen_buffer = BytesIO()
    fig.savefig(imagen_buffer, format="png", dpi=180, bbox_inches="tight")
    imagen_buffer.seek(0)
    elementos.append(Image(imagen_buffer, width=700, height=320))

    doc.build(elementos, onFirstPage=_dibujar_pie_pagina, onLaterPages=_dibujar_pie_pagina)
    buffer.seek(0)
    return buffer.getvalue()
