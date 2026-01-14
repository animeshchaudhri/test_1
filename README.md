# Voice-Enabled Fashion E-Commerce POC

A proof-of-concept voice-enabled fashion e-commerce platform inspired by Nykaa's color scheme, featuring conversational AI shopping with RAG-based product search.

## 🎨 Features

- **Voice Search**: Natural language voice commands for product discovery
- **Text Search**: Traditional text-based search with semantic understanding
- **Conversational AI**: Multi-turn conversations with context retention
- **RAG-Powered Search**: Semantic product search using OpenAI embeddings and Qdrant
- **Smart Recommendations**: AI-driven product suggestions based on user preferences
- **Checkout Flow**: Streamlined order placement process

## 🏗️ Architecture

### Frontend (React)
- Modern React UI with Nykaa-inspired color scheme (#E80071)
- Web Speech API integration for voice input
- Real-time conversation panel
- Responsive product cards and checkout flow

### Backend (Python/Flask)
- Flask REST API
- OpenAI GPT-4o for conversation management
- OpenAI text-embedding-3-large for semantic search
- RAG pipeline with Qdrant vector database
- MongoDB for product and order storage

### Tech Stack

**Frontend:**
- React 18
- Web Speech API
- Axios for API calls
- CSS3 with animations

**Backend:**
- Python 3.9+
- Flask
- OpenAI API (GPT-4o, text-embedding-3-large)
- Qdrant (Vector database)
- MongoDB (Document database)
- LangChain (Optional agent framework)

## 📦 Installation

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- MongoDB (local or cloud)
- Qdrant (local or cloud)
- OpenAI API key

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

The frontend will run on `http://localhost:3000`

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env and add your API keys

# Start the server
python app.py
```

The backend will run on `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-3-large

# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_COLLECTION_NAME=fashion_products
QDRANT_MEMORY_COLLECTION=conversation_memory

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=voice_ecommerce

# Server Configuration
FLASK_ENV=development
FLASK_DEBUG=1
PORT=5000

# CORS Configuration
FRONTEND_URL=http://localhost:3000
```

### Database Setup

**MongoDB:**
```bash
# Install MongoDB locally or use MongoDB Atlas
# No schema setup required - collections will be created automatically
```

**Qdrant:**
```bash
# Option 1: Docker
docker run -p 6333:6333 qdrant/qdrant

# Option 2: Qdrant Cloud
# Sign up at https://cloud.qdrant.io
```

### Initialize Data

Load sample product data into the system:

```bash
curl -X POST http://localhost:5000/api/init-data
```

This will:
1. Load products from `data/sample_styles.csv`
2. Store products in MongoDB
3. Generate embeddings and index in Qdrant

## 🚀 Usage

### Voice Search Flow

1. Click the microphone button
2. Say: "Find me traditional dresses"
3. AI responds with relevant products
4. Refine: "I don't like the first one, show me more colors"
5. Check availability: "Is it available in medium?"
6. Order: "Order this for me"
7. Complete checkout form

### Text Search Flow

1. Type in search bar: "blue kurtas"
2. Browse results
3. Click size to add to cart
4. Click cart icon to checkout
5. Fill delivery details
6. Place order

## 📡 API Endpoints

### Search Products
```http
POST /api/search
Content-Type: application/json

{
  "query": "traditional dresses"
}
```

### Conversation
```http
POST /api/conversation
Content-Type: application/json

{
  "message": "Find me blue kurtas",
  "session_id": "user123"
}
```

### Create Order
```http
POST /api/orders
Content-Type: application/json

{
  "items": [
    {
      "id": 1,
      "name": "Blue Silk Kurta",
      "price": 2499,
      "size": "M"
    }
  ],
  "customer_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "9876543210",
    "address": "123 Main St",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001"
  }
}
```

### Get Product
```http
GET /api/products/:id
```

### Health Check
```http
GET /health
```

## 🎨 UI/UX Design

### Color Scheme (Nykaa-inspired)

- **Primary**: #E80071 (Nykaa Pink)
- **Secondary**: #FFFFFF (White)
- **Text**: #1A1A1A (Dark Gray)
- **Background**: #FAFAFA (Light Gray)
- **Success**: #4CAF50 (Green)
- **Voice Active**: #7C3AED (Purple)

### Key Design Elements

- **Voice Button**: Pulsing animation when active
- **Product Cards**: Hover effects, clear pricing
- **Conversation Panel**: Fixed position, real-time updates
- **Checkout Flow**: Multi-step with order summary

## 📊 Data Structure

### Product Schema (MongoDB)

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
  sizes: String  // Comma-separated
}
```

### Order Schema

```javascript
{
  order_id: String,
  items: Array,
  customer_info: Object,
  total: Number,
  status: String,
  created_at: String,
  updated_at: String
}
```

## 🧪 Testing

### Frontend
```bash
cd frontend
npm test
```

### Backend
```bash
cd backend
pytest
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build and run with docker-compose
docker-compose up -d
```

### Manual Deployment

**Frontend (Vercel/Netlify):**
```bash
cd frontend
npm run build
# Deploy the build folder
```

**Backend (Heroku/Railway/Agent Engine):**
```bash
# Configure environment variables in your platform
# Deploy the backend directory
```

## 📝 Development Roadmap

- [x] Basic voice search functionality
- [x] Text search with RAG
- [x] Conversational AI with context
- [x] Product display and cart
- [x] Checkout flow
- [ ] User authentication
- [ ] Payment integration
- [ ] Order tracking
- [ ] Advanced filters
- [ ] Recommendation engine
- [ ] Multi-language support

## 🎯 UI/UX References

This POC is inspired by award-winning interfaces:

1. **SSENSE** - Minimal navigation, editorial-first approach
2. **Amazon Alexa** - Voice commerce patterns
3. **Nykaa** - Color scheme and trust indicators
4. **Ray-Ban Meta AI** - Concise AI responses
5. **Breez** - Progressive disclosure in conversations

See `docs/UI_UX_ANALYSIS.md` for detailed analysis.

## 🔒 Security

- API keys stored in environment variables
- CORS configured for frontend origin
- Input validation on all endpoints
- MongoDB injection prevention
- Rate limiting (TODO)

## 🤝 Contributing

This is a proof-of-concept. For production use:

1. Add comprehensive error handling
2. Implement rate limiting
3. Add authentication/authorization
4. Set up logging and monitoring
5. Add comprehensive tests
6. Optimize database queries
7. Implement caching

## 📄 License

MIT License - This is a proof-of-concept project.

## 👥 Team

Developed as a POC for voice-enabled e-commerce exploration.

## 📞 Support

For issues or questions, please open an issue in the repository.

---

**Note**: This is a proof-of-concept and requires API keys and database setup to function. Ensure all services are configured before running.