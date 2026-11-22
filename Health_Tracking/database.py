import sqlite3
import json
import datetime

HT_data_base = sqlite3.connect("HT_Data_Base.db")
HT_cursor = HT_data_base.cursor()

HT_cursor.execute("CREATE TABLE IF NOT EXISTS DataBase(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, surname TEXT NOT NULL, login TEXT NOT NULL, password TEXT NOT NULL, module TEXT NOT NULL, info TEXT NOT NULL, dates TEXT NOT NULL, medcard_module TEXT NOT NULL, medcard_info TEXT NOT NULL, medcard_dates TEXT NOT NULL)")

def create_account(Name,Surname,Login,Password):
    HT_cursor.execute('INSERT INTO DataBase(name, surname, login, password, module, info, dates, medcard_module, medcard_info, medcard_dates) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (Name, Surname, Login, Password,"None", "None","None", "None", "None", "None"))
    HT_data_base.commit()

def found_login(login):
    HT_cursor.execute("SELECT * FROM DataBase")
    found_login_massive = HT_cursor.fetchall()

    found_count = 0
    for i in found_login_massive:
        if login in i:
            found_count = 1

    if found_count == 1:
        return True
    else:
        return False

def password_searching(login):
    HT_cursor.execute("SELECT * FROM DataBase")
    found_password_massive = HT_cursor.fetchall()

    searched_password = ""

    for p in found_password_massive:
        if login == p[3]:
            searched_password = p[4]

    return searched_password

def get_name_info(login):
    HT_cursor.execute("SELECT * FROM DataBase")
    get_name_massive = HT_cursor.fetchall()

    name_massive  = []

    for n in get_name_massive:
        if login == n[3]:
            name_massive.append(n[1])
            name_massive.append(n[2])

    return name_massive

def insert_info_to_history(login, info, module):
    HT_cursor.execute("SELECT * FROM DataBase")

    base_massive = HT_cursor.fetchall()

    module_massive = []
    info_module_massive = []
    date_module_massive = []
    print(base_massive)

    for i in base_massive:
        if login in i:
            if i[5] == "None":
                module_massive.append(module)
                info_module_massive.append(info)
                date = str(datetime.datetime.now().date())
                date_module_massive.append(date)

                module_massive_app = json.dumps(module_massive, ensure_ascii=False)
                info_module_massive_app = json.dumps(info_module_massive, ensure_ascii=False)
                date_module_massive_app = json.dumps(date_module_massive,ensure_ascii=False)

                HT_cursor.execute("UPDATE DataBase SET module = ? WHERE login = ?", (module_massive_app, login))
                HT_cursor.execute("UPDATE DataBase SET info = ? WHERE login = ?", (info_module_massive_app, login))
                HT_cursor.execute("UPDATE DataBase SET dates = ? WHERE login = ?", (date_module_massive_app, login))
                HT_data_base.commit()

                HT_cursor.execute("SELECT * FROM DataBase")
                massive = HT_cursor.fetchall()
                print(massive)

            else:
                module_massive = json.loads(i[5])
                info_module_massive = json.loads(i[6])
                dates_module_massive = json.loads(i[7])

                module_massive.append(module)
                info_module_massive.append(info)
                date = str(datetime.datetime.now().date())
                dates_module_massive.append(date)

                module_massive_add = json.dumps(module_massive, ensure_ascii=False)
                info_module_massive_add = json.dumps(info_module_massive, ensure_ascii=False)
                dates_module_massive_add = json.dumps(dates_module_massive, ensure_ascii=False)

                HT_cursor.execute("UPDATE DataBase SET module = ? WHERE login = ?", (module_massive_add, login))
                HT_cursor.execute("UPDATE DataBase SET info = ? WHERE login = ?", (info_module_massive_add, login))
                HT_cursor.execute("UPDATE DataBase SET dates = ? WHERE login = ?", (dates_module_massive_add, login))
                HT_data_base.commit()

                HT_cursor.execute("SELECT * FROM DataBase")
                massive = HT_cursor.fetchall()
                print(massive)

def get_acc_info(login):
    HT_cursor.execute("SELECT module, info FROM DataBase WHERE login = ?",(login,))
    acc_info_massive = HT_cursor.fetchone()
    return acc_info_massive

def insert_into_medcard(login,module, info):
    HT_cursor.execute("SELECT * FROM DataBase")

    medcard_base_massive = HT_cursor.fetchall()

    medcard_module_massive = []
    medcard_info_module_massive = []
    medcard_dates_module_massive = []

    for i in medcard_base_massive:
        if login in i:
            if i[8] == "None":
                medcard_module_massive.append(module)
                medcard_info_module_massive.append(info)
                date = str(datetime.datetime.now().date())
                medcard_dates_module_massive.append(date)

                medcard_module_massive_app = json.dumps(medcard_module_massive, ensure_ascii=False)
                medcard_info_module_massive_app = json.dumps(medcard_info_module_massive, ensure_ascii=False)
                medcard_dates_module_massive_app = json.dumps(medcard_dates_module_massive, ensure_ascii=False)

                HT_cursor.execute("UPDATE DataBase SET medcard_module = ? WHERE login = ?", (medcard_module_massive_app, login))
                HT_cursor.execute("UPDATE DataBase SET medcard_info = ? WHERE login = ?", (medcard_info_module_massive_app, login))
                HT_cursor.execute("UPDATE DataBase SET medcard_dates = ? WHERE login = ?", (medcard_dates_module_massive_app, login))
                HT_data_base.commit()

                HT_cursor.execute("SELECT * FROM DataBase")
                medcard_massive = HT_cursor.fetchall()
                print(medcard_massive)

            else:
                medcard_module_massive = json.loads(i[8])
                medcard_info_module_massive = json.loads(i[9])
                medcard_dates_module_massive = json.loads(i[10])

                medcard_module_massive.append(module)
                medcard_info_module_massive.append(info)
                date = str(datetime.datetime.now().date())
                medcard_dates_module_massive.append(date)

                medcard_module_massive_add = json.dumps(medcard_module_massive, ensure_ascii=False)
                medcard_info_module_massive_add = json.dumps(medcard_info_module_massive, ensure_ascii=False)
                medcard_dates_module_massive_add = json.dumps(medcard_dates_module_massive, ensure_ascii=False)

                HT_cursor.execute("UPDATE DataBase SET medcard_module = ? WHERE login = ?", (medcard_module_massive_add, login))
                HT_cursor.execute("UPDATE DataBase SET medcard_info = ? WHERE login = ?", (medcard_info_module_massive_add, login))
                HT_cursor.execute("UPDATE DataBase SET medcard_dates = ? WHERE login = ?", (medcard_dates_module_massive_add, login))
                HT_data_base.commit()

                HT_cursor.execute("SELECT * FROM DataBase")
                medcard_massive = HT_cursor.fetchall()
                print(medcard_massive)

def get_acc_medcard_info(login):
    HT_cursor.execute("SELECT medcard_module, medcard_info, medcard_dates FROM DataBase WHERE login = ?",(login,))
    medcard_acc_info_massive = HT_cursor.fetchone()
    return medcard_acc_info_massive

def delete_acc_medcard_info(login,text):
    HT_cursor.execute("SELECT medcard_module, medcard_info, medcard_dates FROM DataBase WHERE login = ?",(login,))
    del_medcard_base_massive = HT_cursor.fetchone()
    print(del_medcard_base_massive)

    del_medcard_module_massive = json.loads(del_medcard_base_massive[0])
    del_medcard_info_massive = json.loads(del_medcard_base_massive[1])
    del_medcard_dates_massive = json.loads(del_medcard_base_massive[2])

    for i in range(len(del_medcard_info_massive)):
        if del_medcard_info_massive[i] == text:
            del_medcard_module_massive.pop(i)
            del_medcard_info_massive.pop(i)
            del_medcard_dates_massive.pop(i)

    del_medcard_module_massive_app = json.dumps(del_medcard_module_massive, ensure_ascii=False)
    del_medcard_info_massive_app = json.dumps(del_medcard_info_massive, ensure_ascii=False)
    del_medcard_dates_massive_app = json.dumps(del_medcard_dates_massive, ensure_ascii=False)

    HT_cursor.execute("UPDATE DataBase SET medcard_module = ?, medcard_info = ?, medcard_dates = ? WHERE login = ?", (del_medcard_module_massive_app, del_medcard_info_massive_app, del_medcard_dates_massive_app, login))
    HT_data_base.commit()
#HT_cursor.execute("SELECT * FROM DataBase")
#massive = HT_cursor.fetchall()
#print(massive)