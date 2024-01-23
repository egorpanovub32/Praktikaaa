import string
import random
import csv
import pyperclip
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Путь к текстовому файлу
file_akk = "accaunts.txt"

#Метки аккаунтов
metki = ("YouTube", "Twitch", "Telegram", "VK", "Gmail", "TikTok", "Steam", "Discord")

#Заголовки таблицы
heads = ['Метка', 'Логин', 'Пароль']


#Генератор пароля
def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


# Функция для кнопки "Генерировать пароль"
def generate_password_btn():
    generated_password = generate_password()
    password.delete(0, tk.END)
    password.insert(0, generated_password)


#Генератор логина
def generate_login(length=8):
    characters = string.ascii_letters + string.digits
    login = ''.join(random.choice(characters) for _ in range(length))
    return login


# Функция для кнопки "Генерировать логин"
def generate_login_btn():
    generated_login = generate_login()
    login.delete(0, tk.END)
    login.insert(0, generated_login)


# Функция для добавления пользователя
def add_akk(login, password, metka):

    # Проверка на полностью заполненные поля
    if not login or not password or not metka:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля.")
        return

    # Проверка на сходство данных
    with open(file_akk, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            # Проверка сходства логина и метки
            if row[1].strip() == login and row[0].strip() == metka:
                messagebox.showwarning("Внимание", "Пользователь с таким логином и меткой уже существует.")
                return

    with open(file_akk, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([metka, ' ' + login, ' ' + password])

    messagebox.showinfo("Success", "Пользователь успешно добавлен.")


# Функция для кнопки "Добавить пользователя"
def add_akk_btn():
    add_akk(login.get(), password.get(), metka.get())
    login.delete(0, tk.END)
    password.delete(0, tk.END)
    metka.current(0)


# Проверка наличия пробела
def validate_no_space(char):
    return not ' ' in char


# Функция-обработчик события ввода символа
def on_validate(P):
    # Проверка наличия пробела в введенном символе
    return validate_no_space(P)



#Удаление логина и пароля с ввода
def del_log():
    login.delete(0, tk.END)


def del_pas():
    password.delete(0, tk.END)


# Функции для кнопки "Показать пароль"
def start_show_password(event):
    password.config(show="")


def end_show_password(event):
    password.config(show="*")


#Функция для вкладки Аккаунты
def create_akk_win():
    tab_win = tk.Toplevel(win)
    tab_win.wm_title('Аккаунты')
    photo = tk.PhotoImage(file='zamok.png')
    tab_win.iconphoto(False, photo)
    tab_win.resizable(width=False, height=False)

    tab_akk = ttk.Treeview(tab_win, show='headings')
    tab_akk['columns'] = heads
    tab_akk['displaycolumns'] = ['Метка', 'Логин', 'Пароль']


    def search_in_table():
        # Получаем запрос из Entry
        query = entry_search.get()

        # Очищаем таблицу
        tab_akk.delete(*tab_akk.get_children())

        with open(file_akk, mode='r') as file:
            accs = [line.strip().split(",") for line in file]

        # Ищем соответствия в данных и добавляем их в таблицу
        for row in accs:
            # Поиск по метке (если метка совпадает)
            if query in row[1].lower():
                tab_akk.insert("", "end", values=row)
            # Поиск по логину (если логин совпадает)
            elif query in row[0].lower():
                tab_akk.insert("", "end", values=row)

    def clear_entry_in_table():
        entry_search.delete(0, "end")

    # Функция для копирования выбранной строки
    def copy_to_clipboard():
        selected_item = tab_akk.selection()
        if selected_item:
            values = tab_akk.item(selected_item)['values']
            data_to_copy = "\t".join(map(str, values))
            pyperclip.copy(data_to_copy)
            pyperclip.determine_clipboard()
        else:
            messagebox.showinfo("Error", "Выберете строку для копирования.")

    # Функция для удаления выбранной строки
    def delete_selected_row():
        selected_item = tab_akk.selection()

        if selected_item:
            selected_index = tab_akk.index(selected_item)
            tab_akk.delete(selected_item)

            with open(file_akk, 'r') as file:
                lines = file.readlines()

            with open(file_akk, 'w') as file:
                for i, line in enumerate(lines):
                    if i != selected_index:
                        file.write(line)

            messagebox.showinfo('Внимание', 'Выбранная строка удалена.')
        else:
            messagebox.showwarning('Внимание', 'Выберите строку для удаления')


    #Создаем поле для поиска
    entry_search = ttk.Entry(tab_win, width=32)
    entry_search.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    # Создаем кнопку для запуска поиска
    btn_search = tk.Button(tab_win, text="Поиск", command=search_in_table)
    btn_search.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    ## Создаем кнопку для очистки Entry
    btn_clear = tk.Button(tab_win, text="Очистить", command=clear_entry_in_table)
    btn_clear.grid(row=0, column=2, padx=10, pady=10, sticky='w')

    # Создаем кнопку для копирования
    btn_copy = tk.Button(tab_win, text="Копировать", command=copy_to_clipboard, activebackground='#919191')
    btn_copy.grid(row=0, column=3, padx=10, pady=10, sticky='w')

    # Кнопка для удаления выбранной строки
    btn_delete = tk.Button(tab_win, text='Удалить строку', command=delete_selected_row)
    btn_delete.grid(row=1, column=3,padx=10, pady=10, sticky='w')

    for header in heads:
        tab_akk.heading(header, text=header, anchor='center')
        tab_akk.column(header, anchor='center')
    with open(file_akk, mode='r') as file:
        for i in file:
            tab_akk.insert('', tk.END, values=i)

    scroll_panel = ttk.Scrollbar(tab_win, command=tab_akk.yview)
    scroll_panel.grid(row=2, rowspan=2, column=3, sticky='ns',padx=10, pady=10)

    tab_akk.configure(yscrollcommand=scroll_panel.set)
    tab_akk.columnconfigure(0,  weight=1, minsize= 30)
    tab_akk.columnconfigure(1,  weight=1, minsize= 30)
    tab_akk.columnconfigure(2,  weight=1, minsize= 30)
    tab_akk.grid(row=2, column=0, columnspan=3, padx=10, pady=10)


#Функция для вкладки Выход
def close_win():
    win.destroy()


#Неизменяемый комбобокс
def make_combobox_readonly(combobox):
    combobox.bind("<FocusIn>", lambda e: combobox.unbind("<FocusIn>"))


#Главное окно
win = tk.Tk()
win.title('Менеджер аккаунтов')
photo = tk.PhotoImage(file='zamok.png')
win.iconphoto(False, photo)
win.geometry('335x170')
win.resizable(width=False, height=False)

metka = ttk.Combobox(win, values=metki)
make_combobox_readonly(metka)
metka.current(0)
metka.grid(row=2, column=1)

label_1 = tk.Label(win, text='Логин:')
label_1.grid(row=0, column=0)
label_1 = tk.Label(win, text='Пароль:')
label_1.grid(row=1, column=0)
label_1 = tk.Label(win, text='Метка:')
label_1.grid(row=2, column=0)

btn_generate_password = tk.Button(win, text='Сгенерировать пароль', command=generate_password_btn, activebackground='#919191')
btn_generate_password.grid(row=3, column=1, stick='we')

btn_generate_login = tk.Button(win, text='Сгенерировать логин', command=generate_login_btn, activebackground='#919191')
btn_generate_login.grid(row=3, column=0, stick='we')

btn_add_lp = tk.Button(win, text='Добавить', activebackground='#919191', command=add_akk_btn)
btn_add_lp.grid(row=4, column=0, columnspan=3, stick='we')

btn_watch_p = tk.Button(win,text="Показать пароль",activebackground='#919191')
btn_watch_p.bind("<Button-1>",start_show_password)
btn_watch_p.bind("<ButtonRelease-1>",end_show_password)
btn_watch_p.grid(row=5, column=0, columnspan=3, stick='we')

var_log = tk.StringVar()
var_pas = tk.StringVar()

login = tk.Entry(win, textvariable=var_log, validate='key', validatecommand=(win.register(on_validate), '%P'))
login.grid(row=0, column=1)

password = tk.Entry(win, show="*", textvariable=var_pas, validate='key', validatecommand=(win.register(on_validate), '%P'))
password.grid(row=1, column=1)

btn_del_l = tk.Button(win, text='Очистить', command=del_log, activebackground='#919191')
btn_del_l.grid(row=0, column=3)
btn_del_p = tk.Button(win, text='Очистить', command=del_pas, activebackground='#919191')
btn_del_p.grid(row=1, column=3)

menubar = tk.Menu(win)
win.config(menu=menubar)
accaunt_menu = tk.Menu(menubar, tearoff=0)
accaunt_menu.add_command(label='Аккаунты', command=create_akk_win)
accaunt_menu.add_command(label='Выход', command=close_win)
menubar.add_cascade(label='Вкладки', menu=accaunt_menu)


win.mainloop()