import streamlit as st
import mysql.connector
from mysql.connector import Error
import hashlib

# Функция для подключения к базе данных
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="sql301.infinityfree.com",
            user="if0_38180994",  # Замените на ваше имя пользователя
            password="V7X3WL7HGMXFG ",  # Замените на ваш пароль
            database="fif0_38180994_python"
        )
        return connection
    except Error as e:
        st.error(f"Ошибка подключения к базе данных: {e}")
        return None

# Функция для хеширования пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Регистрация пользователя
def register_user(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            connection.commit()
            st.success("Регистрация прошла успешно!")
        except Error as e:
            st.error(f"Ошибка регистрации: {e}")
        finally:
            cursor.close()
            connection.close()

# Авторизация пользователя
def login_user(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        cursor.execute("SELECT id FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()
        return user

# Создание новой темы
def create_topic(title, user_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO topics (title, user_id) VALUES (%s, %s)", (title, user_id))
            connection.commit()
            st.success("Тема создана успешно!")
        except Error as e:
            st.error(f"Ошибка создания темы: {e}")
        finally:
            cursor.close()
            connection.close()

# Получение списка тем
def get_topics():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, title FROM topics")
        topics = cursor.fetchall()
        cursor.close()
        connection.close()
        return topics

# Создание сообщения
def create_message(content, topic_id, user_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO messages (content, topic_id, user_id) VALUES (%s, %s, %s)", (content, topic_id, user_id))
            connection.commit()
            st.success("Сообщение добавлено!")
        except Error as e:
            st.error(f"Ошибка добавления сообщения: {e}")
        finally:
            cursor.close()
            connection.close()

# Получение сообщений по теме
def get_messages(topic_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT m.content, u.username, m.created_at
            FROM messages m
            JOIN users u ON m.user_id = u.id
            WHERE m.topic_id = %s
            ORDER BY m.created_at
        """, (topic_id,))
        messages = cursor.fetchall()
        cursor.close()
        connection.close()
        return messages

# Основной интерфейс
def main():
    st.title("Интернет-форум")

    # Меню
    menu = ["Главная", "Регистрация", "Вход"]
    choice = st.sidebar.selectbox("Меню", menu)

    if choice == "Главная":
        st.subheader("Темы")
        topics = get_topics()
        if topics:
            for topic in topics:
                st.write(f"**{topic[1]}**")
                if st.button(f"Перейти к теме {topic[0]}"):
                    st.session_state.topic_id = topic[0]
        else:
            st.info("Темы пока отсутствуют.")

        if "topic_id" in st.session_state:
            st.subheader("Сообщения")
            messages = get_messages(st.session_state.topic_id)
            if messages:
                for message in messages:
                    st.write(f"**{message[1]}** ({message[2]}): {message[0]}")
            else:
                st.info("Сообщений пока нет.")

            if "user_id" in st.session_state:
                new_message = st.text_area("Напишите сообщение:")
                if st.button("Отправить"):
                    create_message(new_message, st.session_state.topic_id, st.session_state.user_id)

    elif choice == "Регистрация":
        st.subheader("Регистрация")
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type="password")
        if st.button("Зарегистрироваться"):
            register_user(username, password)

    elif choice == "Вход":
        st.subheader("Вход")
        username = st.text_input("Имя пользователя")
        password = st.text_input("Пароль", type="password")
        if st.button("Войти"):
            user = login_user(username, password)
            if user:
                st.session_state.user_id = user[0]
                st.success("Вход выполнен успешно!")
            else:
                st.error("Неверное имя пользователя или пароль.")

    if "user_id" in st.session_state:
        st.sidebar.write(f"Вы вошли как пользователь с ID: {st.session_state.user_id}")
        if st.sidebar.button("Выйти"):
            del st.session_state.user_id
            st.success("Вы вышли из системы.")

        if st.sidebar.button("Создать тему"):
            title = st.text_input("Название темы")
            if st.button("Создать"):
                create_topic(title, st.session_state.user_id)

if __name__ == "__main__":
    main()
