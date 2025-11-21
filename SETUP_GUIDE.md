# Simple Setup Guide - AI Criminal Justice News Scraper

Follow these steps exactly to get your daily news emails working.

## Step 1: Install Python Requirements

Open a terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

Wait for it to finish. You should see messages about installing `requests`, `feedparser`, and `schedule`.

---

## Step 2: Get a Gmail App Password

You need a special password from Google (NOT your regular Gmail password):

1. **Go to your Google Account**: https://myaccount.google.com/

2. **Click "Security"** in the left menu

3. **Turn on 2-Step Verification** (if not already on):
   - Click "2-Step Verification"
   - Follow the prompts to set it up

4. **Create an App Password**:
   - Go back to Security page
   - Click "App passwords" (near the bottom)
   - In the "Select app" dropdown, choose **"Mail"**
   - In the "Select device" dropdown, choose **"Other"** and type "News Scraper"
   - Click **"Generate"**
   - Google will show you a 16-character password (looks like: `abcd efgh ijkl mnop`)
   - **COPY THIS PASSWORD** - you'll need it in the next step

---

## Step 3: Create Your Configuration File

1. **Copy the example file**:
   ```bash
   cp config.example.json config.json
   ```

2. **Open `config.json` in a text editor** (like Notepad, TextEdit, VS Code, etc.)

3. **Replace these values**:

   ```json
   {
     "email": {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "sender_email": "PUT_YOUR_GMAIL_HERE@gmail.com",
       "sender_password": "PUT_YOUR_16_CHAR_APP_PASSWORD_HERE",
       "recipient_email": "jessesrothman@gmail.com"
     },
     "database_path": "news_articles.db",
     "send_empty_digest": false
   }
   ```

   **Example** (with fake data):
   ```json
   {
     "email": {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "sender_email": "john.smith@gmail.com",
       "sender_password": "abcd efgh ijkl mnop",
       "recipient_email": "jessesrothman@gmail.com"
     },
     "database_path": "news_articles.db",
     "send_empty_digest": false
   }
   ```

4. **Save the file**

---

## Step 4: Test It!

Run the test script to make sure everything works:

```bash
python3 test_scraper.py
```

You should see:
- ✅ Configuration looks good
- A list of news articles it found
- Messages about testing the database

If you see errors, double-check your config.json file.

---

## Step 5: Send Your First Email

Run the scraper manually:

```bash
python3 news_scraper.py
```

You should see:
- Messages about searching for articles
- "Email sent successfully to jessesrothman@gmail.com"

**Check your email!** You should have received the news digest.

---

## Step 6: Set Up Daily Automation

Now make it run automatically every day. Choose ONE option:

### Option A: For Mac/Linux (Cron - Recommended)

Run this command:
```bash
chmod +x setup_cron.sh
./setup_cron.sh
```

Done! It will now run every day at 9:00 AM.

**To change the time:**
1. Type: `crontab -e`
2. Find the line with `news_scraper.py`
3. Change `0 9` to your preferred time (e.g., `0 17` for 5 PM)
4. Save and exit

### Option B: For Windows (Task Scheduler)

1. Open **Task Scheduler** (search for it in Start menu)
2. Click **"Create Basic Task"** in the right panel
3. Name it: "AI News Scraper"
4. Click **Next**
5. Choose **"Daily"**, click **Next**
6. Set your preferred time (e.g., 9:00 AM), click **Next**
7. Choose **"Start a program"**, click **Next**
8. For "Program/script", browse to `python.exe` (usually `C:\Python\python.exe`)
9. For "Add arguments", enter the full path to `news_scraper.py` (e.g., `C:\Users\YourName\testing\news_scraper.py`)
10. For "Start in", enter the folder containing the script (e.g., `C:\Users\YourName\testing`)
11. Click **Next**, then **Finish**

### Option C: Keep Python Running (Any OS)

Run this command and leave it running:
```bash
python3 run_daily.py
```

It will run the scraper immediately, then again every day at 9:00 AM.

To run it in the background on Mac/Linux:
```bash
nohup python3 run_daily.py &
```

---

## You're Done! 🎉

You should now receive a daily email at jessesrothman@gmail.com with all the latest AI criminal justice news.

---

## Quick Troubleshooting

**Problem: "Authentication failed" or email not sending**
- Make sure you used the 16-character app password (NOT your regular Gmail password)
- Check that 2-Step Verification is enabled
- Verify the sender_email is correct

**Problem: "No module named 'requests'" or similar**
- Run: `pip install -r requirements.txt` again
- Or try: `pip3 install -r requirements.txt`

**Problem: No articles found**
- This can happen occasionally - try running it again later
- Check your internet connection

**Problem: Articles repeating in emails**
- Delete the database file: `rm news_articles.db`
- It will rebuild automatically

---

## Need Help?

Check the full README.md for more detailed information and advanced options.
