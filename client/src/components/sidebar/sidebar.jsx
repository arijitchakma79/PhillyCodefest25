import React, { useState, useEffect } from 'react';
import SidebarHeader from './sidebarHeader';
import '../../styles/sidebar.css';

const Sidebar = ({ showSidebar, setShowSidebar, initialContent, updateContent }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [content, setContent] = useState(initialContent);

  // Update local content when prop changes
  useEffect(() => {
    setContent(initialContent);
  }, [initialContent]);

  // Tab sections
  const tabs = [
    { id: 'marketTrends', label: 'Market Trends' },
    { id: 'competitorResearch', label: 'Competitor Research' },
    { id: 'swotAnalysis', label: 'SWOT Analysis' },
    { id: 'simulate', label: 'Simulate' }
  ];

  const renderTabContent = () => {
    const activeTabId = tabs[activeTab].id;
    const tabContent = content[activeTabId];
    
    return (
      <div className="sidebar-content-wrapper">
        <h2 className="sidebar-content-title">{tabs[activeTab].label}</h2>
        <div className="sidebar-content-box">
          {tabContent ? (
            <pre>{tabContent}</pre>
          ) : (
            <p className="no-data-message">No data available</p>
          )}
        </div>
      </div>
    );
  };

  // Use CSS to control visibility instead of conditional rendering
  return (
    <div className={`sidebar ${showSidebar ? 'visible' : 'hidden'}`}>
      <SidebarHeader title="Generated Content" onClose={() => setShowSidebar(false)} />
      
      {/* Tab Navigation */}
      <div className="sidebar-navbar">
        {tabs.map((tab, index) => (
          <div
            key={tab.id}
            className={`sidebar-navbar-item ${activeTab === index ? 'active' : ''}`}
            onClick={() => setActiveTab(index)}
            role="button"
            tabIndex={0}
            aria-selected={activeTab === index}
          >
            {tab.label}
          </div>
        ))}
      </div>
      
      {/* Tab Content Area */}
      <div className="sidebar-content">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default Sidebar;