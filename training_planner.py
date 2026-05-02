import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_training():
    date = entry_date.get()
    tr_type = entry_type.get()
    duration = entry_duration.get()

    # Валидация
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
        return

    try:
        duration = float(duration)
        if duration <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
        return

    # Добавление в таблицу и данные
    data.append({"date": date, "type": tr_type, "duration": duration})
    save_data(data)
    update_table()

def filter_data():
    f_type = filter_type.get()
    f_date = filter_date.get()

    filtered = data.copy()

    if f_type:
        filtered = [x for x in filtered if x["type"] == f_type]
    if f_date:
        try:
            datetime.strptime(f_date, "%Y-%m-%d")
            filtered = [x for x in filtered if x["date"] == f_date]
        except ValueError:
            messagebox.showerror("Ошибка", "Дата фильтра должна быть в формате ГГГГ-ММ-ДД")
            return

    update_table(filtered)

def update_table(filtered_data=None):
    for i in tree.get_children():
        tree.delete(i)
    for item in (filtered_data or data):
        tree.insert("", "end", values=(item["date"], item["type"], item["duration"]))

# Загрузка данных
data = load_data()

# Создание окна
root = tk.Tk()
root.title("Training Planner")
root.geometry("600x400")

# Ввод данных
frame_input = tk.LabelFrame(root, text="Добавить тренировку")
frame_input.pack(pady=10, fill="x")

tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Тип:").grid(row=1, column=0, padx=5, pady=5)
entry_type = tk.Entry(frame_input)
entry_type.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Длительность:").grid(row=2, column=0, padx=5, pady=5)
entry_duration = tk.Entry(frame_input)
entry_duration.grid(row=2, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_input, text="Добавить тренировку", command=add_training)
btn_add.grid(row=3, columnspan=2, pady=10)

# Фильтрация
frame_filter = tk.LabelFrame(root, text="Фильтр")
frame_filter.pack(pady=10, fill="x")

tk.Label(frame_filter, text="Тип:").grid(row=0, column=0, padx=5, pady=5)
filter_type = tk.Entry(frame_filter)
filter_type.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_filter, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0, padx=5, pady=5)
filter_date = tk.Entry(frame_filter)
filter_date.grid(row=1, column=1, padx=5, pady=5)

btn_filter = tk.Button(frame_filter, text="Фильтровать", command=filter_data)
btn_filter.grid(row=2, columnspan=2, pady=10)

# Таблица
tree = ttk.Treeview(root, columns=("date", "type", "duration"), show="headings")
tree.heading("date", text="Дата")
tree.heading("type", text="Тип")
tree.heading("duration", text="Длительность")
tree.pack(fill="both", expand=True)

# Обновление таблицы при запуске
update_table()

root.mainloop()
