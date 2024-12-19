import re
import pandas as pd
# Función para consultar la novedad de un cotizante
def consultar_planilla(df_planilla, tipo_cotizante_numero, planilla):
        #print(df_planilla)
        if planilla not in df_planilla:
            return f"planilla '{planilla}' no encontrada en el archivo."

        # Buscar la fila correspondiente al tipo de cotizante por su número
        tipo_cotizante_row = df_planilla[df_planilla['No'] == tipo_cotizante_numero]
        # Verificar que se haya encontrado el tipo de cotizante
        if tipo_cotizante_row.empty:
            return f"Tipo de cotizante con número '{tipo_cotizante_numero}' no encontrado."

        # Verificar el valor en la columna específica
        aporte = tipo_cotizante_row[planilla].values[0]

        planilla_permitida,planilla_no_permitida = planillas_validas(df_planilla, tipo_cotizante_numero, planilla)
        planilla_permitida_str = ", ".join(map(str, planilla_permitida))
        if aporte == 'X':
             return f"Para el tipo de cotizante {tipo_cotizante_numero} es permitido liquidar con el tipo de planilla {planilla}."
        else:
             return f"No se permite realizar la liquidación con la planilla tipo {planilla} para el tipo de cotizante {tipo_cotizante_numero}. Sin embargo, es posible efectuar la liquidación utilizando los siguientes tipos de planilla: {planilla_permitida_str}."

# Función para verificar si el tipo de cotizante tiene permisos para otros subtipos
def planillas_validas(df_planilla, tipo_cotizante_numero, planilla):
    # Define los subtipos válidos a verificar
    validas = ['A','E','F','H','I','J','K','M','N','S','T','U','X','Y','O','Q','B','D']
    planilla_permitida = []
    planilla_no_permitida = []

    for i in validas:  # 'i' representa cada subtipo en la lista validas

            tipo_cotizante_row = df_planilla[df_planilla['No'] == tipo_cotizante_numero]
        
        # Verificar el valor en la columna correspondiente al subtipo
            aporte = tipo_cotizante_row[i].values[0]
        
        # Si el aporte es 'X', es permitido liquidar con ese subtipo
            if aporte == 'X':
                planilla_permitida.append(i) 
            else:
                planilla_no_permitida.append(i) 

    return planilla_permitida, planilla_no_permitida

def main(question, predicted_label):
    user_input = question
    tipo_pregunta = predicted_label
    try:
        # Limpiar la entrada de la pregunta (eliminar caracteres especiales y convertir a minúsculas)
        user_input = user_input.strip().lower()
        user_input = re.sub(r'[^\w\s]', '', user_input)  # Eliminar signos de puntuación
        # Lógica para la pregunta de tipo "novedad"
        if tipo_pregunta == "planilla":
            cotizantes_excel_file = 'data/train_data.xlsx'
            # Leer la hoja 'Novedades' del archivo Excel
            df_planilla = pd.read_excel(cotizantes_excel_file, sheet_name='Tipo_planilla')
            if 'planilla' not in user_input:
                return "Pregunta no válida. Asegúrese de que la pregunta tenga el formato: 'El tipo de cotizante X liquida el tipo de planilla COLUMN'"
            
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
            #print (tipo_cotizante_numero)
            # Extraer la novedad (después de "novedad")
            planilla = words[-1].upper()  # Convertir a mayúsculas para hacer coincidir las novedades en el sistema
            #print (planilla)
            # Validar que la novedad sea válida
            valid_planillas = ['A','E','F','H','I','J','K','M','N','S','T','U','X','Y','O','Q','B','D']
            if planilla not in valid_planillas:
                return f"Planilla '{planilla}' no válida. Las planillas válidas son: {', '.join(valid_planillas)}."

            # Aquí deberías implementar la lógica de consulta de la novedad
            return consultar_planilla(df_planilla, tipo_cotizante_numero, planilla)
        else:
            return "Tipo de pregunta no reconocido. Asegúrese de que la pregunta sea de tipo 'relacion','novedad' o 'planilla'."
    except Exception as e:
        return f"Error al procesar la pregunta. Asegúrese de seguir el formato correcto. {str(e)}"
        