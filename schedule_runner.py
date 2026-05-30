#!/usr/bin/env python
"""
Scheduled Job Pipeline Runner
Runs the pipeline automatically at specified time daily and sends email notifications
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime
from scheduler import create_scheduler, SimpleScheduler
from config import SCHEDULER_CONFIG, SEND_EMAIL_ON_RUN
from email_notifier import EmailNotifier


def install_dependencies():
    """Install required packages"""
    print("📦 Checking dependencies...")
    
    required = {
        "requests": "requests",
        "beautifulsoup4": "bs4",
        "openpyxl": "openpyxl",
    }
    
    missing = []
    for package, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"   Installing {', '.join(missing)}...")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
        print("   ✓ Dependencies installed")
    else:
        print("   ✓ All dependencies installed")


def run_pipeline():
    """Run the job pipeline"""
    try:
        from pipeline import JobPipeline
        
        print(f"\n🚀 Running pipeline at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        pipeline = JobPipeline()
        pipeline.run()
        
        return True
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def verify_email_config():
    """Verify email configuration before scheduling"""
    from config import EMAIL_CONFIG
    
    if not SEND_EMAIL_ON_RUN:
        return True
    
    if not EMAIL_CONFIG.get("enabled"):
        print("\n⚠️  Email notifications are disabled in config.py")
        print("   To enable emails:")
        print("   1. Edit config.py")
        print("   2. Set EMAIL_CONFIG['enabled'] = True")
        print("   3. Configure SMTP settings for your email provider")
        return False
    
    if not (EMAIL_CONFIG.get("sender_email") and EMAIL_CONFIG.get("sender_password")):
        print("\n⚠️  Email credentials not configured in config.py")
        print("   Set sender_email and sender_password in EMAIL_CONFIG")
        return False
    
    print("   ✓ Email configuration valid")
    return True


def main():
    """Main entry point"""
    print("="*60)
    print("🎯 SCHEDULED JOB PIPELINE")
    print("="*60)
    print()
    
    # Install dependencies
    install_dependencies()
    
    # Verify email config
    if SEND_EMAIL_ON_RUN:
        print("\n📧 Email Configuration:")
        if not verify_email_config():
            print("\n💡 Continue with scheduled runs but without email?")
            response = input("   Type 'yes' to continue, or 'no' to exit: ").strip().lower()
            if response != 'yes':
                print("Exiting...")
                return
    
    # Get schedule time
    schedule_time = SCHEDULER_CONFIG.get("schedule_time", "09:00")
    timezone = SCHEDULER_CONFIG.get("timezone", "UTC")
    
    print("\n" + "="*60)
    print("⏰ SCHEDULER SETTINGS")
    print("="*60)
    print(f"   Schedule Time: {schedule_time} daily")
    print(f"   Timezone: {timezone}")
    print(f"   Email Notifications: {'Enabled' if SEND_EMAIL_ON_RUN else 'Disabled'}")
    print()
    print("   Starting scheduler...")
    print("   (Press Ctrl+C to stop)\n")
    
    # Create and start scheduler
    scheduler = create_scheduler(prefer_apscheduler=True)
    scheduler.schedule_daily(run_pipeline, schedule_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Scheduler stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
