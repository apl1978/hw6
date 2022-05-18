def load_file_to_dict(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        result = {}
        dish = file.readline().strip()
        for line in file:
            quant = int(line)
            lines = []
            for item in range(quant):
                ingredient_name, quantity, measure = file.readline().strip().split(' | ')
                t_dict = {}
                t_dict["ingredient_name"] = ingredient_name
                t_dict["quantity"] = int(quantity)
                t_dict["measure"] = measure
                lines.append(t_dict)
            result[dish] = lines
            file.readline().strip()
            dish = file.readline().strip()
    return result


def get_shop_list_by_dishes(dishes, person_count):
    cook_book = load_file_to_dict('recipes.txt')
    result = {}
    for dish in dishes:
        if dish in cook_book:
            for ing in cook_book[dish]:
                ingredient_name = ing["ingredient_name"]
                if ingredient_name in result:
                    result[ingredient_name]["quantity"] += ing["quantity"] * person_count
                else:
                    t_dict = {}
                    t_dict["measure"] = ing["measure"]
                    t_dict["quantity"] = ing["quantity"] * person_count
                    result[ingredient_name] = t_dict
    return result


print(get_shop_list_by_dishes(['Омлет', 'Омлет'], 1))
print(get_shop_list_by_dishes(['Омлет'], 2))
print(get_shop_list_by_dishes(['Запеченный картофель', 'Омлет'], 2))
