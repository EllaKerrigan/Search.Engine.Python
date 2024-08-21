# Search.Engine.Python

<img width="428" alt="Screenshot 2024-08-12 at 14 33 43" src="https://github.com/user-attachments/assets/f5ef680e-675b-4dea-adad-c09559d2b7bc">

This Python project implements a search engine that utilizes the PageRank algorithm to rank Reddit posts. The project was inspired by relevant Reddit topics shared by myself and my peers, adding an element of personal engagement to the development process. The primary objective is to demonstrate techniques in web crawling, data processing, and search ranking.

Key Features:

- Reddit Post Crawling: Extracts posts and comments from designated subreddits.
- PageRank Algorithm: Ranks posts based on their relevance and significance.
- Search Functionality: Provides a search interface for users to find posts and view results sorted by rank.

Technical Requirements:

- PRAW: For accessing Reddit's API to crawl posts and comments.
- BeautifulSoup: For parsing HTML content.
- Multiprocessing Library: To enable concurrent crawling of multiple subreddits.
- PyLucene: For indexing and searching data.
- Django: For hosting the web interface.
- Database: For storing crawled data and search results.
