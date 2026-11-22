import cv2
import customtkinter as ctk
from PIL import Image, ImageTk

# Настройка CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Глобальные переменные
cap = None
video_label = None
is_running = False


def update_frame():
    """Получает кадр из камеры, конвертирует и отображает."""
    global cap, video_label, is_running

    if not is_running:
        return

    ret, frame = cap.read()
    if ret:
        # Конвертируем BGR (OpenCV) в RGB (для PIL)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Конвертируем кадр в PIL Image
        img = Image.fromarray(frame_rgb)
        # Конвертируем в ImageTk для отображения в Tkinter
        imgtk = ImageTk.PhotoImage(image=img)

        # Обновляем изображение в CTkLabel
        video_label.configure(image=imgtk)
        video_label.image = imgtk  # Сохраняем ссылку, чтобы не удалил сборщик мусора

    # Планируем следующий вызов функции через 10 миллисекунд
    if is_running:
        video_label.after(10, update_frame)


def start_camera():
    """Запускает камеру и начинает показ видео."""
    global cap, video_label, is_running

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        video_label.configure(text="Ошибка: Камера не найдена")
        return

    is_running = True
    update_frame()


def stop_camera():
    """Останавливает показ видео и освобождает камеру."""
    global cap, is_running

    is_running = False

    if cap is not None and cap.isOpened():
        cap.release()
        cap = None

    video_label.configure(image="", text="Камера остановлена")


def on_closing():
    """Обработчик закрытия окна."""
    stop_camera()
    root.destroy()


# ========== СОЗДАНИЕ ИНТЕРФЕЙСА ==========
root = ctk.CTk()
root.title("Камера в CustomTkinter (без ООП)")
root.geometry("800x600")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Виджет для отображения видео
video_label = ctk.CTkLabel(root, text="Нажмите 'Запустить камеру'")
video_label.pack(padx=10, pady=10, fill="both", expand=True)

# Кнопки управления
button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

btn_start = ctk.CTkButton(button_frame, text="▶ Запустить камеру", command=start_camera)
btn_start.pack(side="left", padx=5)

btn_stop = ctk.CTkButton(button_frame, text="⏹ Остановить", command=stop_camera)
btn_stop.pack(side="left", padx=5)

# Запуск приложения
root.mainloop()