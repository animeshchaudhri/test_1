import React from 'react';
import './Header.css';

function Header({ cartCount, onCartClick }) {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <h2>Voice Fashion</h2>
          <span className="logo-tagline">Shop with Voice</span>
        </div>
        
        <nav className="nav-menu">
          <a href="#women">Women</a>
          <a href="#men">Men</a>
          <a href="#ethnic">Ethnic</a>
          <a href="#accessories">Accessories</a>
        </nav>
        
        <button className="cart-button" onClick={onCartClick}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="cart-icon">
            <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
          </svg>
          {cartCount > 0 && <span className="cart-badge">{cartCount}</span>}
        </button>
      </div>
    </header>
  );
}

export default Header;
