from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from utils_gemini import create_gemini_qa_system, answer_question
import threading
import time

app = Flask(__name__)
CORS(app)

# Global variable to hold the Gemini QA system
qa_system = None
is_loading = False

def load_model():
    """Load the Gemini QA system in background"""
    global qa_system, is_loading
    is_loading = True
    try:
        qa_system = create_gemini_qa_system()
        is_loading = False
        print("✅ Law-GPT with Gemini loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        is_loading = False

# Start loading the model in background on startup
threading.Thread(target=load_model, daemon=True).start()

@app.route('/')
def index():
    """Serve the HTML frontend"""
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests from frontend"""
    global qa_system, is_loading
    
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'error': True,
                'response': 'Please provide a message.'
            })
        
        # Check if model is still loading
        if is_loading:
            return jsonify({
                'error': False,
                'response': 'The Gemini AI model is still loading. Please wait a moment and try again.',
                'loading': True
            })
        
        # Check if model is loaded
        if qa_system is None:
            return jsonify({
                'error': True,
                'response': 'The Gemini AI model failed to load. Please try restarting the server.'
            })
        
        # Get response from the Gemini QA system
        print(f"📝 User question: {message}")
        response = answer_question(qa_system, message)
        
        print(f"🤖 Gemini response: {response[:100]}...")
        
        return jsonify({
            'error': False,
            'response': response,
            'loading': False
        })
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({
            'error': True,
            'response': f'An error occurred: {str(e)}'
        })

@app.route('/status')
def status():
    """Check if the Gemini model is ready"""
    global qa_system, is_loading
    return jsonify({
        'model_loaded': qa_system is not None,
        'is_loading': is_loading,
        'status': 'loading' if is_loading else ('ready' if qa_system else 'error')
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Law-GPT API'})

if __name__ == '__main__':
    print("🚀 Starting Law-GPT Flask Server with Google Gemini...")
    print("📚 Loading Gemini AI model in background...")
    print("🌐 Frontend will be available at: http://localhost:5000")
    print("🔗 API endpoint: http://localhost:5000/chat")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
