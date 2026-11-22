import customtkinter as ctk

app = ctk.CTk()
app.geometry("400x300")

# Создаём скроллируемый фрейм
scrollable_frame = ctk.CTkScrollableFrame(
    master=app,
    width=300,
    height=200,
    border_width=2,
    fg_color="lightgrey"
)
scrollable_frame.pack(padx=20, pady=20)

# Добавляем виджеты внутрь — они будут прокручиваться
for i in range(20):
    label = ctk.CTkLabel(master=scrollable_frame, text=f"Сообщение {i+1}")
    label.pack(pady=5, padx=10)

app.mainloop()