import json
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'portfolio-flask-secret-key'

DATA_FILE = Path(__file__).with_name('data.json')


def load_data():
    try:
        with DATA_FILE.open('r', encoding='utf-8') as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return [
            {"nama": "Devon", "nilai": 90},
            {"nama": "Farrel", "nilai": 84},
        ]


def save_data(data):
    with DATA_FILE.open('w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


project_list = [
    {
        "title": "Academic Student Tracker",
        "description": "Aplikasi pencatat nilai siswa, kelulusan, dan rata-rata nilai.",
        "url": "/student-tracker",
    },
    {
        "title": "Finance Tracker",
        "description": "Aplikasi pencatat saldo, pendapatan, dan pengeluaran.",
        "url": "/finance",
    },
    {
        "title": "To do App",
        "description": "Aplikasi untuk mencatat dan mengelola aktivitas sehari-hari.",
        "url": "/todo",
    },
]

students = load_data()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Pesan berhasil dikirim!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    hasil = [p for p in project_list if query.casefold() in p['title'].casefold()]
    return render_template('search.html', hasil=hasil, query=query)

@app.route('/api/projects')
def api_projects():
    return jsonify(project_list)

@app.route('/student-tracker', methods=['GET','POST'])
def student_tracker():
    error = None
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        nilai = request.form.get('nilai', '').strip()
        if not nama:
            error = "Nama harus diisi!"
        elif not nilai:
            error = "Nilai harus diisi!"
        else:
            try:
                nilai = int(nilai)
                if nilai < 0 or nilai > 100:
                    error = "Nilai harus antara 0-100"
            except ValueError:
                error = "Nilai harus berupa angka!"
            if not error:
                students.append({"nama": nama, "nilai": nilai})
                save_data(students)
    avg = (
        sum(s['nilai'] for s in students)/len(students)
        if students else 0
    )
    return render_template(
        'student_tracker.html',
        students=students,
        avg=avg,
        error=error
    )

transactions = [
    {"type":"masuk", "desc":"Gaji", "amount": 5000000},
    {"type":"keluar", "desc":"Jajan", "amount": 100000},
]

@app.route('/finance', methods=['GET', 'POST'])
def finance():
    error = None
    if request.method == 'POST':
        tipe = request.form.get('type')
        desc = request.form.get('desc', '').strip()
        amount_text = request.form.get('amount', '').strip()
        if not desc:
            error = "Deskripsi harus diisi!"
        elif not amount_text:
            error = "Jumlah harus diisi"
        else:
            amount = int(amount_text)
            if amount <= 0:
                error = "Jumlah harus lebih dari 0"
            else:
                transactions.append({
                    "type": tipe,
                    "desc": desc,
                    "amount": amount
                })
    saldo = sum(
        t['amount'] if t['type'] == 'masuk' else -t['amount']
        for t in transactions
    )
    total_in = sum(
        t['amount']
        for t in transactions
        if t['type'] == 'masuk'
    )
    total_out = sum(
        t['amount']
        for t in transactions
        if t['type'] == 'keluar'
    )
    return render_template(
        'finance.html',
        transactions = transactions,
        saldo = saldo,
        total_in = total_in,
        total_out = total_out,
        error = error
    )    
    
from flask import redirect
@app.route('/hapus/<int:index>')
def hapus(index):
    if 0 <= index < len(transactions):
        del transactions[index]
    return redirect('/finance')

todo_list = [] #berguna menyimpan data todo list

@app.route('/todo', methods=['GET', 'POST'])
def todo():
    if request.method == 'POST':
        item = request.form['item']
        if item != '':
            todo_list.append(item)
        return redirect('/todo')
    return render_template('todo.html', todos=todo_list)

@app.route('/todo/edit/<int:index>', methods=['GET', 'POST'])
def todo_edit(index):
    if request.method == 'POST':
        todo_list[index] = request.form['item']
        return redirect('/todo')
    return render_template('todo.html', 
                           todos=todo_list,
                           edit_index=index, 
                           edit_value=todo_list[index])

@app.route('/todo/hapus/<int:index>')
def todo_hapus(index):
    todo_list.pop(index)
    return redirect('/todo')

# Route Halaman Skills
@app.route('/skills')
def skills():
    skills_list = [
        {"name": "Python", "level": "Advanced", "percent": 90},
        {"name": "Flask", "level": "Intermediate", "percent": 75},
        {"name": "HTML/CSS", "level": "Intermediate", "percent": 80},
        {"name": "Git & GitHub", "level": "Intermediate", "percent": 70},
        {"name": "Data Science (Pandas, dsb)", "level": "Intermediate", "percent": 75}
    ]
    return render_template('skills.html', skills=skills_list)

# Route Halaman Experience
@app.route('/experience')
def experience():
    exp_list = [
        {
            "year": "2024 - 2025", 
            "title": "Mahasiswa Informatika", 
            "desc": "Mempelajari dasar-dasar pemrograman, struktur data, algoritma, serta pengembangan aplikasi web."
        },
        {
            "year": "2025 - 2026", 
            "title": "Coding Mentor", 
            "desc": "Membimbing siswa dalam memahami logika pemrograman Python, dasar web, dan pembuatan proyek kreatif."
        },
        {
            "year": "2026 - Sekarang", 
            "title": "AI & Python Educator", 
            "desc": "Merancang kurikulum dan mengajar pemrograman tingkat lanjut, pembuatan GUI, serta pengembangan perangkat lunak."
        }
    ]
    return render_template('experience.html', experiences=exp_list)

if __name__ == '__main__':
    app.run(debug=True)
    
