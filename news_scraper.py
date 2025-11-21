#!/usr/bin/env python3
"""
AI Criminal Justice News Scraper
Searches for news about AI in criminal justice (law enforcement, courts, corrections)
and sends daily email digest with links to relevant articles.
"""

import os
import sys
import json
import hashlib
import sqlite3
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Set
import feedparser
import time


class NewsDatabase:
    """Manages SQLite database for tracking articles."""

    def __init__(self, db_path: str = "news_articles.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url_hash TEXT UNIQUE NOT NULL,
                url TEXT NOT NULL,
                title TEXT NOT NULL,
                source TEXT,
                published_date TEXT,
                found_date TEXT NOT NULL,
                sent_date TEXT
            )
        """)
        conn.commit()
        conn.close()

    def get_url_hash(self, url: str) -> str:
        """Generate hash for URL to detect duplicates."""
        return hashlib.md5(url.encode()).hexdigest()

    def is_article_sent(self, url: str) -> bool:
        """Check if article has already been sent."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        url_hash = self.get_url_hash(url)
        cursor.execute("SELECT sent_date FROM articles WHERE url_hash = ?", (url_hash,))
        result = cursor.fetchone()
        conn.close()
        return result is not None and result[0] is not None

    def save_articles(self, articles: List[Dict], mark_sent: bool = False):
        """Save articles to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for article in articles:
            url_hash = self.get_url_hash(article['url'])
            sent_date = datetime.now().isoformat() if mark_sent else None

            try:
                cursor.execute("""
                    INSERT INTO articles (url_hash, url, title, source, published_date, found_date, sent_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    url_hash,
                    article['url'],
                    article['title'],
                    article.get('source', 'Unknown'),
                    article.get('published', ''),
                    datetime.now().isoformat(),
                    sent_date
                ))
            except sqlite3.IntegrityError:
                # Article already exists, update sent_date if marking as sent
                if mark_sent:
                    cursor.execute("""
                        UPDATE articles SET sent_date = ? WHERE url_hash = ?
                    """, (sent_date, url_hash))

        conn.commit()
        conn.close()


