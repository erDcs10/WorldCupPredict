import streamlit as st
import os

from src.query import RAGQueryEngine

# Page Setup
st.set_page_config(page_title="World Cup Predict", page_icon="docs\WCP_Kecil-01.svg", layout="centered")
st.title("World Cup Analyst v1.0.0")

# Inisialisasi Backend Engine menggunakan Streamlit Cache
@st.cache_resource
def load_engine():
    try:
        return RAGQueryEngine()
    except FileNotFoundError as e:
        st.error(f"❌ {e}")
        st.stop()

# Load the engine
engine = load_engine()

# ==========================================
# UI: SIDEBAR PENGATURAN
# ==========================================
with st.sidebar:
    st.image("docs/WCP_Logo-01.svg", use_container_width=True)

    st.divider()

    st.header("⚙️ Pengaturan Pencarian")
    st.markdown("Atur seberapa pintar AI mencari data di database.")

    st.divider()
    

    # Slider untuk mengatur bobot Keyword (BM25)
    # Format: st.slider(label, min_value, max_value, default_value, step)
    keyword_val = st.slider(
        "Porsi Keyword Persis (BM25)", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.1, 
        step=0.1
    )
    
    # Kalkulasi otomatis untuk Semantic
    semantic_val = 1.0 - keyword_val
    
    # Tampilkan persentase agar user/tim mudah membacanya
    st.info(f"🔍 **Komposisi Saat Ini:**\n- Keyword: {int(keyword_val*100)}%\n- Makna Kalimat: {int(semantic_val*100)}%")

    st.markdown("""
    **Kelompok:** *WCP*  
    **Domain:** *http://localhost:8501*  
    **LLM:** *Llama3.2*  
    **Vector DB:** ChromaDB  
    **Embedding:** nomic-embed-text
    """)
    
# Update bobot di dalam engine setiap kali slider digeser
engine.update_retriever_weights(keyword_val)

# Management UI messages Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

    # --- BAGIAN PERKENALAN OTOMATIS ---
    intro_text = (
        "Halo! Saya adalah **World Cup Analyst AI**. 🏆\n\n"
        "Saya siap membantu memberikan analisis mendalam "
        "terkait dunia sepak bola. "
        "Ada yang ingin kamu tanyakan?"
    )
    # Simpan pesan perkenalan ke dalam chat history UI
    st.session_state.messages.append({"role": "assistant", "content": intro_text})

# Menampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Redraw citations if they exist
        if "citations" in message and message["citations"]:
            with st.expander("Sources"):
                for citation in message["citations"]:
                    st.write(citation)

# User Input Box
if prompt := st.chat_input("Ask a question about your document..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. Gunakan placeholder untuk streaming
        response_placeholder = st.empty()
        full_answer = ""
        context_docs = []

        # 2. Panggil engine dengan stream
        # Karena kita butuh context (sources), kita harus menangkap chunk stream-nya
        stream_generator = engine.ask(user_input=prompt, session_id="streamlit_user")
        
        # 3. Looping untuk menampilkan kata per kata
        # LangChain stream untuk retrieval chain biasanya mengirimkan dictionary
        for chunk in stream_generator:
            # Ambil potongan jawaban jika ada
            if "answer" in chunk:
                full_answer += chunk["answer"]
                response_placeholder.markdown(full_answer + "▌")
            
            # Simpan context untuk citation nanti (biasanya muncul di awal atau akhir stream)
            if "context" in chunk:
                context_docs = chunk["context"]

        # Hilangkan kursor "▌" setelah selesai
        response_placeholder.markdown(full_answer)

        # 4. Tampilkan Citations (Gunakan context_docs yang sudah ditangkap)
        unique_sources = set()
        for doc in context_docs:
            source_file = os.path.basename(doc.metadata.get('source', 'Unknown File'))
            chunk_id = doc.metadata.get('chunk_id', 'Unknown Chunk')
            page_num = doc.metadata.get('page')
            
            label = f"📄 **File:** {source_file} | **Chunk:** {chunk_id}"
            if page_num is not None:
                label += f" | **Page:** {page_num}"
            unique_sources.add(label)

        if unique_sources:
            with st.expander("Sources"):
                for source in unique_sources:
                    st.write(source)

    # 5. Simpan ke Session State
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_answer,
        "citations": list(unique_sources)
    })