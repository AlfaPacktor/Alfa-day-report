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
    safe_username = "".join(c for c in username if c.isalnum() or c in (' ', '_')).rstrip()
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
        st.session_state['view'] = 'main_menu'
    if 'current_product' not in st.session_state:
        st.session_state['current_product'] = None

# --- ФУНКЦИИ-ПОМОЩНИКИ (Навигация) ---
def go_to_menu(menu_name):
    st.session_state['view'] = menu_name

def go_to_main_menu():
    st.session_state['view'] = 'main_menu'

def go_to_input(product_name):
    st.session_state['view'] = 'input_form'
    st.session_state['current_product'] = product_name

def go_to_report():
    st.session_state['view'] = 'report'

def go_to_rubles_report():
    st.session_state['view'] = 'calculate_rubles'

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
    
    username = st.text_input("Введите ваше имя (например, Иванов Иван):", key="login_input")
    
    if st.button("Войти", key="login_button"):
        if username:
            st.session_state['username'] = username
            cookies.set('username', username, expires_at=datetime.datetime.now() + datetime.timedelta(days=30))
            st.rerun()
        else:
            st.warning("Пожалуйста, введите имя.")

def display_main_menu():
    """Отображает кнопки главного меню."""
    st.header("Основное меню")
    col1, col2 = st.columns(2)
    with col1:
        st.button("ДК", on_click=go_to_menu, args=("ДК",), key="dk_menu")
        st.button("Селфи", on_click=go_to_menu, args=("Селфи",), key="selfie_menu")
    with col2:
        st.button("КК", on_click=go_to_menu, args=("КК",), key="kk_menu")
        st.button("МП", on_click=go_to_menu, args=("МП",), key="mp_menu")
    st.button("Сформировать отчет", on_click=go_to_report)

def display_submenu(menu_key, title):
    """Отображает кнопки подменю."""
    st.header(title)
    for product in MENUS[menu_key]:
        st.button(product, key=f"{menu_key}_{product}", on_click=go_to_input, args=(product,))
    st.button("Вернуться в основное меню", key=f"back_{menu_key}", on_click=go_to_main_menu)

def display_input_form():
    """Отображает форму для ввода количества продукта."""
    product = st.session_state['current_product']
    st.header(f"Ввод данных для: {product}")
    quantity = st.number_input("Введите количество:", min_value=0, step=1, key=f"input_{product}")
    if st.button("Добавить", key=f"add_{product}"):
        if 'data' not in st.session_state:
            st.session_state['data'] = {category: 0 for category in ALL_PRODUCT_CATEGORIES}
        st.session_state['data'][product] = st.session_state['data'].get(product, 0) + quantity
        save_data_to_file(st.session_state['username'], st.session_state['data'])
        st.success(f"Добавлено: {quantity} к '{product}'. Возврат в главное меню.")
        go_to_main_menu()
        st.rerun()

def display_report():
    """Отображает итоговый отчет."""
    st.header("Отчет")
    
    report_lines = []
    # Мы проходимся по нашему главному списку продуктов, чтобы порядок всегда был одинаковый
    for i, product in enumerate(ALL_PRODUCT_CATEGORIES, 1):
        # Вежливо и безопасно спрашиваем у памяти, какое количество для этого продукта записано.
        # Если ничего нет, считаем, что это 0.
        count = st.session_state.get('data', {}).get(product, 0)
        if count > 0: # Показываем только те продукты, которые были добавлены
            report_lines.append(f"{i}. {product} - {count}")

    # Выводим весь отчет как единый красивый текст
    if report_lines:
        st.markdown(f"<div class='report-text'>{'<br>'.join(report_lines)}</div>", unsafe_allow_html=True)
    else:
        st.info("Данных для отчета пока нет.")

    st.markdown("<br>", unsafe_allow_html=True) # Небольшой отступ
    
    # Кнопки для управления
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Сбросить", on_click=reset_data)
    with col2:
        st.button("Посчитать в рублях", on_click=go_to_rubles_report)
    with col3:
        st.button("Вернуться в меню", on_click=go_to_main_menu)


def display_rubles_report():
    """Отображает отчет, пересчитанный в рубли."""
    st.header("Отчет в рублях")

    report_lines = []
    total_rubles = 0

    # Проходимся по всем продуктам, чтобы посчитать стоимость
    for product in ALL_PRODUCT_CATEGORIES:
        count = st.session_state.get('data', {}).get(product, 0)
        if count > 0:
            price = PRODUCT_PRICES.get(product, 0)
            product_total = count * price
            total_rubles += product_total
            report_lines.append(f"{product} - {product_total} руб.")
    
    # Выводим отчет
    if report_lines:
        st.markdown(f"<div class='report-text'>{'<br>'.join(report_lines)}</div>", unsafe_allow_html=True)
        st.markdown("<hr>") # Горизонтальная линия для разделения
        st.markdown(f"<div class='report-text'><b>ИТОГО: {total_rubles} руб.</b></div>", unsafe_allow_html=True)
    else:
        st.info("Нет данных для расчета.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Кнопки навигации
    col1, col2 = st.columns(2)
    with col1:
        st.button("Вернуться", on_click=go_to_report, key="back_to_report")
    with col2:
        st.button("Вернуться в основное меню", on_click=go_to_main_menu, key="back_to_main_from_rubles")


# --- ГЛАВНАЯ ЧАСТЬ ПРОГРАММЫ (НАШ "ДИРИЖЕР") ---
def main():
    """Основная функция, запускающая приложение."""
    set_styles()
    
    cookies = stx.CookieManager()
    
    username_from_cookie = cookies.get('username')
    
    if 'username' not in st.session_state:
        st.session_state['username'] = username_from_cookie
    
    initialize_state()

    if st.session_state.get('username') is None:
        display_login_screen(cookies)
    else:
        if 'data_loaded' not in st.session_state:
            st.session_state['data'] = load_data_from_file(st.session_state['username'])
            st.session_state['data_loaded'] = True
        
        st.sidebar.success(f"Вы вошли как: {st.session_state['username']}")
        if st.sidebar.button("Сменить пользователя"):
            cookies.delete('username')
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        view = st.session_state.get('view', 'main_menu')
        
        if view == 'main_menu':
            display_main_menu()
        elif view == 'ДК':
            display_submenu('ДК', 'Меню для ДК')
        elif view == 'КК':
            display_submenu('КК', 'Меню для КК')
        elif view == 'Селфи':
            display_submenu('Селфи', 'Меню для Селфи')
        elif view == 'МП':
            display_submenu('МП', 'Меню для МП')
        elif view == 'input_form':
            display_input_form()
        elif view == 'report':
            display_report()
        elif view == 'calculate_rubles':
            display_rubles_report()

# --- КЛЮЧ ЗАЖИГАНИЯ ---
if __name__ == "__main__":
    main()
