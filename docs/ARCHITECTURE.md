# System Architecture Documentation

## Overview

This document describes the technical architecture of the Voice-Enabled Fashion E-Commerce POC.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React)                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Voice     │  │   Text      │  │   Product   │  │     Checkout        │ │
│  │   Search    │  │   Search    │  │   Display   │  │     Flow            │ │
│  │   Component │  │   Bar       │  │   Cards     │  │                     │ │
│  └──────┬──────┘  └──────┬──────┘  └─────────────┘  └─────────────────────┘ │
│         │                │                                                   │
│         └────────┬───────┘                                                   │
│                  ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │              Web Speech API (Browser)                                    ││
│  │              - Voice Input/Output                                        ││
│  │              - Text Transcription                                        ││
│  └──────────────────────────────┬──────────────────────────────────────────┘│
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                         HTTP/REST API
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (Python/Flask)                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    API LAYER (Flask Routes)                              ││
│  │  - /api/search          - /api/conversation                              ││
│  │  - /api/products/:id    - /api/orders                                    ││
│  │  - /api/init-data       - /health                                        ││
│  └──────────────────────────────┬──────────────────────────────────────────┘│
│                                  │                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    SERVICE LAYER                                         ││
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────────────┐││
│  │  │   RAG         │  │   Conversation│  │   Product / Order             │││
│  │  │   Service     │  │   Service     │  │   Services                    │││
│  │  └───────┬───────┘  └───────┬───────┘  └───────────────┬───────────────┘││
│  │          │                  │                          │                 ││
│  └──────────┼──────────────────┼──────────────────────────┼─────────────────┘│
│             │                  │                          │                  │
│  ┌──────────▼──────────────────▼──────────────────────────▼────────────────┐│
│  │                    EXTERNAL INTEGRATIONS                                 ││
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────────────┐││
│  │  │   OpenAI      │  │   OpenAI      │  │   LangChain (Optional)        │││
│  │  │   Embeddings  │  │   GPT-4o      │  │   Agent Framework             │││
│  │  │   (3072-dim)  │  │   Chat        │  │                               │││
│  │  └───────────────┘  └───────────────┘  └───────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────┬───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DATA LAYER                                        │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │
│  │      Qdrant         │  │      Qdrant         │  │     MongoDB         │  │
│  │   (Vector Store)    │  │   (Memory Store)    │  │   (Document Store)  │  │
│  │                     │  │                     │  │                     │  │
│  │   Collection:       │  │   Collection:       │  │   Collections:      │  │
│  │   fashion_products  │  │   conversation_     │  │   - products        │  │
│  │                     │  │     memory          │  │   - orders          │  │
│  │   Vectors:          │  │                     │  │   - users (future)  │  │
│  │   - 3072 dimensions │  │   Session context   │  │                     │  │
│  │   - COSINE distance │  │   User preferences  │  │   Full documents    │  │
│  │                     │  │   Conversation hist │  │   Flexible schema   │  │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Components

#### 1. Voice Search Component
- **Technology**: Web Speech API
- **Features**:
  - Real-time speech-to-text transcription
  - Visual feedback (pulsing animation)
  - Waveform visualization
  - Error handling
- **Browser Support**: Chrome, Edge, Safari (partial)

#### 2. Text Search Component
- **Features**:
  - Autocomplete (future)
  - Search history (future)
  - Real-time results

#### 3. Product Display
- **Features**:
  - Grid/List view
  - Image optimization
  - Size selection
  - Quick actions

#### 4. Conversation Panel
- **Features**:
  - Message history
  - Real-time updates
  - Context indicators
  - Fixed positioning

#### 5. Checkout Flow
- **Features**:
  - Multi-step form
  - Order summary
  - Address autofill
  - Success confirmation

### Backend Services

#### 1. RAG Service (`rag_service.py`)

**Purpose**: Semantic product search using embeddings

**Key Methods**:
- `get_embedding(text)`: Generate OpenAI embeddings
- `index_products(products)`: Index products into Qdrant
- `search_products(query, limit)`: Vector similarity search
- `get_context_for_query(query)`: Generate context for LLM

