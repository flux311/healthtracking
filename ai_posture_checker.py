"""
Модуль «Здоровая осанка».
Одно окно OpenCV (латинское имя — иначе Windows создаёт два окна).
Весь русский текст рисуется на кадре через Pillow.
"""
import cv2
import os
import sys
import time
import threading
import subprocess
from collections import defaultdict

import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ВАЖНО: только ASCII в имени окна — иначе на Windows появляется 2 окна
WINDOW_NAME = "Zdorovaya Osanka"

# ---------- Модель ----------
_model = None
_model_ready = False
_model_error = None
_preload_started = False


def _load_model():
    global _model, _model_ready, _model_error
    try:
        from ultralytics import YOLO
        model_path = os.path.join("Health_Tracking", "models", "yolov8n-pose.pt")
        if os.path.exists(model_path):
            m = YOLO(model_path)
        else:
            m = YOLO("yolov8n-pose.pt")
        _model = m
        _model_ready = True
    except Exception as e:
        _model_error = str(e)
        _model_ready = False


def _ensure_preload():
    global _preload_started
    if not _preload_started:
        _preload_started = True
        threading.Thread(target=_load_model, daemon=True).start()


def _get_font(size=20):
    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def put_text_ru(frame, text, xy, font_size=20, color_bgr=(255, 255, 255)):
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    font = _get_font(font_size)
    color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])
    draw.text(xy, text, font=font, fill=color_rgb)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def put_lines_ru(frame, lines, xy, font_size=18, color_bgr=(220, 220, 220), line_h=24):
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    font = _get_font(font_size)
    color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])
    x, y = xy
    for i, line in enumerate(lines):
        draw.text((x, y + i * line_h), line, font=font, fill=color_rgb)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def check_posture(kp):
    person_kp = kp[0]
    nose = person_kp[0]
    l_shoulder = person_kp[5]
    r_shoulder = person_kp[6]

    if min(float(nose[2]), float(l_shoulder[2]), float(r_shoulder[2])) < 0.5:
        return "searching", "Поиск человека...", (200, 200, 200)

    shoulder_mid_y = (float(l_shoulder[1]) + float(r_shoulder[1])) / 2.0
    shoulder_width = abs(float(l_shoulder[0]) - float(r_shoulder[0]))

    if shoulder_width < 30:
        return "far", "Подойдите ближе", (200, 200, 200)

    head_drop = shoulder_mid_y - float(nose[1])
    is_slouching = head_drop < (shoulder_width * 0.4)
    is_asymmetric = abs(float(l_shoulder[1]) - float(r_shoulder[1])) > (shoulder_width * 0.15)

    if is_slouching and is_asymmetric:
        return "both", "Сутулость и перекос", (0, 0, 255)
    if is_slouching:
        return "slouch", "Выпрямите спину", (0, 0, 255)
    if is_asymmetric:
        return "lean", "Выровняйте плечи", (0, 255, 255)
    return "good", "Хорошая осанка", (0, 255, 0)


def _build_recommendations(stats, total_tracked, good_pct):
    recs = []
    if total_tracked < 30:
        recs.append("Сессия слишком короткая. Повторите проверку 1–2 минуты.")
        return recs

    if good_pct >= 80:
        recs.append("Отличный результат! Сохраняйте привычку держать спину ровно.")
        recs.append("Делайте короткие перерывы каждые 40–50 минут работы.")
    elif good_pct >= 50:
        recs.append("Осанка в целом приемлемая — следите за положением головы.")
        recs.append("Поставьте монитор на уровень глаз, не наклоняйте голову вперёд.")
    else:
        recs.append("Частая сутулость. Контроль: плечи назад, макушка вверх.")
        recs.append("Каждые 30 минут — минута упражнений: лопатки, повороты головы.")

    slouch = stats.get("slouch", 0) + stats.get("both", 0)
    lean = stats.get("lean", 0) + stats.get("both", 0)
    if total_tracked > 0:
        if slouch / total_tracked > 0.35:
            recs.append("Сутулость: подтяните подбородок, грудь вперёд, лопатки сведите.")
            recs.append("Упражнение: «кошка-корова» 10 раз или руки назад у стены.")
        if lean / total_tracked > 0.25:
            recs.append("Перекос плеч: проверьте высоту стола, не опирайтесь на один локоть.")
            recs.append("Упражнение: подъёмы плеч и наклоны в стороны по 8–10 раз.")
    if good_pct < 50:
        recs.append("При длительном дискомфорте в шее/спине обратитесь к врачу или ЛФК.")

    seen, unique = set(), []
    for r in recs:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    return unique[:5]


