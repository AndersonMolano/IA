import re
import pandas as pd  

# Función para consultar la novedad de un cotizante
def consultar_subtipo(df_subtipo, tipo_cotizante_numero, subtipo):
    # Mantener subtipo como cadena
    subtipo = int(subtipo)
    
    # Verificar si el subtipo existe como columna en el DataFrame
    if subtipo not in df_subtipo.columns:
        return f"subtipo '{subtipo}' no encontrado en el archivo."

    # Buscar la fila correspondiente al tipo de cotizante por su número
    tipo_cotizante_row = df_subtipo[df_subtipo['No'] == tipo_cotizante_numero]
    
    # Verificar que se haya encontrado el tipo de cotizante
    if tipo_cotizante_row.empty:
        return f"Tipo de cotizante con número '{tipo_cotizante_numero}' no encontrado."

    # Verificar el valor en la columna específica para el subtipo
    aporte = tipo_cotizante_row[subtipo].values[0]

    if aporte == 'X':
        return f"Para el tipo de cotizante {tipo_cotizante_numero} es permitido liquidar con el subtipo {subtipo}."
    else:
        subtipos_permitidos,subtipos_no_permitidos = subtipos_validos(df_subtipo, tipo_cotizante_numero, subtipo)
        #print (subtipos_permitidos)
        #print (subtipos_no_permitidos)
        subtipos_permitidos_str = ", ".join(map(str, subtipos_permitidos))
        return f"No se permite realizar la liquidación con el subtipo {subtipo} para el tipo de cotizante {tipo_cotizante_numero}. Sin embargo, es posible efectuar la liquidación utilizando alguno de los siguientes subtipos: {subtipos_permitidos_str}"

# Función para verificar si el tipo de cotizante tiene permisos para otros subtipos
def subtipos_validos(df_subtipo, tipo_cotizante_numero, subtipo):
    # Define los subtipos válidos a verificar
    subtipo = int(subtipo)
    validas = ['0','1','2','3','4','5','6','9','10','11','12']
    subtipos_permitidos = []
    subtipos_no_permitidos = []

    for i in validas:  # 'i' representa cada subtipo en la lista validas
            i = int(i)
        
            # Buscar la fila correspondiente al tipo de cotizante
            tipo_cotizante_row = df_subtipo[df_subtipo['No'] == tipo_cotizante_numero]
        
        # Verificar el valor en la columna correspondiente al subtipo
            aporte = tipo_cotizante_row[i].values[0]
        
        # Si el aporte es 'X', es permitido liquidar con ese subtipo
            if aporte == 'X':
                subtipos_permitidos.append(i) 
            else:
                subtipos_no_permitidos.append(i) 

    return subtipos_permitidos, subtipos_no_permitidos

# Función principal para procesar la pregunta del usuario
def main(question, predicted_label):
    user_input = question
    tipo_pregunta = predicted_label
    try:
        if tipo_pregunta == "subtipo":
            cotizantes_excel_file = 'data/train_data.xlsx'
            # Leer la hoja 'Subtipo_cotizante' del archivo Excel
            df_subtipo = pd.read_excel(cotizantes_excel_file, sheet_name='Subtipo_cotizante')
            
            if 'subtipo' not in user_input:
                return "Pregunta no válida. Asegúrese de que la pregunta tenga el formato: 'El tipo de cotizante X es permitido para el subtipo COLUMN'"
            
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

            # Extraer el subtipo (última palabra de la pregunta)
            subtipo = words[-1].upper()  # Convertir a mayúsculas para hacer coincidir las novedades en el sistema

            # Validar que el subtipo sea válido
            subtipo_valido = ['0', '1', '2', '3', '4', '5', '6', '9', '10', '11', '12']
            if subtipo not in subtipo_valido:
                return f"subtipo '{subtipo}' no válido. Los subtipos válidos son: {', '.join(subtipo_valido)}."

            # Aquí deberías implementar la lógica de consulta de la novedad
            return consultar_subtipo(df_subtipo, tipo_cotizante_numero, subtipo)
        else:
            return "Tipo de pregunta no reconocido. Asegúrese de que la pregunta sea de tipo 'relacion','novedad' o 'planilla'."
    except Exception as e:
        return f"Error al procesar la pregunta. Asegúrese de seguir el formato correcto. {str(e)}"
