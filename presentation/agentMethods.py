import json



agent ={ "Name_of_agent": "Sheep",
        "Class_component_name": "energy_component",
        "Type_of_agent": "COMPLEX",
        "Components": []
      }

compx ={
        "Name_of_component": "EnergyComponent",
        "Component_attributes": [
            {
                "name": "speed",
                "description": "",
                "default_value": ""
            },
            {
                "name": "direction",
                "description": "",
                "default_value": ""
            }
        ]
    }

component = {
            "Name_of_component": "EnergyComponent",
            "Names_of_component_atributes": ["speed","direction"]
}



def add_component_to_agent(agent, component_name):
    agents=[]
    with open (".,/data/agents.json") as agents_file:
        agents = json.dumps(agents_file)
    print (agents)
    # with open('components.json') as f:
    #     components = f
    # for i in components:
    #     if i["Name_of_component"]==component_name:
    pass

def add_agent(agent):
    agents=[]
    with open("../data/agents.json") as agentsx:
          agents=agentsx
    if agent in agents:
        agents.remove(agent)
    agents.append[agent]
    
def create_component():
        
        pass

def create_component_summary(compx):
        summary ={}
        summary["Name_of_component"]=compx["Name_of_component"]
        atts = []
        for i in compx["Component_attributes"]:
                atts.append(i["name"])

        summary["Names_of_component_attributs"] = atts
        print (summary)


def create_json(contents,name):
     jsonObj = json.dumps(contents , indent=4)
     with open(f"{name}.json", "w") as outfile:
        outfile.write(jsonObj)

create_component_summary(compx)