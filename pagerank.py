import sqlite3

def calculate_ranking_scores(db_path):
    conn = sqlite3.connect(db_path)#connecting the database
    cursor = conn.cursor()

    #Make sure that the posts table has a column for ranking score
    cursor.execute('''
        ALTER TABLE posts
        ADD COLUMN ranking_score REAL DEFAULT 0
    ''')
    
    # Fetch post details(including the number of comments and total comment scores)
    cursor.execute('''
        SELECT p.id, p.title,
               COALESCE(COUNT(c.id), 0) AS num_comments,
               COALESCE(SUM(c.score), 0) AS total_comment_score
        FROM posts p
        LEFT JOIN comments c ON p.id = c.post_id
        GROUP BY p.id
    ''')
    posts = cursor.fetchall()

    for post in posts: #go through each post in the fetched results
        post_id = post[0]
        title_length = len(post[1].split())  #Num of words in the title
        num_comments = post[2]  #Num of comments
        total_comment_score = post[3]  # Total score of comments

        # Calculate the ranking score(weighting formula)
        ranking_score = (0.4 * num_comments) + (0.5 * total_comment_score) + (0.1 * title_length)

        # Update the posts table with ranking score
        cursor.execute('''
            UPDATE posts
            SET ranking_score = ?
            WHERE id = ?
        ''', (ranking_score, post_id))

    conn.commit()
    conn.close()

    print("Ranking scores calculated and updated successfully.")

if __name__ == "__main__":
    db_path = 'mydatabaseSearchEngine.db'
    

    calculate_ranking_scores(db_path)
