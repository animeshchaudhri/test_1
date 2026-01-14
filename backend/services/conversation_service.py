from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config.settings import Config
from services.rag_service import RAGService
import json
from datetime import datetime

class ConversationService:
    """Service for managing conversational AI interactions"""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.qdrant_client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY
        )
        self.memory_collection = Config.QDRANT_MEMORY_COLLECTION
        self.rag_service = RAGService()
        self._ensure_memory_collection()
        
        # Conversation sessions (in-memory for POC)
        self.sessions = {}
    
    def _ensure_memory_collection(self):
        """Ensure the memory collection exists"""
        try:
            collections = self.qdrant_client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.memory_collection not in collection_names:
                self.qdrant_client.create_collection(
                    collection_name=self.memory_collection,
                    vectors_config=VectorParams(
                        size=Config.EMBEDDING_DIMENSION,
                        distance=Distance.COSINE
                    )
                )
                print(f"✅ Created memory collection: {self.memory_collection}")
        except Exception as e:
            print(f"⚠️ Could not create memory collection: {e}")
    
    def get_session_context(self, session_id):
        """Get conversation context for a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'messages': [],
                'last_products': [],
                'current_selection': None
            }
        return self.sessions[session_id]
    
    def detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['find', 'search', 'show', 'looking for', 'want']):
            return 'search'
        elif any(word in message_lower for word in ['size', 'available', 'stock']):
            return 'check_availability'
        elif any(word in message_lower for word in ['more', 'different', 'other', 'another']):
            return 'refine_search'
        elif any(word in message_lower for word in ['order', 'buy', 'purchase', 'checkout']):
            return 'order'
        elif any(word in message_lower for word in ['color', 'colour']):
            return 'color_query'
        else:
            return 'general'
    
    def process_message(self, message, session_id='default'):
        """Process user message and generate response"""
        try:
            context = self.get_session_context(session_id)
            intent = self.detect_intent(message)
            
            # Add user message to context
            context['messages'].append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Handle different intents
            if intent == 'search':
                return self._handle_search(message, context)
            elif intent == 'check_availability':
                return self._handle_availability(message, context)
            elif intent == 'refine_search':
                return self._handle_refinement(message, context)
            elif intent == 'order':
                return self._handle_order(message, context)
            elif intent == 'color_query':
                return self._handle_color_query(message, context)
            else:
                return self._handle_general(message, context)
                
        except Exception as e:
            print(f"Error processing message: {e}")
            return {
                'message': "I'm sorry, I encountered an error. Please try again.",
                'intent': 'error',
                'products': []
            }
    
    def _handle_search(self, message, context):
        """Handle search intent"""
        # Use RAG to find products
        products = self.rag_service.search_products(message, limit=5)
        context['last_products'] = products
        
        if products:
            response = f"I found {len(products)} products for you! "
            response += f"The first one is {products[0]['name']} "
            response += f"in {products[0]['color']} for ₹{products[0]['price']}. "
            response += "Would you like to know more about any of these?"
        else:
            response = "I couldn't find any products matching your search. Could you try describing what you're looking for differently?"
        
        context['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'message': response,
            'intent': 'search',
            'products': products
        }
    
    def _handle_availability(self, message, context):
        """Handle size/availability queries"""
        last_products = context.get('last_products', [])
        
        if not last_products:
            return {
                'message': "Could you first tell me what product you're interested in?",
                'intent': 'check_availability',
                'products': []
            }
        
        # Extract size from message
        sizes = ['xs', 's', 'm', 'l', 'xl', 'xxl']
        requested_size = None
        for size in sizes:
            if size in message.lower():
                requested_size = size.upper()
                break
        
        product = last_products[0]
        
        if requested_size:
            if requested_size in product['sizes']:
                response = f"Yes! {product['name']} is available in {requested_size}. Would you like me to add it to your cart?"
                context['current_selection'] = {
                    'product': product,
                    'size': requested_size
                }
            else:
                available_sizes = ', '.join(product['sizes'])
                response = f"Sorry, {product['name']} is not available in {requested_size}. It's available in: {available_sizes}"
        else:
            available_sizes = ', '.join(product['sizes'])
            response = f"{product['name']} is available in sizes: {available_sizes}. Which size would you like?"
        
        context['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'message': response,
            'intent': 'check_availability',
            'products': [product]
        }
    
    def _handle_refinement(self, message, context):
        """Handle refinement requests (show more, different colors, etc.)"""
        last_query = None
        for msg in reversed(context['messages']):
            if msg['role'] == 'user' and msg['content']:
                last_query = msg['content']
                break
        
        if last_query:
            products = self.rag_service.search_products(last_query, limit=10)
            # Skip the first ones if we've already shown them
            skip = len(context.get('last_products', []))
            products = products[skip:skip+5]
            context['last_products'] = products
            
            if products:
                response = f"Here are {len(products)} more options! "
                response += f"How about {products[0]['name']} in {products[0]['color']}?"
            else:
                response = "I've shown you all the products I have. Would you like to search for something else?"
        else:
            response = "What would you like to see more of?"
        
        context['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'message': response,
            'intent': 'refine_search',
            'products': products if products else []
        }
    
    def _handle_order(self, message, context):
        """Handle order placement"""
        current_selection = context.get('current_selection')
        
        if current_selection:
            response = f"Great! I'll add {current_selection['product']['name']} "
            response += f"in size {current_selection['size']} to your cart. "
            response += "Please proceed to checkout to complete your order."
        else:
            response = "Please select a product and size first, then I can help you place the order."
        
        context['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'message': response,
            'intent': 'order',
            'products': [current_selection['product']] if current_selection else []
        }
    
    def _handle_color_query(self, message, context):
        """Handle color-related queries"""
        last_products = context.get('last_products', [])
        
        if not last_products:
            return self._handle_general(message, context)
        
        # Check if asking about more colors
        product_name = last_products[0]['name'].split()[0]  # Get brand/type
        
        # Search for similar products
        query = f"{product_name} different colors"
        products = self.rag_service.search_products(query, limit=5)
        context['last_products'] = products
        
        if len(products) > 1:
            colors = [p['color'] for p in products[:3]]
            response = f"Yes! I found it in {', '.join(colors)}. Which color would you prefer?"
        else:
            response = f"Currently, {last_products[0]['name']} is only available in {last_products[0]['color']}."
        
        context['messages'].append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'message': response,
            'intent': 'color_query',
            'products': products
        }
    
    def _handle_general(self, message, context):
        """Handle general queries using GPT"""
        try:
            # Get conversation history
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful fashion shopping assistant. Be friendly, concise, and help users find products they'll love."
                }
            ]
            
            # Add recent conversation history
            for msg in context['messages'][-5:]:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages,
                max_tokens=150
            )
            
            assistant_message = response.choices[0].message.content
            
            context['messages'].append({
                'role': 'assistant',
                'content': assistant_message,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'message': assistant_message,
                'intent': 'general',
                'products': []
            }
        except Exception as e:
            print(f"Error in general handler: {e}")
            return {
                'message': "I'm here to help you shop! You can ask me to find products, check sizes, or learn more about items.",
                'intent': 'general',
                'products': []
            }
