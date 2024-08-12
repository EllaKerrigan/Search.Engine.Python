#!/usr/bin/env python3

import re
import sqlite3

#tokenize the text
def tokenize(text):
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

#normalize the tokens
def normalize(tokens):
    normalized_tokens = [token.lower() for token in tokens]
    return normalized_tokens

#build an inverted index from the documents
def build_inverted_index(documents):
    inverted_index = {}
    for doc_id, text in documents.items():
        tokens = normalize(tokenize(text))
        for token in tokens:
            if token in inverted_index:
                inverted_index[token].add(doc_id)
            else:
                inverted_index[token] = {doc_id}
    return inverted_index

#Storing the inverted index in the database
def store_inverted_index(inverted_index, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inverted_index (
            token TEXT,
            doc_id TEXT
        )
    ''')
    for token, doc_ids in inverted_index.items():
        for doc_id in doc_ids:
            cursor.execute('INSERT INTO inverted_index (token, doc_id) VALUES (?, ?)', 
                           (token, doc_id))
    conn.commit()
    conn.close()

def main():
    db_path = 'mydatabaseSearchEngine.db'  
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # retrieve the data from both posts and comments
    cursor.execute('SELECT id, title FROM posts')
    posts = {row[0]: row[1] for row in cursor.fetchall()}
    print("Posts:", posts)  #using to debug
    cursor.execute('SELECT post_id, body FROM comments')
    comments = {}
    for row in cursor.fetchall():
        if row[0] in comments:
            comments[row[0]] += ' ' + row[1]
        else:
            comments[row[0]] = row[1]
    print("Comments:", comments)  #using to debug

    documents = {**posts, **comments}
    print("Documents:", documents)  #using to debug

    conn.close()

    inverted_index = build_inverted_index(documents)
    print("Inverted Index:", inverted_index)  # Debugging print

    store_inverted_index(inverted_index, db_path)
    print("Indexing completed successfully.")
