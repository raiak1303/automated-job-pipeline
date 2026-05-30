# Job Finder v2 - Complete Multi-Source, Multi-Country Fetcher
# 18 Sources: Gulf, Europe, Asia-Pacific, Canada, Visa Sponsorship countries

import requests
from bs4 import BeautifulSoup
from typing import List
import re
import time
from job_model import Job
from config import HEADERS, TARGET_JOB_TITLES, ADZUNA_APP_ID, ADZUNA_APP_KEY, REED_API_KEY, JOOBLE_API_KEY


def safe_get(url, headers=None, params=None, timeout=15):
    try:
        r = requests.get(url, headers=headers or HEADERS, params=params, timeout=timeout)
        return r if r.status_code == 200 else None
    except Exception:
        return None


class JobFetcher:
    def __init__(self):
        self.source = "Unknown"
    def fetch(self) -> List[Job]:
        raise NotImplementedError


# 1. REMOTEOK — Remote worldwide (FREE)
class RemoteOKFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "RemoteOK"
    def fetch(self) -> List[Job]:
        try:
            r = safe_get("https://remoteok.com/api", headers={**HEADERS, "User-Agent": "Mozilla/5.0"})
            if not r: return []
            jobs = []
            for item in r.json()[1:]:
                if not isinstance(item, dict): continue
                jobs.append(Job(
                    title=item.get('position',''), company=item.get('company',''),
                    location=item.get('location','Remote'), work_type="Remote",
                    url=item.get('url',''), apply_url=item.get('apply_url', item.get('url','')),
                    description=item.get('description','')[:300],
                    source=self.source, posted_date=item.get('date','')
                ))
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 2. ARBEITNOW — European + Remote (FREE)
class ArbeitNowFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "ArbeitNow"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for page in range(1, 5):
                r = safe_get(f"https://www.arbeitnow.com/api/job-board-api?page={page}")
                if not r: break
                for item in r.json().get('data', []):
                    jobs.append(Job(
                        title=item.get('title',''), company=item.get('company_name',''),
                        location=item.get('location',''),
                        work_type="Remote" if item.get('remote') else "On-site",
                        url=item.get('url',''), apply_url=item.get('url',''),
                        description=item.get('description','')[:300],
                        source=self.source, posted_date=str(item.get('created_at',''))
                    ))
                time.sleep(0.5)
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 3. THE MUSE — Fortune 500 companies (FREE)
class TheMuseFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "TheMuse"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for page in range(1, 6):
                r = safe_get(f"https://www.themuse.com/api/public/jobs?page={page}&api_key=public")
                if not r: break
                for item in r.json().get('results', []):
                    locs = item.get('locations', [])
                    location = locs[0].get('name','') if locs else ''
                    jobs.append(Job(
                        title=item.get('name',''),
                        company=item.get('company',{}).get('name',''),
                        location=location, work_type="Full-time",
                        url=item.get('refs',{}).get('landing_page',''),
                        apply_url=item.get('refs',{}).get('landing_page',''),
                        company_website=item.get('company',{}).get('refs',{}).get('landing_page',''),
                        description=item.get('contents','')[:300],
                        source=self.source, posted_date=item.get('publication_date','')
                    ))
                time.sleep(0.5)
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 4. WORKINGNOMADS — Remote international (FREE)
class WorkingNomadsFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "WorkingNomads"
    def fetch(self) -> List[Job]:
        try:
            r = safe_get("https://www.workingnomads.com/api/exposed_jobs/?limit=100")
            if not r: return []
            jobs = []
            for item in r.json():
                jobs.append(Job(
                    title=item.get('title',''), company=item.get('company_name',''),
                    location=item.get('location','Remote'), work_type="Remote",
                    url=item.get('url',''), apply_url=item.get('url',''),
                    source=self.source, posted_date=item.get('pub_date','')
                ))
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 5. JOBICY — Remote worldwide (FREE)
class JobicyFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Jobicy"
    def fetch(self) -> List[Job]:
        try:
            r = safe_get("https://jobicy.com/api/v2/remote-jobs?count=50&industry=engineering")
            if not r: return []
            jobs = []
            for item in r.json().get('jobs', []):
                jobs.append(Job(
                    title=item.get('jobTitle',''), company=item.get('companyName',''),
                    location=item.get('jobGeo','Remote'), work_type="Remote",
                    url=item.get('url',''), apply_url=item.get('url',''),
                    company_website=item.get('companyUrl',''),
                    description=item.get('jobExcerpt','')[:300],
                    source=self.source, posted_date=item.get('pubDate','')
                ))
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 6. ADZUNA — UK, Germany, Australia, Canada, NL, France, Singapore, NZ
# FREE key from: developer.adzuna.com
class AdzunaFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Adzuna"
        self.app_id = ADZUNA_APP_ID
        self.app_key = ADZUNA_APP_KEY
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            countries = {"gb":"UK","de":"Germany","au":"Australia","ca":"Canada",
                         "nl":"Netherlands","fr":"France","sg":"Singapore","nz":"New Zealand"}
            for code, name in countries.items():
                for title in TARGET_JOB_TITLES[:5]:
                    r = safe_get(f"https://api.adzuna.com/v1/api/jobs/{code}/search/1",
                        params={"app_id":self.app_id,"app_key":self.app_key,
                                "results_per_page":20,"what":title})
                    if not r: continue
                    for item in r.json().get('results', []):
                        jobs.append(Job(
                            title=item.get('title',''),
                            company=item.get('company',{}).get('display_name',''),
                            location=item.get('location',{}).get('display_name', name),
                            work_type="Full-time",
                            url=item.get('redirect_url',''), apply_url=item.get('redirect_url',''),
                            description=item.get('description','')[:300],
                            source=f"{self.source} ({name})", posted_date=item.get('created','')
                        ))
                    time.sleep(0.3)
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 7. REED.CO.UK — UK jobs with recruiter emails (FREE key)
# FREE key from: reed.co.uk/developers
class ReedFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Reed.co.uk"
        self.api_key = REED_API_KEY
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for title in TARGET_JOB_TITLES[:8]:
                r = safe_get("https://www.reed.co.uk/api/1.0/search",
                    headers={**HEADERS,"Authorization":f"Basic {self.api_key}"},
                    params={"keywords":title,"resultsToTake":25})
                if not r: continue
                for item in r.json().get('results', []):
                    jobs.append(Job(
                        title=item.get('jobTitle',''), company=item.get('employerName',''),
                        location=item.get('locationName','UK'), work_type="Full-time",
                        url=item.get('jobUrl',''), apply_url=item.get('jobUrl',''),
                        recruiter_email=item.get('contactEmail',''),
                        description=item.get('jobDescription','')[:300],
                        source=self.source, posted_date=item.get('date','')
                    ))
                time.sleep(0.5)
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 8. JOOBLE — 60+ countries (FREE key)
# FREE key from: jooble.org/api/about
class JoobleFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Jooble"
        self.api_key = JOOBLE_API_KEY
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            locations = ["Dubai","Abu Dhabi","Riyadh","Doha","London","Amsterdam",
                         "Berlin","Paris","Singapore","Sydney","Toronto","Oslo",
                         "Zurich","Dublin","Luxembourg","Copenhagen","Athens","Brussels"]
            for location in locations:
                for title in TARGET_JOB_TITLES[:3]:
                    r = safe_get(f"https://jooble.org/api/{self.api_key}",
                        params={"keywords":title,"location":location,"page":1})
                    if not r: continue
                    for item in r.json().get('jobs', [])[:8]:
                        jobs.append(Job(
                            title=item.get('title',''), company=item.get('company',''),
                            location=item.get('location', location), work_type="Full-time",
                            url=item.get('link',''), apply_url=item.get('link',''),
                            description=item.get('snippet','')[:300],
                            source=self.source, posted_date=item.get('updated','')
                        ))
                    time.sleep(0.3)
            return [j for j in jobs if j.title]
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 9. LINKEDIN — Public search
class LinkedInFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "LinkedIn"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            searches = [
                ("Planning Engineer","Dubai"),("Project Engineer","UAE"),
                ("PMO Analyst","Saudi Arabia"),("Cost Control Engineer","Qatar"),
                ("Project Scheduler","London"),("Planning Engineer","Singapore"),
                ("Project Manager","Australia"),("Project Controller","Netherlands"),
                ("Cost Engineer","Germany"),("PMO Analyst","Canada"),
                ("Planning Engineer","Norway"),("Project Scheduler","Switzerland"),
                ("Digital Planning Engineer","France"),("BI Analyst","Ireland"),
                ("Reporting Analyst","Luxembourg"),("Planning Engineer","Denmark"),
                ("Project Engineer","Greece"),("Cost Control","Belgium"),
            ]
            for keyword, location in searches:
                r = safe_get("https://www.linkedin.com/jobs/search",
                    headers={**HEADERS,"Accept-Language":"en-US,en;q=0.9"},
                    params={"keywords":keyword,"location":location,"position":1,"pageNum":0})
                if not r:
                    time.sleep(2); continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('div', {'class': lambda x: x and 'base-card' in str(x)})[:8]:
                    try:
                        t = card.find('h3', {'class': lambda x: x and 'base-search-card__title' in str(x)})
                        c = card.find('h4', {'class': lambda x: x and 'base-search-card__subtitle' in str(x)})
                        l = card.find('span', {'class': lambda x: x and 'job-search-card__location' in str(x)})
                        a = card.find('a', {'class': lambda x: x and 'base-card__full-link' in str(x)})
                        rn = card.find('span', {'class': lambda x: x and 'job-poster' in str(x)})
                        rl = card.find('a', {'class': lambda x: x and 'job-poster' in str(x)})
                        title_text = t.get_text(strip=True) if t else ''
                        if title_text:
                            jobs.append(Job(
                                title=title_text,
                                company=c.get_text(strip=True) if c else '',
                                location=l.get_text(strip=True) if l else location,
                                work_type="Full-time",
                                url=a['href'] if a else '', apply_url=a['href'] if a else '',
                                recruiter_name=rn.get_text(strip=True) if rn else '',
                                recruiter_url=rl['href'] if rl else '',
                                source=self.source
                            ))
                    except Exception: continue
                time.sleep(2)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 10. BAYT.COM — Gulf
class BaytFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Bayt"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            terms = ["planning-engineer","project-engineer","pmo-analyst",
                     "cost-control-engineer","project-scheduler","project-manager"]
            for term in terms:
                r = safe_get(f"https://www.bayt.com/en/international/jobs/{term}-jobs/")
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('li', {'class': lambda x: x and 'has-pointer-d' in str(x)})[:15]:
                    try:
                        t = card.find('h2') or card.find('a', {'class': lambda x: x and 'jb-title' in str(x)})
                        c = card.find('b', {'class':'jb-company'})
                        l = card.find('span', {'class':'jb-loc'})
                        a = card.find('a', href=True)
                        title_text = t.get_text(strip=True) if t else ''
                        link = 'https://www.bayt.com'+a['href'] if a and a['href'].startswith('/') else ''
                        if title_text:
                            jobs.append(Job(title=title_text, company=c.get_text(strip=True) if c else '',
                                location=l.get_text(strip=True) if l else 'Gulf', work_type="On-site",
                                url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 11. NAUKRIGULF — Gulf
class NaukriGulfFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "NaukriGulf"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            terms = ["planning+engineer","project+engineer","pmo+analyst","cost+control","project+scheduler"]
            for term in terms:
                r = safe_get(f"https://www.naukrigulf.com/{term}-jobs")
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('div', {'class': lambda x: x and 'job-capsule' in str(x)})[:15]:
                    try:
                        t = card.find('a', {'class': lambda x: x and 'designation' in str(x)})
                        c = card.find('span', {'class': lambda x: x and 'comp-name' in str(x)})
                        l = card.find('span', {'class': lambda x: x and 'loc' in str(x)})
                        a = card.find('a', href=True)
                        title_text = t.get_text(strip=True) if t else ''
                        link = 'https://www.naukrigulf.com'+a['href'] if a and a['href'].startswith('/') else ''
                        if title_text:
                            jobs.append(Job(title=title_text, company=c.get_text(strip=True) if c else '',
                                location=l.get_text(strip=True) if l else 'Gulf', work_type="On-site",
                                url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 12. GULFTALENT — Gulf
class GulfTalentFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "GulfTalent"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            terms = ["planning-engineer","project-engineer","project-manager","cost-engineer","pmo"]
            for term in terms:
                r = safe_get(f"https://www.gulftalent.com/jobs/title/{term}")
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('div', {'class': lambda x: x and 'job' in str(x).lower()})[:15]:
                    try:
                        t = card.find('h2') or card.find('h3')
                        a = card.find('a', href=True)
                        title_text = t.get_text(strip=True) if t else ''
                        link = 'https://www.gulftalent.com'+a['href'] if a and a['href'].startswith('/') else ''
                        if title_text:
                            jobs.append(Job(title=title_text, company='', location='Gulf',
                                work_type="On-site", url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 13. SEEK — Australia & New Zealand
class SeekFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Seek (AU/NZ)"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for title in TARGET_JOB_TITLES[:5]:
                r = safe_get(f"https://www.seek.com.au/{title.lower().replace(' ','-')}-jobs")
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('article', {'data-card-type':'JobCard'})[:15]:
                    try:
                        t = card.find('a', {'data-automation':'jobTitle'})
                        c = card.find('a', {'data-automation':'jobCompany'})
                        l = card.find('a', {'data-automation':'jobLocation'})
                        title_text = t.get_text(strip=True) if t else ''
                        link = 'https://www.seek.com.au'+t['href'] if t and t.get('href') else ''
                        if title_text:
                            jobs.append(Job(title=title_text, company=c.get_text(strip=True) if c else '',
                                location=(l.get_text(strip=True) if l else '')+', Australia',
                                work_type='Full-time', url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 14. JOBSDB — Singapore
class JobsDBFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "JobsDB (Singapore)"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for title in TARGET_JOB_TITLES[:5]:
                r = safe_get(f"https://sg.jobsdb.com/{title.lower().replace(' ','-')}-jobs")
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('div', {'data-automation':'normalJob'})[:15]:
                    try:
                        t = card.find('a', {'data-automation':'jobTitle'})
                        c = card.find('span', {'data-automation':'jobCompany'})
                        l = card.find('span', {'data-automation':'jobLocation'})
                        title_text = t.get_text(strip=True) if t else ''
                        link = 'https://sg.jobsdb.com'+t['href'] if t and t.get('href') else ''
                        if title_text:
                            jobs.append(Job(title=title_text, company=c.get_text(strip=True) if c else '',
                                location=(l.get_text(strip=True) if l else '')+', Singapore',
                                work_type='Full-time', url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 15. JOBS.CH — Switzerland
class JobsChFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Jobs.ch (Switzerland)"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for title in TARGET_JOB_TITLES[:5]:
                r = safe_get("https://www.jobs.ch/en/vacancies/", params={"term":title,"location":"Switzerland"})
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('article')[:15]:
                    try:
                        t = card.find('h2') or card.find('h3')
                        a = card.find('a', href=True)
                        title_text = t.get_text(strip=True) if t else ''
                        link = a['href'] if a else ''
                        if not link.startswith('http'): link = 'https://www.jobs.ch'+link
                        if title_text:
                            jobs.append(Job(title=title_text, company='', location='Switzerland',
                                work_type='Full-time', url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 16. FINN.NO — Norway
class FinnNoFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "Finn.no (Norway)"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for title in TARGET_JOB_TITLES[:4]:
                r = safe_get("https://www.finn.no/job/fulltime/search.html", params={"q":title})
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('article')[:15]:
                    try:
                        t = card.find('h2') or card.find('a')
                        a = card.find('a', href=True)
                        title_text = t.get_text(strip=True) if t else ''
                        link = a['href'] if a else ''
                        if not link.startswith('http'): link = 'https://www.finn.no'+link
                        if title_text:
                            jobs.append(Job(title=title_text, company='', location='Norway',
                                work_type='Full-time', url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 17. EUROJOBS — Europe wide
class EuroJobsFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "EuroJobs"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for title in TARGET_JOB_TITLES[:5]:
                r = safe_get("https://www.eurojobs.com/search-results", params={"q":title,"l":"Europe"})
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all('div', {'class': lambda x: x and 'job' in str(x).lower()})[:10]:
                    try:
                        t = card.find('h2') or card.find('h3') or card.find('a')
                        a = card.find('a', href=True)
                        title_text = t.get_text(strip=True) if t else ''
                        link = a['href'] if a else ''
                        if not link.startswith('http'): link = 'https://www.eurojobs.com'+link
                        if title_text:
                            jobs.append(Job(title=title_text, company='', location='Europe',
                                work_type='Full-time', url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# 18. AVIATIONJOBNET — Aviation specific
class AviationJobNetFetcher(JobFetcher):
    def __init__(self):
        super().__init__()
        self.source = "AviationJobNet"
    def fetch(self) -> List[Job]:
        try:
            jobs = []
            for term in ["planning+engineer","project+engineer","project+manager"]:
                r = safe_get(f"https://www.aviationjobnet.com/jobsearch.php?keywords={term}")
                if not r: continue
                soup = BeautifulSoup(r.text, 'html.parser')
                for card in soup.find_all(['div','li'], {'class': lambda x: x and 'job' in str(x).lower()})[:15]:
                    try:
                        t = card.find('h2') or card.find('h3') or card.find('a')
                        a = card.find('a', href=True)
                        title_text = t.get_text(strip=True) if t else ''
                        link = a['href'] if a else ''
                        if not link.startswith('http'): link = 'https://www.aviationjobnet.com'+link
                        if title_text:
                            jobs.append(Job(title=title_text, company='Aviation Company',
                                location='International', work_type='On-site',
                                url=link, apply_url=link, source=self.source))
                    except Exception: continue
                time.sleep(1)
            return jobs
        except Exception as e:
            print(f"    {self.source}: {e}"); return []


# ============================================================
# MAIN ORCHESTRATOR
# ============================================================
class AllJobsFetcher:
    def __init__(self):
        self.fetchers = [
            # Free APIs — no key needed
            RemoteOKFetcher(),
            ArbeitNowFetcher(),
            TheMuseFetcher(),
            WorkingNomadsFetcher(),
            JobicyFetcher(),
            # Gulf
            BaytFetcher(),
            NaukriGulfFetcher(),
            GulfTalentFetcher(),
            # Multi-country (add free API keys for more results)
            LinkedInFetcher(),
            AdzunaFetcher(),        # FREE key: developer.adzuna.com
            ReedFetcher(),          # FREE key: reed.co.uk/developers
            JoobleFetcher(),        # FREE key: jooble.org/api/about
            # Country specific
            SeekFetcher(),          # Australia / New Zealand
            JobsDBFetcher(),        # Singapore
            JobsChFetcher(),        # Switzerland
            FinnNoFetcher(),        # Norway
            EuroJobsFetcher(),      # Europe wide
            AviationJobNetFetcher(), # Aviation
        ]

    def fetch_all(self) -> List[Job]:
        all_jobs = []
        for fetcher in self.fetchers:
            print(f"  Fetching from {fetcher.source}...")
            try:
                jobs = fetcher.fetch()
                all_jobs.extend(jobs)
                print(f"  ✓ {len(jobs)} jobs from {fetcher.source}")
            except Exception as e:
                print(f"  ✗ {fetcher.source}: {e}")
        return all_jobs
