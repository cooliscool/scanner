from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# output to file
file_path = 'output.txt'
file = open(file_path, 'a')

# output to db
DB = 'my_database.db'
CONN = sqlite3.connect(DB)
CURSOR = CONN.cursor()
CURSOR.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY,
        parameter TEXT
    )
''')
CONN.close()



@app.route('/bin', methods=['POST'])
def receive_post():
    try:
        post_data = request.get_json()
        id_value = post_data['id']

        # Write the 'id' parameter to the file
        if id_value:
            file.write(str(id_value) + '\n' )
            # print(file)
            # print(id_value)
            file.flush()

        response_message = {'message': 'ID parameter written to file.'}
        return jsonify(response_message), 200
    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400


@app.route('/sqli', methods=['POST'])
def receive_sqli():
    try: 
        post_data = request.get_json()
        id_value = post_data['id']

        # Write the 'id' parameter to the db
        if id_value:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()
            # cursor.execute('INSERT INTO my_table (parameter) VALUES ('+id_value+')')
            cursor.execute("INSERT INTO my_table (parameter) VALUES ('{}');".format(id_value))
            conn.commit()
            conn.close()
            # print(id_value)

        response_message = {'message': 'ID parameter written to db.'}
        return jsonify(response_message), 200

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4444)
