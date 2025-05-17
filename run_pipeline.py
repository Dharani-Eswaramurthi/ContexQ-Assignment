import json
import logging
from pathlib import Path

from ingestion.ingest import fetch_feeds
from nlp.extract import NLPProcessor
from graph.build_and_analyze import build_graph, analyze_graph, export_gexf
from viz.visualize import visualize_subgraph
import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config

def main():
    try:
        config = load_config()
        feed_urls = list(config.get("feeds", {}).values())
        spacy_model = config.get("spacy_model", "en_core_web_trf")
        sentiment_model = config.get("sentiment_model", "distilbert-base-uncased-finetuned-sst-2-english")
        min_cooccurrence = config.get("min_cooccurrence", 2)

        # 1. Fetch feeds
        logging.info("Fetching feeds...")
        df = fetch_feeds(feed_urls)

        # 2. NLP processing
        logging.info("Initializing NLP processor...")
        nlp_processor = NLPProcessor(spacy_model_name=spacy_model, sentiment_model_name=sentiment_model)

        records = []
        for _, row in df.iterrows():
            try:
                ents, events = nlp_processor.extract_entities_and_events(row["summary"])
                sentiment_label, sentiment_score = nlp_processor.analyze_sentiment(row["summary"])
                records.append({
                    "id": row["id"],
                    "title": row["title"],
                    "summary": row["summary"],
                    "date": row["date"],
                    "entities": ents,
                    "events": events,
                    "sentiment": {"label": sentiment_label, "score": sentiment_score}
                })
            except Exception as e:
                logging.warning(f"Error processing row {row['id']}: {e}")

        # Save records JSON
        output_json = Path("records.json")
        logging.info(f"Saving records to {output_json}...")
        with output_json.open("w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)

        # 3. Build and analyze graph
        logging.info("Building and analyzing graph...")
        G = build_graph(records, min_cooccurrence=min_cooccurrence)
        deg, comms = analyze_graph(G)
        export_gexf(G, "graph.gexf")

        # 4. Visualization: top-5 negative sentiment hub nodes
        logging.info("Selecting top negative sentiment nodes for visualization...")
        # Aggregate sentiment per entity to avoid duplicates
        entity_sentiments = {}
        for rec in records:
            sentiment_label = rec["sentiment"]["label"]
            if sentiment_label != "NEGATIVE":
                continue
            for ent, _ in rec["entities"]:
                # Track max degree and sentiment score per entity
                deg_val = deg.get(ent, 0)
                sentiment_score = rec["sentiment"]["score"]
                if ent not in entity_sentiments or deg_val > entity_sentiments[ent][0]:
                    entity_sentiments[ent] = (deg_val, sentiment_score)

        # Sort by degree centrality descending
        sorted_entities = sorted(entity_sentiments.items(), key=lambda x: x[1][0], reverse=True)
        top_nodes = [ent for ent, _ in sorted_entities[:5]]

        if top_nodes:
            visualize_subgraph(G, top_nodes, output="viz.html")
        else:
            logging.info("No negative sentiment nodes found for visualization.")

        logging.info("Pipeline execution completed successfully.")

    except Exception as e:
        logging.error(f"Pipeline execution failed: {e}")

if __name__ == "__main__":
    main()
