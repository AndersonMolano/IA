import ollama  # Importa la librería Ollama para interactuar con el modelo de lenguaje
import hashlib  # Importa hashlib para generar un hash del prompt y utilizarlo como clave en el caché

# Diccionario para almacenar las respuestas previas
cache = {}

def main(question):
    """
    Función principal que procesa una pregunta, verifica si ya existe una respuesta en cache, 
    y si no, realiza una consulta al modelo de Ollama para obtener una respuesta.

    :param question: Pregunta que el usuario quiere hacer al modelo.
    :return: La respuesta generada por el modelo o la respuesta en caché si ya fue calculada previamente.
    """
    
    # Convierte la pregunta a una cadena de texto (por si el input no es una cadena)
    prompt = str(question)
    
    # Define el modelo a utilizar, en este caso "llama3.2"
    modelo = "llama3.2"
    
    # Genera un hash único para la pregunta usando SHA256. Este hash se usará como clave para almacenar la respuesta en cache.
    prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
    
    # Verifica si la respuesta para esta pregunta ya está en el cache
    if prompt_hash in cache:
        # Si la respuesta ya está en cache, la recupera y la devuelve
        print("Usando respuesta de cache")  # Mensaje para depuración
        return cache[prompt_hash]
    
    # Si la respuesta no está en el cache, realiza una llamada al modelo de Ollama para obtener una nueva respuesta
    response = ollama.chat(
        model=modelo,  # Nombre del modelo que se utilizará para generar la respuesta
        messages=[{'role': 'user', 'content': prompt}],  # El mensaje que envías al modelo
        tools=None,  # No estamos usando herramientas externas, por lo que se deja en None
        stream=False,  # Respuesta completa, no streaming
        format='',  # En formato JSON, para asegurarnos de recibir la respuesta de forma estructurada
        options={
            'temperature': 0.3,  # Reducir la aleatoriedad para respuestas más concisas y controladas
            'max_tokens': 100,  # Limitar la longitud de la respuesta a 100 tokens (ajustable según necesidad)
            'stop_sequences': ['\n']  # Usar una secuencia de parada para que termine la respuesta en el primer salto de línea
        },
        keep_alive=None  # No necesitamos mantener la conexión abierta por más tiempo
    )
    
    # Imprime la respuesta completa para depuración (puede variar según la estructura de la respuesta del modelo)
    #print(response)  # Mensaje para depurar y verificar la respuesta completa del modelo
    
    # Intenta extraer el contenido de la respuesta del modelo y almacenarlo en el cache
    try:
        # Extrae el texto de la respuesta (se espera que la respuesta esté en la clave 'message' -> 'content')
        response_text = response['message']['content']
        
        # Imprime la respuesta obtenida para depuración
        print(response_text)
        
        # Almacena la respuesta en cache usando el hash del prompt como clave
        cache[prompt_hash] = response_text
        
        # Devuelve la respuesta generada
        return response_text
    except KeyError:
        # Si no se puede encontrar la clave 'message' en la respuesta, muestra un mensaje de error
        print("Error: no se pudo encontrar la clave 'message' en la respuesta")
        return None  # Retorna None si no se pudo procesar la respuesta
