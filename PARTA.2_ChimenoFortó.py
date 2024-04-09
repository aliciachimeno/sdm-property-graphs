# https://neo4j.com/docs/python-manual/current/
from neo4j_classes import Neo4jConnection
from neo4jconfig import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, BASE_URL

# Neo4j connection parameters
uri = NEO4J_URI  
username = NEO4J_USERNAME        
password = NEO4J_PASSWORD
base_url = BASE_URL

def main():
    # Connect to Neo4j
    connection = Neo4jConnection(uri, username, password)
     
    # Queries to execute, formatted for readability
    queries = [

        f"""
        MATCH (n)
        DETACH DELETE n
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_author.csv' AS row
        MERGE (a:Author {{name: row.author}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_paper.csv' AS row
        MERGE (a:Papers {{name: row.paper_title, id: row.id_paper, doi: row.doi, abstract: row.abstract, pages: toInteger(row.year)}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_volumes.csv' AS row
        MERGE (a:Volume {{name: row.volume, year: toInteger(row.year)}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_edition.csv' AS row
        MERGE (a:Edition {{name: row.edition, ref_edition: row.ref_edition, num: row.edition_num, location: row.location, year: toInteger(row.year)}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_conference.csv' AS row
        MERGE (a:Conference {{name: row.conference}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_journals.csv' AS row
        MERGE (a:Journal {{name: row.x}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_papers_author.csv' AS row
        MATCH (a:Author {{name: row.author}})
        MATCH (b:Papers {{id: row.id_paper}})
        MERGE (a)-[r:writes {{main_author: row.main_author}}]->(b);
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_edition_conference.csv' AS row
        MATCH (a:Edition {{ref_edition: row.ref_edition}})
        MATCH (b:Conference {{name: row.conference}})
        MERGE (a)-[r:belongs_to]->(b);
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_paper_volumes.csv' AS row
        MATCH (a:Papers {{id: row.id_paper}})
        MATCH (b:Volume {{name: row.id_volume}})
        MERGE (a)-[r:contained_in]->(b);
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_paper_paper.csv' AS row
        MATCH (a:Papers {{id: row.id_paper}})
        MATCH (b:Papers {{id: row.cites_value}})
        MERGE (a)-[r:cites]->(b);
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_papers_edition.csv' AS row
        MATCH (a:Papers {{id: row.id_paper}})
        MATCH (b:Edition {{ref_edition: row.ref_edition}})
        MERGE (a)-[r:published_in]->(b);
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Node_keywords.csv' AS row
        MERGE (a:Keywords {{name: row.Node_keywords}})
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_papers_keywords.csv' AS row
        MATCH (a:Papers {{id: row.id_paper}})
        MATCH (b:Keywords {{name: row.keywords}})
        MERGE (a)-[r:relates_to]->(b);
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_volumes_journal.csv' AS row
        MATCH (a:Volume {{name: row.id_volume}})
        MATCH (b:Journal {{name: row.journal}})
        MERGE (a)-[r:belongs_to]->(b);
        """,

        f"""
        LOAD CSV WITH HEADERS FROM '{base_url}/Edge_paper_author_reviews.csv' AS row
        MATCH (a:Author {{name: row.author}})
        MATCH (b:Papers {{id: row.id_paper}})
        MERGE (a)-[r:reviews]->(b);
        """
    ]

    # Execute each query, respecting the readable formatting
    for i, query in enumerate(queries, start=1):
        print(f"Executing Query {i}...")
        connection.load_csv_data(query)

    connection.close()

if __name__ == '__main__':
    main()
