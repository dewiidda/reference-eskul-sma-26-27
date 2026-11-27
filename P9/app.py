from flask import Flask, render_template, request

app = Flask(__name__)

students = [
    {"nama": "Andi", "nilai": 80},
    {"nama": "Budi", "nilai": 65}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/student-tracker', methods=['GET', 'POST'])
def student_tracker():
    error = None
    if request.method == 'POST':
        nama = request.form.get('nama', '').strip()
        nilai_text = request.form.get('nilai', '').strip()
        if not nama:
            error = "Nama harus diisi."

        elif not nilai_text:
            error = "Nilai harus diisi."

        else:
            nilai = int(nilai_text)

            if nilai < 0 or nilai > 100:
                error = "Nilai harus antara 0-100."
            else:
                students.append({
                    "nama": nama,
                    "nilai": nilai
                })
    avg = (
        sum(s['nilai'] for s in students) / len(students)
        if students else 0
    )
    return render_template(
        'student_tracker.html',
        students=students,
        avg=avg,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)