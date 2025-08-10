import os
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm import tqdm

# Quick ingestion for faster startup
def quick_embed():
    """
    Quick embedding of only a few key documents for fast startup
    """
    print("🚀 Starting QUICK ingestion process...")
    
    # Select only a few key documents for quick processing
    quick_files = [
        "dataset/Blacks-Law-Dictionary-8th-Edition.pdf",
        "dataset/REYES - Criminal Law Reviewer (1968).pdf",
        "dataset/NACHURA - POLITICAL LAW (2014).pdf"
    ]
    
    # Filter to only existing files
    existing_files = []
    for file in quick_files:
        if os.path.exists(file):
            existing_files.append(file)
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Not found: {file}")
    
    if not existing_files:
        print("📄 No quick files found, processing first available PDF...")
        # Find first available PDF
        for root, dirs, files in os.walk("dataset/"):
            for file in files:
                if file.endswith('.pdf'):
                    existing_files.append(os.path.join(root, file))
                    break
            if existing_files:
                break
    
    if not existing_files:
        print("❌ No PDF files found in dataset!")
        return
    
    print(f"📚 Processing {len(existing_files)} documents...")
    
    # Load documents
    all_documents = []
    for file_path in existing_files:
        try:
            print(f"📖 Loading: {os.path.basename(file_path)}")
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            # Limit pages per document for speed (first 20 pages only)
            if len(documents) > 20:
                documents = documents[:20]
                print(f"  → Limited to first 20 pages")
            
            all_documents.extend(documents)
            print(f"  → Loaded {len(documents)} pages")
        except Exception as e:
            print(f"  ❌ Error loading {file_path}: {str(e)}")
            continue
    
    if not all_documents:
        print("❌ No documents were successfully loaded!")
        return
    
    print(f"📄 Total pages loaded: {len(all_documents)}")
    
    # Split documents into smaller chunks
    print("✂️ Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Smaller chunks for faster processing
        chunk_overlap=50,
        length_function=len
    )
    
    texts = text_splitter.split_documents(all_documents)
    print(f"📝 Created {len(texts)} text chunks")
    
    # Create embeddings (using faster model)
    print("🧠 Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",  # Faster, smaller model
        model_kwargs={'device': 'cpu'}
    )
    
    # Create FAISS vector store
    print("💾 Creating vector database...")
    vectorstore = FAISS.from_documents(texts, embeddings)
    
    # Save the vector store
    if not os.path.exists("vectorstore"):
        os.makedirs("vectorstore")
    
    vectorstore.save_local("vectorstore/")
    print("✅ Vector database saved!")
    
    print("🎉 Quick ingestion completed successfully!")
    print("🚀 Your Law Chatbot is now ready!")

if __name__ == "__main__":
    quick_embed()
