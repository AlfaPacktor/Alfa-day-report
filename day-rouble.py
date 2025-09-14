import streamlit as st
import json
from collections import defaultdict
from datetime import datetime, timedelta
import extra_streamlit_components as stx

# --- CONSTANTS ---
CATEGORIES = {
    "ДК": ["ДК", "Комбо/Кросс КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС", "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет", "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта"],
    "КК": ["КК", "ЦП", "Смарт", "Кешбек", "ЖКУ", "БС", "Инвесткопилка", "БС со Стратегией", "Токенизация", "Накопительный Счет", "Вклад", "Детская Кросс", "Стикер Кросс", "Сим-Карта", "Кросс ДК"],
    "Селфи": ["Селфи ДК", "Селфи КК"],
    "Мобильное Приложение": ["Мобильное Приложение"]
}

PRICES = {
    "ДК": 310, "КК": 570, "Комбо/Кросс КК": 570, "ЦП": 30, "Смарт": 30, "Кешбек": 30,
    "ЖКУ": 50, "БС": 270, "Инвесткопилка": 270, "БС со Стратегией": 270, "Токенизация": 30,
    "Накопительный Счет": 150, "Вклад": 0, "Детская Кросс": 430, "Стикер Кросс": 270,
    "Сим-Карта": 310, "Кросс ДК": 270, "Селфи ДК": 270, "Селфи КК": 570, "Мобильное Приложение": 310
}

# --- HELPER FUNCTIONS ---
def get_data_file(username):
    """Generates a safe filename for storing user data."""
    return f"data_{''.join(c for c in username if c.isalnum() or c == '_')}.json"

def load_user_data(username):
    """Loads user data from a file."""
    file = get_data_file(username)
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {cat: 0 for cat in PRICES.keys()}

def save_user_data(username, data):
    """Saves user data to a file."""
    with open(get_data_file(username), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# --- STATE MANAGEMENT ---
def init_state():
    """Initializes session state variables."""
    if 'view' not in st.session_state:
        st.session_state['view'] = 'main'
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'data' not in st.session_state:
        st.session_state['data'] = defaultdict(int)

# --- VIEWS ---
def login_view():
    """Displays the login screen."""
    st.title("Добро пожаловать!")
    username = st.text_input("Введите ваше имя:", key="login_input")
    if st.button("Войти"):
        if username.strip():
            st.session_state['username'] = username.strip()
            st.session_state['data'] = load_user_data(username)
            st.experimental_rerun()
        else:
            st.warning("Пожалуйста, введите имя.")

def main_menu():
    """Displays the main menu."""
    st.title("Основное меню")
    col1, col2 = st.columns(2)
    with col1:
        st.button("ДК", on_click=lambda: set_view('ДК'))
        st.button("Селфи", on_click=lambda: set_view('Селфи'))
    with col2:
        st.button("КК", on_click=lambda: set_view('КК'))
        st.button("Мобильное Приложение", on_click=lambda: set_view('Мобильное Приложение'))
    st.button("Отчет", on_click=lambda: set_view('report'))

def category_menu(category):
    """Displays a submenu for a specific category."""
    st.title(f"Меню: {category}")
    for product in CATEGORIES[category]:
        st.button(product, on_click=lambda p=product: set_product(p))
    st.button("Назад", on_click=lambda: set_view('main'))

def product_input():
    """Displays the product input form."""
    product = st.session_state.get('current_product')
    if product:
        st.title(f"Добавить данные: {product}")
        quantity = st.number_input("Количество:", min_value=0, step=1)
        if st.button("Сохранить"):
            st.session_state['data'][product] += quantity
            save_user_data(st.session_state['username'], st.session_state['data'])
            st.success(f"{quantity} добавлено к {product}")
            set_view('main')
    else:
        st.error("Продукт не выбран.")
        set_view('main')

def report_view():
    """Displays the report of all products."""
    st.title("Отчет")
    data = st.session_state['data']
    total = 0
    for product, count in data.items():
        if count > 0:
            cost = PRICES.get(product, 0) * count
            total += cost
            st.write(f"{product}: {count} x {PRICES[product]} = {cost} руб.")
    st.write(f"ИТОГО: {total} руб.")
    st.button("Назад", on_click=lambda: set_view('main'))

# --- NAVIGATION HELPERS ---
def set_view(view_name):
    """Sets the current view."""
    st.session_state['view'] = view_name

def set_product(product_name):
    """Sets the current product and navigates to the input view."""
    st.session_state['current_product'] = product_name
    set_view('product_input')

# --- MAIN FUNCTION ---
def main():
    """Main entry point for the app."""
    st.set_page_config(layout="centered")
    cookies = stx.CookieManager()

    init_state()

    # Check if user is logged in
    if not st.session_state['username']:
        login_view()
        return

    # Define views
    views = {
        'main': main_menu,
        'ДК': lambda: category_menu('ДК'),
        'КК': lambda: category_menu('КК'),
        'Селфи': lambda: category_menu('Селфи'),
        'Мобильное Приложение': lambda: category_menu('Мобильное Приложение'),
        'product_input': product_input,
        'report': report_view,
    }

    # Render current view
    current_view = st.session_state['view']
    views.get(current_view, main_menu)()

if __name__ == "__main__":
    main()
