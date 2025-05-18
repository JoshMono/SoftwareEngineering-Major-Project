def concatonate_list_of_strings_with_ampersand(list_of_strings):
    if len(list_of_strings) == 1:
        new_string = list_of_strings[0]
    else:
        new_string = ""
        for i, string in enumerate(list_of_strings):
            if i + 2 == len(list_of_strings):
                new_string += f"{string} & "
            elif i + 1 == len(list_of_strings):
                new_string += f"{string}"
            else:
                new_string += f"{string}, "
    return new_string