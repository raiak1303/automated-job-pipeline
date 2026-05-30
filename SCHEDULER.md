# ⏰ SCHEDULING & EMAIL SETUP GUIDE

## Overview

Your job pipeline can now:
- ✅ **Run automatically** every day at a scheduled time
- ✅ **Send email notifications** with job listings
- ✅ **Attach Excel files** with complete job details

---

## 🚀 QUICK START

### Option 1: Python Scheduler (Recommended for Easy Testing)

```bash
python schedule_runner.py
```

This starts a continuous process that runs the pipeline daily at the configured time.

### Option 2: Windows Task Scheduler (Recommended for Production)

See [Windows Task Scheduler Setup](#windows-task-scheduler-setup) below.

---

## 📧 EMAIL SETUP

### Step 1: Enable Email in Config

Edit `config.py` and modify EMAIL_CONFIG:

```python
EMAIL_CONFIG = {
    "enabled": True,  # ← Change to True
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "your-email@gmail.com",  # Your email
    "sender_password": "your-app-password",  # See below
    "recipient_emails": ["recipient1@gmail.com", "recipient2@gmail.com"],
    "subject_template": "🎯 New Job Opportunities - {date}",
}
```

### Step 2: Get Email Credentials

#### For Gmail:
1. Enable 2-Factor Authentication
2. Go to https://myaccount.google.com/apppasswords
3. Create an "App Password"
4. Copy the 16-character password to `sender_password`
5. **Do NOT use your regular Gmail password**

#### For Other Email Providers:
- **Outlook/Hotmail**: Use regular password, `smtp_server: "smtp-mail.outlook.com"`, `smtp_port: 587`
- **Yahoo**: Use app password, `smtp_server: "smtp.mail.yahoo.com"`, `smtp_port: 587`
- **Custom Domain**: Contact your email provider for SMTP details

### Step 3: Test Email Sending

```bash
python -c "
from email_notifier import EmailNotifier
from job_model import Job

notifier = EmailNotifier()
test_job = Job(
    title='Test Job',
    company='Test Company',
    location='Dubai, UAE',
    salary=2000,
    work_type='Hybrid',
    url='https://example.com'
)
notifier.send_jobs_report([test_job])
"
```

Expected output:
```
📧 Sending email to 1 recipient(s)...
✓ Email sent successfully!
```

---

## ⏰ SCHEDULING SETUP

### Configuration

Edit `config.py`:

```python
SCHEDULER_CONFIG = {
    "enabled": True,  # Set to True to enable scheduling
    "schedule_time": "09:00",  # Run daily at 9:00 AM (24-hour format)
    "timezone": "Asia/Dubai",  # Your timezone
}

SEND_EMAIL_ON_RUN = True  # Send email after each run
INCLUDE_EXCEL_ATTACHMENT = True  # Attach Excel file
```

### Option 1: Python Scheduler

**Start the scheduler:**
```bash
python schedule_runner.py
```

**What happens:**
- Runs daily at configured time
- Fetches jobs, filters them
- Sends email if configured
- Generates Excel and database files
- Keep this window/terminal open

**To stop:** Press Ctrl+C

---

### Option 2: Windows Task Scheduler (Recommended for Always-On)

#### Setup Steps:

**Step 1: Open Task Scheduler**
- Press `Win + R`
- Type `taskschd.msc` and press Enter
- Or search for "Task Scheduler"

**Step 2: Create New Task**
- Right-click "Task Scheduler Library"
- Select "Create Basic Task..."
- Name: `Job Pipeline Daily`
- Description: `Automatically run job pipeline and send email notifications`
- Click Next

**Step 3: Set Trigger**
- Select "Daily"
- Set start time (e.g., 9:00 AM)
- Click Next

**Step 4: Set Action**
- Select "Start a program"
- Program/script: `C:\Windows\System32\cmd.exe`
- Arguments: `/c c:\Users\raiak\OneDrive\Desktop\python\pipeline\run_pipeline.bat`
- Start in: `c:\Users\raiak\OneDrive\Desktop\python\pipeline`
- Click Next

**Step 5: Finish**
- Review settings
- Check "Open the Properties dialog for this task when I click Finish"
- Click Finish

**Step 6: Advanced Settings**
In the Properties dialog:
- General tab: Check "Run whether user is logged in or not"
- Triggers tab: Check "Enabled"
- Actions tab: Verify the command

**Step 7: Test**
- Right-click the task
- Select "Run"
- Check if `jobs_report.xlsx` was created
- Check if email was sent

---

## 📋 EMAIL CUSTOMIZATION

### HTML Email Template

The email includes:
- ✅ Formatted table with all jobs
- ✅ Summary statistics
- ✅ Call-to-action buttons
- ✅ Professional branding
- ✅ Footer with next steps

### Customize Subject Line

Edit `config.py`:

```python
EMAIL_CONFIG = {
    # ... other settings ...
    "subject_template": "🎯 Daily Jobs Report - {date}",  # Customize here
}
```

### Add More Recipients

Edit `config.py`:

```python
EMAIL_CONFIG = {
    # ... other settings ...
    "recipient_emails": [
        "you@gmail.com",
        "colleague@company.com",
        "friend@example.com",
    ],
}
```

### Include All Jobs or Limit

The email shows max 50 jobs in the table, but all jobs are in the Excel attachment.

To change:
Edit `email_notifier.py`, line 108:
```python
for i, job in enumerate(jobs[:50]):  # Change 50 to your limit
```

---

## 🐛 TROUBLESHOOTING

### Email Not Sending

**Problem:** "Error sending email: [SMTP ERROR]"

**Solutions:**
1. Check credentials are correct
2. For Gmail: Use 16-character app password (not regular password)
3. Check internet connection
4. Try test first: `python -c "from email_notifier import EmailNotifier; EmailNotifier().send_jobs_report([])"`

### Scheduler Not Starting

**Problem:** "ModuleNotFoundError: No module named 'scheduler'"

**Solution:** Run from pipeline directory:
```bash
cd c:\Users\raiak\OneDrive\Desktop\python\pipeline
python schedule_runner.py
```

### Task Scheduler Task Won't Run

**Problem:** Task shows "Last Run Result: ERROR"

**Solutions:**
1. Right-click task → Properties
2. General tab: Check "Run with highest privileges"
3. Conditions tab: Uncheck "Stop if computer switches to battery power"
4. Run task manually first to test

### No Email Received

**Problem:** Email not arriving in inbox

**Solutions:**
1. Check Spam/Junk folder
2. Verify recipient email is correct
3. Try sending test email first
4. Check if sender email is in contacts

### Logs & Debugging

View pipeline execution log:
```bash
# From pipeline directory
type pipeline_log.txt
```

Or run manually to see detailed output:
```bash
python pipeline.py
```

---

## 📊 SCHEDULED RUNS LOG

The pipeline automatically logs runs to `pipeline_log.txt`:

```
Pipeline executed at 05/28/2024 09:00:15
Pipeline executed at 05/29/2024 09:00:22
...
```

---

## 🔐 SECURITY NOTES

### Email Password Safety

⚠️ **IMPORTANT**: Your `config.py` contains email credentials!

**Protect it:**
1. Never commit to public git repositories
2. Don't share with others
3. Use `.gitignore` to exclude config.py
4. For production: Use environment variables

**Better approach - Use Environment Variables:**

Create `.env` file:
```
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECIPIENTS=recipient@gmail.com
```

Then update `config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_CONFIG = {
    "sender_email": os.getenv("EMAIL_SENDER"),
    "sender_password": os.getenv("EMAIL_PASSWORD"),
    "recipient_emails": os.getenv("EMAIL_RECIPIENTS", "").split(","),
}
```

Install dotenv:
```bash
pip install python-dotenv
```

---

## ⚡ PERFORMANCE

- **Pipeline run time**: 30-60 seconds
- **Email send time**: 2-5 seconds
- **Total time**: ~40-65 seconds

**Scheduled runs don't block other tasks** - Windows will run them in the background.

---

## 📅 SCHEDULE VARIATIONS

### Run Multiple Times Per Day

Edit `schedule_runner.py` to call pipeline multiple times:

```python
def main():
    # ... existing code ...
    
    times = ["08:00", "13:00", "18:00"]  # Morning, afternoon, evening
    for time in times:
        scheduler.schedule_daily(run_pipeline, time)
```

### Run Weekly Instead of Daily

For weekly runs, use Windows Task Scheduler:
- In trigger settings, select "Weekly"
- Choose day of week

### Run Monthly Report

Edit `SCHEDULER_CONFIG` in `config.py` to run once monthly.

---

## 🔄 WORKFLOW

```
Daily at 9:00 AM (or scheduled time)
    ↓
Windows Task Scheduler triggers
    ↓
run_pipeline.bat executes
    ↓
pipeline.py runs
    ↓
Jobs are fetched & filtered
    ↓
jobs_report.xlsx is generated
    ↓
jobs.db is updated
    ↓
Email sent with results
    ↓
pipeline_log.txt is updated
```

---

## 📝 NEXT STEPS

1. **Enable Email**:
   - Edit `config.py`
   - Set `EMAIL_CONFIG["enabled"] = True`
   - Add your email and password

2. **Test Email**:
   - Run: `python schedule_runner.py`
   - Manually trigger to test email

3. **Setup Scheduling**:
   - Use Windows Task Scheduler for automatic runs
   - Or run `python schedule_runner.py` in terminal

4. **Customize Schedule**:
   - Edit `SCHEDULER_CONFIG` in `config.py`
   - Change time, timezone, email template

5. **Monitor**:
   - Check `pipeline_log.txt` for execution log
   - Verify emails are arriving daily

---

## 💡 TIPS

- **Test first**: Run manually before scheduling
- **Check logs**: Review `pipeline_log.txt` for issues
- **Email templates**: Customize subject and recipients in `config.py`
- **Multiple recipients**: Just add more emails to `recipient_emails` list
- **Timezone**: Update `SCHEDULER_CONFIG["timezone"]` for your location

---

## 🎯 YOU'RE ALL SET!

Your job pipeline will now:
✅ Run automatically every day
✅ Send you email notifications
✅ Include formatted job listings
✅ Attach Excel file with full details

Happy automated job hunting! 🚀
