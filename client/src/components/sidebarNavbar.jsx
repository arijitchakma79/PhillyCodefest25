// SidebarNavbar.jsx
import React from 'react';

const SidebarNavbar = ({ activeNavItem, setActiveNavItem }) => {
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

export default SidebarNavbar;
