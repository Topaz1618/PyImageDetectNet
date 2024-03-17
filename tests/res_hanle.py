from enum import Enum

class MaterialType(Enum):
    ID_CARD = "身份证"
    LAND_MAP = "宗地图"
    HOUSEHOLD_REGISTER = "户口本"
    HOUSE_FLOOR_PLAN = "房屋平面图"
    REAL_ESTATE_APPLICATION = "不动产申请表"


def handle_material(file_data):
    material_type = file_data.get("material_type")
    if material_type in [m.value for m in MaterialType]:
        return material_type

def res_dict(data):
    if data and isinstance(data, dict):
        l = list()
        for filename, file_data in data.items():
            if not isinstance(file_data, dict):
                continue

            material_type = handle_material(file_data)
            if material_type:
                l.append({material_type: filename})
    print(l)


data = {'17 房屋平面图.pdf': {'file_type': 'PDF', 'material_type': '房屋平面图'},
 '15 不动产调查登记申请表.pdf': {'file_type': 'PDF', 'material_type': '不动产申请表'},
 '05 户口薄.pdf': {'file_type': 'PDF', 'material_type': 'Unknown'},
 '16 宗地图.pdf': {'file_type': 'PDF', 'material_type': 'Unknown'},
 '03 权利人身份证.pdf': {'file_type': 'PDF', 'material_type': 'Unknown'}
 }

res_dict(data)