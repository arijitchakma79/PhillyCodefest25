import React, { useState, useEffect } from 'react';
import SidebarHeader from './sidebarHeader';
import TreeVisualization from '../treeVisualization';
import GraphVisualization from '../graphVisualization';
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

  // Convert markdown to HTML
  const renderMarkdown = (text) => {
    // Simple markdown-like formatting
    // Convert headers
    let formattedText = text
      .replace(/^# (.*$)/gm, '<h1>$1</h1>')
      .replace(/^## (.*$)/gm, '<h2>$1</h2>')
      .replace(/^### (.*$)/gm, '<h3>$1</h3>')
      // Convert bullet points
      .replace(/^• (.*$)/gm, '<li>$1</li>')
      // Wrap lists
      .replace(/<li>(.*?)<\/li>/g, (match) => {
        return '<ul>' + match + '</ul>';
      })
      // Remove duplicate list tags
      .replace(/<\/ul><ul>/g, '')
      // Bold text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Italic text
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Line breaks
      .replace(/\n/g, '<br>');
    
    return { __html: formattedText };
  };

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

    // Special handling for the graphs visualization
    if (activeTabId === 'graphs') {
      return (
        <div className="sidebar-content-wrapper">
          <h2 className="sidebar-content-title">{tabs[activeTab].label}</h2>
          <div className="sidebar-content-box">
            <GraphVisualization data={rawData} />
          </div>
        </div>
      );
    }
    
    // Regular text content for other tabs with markdown formatting
    return (
      <div className="sidebar-content-wrapper">
        <h2 className="sidebar-content-title">{tabs[activeTab].label}</h2>
        <div className="sidebar-content-box">
          {tabContent ? (
            <div dangerouslySetInnerHTML={renderMarkdown(tabContent)} />
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