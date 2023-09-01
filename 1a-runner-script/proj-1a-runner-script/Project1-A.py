import re
import urllib.parse
import sys


def num_nosj(data, key):

    match = re.match(r'f(-?\d+\.\d+)f',data)
    if match:
        return key, "num", float(match.group(1))
    else:
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)


def simple_string_nosj(data, key):
    match = re.match(r'([a-zA-Z0-9 \t]+)s',data)
    if match:
        return key, "simple string", match.group(1)
    else:
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)


def complex_string_nosj(data, key):
    match = re.match(r'([^s]+)', data)
    if match and '%' in match.group(1):
        return key, "complex string", urllib.parse.unquote(match.group(1))
    else:
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)


def map_nosj(data):

    if data.startswith('<< ') or data.endswith(' >>'):
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)

    newData = data[2:-2].strip()

    items = re.split(r',(?![^<>]*>)', newData)
    result = {}
    for item in items:
        key_match = re.match(r'([a-z+]):', item)
        if not key_match:
            sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
            sys.exit(66)
        keyName = key_match.group(1)

        # if key.startswith(' ') or key.endswith(' '):
        #     raise ValueError(f"Invalid map value: {data}")

        item = item[len(keyName) + 1:]

        value = parse_nosj(item, keyName)
        result[keyName] = value
    return data, "map", result


def parse_nosj(data, key):
    if data.startswith('f') and data.endswith('f'):
        return num_nosj(data, key)
    elif data.endswith('s'):
        return simple_string_nosj(data, key)
    elif '%' in data:
        return complex_string_nosj(data, key)
    elif data.startswith('<<') and data.endswith('>>'):
        return map_nosj(data)
    else:
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)


def print_parse_result(result):

    keyName = result[0]
    type = result[1]
    value = result[2]

    # for keyName, type, value in result.items():
    if isinstance(value, dict):
        list = [(k1, v1) for k1, v1 in value.items()]
        print("\nbegin-map")
        for k1, v1 in list:
            if v1[1] == "map":
                print(f"{k1} -- {v1[1]} -- ")
            print_parse_result(v1)
        print("end-map")
    else:
        print(f"{keyName} -- {type} -- {value}")

# print(parse_nosj("  <<x:  <<y:f1.23f>>  >>", ''))
# print(print_parse_result(map_nosj("<<x:<<y:f1.23f>>>>")))

if len(sys.argv) < 2:
    sys.stderr.write(f"ERROR -- Please provide a file name as an argument.\n")
    sys.exit(66)
file_path = sys.argv[1]
with open(file_path, "r") as file:
    list = [line for line in file.readlines() if line.strip()]
    print(list)
    data = []
    for d in list:

        if d.endswith('\n'):
            data.append(d[:-1].strip())
        else:
            data.append(d.strip())
    print(f"1{data}")
    try:
        for d in data:
            result = map_nosj(d)
            print_parse_result(result)
    except Exception as e:
        sys.stderr.write(f"ERROR -- {e}\n")
        sys.exit(66)
# def main():
#     if len(sys.argv) < 2:
#         sys.stderr.write(f"ERROR -- Please provide a file name as an argument.\n")
#         sys.exit(66)
#     file_path = sys.argv[1]
#     with open(file_path, "r") as file:
#         list = [line for line in file.readlines() if line.strip()]
#         print(list)
#         data = []
#         for d in list:
#
#             if d.endswith('\n'):
#                 data.append(d[:-1].strip())
#             else:
#                 data.append(d.strip())
#         print(f"1{data}")
#         try:
#             for d in data:
#                 result = map_nosj(d)
#                 print_parse_result(result)
#         except Exception as e:
#             sys.stderr.write(f"ERROR -- {e}\n")
#             sys.exit(66)
#
# if __name__ == "__main__":
#     main()