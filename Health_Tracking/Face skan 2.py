import cv2
import customtkinter as ctk
from PIL import Image, ImageTk

# Настройка CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Камера в CustomTkinter")
        self.geometry("800x600")

        # 1. Создаём виджет для отображения видео (CTkLabel)
        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack(padx=10, pady=10, fill="both", expand=True)

        # 2. Захват видео с камеры (0 - встроенная камера)
        self.cap = cv2.VideoCapture(0)

        # Проверка, открылась ли камера
        if not self.cap.isOpened():
            print("Ошибка: Не удалось открыть камеру")
            self.video_label.configure(text="Камера не найдена")
            return

        # 3. Запускаем обновление кадров
        self.update_frame()

    def update_frame(self):
        """Получает кадр из камеры, конвертирует и отображает."""
        ret, frame = self.cap.read()
        if ret:
            # Конвертируем BGR (OpenCV) в RGB (для PIL)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Конвертируем кадр в PIL Image
            img = Image.fromarray(frame_rgb)
            # Конвертируем в ImageTk для отображения в Tkinter
            imgtk = ImageTk.PhotoImage(image=img)

            # Обновляем изображение в CTkLabel
            self.video_label.configure(image=imgtk)
            self.video_label.image = imgtk  # Сохраняем ссылку, чтобы не удалил сборщик мусора

        # Планируем следующий вызов функции через 10 миллисекунд (≈ 100 FPS) [citation:1]
        self.after(10, self.update_frame)

    def __del__(self):
        # Освобождаем камеру при закрытии приложения
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

# Запуск приложения
if __name__ == "__main__":
    app = App()
    app.mainloop()