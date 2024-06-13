import mysql.connector
import os

class DatabaseModel:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database="konf"
        )

    def fetch(self, query, values=None):
        cursor = self.conn.cursor()
        cursor.execute(query, values or ())
        records = cursor.fetchall()
        cursor.close()
        return records

    def execute(self, query, values=None):
        cursor = self.conn.cursor()
        cursor.execute(query, values or ())
        self.conn.commit()
        cursor.close()

    def get_conferences(self):
        return self.fetch("""
            SELECT к.id_конференции, к.название, о.название, к.статус, к.дата_начала, к.организатор
            FROM конференции к
            JOIN организаторы о
                ON к.id_организатора = о.id_организатора
        """)

    def find_conference(self, conf_id):
        return self.fetch("""
            SELECT к.id_конференции, к.название, о.название, к.статус, к.дата_начала, к.организатор
            FROM конференции к
            JOIN организаторы о
                ON к.id_организатора = о.id_организатора
            WHERE к.id_конференции = %s
        """, (conf_id, ))

    def get_organizers(self):
        return self.fetch("""
            SELECT id_организатора, название
            FROM организаторы
        """)

    def add_conference(self, organizer_id, conf_name, conf_status, conf_date, conf_organizer):
        self.execute("""
            INSERT INTO конференции (id_организатора, название, статус, дата_начала, организатор)
            VALUES (%s, %s, %s, %s, %s)
        """, (organizer_id, conf_name, conf_status, conf_date, conf_organizer))
        return self.get_last_insert_id()

    def get_last_insert_id(self):
        return self.fetch("""
            SELECT LAST_INSERT_ID()
        """)[0][0]