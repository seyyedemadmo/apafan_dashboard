from permissions.helpers.translate_json import *


def translate_permission(perm):
    try:
        perms = perm.split(' ', 2)
        translated = [can[perms[0]], four_option_in_permission[perms[1]], model_name_mapper[perms[2]]]
        return " ".join(translated)

    except Exception as e:
        return ""
