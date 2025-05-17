# ContexQ-PoC: News Feed Entity & Sentiment Graph Pipeline

This project is a proof-of-concept (PoC) pipeline that fetches news articles from multiple RSS feeds, extracts key information using NLP, analyzes relationships between entities, and visualizes the results as an interactive network graph.

## What Does It Do?

1. **Fetches News Articles**: Downloads the latest articles from several business and world news RSS feeds (Reuters, BBC, Al Jazeera, CNA).
2. **Extracts Entities & Events**: Uses spaCy and Hugging Face models to find important people, organizations, and events in each article.
3. **Analyzes Sentiment**: Determines if the article's summary is positive, negative, or neutral.
4. **Builds a Relationship Graph**: Creates a network graph showing how often entities appear together in the news.
5. **Finds Key Entities**: Identifies the most connected (important) entities, especially those linked to negative news.
6. **Visualizes the Network**: Generates an interactive HTML graph showing the top negative sentiment hubs and their connections.

## How the Pipeline Works

1. **Configuration**: The `config.yaml` file lists the news sources and model settings.
2. **Ingestion**: The pipeline fetches and deduplicates articles from the RSS feeds.
3. **NLP Processing**: For each article, it extracts entities, events, and sentiment.
4. **Graph Construction**: Entities that appear together are connected in a graph. Only strong connections (co-occurring at least twice) are kept.
5. **Analysis**: Calculates which entities are most central and detects communities.
6. **Visualization**: The top 5 most central entities with negative sentiment are visualized in `viz.html`.

## Output Files
- `records.json`: All processed articles with extracted entities, events, and sentiment.
- `graph.gexf`: The full entity co-occurrence graph (for use in Gephi, etc.).
- `viz.html`: Interactive visualization of the top negative sentiment hubs.

## How to Run
1. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Pipeline**:
   ```bash
   python run_pipeline.py
   ```
3. **View Results**:
   - Open `viz.html` in your browser to explore the network graph.
   - Check `records.json` and `graph.gexf` for data outputs.

## Project Structure
- `run_pipeline.py`: Main script to run the full process.
- `ingestion/ingest.py`: Fetches and parses RSS feeds.
- `nlp/extract.py`: Extracts entities, events, and sentiment.
- `graph/build_and_analyze.py`: Builds and analyzes the entity graph.
- `viz/visualize.py`: Creates the interactive visualization.
- `config.yaml`: Configuration for feeds and models.

## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies (spaCy, transformers, pyvis, pandas, etc.)

## Notes
- The pipeline is designed for demonstration and exploration. It can be extended with more feeds, custom event patterns, or advanced analytics.
- The visualization focuses on negative sentiment hubs to help spot potential issues or risks in the news.

---

**Simple Summary:**
> This project helps you see which companies or people are most often mentioned together in the news, especially in negative stories. It fetches news, finds important names, checks the mood, and shows the results as a network you can explore in your browser.
