from flask import Flask, request, render_template, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import leer_documento  
from flask import Flask, request, jsonify, render_template 
from sklearn.model_selection import train_test_split, GridSearchCV, KFold

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
    ('classifier', SVC())
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
    
    # Procesar la pregunta utilizando el modelo ya entrenado
    start_time = time.time()  # Tomamos el tiempo de inicio
    predicted_label = classification_model.predict([question])[0]
    predicted_label = predicted_label.strip().replace('"', '')  # Limpiar el valor de predicted_label (quitar comillas extra)
    execution_time = round(time.time() - start_time, 4)  # Calculamos el tiempo de ejecución

    # Preparar la respuesta
    response = f"La pregunta: '{question}' fue clasificada como tipo '{predicted_label}'"
    
    print(f"Tiempo de ejecución: {execution_time} segundos")
    
# Lógica para cada tipo de clasificación
    if predicted_label == 'relacion' or predicted_label == 'novedad' or predicted_label == 'planilla':
      respuesta = ejecutar_leer_documento(question, predicted_label)  
      print (respuesta)
    elif predicted_label == 'consulta':
       respuesta = ejecutar_consulta_general(question)  
    else:
       print("No se obtiene ningún tipo de clasificación")
    # Devolver la respuesta como JSON
    return jsonify(response=response, answer=respuesta, time=execution_time)

def ejecutar_leer_documento(question, predicted_label):
    # Inicia el proceso de cada pregunta
    print("Inicia el modelo de relación")
    respuesta = leer_documento.main(question, predicted_label)  
    return respuesta  # Retorna la respuesta obtenida

def ejecutar_consulta_general(question):
    # Inicia el proceso de cada pregunta
    print("Inicia el modelo de consulta")

    # Cargar datos de preguntas y respuestas (consulta)
    qa_df = pd.read_csv('data/train.csv')  # Preguntas de consulta
    print("Datos de consulta cargados con éxito.")

    # Verificar y limpiar datos, eliminar filas con valores nulos en 'Pregunta' o 'Respuesta'
    qa_df.dropna(subset=['Pregunta', 'Respuesta'], inplace=True)

    # Separar características (X) y etiquetas (y), pero aquí solo utilizamos las preguntas (X) y respuestas (y)
    X = qa_df['Pregunta']
    y = qa_df['Respuesta']  # Ahora 'Respuesta' es la etiqueta que queremos predecir

    # Dividir los datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Crear un pipeline para el modelo de clasificación con SVC
    classification_model = Pipeline([
        ('vectorizer', TfidfVectorizer()),  # Convertir texto a vectores usando TF-IDF
        ('classifier', SVC())  # Clasificador SVC
    ])

    # Entrenar el modelo
    classification_model.fit(X_train, y_train)

    # Evaluar el modelo
    accuracy = classification_model.score(X_test, y_test)
    print(f'Precisión del modelo de clasificación: {accuracy}')

    # Ajustar hiperparámetros con GridSearchCV para la mejor combinación de parámetros
    vectorizer_qa = TfidfVectorizer()
    model_qa = Pipeline([
        ('vectorizer', vectorizer_qa),
        ('classifier', SVC())
    ])

    # Ajustar hiperparámetros para consultas
    parameters_qa = {'classifier__C': [0.1, 1, 10], 'classifier__kernel': ['linear', 'rbf']}
    grid_search_qa = GridSearchCV(model_qa, parameters_qa, cv=KFold(n_splits=2))
    grid_search_qa.fit(X_train, y_train)

    print(f"Mejores parámetros para preguntas de consulta: {grid_search_qa.best_params_}")

    # Clasificar la pregunta y obtener la respuesta
    user_input = question

    # Predecir la respuesta para la pregunta ingresada
    answer = classification_model.predict([user_input])[0]
    print(f"Pregunta: '{user_input}' -> Respuesta: {answer}")
    return answer

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)  # Ejecuta el servidor con el modo de depuración activado
