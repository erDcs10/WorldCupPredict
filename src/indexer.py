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

# Define where your data lives
DATA_FOLDER = "./data"
PERSIST_DIR = "./chroma_db"

# Create the data folder if it doesn't exist yet
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)
    print(f"Created '{DATA_FOLDER}' folder. Please put your files in there and run again.")
    exit()

# Add any websites you want to scrape here
WEBSITES_TO_SCRAPE = [
    "https://www.fifa.com/en/world-rankings",
]

# ==========================================
# 2. FILE SCANNER & LOADER
# ==========================================
all_docs = []
print(f"\nScanning '{DATA_FOLDER}' for documents...")

# Loop through every file in the data folder
for filename in os.listdir(DATA_FOLDER):
    file_path = os.path.join(DATA_FOLDER, filename)
    
    # Skip directories, only process files
    if not os.path.isfile(file_path):
        continue

    print(f"Loading: {filename}...")
    
    try:
        # Check the extension and use the correct loader
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

# Load Websites
if WEBSITES_TO_SCRAPE:
    print("\nScraping websites...")
    for url in WEBSITES_TO_SCRAPE:
        print(f"Loading: {url}...")
        try:
            loader = WebBaseLoader(url)
            all_docs.extend(loader.load())
        except Exception as e:
             print(f"  -> ❌ Error loading {url}: {e}")

# Check if we actually loaded anything
if not all_docs:
    print("\n❌ No valid documents were found to process! Exiting.")
    exit()

print(f"\n✅ Successfully loaded {len(all_docs)} total document pages/rows.")

# ==========================================
# 3. SPLIT AND EMBED
# ==========================================
print("Splitting text into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(all_docs)

# Add chunk IDs for precise citations
for i, split in enumerate(splits):
    split.metadata['chunk_id'] = i

print(f"Generated {len(splits)} chunks. Saving to Vector DB...")

vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings,
    persist_directory=PERSIST_DIR
)

print(f"\n🎉 Indexing complete! Database saved to '{PERSIST_DIR}'.")