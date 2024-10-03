import re
import json

def parse_hpp_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

            # Regex patterns for namespace, enum, and constant extraction
            namespace_pattern = r'namespace\s+(\w+)\s*\{([^{}]+)\}'
            enum_pattern = r'enum\s+class\s+(\w+)\s*\{([^{}]+)\};'
            constant_pattern = r'constexpr\s+std::ptrdiff_t\s+(\w+)\s+=\s+0x([0-9a-fA-F]+);'

            namespaces = []

            # Extract namespaces
            for match in re.finditer(namespace_pattern, file_content):
                ns_name = match.group(1).strip()
                ns_body = match.group(2).strip()

                enums = []
                constants = []

                # Extract enums
                for enum_match in re.finditer(enum_pattern, ns_body):
                    enum_name = enum_match.group(1).strip()
                    enum_members = enum_match.group(2).strip().split(',')
                    enum_values = {member.split('=')[0].strip(): int(member.split('=')[1].strip(), 16) for member in enum_members}
                    enums.append({"name": enum_name, "values": enum_values})

                # Extract constants
                for const_match in re.finditer(constant_pattern, ns_body):
                    const_name = const_match.group(1).strip()
                    const_value = const_match.group(2).strip()  # Mantém o valor como string hexadecimal
                    constants.append({"name": const_name, "value": "0x" + const_value})  # Adiciona prefixo "0x"

                namespaces.append({
                    "name": ns_name,
                    "enums": enums,
                    "constants": constants
                })

            return namespaces

    except IOError:
        print(f"Error: File '{file_path}' not found or could not be read.")
        return None
    except Exception as e:
        print(f"Error parsing file: {e}")
        return None

def group_constants_by_namespace(data):
    grouped_data = {}
    
    for item in data:
        ns_name = item['name']
        constants = item['constants']
        
        if ns_name not in grouped_data:
            grouped_data[ns_name] = constants
        else:
            grouped_data[ns_name].extend(constants)
    
    return grouped_data

def convert_to_json(data):
    return json.dumps(data, indent=4)

def save_to_json(data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"Data saved to '{output_file}' successfully.")
    except Exception as e:
        print(f"Error saving data to '{output_file}': {e}")

if __name__ == "__main__":
    # Define os caminhos dos arquivos adicionais
    file_paths = [
        r"C:\Dumper\First Dump\client.dll.hpp",
        r"C:\Dumper\First Dump\buttons.hpp",
        r"C:\Dumper\First Dump\offsets.hpp"
    ]

    output_files = [
        r"C:\Dumper\Second Dump\client.dll.json",
        r"C:\Dumper\Second Dump\buttons.hpp.json",
        r"C:\Dumper\Second Dump\offsets.hpp.json"
    ]

    for idx, file_path in enumerate(file_paths):
        parsed_data = parse_hpp_file(file_path)
        
        if parsed_data:
            grouped_constants = group_constants_by_namespace(parsed_data)
            save_to_json(grouped_constants, output_files[idx])
