# https://neo4j.com/docs/python-manual/current/
import os
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

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

# Neo4j connection parameters
uri = NEO4J_URI  
username = NEO4J_USERNAME        
password = NEO4J_PASSWORD

# Connect to Neo4j
connection = Neo4jConnection(uri, username, password)

# Delete all nodes and relationships
connection.delete_all_nodes_and_relationships()

# Close the connection
connection.close()