**Technology Stack**:
- OpenAI text-embedding-3-large (3072 dimensions)
- Qdrant vector database
- COSINE similarity for search

**Flow**:
```
User Query → Embedding Generation → Vector Search → Results Ranking → Response
```

#### 2. Conversation Service (`conversation_service.py`)

**Purpose**: Manage multi-turn conversations with context

**Key Methods**:
- `process_message(message, session_id)`: Main conversation handler
- `detect_intent(message)`: Intent classification
- `get_session_context(session_id)`: Session management
- Intent handlers: search, availability, refinement, order, color query

**Intent Types**:
- `search`: Product discovery
- `check_availability`: Size/stock queries
- `refine_search`: Show more options
- `order`: Place order
- `color_query`: Color variations
- `general`: General conversation

**Context Management**:
```python
{
    'messages': [],           # Conversation history
    'last_products': [],      # Recently shown products
    'current_selection': {}   # User's current selection
}
```

#### 3. Product Service (`product_service.py`)

**Purpose**: Product data management

**Key Methods**:
- `load_products_from_csv()`: Data ingestion
- `get_product_by_id(id)`: Single product retrieval
- `get_all_products(skip, limit)`: Pagination
- `search_products_text(query)`: MongoDB text search

**Data Flow**:
```
CSV → Pandas → MongoDB → Qdrant Indexing
```

#### 4. Order Service (`order_service.py`)

**Purpose**: Order management

**Key Methods**:
- `create_order(items, customer_info)`: Create order
- `get_order(order_id)`: Retrieve order
- `update_order_status(order_id, status)`: Update status

**Order Schema**:
```python
{
    'order_id': str(uuid),
    'items': [],
    'customer_info': {},
    'total': int,
    'status': str,
    'created_at': datetime,
    'updated_at': datetime
}
```

### Data Layer

#### 1. Qdrant (Vector Database)

**Collections**:

1. **fashion_products**
   - Purpose: Product embeddings for semantic search
   - Vector size: 3072 dimensions
   - Distance: COSINE
   - Payload: Product metadata

2. **conversation_memory**
   - Purpose: Conversation context and history
   - Vector size: 3072 dimensions
   - Distance: COSINE
   - Payload: Session data

**Configuration**:
```python
VectorParams(
    size=3072,
    distance=Distance.COSINE
)
```

#### 2. MongoDB (Document Database)

**Collections**:

1. **products**
   ```javascript
   {
       id: Number,
       gender: String,
       masterCategory: String,
       subCategory: String,
       articleType: String,
       baseColour: String,
       season: String,
       year: Number,
       usage: String,
       productDisplayName: String,
       price: Number,
       stock: Number,
       sizes: String
   }
   ```

2. **orders**
   ```javascript
   {
       order_id: String,
       items: Array,
       customer_info: Object,
       total: Number,
       status: String,
       created_at: ISODate,
       updated_at: ISODate
   }
   ```

**Indexes**:
- products: Text index on (productDisplayName, articleType, baseColour)
- orders: Index on order_id, created_at

## Data Flow Diagrams

### 1. Voice Search Flow

```
User Speech Input
    ↓
Web Speech API (Browser)
    ↓
Transcription
    ↓
POST /api/conversation
    ↓
Conversation Service
    ├─→ Intent Detection
    ├─→ RAG Service (if search intent)
    │   ├─→ Generate Embedding
    │   ├─→ Qdrant Vector Search
    │   └─→ Retrieve Products
    ├─→ GPT-4o (if general intent)
    └─→ Response Generation
    ↓
JSON Response
    ↓
Frontend Update
    ├─→ Conversation Panel
    └─→ Product Display
```

### 2. RAG Pipeline Flow

```
User Query: "Find traditional dresses"
    ↓
Generate Embedding (OpenAI)
    ↓
Query Vector: [3072-dimensional array]
    ↓
Qdrant Vector Search
    ├─→ Compare with indexed products
    ├─→ Calculate COSINE similarity
    └─→ Return top K results
    ↓
Format Results
    ├─→ Product details
    ├─→ Relevance scores
    └─→ Availability info
    ↓
Return to Conversation Service
    ↓
Generate Natural Response (GPT-4o)
    ↓
Return to User
```

