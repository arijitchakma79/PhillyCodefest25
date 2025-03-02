import React from 'react';

const SidebarNavbar = ({ activeNavItem, setActiveNavItem }) => {
  const navItems = ['Market Trends', 'Business Information', 'SWOT Analysis', 'Deep Simulation'];

  return (
    <nav className="sidebar-navbar">
      {navItems.map((item, index) => (
        <div 
          key={index}
          className={`sidebar-navbar-item ${activeNavItem === index ? 'active' : ''}`}
          onClick={() => setActiveNavItem(index)}
          role="button"
          tabIndex={0}
          aria-selected={activeNavItem === index}
        >
          {item}
        </div>
      ))}
    </nav>
  );
};

export default SidebarNavbar;
