import requests
from bs4 import BeautifulSoup

def get_courses_from_golflink(state_slug):
    url = f"https://www.golflink.com/golf-courses/state/{state_slug}"
    print(f"🛰️ Fetching course list from {url}")
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if "403" in res.text or res.status_code == 403:
        print("❌ Access denied. Golflink may be blocking non-browser requests.")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    courses = []

    for item in soup.select("div.card-body"):
        a_tag = item.find("a", href=True)
        name_tag = item.find("h2")

        if a_tag and name_tag:
            href = a_tag["href"]
            name = name_tag.get_text(strip=True)

            if href.startswith("/golf-courses/"):
                course_url = f"https://www.golflink.com{href}"
                courses.append({"name": name, "golflink_url": course_url})

    return courses
