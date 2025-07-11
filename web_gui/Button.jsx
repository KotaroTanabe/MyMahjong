import React from 'react';
import './style.css';

export default function Button({ children, "aria-label": ariaLabel, className = '', ...props }) {
  const label =
    ariaLabel || (typeof children === 'string' ? children : undefined);
  return (
    <button
      className={`flat-btn${className ? ` ${className}` : ''}`}
      aria-label={label}
      {...props}
    >
      {children}
    </button>
  );
}
