#!/usr/bin/env python3
"""
Веб-сервер для отслеживания пальца через камеру.
Рисование: направьте палец в сторону камеры (указательный вперёд).
Запуск: python finger_tracker_server.py
"""
import os
import numpy as np
import cv2
from flask import Flask, Response, render_template_string
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    HandLandmarker,
    HandLandmarkerOptions,
    HandLandmarksConnections,
    RunningMode,
)
from mediapipe.tasks.python.vision import drawing_utils as mp_draw
from mediapipe.tasks.python.vision.core import image as mp_image

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_SCRIPT_DIR, "hand_landmarker.task")
FINGER_TIP = 8  # указательный
# Палец направлен к камере: кончик ближе к камере, чем запястье (z кончика > z запястья + порог)
Z_POINTING_OFFSET = 0.02  # насколько кончик должен быть "впереди" запястья

app = Flask(__name__)

_cap = None
_landmarker = None
# Холст для рисования (создаётся при первом кадре)
_drawing_canvas = None
_prev_point = None
_frame_size = None


def get_camera():
    global _cap
    if _cap is None:
        _cap = cv2.VideoCapture(0)
    return _cap


def get_landmarker():
    global _landmarker
    if _landmarker is None and os.path.exists(MODEL_PATH):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        _landmarker = HandLandmarker.create_from_options(options)
    return _landmarker


