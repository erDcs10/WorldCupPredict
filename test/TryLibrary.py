try:
    from langchain_classic.chains.retrieval import create_retrieval_chain
    from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain
    print("✅ Imports are working perfectly!")
except ImportError as e:
    print(f"❌ Error: {e}")