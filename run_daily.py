#!/usr/bin/env python3
"""
Daily scheduler for AI Criminal Justice News Scraper.
This script keeps running and executes the scraper once per day.
For production use, consider using system cron instead.
"""

import schedule
import time
from news_scraper import NewsScraperApp


def job():
    """Job to run daily."""
    try:
        app = NewsScraperApp()
        app.run()
    except Exception as e:
        print(f"Error running scraper: {e}")


def main():
    """Run the scheduler."""
    print("Daily news scraper scheduler started")
    print("Will run every day at 9:00 AM")
    print("Press Ctrl+C to stop")

    # Schedule job to run every day at 9:00 AM
    schedule.every().day.at("09:00").do(job)

    # Run once immediately on startup (optional)
    print("\nRunning initial scrape...")
    job()

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    main()
