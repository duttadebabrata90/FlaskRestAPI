from neo4j import GraphDatabase


def get_connection():
    url = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(url, auth=("neo4j", "admin"))
    session = driver.session()
    return session


def post_movies():
    session = get_connection()
    try:
        post_movie_sql = 'LOAD CSV WITH HEADERS from ' \
                         '"file:///movie.csv" as data ' \
                         'MERGE (n:Movie{name:data.movie_name,tagline:data.tagline,released:data.released})' \
                         'RETURN COUNT(n) as movie_count'
        count = session.run(post_movie_sql)
    except:
        pass
    finally:
        session.close()
    if count.single():
        return count.single()[0]
    else:
        count


def post_person():
    session = get_connection()
    try:
        post_person_sql = 'LOAD CSV WITH HEADERS from ' \
                          '"file:///person.csv" as data ' \
                          'MERGE (n:Person{name:data.name,born:data.born})' \
                          'RETURN COUNT(n) as person_count'
        count = session.run(post_person_sql)
    except:
        pass
    finally:
        session.close()
    if count.single():
        return count.single()[0]
    else:
        return count


def get_all_movies():
    session = get_connection()
    try:
        post_person_sql = 'MATCH (m:Movie) '\
                          'RETURN m.name,m.tagline,m.released '
        results = session.run(post_person_sql)
        movies = dict()
        for data in results:
            movies[data[0]] = {'name': data[0], 'tagline': data[1], 'released': data[2]}
    except:
        pass
    finally:
        session.close()
    return movies


def clean_neo4j_db():
    session = get_connection()
    try:
        clean_db_sql = 'MATCH (n) DETACH DELETE n '
        session.run(clean_db_sql)
    except:
        pass
    finally:
        session.close()






