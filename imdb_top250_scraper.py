from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://www.imdb.com/chart/top/")

# Wait until movie list is visible (max 15 seconds)
WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"))
)

# Extract movie elements
movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

titles, years, ratings = [], [], []

for movie in movies:
    try:
        title = movie.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text
    except:
        title = "N/A"

    try:
        year = movie.find_element(By.CSS_SELECTOR, "span.sc-b189961a-8").text
    except:
        year = "N/A"

    try:
        rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
    except:
        rating = "N/A"

    titles.append(title)
    years.append(year)
    ratings.append(rating)

driver.quit()

# Create DataFrame
df = pd.DataFrame({
    "Rank": range(1, len(titles) + 1),
    "Title": titles,
    "Year": years,
    "Rating": ratings
})

# Save to CSV
df.to_csv("imdb_top250.csv", index=False, encoding="utf-8-sig")

print("✅ Scraping completed! Data saved to imdb_top250.csv")
print(df.head(10))