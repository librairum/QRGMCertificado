import fitz
import re
import qrcode
from datetime import datetime

def leer_pdf(ruta_pdf):
    texto = ""
    with fitz.open(ruta_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

def extraer_datos(texto):
    ruc = re.search(r'RUC\s+(\d{11})', texto)
    dni = re.search(r'DNI\s+N\.°\s*(\d{8})', texto)
    universidad = re.search(r'UNIVERSIDAD\s+[^\n,]+', texto, re.IGNORECASE)
    carrera = re.search(r'carrera\s+de\s+([^\n,]+)', texto, re.IGNORECASE)
    fecha_emi = re.search(r'Lima,\s+(\d{2})\s+de\s+([a-zA-Z]+)\s+del\s+(\d{4})', texto)

    meses ={
        "enero": "01", "febrero": "02", "marzo": "03", "abril": "04", "mayo": "05",
        "junio": "06", "julio": "07", "agosto": "08", "septiembre": "09",
        "octubre": "10", "noviembre": "11", "diciembre": "12"
    }
    if fecha_emi:
        dia = fecha_emi.group(1)
        mes = meses[fecha_emi.group(2).lower()]
        anio = fecha_emi.group(3)
        fecha = f"{dia}/{mes}/{anio}"
    else:
        fecha = "N/A"

    return {
        "ruc": ruc.group(1) if ruc else "N/A",
        "dni": dni.group(1) if dni else "N/A",
        "fecha": fecha,
        "universidad": universidad.group().strip().title() if universidad else "N/A",
        "carrera": carrera.group(1).strip().lower() if carrera else "N/A"
    }

def generar_qr(datos, nombre_archivo='qr_certificado.png'):
    texto_qr = f"|{datos['ruc']}|{datos['dni']}|{datos['fecha']}|{datos['universidad']}|{datos['carrera']}|"
    print("Muestra de la lectura del QR:", texto_qr)

    img = qrcode.make(texto_qr)
    img.save(nombre_archivo)
    print(f"QR guardado como: {nombre_archivo}")

ruta_pdf = "Certificados/certificado de practicas darlyne Ponce.pdf"
texto_extraido = leer_pdf(ruta_pdf)
datos = extraer_datos(texto_extraido)
generar_qr(datos)
