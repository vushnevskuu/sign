#!/usr/bin/env python3
"""
Отслеживание одного пальца через камеру.
План: Camera → Frame → RGB → MediaPipe → Landmarks → Tip → Draw → Display
"""
import argparse
import collections
import os
import numpy as np
import cv2
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    HandLandmarker,
    HandLandmarkerOptions,
    HandLandmarksConnections,
    RunningMode,
)
from mediapipe.tasks.python.vision import drawing_utils as mp_draw
from mediapipe.tasks.python.vision.core import image as mp_image

# MediaPipe HandLandmark: 4=THUMB_TIP, 8=INDEX_FINGER_TIP, 12=MIDDLE_FINGER_TIP, 16=RING_FINGER_TIP, 20=PINKY_TIP
FINGER_NAMES = {4: "большой", 8: "указательный", 12: "средний", 16: "безымянный", 20: "мизинец"}
# Палец направлен к камере: кончик впереди запястья (z кончика > z запястья + порог)
Z_POINTING_OFFSET = 0.02

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")


def smooth_point(history: collections.deque, x: float, y: float, z: float = 0) -> tuple:
    """Скользящее среднее по последним N кадрам."""
    history.append((x, y, z))
    sx = sum(p[0] for p in history) / len(history)
    sy = sum(p[1] for p in history) / len(history)
    sz = sum(p[2] for p in history) / len(history)
    return sx, sy, sz


def main():
    parser = argparse.ArgumentParser(description="Отслеживание пальца через камеру")
    parser.add_argument(
        "-f", "--finger",
        type=int,
        default=8,
        choices=[4, 8, 12, 16, 20],
        help="Палец: 4=большой, 8=указательный, 12=средний, 16=безымянный, 20=мизинец",
    )
    parser.add_argument(
        "-s", "--smooth",
        type=int,
        default=5,
        metavar="N",
        help="Сглаживание: скользящее среднее по N кадрам (0=выкл)",
    )
    parser.add_argument(
        "-r", "--record",
        metavar="FILE",
        help="Запись траектории в файл (x,y по строкам)",
    )
    parser.add_argument(
        "-c", "--camera",
        type=int,
        default=0,
        help="Индекс камеры",
    )
    args = parser.parse_args()

    if not os.path.exists(MODEL_PATH):
        print(f"Модель не найдена: {MODEL_PATH}")
        print("Скачайте: curl -sL https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -o hand_landmarker.task")
        return

    finger_tip = args.finger
    smooth_n = max(0, args.smooth)
    history = collections.deque(maxlen=smooth_n) if smooth_n else None
    traj_file = open(args.record, "w") if args.record else None

    def on_tip(x: int, y: int, z: float):
        if traj_file:
            traj_file.write(f"{x},{y}\n")
            traj_file.flush()

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("Не удалось открыть камеру")
        return

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    drawing_canvas = None
    prev_point = None

    with HandLandmarker.create_from_options(options) as landmarker:
        print("Камера запущена. Q — выход. C — очистить. Направьте палец в камеру — рисование.")
        print(f"Отслеживается: {FINGER_NAMES.get(finger_tip, finger_tip)} (landmark {finger_tip})")
        if smooth_n:
            print(f"Сглаживание: {smooth_n} кадров")
        if traj_file:
            print(f"Запись траектории: {args.record}")

        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            if drawing_canvas is None or drawing_canvas.shape[:2] != (h, w):
                drawing_canvas = np.ones((h, w, 3), dtype=np.uint8) * 255
                prev_point = None

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp_image.Image(image_format=mp_image.ImageFormat.SRGB, data=rgb)

            timestamp_ms = int(frame_idx * 1000 / 30)
            result = landmarker.detect_for_video(image, timestamp_ms)

            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        HandLandmarksConnections.HAND_CONNECTIONS,
                        mp_draw.DrawingSpec(color=(0, 255, 0), thickness=1),
                        mp_draw.DrawingSpec(color=(255, 255, 255), thickness=1),
                    )
                    tip = hand_landmarks[finger_tip]
                    wrist = hand_landmarks[0]
                    x_norm, y_norm, z = tip.x, tip.y, tip.z or 0
                    wrist_z = wrist.z if wrist.z is not None else 0
                    is_pointing = z > wrist_z + Z_POINTING_OFFSET

                    if history is not None:
                        x_norm, y_norm, z = smooth_point(history, x_norm, y_norm, z)

                    x = int(x_norm * w)
                    y = int(y_norm * h)

                    on_tip(x, y, z)

                    if is_pointing:
                        cv2.circle(frame, (x, y), 12, (0, 255, 0), -1)
                        if prev_point is not None:
                            cv2.line(drawing_canvas, prev_point, (x, y), (0, 0, 0), 4)
                        prev_point = (x, y)
                    else:
                        cv2.circle(frame, (x, y), 12, (0, 255, 255), -1)
                        prev_point = None

                    cv2.putText(
                        frame, f"({x},{y}) {'РИСУЕМ' if is_pointing else ''}", (x + 15, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                    )
            else:
                if history:
                    history.clear()
                prev_point = None

            mask = np.any(drawing_canvas != 255, axis=2)
            frame[mask] = drawing_canvas[mask]

            cv2.imshow("Finger Tracker", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("c"):
                drawing_canvas[:] = 255
                prev_point = None
            frame_idx += 1

    if traj_file:
        traj_file.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
