#!/usr/bin/env python3
"""
Test script for AI Criminal Justice News Scraper
Tests the scraper functionality without sending emails.
"""

import json
import os
from news_scraper import NewsSearcher, NewsDatabase


def test_search():
    """Test the news search functionality."""
    print("="*60)
    print("Testing News Search")
    print("="*60)

    searcher = NewsSearcher()
    articles = searcher.search_all_sources()

    print(f"\nFound {len(articles)} articles:\n")

    for i, article in enumerate(articles[:10], 1):  # Show first 10
        print(f"{i}. {article['title']}")
        print(f"   Source: {article.get('source', 'Unknown')}")
        print(f"   URL: {article['url']}")
        print(f"   Published: {article.get('published', 'N/A')}")
        print()

    if len(articles) > 10:
        print(f"... and {len(articles) - 10} more articles")

    return articles


def test_database(articles):
    """Test database functionality."""
    print("\n" + "="*60)
    print("Testing Database")
    print("="*60)

    # Use a test database
    db = NewsDatabase("test_articles.db")

    # Save articles
    print(f"\nSaving {len(articles)} articles to test database...")
    db.save_articles(articles[:5])  # Save first 5 for testing

    # Check for duplicates
    if articles:
        print(f"\nChecking if first article is in database...")
        is_sent = db.is_article_sent(articles[0]['url'])
        print(f"Article found in database: {is_sent}")

    print("\nTest database created: test_articles.db")
    print("(Delete this file after testing)")


def test_config():
    """Test configuration file."""
    print("\n" + "="*60)
    print("Testing Configuration")
    print("="*60)

    if not os.path.exists('config.json'):
        print("\n❌ config.json not found!")
        print("\nPlease create config.json from config.example.json:")
        print("  cp config.example.json config.json")
        print("  # Then edit config.json with your email settings")
        return False

    with open('config.json', 'r') as f:
        config = json.load(f)

    print("\n✅ config.json found")

    # Check email config
    email_config = config.get('email', {})
    checks = {
        'SMTP Server': email_config.get('smtp_server'),
        'SMTP Port': email_config.get('smtp_port'),
        'Sender Email': email_config.get('sender_email'),
        'Sender Password': email_config.get('sender_password'),
        'Recipient Email': email_config.get('recipient_email'),
    }

    print("\nConfiguration check:")
    all_ok = True
    for key, value in checks.items():
        if value and value not in ['your-email@gmail.com', 'your-app-password']:
            print(f"  ✅ {key}: configured")
        else:
            print(f"  ❌ {key}: NOT configured or using default")
            all_ok = False

    if all_ok:
        print("\n✅ Configuration looks good!")
        print("\nYou can now run the scraper with:")
        print("  python3 news_scraper.py")
    else:
        print("\n⚠️  Please complete your configuration in config.json")

    return all_ok


def main():
    """Run all tests."""
    print("AI Criminal Justice News Scraper - Test Suite")
    print()

    # Test configuration
    config_ok = test_config()

    # Test search
    try:
        articles = test_search()
    except Exception as e:
        print(f"\n❌ Error during search test: {e}")
        articles = []

    # Test database
    if articles:
        try:
            test_database(articles)
        except Exception as e:
            print(f"\n❌ Error during database test: {e}")

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    if config_ok and articles:
        print("\n✅ All tests passed!")
        print("\nNext steps:")
        print("1. Review the articles found above")
        print("2. Run the scraper manually: python3 news_scraper.py")
        print("3. Check your email for the digest")
        print("4. Set up daily automation (see README.md)")
    elif not config_ok:
        print("\n⚠️  Configuration needs attention")
        print("Please complete config.json setup")
    elif not articles:
        print("\n⚠️  No articles found")
        print("This might be temporary - try again later")
    else:
        print("\n⚠️  Some tests failed")
        print("Please review error messages above")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
