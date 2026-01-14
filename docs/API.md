# API Documentation

## Base URL

Development: `http://localhost:5000`  
Production: `https://your-domain.com`

## Authentication

This POC does not require authentication. For production, implement:
- API key authentication
- JWT tokens
- OAuth 2.0

---

## Endpoints

### Health Check

Check if the API is running.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "message": "Voice E-Commerce API is running"
}
```

**Status Codes**:
- `200`: API is healthy

---

### Search Products

Search for products using text or voice input with semantic understanding.

**Endpoint**: `POST /api/search`

**Request Body**:
```json
{
  "query": "traditional dresses"
}
```

**Response**:
```json
{
  "success": true,
  "query": "traditional dresses",
  "products": [
    {
      "id": 2,
      "name": "Libas Women Pink Kurta",
      "articleType": "Kurtas",
      "color": "Pink",
      "price": 2499,
      "gender": "Women",
      "usage": "Ethnic",
      "season": "Summer",
      "sizes": ["XS", "S", "M", "L", "XL"],
      "stock": 30,
      "relevance_score": 0.89
    }
  ]
}
```

**Status Codes**:
- `200`: Success
- `400`: Missing query parameter
- `500`: Server error

**Example cURL**:
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "blue kurtas"}'
```

---

### Conversation

Handle conversational queries with context and multi-turn support.

**Endpoint**: `POST /api/conversation`

**Request Body**:
```json
{
  "message": "Find me blue kurtas",
  "session_id": "user123"
}
```

**Parameters**:
- `message` (required): User's conversational message
- `session_id` (optional): Session identifier for context. Default: "default"

**Response**:
```json
{
  "success": true,
  "response": "I found 5 blue kurtas. The first is Vishudh Women Blue Silk Kurta at ₹2,499. Would you like to know more?",
  "intent": "search",
  "products": [
    {
      "id": 6,
      "name": "Vishudh Women Blue Silk Kurta",
      "color": "Blue",
      "price": 2499,
      "sizes": ["S", "M", "L", "XL"],
      "stock": 20
    }
  ]
}
```

**Intent Types**:
- `search`: Product discovery
- `check_availability`: Size/stock queries
- `refine_search`: Show more options
- `order`: Place order
- `color_query`: Color variations
- `general`: General conversation

**Status Codes**:
- `200`: Success
- `400`: Missing message
- `500`: Server error

**Example Conversation Flow**:

1. **Initial Search**:
```bash
curl -X POST http://localhost:5000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Find traditional dresses",
    "session_id": "session_001"
  }'
```

2. **Follow-up**:
```bash
curl -X POST http://localhost:5000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Is it available in medium?",
    "session_id": "session_001"
  }'
```

3. **Refinement**:
```bash
curl -X POST http://localhost:5000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me more colors",
    "session_id": "session_001"
  }'
```

---

### Get Product

Retrieve details of a specific product by ID.

**Endpoint**: `GET /api/products/:id`

**Parameters**:
- `id` (path): Product ID

**Response**:
```json
{
  "success": true,
  "product": {
    "id": 6,
    "gender": "Women",
    "masterCategory": "Apparel",
    "subCategory": "Topwear",
    "articleType": "Kurtas",
    "baseColour": "Blue",
    "season": "Summer",
    "year": 2012,
    "usage": "Ethnic",
    "productDisplayName": "Vishudh Women Blue Silk Kurta",
    "price": 2499,
    "stock": 20,
    "sizes": "S,M,L,XL"
  }
}
```

**Status Codes**:
- `200`: Success
- `404`: Product not found
- `500`: Server error

**Example cURL**:
```bash
curl http://localhost:5000/api/products/6
```

---

### Create Order

Place a new order with items and customer information.

**Endpoint**: `POST /api/orders`

**Request Body**:
```json
{
  "items": [
    {
      "id": 6,
      "name": "Vishudh Women Blue Silk Kurta",
      "price": 2499,
      "size": "M",
      "quantity": 1
    }
  ],
  "customer_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "address": "123 Main Street, Apartment 4B",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001"
  }
}
```

**Response**:
```json
{
  "success": true,
  "order_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Order placed successfully"
}
```

**Status Codes**:
- `200`: Success
- `400`: Missing required fields
- `500`: Server error

**Example cURL**:
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "id": 6,
        "name": "Blue Silk Kurta",
        "price": 2499,
        "size": "M",
        "quantity": 1
      }
    ],
    "customer_info": {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "9876543210",
      "address": "123 Main St",
      "city": "Mumbai",
      "state": "Maharashtra",
      "pincode": "400001"
    }
  }'
