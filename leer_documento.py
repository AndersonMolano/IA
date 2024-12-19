import pandas as pd
import re
from templates import aportante, novedad, planilla, relacion, subtipos, consulta, error


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
            print("Inicia el modelo de relación")
            respuesta = relacion.main(question, predicted_label)  
            return respuesta  # Retorna la respuesta obtenida   
        # Lógica para la pregunta de tipo "novedad"
        elif tipo_pregunta == "novedad":
            print("Inicia el modelo de novedad")
            respuesta = novedad.main(question, predicted_label)  
            return respuesta  # Retorna la respuesta obtenida   
        # Lógica para la pregunta de tipo "novedad"
        elif tipo_pregunta == "IA":
            print("Inicia el modelo de IA")
            respuesta = consulta.main(question) 
            print ("obtiene la siguiente respuesta:" + respuesta) 
            return respuesta  # Retorna la respuesta obtenida   
        elif tipo_pregunta == "planilla":
            print("Inicia el modelo de planilla")
            respuesta = planilla.main(question, predicted_label)  
            return respuesta  # Retorna la respuesta obtenida  
        elif tipo_pregunta == "aportante":
            print("Inicia el modelo de aportante")
            respuesta = aportante.main(question, predicted_label)  
            return respuesta  # Retorna la respuesta obtenida  
        elif tipo_pregunta == "error":
            print("Inicia el modelo de error")
            respuesta = error.main(question)  
            return respuesta  # Retorna la respuesta obtenida 
        elif tipo_pregunta == "subtipo":
            print("Inicia el modelo de subtipo")
            respuesta = subtipos.main(question, predicted_label)  
            return respuesta  # Retorna la respuesta obtenida 
        else:
            print(tipo_pregunta)
            return "Tipo de pregunta no reconocido. Asegúrese de que la pregunta sea de tipo 'relacion','novedad' o 'planilla'."
    except Exception as e:
        return f"Error al procesar la pregunta. Asegúrese de seguir el formato correcto. {str(e)}"


