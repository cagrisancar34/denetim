from flask import Flask, render_template, request, jsonify, send_file
from data_utils import load_data, save_data
from score_utils import calculate_score, get_failed_questions, get_category_scores, extract_answers
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///denetimler.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Denetim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tesis_adi = db.Column(db.String(128))
    tarih = db.Column(db.String(32))
    denetim_yapan = db.Column(db.String(128))
    cevaplar = db.Column(db.Text)  # JSON string olarak saklanacak
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

DATA_FILE = os.path.join(app.root_path, "data.json")
categories = load_data()

@app.before_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add_category", methods=["POST"])
def add_category():
    category = request.form.get("category")
    if category and category not in categories:
        categories[category] = []
        save_data(categories)
        return jsonify({"success": True, "categories": list(categories.keys())})
    return jsonify({"success": False})

@app.route("/add_question", methods=["POST"])
def add_question():
    category = request.form.get("category")
    question = request.form.get("question")
    if category in categories and question:
        categories[category].append(question)
        save_data(categories)
        return jsonify({"success": True, "questions": categories[category]})
    return jsonify({"success": False})

@app.route("/add_questions", methods=["POST"])
def add_questions():
    data = request.get_json()
    category = data.get("category")
    questions = data.get("questions", [])
    if category in categories and questions:
        for q in questions:
            if q:
                categories[category].append(q)
        save_data(categories)
        return jsonify({"success": True, "questions": categories[category]})
    return jsonify({"success": False})

@app.route("/submit", methods=["POST"])
def submit():
    form_data = request.form.to_dict()
    answers = extract_answers(form_data, categories)
    score, total = calculate_score(answers, categories)
    failed_questions = get_failed_questions(answers, categories)
    category_scores = get_category_scores(answers, categories)
    denetim = Denetim(
        tesis_adi=form_data.get("tesis_adi", ""),
        tarih=form_data.get("denetim_tarihi", ""),
        denetim_yapan=form_data.get("denetim_yapan", ""),
        cevaplar=json.dumps(answers)
    )
    db.session.add(denetim)
    db.session.commit()
    return render_template("submit.html", form_data=answers, categories=categories, score=score, total=total, failed_questions=failed_questions, category_scores=category_scores)

@app.route("/kategori")
def kategori():
    return render_template("kategori.html", categories=categories)

@app.route("/tesis_karnesi")
def tesis_karnesi():
    # Son denetim kaydını veritabanından oku
    d = Denetim.query.order_by(Denetim.created_at.desc()).first()
    if d:
        last = json.loads(d.cevaplar)
    else:
        last = {}
    score, total = calculate_score(last, categories)
    failed_questions = get_failed_questions(last, categories)
    category_scores = get_category_scores(last, categories)
    return render_template("tesis_karnesi.html", form_data=last, categories=categories, score=score, total=total, failed_questions=failed_questions, category_scores=category_scores)

@app.route("/get_last_denetim")
def get_last_denetim():
    d = Denetim.query.order_by(Denetim.created_at.desc()).first()
    if d:
        cevaplar = json.loads(d.cevaplar)
        cevaplar["tesis_adi"] = d.tesis_adi
        cevaplar["tarih"] = d.tarih
        cevaplar["denetim_yapan"] = d.denetim_yapan
        return jsonify({"form_data": cevaplar, "categories": categories})
    else:
        return jsonify({"form_data": {}, "categories": categories})

@app.route("/get_all_denetimler")
def get_all_denetimler():
    denetimler = Denetim.query.order_by(Denetim.created_at).all()
    result = []
    for d in denetimler:
        cevaplar = json.loads(d.cevaplar)
        cevaplar["tesis_adi"] = d.tesis_adi
        cevaplar["tarih"] = d.tarih
        cevaplar["denetim_yapan"] = d.denetim_yapan
        result.append(cevaplar)
    return jsonify({"denetimler": result, "categories": categories})

@app.route("/tesis_karnesi_data")
def tesis_karnesi_data():
    tesis_adi = request.args.get("tesis_adi", "")
    denetimler = Denetim.query.order_by(Denetim.created_at).all()
    filtered = []
    for d in denetimler:
        cevaplar = json.loads(d.cevaplar)
        if not tesis_adi or d.tesis_adi == tesis_adi:
            cevaplar["tesis_adi"] = d.tesis_adi
            cevaplar["tarih"] = d.tarih
            cevaplar["denetim_yapan"] = d.denetim_yapan
            filtered.append(cevaplar)
    if filtered:
        form_data = filtered[-1]
        score, total = calculate_score(form_data, categories)
        category_scores = get_category_scores(form_data, categories)
        failed_questions = get_failed_questions(form_data, categories)
        return jsonify({
            "score": score,
            "total": total,
            "category_scores": category_scores,
            "failed_questions": failed_questions,
            "form_data": form_data
        })
    else:
        return jsonify({
            "score": 0,
            "total": 0,
            "category_scores": {},
            "failed_questions": [],
            "form_data": {}
        })

@app.route("/export_excel")
def export_excel():
    denetimler = Denetim.query.order_by(Denetim.created_at).all()
    rows = []
    for d in denetimler:
        cevaplar = json.loads(d.cevaplar)
        row = {
            "tesis_adi": d.tesis_adi,
            "tarih": d.tarih,
            "denetim_yapan": d.denetim_yapan,
            **cevaplar
        }
        rows.append(row)
    if not rows:
        return "Hiç denetim kaydı yok.", 404
    df = pd.DataFrame(rows)
    excel_path = os.path.join(app.root_path, "denetimler_export.xlsx")
    df.to_excel(excel_path, index=False)
    return send_file(excel_path, as_attachment=True)

@app.route("/form")
def form():
    return render_template("form.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)