class NewsSearcher:
    """Searches for news articles about AI in criminal justice."""

    def __init__(self):
        self.search_queries = [
            "artificial intelligence criminal justice legislation",
            "AI law enforcement policy",
            "AI courts sentencing",
            "AI corrections prisons",
            "facial recognition policing law",
            "predictive policing AI policy",
            "AI bias criminal justice reform",
            "algorithmic sentencing legislation",
        ]

    def search_google_news_rss(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search Google News RSS feeds."""
        articles = []

        # Google News RSS feed URL
        encoded_query = requests.utils.quote(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

        try:
            feed = feedparser.parse(rss_url)

            for entry in feed.entries[:max_results]:
                articles.append({
                    'title': entry.title,
                    'url': entry.link,
                    'source': entry.get('source', {}).get('title', 'Google News'),
                    'published': entry.get('published', ''),
                    'description': entry.get('summary', '')
                })
        except Exception as e:
            print(f"Error fetching RSS feed for '{query}': {e}")

        return articles

    def search_all_sources(self) -> List[Dict]:
        """Search all configured sources and return combined results."""
        all_articles = []

        print(f"Starting news search at {datetime.now().isoformat()}")

        for query in self.search_queries:
            print(f"Searching for: {query}")
            articles = self.search_google_news_rss(query, max_results=5)
            all_articles.extend(articles)
            time.sleep(1)  # Be respectful with requests

        # Remove duplicates based on URL
        unique_articles = {}
        for article in all_articles:
            url = article['url']
            if url not in unique_articles:
                unique_articles[url] = article

        print(f"Found {len(unique_articles)} unique articles")
        return list(unique_articles.values())


class EmailSender:
    """Sends email digests of news articles."""

    def __init__(self, smtp_server: str, smtp_port: int, sender_email: str,
                 sender_password: str, recipient_email: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def create_html_email(self, articles: List[Dict]) -> str:
        """Create HTML formatted email body."""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                h1 { color: #2c3e50; }
                h2 { color: #34495e; font-size: 1.2em; margin-top: 20px; }
                .article {
                    margin-bottom: 25px;
                    padding: 15px;
                    border-left: 3px solid #3498db;
                    background-color: #f8f9fa;
                }
                .article-title {
                    font-weight: bold;
                    color: #2980b9;
                    font-size: 1.1em;
                }
                .article-source {
                    color: #7f8c8d;
                    font-size: 0.9em;
                    margin-top: 5px;
                }
                .article-date {
                    color: #95a5a6;
                    font-size: 0.85em;
                }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .footer {
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #bdc3c7;
                    color: #7f8c8d;
                    font-size: 0.9em;
                }
            </style>
        </head>
        <body>
            <h1>🤖 AI & Criminal Justice News Digest</h1>
            <p><strong>Date:</strong> {date}</p>
            <p>Here are the latest news articles about artificial intelligence in criminal justice,
            covering law enforcement, courts, and corrections:</p>
            <hr>
        """.format(date=datetime.now().strftime("%B %d, %Y"))

        if not articles:
            html += """
            <p><em>No new articles found today.</em></p>
            """
        else:
            for i, article in enumerate(articles, 1):
                html += f"""
                <div class="article">
                    <div class="article-title">{i}. {article['title']}</div>
                    <div class="article-source">Source: {article.get('source', 'Unknown')}</div>
                    {f"<div class='article-date'>Published: {article.get('published', 'N/A')}</div>" if article.get('published') else ""}
                    <div style="margin-top: 10px;">
                        <a href="{article['url']}" target="_blank">Read Full Article →</a>
                    </div>
                </div>
                """

        html += """
            <div class="footer">
                <p>This automated digest searches for news about AI in criminal justice including:</p>
                <ul>
                    <li>Legislation and policy proposals</li>
                    <li>Law enforcement technology</li>
                    <li>Court systems and sentencing algorithms</li>
                    <li>Corrections and prison technology</li>
                    <li>Privacy, bias, and reform discussions</li>
                </ul>
                <p><em>To unsubscribe or modify settings, update your configuration.</em></p>
            </div>
        </body>
        </html>
        """

        return html

    def send_email(self, articles: List[Dict]) -> bool:
        """Send email digest."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            msg['Subject'] = f"AI Criminal Justice News Digest - {datetime.now().strftime('%B %d, %Y')} ({len(articles)} articles)"

            # Create HTML content
            html_content = self.create_html_email(articles)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            # Send email
            print(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            print(f"Email sent successfully to {self.recipient_email}")
            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False


class NewsScraperApp:
    """Main application coordinator."""

    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.db = NewsDatabase(self.config.get('database_path', 'news_articles.db'))
        self.searcher = NewsSearcher()

        email_config = self.config.get('email', {})
        self.emailer = EmailSender(
            smtp_server=email_config.get('smtp_server', 'smtp.gmail.com'),
            smtp_port=email_config.get('smtp_port', 587),
            sender_email=email_config.get('sender_email', ''),
            sender_password=email_config.get('sender_password', ''),
            recipient_email=email_config.get('recipient_email', '')
        )

    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            print(f"Warning: Config file {config_path} not found. Using defaults.")
            return {}

    def run(self):
        """Execute the main scraping and email workflow."""
        print("="*60)
        print("AI Criminal Justice News Scraper")
        print("="*60)

        # Search for articles
        all_articles = self.searcher.search_all_sources()

        # Filter out articles already sent
        new_articles = [
            article for article in all_articles
            if not self.db.is_article_sent(article['url'])
        ]

        print(f"New articles to send: {len(new_articles)}")

        # Send email if there are new articles or if configured to send empty digests
        send_empty = self.config.get('send_empty_digest', False)

        if new_articles or send_empty:
            success = self.emailer.send_email(new_articles)

            if success and new_articles:
                # Mark articles as sent
                self.db.save_articles(new_articles, mark_sent=True)
                print(f"Successfully sent digest with {len(new_articles)} articles")
            elif success:
                print("Sent empty digest")
        else:
            print("No new articles found. Skipping email.")

        print("="*60)
        print("Scraper run completed")
        print("="*60)


def main():
    """Main entry point."""
    config_path = os.environ.get('NEWS_SCRAPER_CONFIG', 'config.json')

    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found!")
        print("Please create a config.json file with your email settings.")
        print("See config.example.json for template.")
        sys.exit(1)

    app = NewsScraperApp(config_path)
    app.run()


if __name__ == "__main__":
    main()
