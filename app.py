import streamlit as st
from rag_pipeline import ask

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Chatbot RPS",
    page_icon="🎓",
    layout="wide"
)

# ======================================================
# CSS
# ======================================================
st.markdown("""
<style>

.stApp{
    background-color:#F6F8FC;
}

.title-box{
    background:linear-gradient(90deg,#0F4C81,#2563EB);
    padding:25px;
    border-radius:15px;
    color:white;
    margin-bottom:20px;
    box-shadow:0px 5px 15px rgba(0,0,0,.15);
}

section[data-testid="stSidebar"]{
    background-color:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white;
}

.stChatInput{
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown("""
<div class="title-box">

<h1>🎓 Chatbot RPS</h1>

<p style="font-size:18px;">
Sistem Tanya Jawab Dokumen Rencana Pembelajaran Semester (RPS)
menggunakan Retrieval-Augmented Generation (RAG)
</p>

</div>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================
with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/chatbot.png",
        width=90
    )

    st.title("Chatbot RPS")

    st.markdown("---")

    st.subheader("📚 Tentang")

    st.write("""
Chatbot ini membantu menjawab pertanyaan mengenai dokumen RPS
menggunakan metode Retrieval-Augmented Generation (RAG).
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

    st.subheader("💡 Contoh Pertanyaan")

    st.write("""
• Apa CPL dan CPMK bahasa inggris bisnis 2?

• Tools yang di gunakan mata kuliah pengolahan citra?

• Apa materi pembelajaran Basis Data?

• Berapa SKS sistem multimedia?
""")

    st.markdown("---")

    st.caption("© 2026")

# ======================================================
# SESSION STATE
# ======================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================================================
# CHAT HISTORY
# ======================================================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and "sources" in message
        ):

            with st.expander("📄 Lihat Sumber"):

                for source in message["sources"]:
                    st.write(source)

# ======================================================
# INPUT
# ======================================================
prompt = st.chat_input(
    "Masukkan pertanyaan mengenai RPS...",
    key="chat_input"
)

# ======================================================
# GENERATE
# ======================================================
if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Mencari informasi pada dokumen RPS..."):

            answer, sources = ask(prompt)

            st.markdown(answer)

            with st.expander("📄 Lihat Sumber"):

                for source in sources:
                    st.write(source)

    st.session_state.messages.append({
        "role":"assistant",
        "content":answer,
        "sources":sources
    })

# ======================================================
# FOOTER
# ======================================================
st.divider()

st.caption(
    "🎓 Chatbot RPS | Streamlit • Qdrant • Gemini • Hugging Face • Sumopod"
)
