# https://neo4j.com/docs/python-manual/current/
import os
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

# Neo4j connection parameters
uri = NEO4J_URI  
username = NEO4J_USERNAME        
password = NEO4J_PASSWORD

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def delete_all_nodes_and_relationships(self):
        with self.__driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("All nodes and relationships deleted.")
    
    def load_csv_data(self, url):
        with self.__driver.session() as session:
            session.run(url)
            print("CSV data loaded successfully.")

# Connect to Neo4j
connection = Neo4jConnection(uri, username, password)

# Load Author nodes from CSV
author_load = """
LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-1de224d0-cae0-497a-820c-bcc46684fd5f/authors.csv' AS row
MERGE (a:Author {name: row.x})
"""
connection.load_csv_data(author_load)

# Load Paper nodes from CSV
paper_load = """
LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-1de224d0-cae0-497a-820c-bcc46684fd5f/paperID_paper.csv' AS row
MERGE (p:Paper {name: row.paper_title, paperID: row.id_paper})
"""
connection.load_csv_data(paper_load)

# Create relationships between Authors and Papers
relationship_load = """
LOAD CSV WITH HEADERS FROM 'http://localhost:11001/project-1de224d0-cae0-497a-820c-bcc46684fd5f/authors_papersID.csv' AS row
MATCH (p:Paper {paperID: row.id_paper})
MATCH (a:Author {name: row.author})
MERGE (a)-[r:WRITES]->(p)
"""
connection.load_csv_data(relationship_load)

# Close the connection
connection.close()
