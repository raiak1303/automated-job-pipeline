# Task scheduler for automatic pipeline execution

import time
from datetime import datetime
from typing import Callable
from config import SCHEDULER_CONFIG
import threading


class SimpleScheduler:
    """Simple cross-platform scheduler (no external dependencies)"""
    
    def __init__(self):
        self.is_running = False
        self.schedule_time = SCHEDULER_CONFIG.get("schedule_time", "09:00")
        self.timezone = SCHEDULER_CONFIG.get("timezone", "UTC")
    
    def schedule_daily(self, job_func: Callable, run_time: str = None):
        """
        Schedule a job to run daily at specified time
        
        Args:
            job_func: Function to execute
            run_time: Time in HH:MM format (24-hour), e.g., "09:00"
        """
        if run_time is None:
            run_time = self.schedule_time
        
        self.is_running = True
        
        print(f"⏰ Scheduler started - Running daily at {run_time}")
        print(f"   Timezone: {self.timezone}")
        print(f"   Press Ctrl+C to stop scheduler\n")
        
        try:
            while self.is_running:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                
                # Check if it's time to run
                if current_time == run_time:
                    print(f"🚀 Scheduled job triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    try:
                        job_func()
                    except Exception as e:
                        print(f"✗ Job execution failed: {e}")
                        import traceback
                        traceback.print_exc()
                    
                    # Wait 61 seconds to avoid running multiple times in same minute
                    time.sleep(61)
                else:
                    # Check every 30 seconds
                    time.sleep(30)
        
        except KeyboardInterrupt:
            print("\n⏸️  Scheduler stopped by user")
            self.is_running = False
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        print("Scheduler stopped")


class APSchedulerWrapper:
    """APScheduler-based scheduler (more reliable)
    
    To use this, install: pip install apscheduler
    """
    
    def __init__(self):
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            self.scheduler = BackgroundScheduler()
            self.available = True
        except ImportError:
            print("⚠️  APScheduler not installed. Install with: pip install apscheduler")
            self.scheduler = None
            self.available = False
    
    def schedule_daily(self, job_func: Callable, run_time: str = "09:00"):
        """Schedule job to run daily at specified time"""
        if not self.available:
            print("APScheduler not available. Use SimpleScheduler instead.")
            return False
        
        try:
            hour, minute = map(int, run_time.split(":"))
            
            self.scheduler.add_job(
                job_func,
                'cron',
                hour=hour,
                minute=minute,
                id='daily_job_pipeline'
            )
            
            self.scheduler.start()
            print(f"✓ APScheduler started - Running daily at {run_time}")
            
            return True
        except Exception as e:
            print(f"✗ Error setting up APScheduler: {e}")
            return False
    
    def is_running(self) -> bool:
        """Check if scheduler is running"""
        return self.scheduler and self.scheduler.running
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler:
            self.scheduler.shutdown()
            print("Scheduler stopped")


def create_scheduler(prefer_apscheduler: bool = False):
    """Factory function to create appropriate scheduler
    
    Args:
        prefer_apscheduler: If True, try to use APScheduler first
    
    Returns:
        Scheduler instance
    """
    if prefer_apscheduler:
        scheduler = APSchedulerWrapper()
        if scheduler.available:
            return scheduler
        print("Falling back to SimpleScheduler...")
    
    return SimpleScheduler()
