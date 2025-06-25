# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Пути к данным
DATA_DIR = 'data'
LIBRARY_FILE = os.path.join(DATA_DIR, 'library.json')
BOOKS_DIR = os.path.join(DATA_DIR, 'books')


# Загрузка библиотеки
def load_library():
    try:
        with open(LIBRARY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                return []
            return json.loads(content)
    except Exception as e:
        print(f"Ошибка при загрузке библиотеки: {e}")
        return []


# Сохранение библиотеки
def save_library(library):
    try:
        with open(LIBRARY_FILE, 'w', encoding='utf-8') as f:
            json.dump(library, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении библиотеки: {e}")


# Загрузка книги
def load_book(book_id):
    try:
        book_path = os.path.join(BOOKS_DIR, f'{book_id}.json')
        if os.path.exists(book_path):
            with open(book_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    return None
                return json.loads(content)
        return None
    except Exception as e:
        print(f"Ошибка при загрузке книги {book_id}: {e}")
        return None


# Сохранение книги
def save_book(book_id, book_data):
    try:
        book_path = os.path.join(BOOKS_DIR, f'{book_id}.json')
        with open(book_path, 'w', encoding='utf-8') as f:
            json.dump(book_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении книги {book_id}: {e}")


# Генерация ID
def generate_id():
    return int(datetime.now().timestamp() * 1000)


# Главная страница (Библиотека)
@app.route('/')
def library():
    library_data = load_library()
    return render_template('library.html', library=library_data)


# Страница книги
@app.route('/book/<int:book_id>')
def book_page(book_id):
    book = load_book(book_id)
    if not book:
        return "Книга не найдена", 404
    return render_template('book.html', book=book)


# Страница главы
@app.route('/book/<int:book_id>/chapter/<int:chapter_id>')
def chapter_page(book_id, chapter_id):
    book = load_book(book_id)
    if not book:
        return "Книга не найдена", 404

    chapter = next((ch for ch in book['chapters'] if ch['id'] == chapter_id), None)
    if not chapter:
        return "Глава не найдена", 404

    return render_template('chapter.html', book=book, chapter=chapter)


# Админ-панель
@app.route('/admin')
def admin_panel():
    library_data = load_library()
    return render_template('admin.html', library=library_data)


# Добавление новой книги
@app.route('/admin/new_book', methods=['POST'])
def new_book():
    title = request.form['title']
    author = request.form['author']

    if not title or not author:
        return "Не заполнены обязательные поля", 400

    library_data = load_library()
    book_id = generate_id()

    library_data.append({
        'id': book_id,
        'title': title,
        'author': author,
        'created': datetime.now().isoformat()
    })
    save_library(library_data)

    new_book = {
        'id': book_id,
        'title': title,
        'author': author,
        'chapters': []
    }
    save_book(book_id, new_book)

    return redirect(url_for('admin_panel'))


# Добавление новой главы
@app.route('/admin/new_chapter', methods=['POST'])
def new_chapter():
    book_id = int(request.form['book_id'])
    title = request.form['title']

    if not title:
        return "Не заполнены обязательные поля", 400

    book = load_book(book_id)
    if not book:
        return "Книга не найдена", 404

    chapter_id = generate_id()
    book['chapters'].append({
        'id': chapter_id,
        'title': title,
        'sections': []
    })
    save_book(book_id, book)

    return redirect(url_for('admin_panel'))


# Добавление нового фрагмента
@app.route('/admin/new_section', methods=['POST'])
def new_section():
    book_id = int(request.form['book_id'])
    chapter_id = int(request.form['chapter_id'])
    content = request.form['content']
    comment = request.form['comment']

    if not content:
        return "Не заполнены обязательные поля", 400

    book = load_book(book_id)
    if not book:
        return "Книга не найдена", 404

    chapter = next((ch for ch in book['chapters'] if ch['id'] == chapter_id), None)
    if not chapter:
        return "Глава не найдена", 404

    section_id = generate_id()
    chapter['sections'].append({
        'id': section_id,
        'content': content,
        'comment': comment
    })
    save_book(book_id, book)

    return redirect(url_for('admin_panel'))

@app.route('/admin/get_chapters')
def get_chapters():
    book_id = int(request.args.get('book_id'))
    book = load_book(book_id)
    if not book:
        return jsonify([])
    return jsonify(book.get('chapters', []))

if __name__ == '__main__':
    init_data()
    app.run(debug=True)