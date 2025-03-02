import React from 'react';

const SidebarHeader = ({ title, onClose }) => {
  return (
    <div className="sidebar-header">
      <h3>{title}</h3>
      <button 
        onClick={onClose} 
        className="sidebar-close"
        aria-label="Close sidebar"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  );
};

export default SidebarHeader;