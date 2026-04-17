import os
from datetime import datetime
import pygame


# Загрузка картинки руки Микки
def load_hand_image():
    image_path = os.path.join("images", "mickey_hand.png")
    image = pygame.image.load(image_path).convert_alpha()
    return image


# Получаем текущее время и переводим в углы
def get_time_angles():
    now = datetime.now()

    minutes = now.minute
    seconds = now.second

    # 1 секунда = 6 градусов
    second_angle = -seconds * 6

    # 1 минута = 6 градусов
    minute_angle = -minutes * 6

    return minute_angle, second_angle, minutes, seconds


# Вращение картинки вокруг центра (самое важное!)
def rotate_hand(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)

    # фикс позиции центра (чтобы не уезжала)
    rotated_rect = rotated_image.get_rect(center=center)

    return rotated_image, rotated_rect


# Изменение размера руки
def scale_hand(image, width, height):
    return pygame.transform.smoothscale(image, (width, height))