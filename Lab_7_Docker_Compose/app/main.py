import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("DB_NAME", "scholarship_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres_secret")
DB_PORT = os.getenv("DB_PORT", "5432")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scholarship_applications (
            id SERIAL PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            student_card VARCHAR(30) NOT NULL,
            scholarship_type VARCHAR(50) NOT NULL,
            status VARCHAR(30) NOT NULL DEFAULT 'SUBMITTED',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@app.route("/applications", methods=["POST"])
def create_application():
    data = request.get_json() or {}
    student_name = data.get("student_name")
    student_card = data.get("student_card")
    scholarship_type = data.get("scholarship_type", "ACADEMIC")

    if not student_name or not student_card:
        return jsonify({"error": "student_name and student_card are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        """
        INSERT INTO scholarship_applications (student_name, student_card, scholarship_type, status)
        VALUES (%s, %s, %s, 'SUBMITTED') RETURNING *;
        """,
        (student_name, student_card, scholarship_type)
    )
    new_app = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_app), 201


@app.route("/applications", methods=["GET"])
def list_applications():
    status = request.args.get("status")
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if status:
        cur.execute("SELECT * FROM scholarship_applications WHERE status = %s ORDER BY id;", (status,))
    else:
        cur.execute("SELECT * FROM scholarship_applications ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows), 200


@app.route("/applications/<int:app_id>/status", methods=["PATCH"])
def update_status(app_id):
    data = request.get_json() or {}
    new_status = data.get("status")
    valid_statuses = ["SUBMITTED", "IN_REVIEW", "APPROVED", "REJECTED"]

    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of {valid_statuses}"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "UPDATE scholarship_applications SET status = %s WHERE id = %s RETURNING *;",
        (new_status, app_id)
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        return jsonify({"error": "Application not found"}), 404

    return jsonify(updated), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
