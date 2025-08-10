# Gemini-specific implementation for Law Chatbot
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Set the Google API key
os.environ['GOOGLE_API_KEY'] = ''

def load_gemini_llm():
    """
    Load Google Gemini LLM
    """
    try:
        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Updated to current available model
            temperature=0.7,
            max_output_tokens=1000,
            convert_system_message_to_human=True
        )
        
        print("✅ Gemini model initialized successfully!")
        return llm
    
    except Exception as e:
        print(f"❌ Error loading Gemini model: {str(e)}")
        return None

def create_gemini_qa_system():
    """
    Create a simplified QA system using Gemini
    """
    try:
        print("🔄 Initializing Gemini QA system...")
        
        # Load embeddings (same model as used in ingestion)
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",  # Same model as quick_ingest.py
            model_kwargs={'device': 'cpu'}
        )
        print("✅ Embeddings loaded")
        
        # Load vector database
        db = FAISS.load_local("vectorstore/", embeddings, allow_dangerous_deserialization=True)
        print("✅ Vector database loaded")
        
        # Load Gemini
        llm = load_gemini_llm()
        if llm is None:
            return None
            
        print("✅ Gemini QA system ready!")
        return {'llm': llm, 'db': db}
        
    except Exception as e:
        print(f"❌ Error creating Gemini QA system: {str(e)}")
        return None

def answer_question(qa_system, question):
    """
    Answer a question using Gemini and vector search
    """
    try:
        llm = qa_system['llm']
        db = qa_system['db']
        
        print(f"🔍 Searching for relevant documents for: {question}")
        # Search for relevant documents
        docs = db.similarity_search(question, k=3)
        print(f"📄 Found {len(docs)} relevant documents")
        
        # Combine retrieved context
        context = "\n\n".join([doc.page_content for doc in docs])
        print(f"📝 Context length: {len(context)} characters")
        
        # Create enhanced prompt for Gemini with better formatting instructions
        prompt = f"""You are an expert legal assistant with extensive knowledge of Indian law. Your responses should be professional, well-structured, and comprehensive.

**CONTEXT FROM LEGAL DOCUMENTS:**
{context}

**USER QUESTION:** {question}

**INSTRUCTIONS FOR YOUR RESPONSE:**
1. Provide a clear, comprehensive answer based on the legal documents
2. Use proper formatting with headers, bullet points, and sections where appropriate
3. Include relevant legal principles, definitions, and explanations
4. If citing specific laws or sections, format them clearly
5. Use professional legal language while remaining accessible
6. Structure your response with clear headings and subheadings
7. If information is incomplete, clearly state what additional information would be helpful

**Please provide your response in a well-formatted, professional manner:**"""

        print("🤖 Calling Gemini API...")
        # Get response from Gemini
        response = llm.invoke(prompt)
        
        if hasattr(response, 'content'):
            result = response.content
        else:
            result = str(response)
            
        print(f"✅ Gemini responded with {len(result)} characters")
        return result
            
    except Exception as e:
        error_msg = f"Error in answer_question: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        print(f"📋 Full traceback: {traceback.format_exc()}")
        return f"I apologize, but I encountered an error: {str(e)}"
