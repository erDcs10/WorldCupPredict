# 1. Document Loaders & Splitters
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 2. Ollama & Vector Store (Note the new specific packages)
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

# 3. Chains (Using retrieval-specific sub-paths)
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# 4. Core logic & History
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

import os

# ==========================================
# 1. SETUP & PDF LOADER (INDEXING)
# ==========================================
llm = ChatOllama(model="llama3.2", temperature=0)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load a local PDF (Replace with your actual PDF path)
# PyPDFLoader automatically adds 'source' and 'page' to the metadata
pdf_path = "D:\Projects\Python\World_Cup_Predict\data\Piala_Dunia_FIFA_2026.pdf" 
loader = PyPDFLoader(pdf_path)
docs = loader.load()

# Split the document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Add chunk IDs manually to the metadata so we know exactly which chunk was used
for i, split in enumerate(splits):
    split.metadata['chunk_id'] = i

print(f"Number of documents loaded: {len(docs)}")
print(f"Number of chunks created: {len(splits)}")

if len(splits) == 0:
    print("Error: No text was found to embed! Check your file path or document content.")
    exit()

# Create Vector DB
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever()

# ==========================================
# 2. HISTORY-AWARE RETRIEVER (QUERY)
# ==========================================
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# ==========================================
# 3. QUESTION-ANSWERING CHAIN
# ==========================================
# Notice we added an instruction to rely strictly on the context
qa_system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer the question. "
    "If the answer is not in the context, don't say 'I cannot find the answer in the provided documents.' "
    "Keep the answer concise."
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# ==========================================
# 4. MEMORY MANAGEMENT
# ==========================================
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer", 
)

# ==========================================
# 5. CHAT LOOP WITH CITATION EXTRACTION
# ==========================================
print("\n--- RAG Chatbot with Citations Ready! (Type 'exit' to quit) ---")
config = {"configurable": {"session_id": "session_1"}}

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["exit", "quit"]:
        break
        
    # Invoke the chain
    response = conversational_rag_chain.invoke(
        {"input": user_input},
        config=config
    )
    
    # 1. Print the AI's Answer
    print(f"\nAI: {response['answer']}\n")
    
    # 2. Extract and Print the Citations
    print("--- Sources Used ---")
    
    # Use a set to prevent printing the exact same page twice if multiple 
    # chunks from the same page were retrieved.
    unique_sources = set()
    
    # The retrieved documents are stored in the 'context' key
    for doc in response['context']:
        # Extract metadata
        source_file = os.path.basename(doc.metadata.get('source', 'Unknown File'))
        page_num = doc.metadata.get('page', 'Unknown Page')
        chunk_id = doc.metadata.get('chunk_id', 'Unknown Chunk')
        
        # Format the citation string
        citation = f"📄 File: {source_file} | Page: {page_num} | Chunk: {chunk_id}"
        unique_sources.add(citation)
        
    # Print the unique citations
    for source in unique_sources:
        print(source)
    print("--------------------")