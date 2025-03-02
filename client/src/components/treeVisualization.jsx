import React, { useEffect, useRef, useState } from 'react';
import Tree from 'react-d3-tree';
import '../styles/treeVisualization.css';

const TreeVisualization = ({ data }) => {
  const treeContainerRef = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 400 });

  // Convert the thinking data structure to the format required by react-d3-tree
  const prepareTreeData = () => {
    // Check if data exists and has the right structure
    if (!data) return { name: 'No data available' };

    // Handle nested thinking structure
    const thinkingData = data.thinking && typeof data.thinking === 'object' 
      ? data.thinking 
      : data;

    // Find the initial state
    let initialState;
    if (thinkingData.Initial_State) {
      initialState = { id: 'Initial_State', data: thinkingData.Initial_State };
    } else {
      // If Initial_State doesn't exist, use the first property
      const keys = Object.keys(thinkingData).filter(key => typeof thinkingData[key] === 'object');
      if (keys.length > 0) {
        initialState = { id: keys[0], data: thinkingData[keys[0]] };
      } else {
        return { name: 'No valid tree data found' };
      }
    }

    // Recursive function to convert the nested structure
    const convertNode = (nodeId, nodeData) => {
      if (!nodeData || typeof nodeData !== 'object') {
        return { name: nodeId };
      }

      const node = {
        name: nodeId.replace(/_/g, ' '),
        attributes: {
          description: nodeData.state_description || ''
        },
        children: []
      };

      // Add children if next_steps exists
      if (nodeData.next_steps && typeof nodeData.next_steps === 'object') {
        const childKeys = Object.keys(nodeData.next_steps);
        
        childKeys.forEach(childKey => {
          const childNode = convertNode(childKey, nodeData.next_steps[childKey]);
          if (childNode) {
            node.children.push(childNode);
          }
        });
      }

      return node;
    };

    // Start the conversion with the initial state
    return convertNode(initialState.id, initialState.data);
  };

  // Update dimensions when component mounts or window resizes
  useEffect(() => {
    const updateDimensions = () => {
      if (treeContainerRef.current) {
        const { width, height } = treeContainerRef.current.getBoundingClientRect();
        setDimensions({ width, height });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);

    return () => {
      window.removeEventListener('resize', updateDimensions);
    };
  }, []);

  // Prepare the tree data
  const treeData = prepareTreeData();
  
  // Custom node renderer for better readability
  const renderCustomNode = ({ nodeDatum }) => (
    <g className="rd3t-node-container">
      <circle r={20} fill="#3b82f6" className="rd3t-node-circle" />
      <foreignObject x={25} y={-30} width={220} height={120}>
        <div className="node-description">
          <h4>{nodeDatum.name}</h4>
          <p>{nodeDatum.attributes?.description || ''}</p>
        </div>
      </foreignObject>
    </g>
  );

  return (
    <div className="tree-container" ref={treeContainerRef}>
      {dimensions.width > 0 && (
        <Tree
          data={treeData}
          orientation="vertical"
          pathFunc="step"
          renderCustomNodeElement={renderCustomNode}
          collapsible={false} // Disable collapse to show all nodes
          zoomable={true}
          draggable={true}
          initialDepth={999} // Show all nodes by setting a very high initial depth
          separation={{ siblings: 3, nonSiblings: 3.5 }} // Increase separation for better visibility
          translate={{ x: dimensions.width / 2, y: 50 }}
          nodeSize={{ x: 250, y: 150 }} // Increase y spacing between nodes
          scaleExtent={{ min: 0.1, max: 2 }} // Allow more zoom out
          zoom={0.6} // Start zoomed out to show more of the tree
        />
      )}
      <div className="tree-controls">
        <div className="tree-instructions">
          <p>• Drag to pan the view</p>
          <p>• Use mouse wheel to zoom</p>
        </div>
      </div>
    </div>
  );
};

export default TreeVisualization;