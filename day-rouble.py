import extra_streamlit_components as stx
import streamlit as st
import json
import os
import datetime

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
    safe_username = "".join(c for c in username if c.isalnum() or c in (' ', '-')).strip()
    return f"data_{safe_username}.json"

def load_data_from_file(username):
    filename = get_user_data_file(username)
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    return {category: 0 for category in ALL_PRODUCT_CATEGORIES}

def save_data_to_file(username, data):
    filename = get_user_data_file(username)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- УПРАВЛЕНИЕ СОСТОЯНИЕМ ---
def initialize_state():
    if 'view' not in st.session_state:
        st.session_state['view'] = 'main'
    if 'current_product' not in st.session_state:
        st.session_state['current_product'] = None

# --- ФУНКЦИИ-ПОМОЩНИКИ (Навигация) ---
def go_to_menu(menu_name):
    st.session_state['view'] = menu_name

def go_to_main_menu():
    st.session_state['view'] = 'main'

def go_to_input(product_name):
    st.session_state['view'] = 'input'
    st.session_state['current_product'] = product_name

def go_to_report():
    st.session_state['view'] = 'report'

def go_to_rubles_report():
    st.session_state['view'] = 'report_rubles'

def reset_data():
    fresh_data = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
    st.session_state['data'] = fresh_data
    save_data_to_file(st.session_state['username'], fresh_data)
    go_to_main_menu()

# --- ЛОГИКА ОТОБРАЖЕНИЯ ---
def display_login_screen(cookies):
    """Отображает экран для ввода имени пользователя и устанавливает cookie."""
    st.header("Добро пожаловать в калькулятор!")
    st.subheader("Пожалуйста, представьтесь, чтобы мы могли сохранить ваши данные.")
    
    username = st.text_input("Введите ваше имя (например, Иван Иванов):", key="login_input")
    
    if st.button("Войти", key="login_button"):
        if username:
            st.session_state['username'] = username
            cookies.set('username', username, expires_at=datetime.datetime.now() + datetime.timedelta(days=30))
            st.rerun()
        else:
            st.warning("Пожалуйста, введите имя.")
            def display_main_menu():
    """Displays the main menu buttons."""
    st.header("Основное меню")
    col1, col2 = st.columns(2)
    # Using the unified set_view function for navigation.
    with col1:
        st.button("ДК", on_click=set_view, args=("ДК",), key="dk_menu")
        st.button("Селфи", on_click=set_view, args=("Селфи",), key="selfie_menu")
    with col2:
        st.button("КК", on_click=set_view, args=("КК",), key="kk_menu")
        st.button("МП", on_click=set_view, args=("МП",), key="mp_menu")
    st.button("Сформировать отчет", on_click=set_view, args=('report',))

def display_submenu(menu_key, title):
    """Displays a submenu based on the provided key."""
    st.header(title)
    for product in MENUS[menu_key]:
        st.button(product, key=f"{menu_key}_{product}", on_click=set_view, args=('input', product))
    st.button("Вернуться в основное меню", key=f"back_{menu_key}", on_click=set_view, args=('main',))

def display_input_form():
    """Displays the form for product quantity input."""
    product = st.session_state['current_product']
    st.header(f"Ввод данных для: {product}")
    
    # Using a form to group input and button.
    with st.form(key=f"form_{product}"):
        quantity = st.number_input("Введите количество:", min_value=0, step=1, key=f"input_{product}")
        submitted = st.form_submit_button("Добавить")
        
        if submitted:
            # defaultdict simplifies adding new values.
            st.session_state['data'][product] += quantity
            save_data_to_file(st.session_state['username'], st.session_state['data'])
            st.success(f"Добавлено: {quantity} к '{product}'.")
            set_view('main')
            st.rerun()

def display_report():
    """Displays the final report of product counts."""
    st.header("Отчет")
    data = st.session_state.get('data', defaultdict(int))
    
    # Using a list comprehension for cleaner code.
    report_lines = [
        f"{i}. {product} - {count}"
        for i, product in enumerate(ALL_PRODUCT_CATEGORIES, 1)
        if (count := data[product]) > 0
    ]

    if report_lines:
        st.markdown(f"<div class='report-text'>{'<br>'.join(report_lines)}</div>", unsafe_allow_html=True)
    else:
        st.info("Данных для отчета пока нет.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Сбросить", on_click=reset_data)
    with col2:
        st.button("Посчитать в рублях", on_click=set_view, args=('report_rubles',))
    with col3:
        st.button("Вернуться в меню", on_click=set_view, args=('main',))

def display_rubles_report():
    """Displays the report converted to rubles."""
    st.header("Отчет в рублях")
    data = st.session_state.get('data', defaultdict(int))

    # Filter for products with count > 0 first to avoid unnecessary calculations.
    active_products = {p: c for p, c in data.items() if c > 0}
    
    if not active_products:
        st.info("Нет данных для расчета.")
    else:
        report_lines = [
            f"{product} - {count * PRODUCT_PRICES.get(product, 0)} руб."
            for product, count in active_products.items()
        ]
        total_rubles = sum(count * PRODUCT_PRICES.get(product, 0) for product, count in active_products.items())
        
        st.markdown(f"<div class='report-text'>{'<br>'.join(report_lines)}</div>", unsafe_allow_html=True)
        st.markdown("<hr>")
        st.markdown(f"<div class='report-text'><b>ИТОГО: {total_rubles} руб.</b></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Вернуться", on_click=set_view, args=('report',), key="back_to_report")
    with col2:
        st.button("Вернуться в основное меню", on_click=set_view, args=('main',), key="back_to_main_from_rubles")

# --- MAIN APPLICATION LOGIC ---
def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(layout="centered")
    set_styles()
    cookies = stx.CookieManager()

    # Initialize session state from cookie if not already set.
    if 'username' not in st.session_state:
        st.session_state['username'] = cookies.get('username')

    # If no user is logged in, show the login screen.
    if not st.session_state.get('username'):
        display_login_screen(cookies)
        return

    # Load data only once after login.
    if 'data' not in st.session_state:
        st.session_state['data'] = load_data_from_file(st.session_state['username'])

    # User info and logout button in the sidebar for better UI.
    st.sidebar.info(f"Вы вошли как: {st.session_state['username']}")
    if st.sidebar.button("Сменить пользователя"):
        cookies.delete('username')
        # Clear the entire session state to ensure a clean login.
        st.session_state.clear()
        st.rerun()

    # --- View Router ---
    # A dictionary-based router is cleaner than multiple if/elif statements.
    VIEWS = {
        'main': display_main_menu,
        'ДК': lambda: display_submenu('ДК', 'Меню для ДК'),
        'КК': lambda: display_submenu('КК', 'Меню для КК'),
        'Селфи': lambda: display_submenu('Селфи', 'Меню для Селфи'),
        'МП': lambda: display_submenu('МП', 'Меню для МП'),
        'input': display_input_form,
        'report': display_report,
        'report_rubles': display_rubles_report,
    }
    
    current_view = st.session_state.get('view', 'main')
    render_function = VIEWS.get(current_view, display_main_menu)
    render_function()

# --- APPLICATION ENTRY POINT ---
if __name__ == "__main__":
    main()
