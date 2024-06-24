from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import (RangeSlider, Slider,
                                RadioButtons, CheckButtons,
                                TextBox)


def gaussian(sigma, mu, x):
    """Отображаемая фукнция"""
    return (1.0 / (sigma * np.sqrt(2.0 * np.pi))
            * np.exp(-((x - mu) ** 2) / (2 * sigma * sigma)))


def updateGraph():
    """!!! Функция для обновления графика"""
    global slider_sigma
    global slider_mu
    global slider_x_range
    global graph_axes
    global x_min
    global x_max
    global radiobuttons_color
    global checkbuttons_grid

    # Словарь соответсвий текста и стиля линии
    colors = {"Красный": "r", "Синий": "b", "Зеленый": "g"}

    # Используем атрибут val, чтобы получить значение слайдеров
    sigma = slider_sigma.val
    mu = slider_mu.val

    # Получаем значение интервала
    x_min, x_max = slider_x_range.val

    x = np.arange(x_min, x_max, 0.01)
    y = gaussian(sigma, mu, x)

    # Выберем стиль линии по выбранному значению радиокнопок
    style = colors[radiobuttons_color.value_selected]

    graph_axes.clear()
    graph_axes.plot(x, y, style)
    graph_axes.set_xlim(x_min, x_max)

    # Определяем, нужно ли показывать сетку на графике
    grid_visible = checkbuttons_grid.get_status()[0]
    graph_axes.grid(grid_visible)

    plt.draw()


def onTitleChange(value: str):
    """!!! Обработчик события при изменении текста в поле ввода"""
    global graph_axes
    graph_axes.set_title(value)
    plt.draw()


def onCheckClicked(value: str):
    """Обработчик события при нажатии на флажок"""
    updateGraph()


def onRadioButtonsClicked(value: str):
    """Обработчик события при клике по RadioButtons"""
    updateGraph()


def onChangeValue(value: np.float64):
    """Обработчик события изменения значений μ и σ"""
    updateGraph()


def onChangeXRange(value: Tuple[np.float64, np.float64]):
    """Обработчик события измерения значения интервала по оси X"""
    updateGraph()


if __name__ == "__main__":
    # Начальные параметры графиков
    current_sigma = 0.2
    current_mu = 0.0
    x_min = -5
    x_max = 5

    # Создадим окно с графиком
    fig, graph_axes = plt.subplots()

    # Выделим область, которую будет занимать график
    fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.4)

    # Создадим слайдер для задания sigma
    axes_slider_sigma = plt.axes([0.3, 0.25, 0.5, 0.04])
    slider_sigma = Slider(
        axes_slider_sigma,
        label="σ",
        valmin=0.1,
        valmax=10.0,
        valinit=0.5,
        valfmt="%1.2f",
    )

    # Создадим слайдер для задания mu
    axes_slider_mu = plt.axes([0.3, 0.17, 0.5, 0.04])
    slider_mu = Slider(
        axes_slider_mu,
        label="μ",
        valmin=-20.0,
        valmax=20.0,
        valinit=0.0,
        valfmt="%1.2f",
    )

    # Создадим слайдер для задания интервала по оси X
    axes_slider_x_range = plt.axes([0.3, 0.09, 0.5, 0.04])
    slider_x_range = RangeSlider(
        axes_slider_x_range,
        label="x",
        valmin=-20.0,
        valmax=20.0,
        valinit=(x_min, x_max),
        valfmt="%1.2f",
    )

    # Создадим оси для переключателей
    axes_radiobuttons = plt.axes([0.05, 0.09, 0.17, 0.2])

    # Создадим переключатель
    radiobuttons_color = RadioButtons(
        axes_radiobuttons, ["Красный", "Синий", "Зеленый"]
    )

    # Создадим оси для флажка
    axes_checkbuttons = plt.axes([0.05, 0.01, 0.17, 0.07])

    # Создадим флажок
    checkbuttons_grid = CheckButtons(axes_checkbuttons, ["Сетка"], [True])

    # !!! Создадим оси для текстового поля
    axes_textbox = plt.axes([0.4, 0.01, 0.4, 0.05])

    # !!! Создадим текстовое поле
    textbox_title = TextBox(axes_textbox, "Заголовок")

    # Подпишемся на события при изменении значения слайдеров.
    slider_sigma.on_changed(onChangeValue)
    slider_mu.on_changed(onChangeValue)

    # Подпишемся на событие изменения интервала по оси X
    slider_x_range.on_changed(onChangeXRange)

    # Подпишемся на событие при переключении радиокнопок
    radiobuttons_color.on_clicked(onRadioButtonsClicked)

    # Подпишемся на событие при клике по флажку
    checkbuttons_grid.on_clicked(onCheckClicked)

    # !!! Подпишемся на события текстового поля
    textbox_title.on_text_change(onTitleChange)
    textbox_title.on_submit(onTitleChange)

    updateGraph()
    plt.show()
