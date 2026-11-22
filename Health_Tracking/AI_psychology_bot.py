import threading
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from tkinter import PhotoImage
import openai
from openai import OpenAI
from customtkinter import*
import thread
import speech_recognition as sr
import pyaudio
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
from fer.fer import FER
import torch
import sounddevice as sd
import database

def AI_psychology_bot_opening(is_aftarisation, aftarisation_login):
    device = torch.device("cpu")
    text_to_voice_model, example_text = torch.hub.load(repo_or_dir = "snakers4/silero-models", model = "silero_tts", language = "ru", speaker = "v3_1_ru")

    global emotion_rander
    emotion_rander = "нет информации"

    global open_camera
    open_camera = False

    is_running_camera = False

    emotions_detect = FER()

    client = OpenAI(base_url = "https://api.llm7.io/v1", api_key=os.environ.get("LLM7_API_KEY"))
    chat_history = [{"role":"system", "content":"Ты - психолог. Твоя задача общаться с собеседником, поддерживать разговор, помогать ему морально и копировать манеру общения. В конце каждого запроса будет информация о эмоциональном состоянии собеседника, полученом из анализа камеры пользователя(Эмоциональное состояние: **название эмоционального состояния**).В случае отсутствия информации о состоянии человека(например он выключил камеру) на месте эмоции будет надпись **нет информации**. Вот перечень всех эмоций: neutral - спокойный, sad - грустный, angry - злой, disgust - испытывающий отвращение, fear - напуганный, happy - весёлый, surprise - удивлённый"}]

    recognition = sr.Recognizer()
    recognition.pause_threshold = 0.8
    recognition.energy_threshold = 300

    main_root = CTkToplevel()
    main_root.geometry("1050x600")
    main_root.title("ИИ Психолог")
    set_appearance_mode("Dark")

    speak_button_image = PhotoImage(file="Speak button.png")
    restangle_image = PhotoImage(file="HT restangle psihology bot.png")

    offed_camera_image = PhotoImage(file = "frame camera off.png")

    main_canvas = CTkCanvas(main_root, width = 1050, height = 600, bg = "#242424")
    main_canvas.place(relx = .5, rely = .5, anchor = CENTER)


    chat_bg_frame = CTkScrollableFrame(main_canvas, width = 500, height = 520, corner_radius = 20, fg_color = "#3c3c3c")
    chat_bg_frame.place(relx = .27, rely = .495, anchor = CENTER)

    #camera_bg_frame = CTkFrame(main_canvas, width = 460, height = 300, corner_radius = 20, fg_color = "#bababa")
    #camera_bg_frame.place(relx = .76, rely = .285, anchor = CENTER)

    main_canvas.create_image(800, 173, image=offed_camera_image)

    main_canvas.create_image(798, 519, image = restangle_image)

    speaking_button = main_canvas.create_image(798, 440, image = speak_button_image)

    def speaking_with_bot():
        global emotion_rander
        swb_text = ""
        with sr.Microphone() as sound:
            recognition.adjust_for_ambient_noise(sound, duration = 0.5)
            try:
                audio = recognition.listen(sound, timeout = 3)
                swb_text = recognition.recognize_google(audio, language = "ru-RU")

            except sr.RequestError:
                swb_text = "Ошибка чтения"
            except sr.WaitTimeoutError:
                swb_text = "Ошибка чтения"
            except sr.UnknownValueError:
                swb_text = "Ошибка чтения"

        if swb_text != "Ошибка чтения":
            print(f"Информация собрана: {swb_text}")

            chat_history.append({"role":"user", "content": f"{swb_text} ЭМОЦИОНАЛЬНОЕ СОСТОЯНИЕ: {emotion_rander}"})

            swb_response = client.chat.completions.create(model = "fast", temperature = 0.7, messages = chat_history, max_tokens = 1000)

            swb_response_text = swb_response.choices[0].message.content

            chat_history.append({"role":"assistant", "content": swb_response_text})

            print(swb_response_text)

            text_to_voice_audio = text_to_voice_model.apply_tts(text = swb_response_text, speaker = "aidar", sample_rate = 48000)
            sd.play(text_to_voice_audio.numpy(), 48000)

    def speaking_with_bot_thread():
        global emotion_rander
        thread3 = threading.Thread(target=speaking_with_bot)
        thread3.daemon = True
        thread3.start()


    main_canvas.tag_bind(speaking_button, "<Button-1>", lambda event: speaking_with_bot_thread())

    input_text_box = CTkTextbox(main_canvas, wrap = "word", height = 65, width = 390, fg_color = "#3c3c3c", bg_color = "#3c3c3c")
    input_text_box.place(relx = .735, rely = .88, anchor = CENTER)

    def opening_camera():
        global frame_counter
        global cap
        global camera_label
        global emotion_rander
        global open_camera
        frame_counter = 0

        if not open_camera:
            open_camera = True

            frame_counter = 0

            camera_label = CTkLabel(main_canvas, text="")
            camera_label.place(relx=.76, rely=.285, anchor=CENTER)


            cap = cv2.VideoCapture(0)

            is_running_camera = True


            def frame_update():
                global open_camera
                global emotion_rander
                global frame_counter
                if not is_running_camera:
                    return

                ret, frame = cap.read()

                frame = cv2.resize(frame,(415,285), interpolation=cv2.INTER_AREA)

                if not ret:
                    return

                else:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

                    frame_counter += 1

                    if frame_counter % 5 == 0:
                        try:
                            emotion = emotions_detect.detect_emotions(frame)

                            emotion_dict = emotion[0]['emotions']
                            emotion_rander = max(emotion_dict, key=emotion_dict.get)

                        except Exception as e:
                            pass

                    streaming_image = Image.fromarray(rgb_frame)

                    tk_streaming_image = ImageTk.PhotoImage(streaming_image)

                    camera_label.configure(image = tk_streaming_image)
                    camera_label.image = tk_streaming_image

                    if is_running_camera:
                        camera_label.after(10, frame_update)

            frame_update()

    def camera_off():
        global open_camera
        global emotion_rander
        is_running_camera = False
        open_camera = False
        camera_label.destroy()
        emotion_rander = "нет информации"
        cap.release()

    def sending_message():
        global emotion_rander
        sending_text = input_text_box.get("1.0", "end")

        if len(sending_text) <= 25:
            user_message_height_count = 0.8

        else:
            user_message_height_count = 0.75

        chat_history.append({"role":"user", "content":f"{sending_text} ЭМОЦИОНАЛЬНОЕ СОСТОЯНИЕ: {emotion_rander}"})
        print(emotion_rander)

        user_message_text_box = CTkTextbox(chat_bg_frame, wrap = "word", height = len(sending_text)*user_message_height_count)
        user_message_text_box.insert("1.0", f"{sending_text}")
        user_message_text_box.pack(side = "top", pady = 10, anchor = "e")

        input_text_box.delete("1.0", "end")

        response = client.chat.completions.create(model = "fast", temperature = 0.7, max_tokens = 1000, messages = chat_history)

        bot_response_text = response.choices[0].message.content

        chat_history.append({"role":"assistant", "content":f"{bot_response_text}"})

        bot_message_text_box = CTkTextbox(chat_bg_frame, wrap = "word", height = len(bot_response_text)*0.75)
        bot_message_text_box.insert("1.0", f"{bot_response_text}")
        bot_message_text_box.pack(pady = 10, side = "top", anchor = "w")

    def sanding_message_thread():
        thread1 = threading.Thread(target = sending_message)
        thread1.daemon = True
        thread1.start()

    def voice_text_input():
        with sr.Microphone() as sound:
            recognition.adjust_for_ambient_noise(sound, duration = 0.5)
            try:
                audio = recognition.listen(sound, timeout = 3)
                text = recognition.recognize_google(audio, language = "ru-RU")
            except sr.WaitTimeoutError:
                text = ""
                text = "Ошибка WaitTimeoutError"
            except sr.RequestError:
                text = ""
                text = "Ошибка RequestError"
            except sr.UnknownValueError:
                text = ""
                text = "Ошибка UnknownValueError"
        main_root.after(0, lambda: text_uploading(text))

    def text_uploading(text):
        input_text_box.insert("end", f"{text}")
        print(text)
        voice_input_button.configure(fg_color="#1f6aa5")


    def voice_text_input_thread():
        voice_input_button.configure(fg_color = "green")
        thread2 = threading.Thread(target = voice_text_input)
        thread2.daemon = True
        thread2.start()

    send_button = CTkButton(main_canvas, text="⯈", width=10, corner_radius=10, bg_color="#3c3c3c", command = sanding_message_thread)
    send_button.place(relx=.95, rely=.85, anchor=CENTER)

    voice_input_button = CTkButton(main_canvas, text="🎤", width=10, corner_radius=10, bg_color="#3c3c3c", command = voice_text_input_thread)
    voice_input_button.place(relx=.95, rely=.915, anchor=CENTER)

    camera_on_button = CTkButton(main_canvas, text = "Вкл.", width = 70, corner_radius=10, command = opening_camera)
    camera_on_button.place(relx = .85, rely = .575, anchor = CENTER)

    camera_on_button = CTkButton(main_canvas, text="Выкл.", width=70, corner_radius=10, command = camera_off)
    camera_on_button.place(relx=.928, rely=.575, anchor=CENTER)

    main_canvas.lift(speaking_button)

    def on_closing_add_history():
        if len(chat_history) >= 2 and is_aftarisation == True:
            chat_history.append({"role":"system", "content":"Сейчас ты это программа системного отчёта. Твоя задача проанализировать весь диалог и выдать краткую информацию-вывод из всего диалога."})
            add_history_response = client.chat.completions.create(model = "fast", max_tokens = 1000, temperature = 0.7, messages = chat_history)
            add_history_message = add_history_response.choices[0].message.content
            print(add_history_message)
            database.insert_info_to_history(aftarisation_login, add_history_message, "ИИ Психолог")
        main_root.destroy()

    main_root.protocol("WM_DELETE_WINDOW", on_closing_add_history)

    main_root.mainloop()

#AI_psychology_bot_opening()