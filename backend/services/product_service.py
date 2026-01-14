from pymongo import MongoClient
from config.settings import Config
import pandas as pd
import os

class ProductService:
    """Service for managing product data"""
    
    def __init__(self):
        try:
            self.mongo_client = MongoClient(Config.MONGODB_URI)
            self.db = self.mongo_client[Config.MONGODB_DATABASE]
            self.products_collection = self.db['products']
            print("✅ Connected to MongoDB")
        except Exception as e:
            print(f"⚠️ MongoDB connection error: {e}")
            self.mongo_client = None
            self.db = None
            self.products_collection = None
    
    def load_products_from_csv(self):
        """Load products from CSV file and store in MongoDB and Qdrant"""
        try:
            # Find the CSV file
            csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data', 'sample_styles.csv')
            
            if not os.path.exists(csv_path):
                print(f"⚠️ CSV file not found at: {csv_path}")
                return {'count': 0, 'error': 'CSV file not found'}
            
            # Read CSV
            df = pd.read_csv(csv_path)
            products = df.to_dict('records')
            
            # Store in MongoDB if available
            if self.products_collection is not None:
                self.products_collection.delete_many({})  # Clear existing
                self.products_collection.insert_many(products)
                print(f"✅ Loaded {len(products)} products into MongoDB")
            
            # Index in Qdrant for RAG
            from services.rag_service import RAGService
            rag_service = RAGService()
            indexed_count = rag_service.index_products(products)
            
            return {
                'count': len(products),
                'indexed': indexed_count,
                'success': True
            }
            
        except Exception as e:
            print(f"Error loading products: {e}")
            return {'count': 0, 'error': str(e)}
    
    def get_product_by_id(self, product_id):
        """Get a specific product by ID"""
        try:
            if self.products_collection is None:
                return None
            
            product = self.products_collection.find_one({'id': product_id})
            
            if product:
                product['_id'] = str(product['_id'])  # Convert ObjectId to string
            
            return product
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    def get_all_products(self, skip=0, limit=50):
        """Get all products with pagination"""
        try:
            if self.products_collection is None:
                return []
            
            products = list(self.products_collection.find().skip(skip).limit(limit))
            
            for product in products:
                product['_id'] = str(product['_id'])
            
            return products
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    def search_products_text(self, query):
        """Simple text search in MongoDB"""
        try:
            if self.products_collection is None:
                return []
            
            # Create text index if it doesn't exist
            try:
                self.products_collection.create_index([
                    ('productDisplayName', 'text'),
                    ('articleType', 'text'),
                    ('baseColour', 'text')
                ])
            except:
                pass  # Index might already exist
            
            products = list(self.products_collection.find(
                {'$text': {'$search': query}}
            ).limit(20))
            
            for product in products:
                product['_id'] = str(product['_id'])
            
            return products
        except Exception as e:
            print(f"Error searching products: {e}")
            return []
