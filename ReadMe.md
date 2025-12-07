# <h1 style="font-size: 36px; margin: 0;">Scrapeman - Data Collector 🕷️</h1>

A powerful web scraping application built with Scrapy that extracts listings from online marketplaces. This project automatically collects product information including titles, prices, publication dates, and locations, then exports the data to a formatted Excel spreadsheet with automatic currency conversion and hyperlink support.


⚠️ **Please read Important Requirements & Limitations section carefully before attempting to use this scraper on any website.**

- [Important Requirements & Limitations](#important-requirements--limitations)
- [Features](#features-)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Features 

- **Automated Web Scraping**: Efficiently crawls multiple pages of product listings using Scrapy's powerful framework with built-in request throttling and concurrency control.
- **Currency Conversion**: Automatically converts prices from EUR to RSD (Serbian Dinar) with configurable exchange rates. Supports both EUR and RSD price formats.
- **Excel Export**: Generates professionally formatted Excel files with styled headers, colored cells, and clickable hyperlinks to product listings.
- **Pagination Support**: Automatically navigates through multiple pages of search results up to a configurable maximum page limit.
- **Data Extraction**: Extracts product titles, prices, publication dates, and seller locations from marketplace listings.
- **Respectful Crawling**: Configured to respect robots.txt rules and includes download delays to avoid overloading target servers.
- **Error Handling**: Gracefully handles missing data and stops pagination when no items are found on a page.
- **Customizable**: Easy to modify target URLs, search parameters, output paths, and scraping limits through simple configuration changes.

---

## Tech Stack

- **Python 3.x** - Core programming language
- **Scrapy** - Web scraping framework for efficient crawling and data extraction
- **openpyxl** - Excel file generation and formatting library
- **Regular Expressions (re)** - Pattern matching for price extraction and currency conversion
- **OS Module** - File system operations for directory creation and path management

---

## Project Structure

```
WebScraper/
├── webscraper/
│   ├── scrapy.cfg              # Scrapy project configuration
│   └── webscraper/
│       ├── __init__.py         # Package initialization
│       ├── items.py             # Data structure definitions (FragranceItem)
│       ├── middlewares.py      # Request/response middleware components
│       ├── pipelines.py         # Data processing pipelines
│       ├── settings.py          # Scrapy framework settings
│       └── spiders/
│           ├── __init__.py
│           └── MainSpiderScraper.py  # Main spider implementation
└── ReadMe.md                    # Project documentation
```

### Key Components

- **MainSpiderScraper.py**: The main spider class that handles URL crawling, data extraction, and Excel file generation. Contains logic for pagination, price conversion, and data formatting.
- **items.py**: Defines the `FragranceItem` data structure with fields for header, price_rsd, date, location, and link.
- **settings.py**: Configures Scrapy behavior including download delays, concurrency limits, robots.txt compliance, and encoding settings.
- **pipelines.py**: Data processing pipeline (currently passes items through without modification, ready for custom processing if needed).

---

## Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.7 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (usually comes with Python)
- **Git** - For cloning the repository (optional)

### Step-by-Step Installation

1. **Clone the repository** (or download the project files):
   ```bash
   git clone <repository-url>
   cd WebScraper
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If you don't have a `requirements.txt` file, install packages manually:
   ```bash
   pip install scrapy openpyxl
   ```

4. **Verify installation**:
   ```bash
   scrapy version
   python -c "import openpyxl; print('openpyxl installed successfully')"
   ```

---

## Important Requirements & Limitations

### Website Requirements

This scraper is **explicitly designed** for websites with specific characteristics. It will **NOT work** with all types of websites:

#### 1. **Server-Side Rendering (SSR) Required**

- ✅ **Works with**: Traditional websites that render HTML on the server
- ❌ **Does NOT work with**: Single Page Applications (SPAs) that require JavaScript execution
- ❌ **Does NOT work with**: React, Vue, Angular, or other JavaScript frameworks that load content dynamically
- **Why**: The scraper uses Scrapy's built-in HTML parser (`response.css()`, `response.xpath()`) which only processes static HTML. It does not execute JavaScript or wait for dynamic content to load.

**How to check**: If you can view the page source (right-click → View Page Source) and see the content you want to scrape, the site likely uses SSR. If the content is missing from the source but visible in the browser, it's likely a JavaScript-rendered site.

#### 2. **URL-Based Page Numeration Required**

- ✅ **Works with**: URLs that include page numbers as query parameters or path segments
  - Example: `https://example.com/search?page=1`, `https://example.com/search?page=2`
  - Example: `https://example.com/search/page/1`, `https://example.com/search/page/2`
- ❌ **Does NOT work with**: Infinite scroll or "Load More" button pagination
- ❌ **Does NOT work with**: JavaScript-based pagination that doesn't change the URL

**Current implementation**: The scraper expects URLs in the format:
```
base_url = "https://example.com/search?keywords=term&page="
```
It then appends page numbers: `page=1`, `page=2`, `page=3`, etc.

#### 3. **Stable CSS Selectors Required**

- The scraper relies on **specific CSS selectors** to extract data
- These selectors are **hardcoded** in the spider code and are specific to the target website's HTML structure
- If the website changes its HTML structure, CSS classes, or element hierarchy, the scraper will **stop working**

**Current selectors used** (as examples):
- `.AdItem_adOuterHolder__hb5N_` - Container for each listing
- `div.AdItem_name__iOZvA` - Product title
- `div.AdItem_price__VZ_at div` - Price element
- `div.AdItem_originAndPromoLocation__rQvKl p` - Location element

**Before using on a different website**: You **MUST** update all CSS selectors in `MainSpiderScraper.py` to match the target website's HTML structure.

#### 4. **Consistent HTML Structure**

- The website must have a **consistent HTML structure** across all pages
- Each listing/item must follow the same pattern and use the same CSS classes or element hierarchy
- The scraper expects to find multiple items on each page using the same selector

### Legal & Ethical Considerations

⚠️ **Important**: Web scraping may be subject to legal restrictions and website terms of service.

- **Check robots.txt**: The scraper is configured to respect `robots.txt` files. Ensure the target website allows scraping.
- **Review Terms of Service**: Many websites prohibit automated data collection. Always review and comply with the website's Terms of Service.
- **Rate Limiting**: The scraper includes delays (1 second between requests) to avoid overloading servers. Do not reduce these delays without careful consideration.
- **Personal Responsibility**: You are responsible for ensuring your use of this scraper complies with applicable laws and website policies.

### Technical Limitations

1. **No JavaScript Execution**: Cannot scrape content loaded via JavaScript/AJAX
2. **No Browser Automation**: Does not use Selenium, Playwright, or similar tools
3. **Fixed Selectors**: CSS selectors must be manually updated for each target website
4. **Single Domain**: Configured to work with one domain at a time (see `allowed_domains`)
5. **No Authentication**: Does not handle login-protected content or session management
6. **No CAPTCHA Handling**: Cannot bypass CAPTCHA or other anti-bot measures

### Before Using on a New Website

1. ✅ Verify the website uses SSR (check page source)
2. ✅ Confirm URL-based pagination exists
3. ✅ Inspect the HTML structure and identify CSS selectors
4. ✅ Update `base_url` with the correct pagination pattern
5. ✅ Update all CSS selectors in the spider code
6. ✅ Update `allowed_domains` to match the target website
7. ✅ Test with a small number of pages first (`max_pages = 2`)
8. ✅ Verify the website's robots.txt and Terms of Service

### Modifying for Different Websites

To adapt this scraper for a different website, you will need to:

1. **Update CSS Selectors**: Modify all `response.css()` and `response.xpath()` calls in `MainSpiderScraper.py`
2. **Update URL Pattern**: Change `base_url` to match the target website's pagination format
3. **Update Data Extraction Logic**: Adjust the parsing logic to match the new HTML structure
4. **Update Item Fields**: Modify `items.py` if you need different data fields
5. **Test Thoroughly**: Always test with a small sample before running on many pages

---

## Usage

### Basic Usage

1. **Navigate to the project directory**:
   ```bash
   cd webscraper
   ```

2. **Run the spider**:
   ```bash
   scrapy crawl FragranceSpider
   ```

3. **Check the output**: The Excel file will be saved to the path specified in `MainSpiderScraper.py` (default: `C:\Users\lekid\OneDrive\Desktop\YSL.xlsx`)

### Customizing the Scraper

Before running, you may want to customize the following settings in `MainSpiderScraper.py`:

- **Target URL**: Modify `base_url` to scrape different search queries or categories
- **Output Path**: Change `excel_path` to save the file to your desired location
- **Page Limit**: Adjust `max_pages` to control how many pages to scrape
- **Exchange Rate**: Update `EUR_TO_RSD` if the conversion rate changes

### Example Configuration

```python
# Change the search query
base_url = "https://www.kupujemprodajem.com/nega-i-licna-higijena/parfemi-muski/pretraga?categoryId=20&groupId=1314&keywords=your_search_term&page="

# Change output location
excel_path = r"C:\Users\YourUsername\Desktop\Output.xlsx"

# Limit pages to scrape
max_pages = 10

# Update exchange rate
EUR_TO_RSD = 120.0
```

---

## Configuration

### Scrapy Settings

The project uses default Scrapy settings with the following customizations in `settings.py`:

- **ROBOTSTXT_OBEY**: Set to `True` to respect robots.txt rules
- **CONCURRENT_REQUESTS_PER_DOMAIN**: Limited to 1 to be respectful to the server
- **DOWNLOAD_DELAY**: 1 second delay between requests
- **FEED_EXPORT_ENCODING**: UTF-8 encoding for proper character support

### Spider-Specific Settings

The `MainSpiderScraper` class includes custom settings:
- `DOWNLOAD_DELAY`: 1 second
- `CONCURRENT_REQUESTS`: 1 request at a time

These settings ensure respectful crawling behavior and can be adjusted in the spider's `custom_settings` dictionary.

### Output Format

The generated Excel file includes:
- **Headers**: Styled with blue background (#4472C4) and white bold text
- **Data Columns**: Title, Price (RSD), Publication Date, Location
- **Hyperlinks**: Product titles are clickable links to the original listings
- **Automatic Formatting**: Prices converted to RSD, dates preserved as scraped

---

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are installed and the virtual environment is activated
   ```bash
   pip install scrapy openpyxl
   ```

2. **Permission Denied**: Check that the output directory exists and you have write permissions
   - The script will attempt to create the directory if it doesn't exist

3. **No Items Found**: The spider will stop automatically if no items are found on a page
   - Check that the target URL is still valid
   - Verify the website structure hasn't changed

4. **Encoding Issues**: The project uses UTF-8 encoding by default. If you encounter character display issues, ensure your Excel viewer supports UTF-8.

### Getting Help

- Check Scrapy documentation: https://docs.scrapy.org/
- Review the spider code comments for inline documentation
- Verify your Python and package versions are compatible

---

## License

This project is open-source and available under the MIT License.

---

## Notes

- This scraper is **specifically designed** for SSR websites with URL-based pagination
- Always respect website terms of service and robots.txt when scraping
- Website structures may change over time, requiring code updates to CSS selectors
- This scraper is currently configured for a specific marketplace structure and requires modifications for other sites
- For JavaScript-heavy websites, consider using browser automation tools (Selenium, Playwright) instead of this Scrapy-based solution

