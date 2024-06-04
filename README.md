# UDN News Scrapper & GPT Categorizer 

## Overview
This project is designed to scrape news articles from the United Daily News (UDN) website, filter them based on specified keywords, process the articles using GPT for Named Entity Recognition (NER), and save the categorized articles into a CSV file for further analysis. The project combines web scraping, data extraction, and AI-powered text processing to automate the process of gathering, categorizing, and saving news data.

## Features
- Web Scraping: Uses `requests` and `BeautifulSoup` to scrape news articles from UDN.
- Keyword Filtering: Filters articles based on specified keywords related to corruption and fraud.
- Data Extraction: Extracts article titles, content, publication dates, and URLs.
- Date Filtering: Filters articles based on their publication dates to only include recent news.
- CSV Export: Saves the filtered articles into a CSV file for easy visualization and analysis.
- Scheduling: Automates the scraping process to run at a specified time every day using `APScheduler`.
- GPT Processing: Uses OpenAI's GPT models to perform NER and categorize the scraped articles.
- Parallel Processing: Utilizes pandarallel for efficient parallel processing of DataFrame operations.

## Requirements 
- Python 3.6+
- Requests
- BeautifulSoup4
- Pandas
- APScheduler
- tqdm
- openai
- tiktoken
- jieba
- numpy
- pandarallel

## Installation
`pip install requests beautifulsoup4 pandas apscheduler tqdm openai tiktoken jieba numpy pandarallel`
