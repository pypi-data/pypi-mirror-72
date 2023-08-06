import json
from pathlib import Path
# import pandas


class JsonHelper(dict):
    def __str__(self):
        return json.dumps(self)


def options_to_json(obj):
    attributes = JsonHelper(vars(obj))
    sub_attributes_json = JsonHelper({})
    for k in attributes.keys():
        sub_attributes = JsonHelper(vars(attributes[k]))
        sub_attributes_json[k] = sub_attributes
    return sub_attributes_json


def options_to_json_str(obj):
    return str(options_to_json(obj))


def json_to_pydict(json_item):
    py_dict = json.loads(str(json_item))
    return py_dict


def flatten_json_dict_to_str(nested_json_dict):
    dict_output = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            dict_output[name[:-1]] = x

    flatten(nested_json_dict)
    dict_output_to_json_str = JsonHelper(dict_output)

    return dict_output_to_json_str


# def write_json_dict_to_csv(json_dict, csv_file_name):
#     flattened_json = flatten_json_dict_to_str(json_dict)
#     print("FLATTENED JSON: ", flattened_json)
#
#     read_json = pandas.read_json(json.dumps([flattened_json]))
#
#     add_header = False
#     if Path(csv_file_name).is_file():
#         print("File exists")
#         add_header = False
#     else:
#         print("File not exist")
#         add_header = True
#
#     read_json.to_csv(str(csv_file_name), mode='a', header=add_header)
#     # read_json.to_csv(str(csv_file_name), mode='a', header=True)
