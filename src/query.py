import os
import langchain
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.retrievers.multi_query import MultiQueryRetriever # Tambahkan import ini
langchain.debug = True

class RAGQueryEngine:
    def __init__(self, persist_dir="./chroma_db"):
        if not os.path.exists(persist_dir):
            raise FileNotFoundError("Database not found! Please run indexer.py first.")
        
        # 1. SETUP
        self.llm = ChatOllama(model="llama3.2", temperature=0)
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        
        # 2. RETRIEVAL SETUP
        self.vectorstore = Chroma(
            persist_directory=persist_dir, 
            embedding_function=self.embeddings
        )
        
        # --- MODIFIKASI DISINI: Bungkus retriever dasar dengan MultiQueryRetriever ---
        base_retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        self.retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever, 
            llm=self.llm
        )
        # ----------------------------------------------------------------------------

        # 3. PROMPTING & CHAINS
        contextualize_q_system_prompt = (
            "You are a strict query rewriter. Look at the chat history and the user's latest question. "
            "If the user's latest question uses pronouns (it, they, he, she) or refers to the previous topic, "
            "rewrite it into a clear, standalone question. "
            "If the latest question is ALREADY clear, return it word-for-word. "
            "ONLY output the final question."
        )

        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])

        # history_aware_retriever sekarang menggunakan MultiQueryRetriever di dalamnya
        history_aware_retriever = create_history_aware_retriever(
            self.llm, self.retriever, contextualize_q_prompt
        )

        # QA Prompt
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a World Cup Analyst. Use the retrieved context to answer."),
            ("system", "CONTEXT: {context}"),
            MessagesPlaceholder("chat_history"), 
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        # 4. MEMORY & RUNNABLE
        self.store = {}
        self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        
        # Keep only the last 10 messages to prevent "poisoning"
        if len(self.store[session_id].messages) > 10:
            self.store[session_id].messages = self.store[session_id].messages[-10:]
            
        return self.store[session_id]

    # ==========================================
    # STEP 4: SUBMIT TO LLM (Invocation)
    # ==========================================
    def ask(self, user_input: str, session_id: str = "default_session"):
    # Gunakan .stream untuk mendapatkan generator
        return self.conversational_rag_chain.stream(
            {"input": user_input},
            config={"configurable": {"session_id": session_id}}
        )