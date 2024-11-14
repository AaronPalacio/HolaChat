import streamlit as st
from groq import Groq

st.set_page_config(page_title="Hola Chat", page_icon="😂")

st.title("Hola")

nombre = st.text_input("¿Cuál es tu nombre?")

if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! gracias por venir.")
    

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def generar_respuesta(chatcompleto):
    respuesta_completa = ""
    for frase in chatcompleto:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def configurar_pagina():
    st.title("Di Hola al Chat")
    st. sidebar.title("Configuración")
    elegirModelo = st.sidebar.selectbox("Elegir un modelo", options = modelos, index=0)
    return elegirModelo


def creaUsuario ():
    clave = st.secrets["CLAVE_API"]
    return Groq(api_key=clave)

def configurar_modelo(cliente,modelo,mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages = [{"role":"user", "content":mensajeDeEntrada}],
        stream=True
    )
    
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
        

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content":contenido, "avatar": avatar})
    
def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"],avatar = mensaje ["avatar"]):
            st.markdown(mensaje["content"])
            
def area_chat():
    contenedorDelChat = st.container(height=300,border=True)
    with contenedorDelChat:
        mostrar_historial()
    
def main():
    modelo = configurar_pagina()
    Usuario = creaUsuario()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Escribí tu mensaje:")
    if mensaje:
        actualizar_historial("user",mensaje,"😶")
        chat_completo = configurar_modelo(Usuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistent", respuesta_completa,"😂")
        st.rerun()
    
if __name__ == "__main__":
    main()