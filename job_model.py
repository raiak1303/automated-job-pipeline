# Data models for jobs

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Job:
    """Standardized job listing - Enhanced v2"""
    title: str
    company: str
    location: str
    salary: Optional[float] = None       # Removed as required — kept optional
    currency: str = "USD"
    work_type: str = "Not specified"
    url: str = ""
    apply_url: str = ""                  # Direct apply link
    company_website: str = ""            # Company website
    recruiter_name: str = ""             # Recruiter name if available
    recruiter_email: str = ""            # Recruiter email if available
    recruiter_url: str = ""              # Recruiter LinkedIn/profile URL
    description: str = ""
    source: str = ""
    posted_date: Optional[str] = None

    def __hash__(self):
        return hash((self.title, self.company, self.location, self.url))

    def __eq__(self, other):
        if not isinstance(other, Job):
            return False
        return (self.title == other.title and
                self.company == other.company and
                self.location == other.location and
                self.url == other.url)

    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "work_type": self.work_type,
            "apply_url": self.apply_url or self.url,
            "company_website": self.company_website,
            "recruiter_name": self.recruiter_name,
            "recruiter_email": self.recruiter_email,
            "recruiter_url": self.recruiter_url,
            "source": self.source,
            "posted_date": self.posted_date,
            "description": self.description[:200] if self.description else "",
        }
