import requests
import json

def get_visors():
    index = requests.get("https://hi.cylix.guide/index.json").json()
    visors = [i[1] for i in index["manifest"] if i[1]["type"] == "ArmorVisor"]
    visor_things = []
    for visor in visors:
        visor_data = requests.get(f"https://hi.cylix.guide/item/{visor['name']}/{visor['res']}.json").json()
        rough = visor_data["Roughness"]
        if rough == -1:
            rough = 4
        visor_data = {
            "name": visor_data["CommonData"]["Title"],
            "pattern": visor_data["VisorId"]["m_identifier"],
            "color": visor_data["ColorVariant"]["m_identifier"],
            "Roughness": rough,
            "Emissive": visor_data["Emissive"],
        }
        visor_things.append(visor_data)
    with open("visors.json", "w") as file:
        json.dump(visor_things, file, indent=4)
    

def process_visors():
    with open("visors.json", "r") as file:
        visors = json.load(file)
    with open("visor_data.json", "r") as file:
        visor_thing = json.load(file)
    all_visors = {}
    for visor in visors:
        color = visor_thing["colors"].get(str(visor["color"]))
        if color is None:
            continue
        visor_data = visor_thing["patterns"][str(visor["pattern"])]
        layer = {
            "disabled": False,
            "gradient_transform": visor_data["color_and_roughness_transform"],
            "normal_transform": visor_data["normal_texture_transform"],
            "gradient_bitmap": visor_data["color_gradient_map"],
            "normal_bitmap": visor_data["normal_detail_map"],
            "roughness": visor["Roughness"],
            "roughness_white": visor_data["roughness_white"],
            "roughness_black": visor_data["roughness_black"],
            "metallic": visor_data["metallic"],
            "emissive_amount": visor["Emissive"],
            "top_color": color["top_color"],
            "mid_color": color["mid_color"],
            "bot_color": color["bot_color"],
            "scratch_roughness": visor_data["scratch_roughness"],
            "scratch_metallic": visor_data["scratch_metallic"],
            "scratch_color": visor_data["scratch_color"],
        }
        all_visors[visor["name"]] = layer
    with open("all_visors.json", "w") as file:
        json.dump(all_visors, file, indent=4)
        
if __name__ == "__main__":
    get_visors()
    process_visors()
