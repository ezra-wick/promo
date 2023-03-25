from django import template
from typing import Union

register = template.Library()


def darken_hex_color(hex_color: str, percent: Union[int, float]) -> str:
    if not (0 <= percent <= 100):
        raise ValueError("Процент должен быть в диапазоне от 0 до 100")

    if hex_color.startswith("#"):
        hex_color = hex_color[1:]

    length = len(hex_color)
    if length not in (3, 4, 6, 8):
        raise ValueError("Неверный формат цвета: длина должна быть 3, 4, 6 или 8 символов")

    if length in (3, 4):
        hex_color = ''.join([c * 2 for c in hex_color])

    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    a = int(hex_color[6:8], 16) if length == 8 else 255

    r = int(r * (1 - percent / 100))
    g = int(g * (1 - percent / 100))
    b = int(b * (1 - percent / 100))

    if length == 8:
        return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
    else:
        return f"#{r:02x}{g:02x}{b:02x}"



@register.filter(name="darken_color")
def darken_color(value: str, percent: Union[int, float]) -> str:
    return darken_hex_color(value, percent)
