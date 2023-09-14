import json
def read_json(fname):
    result = []
    try:
        with open(f"./data/{fname}s.json") as jfile: #read old file if it exists
            result = json.load(jfile)
    except:
        with open(f"./data/{fname}s.json", "w") as jfile:    #create new file
            pass
    return result

def add_to_json(contents,outfile):
    saved_components = read_json(outfile) #read saved outfile.json
    saved_components.append(contents) #add newcontetes to file
    jsonObj = json.dumps(saved_components , indent=4)

    with open(f"./data/{outfile}s.json", "w") as iof:
        iof.writelines(jsonObj) #write to file

def add_attributes(att_name,  att_desc, att_val):
    attribute = {}
    attribute["name"]=att_name
    attribute["description"]=att_desc
    attribute["default_value"]=att_val
    return attribute

def get_components_by_name(fname):
    saved_comps= read_json(fname)
    results =[]
    for comp in saved_comps:
        results.append(comp[f"Name_of_{fname}"])
    return results

def get_all_components(component_names: list):
    results = []
    components_from_file =read_json("component")   #read components json file
    for comp in components_from_file:
        if comp["Name_of_component"] in component_names:
            results.append(comp)
        else:
            pass
    return results

def get_components_summary(compList):
    results = []
    
    components_from_file =read_json("component")   #read components json file
    for comp in components_from_file:
        comp_summary = {
            "Name_of_component":comp["Name_of_component"],
            "Names_of_component_atributes": []
        }
        if comp["Name_of_component"] in compList:
            for comp_att in comp["Component_attributes"]:
                comp_summary["Names_of_component_atributes"].append(comp_att["name"])
            results.append(comp_summary)
           
        else:
            pass
    print("Summary created")
    return results