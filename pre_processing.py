from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import leer_documento  # Este es el módulo de IA que responderá las preguntas fuera de las categorías

# Inicializar la aplicación Flask
app = Flask(__name__)

# Cargar los datos del CSV solo una vez para entrenamiento
qa_df = pd.read_csv('data/relations.csv')
print("Datos de consulta cargados con éxito.")

# Verificar y limpiar datos
qa_df.dropna(subset=['Pregunta', 'Tipo'], inplace=True)

# Separar características y etiquetas
X = qa_df['Pregunta']
y = qa_df['Tipo']

# Dividir los datos en entrenamiento y prueba (80-20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear un pipeline para el modelo de clasificación
classification_model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', SVC(probability=True))  # Aseguramos que SVC calcule probabilidades
])

# Entrenar el modelo
classification_model.fit(X_train, y_train)

# Evaluar el modelo
accuracy = classification_model.score(X_test, y_test)
print(f'Precisión del modelo de clasificación: {accuracy}')

# Ruta principal para cargar la página de inicio (index.html)
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')  # Renderiza el archivo index.html

# Ruta para procesar las preguntas del usuario (POST)
@app.route('/ask', methods=['POST'])
def ask():
    # Obtener la pregunta enviada por el formulario
    question = request.form['question']
    
    # Tomar el tiempo de inicio antes de procesar la pregunta
    start_time = time.time()

    # Procesar la pregunta utilizando el modelo ya entrenado
    predicted_label = classification_model.predict([question])[0]  # Predicción del tipo de pregunta
    predicted_prob = classification_model.predict_proba([question])[0]  # Probabilidad de cada clase

    # Obtener la probabilidad máxima
    max_prob = max(predicted_prob)

    # Preparar la respuesta básica
    response = f"La pregunta: '{question}' fue clasificada como tipo '{predicted_label}' con una probabilidad de {max_prob:.2f}"

    print(f"Tiempo de ejecución total: {round(time.time() - start_time, 4)} segundos")

    # Validar si la probabilidad es suficientemente alta para aceptar la clasificación
    if max_prob < 0.7:  # Si la probabilidad es menor a 60%, se considera "incierta"
        print(f"Probabilidad baja: {max_prob}. Redirigiendo al modelo de IA.")
        predicted_label = 'IA'  # Establecer la etiqueta de IA

        # Llamar al modelo de IA (debe manejar esta parte)
        try:
            ia_response = leer_documento.main(question, predicted_label)  # Redirigir al modelo de IA para obtener la respuesta
            total_execution_time = round(time.time() - start_time, 4)  # Tiempo total de ejecución

            return jsonify(response="Pregunta redirigida al modelo de IA", 
                           answer=ia_response, 
                           time=total_execution_time)  # Incluir tiempo total de ejecución
        except Exception as e:
            return jsonify(error=f"Error al procesar la pregunta con el modelo de IA: {str(e)}")
    
    # Si la clasificación es confiable, procesarla con el modelo entrenado
    try:
        # Limpiar el valor de predicted_label (eliminar comillas y espacios extras)
        tipo_pregunta = predicted_label.strip().replace('"', '').replace("'", "")
        respuesta = leer_documento.main(question, tipo_pregunta)
        total_execution_time = round(time.time() - start_time, 4)  # Tiempo total de ejecución
        return jsonify(response=response, answer=respuesta, time=total_execution_time)
    except Exception as e:
        print(f"Error al procesar la clasificación: {e}")
        return jsonify(error="No se obtiene ningún tipo de clasificación")

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)  # Ejecuta el servidor con el modo de depuración activado
