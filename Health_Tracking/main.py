from tkinter import PhotoImage
from anyio import move_on_after
from customtkinter import*
import ai_psychology_bot
import database
from CTkMessagebox import CTkMessagebox
import ai_health_chat
import ai_posture_checker
import json
from docxtpl import DocxTemplate
from tkinter import filedialog

set_default_color_theme("blue")
set_appearance_mode("Dark")

main_root = CTk()
main_root.geometry("1000x600")
main_root.title("Health Tracking")

profile_image = PhotoImage(file = "Profile avatar.png")
register_image = PhotoImage(file = "Register image.png")

is_aftarisation = False

aftarisation_login = None

is_login = False

AI_chat_bot_button_image = PhotoImage(file = "ИИ Асистент Здоровья.png")
AI_psihology_button_image = PhotoImage(file = "ИИ Психолог.png")
Health_osanka_button_image = PhotoImage(file = "Здоровая осанка.png")


def main_menu_create():
    global main_canvas
    global history_frame
    global history_filters
    main_canvas = CTkCanvas(main_root, width = 1000, height = 600, background = "#242424")
    main_canvas.place(relx = .5, rely = .5, anchor = CENTER)

    main_canvas.create_rectangle(-10,0,250,610, fill = "#3d3d3d", outline = "#3d3d3d")
    main_canvas.create_rectangle(250,0,1010,50, fill = "#3d3d3d", outline = "#3d3d3d")

    #history_founding = CTkEntry(main_canvas, fg_color = "#1f6aa5", bg_color = "#3d3d3d", border_color = "#1f6aa5", width = 190, placeholder_text = "Поиск...")
    #history_founding.place(relx = .11, rely = .045, anchor = CENTER)

    history_values = ["Все", "ИИ Ассистент Здоровья", "ИИ Психолог", "Здоровая осанка"]
    history_filters = CTkOptionMenu(main_canvas, fg_color = "#1f6aa5", bg_color = "#3d3d3d", width = 190, values = history_values)
    history_filters.place(relx = .11, rely = .045, anchor = CENTER)

    history_frame = CTkScrollableFrame(main_canvas,width = 220, height =520 ,fg_color = "#3d3d3d", bg_color = "#3d3d3d")
    history_frame.place(relx = .125, rely = .53, anchor = CENTER)

    #history_search_button = CTkButton(main_canvas, text = "🔍", width = 20, bg_color = "#3d3d3d")
    #history_search_button.place(relx = .225, rely = .045, anchor = CENTER)

    no_history_label = CTkLabel(main_canvas, text = "Историй не найдено", font = ("Arial", 15), bg_color = "#3d3d3d", text_color = "red")

    def history_upload():
        global history_filters
        global history_frame
        if not is_aftarisation:
            def no_history_label_destroy():
                no_history_label.place(relx=10, rely=.5, anchor=CENTER)

            no_history_label.place(relx = .33, rely = .045, anchor = CENTER)

            main_root.after(2000,no_history_label_destroy)
        else:
            history_frame.destroy()
            history_frame = CTkScrollableFrame(main_canvas, width=220, height=520, fg_color="#3d3d3d",bg_color="#3d3d3d")
            history_frame.place(relx=.125, rely=.53, anchor=CENTER)

            acc_history_info = database.get_acc_info(aftarisation_login)

            acc_module_massive = json.loads(acc_history_info[0])
            acc_info_massive = json.loads(acc_history_info[1])

            def show_history_info(module, info):
                global history_filters
                medcard_add_info_root = CTkToplevel()
                medcard_add_info_root.geometry("500x350")
                medcard_add_info_root.title(f"История Пользователя: {module}")

                medcard_add_info_textbox = CTkTextbox(medcard_add_info_root, width = 490, height = 300)
                medcard_add_info_textbox.place(relx = .5, rely = .45, anchor = CENTER)
                medcard_add_info_textbox.insert("1.0", text = info)

                def add_history_to_medcard():
                    database.insert_into_medcard(login = aftarisation_login, module = module, info =  medcard_add_info_textbox.get("1.0", "end"))
                    medcard_add_info_root.destroy()

                medcard_add_info_button = CTkButton(medcard_add_info_root, width = 490, text = "Добавить в Медицинскую карту", command = add_history_to_medcard)
                medcard_add_info_button.place(relx = .5, rely = .94, anchor = CENTER)

            for i in range(len(acc_module_massive)):
                if history_filters.get() != "Все":
                    if acc_module_massive[i] == history_filters.get():
                        history_button = CTkButton(history_frame, width = 250, height= 40, text = acc_module_massive[i], fg_color = "#43454a", command = lambda m_index = acc_module_massive[i], inf_index = acc_info_massive[i]: show_history_info(m_index, inf_index))
                        history_button.pack(side = "bottom", pady = 10)
                else:
                    history_button = CTkButton(history_frame, width=250, height=40, text=acc_module_massive[i], fg_color="#43454a", command=lambda m_index=acc_module_massive[i],inf_index=acc_info_massive[i]: show_history_info(m_index,inf_index))
                    history_button.pack(side="bottom", pady=10)

    upload_history_button = CTkButton(main_canvas, text = "🔍", width = 20, bg_color = "#3d3d3d", command = history_upload)
    upload_history_button.place(relx = .225, rely = .045, anchor = CENTER)

    def AI_chat_bot_open():
        ai_health_chat.AI_chat_bot_opening(is_aftarisation, aftarisation_login)

    def AI_psihology_bot_open():
        ai_psychology_bot.AI_psychology_bot_opening(is_aftarisation, aftarisation_login)

    def health_osanka_module_open():
        ai_posture_checker.AI_posture_checker_opening(is_aftarisation, aftarisation_login)


    AI_chat_button = main_canvas.create_image(620, 150, image = AI_chat_bot_button_image)
    main_canvas.tag_bind(AI_chat_button, "<Button-1>", lambda event: AI_chat_bot_open())

    AI_psihology_bot_button = main_canvas.create_image(620, 325, image = AI_psihology_button_image)
    main_canvas.tag_bind(AI_psihology_bot_button , "<Button-1>", lambda event: AI_psihology_bot_open())

    health_osanka_module_button = main_canvas.create_image(620, 505, image = Health_osanka_button_image)
    main_canvas.tag_bind(health_osanka_module_button, "<Button-1>", lambda  event: health_osanka_module_open())

    def program_info():
        global move_index
        prog_info_root = CTkToplevel()
        prog_info_root.geometry("1000x850")
        prog_info_root.title("Информация о программе")

        global program_info_image_1
        global program_info_image_2
        global program_info_image_3

        program_info_image_1 = PhotoImage(file="HT program info 1.png")
        program_info_image_2 = PhotoImage(file="HT program info 2.png")
        program_info_image_3 = PhotoImage(file="HT program info 3.png")

        global program_info_image_massive
        program_info_image_massive = [program_info_image_1, program_info_image_2, program_info_image_3]

        prog_info_canvas = CTkCanvas(prog_info_root, width = 1000, height = 850, background = "#242424")
        prog_info_canvas.place(relx = .5, rely = .5, anchor = CENTER)

        global prog_info_image
        prog_info_image = prog_info_canvas.create_image(502, 395, image = program_info_image_1)

        move_index = 0
        def prog_info_move(button_index):
            global program_info_image_1
            global program_info_image_2
            global program_info_image_3
            global move_index
            global program_info_image_massive
            global prog_info_image


            if button_index == 1:
                move_index += 1
                if move_index <= 2:
                    prog_info_image = prog_info_canvas.create_image(502, 395, image=program_info_image_massive[move_index])
                else:
                    move_index = 2
                    prog_info_image = prog_info_canvas.create_image(502, 395,image=program_info_image_massive[move_index])

            elif button_index == 0:
                move_index -= 1
                if move_index >= 0:
                    prog_info_image = prog_info_canvas.create_image(502, 395, image=program_info_image_massive[move_index])
                else:
                    move_index = 0
                    prog_info_image = prog_info_canvas.create_image(502, 395,image=program_info_image_massive[move_index])

        prog_info_move_button = CTkButton(prog_info_root, text = "Дальше", bg_color = "#242424", width = 380, command = lambda: prog_info_move(1))
        prog_info_move_button.place(relx = .8, rely = .96, anchor = CENTER)

        prog_info_back_button = CTkButton(prog_info_root, text = "Назад", bg_color = "#242424", width = 380, command = lambda: prog_info_move(0))
        prog_info_back_button.place(relx = .2, rely = .96, anchor = CENTER)


    program_info_button = CTkButton(main_canvas, text = "🛈", width = 30, bg_color = "#3d3d3d", command = program_info)
    program_info_button.place(relx = .82, rely = .044, anchor = CENTER)

    #module_frame = CTkScrollableFrame(main_canvas, width = 730, height = 539, fg_color = "#242424", bg_color = "#242424")
    #module_frame.place(relx = .625, rely = .542, anchor = CENTER)

    #main_menu_frame_1 = CTkFrame(main_canvas, width = 30, height = 370, corner_radius = 20, fg_color = "#3d3d3d", bg_color = "#242424")
    #main_menu_frame_1.place(relx = .965, rely = .54, anchor = CENTER)

    #main_menu_slight_button_up = CTkButton(main_canvas, width = 20, height = 175, corner_radius = 20, fg_color = "#1f6aa5", bg_color = "#3d3d3d", text = "⯅")
    #main_menu_slight_button_up.place(relx = .965, rely = .465, anchor = CENTER)

