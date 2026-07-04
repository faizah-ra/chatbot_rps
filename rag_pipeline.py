from qdrant_client import QdrantClient
from openai import OpenAI
from google import genai
from google.genai import types

from config import (
    QDRANT_ENDPOINT,
    QDRANT_API_KEY,
    QDRANT_COLLECTION_NAME,
    GOOGLE_GENAI_API_KEY,
    VECTOR_SIZE,
    EMBEDDING_MODEL,
    GOOGLE_GEMINI_MODEL,
    HF_API_KEY,
    HF_BASE_URL,
    HF_LLM_MODEL_ID,
    SUMOPOD_API_KEY,
    SUMOPOD_BASE_URL,
    SUMOPOD_LLM_MODEL,
)
# from transformers import pipeline

# =====================================================================
# 1. ISIALISASI CLIENT & KONFIGURASI
# =====================================================================
qdrant_client = QdrantClient(url=QDRANT_ENDPOINT, api_key=QDRANT_API_KEY)
hf_client = OpenAI(
    api_key=HF_API_KEY,
    base_url=HF_BASE_URL,
)
sumopod_client = OpenAI(
    api_key=SUMOPOD_API_KEY,
    base_url=SUMOPOD_BASE_URL,
)
google_genai_client = genai.Client(
    api_key=GOOGLE_GENAI_API_KEY,
)

# ==========================
# 2. RETRIEVAL
# ==========================
def retrieval(query_text):

    query_text = " ".join(query_text.strip().split())
    embeddings = sumopod_client.embeddings.create(
        input=query_text,
        dimensions=VECTOR_SIZE,
        model=EMBEDDING_MODEL
    )

    query_vector = embeddings.data[0].embedding

    search_results = qdrant_client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=query_vector,
        limit=5,
        with_payload=True
    )
    print("✅ Retrieval selesai.")
    return query_text, search_results

# ==========================
# 3. AUGMENTATION
# ==========================
def augmentation(query_text, search_results):

    context_chunks = []
    sources = []

    for i, hit in enumerate(search_results.points, 1):
        text = hit.payload.get('text', '')
        doc = hit.payload.get('source_document', 'Unknown')
        page = hit.payload.get('page', 'Unknown')

        context_chunks.append(f"[Chunk {i}] {text}")
        sources.append(f"- {doc} (Halaman {page})")

    retrieved_context = "\n\n".join(context_chunks)
    sources_text = "\n".join(sources)

    prompt_text = f"""
========================
KONTEKS
========================
{retrieved_context}

========================
PERTANYAAN
========================
{query_text}

========================
SUMBER
========================
{sources_text}

========================
INSTRUKSI
========================

Jawablah pertanyaan pengguna hanya berdasarkan konteks yang diberikan.

- Gunakan informasi yang relevan saja.
- Jangan menyalin isi konteks secara verbatim.
- Jangan menjelaskan proses berpikir atau langkah-langkahmu.
- Jangan menuliskan "Inti pertanyaan", "Analisis", atau poin-poin instruksi.
- Jika informasi tidak ditemukan pada konteks, jawab:
  "Informasi tersebut tidak ditemukan pada dokumen RPS."
- Berikan jawaban yang ringkas dalam maksimal 5 kalimat.

========================
JAWABAN
========================
"""
    print("✅ Augmentation siap.")
    return prompt_text,sources

# ==========================
# 4. GENERATION
# ==========================
SYSTEM_INSTRUCTION = """
Anda adalah AI Assistant yang membantu menjawab pertanyaan mengenai dokumen RPS.

ATURAN:

1. Gunakan HANYA informasi pada konteks.
2. Jangan menggunakan pengetahuan di luar konteks.
3. Fokus menjawab inti pertanyaan pengguna.
4. Jika pertanyaan panjang, identifikasi terlebih dahulu inti pertanyaannya sebelum menjawab.
5. Jangan mengulang isi konteks.
6. Jangan menambahkan informasi yang tidak ditanyakan.
7. Berikan jawaban singkat, jelas, dan langsung pada inti pertanyaan.
8. Jawaban maksimal sekitar 120 kata kecuali pengguna meminta penjelasan rinci.
9. Jika informasi tidak ditemukan pada konteks, jawab:
"Informasi tersebut tidak ditemukan pada dokumen RPS."
"""

def generation(prompt_text):

    # =====================================================
    # 1. Gemini
    # =====================================================
    try:
        contents = types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)]
        )

        response = google_genai_client.models.generate_content(
            model=GOOGLE_GEMINI_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.1,
                top_p=0.8,
                max_output_tokens=300,
            ),
        )

        print("✅ Response dari Gemini")
        return response.text

    except Exception as gemini_error:

        print(f"⚠️ Gemini gagal:\n{gemini_error}")
        print("➡️ Menggunakan HuggingFace...")

    # =====================================================
    # 2. HuggingFace
    # =====================================================
    try:

        completion = hf_client.chat.completions.create(
            model=HF_LLM_MODEL_ID,
            messages=[
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            temperature=0.1,
            top_p=0.8,
            max_tokens=300,
        )

        print("✅ Response dari HuggingFace")
        return completion.choices[0].message.content

    except Exception as hf_error:

        print(f"⚠️ HuggingFace gagal:\n{hf_error}")
        print("➡️ Menggunakan Sumopod...")

    # =====================================================
    # 3. Sumopod
    # =====================================================
    try:

        completion = sumopod_client.chat.completions.create(
            model=SUMOPOD_LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt_text
                }
            ],
            temperature=0.1,
            top_p=0.8,
            max_tokens=300,
        )

        print("✅ Response dari Sumopod")
        return completion.choices[0].message.content

    except Exception as sumopod_error:

        raise RuntimeError(
            f"""
Semua LLM gagal.

Gemini:
{gemini_error}

HuggingFace:
{hf_error}

Sumopod:
{sumopod_error}
"""
        )

def ask(question):

    question, search_results = retrieval(question)

    prompt_text, sources = augmentation(question, search_results)

    answer = generation(prompt_text)

    return answer, sources