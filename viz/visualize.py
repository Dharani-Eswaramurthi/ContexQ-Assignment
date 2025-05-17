from pyvis.network import Network
import logging

def visualize_subgraph(G, nodes, output="viz.html"):
    """
    Visualize a subgraph induced by the given nodes.

    Args:
        G (nx.Graph): The full graph.
        nodes (list or set): Nodes to include in the subgraph.
        output (str): Output HTML file path.
    """
    logging.info(f"Visualizing subgraph with {len(nodes)} nodes...")

    net = Network(height="750px", width="100%", notebook=False)
    sub_nodes = set(nodes)
    sub_edges = [(u, v) for u, v in G.edges() if u in sub_nodes and v in sub_nodes]

    for n in sub_nodes:
        node_attrs = G.nodes[n]
        label = n
        title = f"Type: {node_attrs.get('type', 'N/A')}<br>Dates: {', '.join(sorted(node_attrs.get('dates', [])))}"
        net.add_node(n, label=label, title=title)

    for e1, e2 in sub_edges:
        weight = G.edges[e1, e2].get("weight", 1)
        net.add_edge(e1, e2, value=weight)

    net.write_html(output)
    logging.info(f"Visualization saved to {output}")
