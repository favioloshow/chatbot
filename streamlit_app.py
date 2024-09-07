import streamlit as st
import requests

# Mostrar título y descripción.
st.title("💬 Chatbot usando AWS Lambda URL")
st.write(
    "Este es un chatbot que utiliza una Lambda Function en AWS para generar respuestas. "
    "Por favor, provee la URL de la Lambda para continuar."
)

lambda_url = st.text_input("Lambda URL", placeholder="Introduce la URL de tu Lambda Function")

if not lambda_url:
    st.info("Por favor, ingresa la URL de la Lambda para continuar.", icon="🗝️")
else:
    # Crear una variable de estado de sesión para almacenar los mensajes.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar los mensajes existentes.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Crear el campo de entrada para permitir al usuario escribir un mensaje.
    if prompt := st.chat_input("Escribe tu mensaje:"):

        # Almacenar y mostrar el mensaje del usuario.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Enviar la solicitud a la Lambda Function URL.
        try:
            response = requests.post(lambda_url, json={"prompt": prompt})
            response.raise_for_status()  # Verificar si la solicitud fue exitosa
            lambda_response = response.json().get("response", "No se recibió una respuesta válida de Lambda")

            # Mostrar la respuesta de la Lambda en el chat.
            with st.chat_message("assistant"):
                st.markdown(lambda_response)
            st.session_state.messages.append({"role": "assistant", "content": lambda_response})

        except requests.exceptions.RequestException as e:
            st.error(f"Error al llamar a la Lambda: {e}")
