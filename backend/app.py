from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from services.rag_service import RAGService
from services.conversation_service import ConversationService
from services.product_service import ProductService
from services.order_service import OrderService

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL", "http://localhost:3000")}})

# Initialize services
rag_service = RAGService()
conversation_service = ConversationService()
product_service = ProductService()
order_service = OrderService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Voice E-Commerce API is running"})

@app.route('/api/search', methods=['POST'])
def search_products():
    """
    Search products using text or voice input
    Uses RAG for semantic search
    """
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Use RAG to find relevant products
        results = rag_service.search_products(query)
        
        return jsonify({
            "success": True,
            "query": query,
            "products": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversation', methods=['POST'])
def handle_conversation():
    """
    Handle conversational queries using LLM agent
    Maintains context and memory
    """
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Process conversation with context
        response = conversation_service.process_message(
            message=user_message,
            session_id=session_id
        )
        
        return jsonify({
            "success": True,
            "response": response['message'],
            "intent": response.get('intent'),
            "products": response.get('products', [])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product details"""
    try:
        product = product_service.get_product_by_id(product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        return jsonify({
            "success": True,
            "product": product
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.json
        
        required_fields = ['items', 'customer_info']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        order = order_service.create_order(
            items=data['items'],
            customer_info=data['customer_info']
        )
        
        return jsonify({
            "success": True,
            "order_id": order['order_id'],
            "message": "Order placed successfully"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/init-data', methods=['POST'])
def initialize_data():
    """
    Initialize the system with product data
    Load CSV and populate vector store
    """
    try:
        result = product_service.load_products_from_csv()
        
        return jsonify({
            "success": True,
            "message": "Data initialized successfully",
            "products_loaded": result['count']
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
    print(f"🚀 Voice E-Commerce API starting on port {port}")
    print(f"📊 Frontend URL: {os.getenv('FRONTEND_URL', 'http://localhost:3000')}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
