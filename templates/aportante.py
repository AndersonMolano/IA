import pandas as pd
import re
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

def consultar_tipo_aportante(question):
    # Cargar datos de preguntas y respuestas (consulta)
        qa_df = pd.read_csv('data/aportantes.csv') 
        print("Datos de consulta cargados con éxito.")
        qa_df.dropna(subset=['Aportante','Numero'], inplace=True)
        X = qa_df['Aportante']
        y = qa_df['Numero'] 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        classification_model = Pipeline([
            ('vectorizer', TfidfVectorizer()),
            ('classifier', SVC())  
        ])
    
        classification_model.fit(X_train, y_train)
        accuracy = classification_model.score(X_test, y_test)
        print(f'Precisión del modelo de clasificación: {accuracy}')

        vectorizer_qa = TfidfVectorizer()
        model_qa = Pipeline([
            ('vectorizer', vectorizer_qa),
            ('classifier', SVC())
        ])
    
        parameters_qa = {'classifier__C': [0.1, 1, 10], 'classifier__kernel': ['linear', 'rbf']}
        grid_search_qa = GridSearchCV(model_qa, parameters_qa, cv=KFold(n_splits=2))
        grid_search_qa.fit(X_train, y_train)
    
        print(f"Mejores parámetros para preguntas de consulta: {grid_search_qa.best_params_}")
    
        user_input = question
        # Usamos una expresión regular para encontrar lo que sigue después de "aportante"
        match = re.search(r'aportante\s+(.+)', user_input)
        # Extraemos el texto después de "aportante"
        aportante = match.group(1)
        print(aportante)
    
        # Predecir la respuesta para la pregunta ingresada
        answer = classification_model.predict([aportante])[0]
        print(f"Aportante: '{aportante}' -> Tipo: {answer}")
        return answer

def consultar_aportante(df_aportante, tipo_cotizante_numero, tipo_aportante, quetion):
     if tipo_aportante not in df_aportante:
             return f"Aportante '{tipo_aportante}' no encontrada en el archivo."

        # Buscar la fila correspondiente al tipo de cotizante por su número
     tipo_cotizante_row = df_aportante[df_aportante['No'] == tipo_cotizante_numero]
        # Verificar que se haya encontrado el tipo de cotizante
     if tipo_cotizante_row.empty:
            return f"Tipo de cotizante con número '{tipo_cotizante_numero}' no encontrado."

        # Verificar el valor en la columna específica
     aporte = tipo_cotizante_row[tipo_aportante].values[0]
     parte = quetion.split('aportante')
    # La parte que sigue a 'aportante' estará en la segunda posición
     texto_aportante = parte[1].strip() 
     aportante_permitido,aportante_no_permitido = aportante_valido(df_aportante, tipo_cotizante_numero, quetion)
     aportante_permitido_str = ", ".join(map(str, aportante_permitido))

     if aporte == 'X':
             return f"Para el tipo de cotizante {tipo_cotizante_numero} es permitido el aportante {texto_aportante}."
     else:
             return f"Para el tipo de cotizante {tipo_cotizante_numero} no es permitido el aportante {texto_aportante}. Sin embargo, es permitido para los siguientes aportantes: {aportante_permitido_str}."

def aportante_valido(df_aportante, tipo_cotizante_numero, quetion):
    # Define los subtipos válidos a verificar
    aportante_valido = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    aportante_permitido = []
    aportante_no_permitido = []

    for i in aportante_valido:  # 'i' representa cada subtipo en la lista validas
            i = int(i)
            tipo_cotizante_row = df_aportante[df_aportante['No'] == tipo_cotizante_numero]
        
        # Verificar el valor en la columna correspondiente al subtipo
            aporte = tipo_cotizante_row[i].values[0]
        
        # Si el aporte es 'X', es permitido liquidar con ese subtipo
            if aporte == 'X':
                aportante_permitido.append(i) 
            else:
                aportante_no_permitido.append(i) 
    return aportante_permitido, aportante_no_permitido

def main(question, predicted_label):
    user_input = question
    tipo_pregunta = predicted_label
    try:
        if tipo_pregunta == "aportante":
            cotizantes_excel_file = 'data/train_data.xlsx'
            # Leer la hoja 'Novedades' del archivo Excel
            df_aportante = pd.read_excel(cotizantes_excel_file, sheet_name='tipo_aportante')
            if 'aportante' not in user_input:
                return "Pregunta no válida. Asegúrese de que la pregunta tenga el formato: 'El tipo de cotizante X es permitido para el aportante COLUMN'"

            tipo_aportante = consultar_tipo_aportante(question)
            print("El tipo de aportante es:"+str(tipo_aportante))
             # Buscar el número del cotizante (después de "cotizante")
            words = user_input.split()
            tipo_cotizante_numero = None
            for i, word in enumerate(words):
                if word == 'cotizante' and i + 1 < len(words):
                    try:
                        tipo_cotizante_numero = int(words[i + 1])  # El número del cotizante es el siguiente a "cotizante"
                    except ValueError:
                        return "No se pudo extraer el número de cotizante."
            print("el tipo de cotizante es: "+str(tipo_cotizante_numero))
            if tipo_cotizante_numero is None:
                return "No se pudo identificar el número de cotizante. Asegúrese de que la pregunta siga el formato esperado."
            
            tipo_aportante_valido = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
            
            if str(tipo_aportante) not in tipo_aportante_valido:
                print(f"Aportante '{tipo_aportante}' no válido. Los tipos válidos son: {', '.join(tipo_aportante_valido)}.") 

            return consultar_aportante(df_aportante, tipo_cotizante_numero, tipo_aportante, user_input)
        else:
            return "Tipo de pregunta no reconocido. Asegúrese de que la pregunta sea de tipo 'relacion','novedad' o 'planilla'."
    except Exception as e:
        return f"Error al procesar la pregunta. Asegúrese de seguir el formato correcto. {str(e)}"