def account_profile_create():
    global med_card_frame
    global profile_canvas
    profile_canvas = CTkCanvas(main_root, width = 1000, height = 600, background = "#242424")
    profile_canvas.create_rectangle(0, 0, 1010, 50, fill="#3d3d3d", outline="#3d3d3d")

    profile_frame3 = CTkFrame(profile_canvas, width = 270, height = 160, corner_radius = 20, fg_color = "#3d3d3d")
    profile_frame3.place(relx = .5, rely = .05, anchor = CENTER)

    profile_med_card_label = CTkLabel(profile_canvas, text = "Мед. Карта", font = ("Arial", 32), bg_color = "#3d3d3d")
    profile_med_card_label.place(relx = .5, rely = .125, anchor = CENTER)

    global profile_name_label
    profile_name_label = CTkLabel(profile_canvas, font = ("Arial", 25), bg_color = "#3d3d3d")
    profile_name_label.place(relx = .5, rely = .043, anchor = CENTER)

    med_card_frame = CTkScrollableFrame(profile_canvas, width = 950, height = 460)
    med_card_frame.place(relx = .5, rely = .59, anchor = CENTER)

    def update_med_card():
        global med_card_frame
        med_card_frame.destroy()

        med_card_frame = CTkScrollableFrame(profile_canvas, width=950, height=460)
        med_card_frame.place(relx=.5, rely=.59, anchor=CENTER)

        med_card_massive = database.get_acc_medcard_info(aftarisation_login)
        med_card_module_massive = json.loads(med_card_massive[0])
        med_card_info_massive = json.loads(med_card_massive[1])
        med_card_dates_massive = json.loads(med_card_massive[2])

        def show_med_card_info(module, info, date):
            global med_card_frame
            med_card_add_info_root = CTkToplevel()
            med_card_add_info_root.geometry("500x350")
            med_card_add_info_root.title(f"История Мед. Карты Пользователя: {module}")

            med_card_add_info_textbox = CTkTextbox(med_card_add_info_root, width=490, height=300)
            med_card_add_info_textbox.place(relx=.5, rely=.45, anchor=CENTER)
            med_card_add_info_textbox.insert("1.0", text=info)

            def docx_export():
                file_path = filedialog.asksaveasfilename(defaultextension=".docx",filetypes=[("Word documents", "*.docx"), ("All files", "*.*")],title="Сохранить файл как...")
                if file_path:
                    doc = DocxTemplate("HT шаблон.docx")
                    name_info_massive = database.get_name_info(aftarisation_login)
                    context = {"name": f"{name_info_massive[0]}", "surname": f"{name_info_massive[1]}","date": f"{date}","recomed": f"{info}"}
                    doc.render(context)
                    doc.save(file_path)

            med_card_add_info_button = CTkButton(med_card_add_info_root, width=300, text="Экспортировать docx", command = docx_export)
            med_card_add_info_button.place(relx=.315, rely=.94, anchor=CENTER)

            def delete_info_from_med_card():
                database.delete_acc_medcard_info(aftarisation_login,info)

            med_card_del_info_button = CTkButton(med_card_add_info_root, width = 180, text = "Удалить", fg_color = 'red', command = delete_info_from_med_card)
            med_card_del_info_button.place(relx = .805, rely = .94, anchor = CENTER)

        for i2 in range(len(med_card_module_massive)):
            med_card_info_button = CTkButton(med_card_frame, fg_color = "#43454a", text = f"{med_card_module_massive[i2]}      {med_card_dates_massive[i2]}", width = 900, command = lambda m1_index = med_card_module_massive[i2], inf1_index = med_card_info_massive[i2], date_index = med_card_dates_massive[i2]: show_med_card_info(m1_index, inf1_index,date_index))
            med_card_info_button.pack(side = "bottom", pady = 20)

    med_card_update = CTkButton(profile_canvas, width = 30, text = "↺", command = update_med_card, bg_color = "#3d3d3d")
    med_card_update.place(relx = .82, rely = .044, anchor = CENTER)

    def profile_log_out():
        global is_login
        global is_aftarisation
        global aftarisation_login
        global history_frame
        global med_card_frame
        med_card_frame.destroy()

        med_card_frame = CTkScrollableFrame(profile_canvas, width=950, height=460)
        med_card_frame.place(relx=.5, rely=.59, anchor=CENTER)

        history_frame.destroy()
        history_frame = CTkScrollableFrame(main_canvas, width=220, height=520, fg_color="#3d3d3d", bg_color="#3d3d3d")
        history_frame.place(relx=.125, rely=.53, anchor=CENTER)

        is_login = False
        is_aftarisation = False
        aftarisation_login = None
        settings_canvas.place(relx = .5, rely = .5, anchor = CENTER)
        profile_canvas.place(relx = 10, rely = .5, anchor = CENTER)

    profile_exit_button = CTkButton(profile_canvas, fg_color = "#1f6aa5", text = "Выйти", bg_color = "#3d3d3d", width = 130, command = profile_log_out)
    profile_exit_button.place(relx = .09, rely = .045, anchor = CENTER)

