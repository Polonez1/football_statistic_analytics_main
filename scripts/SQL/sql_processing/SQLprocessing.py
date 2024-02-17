def __delete_last_coma(element_list: list):
    if len(element_list) > 1:
        return str(tuple(element_list))
    string = str(tuple(element_list))
    last_comma_index = string.rfind(",")
    if last_comma_index != -1:
        modified_string = string[:last_comma_index] + string[last_comma_index + 1 :]
        return modified_string