def _wrap_text(text, max_chars=48):
    if len(text) <= max_chars:
        return [text]
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _draw_stats_panel(frame, lines):
    if not lines:
        return frame
    pad, line_h = 10, 26
    box_w = 280
    box_h = pad * 2 + len(lines) * line_h
    x, y = 10, max(10, frame.shape[0] - box_h - 10)
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + box_w, y + box_h), (25, 25, 25), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    return put_lines_ru(
        frame, lines, (x + pad, y + pad),
        font_size=17, color_bgr=(230, 230, 230), line_h=line_h
    )


def _make_summary_frame(stats, session_sec, good_pct, recommendations, size=(720, 560)):
    w, h = size
    img = np.zeros((h, w, 3), dtype=np.uint8)
    img[:] = (36, 36, 40)

    img = put_text_ru(img, "Итоги проверки осанки", (30, 20), font_size=28, color_bgr=(255, 255, 255))

    stat_lines = [
        f"Длительность: {int(session_sec)} сек",
        f"Хорошая осанка: {good_pct:.0f}%",
        f"Кадров с сутулостью: {stats.get('slouch', 0) + stats.get('both', 0)}",
        f"Кадров с перекосом: {stats.get('lean', 0) + stats.get('both', 0)}",
        f"Кадров с хорошей осанкой: {stats.get('good', 0)}",
    ]
    pct_color = (100, 220, 100) if good_pct >= 60 else (80, 180, 255)
    y = 70
    for i, line in enumerate(stat_lines):
        col = pct_color if i == 1 else (210, 210, 210)
        img = put_text_ru(img, line, (30, y), font_size=20, color_bgr=col)
        y += 32

    y += 8
    cv2.line(img, (30, y), (w - 30, y), (80, 80, 80), 1)
    y += 16

    img = put_text_ru(img, "Рекомендации:", (30, y), font_size=22, color_bgr=(180, 220, 255))
    y += 36

    for rec in recommendations:
        for part in _wrap_text("• " + rec, max_chars=52):
            if y > h - 50:
                break
            img = put_text_ru(img, part, (30, y), font_size=17, color_bgr=(200, 220, 240))
            y += 26

    img = put_text_ru(
        img, "Нажмите любую клавишу, чтобы закрыть",
        (30, h - 35), font_size=16, color_bgr=(140, 140, 140)
    )
    return img


