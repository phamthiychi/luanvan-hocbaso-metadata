from typing import List
from neo4j import GraphDatabase

from src.common.ontology_setting import settings

class Neo4jStudentAssessmentStore:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_DB_URI,
            auth=(settings.NEO4J_DB_USER, settings.NEO4J_DB_PASSWORD))

    def check_neo4j_connection(self):
        try:
            self.driver.verify_connectivity()
            print("✅ Kết nối thành công tới Neo4j!")
        except Exception as e:
            print(f"❌ Kết nối thất bại: {e}")

    def close(self):
        self.driver.close()

    def save_reports(self, reports: List[dict]):
        with self.driver.session(database=settings.NEO4J_DB) as session:
            session.execute_write(self._process_all_reports, reports)

    def clean_database(self):
        with self.driver.session(database=settings.NEO4J_DB) as session:
            session.execute_write(self._delete_all)

    @staticmethod
    def _delete_all(tx):
        tx.run("MATCH (n) DETACH DELETE n")

    @classmethod
    def _process_all_reports(cls, tx, reports_list):
        for report in reports_list:
            student_code = report.get('student_code')
            assessments = report.get('assessments', [])
            cls._ensure_nodes_exist(tx, student_code, assessments)
            cls._create_student_assessments(tx, student_code, assessments)

    @classmethod
    def _ensure_nodes_exist(cls, tx, student_code, assessments):
        tx.run("MERGE (s:Student {name: $name})", name=student_code)
        for ass in assessments:
            tx.run("""
                MERGE (cat:Category {name: $cat_name})
                MERGE (com:Competency {name: $comp_name})
                MERGE (com)-[:BELONGS_TO]->(cat)
            """,
            cat_name=ass.get('category'),
            comp_name=ass.get('competency'))

    @classmethod
    def _create_student_assessments(cls, tx, student_code, assessments):
        cypher = """
            MATCH (stu:Student {name: $student_name})
            MATCH (com:Competency {name: $comp_name})
            MERGE (stu)-[r:HAS_ASSESSMENT {date: date()}]->(com)
            SET r.level = $level,
                r.evidence = $evidence
        """
        for ass in assessments:
            tx.run(cypher,
                student_name=student_code,
                comp_name=ass.get('competency'),
                level=ass.get('level'),
                evidence=ass.get('evidence'))