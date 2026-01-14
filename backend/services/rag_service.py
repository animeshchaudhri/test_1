from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from config.settings import Config
import pandas as pd
import os

class RAGService:
    """RAG (Retrieval-Augmented Generation) Service for product search"""
    
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.qdrant_client = QdrantClient(
            url=Config.QDRANT_URL,
            api_key=Config.QDRANT_API_KEY
        )
        self.collection_name = Config.QDRANT_COLLECTION_NAME
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Ensure the Qdrant collection exists"""
        try:
            collections = self.qdrant_client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=Config.EMBEDDING_DIMENSION,
                        distance=Distance.COSINE
                    )
                )
                print(f"✅ Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            print(f"⚠️ Could not connect to Qdrant: {e}")
            print("⚠️ RAG features will be limited without Qdrant")
    
    def get_embedding(self, text):
        """Generate embedding for text using OpenAI"""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=Config.OPENAI_EMBEDDING_MODEL
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def index_products(self, products):
        """Index products into Qdrant vector store"""
        try:
            points = []
            
            for product in products:
                # Create searchable text from product attributes
                search_text = f"{product['productDisplayName']} {product['articleType']} {product['baseColour']} {product['usage']} {product['gender']}"
                
                embedding = self.get_embedding(search_text)
                if embedding:
                    point = PointStruct(
                        id=int(product['id']),
                        vector=embedding,
                        payload={
                            "id": int(product['id']),
                            "name": product['productDisplayName'],
                            "articleType": product['articleType'],
                            "color": product['baseColour'],
                            "price": int(product['price']),
                            "gender": product['gender'],
                            "usage": product['usage'],
                            "season": product['season'],
                            "sizes": product['sizes'].split(',') if isinstance(product['sizes'], str) else product['sizes'],
                            "stock": int(product['stock']),
                            "search_text": search_text
                        }
                    )
                    points.append(point)
            
            if points:
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                print(f"✅ Indexed {len(points)} products into Qdrant")
                return len(points)
            
            return 0
        except Exception as e:
            print(f"Error indexing products: {e}")
            return 0
    
    def search_products(self, query, limit=10):
        """Search for products using semantic search"""
        try:
            # Generate embedding for the query
            query_embedding = self.get_embedding(query)
            
            if not query_embedding:
                return []
            
            # Search in Qdrant
            results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit
            )
            
            # Format results
            products = []
            for result in results:
                product = result.payload
                product['relevance_score'] = result.score
                products.append(product)
            
            return products
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
    
    def get_context_for_query(self, query, limit=5):
        """Get relevant product context for LLM generation"""
        products = self.search_products(query, limit=limit)
        
        if not products:
            return "No relevant products found."
        
        context = "Here are the relevant products:\n\n"
        for i, product in enumerate(products, 1):
            context += f"{i}. {product['name']}\n"
            context += f"   - Color: {product['color']}\n"
            context += f"   - Price: ₹{product['price']}\n"
            context += f"   - Sizes: {', '.join(product['sizes'])}\n"
            context += f"   - In Stock: {'Yes' if product['stock'] > 0 else 'No'}\n\n"
        
        return context
