from datetime import datetime
import json
import itertools


with open("results_RUN.txt", "r", encoding="utf-8-sig") as results_file:
    results_data = results_file.read().splitlines()

with open("competitors2.json", "r", encoding="utf-8") as competitors_file:
    competitors_data = json.load(competitors_file)

results_dct = {}
for line in results_data:
    line = line.split()
    bib_number = line[0]
    date_string = line[-1]
    date = datetime.strptime(date_string, "%H:%M:%S,%f")

    if bib_number not in results_dct:
        results_dct[bib_number] = date
    else:
        time_diff = date - results_dct[bib_number]
        results_dct[bib_number] = (datetime.min + time_diff).strftime("%M:%S,%f")

sorted_results = dict(sorted(results_dct.items(), key=lambda item: item[1]))

first_four_results = dict(itertools.islice(sorted_results.items(), 4))

final_result = dict()
for place, key in enumerate(first_four_results, start=1):
    name = competitors_data[key]["Name"]
    surname = competitors_data[key]["Surname"]
    print(place, key, name, surname, sorted_results[key])
    final_result[str(place)] = {
        "Нагрудный номер": key,
        "Имя": name,
        "Фамилия": surname,
        "Результат": sorted_results[key],
    }


with open("final_results.json", "w", encoding="utf-8") as data_file:
    json.dump(final_result, data_file, ensure_ascii=False)

print("Результат")
print(
    "| {:<14} | {:<15} | {:<10} | {:<10} | {:<12} |".format(
        "Занятое место", "Нагрудный номер", "Имя", "Фамилия", "Результат"
    )
)
print("-" * 77)
for place, result in enumerate(final_result.values(), start=1):
    print(
        "| {:<14} | {:<15} | {:<10} | {:<10} | {:<12} |".format(
            place,
            result["Нагрудный номер"],
            result["Имя"],
            result["Фамилия"],
            result["Результат"],
        )
    )