def profile_menu_create():

    global settings_canvas
    settings_canvas = CTkCanvas(main_root, width = 1000, height = 600, background = "#242424")
    settings_canvas.create_rectangle(0,0,1010,50, fill = "#3d3d3d", outline = "#3d3d3d")

    settings_canvas.create_image(500, 200, image = profile_image)

    settings_login_input = CTkEntry(settings_canvas, width = 300, border_color = "#1f6aa5", fg_color = "white", placeholder_text = "Логин",text_color = "#242424")
    settings_login_input.place(relx = .5, rely = .5, anchor = CENTER)

    settings_password_input = CTkEntry(settings_canvas, width = 260, border_color = "#1f6aa5", fg_color = "white", placeholder_text = "Пароль", show="•",text_color = "#242424")
    settings_password_input.place(relx = .48, rely = .59, anchor = CENTER)

    global login_show_password_check
    login_show_password_check = 0

    def show_login_password():
        global login_show_password_check
        if login_show_password_check == 0:
            settings_password_input.configure(show="")
            login_show_password_check = 1
        elif login_show_password_check == 1:
            settings_password_input.configure(show="•")
            login_show_password_check = 0

    login_show_password_button = CTkButton(settings_canvas, text="👁", fg_color="#1f6aa5", width=30, command = show_login_password)
    login_show_password_button.place(relx=.635, rely=.59, anchor=CENTER)

    def account_log_in():
        global aftarisation_login
        global is_aftarisation
        if database.found_login(settings_login_input.get()) is False:
            login_error_label = CTkLabel(main_root, text = "Такого пользователя не существует!", text_color = "red", font = ('Arial', 15))
            login_error_label.place(relx = .5, rely = .72, anchor = CENTER)
            settings_login_input.configure(border_color = "red")

            def login_error_destroy():
                login_error_label.destroy()
                settings_login_input.configure(border_color = "#1f6aa5")

            main_root.after(2000, login_error_destroy)

        else:
            if database.password_searching(settings_login_input.get()) != settings_password_input.get():
                log_in_password_error_label = CTkLabel(main_root, text="Неправильный пароль!", text_color="red",font=('Arial', 15))
                log_in_password_error_label.place(relx=.5, rely=.72, anchor=CENTER)
                settings_password_input.configure(border_color="red")

                def log_in_password_error_destroy():
                    log_in_password_error_label.destroy()
                    settings_password_input.configure(border_color="#1f6aa5")

                main_root.after(2000, log_in_password_error_destroy)

            else:

                settings_canvas.place(relx = 10, rely  = .5, anchor = CENTER)
                profile_name_label.configure(text = f"{database.get_name_info(settings_login_input.get())[1]} {database.get_name_info(settings_login_input.get())[0]}")
                profile_canvas.place(relx = .5, rely = .5, anchor = CENTER)

                aftarisation_login = settings_login_input.get()

                settings_login_input.delete(0, END)
                settings_password_input.delete(0, END)

                global is_login
                is_login = True

                is_aftarisation = True
                print(is_aftarisation)
                print(aftarisation_login )


    log_in_button = CTkButton(settings_canvas, text = "Войти", width = 300, fg_color = "#1f6aa5", command = account_log_in)
    log_in_button.place(relx = .5, rely = .67, anchor = CENTER)

    def register_create():
        global reg_canvas
        reg_canvas = CTkCanvas(main_root, width=1000, height=600, background="#242424")
        reg_canvas.create_rectangle(0, 0, 1010, 50, fill="#3d3d3d", outline="#3d3d3d")
        reg_canvas.create_image(350, 335, image = register_image)

        def reg_exit():
            reg_canvas.place(relx = 10, rely = .1, anchor = CENTER)

        reg_name_get = StringVar()
        reg_surname_get = StringVar()
        reg_login_get = StringVar()
        reg_password_get = StringVar()

        exit_button = CTkButton(reg_canvas, text = "⯇ Назад ", bg_color = "#3d3d3d", width = 150, fg_color = "#1f6aa5", command = reg_exit)
        exit_button.place(relx = .1, rely = .045, anchor = CENTER)

        reg_name_label = CTkLabel(reg_canvas, text = "Имя", font = ("Arial", 25))
        reg_name_label.place(relx = .5, rely = .275, anchor = CENTER)

        reg_name_input = CTkEntry(reg_canvas, width = 300, border_color = "#1f6aa5", fg_color = "white", text_color = "#242424", textvariable = reg_name_get)
        reg_name_input.place(relx = .62, rely = .34, anchor = CENTER)

        reg_surname_label = CTkLabel(reg_canvas, text = "Фамилия", font = ("Arial", 25))
        reg_surname_label.place(relx = .53, rely = .405, anchor = CENTER)

        reg_surname_input = CTkEntry(reg_canvas, width = 300, border_color = "#1f6aa5", fg_color = "white", text_color = "#242424", textvariable = reg_surname_get)
        reg_surname_input.place(relx = .62, rely = .47, anchor = CENTER)

        reg_login_label = CTkLabel(reg_canvas, text = "Логин", font = ("Arial", 25))
        reg_login_label.place(relx = .51, rely = .535, anchor = CENTER)

        reg_login_input = CTkEntry(reg_canvas, width = 300, border_color = "#1f6aa5", fg_color = "white", text_color = "#242424", textvariable = reg_login_get)
        reg_login_input.place(relx = .62, rely = .6, anchor = CENTER)

        reg_password_label = CTkLabel(reg_canvas, text = "Пароль", font = ("Arial", 25))
        reg_password_label.place(relx = .52, rely = .665, anchor = CENTER)

        reg_password_input = CTkEntry(reg_canvas, width = 260, border_color = "#1f6aa5", fg_color = "white", text_color = "#242424", textvariable = reg_password_get, show = "•")
        reg_password_input.place(relx = .6, rely = .73, anchor = CENTER)

        global reg_show_password_check
        reg_show_password_check = 0

        def show_reg_password():
            global reg_show_password_check
            if reg_show_password_check == 0:
                reg_password_input.configure(show = "")
                reg_show_password_check = 1
            elif reg_show_password_check == 1:
                reg_password_input.configure(show = "•")
                reg_show_password_check = 0

        reg_show_password_button = CTkButton(reg_canvas, text = "👁", fg_color = "#1f6aa5", width = 30, command = show_reg_password)
        reg_show_password_button.place(relx = .755, rely = .73, anchor = CENTER)

        def reg_account():
            if reg_name_get.get() == "" or reg_surname_get.get() == "" or reg_login_get.get() == "" or reg_password_get.get() == "":
                reg_error_text = CTkLabel(reg_canvas, text = "Необходимо заполнить все поля!", text_color = "red", font = ("Arial", 15))
                reg_error_text.place(relx = .62, rely = .87, anchor = CENTER)

                if reg_name_get.get() == "":
                    reg_name_input.configure(border_color = "red")

                if reg_surname_get.get() == "":
                    reg_surname_input.configure(border_color = "red")

                if reg_login_get.get() == "":
                    reg_login_input.configure(border_color = "red")

                if reg_password_get.get() == "":
                    reg_password_input.configure(border_color = "red")

                def error_back():
                    reg_error_text.destroy()
                    reg_name_input.configure(border_color="#1f6aa5")
                    reg_surname_input.configure(border_color="#1f6aa5")
                    reg_login_input.configure(border_color="#1f6aa5")
                    reg_password_input.configure(border_color="#1f6aa5")

                main_root.after(2000, error_back)

            else:

                if database.found_login(reg_login_get.get()) is True:
                    login_error_text = CTkLabel(reg_canvas, text="Такой Логин уже существует!", text_color="red",font=("Arial", 15))
                    login_error_text.place(relx=.62, rely=.87, anchor=CENTER)
                    reg_login_input.configure(border_color="red")

                    def login_error_back():
                        login_error_text.destroy()
                        reg_login_input.configure(border_color="#1f6aa5")

                    main_root.after(2000, login_error_back)

                elif "1234" in reg_password_get.get() or "qwerty" in reg_password_get.get():
                    password_error_text = CTkLabel(reg_canvas, text="Пароль слишком прост!", text_color="red",font=("Arial", 15))
                    password_error_text.place(relx=.62, rely=.87, anchor=CENTER)
                    reg_password_input.configure(border_color="red")

                    def password_error_back():
                        password_error_text.destroy()
                        reg_password_input.configure(border_color="#1f6aa5")

                    main_root.after(2000, password_error_back)

                else:
                    database.create_account(reg_name_get.get(),reg_surname_get.get(),reg_login_get.get(),reg_password_get.get())
                    reg_name_input.delete(0, END)
                    reg_surname_input.delete(0, END)
                    reg_login_input.delete(0, END)
                    reg_password_input.delete(0, END)

                    reg_canvas.place(relx = 10, rely = 10, anchor = CENTER)

                    CTkMessagebox(title = "Регистрация", message = "Вы успешно зарегистрировали учётную запись!")


        register_button = CTkButton(reg_canvas, text = "Зарегистрироваться", fg_color = "#1f6aa5", bg_color = "#3d3d3d", width = 300, height = 30, command = reg_account)
        register_button.place(relx = .62, rely = .81, anchor = CENTER)


    register_create()

    def register():
        reg_canvas.place(relx=.5, rely=.5, anchor=CENTER)

    reg_button = CTkButton(settings_canvas, text = "Регистрация", width = 140, fg_color = "#1f6aa5", bg_color = "#3d3d3d", command = register)
    reg_button.place(relx = .1, rely = .045, anchor = CENTER)

    def switch_cheng():
        if program_theme_switch.get() == 1:
            set_appearance_mode("Light")
        else:
            set_appearance_mode("Dark")

    program_theme_switch = CTkSwitch(settings_canvas, text=" ", bg_color="#3d3d3d", command=switch_cheng)
    program_theme_switch.place(relx=.85, rely=.042, anchor=CENTER)

main_menu_create()
profile_menu_create()
account_profile_create()

def program_settings(choice):
    if choice == "Главное меню":
        main_canvas.place(relx = .5, rely = .5, anchor = CENTER)
        settings_canvas.place(relx=10, rely=.5, anchor=CENTER)
        profile_canvas.place(relx=10, rely=.5, anchor=CENTER)

    elif choice == "Профиль":
        main_canvas.place(relx=10, rely=.5, anchor=CENTER)
        profile_canvas.place(relx=10, rely=.5, anchor=CENTER)
        if is_login is False:
            settings_canvas.place(relx = .5, rely = .5, anchor = CENTER)
        else:
            profile_canvas.place(relx=.5, rely=.5, anchor=CENTER)

program_menu_options = ["Главное меню","Профиль"]
program_menu = CTkOptionMenu(main_root, values = program_menu_options, width = 120, height = 30, command = program_settings, bg_color = "#3d3d3d")
program_menu.place(relx = .915, rely = .042, anchor = CENTER)

main_root.mainloop()