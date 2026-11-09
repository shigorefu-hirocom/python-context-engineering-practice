import json
import os
import sqlite3


DATABASE_FILE = "data/students.db"
OUTPUT_DIR = "output"


def load_students():
    # mode=ro は、データベースを読み取り専用で開く指定です。
    connection = sqlite3.connect(f"file:{DATABASE_FILE}?mode=ro", uri=True)
    try:
        # SELECT は、表から指定した列のデータを取り出します。
        cursor = connection.execute(
            "SELECT student_id, name, class_name FROM students ORDER BY student_id"
        )
        return cursor.fetchall()
    finally:
        connection.close()


def write_student_files(students):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    created = 0
    skipped = 0

    for student_id, name, class_name in students:
        student = {
            "student_id": student_id,
            "name": name,
            "class_name": class_name,
        }
        filename = os.path.join(OUTPUT_DIR, f"{student_id}.json")

        try:
            # x モードでは新規作成だけを行い、同名のファイルは上書きしません。
            with open(filename, "x", encoding="utf-8") as file:
                json.dump(student, file, ensure_ascii=False, indent=2)
                file.write("\n")
        except FileExistsError:
            print(f"作成をスキップしました: {filename}")
            skipped += 1
        else:
            created += 1

    print(f"新規作成: {created}件、スキップ: {skipped}件")


def main():
    if not os.path.isfile(DATABASE_FILE):
        print(f"データベースが見つかりません: {DATABASE_FILE}")
        return

    students = load_students()
    write_student_files(students)


if __name__ == "__main__":
    main()
