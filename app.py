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

        with st.spinner("🔍 Mencari informasi pada dokumen RPS..."):

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

st.markdown("""
<div class="title-box">

<h1>🎓 Chatbot RPS</h1>

<p style="font-size:18px;">
Sistem Tanya Jawab Dokumen Rencana Pembelajaran Semester (RPS)
menggunakan Retrieval-Augmented Generation (RAG)
</p>

</div>
""", unsafe_allow_html=True)
with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/chatbot.png",
        width=80
    )

    st.title("Chatbot RPS")

    st.markdown("---")

    st.subheader("📚 Tentang")

    st.write("""
Chatbot ini membantu menjawab pertanyaan mengenai
dokumen RPS menggunakan metode
Retrieval-Augmented Generation (RAG).
""")

    st.markdown("---")

    st.subheader("🤖 Teknologi")

    st.success("Gemini 2.0 Flash")
    st.caption("Fallback")
    st.write("""
• Hugging Face

• Sumopod

• Qdrant

• OpenAI Embedding
""")

    st.markdown("---")

    st.subheader("📄 Dataset")

    st.info("77 Dokumen RPS")

    st.markdown("---")

    st.subheader("🔎 Retrieval")

    st.write("Top-K : 5 Chunks")

    st.markdown("---")

    st.caption("© 2026")

    st.info("""
### 💡 Contoh Pertanyaan

• Berapa SKS mata kuliah Bahasa Inggris Bisnis 2?

• Apa CPL mata kuliah Machine Learning?

• Apa prasyarat Sistem Terdistribusi?

• Apa CPMK mata kuliah Basis Data?
""")

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

st.divider()

st.caption(
    "🎓 Chatbot RPS | Dibangun menggunakan Streamlit • Qdrant • Gemini • Hugging Face • Sumopod"
)
