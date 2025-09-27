from flask import Flask, render_template, request, jsonify
import os
import json
from data_utils import load_data, save_data, save_denetim
from score_utils import calculate_score, get_failed_questions, get_category_scores, extract_answers

app = Flask(__name__)

DATA_FILE = os.path.join(app.root_path, "data.json")
DENETIM_FILE = os.path.join(app.root_path, "denetimler.json")

categories = load_data()

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
    save_denetim(answers)
    return render_template("submit.html", form_data=answers, categories=categories, score=score, total=total, failed_questions=failed_questions, category_scores=category_scores)

@app.route("/kategori")
def kategori():
    return render_template("kategori.html", categories=categories)

@app.route("/tesis_karnesi")
def tesis_karnesi():
    # Son denetim kaydını oku
    if os.path.exists(DENETIM_FILE):
        with open(DENETIM_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        if all_data:
            last = all_data[-1]
        else:
            last = {}
    else:
        last = {}
    score, total = calculate_score(last, categories)
    failed_questions = get_failed_questions(last, categories)
    category_scores = get_category_scores(last, categories)
    return render_template("tesis_karnesi.html", form_data=last, categories=categories, score=score, total=total, failed_questions=failed_questions, category_scores=category_scores)

@app.route("/get_last_denetim")
def get_last_denetim():
    if os.path.exists(DENETIM_FILE):
        with open(DENETIM_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        if all_data:
            last = all_data[-1]
        else:
            last = {}
    else:
        last = {}
    return jsonify({"form_data": last, "categories": categories})

@app.route("/get_all_denetimler")
def get_all_denetimler():
    if os.path.exists(DENETIM_FILE):
        with open(DENETIM_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
    else:
        all_data = []
    return jsonify({"denetimler": all_data, "categories": categories})

# Yeni endpoint: Tesis Karnesi için JSON veri
@app.route("/tesis_karnesi_data")
def tesis_karnesi_data():
    tesis_adi = request.args.get("tesis_adi", "")
    with open(DENETIM_FILE, "r", encoding="utf-8") as f:
        all_denetimler = json.load(f)
    filtered = []
    for d in all_denetimler:
        if not tesis_adi or d.get("tesis_adi", "") == tesis_adi:
            filtered.append(d)
    # Son denetimi gösterelim (veya ortalama alınabilir)
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

@app.route("/form")
def form():
    return render_template("form.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)
