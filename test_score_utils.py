import unittest
from score_utils import calculate_score, get_failed_questions, get_category_scores, extract_answers

class TestScoreUtils(unittest.TestCase):
    def setUp(self):
        self.categories = {
            "Kategori1": ["Soru1", "Soru2"],
            "Kategori2": ["Soru3"]
        }
        self.form_data = {
            "Soru1": "Evet",
            "Soru2": "Hayır",
            "Soru3": "Yok"
        }

    def test_calculate_score(self):
        score, total = calculate_score(self.form_data, self.categories)
        self.assertEqual(score, 1)
        self.assertEqual(total, 2)

    def test_get_failed_questions(self):
        failed = get_failed_questions(self.form_data, self.categories)
        self.assertIn(("Soru2", "Kategori1"), failed)

    def test_get_category_scores(self):
        scores = get_category_scores(self.form_data, self.categories)
        self.assertEqual(scores["Kategori1"]["score"], 1)
        self.assertEqual(scores["Kategori1"]["max_score"], 2)

    def test_extract_answers(self):
        answers = extract_answers(self.form_data, self.categories)
        self.assertEqual(answers["Soru1"], "Evet")

if __name__ == "__main__":
    unittest.main()
