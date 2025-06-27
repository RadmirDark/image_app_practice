# Приложение для обработки изображений

## Требование

-Python 3.7

## Описание
Десктоп-приложение на Python для выбора изображения из файла или съёмки с веб-камеры с последующей обработкой:
- отображение красного, зелёного или синего канала,
- изменение размера изображения,
- вращение изображения,
- рисование зелёной линии.

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/RadmirDark/image_app_practice.git
cd ./image_app_practice
```

2. Создайте и активируйте виртуальное окружение (пример с venv):
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate       # Windows
```

3. Установите зависимости и обновите pip:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Запуск
```bash
python app.py
```