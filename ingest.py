# Importing Dependencies
import os
import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Dataset Directory Path
DATASET = "dataset/"

# Faiss Index Path
FAISS_INDEX = "vectorstore/"

# Create Vector Store and Index
def embed_all():
    """
    Embed all files in the dataset directory
    """
    print("🚀 Starting document ingestion process...")
    
    # Get all PDF files recursively
    pdf_files = []
    for root, dirs, files in os.walk(DATASET):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    print(f"📚 Found {len(pdf_files)} PDF files to process")
    
    all_documents = []
    successful_files = 0
    failed_files = 0
    
    # Process each PDF individually
    for pdf_file in pdf_files:
        try:
            print(f"📖 Processing: {os.path.basename(pdf_file)}")
            loader = PyPDFLoader(pdf_file)
            documents = loader.load()
            all_documents.extend(documents)
            successful_files += 1
            print(f"✅ Successfully loaded {len(documents)} pages from {os.path.basename(pdf_file)}")
        except Exception as e:
            failed_files += 1
            print(f"❌ Error loading {os.path.basename(pdf_file)}: {str(e)}")
            print("⏭️  Skipping this file and continuing...")
            continue
    
    if not all_documents:
        print("❌ No documents were successfully loaded!")
        return
    
    print(f"\n📊 Processing Summary:")
    print(f"✅ Successfully processed: {successful_files} files")
    print(f"❌ Failed to process: {failed_files} files")
    print(f"📄 Total pages loaded: {len(all_documents)}")
    
    print("\n🔄 Creating text chunks...")
    # Create the splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
    # Split the documents into chunks
    chunks = splitter.split_documents(all_documents)
    print(f"✂️  Created {len(chunks)} text chunks")
    
    print("\n🧠 Loading embeddings model...")
    # Load the embeddings
    embeddings = HuggingFaceEmbeddings()
    
    print("🏗️  Creating vector store...")
    # Create the vector store
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    print("💾 Saving vector store...")
    # Save the vector store
    vector_store.save_local(FAISS_INDEX)
    
    print(f"\n🎉 Successfully created vector store with {len(chunks)} chunks!")
    print(f"📂 Vector store saved to: {FAISS_INDEX}")
    print("✅ Ingestion process completed!")

if __name__ == "__main__":
    embed_all()