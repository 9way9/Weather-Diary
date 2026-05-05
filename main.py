import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("800x600")

        # Загрузка записей
        self.records = self.load_records()
        self.setup_ui()

    def setup_ui(self):
        # Поле ввода даты
        ttk.Label(self.root, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = ttk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)


        # Поле ввода температуры
        ttk.Label(self.root, text="Температура (°C):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.temp_entry = ttk.Entry(self.root)
        self.temp_entry.grid(row=1, column=1, padx=10, pady=5)

        # Поле ввода описания погоды
        ttk.Label(self.root, text="Описание погоды:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.desc_entry = ttk.Entry(self.root, width=40)
        self.desc_entry.grid(row=2, column=1, padx=10, pady=5)

        # Выбор осадков
        ttk.Label(self.root, text="Осадки:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.precipitation_var = tk.StringVar(value="нет")
        ttk.Radiobutton(self.root, text="Да", variable=self.precipitation_var, value="да").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self.root, text="Нет", variable=self.precipitation_var, value="нет").grid(row=3, column=1, padx=80, sticky="w")

        # Кнопка добавления записи
        self.add_btn = ttk.Button(self.root, text="Добавить запись", command=self.add_record)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        ttk.Label(self.root, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.filter_date_entry = ttk.Entry(self.root)
        self.filter_date_entry.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Фильтр по температуре (>°C):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.filter_temp_entry = ttk.Entry(self.root)
        self.filter_temp_entry.grid(row=6, column=1, padx=10, pady=5)

        self.apply_filter_btn = ttk.Button(self.root, text="Применить фильтры", command=self.refresh_records_table)
        self.apply_filter_btn.grid(row=7, column=0, columnspan=2, pady=5)

        # Таблица записей
        ttk.Label(self.root, text="Записи о погоде:").grid(row=8, column=0, columnspan=2, pady=10)
        columns = ("Дата", "Температура", "Описание", "Осадки")
        self.records_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=12)

        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=150)

        self.records_tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Заполнение таблицы
        self.refresh_records_table()

    def load_records(self):
        if os.path.exists("weather_records.json"):
            with open("weather_records.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_records(self):
        with open("weather_records.json", "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)


    def add_record(self):
        date_str = self.date_entry.get().strip()
        temp_str = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = self.precipitation_var.get()

        # Валидация даты
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД")
            return

        # Валидация температуры
        try:
            temperature = float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return

        # Валидация описания
        if not description:
            messagebox.showerror("Ошибка", "Описание погоды не может быть пустым")
            return

        # Добавление записи
        record = {
            "date": date_str,
            "temperature": temperature,
            "description": description,
            "precipitation": precipitation
        }
        self.records.append(record)
        self.save_records()
        self.refresh_records_table()

        # Очистка полей ввода
        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set("нет")

        messagebox.showinfo("Успех", "Запись добавлена")

    def refresh_records_table(self):
        # Очистка таблицы
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)

        # Получение фильтров
        filter_date = self.filter_date_entry.get().strip()
        filter_temp_str = self.filter_temp_entry.get().strip()

        filtered_records = self.records

        # Фильтр по дате
        if filter_date:
            filtered_records = [r for r in filtered_records if r["date"] == filter_date]


        # Фильтр по температуре
        if filter_temp_str:
            try:
                filter_temp = float(filter_temp_str)
                filtered_records = [r for r in filtered_records if r["temperature"] > filter_temp]
            except ValueError:
                messagebox.showwarning("Предупреждение", "Некорректное значение температуры для фильтра")


        # Заполнение таблицы отфильтрованными записями
        for record in filtered_records:
            self.records_tree.insert("", "end", values=(
                record["date"],
                f"{record['temperature']}°C",
                record["description"],
                record["precipitation"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
