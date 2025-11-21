#!/bin/bash
# Setup script to add daily cron job for news scraper

# Get the absolute path to this script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Python path (adjust if needed)
PYTHON_PATH=$(which python3)

# Cron job to run daily at 9:00 AM
CRON_JOB="0 9 * * * cd $SCRIPT_DIR && $PYTHON_PATH $SCRIPT_DIR/news_scraper.py >> $SCRIPT_DIR/scraper.log 2>&1"

# Check if cron job already exists
crontab -l 2>/dev/null | grep -q "news_scraper.py"

if [ $? -eq 0 ]; then
    echo "Cron job already exists!"
    echo "Current crontab:"
    crontab -l | grep news_scraper.py
else
    # Add cron job
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added successfully!"
    echo "The scraper will run daily at 9:00 AM"
    echo ""
    echo "To view your crontab:"
    echo "  crontab -l"
    echo ""
    echo "To remove the cron job:"
    echo "  crontab -e"
    echo "  (then delete the line with news_scraper.py)"
fi

echo ""
echo "Log file location: $SCRIPT_DIR/scraper.log"
