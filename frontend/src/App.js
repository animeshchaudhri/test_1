import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import VoiceSearch from './components/VoiceSearch';
import ProductGrid from './components/ProductGrid';
import ConversationPanel from './components/ConversationPanel';
import CheckoutFlow from './components/CheckoutFlow';

function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [showCheckout, setShowCheckout] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [isVoiceActive, setIsVoiceActive] = useState(false);

  const handleSearch = async (query) => {
    try {
      // TODO: Connect to backend API
      console.log('Searching for:', query);
      // Mock data for now
      setProducts([
        {
          id: 1,
          name: 'Blue Silk Kurta',
          price: 2499,
          color: 'Blue',
          sizes: ['S', 'M', 'L', 'XL'],
          image: 'https://via.placeholder.com/300x400?text=Blue+Silk+Kurta',
          inStock: true
        }
      ]);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  const handleVoiceSearch = (transcript) => {
    handleSearch(transcript);
    setConversationHistory(prev => [
      ...prev,
      { type: 'user', message: transcript, timestamp: new Date() }
    ]);
  };

  const addToCart = (product, size) => {
    setCart(prev => [...prev, { ...product, selectedSize: size }]);
    setConversationHistory(prev => [
      ...prev,
      { 
        type: 'assistant', 
        message: `Added ${product.name} in size ${size} to your cart!`,
        timestamp: new Date()
      }
    ]);
  };

  const proceedToCheckout = () => {
    setShowCheckout(true);
  };

  return (
    <div className="App">
      <Header cartCount={cart.length} onCartClick={proceedToCheckout} />
      
      <main className="main-content">
        <div className="search-section">
          <h1 className="hero-title">Find Your Perfect Style</h1>
          <p className="hero-subtitle">Search with voice or text</p>
          
          <div className="search-controls">
            <SearchBar onSearch={handleSearch} />
            <VoiceSearch 
              onVoiceResult={handleVoiceSearch}
              isActive={isVoiceActive}
              setIsActive={setIsVoiceActive}
            />
          </div>
        </div>

        {showCheckout ? (
          <CheckoutFlow cart={cart} onBack={() => setShowCheckout(false)} />
        ) : (
          <>
            <ProductGrid 
              products={products} 
              onAddToCart={addToCart}
            />
            
            {conversationHistory.length > 0 && (
              <ConversationPanel 
                history={conversationHistory}
                isVoiceActive={isVoiceActive}
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
