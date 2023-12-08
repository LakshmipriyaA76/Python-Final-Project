from flask import Flask, render_template
import sqlite3
import csv
import os


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('About.html')


@app.route('/datapage')
def datapage():
    # Establish a connection to the SQLite database
    # db_name = 'website.db'
    # conn = sqlite3.connect(db_name)
    # cursor = conn.cursor()
    # Specify the folder where you want to create the database
    folder_path = './Database'  # Replace with the actual path
    db_name = os.path.join(folder_path, 'website.db')  # Specify the full path to the database file

    # Establish a connection to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Specify the SQL table name
    table_name = 'Students_Placement_Info'

    # Create the table if it doesn't exist
    create_table_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        Sl_No INTEGER PRIMARY KEY AUTOINCREMENT,
        Gender TEXT,
        SecondaryClass_Percentage REAL,
        SecondaryClass_Board TEXT,
        HighSecondaryClass_Percentage REAL,
        HighSecondaryClass_Board TEXT,
        HighSecondaryClass_Branch TEXT,
        Degree_Percentage REAL,
        Degree_Branch TEXT,
        WorkExperience INTEGER,
        Etest_Percentage REAL,
        Specialisation TEXT,
        MBA_Percentage REAL,
        Placement_Status TEXT,
        Salary REAL
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()


    # Read data from CSV file and insert or update into the SQLite table
    csv_file_path = './Data Collection/Placement_Data.csv'
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        # Insert or update data in the table based on Sl_No
        for row in csv_reader:
            sl_no = row[0]  # Assuming 'Sl_No' is at index 0

            # Check if a similar record already exists based on Sl_No
            select_existing_query = f'SELECT Sl_No FROM {table_name} WHERE Sl_No = ?;'
            cursor.execute(select_existing_query, (sl_no,))
            existing_record = cursor.fetchone()

            if existing_record:
                # If record exists, you can choose to update it or skip the insertion
                update_query = f'''
                UPDATE {table_name} SET
                    Gender = ?, SecondaryClass_Percentage = ?, SecondaryClass_Board = ?,
                    HighSecondaryClass_Percentage = ?, HighSecondaryClass_Board = ?,
                    HighSecondaryClass_Branch = ?, Degree_Percentage = ?, Degree_Branch = ?,
                    WorkExperience = ?, Etest_Percentage = ?, Specialisation = ?,
                    MBA_Percentage = ?, Placement_Status = ?, Salary = ?
                WHERE Sl_No = ?;
                '''
                cursor.execute(update_query, list(row[1:]) + [sl_no])

            else:
                # If record does not exist, insert the data
                insert_query = f'''
                INSERT INTO {table_name} (
                    Sl_No, Gender, SecondaryClass_Percentage, SecondaryClass_Board,
                    HighSecondaryClass_Percentage, HighSecondaryClass_Board,
                    HighSecondaryClass_Branch, Degree_Percentage, Degree_Branch,
                    WorkExperience, Etest_Percentage, Specialisation,
                    MBA_Percentage, Placement_Status, Salary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                '''
                cursor.execute(insert_query, [sl_no] + row[1:])

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    # Fetch all the rows after inserting or updating data
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    select_query = f"SELECT * FROM {table_name} WHERE Placement_Status = 'Placed';"
    #select_query = f"SELECT * FROM {table_name} ;"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    conn.close()

    # print(rows)

    # Render the HTML template with the fetched data
    return render_template('DataPage.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
