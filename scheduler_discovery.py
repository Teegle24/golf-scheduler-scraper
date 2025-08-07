from playwright.sync_api import sync_playwright
import json
from get_courses_from_golflink import get_courses_from_golflink

def detect_scheduler_from_site(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(2000)

            for a in page.query_selector_all("a"):
                href = a.get_attribute("href") or ""
                if any(s in href for s in ["foreup", "chronogolf", "teeitup", "golfrev"]):
                    return href
        except Exception as e:
            print(f"⚠️ Error: {e}")
        finally:
            browser.close()
    return None

def main():
    courses = get_courses_from_golflink("id")  # Change to your state slug
    print(f"🔍 Found {len(courses)} courses.")

    results = []

    for course in courses:
        scheduler_link = detect_scheduler_from_site(course["golflink_url"])
        course["scheduler_url"] = scheduler_link or "Not found"
        results.append(course)

    with open("courses_with_schedulers.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Done! Saved {len(results)} courses.")

if __name__ == "__main__":
    main()
