import React, { useState, useEffect } from 'react';
import SidebarHeader from './sidebarHeader';
import TreeVisualization from '../treeVisualization'
import '../../styles/sidebar.css';

const Sidebar = ({ showSidebar, setShowSidebar, initialContent, updateContent, rawData }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [content, setContent] = useState(initialContent);

  // Update local content when prop changes
  useEffect(() => {
    setContent(initialContent);
  }, [initialContent]);

  // Tab sections
  const tabs = [
    { id: 'marketTrends', label: 'Business Information' },
    { id: 'competitorResearch', label: 'Market Research' },
    { id: 'swotAnalysis', label: 'SWOT Analysis' },
    { id: 'simulate', label: 'Deep Simulation' },
    { id: 'graphs', label: 'Graphs' }
  ];

  const renderTabContent = () => {
    const activeTabId = tabs[activeTab].id;
    const tabContent = content[activeTabId];
    
    // Special handling for the tree visualization
    if (activeTabId === 'simulate' && tabContent === 'RENDER_TREE_VISUALIZATION') {
      return (
        <div className="sidebar-content-wrapper">
          <h2 className="sidebar-content-title">{tabs[activeTab].label}</h2>
          <div className="sidebar-content-box tree-container">
            <TreeVisualization data={rawData?.thinking || rawData} />
          </div>
        </div>
      );
    }
    
    // Regular text content for other tabs
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