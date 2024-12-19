$(document).ready(function () {
    // Prevenir el envío del formulario al presionar "Enter"
    $('#questionInput').on('keydown', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // Previene el comportamiento predeterminado (envío del formulario)
            $('.submitButton').click(); // Dispara el evento click en la imagen de envío
        }
    });


    $(document).ready(function () {
        // Ajustar el tamaño del textarea automáticamente al escribir
        $('#questionInput').on('input', function () {
            this.style.height = 'auto'; // Resetea la altura para que se pueda calcular la nueva
            this.style.height = (this.scrollHeight) + 'px'; // Ajusta la altura del textarea al contenido

            // Limitar el número de filas a un máximo de 5 (puedes cambiar 5 a cualquier valor)
            var maxRows = 5;
            var lineHeight = parseInt($(this).css('line-height')); // Obtener la altura de una línea
            var maxHeight = lineHeight * maxRows; // Calcula la altura máxima basada en las filas

            if (this.scrollHeight > maxHeight) {
                this.style.height = maxHeight + 'px'; // Ajustar la altura al valor máximo
            }

            // Al hacer clic en el botón de enviar, restablecer la altura del textarea y el número de filas
            $('#sendText').on('click', function (event) {
                // Restablecer la altura a 'auto' y el número de filas a 1.5
                $('#questionInput').css('height', 'auto'); // Restablecer la altura automática
                $('#questionInput').prop('rows', 1.5); // Restablecer el número de filas a 1.5
            });
        });
    });

    // Obtener los elementos del DOM
    const imgPregunta = document.getElementById("img-pregunta");
    const modal = document.getElementById("modal");
    const closeModal = document.getElementsByClassName("close")[0];

    // Mostrar el modal cuando se hace clic en la imagen
    imgPregunta.addEventListener("click", function () {
        // Mensaje a mostrar en el modal
        const mensaje = `
¿Tienes dudas sobre el modelo de IA PILA? Prueba con estas preguntas:  
- ¿El cotizante 20 aporta a EPS?  
- ¿El cotizante 33 es válido para independientes?  
- ¿El cotizante 32 es permitido para el subtipo 0?  

Si tienes más preguntas, sé más específico o envíalas a: andersonm_tec@jaimetorres.net.
    `;

        // Cambiar el texto del modal
        document.getElementById("mensaje-modal").textContent = mensaje;

        // Mostrar el modal
        modal.style.display = "block";
    });

    // Cerrar el modal cuando se hace clic en la "X"
    closeModal.addEventListener("click", function () {
        modal.style.display = "none"; // Ocultar el modal
    });

    // Cerrar el modal si se hace clic fuera de la ventana emergente
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none"; // Ocultar el modal si se hace clic fuera de él
        }
    });

    // Enviar el formulario usando AJAX
    $('.submitButton').on('click', function (event) {
        event.preventDefault(); // Previene el comportamiento por defecto del clic
        const submitButton = $(this); // Identificar cuál botón fue presionado
        submitButton.prop('disabled', true); // Deshabilitar el botón mientras se espera la respuesta

        /** Obtener el valor de la pregunta */
        const questionText = $("#questionInput").val();

        /* limpiar el campo de texto*/
        $("#questionInput").val("")

        // Validar que el campo no esté vacío
        if (questionText.trim() === "") {
            submitButton.prop('disabled', false); // Habilitar el botón nuevamente si el campo está vacío
            return; // No enviar la solicitud si el campo está vacío
        }

        /**
         * Crear el nuevo elemento para la pregunta
         */
        const questionElement = `
            <div class="question" style="position: relative; margin-left: 40px; margin-bottom: 10px;">
                <!-- Imagen posicionada fuera del contenedor de la pregunta -->
                <img src="../static/img/masculino.png" alt="user" style="height: 34px; position: absolute; left: -40px; top: 50%; transform: translateY(-50%); border-radius: 50%;"> 
                <!-- Texto de la pregunta -->
                <p><strong>USER:</strong> ${questionText}</p>
            </div>
        `;
        $('#conversation').append(questionElement); // Agregar la pregunta al contenedor de la conversación

        $(document).ready(function () {
            /**
             * Modificar los estilos dinámicamente
             * @param {string} p1 selector CSS  
             * @param {object} p2 Objeto con la configuración
             */
            const F = (p1, p2) => {
                return $(p1).css(p2);
            }

            // Función para aplicar el estilo al h1
            const adjustH1Position = () => {
                const windowWidth = window.innerWidth;

                if (windowWidth <= 600) {
                    // Si el ancho de la ventana es menor o igual a 600px
                    F('h1', {
                        'top': '10%'  // Cambiar el valor de 'top' a 10%
                    });
                } else {
                    // Si el ancho de la ventana es mayor a 600px
                    F('h1', {
                        'top': '3%'  // Mantener el valor de 'top' en 3%
                    });
                }
            }

            // Llamar a la función para ajustar el h1 al cargar la página
            adjustH1Position();

            // Ajustar el h1 cuando el tamaño de la ventana cambie
            $(window).resize(function () {
                adjustH1Position();
            });

            // Aplicar otros estilos
            F('#conversation', { visibility: 'visible' }).animate({ opacity: 1 }, 500);
            F('body', {
                'justify-content': 'end',
            });
            F('h1', {
                'position': 'absolute',
                'left': '50%',
                'transform': 'translateX(-50%)',
                'border-right': 'none',
            });
            F('footer', {
                'position': 'static'
            });
        });


        // Enviar la solicitud AJAX
        $.ajax({
            url: '/ask',  // Ruta en Flask
            method: 'POST',
            data: { question: questionText },  // Datos del formulario
            success: function (data) {
                // Crear el nuevo elemento para la respuesta
                //<p><strong>TIEMPO:</strong> ${data.time}</p>
                //<p><strong>TIPO PREGUNTA:</strong> ${data.response}</p>
                const responseElement = `
                    <div class="response" style="position: relative; margin-left: 40px; margin-bottom: 10px;">
                        <!-- Imagen posicionada fuera del contenedor de la respuesta -->
                        <img src="../static/img/femenino.png" alt="user" style="height: 34px; position: absolute; left: -40px; top: 50%; transform: translateY(-50%); border-radius: 50%;"> 
                        <!-- Texto de la respuesta -->
                        <p><strong>TIEMPO:</strong> ${data.time}</p>
                        <p><strong>TIPO PREGUNTA:</strong> ${data.response}</p>
                        <p><strong>PILA:</strong> ${data.answer}</p>
                    </div>
                `;
                $('#conversation').append(responseElement); // Agregar la respuesta al contenedor de la conversación

                // Hacer que la conversación se desplace hacia abajo automáticamente
                $('#conversation').scrollTop($('#conversation')[0].scrollHeight);

                // Limpiar el campo de entrada después de enviar la pregunta y recibir la respuesta
                $("#questionInput").val('');
            },
            error: function () {
                alert('Ocurrió un error al enviar la pregunta.');
            },
            complete: function () {
                submitButton.prop('disabled', false);  // Habilitar el botón nuevamente
            }
        });
    });
});
