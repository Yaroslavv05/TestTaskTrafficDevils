# Проект Telegram Request Manager

Ласкаво просимо до проєкту **Telegram Request Manager**! Цей проєкт дає змогу взаємодіяти з Telegram через API, керувати користувачами, ролями та запитами. Запуск проєкту спрощено завдяки використанню Docker Compose.

---

## 📦 Встановлення та запуск

1. **Клонуйте репозиторій:**

   ```bash
   git clone https://github.com/Yaroslavv05/TestTaskTrafficDevils.git
   cd TestTaskTrafficDevils
   ```

2. **Запустіть проект:**

   ```bash
   docker-compose up --build
   ```

3. **Доступ до проєкту:**
   - Після успішного запуску проєкт буде доступний за адресою: `http://localhost:8080/docs#/`.

---

## 🗂️ Основні функції
- **Реєстрація та аутентифікація користувачів**.
- **Управління ролями:** Адміністратор, Менеджер, Користувач.
- **Створення та надсилання запитів через Telegram API.**
- **Управління користувачами та запитами.**

---

## 📋 Документація

### 📑 Опис API
[Посилання на документацію з API](https://docs.google.com/document/d/1d12AycWfBWL7hQaExwzpnav3Xf1Y0oPlVU_KcHoYaHI/edit?usp=sharing)

### 📂 Опис структури бази даних
[Посилання на документацію бази даних](https://docs.google.com/document/d/1Xp06RjRf8JXLVZZghxESuUzRAFQPacLSTzWH5wSYpe4/edit?usp=sharing)

---

## 🛠️ Адміністратор за замовчуванням

Під час запуску проєкту автоматично додається користувач із правами адміністратора:
- **Ім'я користувача:** `admin`
- **Пароль:** `admin`

---

## 🚀 Вдалого використання!