```

---

### Initialize Data

Load product data from CSV into the system (MongoDB and Qdrant).

**Endpoint**: `POST /api/init-data`

**Response**:
```json
{
  "success": true,
  "message": "Data initialized successfully",
  "products_loaded": 45
}
```

**Status Codes**:
- `200`: Success
- `500`: Server error

**Example cURL**:
```bash
curl -X POST http://localhost:5000/api/init-data
```

**Note**: This endpoint should be called once after initial setup to populate the database.

---

## Error Responses

All endpoints may return error responses in this format:

```json
{
  "error": "Error message describing what went wrong"
}
```

**Common Error Codes**:
- `400 Bad Request`: Invalid or missing parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error

---

## Rate Limiting

**Current**: No rate limiting (POC)  
**Production**: Implement rate limiting:
- 100 requests per minute per IP
- 1000 requests per hour per session

---

## CORS

**Allowed Origins**:
- Development: `http://localhost:3000`
- Production: Configure via `FRONTEND_URL` environment variable

**Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS  
**Allowed Headers**: Content-Type, Authorization

---

## WebSocket Support (Future)

For real-time features:
- Live product updates
- Real-time conversation streaming
- Order status notifications

**Endpoint**: `ws://localhost:5000/ws`

---

## Data Models

### Product
```typescript
{
  id: number,
  gender: string,
  masterCategory: string,
  subCategory: string,
  articleType: string,
  baseColour: string,
  season: string,
  year: number,
  usage: string,
  productDisplayName: string,
  price: number,
  stock: number,
  sizes: string  // Comma-separated
}
```

### Order
```typescript
{
  order_id: string,
  items: Array<{
    id: number,
    name: string,
    price: number,
    size: string,
    quantity: number
  }>,
  customer_info: {
    name: string,
    email: string,
    phone: string,
    address: string,
    city: string,
    state: string,
    pincode: string
  },
  total: number,
  status: string,
  created_at: string,
  updated_at: string
}
```

---

## Conversation Context

The conversation service maintains context per session:

```typescript
{
  messages: Array<{
    role: "user" | "assistant",
    content: string,
    timestamp: string
  }>,
  last_products: Array<Product>,
  current_selection: {
    product: Product,
    size: string
  }
}
```

**Session Lifecycle**:
1. First message creates session
2. Context maintained in memory
3. Session expires after inactivity (TODO)

---

## Best Practices

### For Search
- Keep queries natural and conversational
- Use specific terms for better results
- Combine filters: "blue kurtas for women"

### For Conversations
- Use consistent `session_id` for context
- Follow up on previous queries
- Be specific about requirements

### For Orders
- Validate customer info on frontend
- Include all required fields
- Store order_id for tracking

---

## Code Examples

### JavaScript/React

```javascript
// Search Products
async function searchProducts(query) {
  const response = await fetch('http://localhost:5000/api/search', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  return await response.json();
}

// Conversation
async function sendMessage(message, sessionId) {
  const response = await fetch('http://localhost:5000/api/conversation', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      message, 
      session_id: sessionId 
    })
  });
  return await response.json();
}

// Create Order
async function createOrder(items, customerInfo) {
  const response = await fetch('http://localhost:5000/api/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      items, 
      customer_info: customerInfo 
    })
  });
  return await response.json();
}
```

### Python

```python
import requests

# Search Products
def search_products(query):
    response = requests.post(
        'http://localhost:5000/api/search',
        json={'query': query}
    )
    return response.json()

# Conversation
def send_message(message, session_id='default'):
    response = requests.post(
        'http://localhost:5000/api/conversation',
        json={
            'message': message,
            'session_id': session_id
        }
    )
    return response.json()

# Create Order
def create_order(items, customer_info):
    response = requests.post(
        'http://localhost:5000/api/orders',
        json={
            'items': items,
            'customer_info': customer_info
        }
    )
    return response.json()
```

---

## Testing

### Health Check
```bash
curl http://localhost:5000/health
```

### Search Flow
```bash
# 1. Search
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "blue kurtas"}'

# 2. Get Product Details
curl http://localhost:5000/api/products/6
```

### Conversation Flow
```bash
# 1. Initial query
curl -X POST http://localhost:5000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Find traditional dresses", "session_id": "test123"}'

# 2. Follow-up
curl -X POST http://localhost:5000/api/conversation \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me more colors", "session_id": "test123"}'
```

---

## Support

For issues or questions:
- Check the main README.md
- Review docs/SETUP_GUIDE.md
- See docs/ARCHITECTURE.md for technical details

---

**API Version**: 1.0  
**Last Updated**: 2026-01-14  
**Status**: POC
