import re
import urllib.parse
import sys


def num_nosj(data, key):

    match = re.match(r'f(-?\d+\.\d+)f',data)
    number = float(match.group(1))
    if match:
        if isinstance(number, float) and number.is_integer():
            number = int(number)
            return key, "num", number
        else:
            return key, "num", number
    else:
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)


def simple_string_nosj(data, key):
    match = re.match(r'([a-zA-Z0-9 \t]+)s',data)
    if match:
        return key, "string", match.group(1)
    else:
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)


def complex_string_nosj(data, key):
    match = re.match(r'([^s]+)', data)
    if match and '%' in match.group(1):
        return key, "string", urllib.parse.unquote(match.group(1))
    else:
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)


def map_nosj(data):

    if data.startswith('<< ') or data.endswith(' >>'):
        sys.stderr.write(f"ERROR -- Invalid input value: {data}\n")
        sys.exit(66)

    if data != "<<>>":

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
    else:
        return "empty map"


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
    if result != "empty map":
        keyName = result[0]
        type = result[1]
        value = result[2]

        # for keyName, type, value in result.items():
        if isinstance(value, dict):
            list = [(k1, v1) for k1, v1 in value.items()]
            sys.stdout.write("begin-map\n")
            for k1, v1 in list:
                if v1[1] == "map":
                    sys.stdout.write(f"{k1} -- {v1[1]} -- \n")
                print_parse_result(v1)
            sys.stdout.write("end-map\n")
        else:
            sys.stdout.write(f"{keyName} -- {type} -- {value}\n")
    else:
        sys.stdout.write("begin-map\n")
        sys.stdout.write("end-map\n")
def main():
    # if len(sys.argv) < 2:
    #     sys.stderr.write(f"ERROR -- Please provide a file name as an argument.\n")
    #     sys.exit(66)
    # file_path = sys.argv[1]
    # with open("./from-spec/valid/0002.input", "r") as file:
    with open(sys.argv[1], "r") as file:
        list = [line for line in file.readlines() if line.strip()]
        data = []
        for d in list:

            if d.endswith('\n'):
                data.append(d[:-1].strip())
            else:
                data.append(d.strip())
        try:
            for d in data:
                result = map_nosj(d)
                print_parse_result(result)
        except Exception as e:
            sys.stderr.write(f"ERROR -- {e}\n")
            sys.exit(66)

if __name__ == "__main__":
    main()