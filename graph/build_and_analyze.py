import networkx as nx
import logging
from networkx.algorithms import community

def build_graph(records, min_cooccurrence=2):
    """
    Build a co-occurrence graph from records.

    Args:
        records (list): List of dicts with 'entities' and 'date'.
        min_cooccurrence (int): Minimum number of co-occurrences to create an edge.

    Returns:
        nx.Graph: Constructed graph.
    """
    logging.info("Building graph from records...")
    G = nx.Graph()
    cooccurrence_counts = {}

    for rec in records:
        entities = [ent for ent, _ in rec.get("entities", []) if ent.strip()]
        date = rec.get("date", "")
        # Add nodes with attributes (date could be a list if multiple articles)
        for ent in entities:
            if G.has_node(ent):
                dates = set(G.nodes[ent].get("dates", "").split(",") if G.nodes[ent].get("dates") else [])
                dates.add(date)
                G.nodes[ent]["dates"] = ",".join(sorted(dates))
            else:
                G.add_node(ent, type="entity", dates=date)



        # Count co-occurrences
        unique_entities = set(entities)
        for e1 in unique_entities:
            for e2 in unique_entities:
                if e1 < e2:
                    cooccurrence_counts[(e1, e2)] = cooccurrence_counts.get((e1, e2), 0) + 1

    # Add edges only if co-occurrence >= min_cooccurrence
    for (e1, e2), count in cooccurrence_counts.items():
        if count >= min_cooccurrence:
            G.add_edge(e1, e2, weight=count)

    logging.info(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def export_gexf(G, path="graph.gexf"):
    logging.info(f"Exporting graph to {path}...")
    nx.write_gexf(G, path)

def analyze_graph(G):
    logging.info("Analyzing graph...")
    deg = nx.degree_centrality(G)
    try:
        comms = community.louvain_communities(G)
        logging.info(f"Detected {len(comms)} communities.")
    except Exception as e:
        logging.warning(f"Community detection failed: {e}")
        comms = []
    return deg, comms
