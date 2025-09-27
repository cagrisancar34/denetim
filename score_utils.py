def calculate_score(form_data, categories):
    try:
        score = 0
        total = 0
        for category, questions in categories.items():
            for question in questions:
                answer = form_data.get(question)
                if answer == "Evet":
                    score += 1
                    total += 1
                elif answer == "Hayır":
                    total += 1
        return score, total
    except Exception as e:
        print(f"Skor hesaplanırken hata oluştu: {e}")
        return 0, 0

def get_failed_questions(form_data, categories):
    try:
        failed = []
        for category, questions in categories.items():
            for question in questions:
                answer = form_data.get(question)
                if answer == "Hayır":
                    failed.append((question, category))
        return failed
    except Exception as e:
        print(f"Başarısız sorular alınırken hata oluştu: {e}")
        return []

def get_category_scores(form_data, categories):
    try:
        category_scores = {}
        for category, questions in categories.items():
            score = 0
            max_score = 0
            for question in questions:
                answer = form_data.get(question)
                if answer == "Evet":
                    score += 1
                    max_score += 1
                elif answer == "Hayır":
                    max_score += 1
            success_rate = (score / max_score * 100) if max_score > 0 else 0
            category_scores[category] = {
                "score": score,
                "max_score": max_score,
                "success_rate": round(success_rate, 2)
            }
        return category_scores
    except Exception as e:
        print(f"Kategori skorları alınırken hata oluştu: {e}")
        return {}

def extract_answers(form_data, categories):
    try:
        answers = {}
        explanations = {}
        for category, questions in categories.items():
            for question in questions:
                if question in form_data:
                    answers[question] = form_data[question]
                if f"aciklama_{question}" in form_data:
                    explanations[question] = form_data[f"aciklama_{question}"]
        for k in ["tesis_adi", "denetim_tarihi", "denetim_yapan"]:
            if k in form_data:
                answers[k] = form_data[k]
        for k, v in explanations.items():
            answers[f"aciklama_{k}"] = v
        return answers
    except Exception as e:
        print(f"Cevaplar çıkarılırken hata oluştu: {e}")
        return {}
