# 🕷️ Open URLs Crawler

## Overview
**Open URLs Crawler** is a Python-based web scraper designed to extract all unique hyperlinks from a given website.  
It intelligently filters out duplicate links that share the same root domain and excludes unwanted domains such as major social networks or common platforms (e.g., Google, YouTube, Microsoft, etc.).

This tool combines the power of **Selenium** for JavaScript-rendered pages and **BeautifulSoup** for parsing static HTML content.  
The final output is neatly saved into an Excel file for easy review and data management.
---

## 🚀 Features

- Extracts all unique hyperlinks (`<a href="...">`) from any website.
- Automatically ignores repeated links sharing the same domain root.
- Skips irrelevant or common domains (Google, YouTube, Microsoft, etc.).
- Supports both **JavaScript-heavy** and **static HTML** sites.
- Exports results automatically to an **Excel (.xlsx)** file.
- User can input the target URL directly from the console.
---

## 🧰 Technologies Used

| Technology | Description |
|-------------|-------------|
| **Python 3.14** | Main programming language used to build the crawler. |
| **Selenium** | Automates web browsers to load dynamic or JavaScript-rendered content. |
| **BeautifulSoup4** | Parses and extracts links from static HTML pages. |
| **Requests** | Handles standard HTTP requests for faster static page access. |
| **OpenPyXL** | Creates and writes the extracted results into Excel files. |
| **Chrome WebDriver** | Provides browser automation through Selenium for Chrome. |
| **Git** | Version control and project management. |
| **Visual Studio Code** | Development environment used to write and test the code. |
---

## 🧩 How It Works

1. The script prompts the user to input a website URL.
2. Selenium loads the website in headless mode (without opening the browser window).
3. BeautifulSoup parses the HTML content.
4. The script extracts all `<a>` tags with valid `href` attributes.
5. Duplicates are removed by comparing domain roots (e.g., `https://example.com/` is kept only once).
6. Links containing blocked domains (e.g., Google, YouTube, Facebook, etc.) are skipped.
7. The clean list of unique URLs is exported to `output_links.xlsx`.
---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:andres0191/open-urls.git
   cd open-urls
Install dependencies:

bash
pip install selenium beautifulsoup4 requests openpyxl
Make sure you have Chrome and ChromeDriver installed.
Selenium will automatically connect to the ChromeDriver executable.

▶️ Usage
Run the script from the terminal:

bash
Copiar código
python crawler_selenium.py
Then enter the URL you want to analyze (for example):

mathematica

Enter the URL to crawl: https://www.mercadolibre.com.co/
The results will be saved in:

output_links.xlsx
🧹 Example of Excluded Domains
The crawler ignores these (and similar) domains automatically:


google.com
youtube.com
facebook.com
instagram.com
twitter.com
linkedin.com
microsoft.com
bing.com
mozilla.org
yahoo.com
reddit.com
tiktok.com
apple.com

🧠 Future Improvements
Add asynchronous support using aiohttp for faster crawling.
Include multi-page scraping with pagination detection.
Add a graphical interface (GUI) for non-technical users.
Support for exporting results in CSV or JSON formats.

📄 License
This project is open-source and available under the MIT License.

👨‍💻 Author: [Andrés Felipe Garcia Rendon](https://linkedin.com/in/anfegar)

📂 GitHub: [GitHub @andres0191](https://github.com/andres0191)

✉️ Email: [email ](mailto:felipe.garcia0191@gmail.com)



