# ========================================
# FUNCIONES DE CÁLCULO
# ========================================
import math

def area_cilindro(diametro_mm):

    """
    Calcula el área de la sección transversal del cilindro.
    
    Parámetros:
    - diametro_mm: Diámetro del cilindro en mm
    """
    radio_mm = diametro_mm / 2
    area_mm2 = math.pi * (radio_mm ** 2)
    return area_mm2


def volumen_cilindro(diametro_mm, altura_mm):
    """
    Calcula el volumen del cilindro.
    
    Parámetros:
    - diametro_mm: Diámetro del cilindro en mm
    - altura_mm: Altura del cilindro en mm
    """
    radio_mm = diametro_mm / 2
    volumen_mm3 = math.pi * (radio_mm ** 2) * altura_mm
    volumen_m3 = volumen_mm3 / (1e9)
    return volumen_m3 

def densidad_cilindro(volumen_m3, peso_kg):
    """
    Calcula la densidad del cilindro.
    
    Parámetros:
    - volumen_m3: Volumen del cilindro en m³
    - peso_kg: Peso del cilindro en kg
    - densidad en kg/m³ al 10 kg/m³ más cercano
    """

    if volumen_m3 > 0 and peso_kg > 0:
        densidad = round(peso_kg / volumen_m3, 2)
        return round(densidad / 10) * 10

def resistencia_compresion(carga_kn, diametro_mm):
    """
    Calcula la resistencia a la compresión del concreto.
    
    Parámetros:
    - carga_kn: Carga aplicada en kN
    - diametro_mm: Diámetro del cilindro en mm
   """
    radio_mm = diametro_mm / 2
    area_mm2 = math.pi * (radio_mm ** 2)
    carga_n = carga_kn * 1000
    resistencia_mpa = (carga_n / area_mm2)
    return  round(resistencia_mpa, 2)


def evolucion_resistencia(fc, resistencia):
    """
    Evalua % de evolucion entre la resistencia del ensayo y la requerida por diseño.
    """
    if fc > 0:
        return round((resistencia / fc) * 100, 2)
    else:
        return  0.0