export default function TabBox() {
    return (
      <Tabs.Root defaultValue="thinking">
        <Tabs.List>
          <Tabs.Trigger value="thinking">
            Thinking
          </Tabs.Trigger>
          <Tabs.Trigger value="graphs">
            Graphs
          </Tabs.Trigger>
          <Tabs.Trigger value="swot">
            SWOT
          </Tabs.Trigger>
          <Tabs.Trigger value="business">
            Business
          </Tabs.Trigger>
          <Tabs.Trigger value="market">
            Market
          </Tabs.Trigger>
        </Tabs.List>

        <Tabs.Content value="thinking">
            Live thinking tree of the agents 
            <ThinkingTreeChart/>
        </Tabs.Content>
        <Tabs.Content value="graphs">Graphs</Tabs.Content>
        <Tabs.Content value="swot">Strengths, Weaknesses, Opporunity, and Threats Analysis</Tabs.Content>
        <Tabs.Content value="business">Business Documents</Tabs.Content>
        <Tabs.Content value="market">Market Analysis</Tabs.Content>

      </Tabs.Root>
    )
}

  