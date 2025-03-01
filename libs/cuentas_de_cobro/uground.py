import os
import datetime
from docxtpl import DocxTemplate
import subprocess


class Uground():
    def __init__(self, base_dir):
        self.fecha = ""
        self.n_cobro = ""
        self.concepto = ""
        self.base_dir = base_dir

    def leer_parametros(self, fecha="", n_cobro="", concepto=""):
        # si la fecha esta vacia, se asigna la fecha del sistema
        self.fecha = fecha
        self.n_cobro = n_cobro
        self.concepto = concepto
        
        if self.fecha == "":
            hoy = datetime.datetime.now()
            #ponemos el mes en letras
            meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            mes = datetime.datetime.now().month
            nombre_mes = meses[mes - 1]
            self.fecha = "01 "+nombre_mes+" de "+hoy.strftime("%Y")

    def extraer_mes_anio(self,fecha):
        # Si la fecha es del sistema (Ej: "01 Febrero de 2024")
        if " " in fecha:
            partes = fecha.split(" ")  # Divide en ["01", "Febrero", "de", "2024"]
            if len(partes) >= 3:  # Verifica que tenga suficientes partes
                mes = partes[1]  # Extrae "Febrero"
                anio = partes[-1]  # Extrae "2024"
                return mes, anio
        
      

        # Si la fecha es en formato dd-mm-yyyy (Ej: "01-02-2024")
        formatos = ["%d-%m-%Y", "%d/%m/%Y", "%d/%m/%y"]  # Se agregan los formatos válidos
        for fmt in formatos:
            try:
                fecha_dt = datetime.datetime.strptime(fecha, fmt)
                meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                mes = meses[fecha_dt.month - 1]  # Convierte 02 → "Febrero"
                anio = str(fecha_dt.year)  # Convierte el año a string
                return mes, anio
            except ValueError:
                continue  # Si falla, prueba con el siguiente formato

    def convert_to_pdf(self, input_docx):
        # Obtener el directorio donde está el archivo .docx
        docx_dir = os.path.dirname(input_docx)

        # Construir la ruta de salida del PDF en el mismo directorio
        output_pdf = input_docx.replace(".docx", ".pdf")

        # Ejecutar LibreOffice para convertir
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", input_docx, "--outdir", docx_dir])

        return output_pdf
    def generar_cuenta_cobro_uground(self):
        #obtenemos mes en letras
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        #Convertimos self.fecha a mes y ano tener cuenta que la fecha puede ser ingresada dd-mm-yyyy o por sistema
        nombre_mes, ano = self.extraer_mes_anio(self.fecha)
        print(self.base_dir+"/storage/plantillas/PLANTILLA_CUENTA_COBRO_UGROUND.docx")
        doc = DocxTemplate(self.base_dir+"/storage/plantillas/PLANTILLA_CUENTA_COBRO_UGROUND.docx")
        context = {
            'FECHA': self.fecha,
            'N_COBRO':self.n_cobro,
            'CONCEPTO':self.concepto
        }
        print(context)
        doc.render(context)
        doc.save(self.base_dir+'/storage/cuentas_de_cobro/UGROUND-Edilson-Laverde-Molina-'+nombre_mes+'-'+ano+'.docx')
        self.convert_to_pdf(self.base_dir+'/storage/cuentas_de_cobro/UGROUND-Edilson-Laverde-Molina-'+nombre_mes+'-'+ano+'.docx')
        return self.base_dir+'/storage/cuentas_de_cobro/UGROUND-Edilson-Laverde-Molina-'+nombre_mes+'-'+ano+'.pdf'


    