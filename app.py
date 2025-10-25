from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --------------------------
# Inicializar base de datos
# --------------------------
def init_db():
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            concepto TEXT NOT NULL,
            monto REAL NOT NULL,
            persona TEXT NOT NULL,
            fecha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --------------------------
# Página principal
# --------------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()

    # Si se envía el formulario, guardamos el movimiento
    if request.method == 'POST':
        concepto = request.form['concepto']
        monto = float(request.form['monto'])
        persona = request.form['persona']
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute('INSERT INTO movimientos (concepto, monto, persona, fecha) VALUES (?, ?, ?, ?)',
                  (concepto, monto, persona, fecha))
        conn.commit()
        return redirect('/')

    # Obtener todos los movimientos
    c.execute('SELECT * FROM movimientos ORDER BY id DESC')
    movimientos = c.fetchall()

    # Totales por persona
    personas = ['Enai', 'Itur', 'Isma']
    balances = {}
    total_general = 0
    for p in personas:
        c.execute('SELECT SUM(monto) FROM movimientos WHERE persona = ?', (p,))
        total = c.fetchone()[0]
        total = total if total else 0
        balances[p] = round(total, 2)
        total_general += total

    conn.close()

    return render_template(
        'index.html',
        movimientos=movimientos,
        balances=balances,
        total_general=round(total_general, 2)
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# Eliminar un movimiento
@app.route('/delete/<int:id>', methods=['POST'])
def delete_movimiento(id):
    conn = sqlite3.connect('finanzas.db')
    c = conn.cursor()
    c.execute('DELETE FROM movimientos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')
