import React from 'react';
import './style.css';

export default function Button({ children, "aria-label": ariaLabel, ...props }) {
  const label =
    ariaLabel || (typeof children === 'string' ? children : undefined);
  return (
    <button className="flat-btn" aria-label={label} {...props}>
      {children}
    </button>
  );
}
