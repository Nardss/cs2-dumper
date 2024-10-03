import json

# Função para carregar o JSON de um arquivo
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Função para gerar a atribuição C++ com base no JSON
def generate_cpp_assignments(json_data):
    assignments = []
    for key, group in json_data.items():
        struct_name = key.replace("Offsets", "")
        for constant in group["constants"]:
            assignment = f'Offset::{struct_name}.{constant["name"]} = findValueByName(j, "{group["name"]}", "{constant["name"]}");'
            assignments.append(assignment)
    return assignments

# Lista de caminhos dos arquivos JSON atualizados
json_files = [
    r"C:\Dumper\Transformed Json\offsets.hpp_updated.json",
    r"C:\Dumper\Transformed Json\client.dll_updated.json",
    r"C:\Dumper\Transformed Json\buttons.hpp_updated.json"
]

# Função para mesclar múltiplos arquivos JSON em um único dicionário
def merge_json_files(json_files):
    merged_data = {}
    for file_path in json_files:
        data = load_json(file_path)
        merged_data.update(data)
    return merged_data

# Mesclar os arquivos JSON
merged_json_data = merge_json_files(json_files)

# Gerar as atribuições C++ com base no JSON unificado
assignments = generate_cpp_assignments(merged_json_data)

# Salvar o JSON unificado em um arquivo
merged_json_file = r"final.json"
with open(merged_json_file, 'w') as f:
    json.dump(merged_json_data, f, indent=4)

print(f"Dados JSON unificados salvos em {merged_json_file}")
