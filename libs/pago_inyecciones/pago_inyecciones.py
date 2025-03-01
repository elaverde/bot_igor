import calendar
import locale

# Establecer el idioma en español para nombres de mes
# locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

class PagoInyecciones:
    def __init__(self, mes, anio):
        self.mes = mes
        self.anio = anio

    def contar_martes_viernes(self):
        """Cuenta cuántos martes y viernes hay en el mes dado."""
        mes_numero = self.convertir_mes_a_numero(self.mes)
        total_martes = total_viernes = 0

        for dia in range(1, calendar.monthrange(self.anio, mes_numero)[1] + 1):
            dia_semana = calendar.weekday(self.anio, mes_numero, dia)
            if dia_semana == 1:  # Martes
                total_martes += 1
            elif dia_semana == 4:  # Viernes
                total_viernes += 1

        return total_martes, total_viernes

    def calcular_pago(self):
        """Calcula el pago total multiplicando los días por 20,000."""
        martes, viernes = self.contar_martes_viernes()
        total_pagos = (martes + viernes) * 20000
        return f"${total_pagos:,.2f}".replace(",", ".")

    def convertir_mes_a_numero(self, mes):
        """Convierte nombres de mes a número (ej: 'Marzo' → 3, '03' → 3)."""
        meses = {
            "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
            "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
            "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
        }
        mes = mes.lower().strip()

        if mes.isdigit():  # Si es un número
            return int(mes)
        elif mes in meses:
            return meses[mes]
        else:
            raise ValueError(f"Mes no válido: {mes}")
