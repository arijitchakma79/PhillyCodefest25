import React from 'react';
import SidebarSection from './sidebarSection';

const SidebarContent = ({ content }) => {
  return (
    <div className="sidebar-content">
      <SidebarSection title="Market Trends" content={content.marketTrends} />
      <SidebarSection title="Competitor Research" content={content.competitorResearch} />
      <SidebarSection title="SWOT Analysis" content={content.swotAnalysis} />
      <SidebarSection title="Simulate" content={content.simulation} />
    </div>
  );
};

export default SidebarContent;
