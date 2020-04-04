from django import template


register = template.Library()


@register.filter
def bias_to_color(value):
    '''Turns a bias (-1.0 <= b <= 1.0) into a six digit HTML hex value.
    '''
    if value >= 0.0:
        r = int(255*(value))
        g = 0
        b = 0
    else:
        r = 0
        g = 0
        b = int(255*(-value))

    full_hex = ''
    for color in r, g, b:
        color_hex = hex(color)[2:]
        if len(color_hex) < 2:
            color_hex = '0' + color_hex  # FIXME: This is pretty hacky.
        full_hex += color_hex
    return full_hex
