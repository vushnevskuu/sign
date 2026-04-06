# Отслеживание пальца через камеру

Программа отслеживает один палец на руке через веб-камеру (MediaPipe Hands).

## Запуск

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements-python.txt
python finger_tracker.py
```

## Управление

- **Q** — выход
- **C** — очистить холст (десктоп)
- Покажите руку — жёлтая точка на кончике указательного пальца
- **Направьте палец в камеру** — точка станет зелёной, начнётся рисование

## Аргументы командной строки

| Параметр | Описание |
|----------|----------|
| `-f`, `--finger` | Палец: 4, 8, 12, 16, 20 (по умолчанию 8 — указательный) |
| `-s`, `--smooth` | Сглаживание: N кадров (по умолчанию 5, 0 = выкл) |
| `-r`, `--record` | Запись траектории в файл (x,y по строкам) |
| `-c`, `--camera` | Индекс камеры (по умолчанию 0) |

## Примеры

```bash
# Указательный палец, сглаживание 10 кадров
python finger_tracker.py -f 8 -s 10

# Средний палец, запись траектории
python finger_tracker.py -f 12 -r trajectory.csv

# Без сглаживания
python finger_tracker.py -s 0
```

## Веб-версия (рекомендуется)

**Камера в браузере** — не нужен доступ сервера к камере:

```bash
python serve.py
```

Откройте http://localhost:8765. Разрешите доступ к камере. Направьте палец в камеру — начнётся рисование.

---

Альтернатива (камера на сервере, может не работать):

```bash
python finger_tracker_server.py
```

## Модель MediaPipe

Файл `hand_landmarker.task` должен лежать рядом со скриптом. Если его нет:

```bash
curl -sL "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task" -o hand_landmarker.task
```