### 3. Order Placement Flow

```
User: "Order this for me"
    ↓
Conversation Service
    ├─→ Check current_selection
    └─→ Confirm product & size
    ↓
Add to Cart (Frontend)
    ↓
User clicks Checkout
    ↓
Checkout Component
    ├─→ Display Order Summary
    └─→ Show Delivery Form
    ↓
User fills form
    ↓
POST /api/orders
    ↓
Order Service
    ├─→ Validate data
    ├─→ Calculate total
    ├─→ Generate order_id
    └─→ Store in MongoDB
    ↓
Success Response
    ↓
Confirmation Screen
```

## Technology Stack Summary

### Frontend
| Technology | Purpose | Version |
|-----------|---------|---------|
| React | UI Framework | 18.2.0 |
| Web Speech API | Voice Input | Browser Native |
| Axios | HTTP Client | 1.6.0 |
| CSS3 | Styling | - |

### Backend
| Technology | Purpose | Version |
|-----------|---------|---------|
| Python | Runtime | 3.11+ |
| Flask | Web Framework | 3.0.0 |
| OpenAI | LLM & Embeddings | 1.10.0 |
| Qdrant Client | Vector DB | 1.7.0 |
| PyMongo | MongoDB Driver | 4.6.1 |
| LangChain | Agent Framework | 0.1.0 |

### Infrastructure
| Technology | Purpose | Deployment |
|-----------|---------|-----------|
| MongoDB | Document Store | Docker/Cloud |
| Qdrant | Vector Store | Docker/Cloud |
| Docker | Containerization | Local/Cloud |

## Security Architecture

### API Security
- CORS configuration for frontend origin
- Environment variables for secrets
- Input validation on all endpoints
- Rate limiting (TODO)

### Data Security
- No sensitive data in logs
- Encrypted connections (HTTPS in production)
- MongoDB injection prevention
- API key rotation policy

### Privacy
- Voice data not stored permanently
- User sessions in-memory (POC)
- Clear data usage disclosure

## Performance Considerations

### Frontend
- Lazy loading for product images
- Component code splitting
- Debounced search inputs
- Optimized re-renders

### Backend
- Connection pooling for MongoDB
- Qdrant query optimization
- Caching layer (future)
- Async processing for embeddings

### Database
- Qdrant HNSW index for fast search
- MongoDB indexes on common queries
- Vector quantization (future)

## Scalability

### Horizontal Scaling
- Stateless backend services
- Load balancer ready
- Distributed vector search with Qdrant cluster

### Vertical Scaling
- MongoDB Atlas for managed scaling
- Qdrant Cloud for vector storage
- OpenAI API handles LLM load

## Monitoring & Observability

### Metrics to Track
- API response times
- Embedding generation latency
- Vector search performance
- User session duration
- Error rates

### Logging
- Structured logging (JSON)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Centralized logging (future)

## Deployment Architecture

### Development
```
Local Machine
├── Frontend (npm start) :3000
├── Backend (python app.py) :5000
├── MongoDB (docker) :27017
└── Qdrant (docker) :6333
```

### Production
```
Cloud Platform
├── Frontend (Vercel/Netlify)
├── Backend (Railway/Agent Engine)
├── MongoDB (Atlas)
└── Qdrant (Cloud)
```

## API Documentation

See `docs/API.md` for detailed API documentation.

## Future Enhancements

1. **Real-time Voice Streaming**: OpenAI Realtime API integration
2. **Advanced RAG**: Hybrid search (vector + keyword)
3. **User Profiles**: Personalized recommendations
4. **Multi-language**: Support for Hindi, regional languages
5. **Image Search**: Visual similarity search
6. **AR Try-On**: Virtual product preview
7. **Social Features**: Share, reviews, ratings

---

**Version**: 1.0  
**Last Updated**: 2026-01-14  
**Maintainer**: Development Team
