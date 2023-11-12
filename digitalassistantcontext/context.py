import json
import re


class VariableNameError(Exception):
    """Вызывается, когда имя не соответствует ограничениям на имя переменной контекста"""
    pass


class VariableStructureNameError(Exception):
    """Вызывается, когда имя не соответствует ограничениям на имя переменной контекста"""
    pass


def assign_value_to_variable(initial: dict, var_key: str, var_value: str = None, is_assign: bool = False):
    """
    Присвоение значения элементу исходного словаря. При is_assign=False элементу словаря присваивается значение
    пустого словаря, если этот элемент отсутствует в словаре.

    Parameters:
        initial (dict):исходный словарь
        var_key (str):имя переменной
        var_value (str):значения переменной
        is_assign (boolean):присваивать значение

    Returns:
        str:значение переменной
    """
    if type(initial) is not dict:
        initial = dict()

    if is_assign:
        initial[var_key] = var_value
    else:
        if var_key not in initial:
            initial[var_key] = dict()

    return initial[var_key]


def create_var_name(path: list) -> str:
    """
    Создает имя переменной контекста по ее структуре

    :param path: структура переменной в виде упорядоченного списка ее основного имения и свойств

    :return: имя переменной контекста
    """
    if type(path) is list and len(path) > 0:
        name = path.pop(0)
        for p in path:
            name = f'{name}[{p}]'
    else:
        raise VariableStructureNameError("Неверная структура имени переменной контекста")
    return name


pattern = re.compile(r'\[([а-яА-Яa-zA-Z0-9_]+)]')


def parse_var_name(var_name: str) -> tuple:
    """
    Распознает имя переменной и преобразуется ее в набор основного имени и массив имен свойств

    :param var_name:имя переменной

    :return:основное имя и массив имен свойств
    """
    first_part = var_name.split('[', 1)[0]

    try:
        main_name = re.findall(pattern, f'[{first_part}]')[0]

        additional_names = pattern.findall(var_name)

        path = additional_names.copy()
        path.insert(0, main_name)

        if create_var_name(path) == var_name:
            return main_name, additional_names
        else:
            raise VariableNameError
    except IndexError:
        raise VariableNameError


def parse_var_to_list(var, path=None, var_list=None):
    if path is None: path = []
    if var_list is None: var_list = []
    if type(var) is dict:
        for k in var:
            copied_path = path.copy()
            copied_path.append(k)
            var_list = parse_var_to_list(var[k], copied_path, var_list)
    else:
        var_list.append({
            "name": create_var_name(path),
            "value": var
        })
    return var_list


class Context:
    variables: dict

    def __init__(self, variables=None, ctx: "Context" = None):
        self.parent = ctx
        if type(variables) is dict:
            self.variables = variables
        else:
            self.variables = dict()

    def set(self, var_name, var_value) -> None:
        main, add = parse_var_name(var_name)
        len_add = len(add)

        var = assign_value_to_variable(self.variables, main)

        for c, r in enumerate(add, 1):
            if len_add == c:
                var = assign_value_to_variable(var, r, var_value, True)
            else:
                var = assign_value_to_variable(var, r)

    def get(self, var_name) -> dict:
        main, add = parse_var_name(var_name)
        var = None
        if main in self.variables:
            var = self.variables[main]
            for n in add:
                var = var.get(n)
        return var


if __name__ == "__main__":
    try:
        print(create_var_name(['we','0']))
    except VariableStructureNameError as e:
        print(e)

    # with open('./context.json', encoding='utf-8') as f:
    #     context = Context(json.load(f))
    #     vars_list = parse_var_to_list(context.variables)
    #     with open('./variable.json', 'w', encoding='utf-8') as outfile:
    #         json.dump(vars_list, outfile, ensure_ascii=False, indent=4)
    #         context_reload = Context()
    #         for v in vars_list:
    #             context_reload.set(v.get("name"), v.get("value"))
    #         with open('./context_reload.json', 'w', encoding='utf-8') as file:
    #             json.dump(context_reload.variables, file, ensure_ascii=False, indent=4)
