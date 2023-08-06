"""Dataclass to json conversion"""

__author__ = "Wytze Bruinsma"

def rec_to_json(objects):
    """
    Recursive function that can make a json from complex nested objects

    :param objects:
    :return:
    """

    def contains_dict(object):
        """
        Function check if object can be a dict

        :param object:
        :return:
        """

        try:
            _ = dict(object)
            return True
        except:
            return False

    if objects is None:
        return objects

    if contains_dict(objects):
        dic = dict(objects)
    else:
        dic = objects

    for key, value in dic.items():
        if isinstance(value, list):
            temp = []
            for v in value:
                if isinstance(v, dict) or isinstance(v, list) or contains_dict(v):
                    temp.append(rec_to_json(v))
                else:
                    temp.append(v)
            dic[key] = temp
        elif isinstance(value, dict) or contains_dict(value):
            dic[key] = rec_to_json(value)
    return dic
