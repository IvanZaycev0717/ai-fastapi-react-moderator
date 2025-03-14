# :cold_sweat: неТоксичные комментарии
![Image](https://github.com/user-attachments/assets/cd765111-14e9-4507-bb4f-ab17e3a3823f)
Веб-приложение на основе Искусственного Интеллекта (ИИ), которое анализирует полученные комменатарии, и **если они оказываются токсичными, переписывает их, убирая токсичность, но сохраняя смысл.**

## :battery: Технологии
### :fax: Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2
- aiosqlite
- grpcio
- pytest
- mimesis
- yandex-cloud-ml-sdk
- yandexcloud

### :calling: Frontend
- React 19
- Material UI
- Vite

### :inbox_tray: Общие технологии
- Docker

## :department_store: Архитектура приложения
![Image](https://github.com/user-attachments/assets/6b5ef960-e231-4aab-8f3b-e10d6f4bfa94)
В приложении использована распределённая архитектура с архитектурным стилем в виде микросервисов

## :ocean: Демонстрация работы клиентской части
![Image](https://github.com/user-attachments/assets/5c48ec4e-1d44-4cde-ae38-3677e1e31535)

## :clipboard: Спецификация OpenAPI
![Image](https://github.com/user-attachments/assets/f5115842-06a8-4a21-b7f1-980e7f6243e1)
Спецификация OpenAPI доступна по адресу `http://localhost:8000/docs`

## :slot_machine: Тестирование
![Image](https://github.com/user-attachments/assets/981c8039-59e6-4a07-82af-0ad12cb5be24)
Приложение польностью протестировано и готово к работе.

## :whale2: Установка и запуск на локальном компьютере

**ВНИМАНИЕ**: Использование API YandexGPT **ЯВЛЯЕТСЯ ПЛАТНЫМ** и тарифицируется по согласно тарифам Яндекс.Облако  
https://yandex.cloud/ru/prices

**ВАЖНО**: приложение позволяет отключать ИИ-модерацию, сохраняя полностью работоспособность. См. пункт 7

1. Клонировать репозиторий на локальный компьютер
```
git clone git@github.com:IvanZaycev0717/ai-fastapi-react-moderator.git
```
2. Перейти в папку проекта
```
cd ai-fastapi-react-moderator
```
3. Перейти в папку бэкенд части
```
cd backend
```
4. Открыть файл `.env.example` и получить права доступа
```
YC_FOLDER_ID = идентификатор каталога - получить здесь https://yandex.cloud/ru/docs/resource-manager/operations/folder/get-id

YC_SECRET_KEY = Секретный ключ в Yandex Cloud ML SDK - получить здесь https://yandex.cloud/ru/docs/foundation-models/sdk/
```
5. Присвоть `YC_FOLDER_ID` и `YC_SECRET_KEY` полученные данные
6. Переименовать `.env.example` в `.env`
7. Включить ИИ-модерацию в файле `settings.py`
```
# AI MODERATION CONTROL
IS_AI_MODERATION_ENABLED = True
```
8. Перейти в корневую директорию проекта
```
cd ..
```
9. Убедиться, что у вас установлен и запущен Docker
```
sudo docker version
```
10. Если Docker работает правильно, выполнить команду
```
sudo docker compose up -d
```
11. Перейти по адресу
```
http://localhost:3000
```
Если вы вставили неправильные данные в `.env` файл, то приложение выдаст ошибку при попытке опубликовать комментарий в виде всплывающего окна при включенной ИИ-модерации.

## 🧙 Автор
Иван Зайцев,  
FullStack Developer  
©2025


