import sqlite3
import re

# Tokenize the search query
def tokenize_query(query):
    return re.findall(r'\b\w+\b', query.lower())

# Normalize the tokens
def normalize_tokens(tokens):
    return [token.lower() for token in tokens]

# Retrieve and rank documents based on query
def search_documents(query, db_path):
    tokens = normalize_tokens(tokenize_query(query))
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Dictionary to store collected scores of each document
    doc_scores = {}

    for token in tokens:
        cursor.execute('''
            SELECT ii.doc_id, p.ranking_score
            FROM inverted_index ii
            JOIN posts p ON ii.doc_id = p.id
            WHERE ii.token = ?
        ''', (token,))
        
        results = cursor.fetchall()
        
        for doc_id, ranking_score in results:
            if doc_id in doc_scores:
                doc_scores[doc_id] += ranking_score
            else:
                doc_scores[doc_id] = ranking_score
    
    # Sort the documents by their scores in descending order
    sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Fetch and display the top results
    for doc_id, score in sorted_docs[:10]:  # Limit to top 10 results
        cursor.execute('SELECT title, url FROM posts WHERE id = ?', (doc_id,))
        title, url = cursor.fetchone()
        print(f'Title: {title}, URL: {url}, Score: {score}')
    
    conn.close()

if __name__ == "__main__":
    db_path = 'mydatabaseSearchEngine.db'
    
    # Example search query
    query = input("Enter your search query: ")
    search_documents(query, db_path)
