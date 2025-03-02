/**
 * Utility functions to format JSON data for sidebar display
 */

/**
 * Format business information for display
 * @param {Object} data - The complete JSON data object
 * @returns {string} - Formatted text for the Business Information tab
 */
export const formatBusinessInfo = (data) => {
  if (!data || !data.business) {
    return "No business information available";
  }

  const business = data.business;
  
  return `# ${business.business_name}
${business.short_description}

## Business Details
• Industry: ${business.industry}
• Business Model: ${business.business_model}
• Target Customers: ${business.target_customers}
• Revenue Model: ${business.revenue_model}

## Success Metrics
• Success Probability: ${(business.success_probability * 100).toFixed(1)}%

## Market Overview
• Market Size: ${data.market?.market_size || 'N/A'}
• Growth Rate: ${data.market?.market_growth_rate || 'N/A'}
• Total Addressable Market: ${data.market?.total_addressable_market || 'N/A'}
• Serviceable Obtainable Market: ${data.market?.serviceable_obtainable_market || 'N/A'}

## Key Market Trends
${data.market?.market_trends?.map(trend => `• ${trend}`).join('\n') || 'No trends available'}
`;
};

/**
 * Format market research for display
 * @param {Object} data - The complete JSON data object
 * @returns {string} - Formatted text for the Market Research tab
 */
export const formatMarketResearch = (data) => {
  if (!data || !data.market) {
    return "No market research available";
  }

  const market = data.market;
  
  // Format competitors section
  let competitorsSection = '';
  if (market.competitors && market.competitors.length > 0) {
    competitorsSection = `## Competitor Analysis\n\n`;
    
    market.competitors.forEach(competitor => {
      competitorsSection += `### ${competitor.name}
${competitor.short_description}
• Market Share: ${competitor.market_share}

**Strengths:**
${competitor.strengths?.map(strength => `• ${strength}`).join('\n') || 'None specified'}

**Weaknesses:**
${competitor.weaknesses?.map(weakness => `• ${weakness}`).join('\n') || 'None specified'}

`;
    });
  } else {
    competitorsSection = "## Competitor Analysis\nNo competitor data available\n\n";
  }
  
  return `# Market Research

## Market Details
• Market Size: ${market.market_size}
• Growth Rate: ${market.market_growth_rate}
• Total Addressable Market: ${market.total_addressable_market}
• Serviceable Obtainable Market: ${market.serviceable_obtainable_market || 'N/A'}

## Barriers to Entry
${market.barriers_to_entry?.map(barrier => `• ${barrier}`).join('\n') || 'No barriers listed'}

${competitorsSection}
## Target Customer Segments
${market.customer_segments?.map(segment => `• ${segment}`).join('\n') || 'No customer segments specified'}

## Keywords
${market.keywords?.join(', ') || 'No keywords specified'}
`;
};

/**
 * Format SWOT analysis for display
 * @param {Object} data - The complete JSON data object
 * @returns {string} - Formatted text for the SWOT Analysis tab
 */
export const formatSWOTAnalysis = (data) => {
  if (!data || !data.swot) {
    return "No SWOT analysis available";
  }

  const swot = data.swot;
  
  return `# SWOT Analysis

## Strengths
${swot.strengths?.map(item => `• ${item}`).join('\n') || 'No strengths specified'}

## Weaknesses
${swot.weaknesses?.map(item => `• ${item}`).join('\n') || 'No weaknesses specified'}

## Opportunities
${swot.opportunities?.map(item => `• ${item}`).join('\n') || 'No opportunities specified'}

## Threats
${swot.threats?.map(item => `• ${item}`).join('\n') || 'No threats specified'}
`;
};

/**
 * Format deep simulation data for an interactive visualization component
 * @param {Object} data - The complete JSON data object
 * @returns {string} - Special content indicator for the Deep Simulation tab
 */
export const formatDeepSimulation = (data) => {
  if (!data || !data.thinking) {
    return "No simulation data available";
  }

  // Return a special indicator to tell the sidebar to render the tree visualization component
  return "RENDER_TREE_VISUALIZATION";
};

/**
 * Format graphs data for display
 * @param {Object} data - The complete JSON data object
 * @returns {string} - Special indicator for the Graphs tab
 */
export const formatGraphsData = (data) => {
  // Since we're now handling graphs with a dedicated component,
  // we can just return a placeholder. The actual graph rendering
  // is handled by the GraphVisualization component.
  return "GRAPHS_DATA";
};

/**
 * Format API response JSON for display in the sidebar
 * @param {Object} jsonData - The raw JSON data from the API
 * @returns {Object} - Formatted content for all sidebar sections
 */
export const processApiResponse = (jsonData) => {
  try {
    // Parse the JSON if it's a string
    const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
    
    return {
      marketTrends: formatBusinessInfo(data),
      competitorResearch: formatMarketResearch(data),
      swotAnalysis: formatSWOTAnalysis(data),
      simulate: formatDeepSimulation(data),
      graphs: formatGraphsData(data)
    };
  } catch (error) {
    console.error("Error processing API response:", error);
    return {
      marketTrends: "Error processing business information.",
      competitorResearch: "Error processing market research data.",
      swotAnalysis: "Error processing SWOT analysis.",
      simulate: "Error processing simulation data.",
      graphs: "Error processing graph data."
    };
  }
};