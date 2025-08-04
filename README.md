\# ⚡ EVSE Energy Star



Інтеграція для \[Home Assistant](https://www.home-assistant.io/), яка забезпечує локальне керування зарядними станціями \*\*Energy Star Pro\*\* та \*\*Eveus Pro\*\* через їхній вбудований веб-інтерфейс (JSON API).



![Logo](https://raw.githubusercontent.com/V-Plum/evse_energy_star/main/custom_components/evse_energy_star/icon.png)



---



\## 🔧 Можливості



\- Відображення статусу зарядної станції

\- Сенсори потужності, напруги, струму, температури

\- Контроль струму заряду, запуск/зупинка зарядки

\- Планування зарядки, таймери

\- Підтримка синхронізації часу

\- Повна локальна робота без хмари

\- UI-конфігурація через Config Flow

\- Підтримка \*\*Energy Star Pro\*\* і \*\*Eveus Pro\*\*



---



\## 🚀 Встановлення



\### Варіант 1: через HACS (рекомендовано)

1\. Відкрий HACS → "Інтеграції" → "Користувацький репозиторій"

2\. Встав:

https://github.com/V-Plum/evse_energy_star


markdown

Copy

Edit

3\. Вибери тип: `Integration`

4\. Встанови інтеграцію

5\. Перезапусти Home Assistant



\### Варіант 2: вручну

1\. Скачай ZIP архів або клонуй репозиторій

2\. Скопіюй папку `evse\_energy\_star` у:

config/custom\_components/evse\_energy\_star

3\. Перезапусти Home Assistant



---



\## ⚙️ Налаштування



1\. Перейдіть у `Налаштування` → `Пристрої та служби` → `Додати інтеграцію`

2\. Знайдіть "EVSE Energy Star"

3\. Введіть:

\- IP-адресу зарядної станції

\- Ім’я користувача

\- Пароль



---



\## 🖥️ Платформи



\- `sensor` — станція, напруга, струм, потужність, температура, енергія

\- `switch` — перемикач режиму, заземлення, розклад

\- `number` — обмеження струму/напруги

\- `button` — ручний запуск зарядки, синхронізація часу

\- `select` — вибір часової зони



---



\## 📷 Скриншоти



![Dashboard example](images/dashboard_example.png)



---



\## 🛠️ Вимоги



\- Home Assistant 2023.0 або новіше

\- Зарядна станція Energy Star Pro або Eveus Pro з активним web-інтерфейсом



---



\## 👤 Автор



\*\*\[@V-Plum](https://github.com/V-Plum)\*\*  

Pull requests, issues та зірочки — вітаються!



---



\## 📝 Ліцензія



\[MIT License](LICENSE)