def run_camera():
    """Одно окно WINDOW_NAME на всю сессию."""
    _ensure_preload()

    if sys.platform == "win32":
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        err = np.zeros((240, 560, 3), dtype=np.uint8)
        err[:] = (30, 30, 35)
        err = put_text_ru(err, "Камера не найдена", (40, 70), font_size=26, color_bgr=(0, 0, 255))
        err = put_text_ru(err, "Подключите камеру и попробуйте снова", (40, 120), font_size=18, color_bgr=(200, 200, 200))
        err = put_text_ru(err, "Нажмите любую клавишу", (40, 170), font_size=16, color_bgr=(150, 150, 150))
        # Только imshow — без namedWindow заранее
        cv2.imshow(WINDOW_NAME, err)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    stats = defaultdict(int)
    session_start = time.time()
    window_created = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)

        if _model_error:
            frame = put_text_ru(frame, "Ошибка загрузки модели", (20, 20), 22, (0, 0, 255))
            frame = put_text_ru(frame, str(_model_error)[:55], (20, 55), 16, (0, 100, 255))
            frame = put_text_ru(frame, "Q — выход", (20, 90), 16, (180, 180, 180))
            cv2.imshow(WINDOW_NAME, frame)
            if not window_created:
                cv2.resizeWindow(WINDOW_NAME, 720, 560)
                window_created = True
            if cv2.waitKey(5) & 0xFF in (ord("q"), 27):
                break
            continue

        if not _model_ready:
            cv2.circle(frame, (30, 30), 10, (180, 180, 100), -1)
            frame = put_text_ru(frame, "Загрузка модели...", (50, 18), 22, (180, 180, 100))
            frame = put_text_ru(frame, "Q — выход", (50, 50), 16, (160, 160, 160))
            cv2.imshow(WINDOW_NAME, frame)
            if not window_created:
                cv2.resizeWindow(WINDOW_NAME, 720, 560)
                window_created = True
            if cv2.waitKey(5) & 0xFF in (ord("q"), 27):
                break
            continue

        results = _model(frame, verbose=False)
        status_key, status_text, color = "searching", "Поиск...", (200, 200, 200)

        for result in results:
            if result.keypoints is not None and len(result.keypoints) > 0:
                frame = result.plot()
                kp_array = result.keypoints.data.cpu().numpy()
                status_key, status_text, color = check_posture(kp_array)

        if status_key in ("good", "slouch", "lean", "both"):
            stats[status_key] += 1

        total_tracked = sum(stats[k] for k in ("good", "slouch", "lean", "both"))
        good_pct = (100.0 * stats["good"] / total_tracked) if total_tracked else 0.0
        elapsed = int(time.time() - session_start)

        cv2.circle(frame, (30, 30), 10, color, -1)
        frame = put_text_ru(frame, status_text, (50, 15), 22, color)

        tips = {
            "slouch": "Подсказка: поднимите голову, расправьте плечи",
            "lean": "Подсказка: выровняйте оба плеча",
            "both": "Подсказка: сядьте ровно, монитор на уровне глаз",
            "good": "Отлично, продолжайте!",
        }
        tip = tips.get(status_key, "")
        if tip:
            frame = put_text_ru(frame, tip, (50, 48), 16, (200, 220, 180))

        live = [
            f"Время: {elapsed} с",
            f"Хорошая осанка: {good_pct:.0f}%",
            f"Сутулость: {stats['slouch'] + stats['both']}",
            f"Перекос: {stats['lean'] + stats['both']}",
            "Q — выход и итоги",
        ]
        frame = _draw_stats_panel(frame, live)

        cv2.imshow(WINDOW_NAME, frame)
        if not window_created:
            cv2.resizeWindow(WINDOW_NAME, 720, 560)
            window_created = True

        key = cv2.waitKey(5) & 0xFF
        if key in (ord("q"), 27):
            break

    cap.release()

    total_tracked = sum(stats[k] for k in ("good", "slouch", "lean", "both"))
    session_sec = time.time() - session_start
    good_pct = (100.0 * stats["good"] / total_tracked) if total_tracked else 0.0
    recommendations = _build_recommendations(stats, total_tracked, good_pct)

    if total_tracked > 0 or session_sec > 2:
        summary = _make_summary_frame(stats, session_sec, good_pct, recommendations)
        cv2.imshow(WINDOW_NAME, summary)
        cv2.waitKey(0)

    cv2.destroyAllWindows()


def AI_posture_checker_opening(is_aftarisation=False, aftarisation_login=None):
    """Точка входа из main.py."""
    script = os.path.abspath(__file__)
    python = sys.executable
    try:
        kwargs = {"cwd": os.path.dirname(script) or "."}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        subprocess.Popen([python, script], **kwargs)
    except Exception:
        try:
            run_camera()
        except Exception:
            pass


if __name__ == "__main__":
    run_camera()
