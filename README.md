# DevJobScraper – Tech Job Aggregator with Flask & TailwindCSS

A responsive job search web app that scrapes listings from **BerlinStartupJobs**, **WeWorkRemotely**, and **Stepstone.de**.  
Built with **Flask**, **Tailwind CSS**, **Selenium**, and deployable via **Docker**.


## 🌐 Features

- 🔍 Keyword-based job search (e.g., `Python`, `JavaScript`)
- 📊 View job listing counts per site (BSJ, WWR, SSD)
- 📄 Site-specific detailed results page
- 📥 Export listings to CSV
- 📱 Responsive design with site toggle
- ⚡ Fast performance via simple in-memory caching


## 🛠️ Tech Stack

| Layer        | Tech                              |
|--------------|-----------------------------------|
| Backend      | Python, Flask                     |
| Frontend     | HTML, Tailwind CSS, JS            |
| Scraping     | BeautifulSoup, Selenium, Requests |
| Export       | CSV (`csv` standard module)       |
| Deployment   | Docker, Railway-ready             |


## 🐳 Run with Docker

> Dockerfile includes Chrome + ChromeDriver (for Selenium-based scraping)

```bash
# Build image
docker build -t jobscraper .

# Run container
docker run -p 5000:5000 jobscraper

```


## 📂 Routes Overview

| Route                                      | Description                       |
|--------------------------------------------|-----------------------------------|
| `/`                                        | Home page with search bar         |
| `/search?keyword=python`                   | Aggregated job counts per site    |
| `/result?site=bsj&keyword=python`          | Site-specific detailed listings   |
| `/export?site=bsj&keyword=python`          | Export site results as CSV        |


## ✨ Notable Features

- **Scraper Abstraction**: Each scraper inherits from a common `JobScraper` base class
- **JavaScript Toggle**: `main.js` dynamically cycles between job sites
- **Caching**: Keyword-based results stored in-memory for faster repeated searches
- **Responsive UI**: Mobile-ready layout with clean TailwindCSS styling
- **Selenium Support**: WWR scraper uses headless Chrome to render JS-based content


## 📦 Deployment Notes

- `requirements.txt` includes all Python and Selenium dependencies
- `Dockerfile` installs all system dependencies + ChromeDriver
- Production run command:

```dockerfile
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5000}"]
```


## 👨‍💻 Author

Built with ❤️ by **Myeonggyun Park**  
This project is part of a backend web development learning journey.
