import pandas as pd
import re

# Función para consultar el archivo Excel sobre si un cotizante aporta a una columna
def consultar_aporte(df, tipo_cotizante_numero, columna):
    # Verificar si la columna está en el DataFrame
    if columna not in df.columns:
        return f"Columna '{columna}' no encontrada en el archivo."
    
    # Buscar la fila correspondiente al tipo de cotizante por su número
    tipo_cotizante_row = df[df['No'] == tipo_cotizante_numero]
    
    # Verificar que se haya encontrado el tipo de cotizante
    if tipo_cotizante_row.empty:
        return f"Tipo de cotizante con número '{tipo_cotizante_numero}' no encontrado."
    
    # Verificar el valor en la columna específica
    aporte = tipo_cotizante_row[columna].values[0]
    
    if aporte == 'X':
        return f"El tipo de cotizante con número {tipo_cotizante_numero} SÍ aporta a {columna}."
    elif aporte == 'O':
        return f"El tipo de cotizante con número {tipo_cotizante_numero} APORTA OPCIONALMENTE a {columna}."
    elif aporte == 'C':
        return f"El tipo de cotizante con número {tipo_cotizante_numero} APORTA CONDICIONALMENTE a {columna}."
    else:
        return f"El tipo de cotizante con número {tipo_cotizante_numero} NO aporta a {columna}."

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

        if aporte == 'X':
             return f"Para el tipo de cotizante {tipo_cotizante_numero} es permitida la novedad {novedad}."
        else:
             return f"Para el tipo de cotizante {tipo_cotizante_numero} no es permitida la novedad {novedad}."

# Función para consultar la novedad de un cotizante
def consultar_planilla(df_planilla, tipo_cotizante_numero, planilla):
        if planilla not in df_planilla:
            return f"Novedad '{planilla}' no encontrada en el archivo."

        # Buscar la fila correspondiente al tipo de cotizante por su número
        tipo_cotizante_row = df_planilla[df_planilla['No'] == tipo_cotizante_numero]
        # Verificar que se haya encontrado el tipo de cotizante
        if tipo_cotizante_row.empty:
            return f"Tipo de cotizante con número '{tipo_cotizante_numero}' no encontrado."

        # Verificar el valor en la columna específica
        aporte = tipo_cotizante_row[planilla].values[0]

        if aporte == 'X':
             return f"Para el tipo de cotizante {tipo_cotizante_numero} es permitido liquidar con el tipo de planilla {planilla}."
        else:
             return f"Para el tipo de cotizante {tipo_cotizante_numero} no es permitido liquidar con el tipo de planilla {planilla}."
    
# Función principal que recibe la pregunta
def main(question, predicted_label):
    user_input = question
    tipo_pregunta = predicted_label
    try:
        # Limpiar la entrada de la pregunta (eliminar caracteres especiales y convertir a minúsculas)
        user_input = user_input.strip().lower()
        user_input = re.sub(r'[^\w\s]', '', user_input)  # Eliminar signos de puntuación

        # Lógica para la pregunta de tipo "relacion"
        if tipo_pregunta == "relacion":
            # Cargar el archivo Excel para los cotizantes
            cotizantes_excel_file = 'data/train_data.xlsx'
            # Leer la hoja 'Novedades' del archivo Excel
            df_cotizantes = pd.read_excel(cotizantes_excel_file, sheet_name='Datos')
            if 'aporta a' not in user_input:
                return "Pregunta no válida. Asegúrese de que la pregunta tenga el formato: 'el tipo de cotizante X aporta a COLUMN'."

            # Extraer el número del cotizante (anterior a 'aporta')
            words = user_input.split()
            tipo_cotizante_numero = None
            for i, word in enumerate(words):
                if word == 'aporta' and i > 0:
                    try:
                        tipo_cotizante_numero = int(words[i - 1])  # El número del cotizante es la palabra anterior
                    except ValueError:
                        return "No se pudo extraer el número de cotizante."

            if tipo_cotizante_numero is None:
                return "No se pudo identificar el número de cotizante. Asegúrese de que la pregunta siga el formato esperado."

            # Extraer la columna (la palabra después de 'a')
            columna = words[-1].upper()  # Convertir a mayúsculas para hacer coincidir las columnas del Excel

            # Validar que la columna sea válida
            valid_columns = ['EPS', 'PEN', 'ARL', 'CCF', 'SEN', 'ICBF', 'ESAP', 'MIN']
            if columna not in valid_columns:
                return f"Columna '{columna}' no válida. Las columnas válidas son: {', '.join(valid_columns)}."

            # Consultar el aporte en el DataFrame (Aquí implementa tu lógica de consulta)
            return consultar_aporte(df_cotizantes, tipo_cotizante_numero, columna)

        # Lógica para la pregunta de tipo "novedad"
        elif tipo_pregunta == "novedad":

            cotizantes_excel_file = 'data/train_data.xlsx'
            # Leer la hoja 'Novedades' del archivo Excel
            df_cotizantes = pd.read_excel(cotizantes_excel_file, sheet_name='Novedades')
            print (df_cotizantes)
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

        # Lógica para la pregunta de tipo "novedad"
        elif tipo_pregunta == "planilla":
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


