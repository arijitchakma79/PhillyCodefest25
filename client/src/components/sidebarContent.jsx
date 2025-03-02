
// SidebarContent.jsx
import React from 'react';

const SidebarContent = ({ activeNavItem, content }) => {
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

export default SidebarContent;