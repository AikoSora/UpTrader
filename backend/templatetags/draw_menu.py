from django.template import Library
from django.utils.safestring import mark_safe
from backend.models import Menu


register = Library()


def get_index_element_in_array(element: dict, array: list):
    """
    Function for find element in array and return its index

    :element: dict
    :array: list
    
    :return: dict
    """
    return next((i for i, item in enumerate(array) if item["object"] == element), None)


def get_element_in_array(element: dict, array: list) -> dict:
    """
    Function for find element in array and return its element

    :element: dict
    :array: list

    :return: dict
    """
    object = get_index_element_in_array(element, array)
    if object is not None:
        if array:
            return array.pop(object)
    return {"object": element, "childrens": []}


def get_menu_objects(all_items: Menu) -> list:
    """
    Function for create menu object and return its

    :all_items: Menu

    :return: list
    """
    menu_and_items = []

    for item in all_items:
        for parent in item.parents.all():
            element = get_element_in_array(parent, menu_and_items)
            child_element = get_element_in_array(item, menu_and_items)
            element["childrens"].append(child_element)
            menu_and_items.append(element)

    for i, item in enumerate(reversed(menu_and_items), start=1):
        if i + 1 <= len(menu_and_items):
            childrens = menu_and_items[-(i + 1)]["childrens"]
            if item['object'] in [x['object'] for x in childrens]:
                index = get_index_element_in_array(item['object'], childrens)
                if index is not None:
                    childrens.pop(index)
                    childrens.append(item)
                    menu_and_items[-(i + 1)]["childrens"] = childrens

    menu_and_items = [menu_and_items[0]]
    for item in all_items:
        if item.parents.count() == 0 and get_index_element_in_array(item, menu_and_items) is None:
            menu_and_items.append({"object": item, "childrens": []})

    return menu_and_items


def checked_in_childrens(childrens: list, path: str) -> bool:
    """
    Function to check whether the child is selected

    :childrens: list
    :path: str

    :return: bool
    """
    for child in childrens:
        if len(child['childrens']) > 0:
            if checked := checked_in_childrens(child['childrens'], path):
                return checked
        if child['object'].url == path:
            return True
    return False


def serialize_dict_to_html(dict: dict, path: str, stop: bool = False) -> str:
    """
    Function to serialization from dictionary to html

    :dict: dict
    :path: str

    :return: str
    """
    temp_html = ""
    style = "'color: green'"

    menu = dict['object']
    checked = menu.url == path

    temp_html = f"<li><a href='{menu.url}' style={style if checked else ''}>{menu.title}</a></li>"

    if checked or checked_in_childrens(dict['childrens'], path):
        for child in dict['childrens']:
            if not stop:
                temp_html += "<ul>" + serialize_dict_to_html(child, path, checked) + "</ul>"

    return temp_html


@register.simple_tag(takes_context=True)
def draw_menu(context, name: str) -> mark_safe:
    """
    Logic of a draw_menu tag

    :name: str
    """

    html = "<ul>"

    menu = Menu.objects.get(name=name)
    menu_and_items = get_menu_objects(menu.menu_items.all())

    for item in menu_and_items:
        html += serialize_dict_to_html(item, context.request.path)

    return mark_safe(html + "</ul>")
