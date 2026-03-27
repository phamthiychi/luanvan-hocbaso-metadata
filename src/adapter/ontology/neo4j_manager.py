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
            cls._ensure_nodes_exist(tx, report)
            cls._create_student_assessments(tx, report)

    @classmethod
    def _ensure_nodes_exist(cls, tx, report, thing_name="Thing"):
        assessments = report.get('assessments', [])
        for ass in assessments:
            tx.run("""
                MERGE (t:Thing {thing_name: $thing_name})
                MERGE (cat:Category {category_name: $cat_name})
                MERGE (com:Competency {competency_name: $comp_name})
                MERGE (stu:Student {student_id: $student_id})
                MERGE (stu_name:StudentName {student_name: $student_name})
                MERGE (stu_card:StudentCardId {student_edu_id: $student_edu_id})
                MERGE (stu_edu:StudentEduId {student_card_id: $student_card_id})

                MERGE (t)-[:HAS_CATEGORY]->(cat)
                MERGE (cat)-[:HAS_COMPETENCY]->(com)
                MERGE (com)-[:HAS_STUDENT]->(stu)
                MERGE (stu)-[:HAS_NAME]->(stu_name)
                MERGE (stu)-[:HAS_CARD_ID]->(stu_card)
                MERGE (stu)-[:HAS_EDU_ID]->(stu_edu)
            """,
            thing_name=thing_name,
            cat_name=ass.get("category"),
            comp_name=ass.get("competency"),
            student_id=report.get("code"),
            student_name=report.get("name"),
            student_edu_id=report.get("edu_id"),
            student_card_id=report.get("card_id"))

    @classmethod
    def _create_student_assessments(cls, tx, report, thing_name="Thing"):
        assessments = report.get('assessments', [])
        for ass in assessments:
            tx.run("""
                MATCH (t:Thing {thing_name: $thing_name})
                MATCH (cat:Category {category_name: $cat_name})
                MATCH (com:Competency {competency_name: $comp_name})
                MATCH (stu:Student {student_id: $student_id})
                MATCH (stu_name:StudentName {student_name: $student_name})
                MATCH (stu_card:StudentCardId {student_edu_id: $student_edu_id})
                MATCH (stu_edu:StudentEduId {student_card_id: $student_id})

                MERGE (t)-[:HAS_CATEGORY]->(cat)
                MERGE (cat)-[:HAS_COMPETENCY]->(com)
                MERGE (com)-[:HAS_STUDENT]->(stu)
                MERGE (stu)-[:HAS_NAME]->(stu_name)
                MERGE (stu)-[:HAS_CARD_ID]->(stu_card)
                MERGE (stu)-[:HAS_EDU_ID]->(stu_edu)
            """,
            thing_name=thing_name,
            cat_name=ass.get("category"),
            comp_name=ass.get("competency"),
            student_id=report.get("code"),
            student_name=report.get("name"),
            student_edu_id=report.get("edu_id"),
            student_card_id=report.get("card_id"))
