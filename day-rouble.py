import extra_streamlit_components as stx
import streamlit as st
import json
import os
from datetime import datetime, timedelta

# --- СТРУКТУРЫ ДАННЫХ И КОНФИГУРАЦИЯ ---
ALL_PRODUCT_CATEGORIES = [
    "ДК", "КК", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
    "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет",
    "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК",
    "Селфи ДК", "Селфи КК", "Мобильное Приложение"
]

MENUS = {
    "ДК": [
        "ДК", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС",
        "Инвесткопилка", "БС со Стратегией", "Токенизация",
        "Накопительный Счет", "Вклад", "Детская Кросс", "Стикер Кросс",
        "Сим-Карта"
    ],
    "КК": [
        "КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС", "Инвесткопилка",
        "БС со Стратегией", "Токенизация", "Накопительный Счет", "Вклад",
        "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК"
    ],
    "Селфи": ["Селфи ДК", "Селфи КК"],
    "МП": ["Мобильное Приложение"]
}

# Таблица стоимости продуктов
PRODUCT_PRICES = {
    "ДК": 310,
    "КК": 570,
    "Комбо/Кросс КК": 570,
    "ЦП": 30,
    "Смарт": 30,
    "Кешбек": 30,
    "ЖКУ": 50,
    "БС": 270,
    "Инвесткопилка": 270,
    "БС со Стратегией": 270,
    "Токенизация": 30,
    "Накопительный Счет": 150,
    "Вклад": 0,
    "Детская Кросс": 430,
    "Стикер Кросс": 270,
    "Сим-Карта": 310,
    "Кросс ДК": 270,
    "Селфи ДК": 270,
    "Селфи КК": 570,
    "Мобильное Приложение": 310
}

# --- СТИЛИЗАЦИЯ (CSS) ---
def set_styles():
    """Применяет CSS стили для оформления приложения."""
    st.markdown("""
        <style>
            .main .block-container { background-color: #FFFFFF; }
            .stButton > button { width: 100%; height: 50px; border: 1px solid #CCCCCC; border-radius: 8px; color: #000000; font-family: 'Calibri', sans-serif; font-size: 16px; font-weight: normal; text-align: center; margin-bottom: 10px; }
            .stNumberInput > div > div > input { font-family: 'Calibri', sans-serif; color: #000000; }
            .report-text { font-family: 'Calibri', sans-serif; color: #000000; font-size: 18px; line-height: 1.6; }
            h1, h2, h3 { font-family: 'Calibri', sans-serif; color: #000000; }
        </style>
    """, unsafe_allow_html=True)

# --- ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ ---
def get_user_data_file(username):
    safe_username = "".join(c for c in username if c.isalnum() or c in (' ', '_')).strip()
    return f"data_{safe_username}.json"

def load_data_from_file(username):
    filename = get_user_data_file(username)
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("Некорректный формат данных.")
                return data
        except (json.JSONDecodeError, FileNotFoundError, ValueError) as e:
            st.error(f"Ошибка загрузки данных: {e}")
            return {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    return {category: 0 for category in ALL_PRODUCT_CATEGORIES}

def save_data_to_file(username, data):
    filename = get_user_data_file(username)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- УПРАВЛЕНИЕ СОСТОЯНИЕМ ---
def initialize_state():
    if 'view' not in st.session_state:
        st.session_state['view'] = "main_menu"
    if 'current_product' not in st.session_state:
        st.session_state['current_product'] = None

# --- ЛОГИКА ОТОБРАЖЕНИЯ ---
def display_login_screen(cookies):
    """Отображает экран для ввода имени пользователя и устанавливает cookie."""
    st.header("Добро пожаловать в калькулятор!")
    st.subheader("Пожалуйста, представьтесь, чтобы мы могли сохранить ваши данные.")
    
    username = st.text_input("Введите ваше имя:", key="login_input")
    
    if st.button("Войти", key="login_button"):
        if username:
            st.session_state['username'] = username
            cookies.set('username', username, expires_at=(datetime.now() + timedelta(days=30)))
            st.experimental_rerun()
        else:
            st.warning("Пожалуйста, введите имя.")

def display_main_menu():
    """Отображает основное меню."""
    st.header("Основное меню")
    col1, col2 = st.columns(2)
    with col1:
        st.button("ДК", on_click=lambda: go_to_menu("ДК"))
        st.button("Селфи", on_click=lambda: go_to_menu("Селфи"))
    with col2:
        st.button("КК", on_click=lambda: go_to_menu("КК"))
        st.button("МП", on_click=lambda: go_to_menu("МП"))
    st.button("Сформировать отчет", on_click=go_to_report)

def go_to_menu(menu_name):
    st.session_state['view'] = menu_name

def go_to_report():
    st.session_state['view'] = "report"

# --- ОСНОВНАЯ ЛОГИКА ---
def main():
    """Главная функция запуска Streamlit-приложения."""
    st.set_page_config(layout="centered")
    set_styles()
    cookies = stx.CookieManager()

    if 'username' not in st.session_state:
        st.session_state['username'] = cookies.get('username')

    if not st.session_state['username']:
        display_login_screen(cookies)
        return

    if 'data' not in st.session_state:
        st.session_state['data'] = load_data_from_file(st.session_state['username'])

    st.sidebar.text(f"Вы вошли как: {st.session_state['username']}")
    if st.sidebar.button("Сменить пользователя"):
        cookies.delete('username')
        st.session_state.pop('username', None)
        st.experimental_rerun()

    if st.session_state['view'] == "main_menu":
        display_main_menu()

if __name__ == "__main__":
    main()
