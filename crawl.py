import praw
import time
import json
import sys
import sqlite3
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager

# Database setup
def setup_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                permalink TEXT,
                subreddit TEXT
            )
        ''')
        
        # Create comments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT,
                body TEXT,
                score INTEGER,
                FOREIGN KEY (post_id) REFERENCES posts(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database setup complete.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Insert data into database
def insert_data(db_path, post_data):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Insert post data
        cursor.execute('''
            INSERT OR IGNORE INTO posts (id, title, url, permalink, subreddit)
            VALUES (?, ?, ?, ?, ?)
        ''', (post_data['id'], post_data['title'], post_data['url'], post_data['permalink'], post_data['subreddit']))
        
        # Insert comments data
        for comment in post_data['comments']:
            cursor.execute('''
                INSERT INTO comments (post_id, body, score)
                VALUES (?, ?, ?)
            ''', (post_data['id'], comment['body'], comment['score']))
        
        conn.commit()
        conn.close()
        print(f"Successfully inserted post: {post_data['id']}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Fetch the page title for metadata
def get_page_title(url):
    try:
        URL = 'https://reddit.com' + url
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.title.string
    except Exception as e:
        print(f'Error fetching page title: {e}')
        return None


# Setup Reddit API clients
reddit1 = praw.Reddit(
    client_id="cNT1EH-yNK3kKSvOhCem-w",
    client_secret="7HCcEduHHAI6bzL2a3A9YmvROyAaFA",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
)

reddit2 = praw.Reddit(
    client_id="UcJ-738JlR9xKkc5ezoQSQ",
    client_secret="Rk6d6_OPbrTXxQ4ZVPwJbzPTFtQWmg",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
)

reddit3 = praw.Reddit(
    client_id="p509OSKbru5SrwSt_8Ybng",
    client_secret="wXChxj5DifMefhaSSX_EttCZWUMSTw",
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64"
)
reddits = [reddit1, reddit2, reddit3]
subreddit_names = ['school', 'cooking', 'Sephora', 'Tiktok', 'Instagram', 'news', 'books', 'Starbucks', 'baking']
target_size_of_data = 100 * 1024 * 1024  # 100MB target size

# Load crawled IDs
try:
    with open('crawled_ids.json', 'r') as f:
        crawled_ids = set(json.load(f))
except (FileNotFoundError, json.JSONDecodeError):
    crawled_ids = set()
    with open('crawled_ids.json', 'w') as f:
        json.dump(list(crawled_ids), f)

post_types = ['top', 'new', 'controversial', 'trending', 'hot']

def crawl_subreddit(args):
    reddit, subreddit_name, crawled_ids, manager_dict, db_path = args
    subreddit = reddit.subreddit(subreddit_name)
    crawled_ids_set = set(crawled_ids)

    for post_type in post_types:
        for submission in getattr(subreddit, post_type)(limit=None):
            try:
                if manager_dict['current_data_size'] >= target_size_of_data:
                    break
                if submission.id in crawled_ids_set:
                    continue
                crawled_ids_set.add(submission.id)

                post_data = {
                    'subreddit': subreddit_name,
                    'title': submission.title,
                    'id': submission.id,
                    'url': submission.url,
                    'permalink': submission.permalink,
                    'comments': [],
                    'permalink_text': get_page_title(submission.permalink)
                }

                try:
                    submission.comments.replace_more(limit=None)
                    for comment in submission.comments.list():
                        post_data['comments'].append({
                            'body': comment.body,
                            'score': comment.score
                        })
                except Exception as e:
                    print(f"Error fetching comments: {e}")
                    time.sleep(60)  # Rate limit handling

                # Insert post and comments into the database
                insert_data(db_path, post_data)

                manager_dict['current_data_size'] += sys.getsizeof(post_data)

            except Exception as e:
                print(f"Error processing submission: {e}")

    with open('crawled_ids.json', 'w') as f:
        json.dump(list(crawled_ids_set), f)

if __name__ == "__main__":
    db_path = 'mydatabaseSearchEngine.db'
    setup_database(db_path)

    with Manager() as manager:
        crawled_ids = manager.list(crawled_ids)
        manager_dict = manager.dict()
        manager_dict['current_data_size'] = 0

        with Pool() as p:
            p.map(crawl_subreddit, [(reddit, subreddit_name, crawled_ids, manager_dict, db_path) for reddit in reddits for subreddit_name in subreddit_names])

    print(f'Total data size: {manager_dict["current_data_size"] / (1024 * 1024)}MB')