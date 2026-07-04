import streamlit as st
from rag_pipeline import ask

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Chatbot RPS",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Chatbot RPS")
st.caption("Tanyakan apa saja mengenai dokumen RPS.")

# ======================================================
# CHAT HISTORY
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if "sources" in message:

                with st.expander("📄 Lihat Sumber"):

                    for source in message["sources"]:

                        st.write(source)

# ======================================================
# INPUT USER
# ======================================================
prompt = st.chat_input("Masukkan pertanyaan...")

if prompt:

    # tampilkan pertanyaan user
    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # jalankan RAG
    with st.chat_message("assistant"):

        with st.spinner("Sedang mencari jawaban..."):

            answer, sources = ask(prompt)

            st.markdown(answer)

            with st.expander("📄 Lihat Sumber"):

                for source in sources:

                    st.write(source)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer,
            "sources":sources
        }
    )