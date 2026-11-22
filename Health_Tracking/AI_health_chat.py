import threading
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from openai import OpenAI
from customtkinter import*
import thread
import speech_recognition as sr
import pyaudio
import database
import torch
import sounddevice as sd


def AI_chat_bot_opening(is_aftarisation, aftarisation_login):
    device = torch.device("cpu")
    text_to_voice_model, example_text = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_tts",language="ru", speaker="v3_1_ru")
    client = OpenAI(base_url = "https://api.llm7.io/v1", api_key=os.environ.get("LLM7_API_KEY"))
    chat_history = [{"role":"system", "content":"Ты — медицинский помощник. Не ставишь диагнозы, но даёшь рекомендации исходя из запроса"}]

    recognition = sr.Recognizer()
    recognition.pause_threshold = 2

    main_root = CTk()
    main_root.geometry("500x700")
    main_root.title("ИИ Ассистент Здоровья")
    set_appearance_mode("Dark")

    def sanding_message():
        sanded_message = text_input_box.get("1.0", "end")
        chat_history.append({"role":"user", "content": sanded_message})

        if len(sanded_message) <= 25:
            user_message_height_count = 0.8

        else:
            user_message_height_count = 0.75

        user_message_text_box = CTkTextbox(chat_frame, wrap = "word", font = ("Arial", 12), height = len(sanded_message)* user_message_height_count)
        user_message_text_box.pack(pady=10, side = "top", anchor = "e")
        user_message_text_box.insert("1.0", sanded_message)

        text_input_box.delete("1.0", "end")

        response = client.chat.completions.create(model = "fast", messages=chat_history, temperature = 0.7, max_tokens = 1000)

        bot_response = response.choices[0].message.content

        chat_history.append({"role": "assistant", "content": bot_response})

        bot_message_text_box = CTkTextbox(chat_frame, wrap = "word", font = ("Arial", 12), height = len(bot_response)*0.75)
        bot_message_text_box.pack(side = "top", anchor = "w", pady = 10)
        bot_message_text_box.insert("1.0", bot_response)

    def sanding_message_thread():
        thread = threading.Thread(target = sanding_message)
        thread.daemon = True
        thread.start()

    def voice_info_input():
        with sr.Microphone() as sound:
            recognition.adjust_for_ambient_noise(sound, duration = 0.5)
            try:
                audio = recognition.listen(sound, timeout = 3)
                text = recognition.recognize_google(audio, language = "ru-RU").lower()

            except sr.WaitTimeoutError:
                text = ""
                text = "Ошибка"
            except sr.UnknownValueError:
                text = ""
                text = "Ошибка"
            except sr.RequestError:
                text = ""
                text = "Ошибка"

        text_input_box.insert("end", f" {text}")
        speak_button.configure(fg_color="#1f6aa5")

    def voice_info_input_thread():
        thread2 = threading.Thread(target = voice_info_input)
        thread2.daemon = True
        thread2.start()
        speak_button.configure(fg_color = "green")

    def dialog():
        print("ГОВОРИТЕ!")
        with sr.Microphone() as dialog_sound:
            recognition.adjust_for_ambient_noise(dialog_sound, duration=0.5)
            try:
                dialog_audio = recognition.listen(dialog_sound, timeout = 3)
                print("ИНФОРМАЦИЯ СОБРАНА")
                dialog_text = recognition.recognize_google(dialog_audio, language = "ru-RU")
            except sr.RequestError:
                print("Ошибка RequestError")
                dialog_text = ""
            except sr.WaitTimeoutError:
                print("Ошибка WaitTimeoutError")
                dialog_text = ""
            except sr.UnknownValueError:
                print("Ошибка UnknownValueError")
                dialog_text = ""

        print(f"ВЫ СКАЗАЛИ: {dialog_text}")

        chat_history.append({"role":"user", "content": dialog_text})
        dialog_response = client.chat.completions.create(model = "fast", temperature = 0.7, max_tokens = 350, messages = chat_history)

        dialog_AI_message = dialog_response.choices[0].message.content
        print(f"ОТВЕТ НЕЙРОНКИ:{dialog_text}")

        dialog_text_to_voice = text_to_voice_model.apply_tts(text = dialog_AI_message, speaker = "aidar", sample_rate = 48000)
        sd.play(dialog_text_to_voice.numpy(), 48000)

        chat_history.append({"role": "assistant", "content": dialog_AI_message})

    def dialog_thread():
        dialog_thread = threading.Thread(target = dialog)
        dialog_thread.daemon = True
        dialog_thread.start()

    text_frame = CTkFrame(main_root, width = 470, height = 100, fg_color = "#1d1e1e")
    text_frame.place(relx = .5, rely = .9, anchor = CENTER)

    text_input_box = CTkTextbox(main_root, wrap = "word", height = 75, width = 360, fg_color = "#1d1e1e", bg_color = "#1d1e1e")
    text_input_box.place(relx = .41, rely = .89, anchor = CENTER)

    send_button = CTkButton(main_root, text = "⯈",width = 10, corner_radius = 10, bg_color = "#1d1e1e", command = sanding_message_thread)
    send_button.place(relx = .91, rely = .87, anchor = CENTER)

    speak_button = CTkButton(main_root, text = "🎤",width = 10, corner_radius = 10, bg_color = "#1d1e1e", command = voice_info_input_thread)
    speak_button.place(relx = .82, rely = .87, anchor = CENTER)

    dialog_button = CTkButton(main_root, text = "📞", width = 80, bg_color = "#1d1e1e", command = dialog_thread)
    dialog_button.place(relx = .8625, rely = .93, anchor = CENTER)

    chat_frame = CTkScrollableFrame(main_root, width = 440, height = 530, corner_radius = 10)
    chat_frame.place(relx = .5, rely  = .41, anchor = CENTER)

    def on_closing_add_history():
        if len(chat_history) >= 2 and is_aftarisation == True:
            chat_history.append({"role":"system", "content":"Сейчас ты это программа системного отчёта. Твоя задача проанализировать весь диалог и выдать краткую информацию-вывод из всего диалога."})
            add_history_response = client.chat.completions.create(model = "fast", max_tokens = 1000, temperature = 0.7, messages = chat_history)
            add_history_message = add_history_response.choices[0].message.content
            print(add_history_message)
            database.insert_info_to_history(aftarisation_login, add_history_message, "ИИ Ассистент Здоровья")
        main_root.destroy()

    main_root.protocol("WM_DELETE_WINDOW", on_closing_add_history)

    main_root.mainloop()

#AI_chat_bot_opening()