def _error_frame(msg: str) -> bytes:
    """Создать JPEG-кадр с сообщением об ошибке."""
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = (40, 40, 60)
    cv2.putText(img, msg, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
    cv2.putText(img, "Check: System Settings > Privacy > Camera", (50, 290),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
    _, jpg = cv2.imencode(".jpg", img)
    return jpg.tobytes()


def generate_frames():
    global _drawing_canvas, _prev_point, _frame_size

    # Сразу отправить кадр "загрузка", чтобы браузер не показывал alt
    loading = _error_frame("Loading camera...")
    yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + loading

    try:
        cap = get_camera()
    except Exception as e:
        err = _error_frame(f"Camera error: {e}")
        while True:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + err
        return

    if not cap.isOpened():
        err = _error_frame("Camera not available. Grant camera access to Terminal/Cursor in System Settings > Privacy > Camera.")
        while True:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + err
        return

    lm = get_landmarker()
    frame_idx = 0

    if lm is None:
        err = _error_frame("Model hand_landmarker.task not found in project folder.")
        while True:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + err
        return

    while True:
        try:
            ret, frame = cap.read()
        except Exception:
            ret = False
        if not ret:
            err = _error_frame("Camera disconnected")
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + err
            continue
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        if _frame_size != (w, h):
            _frame_size = (w, h)
            _drawing_canvas = np.zeros((h, w, 3), dtype=np.uint8)
            _drawing_canvas[:] = 255  # белый фон
            _prev_point = None

        rgb = np.ascontiguousarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image = mp_image.Image(image_format=mp_image.ImageFormat.SRGB, data=rgb)
        timestamp_ms = int(frame_idx * 1000 / 30)
        result = lm.detect_for_video(image, timestamp_ms)

        is_pointing = False
        x, y = 0, 0

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                try:
                    mp_draw.draw_landmarks(
                        frame, hand_landmarks, HandLandmarksConnections.HAND_CONNECTIONS,
                        mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1),
                        mp_draw.DrawingSpec(color=(255, 255, 255), thickness=1),
                    )
                except Exception:
                    pass  # скелет руки — опционально
                tip = hand_landmarks[FINGER_TIP]
                wrist = hand_landmarks[0]
                x = int(tip.x * w)
                y = int(tip.y * h)
                tip_z = tip.z if tip.z is not None else 0
                wrist_z = wrist.z if wrist.z is not None else 0
                is_pointing = tip_z > wrist_z + Z_POINTING_OFFSET

                if is_pointing:
                    cv2.circle(frame, (x, y), 12, (0, 255, 0), -1)  # зелёный = рисуем
                    if _prev_point is not None:
                        cv2.line(_drawing_canvas, _prev_point, (x, y), (0, 0, 0), 4)
                    _prev_point = (x, y)
                else:
                    cv2.circle(frame, (x, y), 12, (0, 255, 255), -1)  # жёлтый = не рисуем
                    _prev_point = None

                cv2.putText(frame, f"({x},{y}) {'РИСУЕМ' if is_pointing else ''}", (x + 15, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        else:
            _prev_point = None

        # Наложение рисунка на кадр (чёрные линии поверх видео)
        mask = np.any(_drawing_canvas != 255, axis=2)
        frame[mask] = _drawing_canvas[mask]

        _, jpg = cv2.imencode(".jpg", frame)
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes()
        frame_idx += 1


HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Отслеживание пальца</title>
  <style>
    body { margin: 0; background: #1a1a2e; color: #eee; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 20px; }
    h1 { margin-bottom: 10px; }
    img { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
    p { color: #aaa; font-size: 14px; }
  </style>
</head>
<body>
  <h1>Рисование пальцем</h1>
  <p>Жёлтая точка — палец виден. <b>Направьте палец в камеру</b> — точка станет зелёной, начнётся рисование.</p>
  <p><a href="/clear" style="color:#4fc3f7;">Очистить холст</a> | <a href="/raw_feed" style="color:#4fc3f7;">Только камера</a> (если видео не идёт)</p>
  <p style="font-size:12px;color:#666;">Нет видео? Запустите сервер из Terminal (не Cursor), дайте доступ к камере в Системные настройки → Конфиденциальность.</p>
  <img src="/video_feed" alt="Video" style="max-height: 80vh;">
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/raw_feed")
def raw_feed():
    """Поток только с камеры (без MediaPipe) — для проверки доступа к камере."""
    def gen():
        cap = get_camera()
        if not cap.isOpened():
            err = _error_frame("Camera not available")
            while True:
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + err
            return
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            cv2.putText(frame, "Raw camera OK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            _, jpg = cv2.imencode(".jpg", frame)
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg.tobytes()
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/test")
def test_image():
    """Проверка: возвращает тестовое изображение."""
    img = np.zeros((100, 400, 3), dtype=np.uint8)
    img[:] = (60, 60, 80)
    cv2.putText(img, "Server OK", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    _, jpg = cv2.imencode(".jpg", img)
    return Response(jpg.tobytes(), mimetype="image/jpeg")


@app.route("/clear")
def clear_canvas():
    global _drawing_canvas, _frame_size
    if _drawing_canvas is not None:
        _drawing_canvas[:] = 255
    return """<script>window.location='/';</script>Очищено. <a href="/">Назад</a>"""


@app.route("/video_feed")
def video_feed():
    def safe_gen():
        try:
            for chunk in generate_frames():
                yield chunk
        except Exception as e:
            import traceback
            print("video_feed error:", traceback.format_exc(), flush=True)
            try:
                err = _error_frame(str(e)[:60])
            except Exception:
                err = b""
            if err:
                while True:
                    yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + err
    return Response(
        safe_gen(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/debug")
def debug():
    """Проверка компонентов."""
    lines = []
    try:
        cap = get_camera()
        lines.append(f"Camera opened: {cap.isOpened()}")
        if cap.isOpened():
            ret, f = cap.read()
            lines.append(f"Frame read: {ret}, shape: {f.shape if ret else 'N/A'}")
    except Exception as e:
        lines.append(f"Camera error: {e}")
    lines.append(f"Model exists: {os.path.exists(MODEL_PATH)}")
    try:
        lm = get_landmarker()
        lines.append(f"Landmarker: {lm is not None}")
    except Exception as e:
        lines.append(f"Landmarker error: {e}")
    return "<br>".join(lines)


if __name__ == "__main__":
    os.chdir(_SCRIPT_DIR)  # работа из папки проекта
    port = 5001
    print(f"Запуск сервера: http://localhost:{port}")
    print(f"Отладка: http://localhost:{port}/debug")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
