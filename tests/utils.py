def px_to_rem(px_value, root_font_size=16):
    return px_value / root_font_size


def get_root_font_size(terminal_x_ui):
    html_element = terminal_x_ui.driver.find_element(('tag name', 'html'))
    font_size_px = html_element.value_of_css_property('font-size')
    return float(font_size_px.replace('px', ''))
