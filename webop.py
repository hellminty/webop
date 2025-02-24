import time
import threading
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def open_and_scroll_page(url, times, interval):
    try:
        service = Service(executable_path='./chromedriver')  # Укажите путь к вашему chromedriver
        driver = webdriver.Chrome(service=service)
        
        for i in range(times):
            print(f"Открытие страницы {i+1} из {times}")
            driver.get(url)
            
            # Пролистывание страницы до конца
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Задержка для загрузки контента
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Ожидание перед следующим открытием
            if i < times - 1:
                time.sleep(interval)  # Преобразуем минуты в секунды
        
        driver.quit()
        messagebox.showinfo("Успех", "Задача завершена!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def start_task():
    url = url_entry.get()
    times = int(times_entry.get())
    interval = int(interval_entry.get())
    
    if not url or times <= 0 or interval <= 0:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")
        return
    
    # Запуск задачи в отдельном потоке, чтобы не блокировать GUI
    threading.Thread(target=open_and_scroll_page, args=(url, times, interval)).start()

# Создание графического интерфейса
root = Tk()
root.title("Автоматизация открытия страниц")
root.geometry("400x200")

Label(root, text="URL страницы:").grid(row=0, column=0, padx=10, pady=10)
url_entry = Entry(root, width=30)
url_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Количество открытий:").grid(row=1, column=0, padx=10, pady=10)
times_entry = Entry(root, width=30)
times_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text="Интервал (в секундах):").grid(row=2, column=0, padx=10, pady=10)
interval_entry = Entry(root, width=30)
interval_entry.grid(row=2, column=1, padx=10, pady=10)

Button(root, text="Запустить", command=start_task).grid(row=3, column=0, columnspan=2, pady=20)

root.mainloop()