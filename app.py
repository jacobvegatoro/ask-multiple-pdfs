import streamlit as st
from dotenv import load_dotenv
from htmlTemplates import css, bot_template, user_template
from getPdfText import get_pdf_text
from getTextChunks import get_text_chunks
from getVectorStore import get_vectorstore
from getConversationChain import get_conversation_chain

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Extrae información desde archivos PDF",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Extrae información desde archivos PDF :books:")
    user_question = st.text_input("Realiza una pregunta en base a tus documentos:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Tus documentos")
        pdf_docs = st.file_uploader(
            "Sube aqui tus archivos PDF y presiona el botón 'Procesar'", accept_multiple_files=True)
        if st.button("Procesar"):
            with st.spinner("Procesando"):
                # Obtener el texto desde los archivos PDF
                raw_text = get_pdf_text(pdf_docs)

                # Obtiene las porciones de texto
                text_chunks = get_text_chunks(raw_text)

                # Crea una base de datos de tipo vector para búsquedas
                vectorstore = get_vectorstore(text_chunks)

                # Crea una cadena de conversación
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
