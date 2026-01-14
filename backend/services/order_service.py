from pymongo import MongoClient
from config.settings import Config
from datetime import datetime
import uuid

class OrderService:
    """Service for managing orders"""
    
    def __init__(self):
        try:
            self.mongo_client = MongoClient(Config.MONGODB_URI)
            self.db = self.mongo_client[Config.MONGODB_DATABASE]
            self.orders_collection = self.db['orders']
            print("✅ OrderService connected to MongoDB")
        except Exception as e:
            print(f"⚠️ MongoDB connection error: {e}")
            self.mongo_client = None
            self.db = None
            self.orders_collection = None
    
    def create_order(self, items, customer_info):
        """Create a new order"""
        try:
            if self.orders_collection is None:
                # Fallback for when MongoDB is not available
                order_id = str(uuid.uuid4())
                return {
                    'order_id': order_id,
                    'success': True,
                    'message': 'Order created (in-memory only)'
                }
            
            # Calculate total
            total = sum(item.get('price', 0) for item in items)
            
            order = {
                'order_id': str(uuid.uuid4()),
                'items': items,
                'customer_info': customer_info,
                'total': total,
                'status': 'pending',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            result = self.orders_collection.insert_one(order)
            
            return {
                'order_id': order['order_id'],
                'success': True,
                'message': 'Order created successfully'
            }
            
        except Exception as e:
            print(f"Error creating order: {e}")
            return {
                'order_id': None,
                'success': False,
                'error': str(e)
            }
    
    def get_order(self, order_id):
        """Get order by ID"""
        try:
            if self.orders_collection is None:
                return None
            
            order = self.orders_collection.find_one({'order_id': order_id})
            
            if order:
                order['_id'] = str(order['_id'])
            
            return order
        except Exception as e:
            print(f"Error getting order: {e}")
            return None
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        try:
            if self.orders_collection is None:
                return False
            
            result = self.orders_collection.update_one(
                {'order_id': order_id},
                {
                    '$set': {
                        'status': status,
                        'updated_at': datetime.now().isoformat()
                    }
                }
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating order: {e}")
            return False
