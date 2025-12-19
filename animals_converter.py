import csv
import json


def create_animals_csv(csv_path: str) -> None:
    data = [
        ["Животное", "Среда обитания"],
        ["Медведь", "Лес"],
        ["Дельфин", "Океан"],
        ["Верблюд", "Пустыня"],
    ]

    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)



def convert_csv_to_json(csv_path: str, json_path: str) -> None:
    result = []

    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)

    with open(json_path, mode="w", encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)



def convert_json_to_csv(json_path: str, csv_path: str) -> None:
    with open(json_path, mode="r", encoding="utf-8") as file:
        data = json.load(file)

    if not data:
        return

    headers = data[0].keys()

    with open(csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)



if __name__ == "__main__":
    create_animals_csv("animals.csv")
    convert_csv_to_json("animals.csv", "animals.json")
    convert_json_to_csv("animals.json", "animals_from_json.csv")
