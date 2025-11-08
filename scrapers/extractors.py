# Importing scraper classes from job_scrapers and aliasing them
from job_scrapers import BSJscraper as BSJ
from job_scrapers import WWRscraper as WWR
from job_scrapers import SSDscraper as SSD


# Function to extract jobs from BerlinStartupJobs
def extract_bsj_jobs(keyword):
    scraper = BSJ("https://berlinstartupjobs.com/skill-areas/")
    return scraper.run(keyword)


# Function to extract jobs from WeWorkRemotely
def extract_wwr_jobs(keyword):
    scaper = WWR("https://weworkremotely.com/remote-jobs/search?term=")
    return scaper.run(keyword)


# Function to extract jobs from Stepstone.de
def extract_ssd_jobs(keyword):
    scaper = SSD("https://www.stepstone.de/jobs/?page=1&searchOrigin=Homepage_top-search")
    return scaper.run(keyword)
