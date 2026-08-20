type GraphNode = { id: string; label: string; description?: string };
type GraphEdge = { from: string; to: string; label?: string };

export function NodeGraph({ nodes, edges }: { nodes: GraphNode[]; edges: GraphEdge[] }) {
  const labels = new Map(nodes.map((node) => [node.id, node.label]));
  return <figure className="node-graph">
    <div className="node-graph-nodes">{nodes.map((node) => <article key={node.id} id={`node-${node.id}`}>
      <strong>{node.label}</strong>{node.description ? <p>{node.description}</p> : null}
    </article>)}</div>
    {edges.length > 0 ? <figcaption><ol>{edges.map((edge, index) => <li key={`${edge.from}-${edge.to}-${index}`}>
      <a href={`#node-${edge.from}`}>{labels.get(edge.from) ?? edge.from}</a>
      <span aria-hidden="true">→</span>
      <a href={`#node-${edge.to}`}>{labels.get(edge.to) ?? edge.to}</a>
      {edge.label ? <em>{edge.label}</em> : null}
    </li>)}</ol></figcaption> : null}
  </figure>;
}
