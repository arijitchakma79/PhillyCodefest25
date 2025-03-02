// Sidebar.js - All components in a single file
// You can extract these into separate files later

import React from 'react';

// SidebarHeader Component
export const SidebarHeader = ({ onClose }) => {
  return (
    <div className="sidebar-header">
      <h3>Generated Content</h3>
      <button 
        onClick={onClose} 
        className="sidebar-close"
        aria-label="Close sidebar"
      >✕</button>
    </div>
  );
};

// SidebarNavbar Component
export const SidebarNavbar = ({ activeNavItem, setActiveNavItem }) => {
  const navItems = ['Code', 'Data', 'Analysis', 'Results'];
  
  return (
    <div className="sidebar-navbar">
      {navItems.map((item, index) => (
        <div 
          key={index}
          className={`sidebar-navbar-item ${activeNavItem === index ? 'active' : ''}`}
          onClick={() => setActiveNavItem(index)}
        >
          {item}
        </div>
      ))}
    </div>
  );
};

// SidebarContent Component
export const SidebarContent = ({ activeNavItem, content }) => {
  // You can expand this to handle different content types based on activeNavItem
  const renderContent = () => {
    switch (activeNavItem) {
      case 0: // Code
        return <pre>{content}</pre>;
      case 1: // Data
        return <div className="data-container">{content || "No data available"}</div>;
      case 2: // Analysis
        return <div className="analysis-container">{content || "No analysis available"}</div>;
      case 3: // Results
        return <div className="results-container">{content || "No results available"}</div>;
      default:
        return <pre>{content}</pre>;
    }
  };

  return (
    <div className="sidebar-content">
      {renderContent()}
    </div>
  );
};

// Main Sidebar Component
const Sidebar = ({ 
  showSidebar, 
  setShowSidebar, 
  activeNavItem, 
  setActiveNavItem, 
  content 
}) => {
  if (!showSidebar) return null;

  return (
    <div className="sidebar">
      <SidebarHeader onClose={() => setShowSidebar(false)} />
      <SidebarNavbar 
        activeNavItem={activeNavItem} 
        setActiveNavItem={setActiveNavItem} 
      />
      <SidebarContent 
        activeNavItem={activeNavItem} 
        content={content} 
      />
    </div>
  );
};

export default Sidebar;