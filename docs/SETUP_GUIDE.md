# Quick Start Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.9 or higher) - [Download](https://python.org/)
- **Docker** (optional, for MongoDB and Qdrant) - [Download](https://docker.com/)
- **Git** - [Download](https://git-scm.com/)

## Step 1: Clone the Repository

```bash
git clone https://github.com/animeshchaudhri/test_1.git
cd test_1
```

## Step 2: Set Up Databases

### Option A: Using Docker (Recommended)

```bash
# Start MongoDB and Qdrant
docker run -d -p 27017:27017 --name mongodb mongo:7.0
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant:latest
```

### Option B: Using Docker Compose

```bash
# Start all services
docker-compose up -d mongodb qdrant
```

### Option C: Manual Installation

**MongoDB:**
- Follow instructions at https://www.mongodb.com/docs/manual/installation/
- Start MongoDB on default port 27017

**Qdrant:**
- Follow instructions at https://qdrant.tech/documentation/quick-start/
- Or use Qdrant Cloud: https://cloud.qdrant.io/

## Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use any text editor
```

### Configure Environment Variables

Edit the `.env` file:

```env
# REQUIRED: Get your API key from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-api-key-here

# Optional: Use defaults if running locally with Docker
QDRANT_URL=http://localhost:6333
MONGODB_URI=mongodb://localhost:27017/
```

## Step 4: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## Step 5: Initialize Data

Start the backend server:

```bash
cd ../backend
python app.py
```

In a new terminal, load sample data:

```bash
curl -X POST http://localhost:5000/api/init-data
```

You should see:
```json
{
  "success": true,
  "message": "Data initialized successfully",
  "products_loaded": 45
}
```

## Step 6: Start the Application

### Terminal 1: Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

Expected output:
```
✅ Connected to MongoDB
✅ Created Qdrant collection: fashion_products
🚀 Voice E-Commerce API starting on port 5000
📊 Frontend URL: http://localhost:3000
 * Running on http://0.0.0.0:5000
```

### Terminal 2: Frontend
```bash
cd frontend
npm start
```

Expected output:
```
Compiled successfully!

You can now view voice-ecommerce-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

## Step 7: Access the Application

Open your browser and navigate to:
```
http://localhost:3000
```

## Step 8: Test the Features

### Test Voice Search

1. **Click the microphone button** (requires Chrome or Edge)
2. **Say**: "Find me traditional dresses"
3. **Wait for results** to appear
4. **Try refinement**: "Show me more colors"
5. **Check availability**: "Is it available in medium?"

### Test Text Search

1. **Type in search bar**: "blue kurtas"
2. **Press Enter** or click search
3. **Click size button** to add to cart
4. **Click cart icon** to checkout

### Test Checkout

1. **Add items to cart**
2. **Click cart icon** in header
3. **Fill delivery form**
4. **Click "Place Order"**
5. **See success confirmation**

## Troubleshooting

### Issue: "Speech recognition not supported"

**Solution**: Use Google Chrome or Microsoft Edge. Safari has limited support.

### Issue: "MongoDB connection error"

**Solution**: 
```bash
# Check if MongoDB is running
docker ps | grep mongodb
# Or restart MongoDB
docker restart mongodb
```

### Issue: "Qdrant connection error"

**Solution**:
```bash
# Check if Qdrant is running
docker ps | grep qdrant
# Or restart Qdrant
docker restart qdrant
```

### Issue: "OpenAI API error"

**Solution**: 
- Check your API key in `.env`
- Verify you have credits: https://platform.openai.com/usage
- Check API key permissions

### Issue: Port already in use

**Frontend (3000)**:
```bash
# Change port
PORT=3001 npm start
```

**Backend (5000)**:
```bash
# Edit .env
PORT=5001
```

## Verify Installation

Run health check:

```bash
# Backend health
curl http://localhost:5000/health

# Expected response:
# {"status": "healthy", "message": "Voice E-Commerce API is running"}
```

## Next Steps

1. **Explore the UI**: Try different voice commands
2. **Review the code**: Check component structure
3. **Read documentation**: 
   - [Architecture](./ARCHITECTURE.md)
   - [UI/UX Analysis](./UI_UX_ANALYSIS.md)
   - [API Documentation](./API.md)
4. **Customize**: Modify colors, add features
5. **Deploy**: Follow deployment guide

## Common Commands

### Backend
```bash
# Start backend
cd backend && python app.py

# Run tests (if available)
pytest

# Check dependencies
pip list
```

### Frontend
```bash
# Start frontend
cd frontend && npm start

# Build for production
npm run build

# Run tests
npm test
```

### Docker
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend
```

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- **Frontend**: Automatic with React dev server
- **Backend**: Use `FLASK_DEBUG=1` in `.env`

### Debug Mode

**Frontend**: Open browser DevTools (F12)
- Console for logs
- Network tab for API calls

**Backend**: Check terminal output
- All logs print to console
- Error tracebacks included

### Testing Voice in Different Browsers

| Browser | Support | Notes |
|---------|---------|-------|
| Chrome | ✅ Full | Best experience |
| Edge | ✅ Full | Chromium-based |
| Safari | ⚠️ Partial | Limited features |
| Firefox | ❌ None | Not supported |

## Getting Help

1. **Check logs**: Frontend console and backend terminal
2. **Review docs**: In the `docs/` folder
3. **Common issues**: See troubleshooting above
4. **GitHub Issues**: Open an issue if stuck

## What's Next?

Once you have the application running:

1. **Experiment with queries**: Try different voice commands
2. **Modify products**: Edit `data/sample_styles.csv`
3. **Customize UI**: Update colors in `frontend/src/index.css`
4. **Add features**: Extend the conversation service
5. **Deploy**: Follow the deployment guide

---

**Estimated Setup Time**: 15-20 minutes  
**Difficulty**: Beginner to Intermediate  
**Support**: Check troubleshooting section or open an issue
