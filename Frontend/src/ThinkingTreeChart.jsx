import React, { useActionState, useState, useEffect } from 'react';
import Tree from 'react-d3-tree';

// This is a simplified example of an org chart with a depth of 2.
// Note how deeper levels are defined recursively via the `children` property.
const thinkingTreeChart = {
    name: 'CEO',
    children: [
        {
            name: 'Manager',
            attributes: {
                department: 'Production',
            },
            children: [
                {
                    name: 'Foreman',
                    attributes: {
                        department: 'Fabrication',
                    },
                    children: [
                        {
                            name: 'Worker',
                        },
                    ],
                },
                {
                    name: 'Foreman',
                    attributes: {
                        department: 'Assembly',
                    },
                    children: [
                        {
                            name: 'Worker',
                        },
                    ],
                },
            ],
        },
    ],
};

export default function ThinkingTreeChart() {
    const [data, setData] = useState([])
    useEffect(() => {
        setData(thinkingTreeChart)
    }, []);

    return (
        <>
            <div id="treeWrapper" style={{ width: '50em', height: '20em' }}>
                <Tree data={thinkingTreeChart} enableLegacyTransitions />
            </div>
        </>
    );
}