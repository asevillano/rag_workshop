from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Ruta para manejar las consultas SQL
@app.route('/sqlite-query', methods=['POST'])
def sqlite_query():
    try:
        # Obtén la consulta SQL del cuerpo de la solicitud
        data = request.get_json()
        sql_query = data.get('query')
        user = data.get('user')
        password = data.get('password')

        # Verifica las credenciales (esto es solo un ejemplo, en un entorno real deberías usar un método seguro)
        if user != 'admin' or password != 'Password123!':
            return jsonify({'error': 'Invalid credentials'}), 401

        # Conéctate a la base de datos SQLite
        conn = sqlite3.connect('adventureworks.db')
        cursor = conn.cursor()

        # Ejecuta la consulta
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Procesa los resultados
        results = []
        for row in rows:
            results.append(row)

        # Cierra la conexión
        cursor.close()
        conn.close()

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
