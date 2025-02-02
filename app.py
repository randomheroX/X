import streamlit as st

# Заголовок сайта
st.title("Добро пожаловать на мой сайт! 🚀")

# Текстовый блок
st.write("""
Это пример простого сайта, созданного с использованием Streamlit.
Здесь можно добавлять различные элементы, такие как текстовые поля, кнопки, графики и многое другое.
""")

# Ввод данных от пользователя
user_name = st.text_input("Введите ваше имя:")
if user_name:
    st.write(f"Привет, {user_name}! 👋")

# Кнопка
if st.button("Нажми меня"):
    st.write("Вы нажали кнопку! 🎉")

# Слайдер для выбора числа
number = st.slider("Выберите число", 0, 100)
st.write(f"Вы выбрали число: {number}")

# Отображение данных в виде таблицы
data = {
    "Имя": ["Алексей", "Мария", "Иван"],
    "Возраст": [25, 30, 22],
    "Город": ["Москва", "Санкт-Петербург", "Новосибирск"]
}
st.write("Пример таблицы:")
st.table(data)

# График
import pandas as pd
import numpy as np
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
st.line_chart(chart_data)
