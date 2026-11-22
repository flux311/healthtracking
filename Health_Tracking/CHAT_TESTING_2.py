import customtkinter as ctk

# Создаём окно
app = ctk.CTk()
app.geometry("400x300")

# 1. СОЗДАЁМ СКРОЛЛИРУЕМЫЙ ФРЕЙМ
scroll_frame = ctk.CTkScrollableFrame(app, width=350, height=200)
scroll_frame.pack(pady=10)

# 2. ДОБАВЛЯЕМ ВИДЖЕТЫ (они будут прокручиваться)
for i in range(30):
    label = ctk.CTkLabel(scroll_frame, text=f"Строка {i+1}")
    label.pack(pady=2)

# 3. ТЕКСТ С ПЕРЕНОСОМ (используем CTkTextbox)

text1 = "Очень длинный текст, который будет переноситься на следующую строку автоматически, потому что мы"
text_box = ctk.CTkTextbox(scroll_frame,wrap="word",height= len(text1)*0.75,font=("Arial", 12)) # ← ПЕРЕНОС ПО СЛОВАМ

text_box.pack(fill="both", pady=10, side = "right")
text_box.insert("1.0", text = text1)

# 4. АВТОПРОКРУТКА ВНИЗ (после добавления нового элемента)
scroll_frame._parent_canvas.yview_moveto(1.0)

app.mainloop()