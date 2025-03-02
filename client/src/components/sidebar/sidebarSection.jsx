import React from 'react';

const SidebarSection = ({ title, content }) => {
  return (
    <div className="sidebar-section">
      <h4>{title}</h4>
      <div className="sidebar-content-box">
        {content ? <pre>{content}</pre> : <p>No data available</p>}
      </div>
    </div>
  );
};

export default SidebarSection;
