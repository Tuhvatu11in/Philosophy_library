// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const textSections = document.querySelectorAll('.text-section');
    const sidebar = document.getElementById('commentary-sidebar');
    const closeBtn = document.getElementById('close-sidebar');
    const commentText = document.getElementById('comment-text');

    // Обработка клика по тексту
    if (textSections) {
        textSections.forEach(section => {
            section.addEventListener('click', () => {
                const comment = section.dataset.comment;
                commentText.textContent = comment || 'Комментарий отсутствует';
                sidebar.classList.add('active');
            });
        });
    }

    // Закрытие сайдбара
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            sidebar.classList.remove('active');
        });
    }

    // Закрытие по клику вне области
    document.addEventListener('click', (e) => {
        if (sidebar.classList.contains('active') &&
            !sidebar.contains(e.target) &&
            !e.target.classList.contains('text-section')) {
            sidebar.classList.remove('active');
        }
    });
});

document.getElementById('book-select').addEventListener('change', function() {
    const bookId = this.value;
    const chapterSelect = document.getElementById('chapter-select');

    if (!bookId) {
        chapterSelect.disabled = true;
        chapterSelect.innerHTML = '<option value="">Сначала выберите книгу</option>';
        return;
    }

    // Загружаем главы для выбранной книги
    fetch(`/admin/get_chapters?book_id=${bookId}`)
        .then(response => response.json())
        .then(chapters => {
            chapterSelect.disabled = false;
            chapterSelect.innerHTML = '<option value="">Выберите главу</option>';

            chapters.forEach(chapter => {
                const option = document.createElement('option');
                option.value = chapter.id;
                option.textContent = chapter.title || `Глава ${chapter.id}`;
                chapterSelect.appendChild(option);
            });
        });
});