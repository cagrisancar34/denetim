import os
import json

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")
DENETIM_FILE = os.path.join(os.path.dirname(__file__), "denetimler.json")

def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Veri yüklenirken hata oluştu: {e}")
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Veri kaydedilirken hata oluştu: {e}")

def save_denetim(data):
    try:
        if os.path.exists(DENETIM_FILE):
            with open(DENETIM_FILE, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        else:
            all_data = []
        all_data.append(data)
        with open(DENETIM_FILE, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Denetim kaydedilirken hata oluştu: {e}")
