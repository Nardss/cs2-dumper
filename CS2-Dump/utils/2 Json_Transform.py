import json
import os

# Definindo as estruturas com os seus respectivos campos
offsets = {
    "EntityOffsets": [
        "m_bPawnIsAlive", "m_hPlayerPawn", "m_iszPlayerName", "m_flGravityScale"
    ],
    "PawnOffsets": [
        "m_pMovementServices", "m_pWeaponServices", "m_pBulletServices", "m_pCameraServices",
        "m_pViewModelServices", "m_pClippingWeapon", "m_hViewModel", "m_nCrouchState",
        "m_bIsScoped", "m_bIsDefusing", "m_totalHitsOnServer", "m_vOldOrigin",
        "m_ArmorValue", "m_iMaxHealth", "m_iHealth", "m_pGameSceneNode", "m_modelState",
        "m_vecOrigin", "m_hOwnerEntity", "m_angEyeAngles", "m_vecLastClipCameraPos",
        "m_iShotsFired", "m_flFlashMaxAlpha", "m_flFlashDuration", "m_aimPunchAngle",
        "m_aimPunchCache", "m_iIDEntIndex", "m_iTeamNum", "m_iDesiredFOV", "m_iFOVStart",
        "m_entitySpottedState", "m_bSpottedByMask", "m_vecAbsVelocity", "m_bIsBuyMenuOpen"
    ],
    "GlobalVarOffsets": [
        "RealTime", "FrameCount", "MaxClients", "IntervalPerTick", "CurrentTime", 
        "CurrentTime2", "TickCount", "IntervalPerTick2", "CurrentNetchan", "CurrentMap", 
        "CurrentMapName"
    ],
    "PlayerControllerOffsets": [
        "m_hPawn", "m_pObserverServices", "m_hObserverTarget", "m_hController", "m_iPawnArmor", 
        "m_bPawnHasDefuser", "m_bPawnHasHelmet"
    ],
    "EconEntityOffsets": [
        "m_AttributeManager", "m_nFallbackPaintKit", "m_nFallbackSeed", "m_flFallbackWear", 
        "m_nFallbackStatTrak", "m_szCustomName", "m_iEntityQuality", "m_iItemIDHigh"
    ],
    "WeaponBaseOffsets": [
        "WeaponDataPTR", "szName", "Clip1", "m_iMaxClip1", "m_flCycleTime", "m_flPenetration", 
        "m_WeaponType", "m_flInaccuracyMove", "m_bInReload", "WeaponSize", "m_hActiveWeapon", 
        "m_Item", "m_iItemDefinitionIndex", "m_MeshGroupMask"
    ],
    "C4Offsets": [
        "m_bBeingDefused", "m_flDefuseCountDown", "m_nBombSite"
    ],
    "InGameMoneyServicesOffsets": [
        "m_pInGameMoneyServices", "m_iAccount", "m_iTotalCashSpent", "m_iCashSpentThisRound"
    ],
    "SmokeGrenadeProjectileOffsets": [
        "m_nSmokeEffectTickBegin", "m_bDidSmokeEffect", "m_nRandomSeed", "m_vSmokeColor", 
        "m_vSmokeDetonationPos", "m_VoxelFrameData", "m_bSmokeVolumeDataReceived", 
        "m_bSmokeEffectSpawned"
    ],
    "GeneralOffsets": [
        "dwEntityList", "dwLocalPlayerController", "dwGlobalVars", "dwViewAngles",
        "dwLocalPlayerPawn", "dwWindowHeight", "dwWindowWidth", "dwPlantedC4","dwViewMatrix"
    ]
}

# Lista de caminhos dos arquivos JSON
json_files = [
        r"C:\Dumper\Second Dump\client.dll.json",
        r"C:\Dumper\Second Dump\buttons.hpp.json",
        r"C:\Dumper\Second Dump\offsets.hpp.json"
    ]

# Função para carregar e atualizar os grupos no JSON
def update_groups(json_data, offsets):
    new_json_data = {}
    for key, fields in offsets.items():
        new_group = {"name": key, "constants": []}
        for json_key, values in json_data.items():
            for value in values:
                if value["name"] in fields:
                    new_group["constants"].append(value)
        if new_group["constants"]:
            new_json_data[key] = new_group
    return new_json_data

# Iterar sobre os arquivos JSON e processar cada um
output_directory = r"C:\Dumper\Transformed Json"

# Verifica se o diretório de saída existe; se não, cria-o
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Itera sobre os arquivos JSON originais
for file_path in json_files:
    with open(file_path, 'r') as f:
        json_data = json.load(f)
    
    # Atualiza os grupos no JSON
    updated_json_data = update_groups(json_data, offsets)

    # Obtém o nome do arquivo sem extensão para usar como base no nome do arquivo de saída
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Caminho completo para o arquivo de saída no diretório especificado
    output_file = os.path.join(output_directory, f"{file_name}_updated.json")

    # Salva o JSON modificado no novo caminho de saída
    with open(output_file, 'w') as f:
        json.dump(updated_json_data, f, indent=4)
    
    print(f"JSON atualizado e salvo em {output_file}")
