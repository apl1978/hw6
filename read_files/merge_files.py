import os


def load_files_to_dict():
    BASE_PATH = os.getcwd()
    TXT_DIR_NAME = 'sorted'
    result = {}
    files = os.listdir(TXT_DIR_NAME)
    for file_name in files:
        full_path = os.path.join(BASE_PATH, TXT_DIR_NAME, file_name)
        with open(full_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            t_tuple = (len(lines), lines)
            result[file_name] = t_tuple
    return result


def write_sorted_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        dict = load_files_to_dict()
        sorted_keys = sorted(dict, key=dict.get)
        for key in sorted_keys:
            quant_str, list_str = dict[key]
            file.write(f'{key}\n')
            file.write(f'{str(quant_str)}\n')
            file.writelines(list_str)
            file.write('\n')


write_sorted_file('result.txt')
