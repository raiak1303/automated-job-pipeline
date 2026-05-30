# Email notification system for job pipeline

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List
from datetime import datetime
from job_model import Job
from config import EMAIL_CONFIG, OUTPUT_FILE
import os


class EmailNotifier:
    """Send job listings via email"""
    
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = EMAIL_CONFIG.get("smtp_port", 587)
        self.sender_email = EMAIL_CONFIG.get("sender_email")
        self.sender_password = EMAIL_CONFIG.get("sender_password")
        self.recipient_emails = EMAIL_CONFIG.get("recipient_emails", [])
    
    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return (
            self.sender_email and 
            self.sender_password and 
            self.recipient_emails and
            EMAIL_CONFIG.get("enabled", False)
        )
    
    def send_jobs_report(self, jobs: List[Job], excel_file: str = None):
        """Send job listings via email"""
        
        if not self.is_configured():
            print("⚠️  Email not configured. Skipping email notification.")
            print("    Configure EMAIL_CONFIG in config.py and set 'enabled': True")
            return False
        
        try:
            # Create email message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = self._get_subject()
            msg["From"] = self.sender_email
            msg["To"] = ", ".join(self.recipient_emails)
            
            # Create HTML email body
            html_body = self._generate_html_body(jobs)
            msg.attach(MIMEText(html_body, "html"))
            
            # Attach Excel file if available
            if excel_file and os.path.exists(excel_file):
                self._attach_file(msg, excel_file)
            
            # Send email
            print(f"\n📧 Sending email to {len(self.recipient_emails)} recipient(s)...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print("✓ Email sent successfully!")
            return True
            
        except Exception as e:
            print(f"✗ Error sending email: {e}")
            print("\nTroubleshooting:")
            print("  - Gmail: Use 'App Password' (not regular password)")
            print("  - Verify sender_email and sender_password in config.py")
            print("  - Check 'Less secure app access' is enabled (if using Gmail)")
            return False
    
    def _get_subject(self) -> str:
        """Generate email subject"""
        from config import EMAIL_CONFIG
        template = EMAIL_CONFIG.get("subject_template", "🎯 New Job Opportunities - {date}")
        return template.format(date=datetime.now().strftime("%B %d, %Y"))
    
    def _generate_html_body(self, jobs: List[Job]) -> str:
        """Generate HTML email body"""
        
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <div style="max-width: 900px; margin: 0 auto;">
                    
                    <!-- Header -->
                    <div style="background-color: #4472C4; color: white; padding: 20px; text-align: center; border-radius: 5px;">
                        <h1 style="margin: 0; font-size: 24px;">🎯 Job Opportunities Available</h1>
                        <p style="margin: 10px 0 0 0; font-size: 14px;">Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    </div>
                    
                    <!-- Summary -->
                    <div style="background-color: #f5f5f5; padding: 15px; margin: 20px 0; border-radius: 5px;">
                        <h2 style="margin: 0; color: #4472C4; font-size: 18px;">📊 Summary</h2>
                        <p style="margin: 10px 0; font-size: 14px;">
                            <strong>Total Opportunities:</strong> {len(jobs)} jobs found<br>
                            <strong>Filters Applied:</strong> Gulf/Europe • $1500+ USD • On-site/Hybrid/Remote
                        </p>
                    </div>
                    
                    <!-- Jobs Table -->
                    <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                        <thead>
                            <tr style="background-color: #4472C4; color: white;">
                                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Position</th>
                                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Company</th>
                                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Location</th>
                                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Salary</th>
                                <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">Type</th>
                            </tr>
                        </thead>
                        <tbody>
                            {self._generate_job_rows(jobs)}
                        </tbody>
                    </table>
                    
                    <!-- Call to Action -->
                    <div style="background-color: #f0f0f0; padding: 15px; margin: 20px 0; border-left: 4px solid #4472C4; border-radius: 3px;">
                        <p style="margin: 0; font-size: 14px;">
                            <strong>Next Steps:</strong><br>
                            1. Review the attached Excel file for detailed information and URLs<br>
                            2. Click on job links to apply<br>
                            3. Customize your search criteria in config.py<br>
                            4. This report will be sent automatically daily
                        </p>
                    </div>
                    
                    <!-- Footer -->
                    <div style="background-color: #f9f9f9; padding: 15px; margin-top: 20px; border-top: 1px solid #ddd; text-align: center; font-size: 12px; color: #666;">
                        <p style="margin: 0;">
                            This is an automated report from your Job Pipeline<br>
                            Configure email settings in config.py to customize notifications
                        </p>
                    </div>
                    
                </div>
            </body>
        </html>
        """
        return html
    
    def _generate_job_rows(self, jobs: List[Job]) -> str:
        """Generate HTML table rows for jobs"""
        rows = ""
        for i, job in enumerate(jobs[:50]):  # Limit to 50 jobs in email
            bg_color = "#f9f9f9" if i % 2 == 0 else "#ffffff"
            salary_str = f"${job.salary:,.0f}" if job.salary else "Not specified"
            
            rows += f"""
            <tr style="background-color: {bg_color};">
                <td style="padding: 12px; border: 1px solid #ddd;"><strong>{job.title}</strong></td>
                <td style="padding: 12px; border: 1px solid #ddd;">{job.company}</td>
                <td style="padding: 12px; border: 1px solid #ddd;">{job.location}</td>
                <td style="padding: 12px; border: 1px solid #ddd;">{salary_str}</td>
                <td style="padding: 12px; border: 1px solid #ddd;">{job.work_type}</td>
            </tr>
            """
        
        if len(jobs) > 50:
            rows += f"""
            <tr style="background-color: #f0f0f0;">
                <td colspan="5" style="padding: 12px; text-align: center; border: 1px solid #ddd;">
                    ... and {len(jobs) - 50} more jobs. See attached Excel file for complete list.
                </td>
            </tr>
            """
        
        return rows
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach Excel file to email"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(file_path)}",
            )
            msg.attach(part)
            print(f"✓ Attached Excel file: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"⚠️  Could not attach file: {e}")


class EmailTemplate:
    """Email template generator"""
    
    @staticmethod
    def generate_plain_text(jobs: List[Job]) -> str:
        """Generate plain text email"""
        text = f"""
JOB OPPORTUNITIES REPORT
{"="*60}
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

SUMMARY:
Total Jobs Found: {len(jobs)}

OPPORTUNITIES:
"""
        for i, job in enumerate(jobs[:50], 1):
            salary_str = f"${job.salary:,.0f}" if job.salary else "Not specified"
            text += f"""
{i}. {job.title}
   Company: {job.company}
   Location: {job.location}
   Salary: {salary_str}
   Type: {job.work_type}
   Source: {job.source}
   URL: {job.url}
"""
        
        if len(jobs) > 50:
            text += f"\n... and {len(jobs) - 50} more jobs. See attached Excel file for complete list.\n"
        
        text += f"""
{"="*60}
Next Steps:
1. Review the attached Excel file
2. Click on URLs to apply
3. This report is sent automatically daily

Happy job hunting!
"""
        return text
