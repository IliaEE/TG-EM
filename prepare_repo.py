import os
import json

BASE_DIR = os.getcwd()
PART_FOLDERS = [
    'Static Emoji by @EmojiSaverBot (part 1)',
    'Static Emoji by @EmojiSaverBot (part 2)',
    'Static Emoji by @EmojiSaverBot (part 3)',
    'Static Emoji by @EmojiSaverBot (part 4)'
]

emoji_list = []

print("🚀 Начинаю сканирование папок...")

for part in PART_FOLDERS:
    part_path = os.path.join(BASE_DIR, part)
    
    if not os.path.exists(part_path):
        print(f"⚠️ Папка {part} не найдена, пропускаю.")
        continue
        
    print(f"📂 Сканирую: {part}...")
    
    for item in os.listdir(part_path):
        item_path = os.path.join(part_path, item)
        
        if os.path.isdir(item_path) and not item.startswith('.'):
            json_file = os.path.join(item_path, f"{item}.json")
            png_file = os.path.join(item_path, f"{item}.png")
            
            if os.path.exists(json_file) and os.path.exists(png_file):
                emoji_list.append({
                    "id": item,
                    "path": f"{part}/{item}"
                })

emoji_list.sort(key=lambda x: x['id'])

with open('emojis.js', 'w', encoding='utf-8') as f:
    f.write("// Автоматически сгенерированная база данных эмодзи\n")
    f.write(f"const emojiList = {json.dumps(emoji_list, indent=4)};")

print(f"✅ Готово! Индексировано эмодзи: {len(emoji_list)}")

html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Animated Emojis Library</title>
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <style>
        :root {
            --tg-blue: #2481cc;
            --tg-hover-blue: #1e71b3;
            --bg-color: #eff3f6;
            --card-bg: #ffffff;
            --text-color: #222222;
            --text-muted: #707579;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
        }
        header { text-align: center; margin-bottom: 30px; }
        header h1 { margin: 0 0 10px 0; font-size: 28px; color: #212121; }
        .container { max-width: 1200px; margin: 0 auto; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .card {
            background: var(--card-bg);
            border-radius: 14px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
            display: flex;
            flex-direction: column;
            align-items: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        }
        .preview-container {
            width: 100px;
            height: 100px;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }
        .preview-container img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            position: absolute;
            z-index: 2;
            transition: opacity 0.15s;
        }
        .preview-container lottie-player {
            width: 100%;
            height: 100%;
            position: absolute;
            z-index: 1;
        }
        .card:hover .preview-container img { opacity: 0; }
        .name {
            font-size: 10px;
            color: var(--text-muted);
            margin: 12px 0;
            text-align: center;
            width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .download-btn {
            background-color: var(--tg-blue);
            color: white;
            border: none;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 600;
            border-radius: 8px;
            text-decoration: none;
            width: 100%;
            text-align: center;
            box-sizing: border-box;
            transition: background-color 0.15s;
        }
        .download-btn:hover { background-color: var(--tg-hover-blue); }
        .pagination {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 8px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        .page-btn {
            background: var(--card-bg);
            border: 1px solid #dcdfe6;
            color: var(--text-color);
            padding: 8px 14px;
            font-size: 14px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .page-btn:hover:not(:disabled) { border-color: var(--tg-blue); color: var(--tg-blue); }
        .page-btn.active { background-color: var(--tg-blue); border-color: var(--tg-blue); color: white; }
        .page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Telegram Animated Emojis Library</h1>
            <p id="totalCount">Загрузка...</p>
        </header>
        <div class="grid" id="emojiGrid"></div>
        <div class="pagination" id="paginationControls"></div>
    </div>

    <script src="emojis.js"></script>
    <script>
        const ITEMS_PER_PAGE = 60;
        let currentPage = 1;

        const grid = document.getElementById('emojiGrid');
        const paginationControls = document.getElementById('paginationControls');
        const totalCountEl = document.getElementById('totalCount');

        function initLibrary() {
            if (typeof emojiList === 'undefined' || emojiList.length === 0) {
                totalCountEl.innerText = "Список пуст. Проверьте папки.";
                return;
            }
            totalCountEl.innerText = `Всего: ${emojiList.length} эмодзи • Наведите курсор для анимации`;
            renderPage(1);
        }

        function renderPage(page) {
            currentPage = page;
            grid.innerHTML = '';

            const startIndex = (page - 1) * ITEMS_PER_PAGE;
            const endIndex = Math.min(startIndex + ITEMS_PER_PAGE, emojiList.length);
            const pageItems = emojiList.slice(startIndex, endIndex);

            pageItems.forEach(item => {
                const jsonPath = `${item.path}/${item.id}.json`;
                const pngPath = `${item.path}/${item.id}.png`;

                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                    <div class="preview-container">
                        <img src="${pngPath}" alt="${item.id}" loading="lazy">
                        <lottie-player src="${jsonPath}" background="transparent" speed="1" loop autoplay></lottie-player>
                    </div>
                    <div class="name" title="${item.id}">${item.id}</div>
                    <a href="${jsonPath}" download="${item.id}.json" class="download-btn">Скачать JSON</a>
                `;
                grid.appendChild(card);
            });

            renderControls();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function renderControls() {
            paginationControls.innerHTML = '';
            const totalPages = Math.ceil(emojiList.length / ITEMS_PER_PAGE);
            if (totalPages <= 1) return;

            const prevBtn = document.createElement('button');
            prevBtn.className = 'page-btn';
            prevBtn.innerText = '«';
            prevBtn.disabled = currentPage === 1;
            prevBtn.onclick = () => renderPage(currentPage - 1);
            paginationControls.appendChild(prevBtn);

            let startPage = Math.max(1, currentPage - 2);
            let endPage = Math.min(totalPages, startPage + 4);
            if (endPage - startPage < 4) startPage = Math.max(1, endPage - 4);

            for (let i = startPage; i <= endPage; i++) {
                const pageBtn = document.createElement('button');
                pageBtn.className = `page-btn ${i === currentPage ? 'active' : ''}`;
                pageBtn.innerText = i;
                pageBtn.onclick = () => renderPage(i);
                paginationControls.appendChild(pageBtn);
            }

            const nextBtn = document.createElement('button');
            nextBtn.className = 'page-btn';
            nextBtn.innerText = '»';
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.onclick = () => renderPage(currentPage + 1);
            paginationControls.appendChild(nextBtn);
        }

        document.addEventListener("DOMContentLoaded", initLibrary);
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("📝 Файлы index.html и emojis.js успешно созданы!")