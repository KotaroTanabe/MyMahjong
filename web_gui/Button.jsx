import React from 'react';
import './style.css';

export default function Button({ children, ...props }) {
  return (
    <button className="flat-btn" {...props}>
      {children}
    </button>
  );
}
