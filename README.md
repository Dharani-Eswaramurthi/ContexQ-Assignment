# 🚀 ContexQ-PoC: News Entity & Sentiment Graph Pipeline

Welcome to ContexQ-PoC! This project is your backstage pass to understanding how news stories connect people, companies, and events — all visualized as a living network. 🌐✨

## What Does This Project Do? 🤔

1. **Fetches News** 📰  
   Grabs the latest articles from top sources like BBC, Reuters, Al Jazeera, and CNA.

2. **Finds Key Players & Events** 🕵️‍♂️  
   Uses smart NLP (spaCy + Hugging Face) to spot important names, places, and even special events in each article.

3. **Checks the Mood** 😃😐😡  
   Analyzes if the news is positive, negative, or neutral using AI-powered sentiment analysis.

4. **Builds a Relationship Graph** 🕸️  
   Connects entities that appear together, showing who’s in the spotlight and who’s connected to whom.

5. **Highlights the Hot Topics** 🔥  
   Finds the most central (influential) entities, especially those surrounded by negative news.

6. **Visualizes the Network** 🎨  
   Creates an interactive HTML graph so you can explore the news network right in your browser!

---

## How It Works (In Simple Steps) 🛠️

1. **Configure**: Set your news sources and model preferences in `config.yaml`.
2. **Ingest**: The pipeline fetches and cleans up articles from all feeds.
3. **NLP Magic**: For each article, it extracts entities, events, and sentiment.
4. **Graph Time**: Entities that co-occur are linked. Only strong connections (at least 2 co-occurrences) are kept.
5. **Analyze**: Calculates which entities are most central and finds communities.
6. **Visualize**: The top 5 negative sentiment hubs are shown in `viz.html`.

---

## Output Files 📦
- `records.json`: All processed articles with extracted info.
- `graph.gexf`: The full entity co-occurrence graph (for Gephi, etc.).
- `viz.html`: Interactive visualization of the top negative sentiment hubs.
- `outputs/articles.csv`: Raw news articles (if you want to peek under the hood).

---

## How to Run It 🏃‍♂️

1. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Pipeline**
   ```bash
   python run_pipeline.py
   ```
3. **See the Results**
   - Open `viz.html` in your browser to explore the network.
   - Check `records.json` and `graph.gexf` for data.

---

## Project Structure 🗂️
- `run_pipeline.py`: Main script — start here!
- `ingestion/ingest.py`: Fetches and parses RSS feeds.
- `nlp/extract.py`: Extracts entities, events, and sentiment.
- `graph/build_and_analyze.py`: Builds and analyzes the entity graph.
- `viz/visualize.py`: Makes the interactive visualization.
- `config.yaml`: Your config for feeds and models.
- `outputs/articles.csv`: Raw news dump.

---

## Requirements 🧰
- Python 3.8+
- See `requirements.txt` for all the Python goodies (spaCy, transformers, pyvis, pandas, etc.)

---

## Why Use This? 💡
- **Spot trends**: See which people or companies are making headlines — and if it’s for good or bad reasons.
- **Explore connections**: Find out who’s connected in the news, and how.
- **Visual, fun, and insightful**: The interactive graph makes data exploration a breeze.

---

## TL;DR 📝
> This project fetches news, finds important names, checks the mood, and shows you the results as a network you can explore. Perfect for anyone curious about the hidden connections in the news!

---

Made with ❤️ for data explorers, news junkies, and curious minds!
