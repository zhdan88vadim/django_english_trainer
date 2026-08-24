import random
import string
from math import ceil

def read_file(filename):
    pairs = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and ';' in line:
                ru, en = line.split(';', 1)
                pairs.append((ru.strip(), en.strip()))
    return pairs

def generate_html(pairs, cols=5):
    n = len(pairs)
    
    # Генерируем координаты
    rows = ceil(n / cols)
    letters = string.ascii_uppercase[:cols]
    all_coords = [f"{letters[c]}{r+1}" for r in range(rows) for c in range(cols)]
    coords = all_coords[:n]
    random.shuffle(coords)
    
    # Задания -> координаты
    task_coords = {}
    for i, coord in enumerate(coords, 1):
        task_coords[i] = coord
    
    # Координаты -> ответы
    coord_answer = {}
    for i, (ru, en) in enumerate(pairs, 1):
        coord_answer[task_coords[i]] = f"{i}) {en}"
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Тренажёр</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }}
        td, th {{
            border: 1px solid #333;
            padding: 8px 12px;
            text-align: left;
        }}
        .task-num {{
            font-weight: bold;
            width: 30px;
        }}
        .task-ru {{
            width: 400px;
        }}
        .task-ref {{
            font-weight: bold;
            color: red;
            width: 60px;
            text-align: center;
        }}
        .sep {{
            border: none;
            border-top: 3px solid #999;
            margin: 30px 0;
        }}
        .grid-table {{
            border-collapse: collapse;
            margin: 10px auto;
            width: 100%;
        }}
        .grid-table td {{
            border: 2px solid #000;
            padding: 12px 8px;
            text-align: center;
            font-size: 14px;
            width: {100/cols}%;
            height: 50px;
        }}
        .coord {{
            font-weight: bold;
            font-size: 12px;
            color: #0066cc;
        }}
        .answer {{
            font-size: 14px;
        }}
        .empty-cell {{
            background: #f0f0f0;
        }}
        .instructions {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px 15px;
            margin: 15px 0;
            font-size: 14px;
        }}
    </style>
</head>
<body>

<h2>📝 Русский → Английский</h2>

<div class="instructions">
    <b>Как работать:</b> Переведи предложение → посмотри на ссылку (например, <b>А3</b>) → 
    найди клетку в таблице → проверь ответ → <b>зачеркни клетку</b>.
</div>

<table>
    <tr>
        <th>№</th>
        <th>Русский</th>
        <th>Клетка</th>
    </tr>
'''
    
    for i, (ru, en) in enumerate(pairs, 1):
        coord = task_coords[i]
        html += f'''
    <tr>
        <td class="task-num">{i}</td>
        <td class="task-ru">{ru}</td>
        <td class="task-ref">{coord}</td>
    </tr>
'''
    
    html += '''
</table>

<hr class="sep">

<h3 style="text-align:center;">ОТВЕТЫ (найди свою клетку)</h3>

<table class="grid-table">
'''
    
    # Строим таблицу клеток
    for r in range(rows):
        html += "<tr>"
        for c in range(cols):
            coord = f"{letters[c]}{r+1}"
            if coord in coord_answer:
                html += f'''
    <td>
        <div class="coord">{coord}</div>
        <div class="answer">{coord_answer[coord]}</div>
    </td>
'''
            else:
                html += f'''
    <td class="empty-cell">
        <div class="coord">{coord}</div>
        <div style="color:#ccc;">—</div>
    </td>
'''
        html += "</tr>\n"
    
    html += f'''
</table>

<p style="text-align:center; font-size:13px; color:#666; margin-top:20px;">
    Всего: {n} предложений. После проверки зачеркни клетку ✏️
</p>

</body>
</html>
'''
    return html

def main():
    input_file = "oop.txt"
    output_file = "trainer.html"
    cols = 5
    
    pairs = read_file(input_file)
    if not pairs:
        print("Ошибка: файл sentences.txt не найден или пуст.")
        print("Формат: русский;английский")
        return
    
    html = generate_html(pairs, cols)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Готово! Открой {output_file}")

if __name__ == "__main__":
    main()