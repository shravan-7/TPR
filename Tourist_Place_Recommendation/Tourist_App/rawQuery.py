from django.db import connection

def execute_query(raw_query, params=None):
    with connection.cursor() as cursor:
        try:
            if params:
                cursor.execute(raw_query, params)
            else:
                cursor.execute(raw_query)
            
            results = cursor.fetchall()
            
            if cursor.description is None:
                print(f"No results found for query: {raw_query}")
                return []
            
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in results]
            
            print(f"Query executed successfully. Found {len(data)} results.")
            return data
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print(f"Query: {raw_query}")
            print(f"Parameters: {params}")
            return []

def get_data(category_list):
    raw_query = "SELECT * FROM dataset WHERE Category IN %s"
    return execute_query(raw_query, (tuple(category_list),))

def get_top_data():
    raw_query = "SELECT * FROM dataset WHERE Ratings BETWEEN 4.8 AND 5 AND sentiment = 1"
    return execute_query(raw_query)

def get_search_data(query):
    raw_query = "SELECT * FROM dataset WHERE NAME LIKE %s"
    return execute_query(raw_query, [f"%{query}%"])

def get_data_test(place_name):
    raw_query = "SELECT ID,Name,Description,Ratings,Map_link FROM dataset WHERE Name LIKE %s"
    return execute_query(raw_query, [f"%{place_name}%"])

def get_fav_data(user):
    raw_query = """
        SELECT d.* 
        FROM dataset d
        INNER JOIN favorite f ON d.ID = f.place_id
        WHERE f.user_id = %s
    """
    return execute_query(raw_query, [user.id])

def get_review_counts(place_id):
    raw_query = """
        SELECT r.rating, COUNT(t.id) as count
        FROM (
            SELECT 1 as rating UNION ALL
            SELECT 2 UNION ALL
            SELECT 3 UNION ALL
            SELECT 4 UNION ALL
            SELECT 5
        ) as r
        LEFT JOIN Tourist_App_review t
        ON r.rating = t.rating AND t.place_id = %s
        GROUP BY r.rating
        ORDER BY r.rating
    """
    return execute_query(raw_query, [place_id])

def has_user_reviewed(user_id, place_id):
    query = """
    SELECT EXISTS (
        SELECT 1
        FROM Tourist_App_review
        WHERE user_id = %s AND place_id = %s
    ) AS has_reviewed
    """
    result = execute_query(query, [user_id, place_id])
    return result[0]['has_reviewed'] if result else False

def get_user_review(place_id):
    query = """
    SELECT u.name,u.user_name, r.rating, r.review_text,u.gender
    FROM Tourist_App_user AS u
    INNER JOIN Tourist_App_review AS r ON u.id = r.user_id
    WHERE r.place_id = %s
    """
    return execute_query(query, [place_id])

def get_photo_data(review_id, user_id, place_id):
    sql_query = """
        SELECT p.photo_data
        FROM Tourist_App_reviewphoto p
        INNER JOIN Tourist_App_review r ON p.review_id = r.id
        WHERE r.user_id = %s AND r.place_id = %s AND r.id = %s
    """
    result = execute_query(sql_query, [user_id, place_id, review_id])
    return result[0]['photo_data'] if result else None