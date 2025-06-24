import cv2
import numpy as np
from PIL import Image
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

root = Tk()
root.withdraw()  # Скрываем главное окно tkinter

def load_image():
    print("Откроется окно для выбора изображения (png или jpg)")
    root.attributes('-topmost', True)  # Сделать окно выбора файла сверху
    path = askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")], title="Выберите изображение")
    root.attributes('-topmost', False)  # Снять флаг верхнего окна
    if not path:
        print("Файл не выбран")
        return None
    print(f"Выбран файл: {path}")
    path = os.path.normpath(path)

    try:
        pil_img = Image.open(path).convert('RGB')
    except Exception as e:
        print(f"Ошибка при загрузке через Pillow: {e}")
        return None

    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    return img

def capture_from_webcam():
    print("Подключаемся к веб-камере...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Ошибка: не удалось подключиться к веб-камере.")
        print("Проверьте, что веб-камера подключена и не используется другой программой.")
        return None

    print("Нажмите пробел для съёмки фотографии, или ESC для выхода.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка: не удалось получить кадр с веб-камеры.")
            cap.release()
            return None

        cv2.imshow("Веб-камера — нажмите пробел для фото", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            print("Выход без съёмки.")
            cap.release()
            cv2.destroyAllWindows()
            return None
        elif key == 32:  # Пробел
            print("Фото сделано.")
            cap.release()
            cv2.destroyAllWindows()
            return frame

def resize_for_screen(img, max_scale=0.8):
    screen_res = (root.winfo_screenwidth(), root.winfo_screenheight())
    max_width = int(screen_res[0] * max_scale)
    max_height = int(screen_res[1] * max_scale)

    height, width = img.shape[:2]

    scaling_factor = min(max_width / width, max_height / height, 1.0)

    if scaling_factor < 1.0:
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
        return resized_img
    else:
        return img

def show_image(img, title="Изображение"):
    img_to_show = resize_for_screen(img)
    cv2.imshow(title, img_to_show)
    print("Нажмите любую клавишу в окне для закрытия.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def select_channel(img):
    channel_map = {'R': 2, 'G': 1, 'B': 0}
    while True:
        ch = input("Выберите цветовой канал (R, G, B): ").strip().upper()
        if ch in channel_map:
            channel_index = channel_map[ch]
            channel_img = img[:, :, channel_index]
            show_image(channel_img, title=f"Канал {ch}")
            break
        else:
            print("Некорректный ввод. Введите R, G или B.")

def resize_image(img):
    while True:
        try:
            width = int(input("Введите новую ширину изображения (px): "))
            height = int(input("Введите новую высоту изображения (px): "))
            if width <= 0 or height <= 0:
                print("Ширина и высота должны быть положительными числами. Попробуйте ещё раз.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целые числа.")

    resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    print(f"Изображение изменено до размера {width}x{height} пикселей.")
    return resized_img

def rotate_image(img):
    while True:
        try:
            angle = float(input("Введите угол вращения изображения (в градусах, например 45 или -30): "))
            break
        except ValueError:
            print("Ошибка: введите число (например, 45 или -30).")

    height, width = img.shape[:2]
    center = (width // 2, height // 2)

    rot_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    abs_cos = abs(rot_matrix[0, 0])
    abs_sin = abs(rot_matrix[0, 1])
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rot_matrix[0, 2] += bound_w / 2 - center[0]
    rot_matrix[1, 2] += bound_h / 2 - center[1]

    rotated_img = cv2.warpAffine(img, rot_matrix, (bound_w, bound_h))
    print(f"Изображение повернуто на {angle} градусов.")
    return rotated_img

def draw_green_line(img):
    height, width = img.shape[:2]

    def get_coordinate(prompt):
        while True:
            try:
                val = int(input(prompt))
                if ('x' in prompt.lower() and 0 <= val < width) or ('y' in prompt.lower() and 0 <= val < height):
                    return val
                else:
                    limit = width - 1 if 'x' in prompt.lower() else height - 1
                    print(f"Значение должно быть в пределах 0 и {limit}. Попробуйте ещё раз.")
            except ValueError:
                print("Ошибка: введите целое число.")

    print(f"Введите координаты линии. Размер изображения: ширина {width}, высота {height}.")

    x1 = get_coordinate("Введите x1 (начало линии, по ширине): ")
    y1 = get_coordinate("Введите y1 (начало линии, по высоте): ")
    x2 = get_coordinate("Введите x2 (конец линии, по ширине): ")
    y2 = get_coordinate("Введите y2 (конец линии, по высоте): ")

    while True:
        try:
            thickness = int(input("Введите толщину линии (положительное целое число): "))
            if thickness <= 0:
                print("Толщина должна быть положительным числом.")
                continue
            break
        except ValueError:
            print("Ошибка: введите целое число.")

    img_with_line = img.copy()
    cv2.line(img_with_line, (x1, y1), (x2, y2), (0, 255, 0), thickness)
    print("Линия нарисована.")
    return img_with_line

def get_initial_image():
    while True:
        print("Выберите способ загрузки изображения:")
        print("1 - Выбрать изображение из файла")
        print("2 - Сделать фото с веб-камеры")
        choice = input("Введите 1 или 2: ").strip()
        if choice == "1":
            img = load_image()
            if img is not None:
                return img
        elif choice == "2":
            img = capture_from_webcam()
            if img is not None:
                return img
        else:
            print("Некорректный ввод. Попробуйте снова.")

def main():
    img = get_initial_image()
    if img is None:
        print("Изображение не загружено. Завершение программы.")
        return

    show_image(img)

    while True:
        print("\nВыберите действие:")
        print("1 - Показать цветовой канал (R, G, B)")
        print("2 - Изменить размер изображения")
        print("3 - Вращение изображения")
        print("4 - Нарисовать зелёную линию")
        print("5 - Выйти")

        choice = input("Введите номер действия: ").strip()
        if choice == "1":
            select_channel(img)
        elif choice == "2":
            img = resize_image(img)
            show_image(img)
        elif choice == "3":
            img = rotate_image(img)
            show_image(img)
        elif choice == "4":
            img = draw_green_line(img)
            show_image(img)
        elif choice == "5":
            print("Выход.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
