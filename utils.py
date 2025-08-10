# Importing Dependencies
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Set the Google API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyBPjldpvUwIH5HjcL7k35Z6AjQ6AI6nQkY'

# Faiss Index Path
FAISS_INDEX = "vectorstore/"

# Custom prompt template for Gemini
custom_prompt_template = """You are a knowledgeable legal assistant. Use the provided context to answer legal questions accurately and comprehensively.

Context: {context}

Question: {query}

Please provide a clear, detailed answer based on the legal documents provided in the context. If the information is not available in the context, please state that clearly.

Answer:"""

# Return the custom prompt template
def set_custom_prompt_template():
    """
    Set the custom prompt template for the LLMChain
    """
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "query"])

    return prompt

# Return the LLM
def load_llm():
    """
    Load Google Gemini LLM
    """
    try:
        # Initialize Gemini model
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            max_output_tokens=1000,
            convert_system_message_to_human=True
        )
        
        print("✅ Gemini model initialized successfully!")
        return llm
    
    except Exception as e:
        print(f"❌ Error loading Gemini model: {str(e)}")
        return None

# Return the chain
def retrieval_qa_chain(llm, prompt, db):
    """
    Create a retrieval QA chain with Gemini
    """
    try:
        # Create the RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=db.as_retriever(search_kwargs={'k': 2}),
            return_source_documents=True,
            chain_type_kwargs={'prompt': prompt}
        )
        
        print("✅ QA Chain created successfully!")
        return qa_chain
        
    except Exception as e:
        print(f"❌ Error creating QA chain: {str(e)}")
        return None

# Return the chain
def qa_pipeline():
    """
    Create the QA pipeline
    """
    try:
        print("🔄 Initializing QA pipeline...")
        
        # Load the HuggingFace embeddings
        embeddings = HuggingFaceEmbeddings()
        print("✅ Embeddings loaded")

        # Load the index
        db = FAISS.load_local("vectorstore/", embeddings, allow_dangerous_deserialization=True)
        print("✅ Vector database loaded")

        # Load the LLM
        llm = load_llm()
        if llm is None:
            print("❌ Failed to load LLM")
            return None

        # Set the custom prompt template
        qa_prompt = set_custom_prompt_template()
        print("✅ Prompt template set")

        # Create the retrieval QA chain
        chain = retrieval_qa_chain(llm, qa_prompt, db)
        
        if chain is not None:
            print("✅ Law-GPT model loaded successfully!")
        
        return chain
        
    except Exception as e:
        print(f"❌ Error in qa_pipeline: {str(e)}")
        return None