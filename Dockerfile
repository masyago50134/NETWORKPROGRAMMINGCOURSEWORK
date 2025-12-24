# Використовуємо легку версію Python
FROM python:3.9-slim

# Встановлюємо робочу директорію всередині контейнера
WORKDIR /app

# Копіюємо файл зі списком залежностей
COPY requirements.txt .

# Встановлюємо бібліотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту (main.py та інші файли)
COPY . .

# Відкриваємо порт 8000 (той самий, що в ЛБ2 та нашому коді)
EXPOSE 8000

# Команда для запуску застосунку
CMD ["python", "main.py"]