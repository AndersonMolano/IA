import re
import pandas as pd

# Función para consultar la novedad de un cotizante
def consultar_novedad(df_cotizantes, tipo_cotizante_numero, novedad):
        if novedad not in df_cotizantes:
            return f"Novedad '{novedad}' no encontrada en el archivo."

        # Buscar la fila correspondiente al tipo de cotizante por su número
        tipo_cotizante_row = df_cotizantes[df_cotizantes['No'] == tipo_cotizante_numero]
        # Verificar que se haya encontrado el tipo de cotizante
        if tipo_cotizante_row.empty:
            return f"Tipo de cotizante con número '{tipo_cotizante_numero}' no encontrado."

        # Verificar el valor en la columna específica
        aporte = tipo_cotizante_row[novedad].values[0]
        novedad_permitida,novedad_no_permitida = novedades_validas(df_cotizantes, tipo_cotizante_numero, novedad)
        novedad_permitida_str = ", ".join(map(str, novedad_permitida))
        if aporte == 'X':
             return f"Para el tipo de cotizante {tipo_cotizante_numero} es permitida la novedad {novedad}."
        else:
              return f"No es permitido el tipo de novedad {novedad} para el tipo de cotizante {tipo_cotizante_numero}. Sin embargo, es posible marcar la novedad utilizando los siguientes tipos: {novedad_permitida_str}."

def novedades_validas(df_cotizantes, tipo_cotizante_numero, planilla):
    # Define los subtipos válidos a verificar
    valid_novelties = ['ING', 'RET', 'SLN X', 'SLN C', 'IGE', 'LMA', 'VAC', 'TAE', 'VSP', 'VST', 'IRL', 'AVP', 'VCT', 'TDE', 'TAP', 'TDP']
    novedad_permitida = []
    novedad_no_permitida = []

    for i in valid_novelties:  # 'i' representa cada subtipo en la lista validas

            tipo_cotizante_row = df_cotizantes[df_cotizantes['No'] == tipo_cotizante_numero]
        
        # Verificar el valor en la columna correspondiente al subtipo
            aporte = tipo_cotizante_row[i].values[0]
        
        # Si el aporte es 'X', es permitido liquidar con ese subtipo
            if aporte == 'X':
                novedad_permitida.append(i) 
            else:
                novedad_no_permitida.append(i) 

    return novedad_permitida, novedad_no_permitida


def main(question, predicted_label):
    user_input = question
    tipo_pregunta = predicted_label
    try:
        # Lógica para la pregunta de tipo "novedad"
        if tipo_pregunta == "novedad":

            cotizantes_excel_file = 'data/train_data.xlsx'
            # Leer la hoja 'Novedades' del archivo Excel
            df_cotizantes = pd.read_excel(cotizantes_excel_file, sheet_name='Novedades')
            
            # Validar que la pregunta tenga el formato correcto
            if 'la novedad' not in user_input:
                return "Pregunta no válida. Asegúrese de que la pregunta tenga el formato: 'El tipo de cotizante X puede tener la novedad COLUMN?'"
            
            # Buscar el número del cotizante (después de "cotizante")
            words = user_input.split()
            tipo_cotizante_numero = None
            for i, word in enumerate(words):
                if word == 'cotizante' and i + 1 < len(words):
                    try:
                        tipo_cotizante_numero = int(words[i + 1])  # El número del cotizante es el siguiente a "cotizante"
                    except ValueError:
                        return "No se pudo extraer el número de cotizante."

            if tipo_cotizante_numero is None:
                return "No se pudo identificar el número de cotizante. Asegúrese de que la pregunta siga el formato esperado."
            print (tipo_cotizante_numero)
            # Extraer la novedad (después de "novedad")
            novedad = words[-1].upper()  # Convertir a mayúsculas para hacer coincidir las novedades en el sistema
            print (novedad)
            # Validar que la novedad sea válida
            valid_novelties = ['ING', 'RET', 'SLN X', 'SLN C', 'IGE', 'LMA', 'VAC', 'TAE', 'VSP', 'VST', 'IRL', 'AVP', 'VCT', 'TDE', 'TAP', 'TDP']
            if novedad not in valid_novelties:
                return f"Novedad '{novedad}' no válida. Las novedades válidas son: {', '.join(valid_novelties)}."

            # Aquí deberías implementar la lógica de consulta de la novedad
            return consultar_novedad(df_cotizantes, tipo_cotizante_numero, novedad)
        else:
            return "Tipo de pregunta no reconocido. Asegúrese de que la pregunta sea de tipo 'relacion','novedad' o 'planilla'."
    except Exception as e:
        return f"Error al procesar la pregunta. Asegúrese de seguir el formato correcto. {str(e)}"

