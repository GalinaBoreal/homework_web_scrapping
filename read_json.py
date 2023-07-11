import json

with open('vacancies.json', 'r', encoding='utf-8') as f:
    text = json.load(f)

print(f"Всего вакансий: {len(text['vacancies'])}")
for v in text['vacancies']:
    print(v)