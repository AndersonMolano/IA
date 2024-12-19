import re
import pandas as pd

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
    subsistema_permitido,subsistema_no_permitido = subsitema_valido(df, tipo_cotizante_numero, columna)
    subsistema_permitido_str = ", ".join(map(str, subsistema_permitido))
    if aporte == 'X':
        return f"El tipo de cotizante {tipo_cotizante_numero} aporta OBLIGATORIAMENTE a {columna}."
    elif aporte == 'O':
        return f"El tipo de cotizante {tipo_cotizante_numero} aporta OPCIONALMENTE a {columna}."
    elif aporte == 'C':
        return f"El tipo de cotizante {tipo_cotizante_numero} aporta CONDICIONALMENTE a {columna}."
    else:
        return f"El tipo de cotizante {tipo_cotizante_numero} NO APORTA a {columna}. Sin embargo, liquida a los siguientes subsistemas: {subsistema_permitido_str}."

def subsitema_valido(df, tipo_cotizante_numero, columna):
    # Define los subtipos válidos a verificar
    valid_columns = ['EPS', 'AFP', 'ARL', 'CCF', 'SEN', 'ICBF', 'ESAP', 'MIN']
    subsistema_permitido = []
    subsistema_no_permitido = []

    for i in valid_columns:  # 'i' representa cada subtipo en la lista validas

            tipo_cotizante_row = df[df['No'] == tipo_cotizante_numero]
        
        # Verificar el valor en la columna correspondiente al subtipo
            aporte = tipo_cotizante_row[i].values[0]
        
        # Si el aporte es 'X', es permitido liquidar con ese subtipo
            if aporte == 'X':
                subsistema_permitido.append(i) 
            else:
                subsistema_no_permitido.append(i) 

    return subsistema_permitido, subsistema_no_permitido

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
            valid_columns = ['EPS', 'AFP', 'ARL', 'CCF', 'SEN', 'ICBF', 'ESAP', 'MIN']
            if columna not in valid_columns:
                return f"Columna '{columna}' no válida. Las columnas válidas son: {', '.join(valid_columns)}."

            # Consultar el aporte en el DataFrame (Aquí implementa tu lógica de consulta)
            return consultar_aporte(df_cotizantes, tipo_cotizante_numero, columna)
        else:
            return "Tipo de pregunta no reconocido. Asegúrese de que la pregunta sea de tipo 'relacion','novedad' o 'planilla'."
    except Exception as e:
        return f"Error al procesar la pregunta. Asegúrese de seguir el formato correcto. {str(e)}"