# import sqlite3
# import pandas as pd
# import os

# import os

# # Project root (JobRadar folder)
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # CSV folder
# CSV_FOLDER = os.path.join(PROJECT_ROOT, "local backend", "output")

# # CSV prefixes
# CSV_PREFIXES = ["filtered_jobs_", "manual_review_"]

# # SQLite DB path inside local backend/output
# DB_PATH = os.path.join(CSV_FOLDER, "JobRadar.sqlite")


# def get_latest_csv(csv_folder, prefix):
#     files = [f for f in os.listdir(csv_folder) if f.startswith(prefix) and f.endswith(".csv")]
#     if not files:
#         return None
#     files.sort()  # Ascending order
#     return os.path.join(csv_folder, files[-1])  # Latest file

# def import_csv_to_sqlite(csv_path, db_path):
#     table_name = os.path.splitext(os.path.basename(csv_path))[0]
#     df = pd.read_csv(csv_path)

#     conn = sqlite3.connect(db_path)
#     df.to_sql(table_name, conn, if_exists="replace", index=False)
#     conn.close()

#     print(f"CSV '{csv_path}' successfully imported into table '{table_name}' in database '{db_path}'.")

# # Process both filtered and manual CSVs
# for prefix in CSV_PREFIXES:
#     latest_csv = get_latest_csv(CSV_FOLDER, prefix)
#     if latest_csv:
#         import_csv_to_sqlite(latest_csv, DB_PATH)
#     else:
#         print(f"No CSV found with prefix '{prefix}'.")


import sqlite3
import pandas as pd
import os

# Project root (JobRadar folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# CSV folder
CSV_FOLDER = os.path.join(PROJECT_ROOT, "local backend", "output")

# CSV prefixes
CSV_PREFIXES = ["filtered_jobs_", "manual_review_"]

# SQLite DB path inside local backend/output
DB_PATH = os.path.join(CSV_FOLDER, "JobRadar.sqlite")

def get_latest_csv(csv_folder, prefix):
    files = [f for f in os.listdir(csv_folder) if f.startswith(prefix) and f.endswith(".csv")]
    if not files:
        return None
    # Sort by modification time
    files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(csv_folder, f)))
    return os.path.join(csv_folder, files[-1])

def import_csv_to_sqlite(csv_path, db_path):
    table_name = os.path.splitext(os.path.basename(csv_path))[0]
    df = pd.read_csv(csv_path)

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    print(f"CSV '{csv_path}' successfully imported into table '{table_name}' in database '{db_path}'.")

# Process both filtered and manual CSVs
for prefix in CSV_PREFIXES:
    latest_csv = get_latest_csv(CSV_FOLDER, prefix)
    if latest_csv:
        import_csv_to_sqlite(latest_csv, DB_PATH)
    else:
        print(f"No CSV found with prefix '{prefix}'.")
