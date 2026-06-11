import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    Docx2txtLoader,
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# ==========================================
# 1. SETUP
# ==========================================
print("Initializing embedding model...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Define dimana data mentah kita berada dan dimana kita akan menyimpan database yang belum di-index
DATA_FOLDER = "./data"
PERSIST_DIR = "./chroma_db"

# Buat folder data jika belum ada, dan ingatkan user untuk memasukkan file sebelum lanjut
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created '{DATA_FOLDER}' folder. Please put your files in there and run again.")
    exit()

# Tambahkan daftar website yang ingin kita scrape (jika ada)
WEBSITES_TO_SCRAPE = [
    "https://www.fifa.com/en/world-rankings",
]

# ==========================================
# 2. FILE SCANNER & LOADER
# ==========================================
all_docs = []
print(f"\nScanning '{DATA_FOLDER}' for documents...")

# Loop semua file di folder data dan gunakan loader yang sesuai berdasarkan ekstensi file
for filename in os.listdir(DATA_FOLDER):
    file_path = os.path.join(DATA_FOLDER, filename)
    
    # Skip jika bukan file (misal folder atau shortcut)
    if not os.path.isfile(file_path):
        continue

    print(f"Loading: {filename}...")
    
    try:
        # Cek ekstensi file dan gunakan loader yang sesuai
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            all_docs.extend(loader.load())
            
        elif filename.endswith(".csv"):
            loader = CSVLoader(file_path, source_column="Nama_Negara") # Add source_column="X" here if needed
            all_docs.extend(loader.load())
            
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            all_docs.extend(loader.load())
            
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
            all_docs.extend(loader.load())
            
        else:
            print(f"  -> Skipping {filename}: Unsupported file format.")
            
    except Exception as e:
        print(f"  -> ❌ Error loading {filename}: {e}")

# Load websites jika ada
if WEBSITES_TO_SCRAPE:
    print("\nScraping websites...")
    for url in WEBSITES_TO_SCRAPE:
        print(f"Loading: {url}...")
        try:
            loader = WebBaseLoader(url)
            all_docs.extend(loader.load())
        except Exception as e:
             print(f"  -> ❌ Error loading {url}: {e}")

# Cek apakah ada dokumen yang berhasil dimuat
if not all_docs:
    print("\n❌ No valid documents were found to process! Exiting.")
    exit()

print(f"\n✅ Successfully loaded {len(all_docs)} total document pages/rows.")

# ==========================================
# 3. SPLIT AND EMBED
# ==========================================
print("Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(all_docs)

# Tambahkan metadata chunk_id untuk setiap split agar kita bisa melacaknya nanti
for i, split in enumerate(splits):
    split.metadata['chunk_id'] = i

print(f"Generated {len(splits)} chunks. Saving to Vector DB...")

vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings,
    persist_directory=PERSIST_DIR
)

print(f"\n🎉 Indexing complete! Database saved to '{PERSIST_DIR}'.")