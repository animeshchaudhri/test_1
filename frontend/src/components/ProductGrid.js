import React, { useState } from 'react';
import './ProductGrid.css';

function ProductGrid({ products, onAddToCart }) {
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [selectedSize, setSelectedSize] = useState('');

  const handleSizeSelect = (product, size) => {
    setSelectedSize(size);
    onAddToCart(product, size);
    setSelectedProduct(null);
    setSelectedSize('');
  };

  if (products.length === 0) {
    return (
      <div className="no-products">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="empty-icon">
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
        </svg>
        <p>Start searching to discover amazing products!</p>
        <p className="hint">Try: "Find me traditional dresses" or "Show blue kurtas"</p>
      </div>
    );
  }

  return (
    <div className="product-grid">
      {products.map((product) => (
        <div key={product.id} className="product-card">
          <div className="product-image">
            <img src={product.image} alt={product.name} />
            {product.inStock && <span className="stock-badge">In Stock</span>}
          </div>
          
          <div className="product-info">
            <h3 className="product-name">{product.name}</h3>
            <p className="product-color">Color: {product.color}</p>
            <p className="product-price">₹{product.price}</p>
            
            <div className="size-selection">
              <p className="size-label">Select Size:</p>
              <div className="size-buttons">
                {product.sizes.map((size) => (
                  <button
                    key={size}
                    className={`size-button ${selectedSize === size && selectedProduct === product.id ? 'selected' : ''}`}
                    onClick={() => {
                      setSelectedProduct(product.id);
                      handleSizeSelect(product, size);
                    }}
                  >
                    {size}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default ProductGrid;
