from bs4 import BeautifulSoup
import requests


class JobsScraper:
    def __init__(self):
        self.BASE_URL = ""
        self.USER_HEADERS = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
        }
        self.infos_list = []

    def get_url(self, keyword):
        """keyword에 따라 URL 생성"""
        url = f"{self.BASE_URL}{keyword}/"
        return url
        

    def extract_text(self, tag):
        """단일 태그 또는 리스트에서 텍스트 추출"""

        if isinstance(tag, list):
            return [t.text.strip() for t in tag] if tag else ["No Information"]
        elif tag:
            return tag.text.strip()
        else:
            return "No Information"

    def get_pages(self, url):
        """해당 URL의 총 페이지 수 확인"""

        print(f"📄 Checking pages for: {url}")
        response = requests.get(url, headers=self.USER_HEADERS)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            page_list = soup.find_all("a", class_="page-numbers")
            return len(page_list)
        else:
            print(f"❌ Error fetching pages: {response.status_code}")
            return 0

    def get_infos(self, url):
        """각 URL에서 공고 정보 추출"""

        print(f"🔍 Scraping: {url}")
        response = requests.get(url, headers=self.USER_HEADERS)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            jobs_list = soup.find_all("li", class_="bjs-jlid")

            for job in jobs_list:
                title_tag = job.find("h4", class_="bjs-jlid__h")
                company_tag = job.find("a", class_="bjs-jlid__b")
                skills_tag = job.find_all("a", class_="bjs-bl bjs-bl-porcelain")
                description_tag = job.find("div", class_="bjs-jlid__description")

                link_tag = title_tag.find("a") if title_tag else None
                title_link = (
                    link_tag["href"]
                    if link_tag and "href" in link_tag.attrs
                    else "No Link"
                )

                infos = {
                    "company": self.extract_text(company_tag),
                    "title": self.extract_text(title_tag),
                    "skills": self.extract_text(skills_tag),
                    "description": self.extract_text(description_tag),
                    "link": title_link,
                }

                self.infos_list.append(infos)
        else:
            print(f"❌ Error fetching infos: {response.status_code}")

    def infos_print(self, info):
        """정보 출력 함수"""
        print("\n======= [📑 INFO] ======")
        for k, v in info.items():
            if isinstance(v, list):
                print(f"{k} {' / '.join(v)}")
            else:
                print(f"{k} {v}")

    def run(self):
        """전체 실행 함수"""

        # URL 목록 생성
        for keyword in self.all_keywords:
            self.get_url(keyword)

        # 첫 번째 카테고리 engineering의 페이지 수만큼 순회
        first_url = self.urls_list[0]
        total_pages = self.get_pages(first_url)

        for page in range(total_pages):
            paged_url = f"{first_url}page/{page + 1}"
            self.get_infos(paged_url)

        # skill-based URL들 추출
        for url in self.urls_list[2:]:
            self.get_infos(url)

        # 결과 출력
        for info in self.infos_list:
            self.infos_print(info)


if __name__ == "__main__":
    scraper = JobsScraper()
    scraper.run()
