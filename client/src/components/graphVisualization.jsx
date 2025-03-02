import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../styles/graphVisualization.css'

const GraphVisualization = ({ data }) => {
  // Process graph data from JSON
  const processGraphData = () => {
    if (!data || !data.graphs) {
      return {
        graphs: [],
        hasData: false
      };
    }

    const processedGraphs = [];
    const graphIds = Object.keys(data.graphs);

    graphIds.forEach(graphId => {
      const graphData = data.graphs[graphId];
      
      // Skip if graph data is incomplete
      if (!graphData || !graphData.data || !Array.isArray(graphData.data)) return;
      
      // Generate chart data in the format needed by recharts
      const chartData = graphData.data.map((value, index) => ({
        month: `Month ${index + 1}`,
        value: value
      }));
      
      // Add the processed graph
      processedGraphs.push({
        id: graphId,
        title: graphData.title || graphId.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
        xLabel: graphData.x_label || 'Month',
        yLabel: graphData.y_label || 'Value',
        data: chartData,
        color: graphId.includes('revenue') ? '#3b82f6' : '#ef4444' // Blue for revenue, red for costs/burn rate
      });
    });
    
    return {
      graphs: processedGraphs,
      hasData: processedGraphs.length > 0
    };
  };

  const { graphs, hasData } = processGraphData();

  // If no valid graph data is found
  if (!hasData) {
    return (
      <div className="no-graph-data">
        <p>No graph data available</p>
      </div>
    );
  }

  return (
    <div className="graphs-container">
      {graphs.map((graph, index) => (
        <div key={graph.id} className="graph-item">
          <h2 className="graph-title">{graph.title}</h2>
          
          <div className="graph-chart">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={graph.data}
                margin={{ top: 10, right: 30, left: 20, bottom: 30 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="month" 
                  label={{ 
                    value: graph.xLabel, 
                    position: 'insideBottomRight', 
                    offset: -10 
                  }} 
                />
                <YAxis 
                  label={{ 
                    value: graph.yLabel, 
                    angle: -90, 
                    position: 'insideLeft',
                    style: { textAnchor: 'middle' }
                  }} 
                />
                <Tooltip 
                  formatter={(value) => [`${value}`, graph.yLabel]}
                  labelFormatter={(label) => `${label}`}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="value" 
                  name={graph.yLabel} 
                  stroke={graph.color} 
                  strokeWidth={2}
                  activeDot={{ r: 8 }} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          
          {/* Data table */}
          <div className="graph-data-table">
            <h3>Data Values</h3>
            <table className="data-table">
              <thead>
                <tr>
                  <th>{graph.xLabel}</th>
                  <th>{graph.yLabel}</th>
                </tr>
              </thead>
              <tbody>
                {graph.data.map((point, i) => (
                  <tr key={i}>
                    <td>{point.month}</td>
                    <td>{point.value}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {index < graphs.length - 1 && <hr className="graph-divider" />}
        </div>
      ))}
    </div>
  );
};

export default GraphVisualization;