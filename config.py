# ============================================================
# Job Finder v2 - Configuration
# ============================================================

# -----------------------------------------------------------
# API Keys
# -----------------------------------------------------------
ADZUNA_APP_ID  = "id name"
ADZUNA_APP_KEY = "id key"
REED_API_KEY   = "id key"
JOOBLE_API_KEY = "id key"

# -----------------------------------------------------------
# HTTP Headers
# -----------------------------------------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html, */*",
    "Accept-Language": "en-US,en;q=0.9",
}

# -----------------------------------------------------------
# Job Titles
# -----------------------------------------------------------
TARGET_JOB_TITLES = [
    # Original
    "Planning Engineer",
    "Project Control Engineer",
    "Project Engineer",
    "Product Manager",
    "Data Analyst",
    # New
    "PMO Analyst",
    "Project Scheduler",
    "Cost Control Engineer",
    "Project Controller",
    "Digital Planning Engineer",
    "BI Analyst",
    "Reporting Analyst",
    "Business Intelligence Analyst",
    "Planning Manager",
    "Project Manager",
    "Cost Engineer",
    "Schedule Engineer",
    "PMO Manager",
    "Project Controls Manager",
]

# -----------------------------------------------------------
# Target Locations
# -----------------------------------------------------------
TARGET_LOCATIONS_KEYWORDS = [
    # Gulf
    "dubai", "abu dhabi", "uae", "sharjah", "ajman",
    "doha", "qatar",
    "riyadh", "jeddah", "saudi", "ksa",
    "kuwait", "bahrain", "oman", "muscat",
    # Europe
    "london", "uk", "england", "manchester", "birmingham",
    "paris", "france",
    "berlin", "munich", "germany", "frankfurt",
    "amsterdam", "netherlands",
    "brussels", "belgium",
    "madrid", "spain",
    "rome", "milan", "italy",
    "zurich", "switzerland",
    "dublin", "ireland",
    "athens", "greece",
    "lisbon", "portugal",
    "warsaw", "poland",
    "stockholm", "sweden",
    "oslo", "norway",
    "copenhagen", "denmark",
    "helsinki", "finland",
    "vienna", "austria",
    "prague", "czech",
    "luxembourg",
    "reykjavik", "iceland",
    # Asia Pacific
    "singapore",
    "sydney", "melbourne", "brisbane", "australia",
    "auckland", "wellington", "new zealand",
    # Canada
    "toronto", "vancouver", "calgary", "montreal", "canada",
    # General
    "europe", "eu", "remote",
]

# -----------------------------------------------------------
# Fortune 2000 & Top Target Companies
# -----------------------------------------------------------
TARGET_COMPANIES = [
    # Oil & Gas
    "Shell", "BP", "ExxonMobil", "Chevron", "TotalEnergies",
    "ADNOC", "Saudi Aramco", "QatarEnergy", "KNPC", "ADCO",
    "Schlumberger", "SLB", "Halliburton", "Baker Hughes",
    "Wood Group", "Petrofac", "Technip", "McDermott", "Saipem",
    # Engineering & Construction
    "Bechtel", "Fluor", "Jacobs", "AECOM", "WSP", "Mott MacDonald",
    "Turner & Townsend", "Parsons", "KBR", "Foster Wheeler",
    "Worley", "SNC-Lavalin", "Arcadis", "Atkins",
    # Technology
    "Microsoft", "Google", "Amazon", "IBM", "SAP", "Oracle",
    "Accenture", "Capgemini", "Infosys", "TCS", "Wipro",
    # Aviation
    "Emirates", "Etihad", "Qatar Airways", "Lufthansa",
    "British Airways", "Air France", "KLM", "Singapore Airlines",
    "Airbus", "Boeing", "Rolls Royce", "GE Aviation",
    "Safran", "Honeywell", "Collins Aerospace",
    "dnata", "Swissport", "Menzies Aviation",
    # Consulting
    "McKinsey", "Deloitte", "PwC", "KPMG", "EY",
    "Boston Consulting Group", "Oliver Wyman",
    # Infrastructure
    "Siemens", "ABB", "Schneider Electric", "Alstom",
    "Thales", "Laing O Rourke",
]

# -----------------------------------------------------------
# Work Types
# -----------------------------------------------------------
WORK_TYPES = ["On-site", "Hybrid", "Remote", "Full-time", "Contract"]

# -----------------------------------------------------------
# Output Files
# -----------------------------------------------------------
DB_FILE     = "jobs_v2.db"
OUTPUT_FILE = "jobs_report_v2.xlsx"

# -----------------------------------------------------------
# Email Configuration
# -----------------------------------------------------------
EMAIL_CONFIG = {
    "enabled": True,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "sender email address",
    "sender_password": "sender password",
    "recipient_emails": ["reciever email address"],
    "subject_template": "\U0001f3af Job Opportunities Report - {date}",
}

# -----------------------------------------------------------
# Scheduler
# -----------------------------------------------------------
SCHEDULER_CONFIG = {
    "enabled": True,
    "schedule_time": "10:00",
    "timezone": "Asia/Dubai",
}

# -----------------------------------------------------------
# Behaviour Flags
# -----------------------------------------------------------
SEND_EMAIL_ON_RUN        = True
INCLUDE_EXCEL_ATTACHMENT = True
EMAIL_HTML_TEMPLATE      = "html"
