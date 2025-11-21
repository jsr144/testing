# AI Criminal Justice News Scraper

An automated news scraper that searches daily for articles about artificial intelligence in the U.S. criminal justice system, covering law enforcement, courts, and corrections. The scraper sends a daily email digest with links to all relevant news stories.

## Features

- 🔍 **Comprehensive Search**: Searches multiple queries related to AI in criminal justice
- 📧 **Daily Email Digest**: Beautifully formatted HTML email with article summaries
- 🗄️ **Duplicate Detection**: SQLite database prevents sending the same article twice
- ⏰ **Automated Scheduling**: Can run via cron job or Python scheduler
- 🎯 **Targeted Topics**: Covers legislation, policy, law enforcement, courts, and corrections

## Topics Covered

The scraper searches for news about:
- AI and criminal justice legislation
- Law enforcement AI technology and policy
- Court systems and algorithmic sentencing
- Corrections and prison technology
- Facial recognition and predictive policing
- AI bias and criminal justice reform

## Requirements

- Python 3.7 or higher
- Internet connection
- Email account (Gmail recommended) with app-specific password

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create configuration file:**
   ```bash
   cp config.example.json config.json
   ```

4. **Edit `config.json` with your email settings:**
   ```json
   {
     "email": {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "sender_email": "your-email@gmail.com",
       "sender_password": "your-app-password",
       "recipient_email": "jessesrothman@gmail.com"
     },
     "database_path": "news_articles.db",
     "send_empty_digest": false
   }
   ```

## Email Setup (Gmail)

If using Gmail, you'll need to create an **App Password**:

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification** (enable if not already)
3. Scroll down to **App passwords**
4. Generate a new app password for "Mail"
5. Use this 16-character password in your `config.json` file

**Note**: Regular Gmail passwords won't work due to security restrictions. You must use an app-specific password.

## Usage

### Manual Run (Test)

Run the scraper once to test:

```bash
python3 news_scraper.py
```

This will:
1. Search for relevant news articles
2. Filter out previously sent articles
3. Send an email digest to the configured recipient
4. Save article records to the database

### Automated Daily Runs

#### Option 1: Python Scheduler (Simple)

Keep the scraper running continuously and it will execute daily at 9:00 AM:

```bash
python3 run_daily.py
```

To run in the background:
```bash
nohup python3 run_daily.py > scraper_output.log 2>&1 &
```

#### Option 2: Cron Job (Recommended for Linux/Mac)

1. **Run the setup script:**
   ```bash
   chmod +x setup_cron.sh
   ./setup_cron.sh
   ```

2. **Or manually add to crontab:**
   ```bash
   crontab -e
   ```

   Add this line (adjust path and time as needed):
   ```
   0 9 * * * cd /path/to/news-scraper && /usr/bin/python3 news_scraper.py >> scraper.log 2>&1
   ```

   This runs the scraper daily at 9:00 AM.

#### Option 3: Windows Task Scheduler

1. Open **Task Scheduler**
2. Create a new **Basic Task**
3. Set trigger to **Daily** at your preferred time
4. Set action to **Start a program**
5. Program: Path to `python.exe`
6. Arguments: Full path to `news_scraper.py`
7. Start in: Directory containing the script

## Configuration Options

Edit `config.json` to customize:

- **smtp_server**: SMTP server address (default: smtp.gmail.com)
- **smtp_port**: SMTP port (default: 587 for TLS)
- **sender_email**: Email address sending the digest
- **sender_password**: App-specific password for the sender email
- **recipient_email**: Email address to receive the digest
- **database_path**: Path to SQLite database file
- **send_empty_digest**: If `true`, sends email even when no new articles found

## Database

The scraper uses SQLite to track articles and prevent duplicates. The database stores:
- Article URLs and titles
- Source and publication dates
- Date article was found
- Date article was sent in digest

To reset the database (resend all articles):
```bash
rm news_articles.db
```

## Customizing Search Queries

Edit the `search_queries` list in `news_scraper.py` (line ~58) to modify what topics are searched:

```python
self.search_queries = [
    "artificial intelligence criminal justice legislation",
    "AI law enforcement policy",
    # Add your own queries here
]
```

## Troubleshooting

### No articles found
- Check your internet connection
- Google News RSS feeds may have rate limiting
- Try running manually to see error messages

### Email not sending
- Verify SMTP settings in `config.json`
- Ensure you're using an app-specific password (not regular password)
- Check if your email provider allows SMTP access
- Review error messages in console/log output

### Permission denied errors
- Make scripts executable: `chmod +x *.py *.sh`
- Ensure Python has write permissions for database file

### Cron job not running
- Check cron logs: `grep CRON /var/log/syslog` (Linux)
- Verify full paths in crontab (don't use relative paths)
- Check if script has execution permissions
- Review scraper.log for errors

## File Structure

```
.
├── news_scraper.py          # Main scraper application
├── run_daily.py             # Python-based daily scheduler
├── setup_cron.sh            # Bash script to setup cron job
├── config.json              # Your configuration (not in git)
├── config.example.json      # Example configuration template
├── requirements.txt         # Python dependencies
├── news_articles.db         # SQLite database (created automatically)
├── README.md                # This file
└── .gitignore              # Git ignore rules
```

## Security Notes

- **Never commit `config.json`** to version control (it contains passwords)
- Use app-specific passwords, not your main email password
- The `.gitignore` file prevents accidental commits of sensitive files
- Store config files with restricted permissions: `chmod 600 config.json`

## License

This project is provided as-is for personal and educational use.

## Contributing

Feel free to submit issues or pull requests to improve the scraper!

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review error messages in console or log files
3. Verify your configuration settings
4. Test email settings with a manual run

---

**Last Updated**: November 2025
