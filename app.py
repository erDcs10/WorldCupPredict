import streamlit as st
import os

from src.query import RAGQueryEngine


# Page Setup
st.set_page_config(page_title="Seputar Piala Dunia 2026", page_icon="🦙", layout="centered")
st.title("Seputar Piala Dunia 2026")

# Initialize the Backend Engine ONCE using Streamlit Cache
@st.cache_resource
def load_engine():
    try:
        return RAGQueryEngine()
    except FileNotFoundError as e:
        st.error(f"❌ {e}")
        st.stop()

# Load the engine
engine = load_engine()

# Manage UI message state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Redraw previous chat bubbles
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