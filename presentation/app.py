import flask
from flask import Flask, render_template, redirect, request, url_for, session
import helperMethods
import copy
app = Flask(__name__)
components = []
component ={"Name_of_component":"",
            "Component_attributes":[]
            }
attributes = []
agent = {
        "Name_of_agent": "",
        "Class_component_name":"",
        "Components":[],
        "Type_of_agent": "",
        }

comp_type = "SIMPLE"


################################################ Home ################################################
#Set up site navigation

@app.route("/", methods=["GET","POST"])
def home():
    if(request.method=="POST"): 
        match request.form['browse']:
            case "Components":
                return render_template("add_component_tab.html",
                                        all_components=helperMethods.get_components_by_name("component"))
            case "Agents":
                return render_template("add_agent_tab.html", 
                                       all_components=helperMethods.get_components_by_name("component"),
                                       all_agents = helperMethods.get_components_by_name("agent"))
            case "Systems":
                return render_template("add_system_tab.html",
                                       all_systems=helperMethods.get_components_by_name("system"),
                                       all_agents = helperMethods.get_components_by_name("agent"))
            case "Models":
                session.clear()
                return render_template("setup_model.html", model_type="")
            
            case "Execute":
                return render_template("execute_model_tab.html",
                                       input_params = session["input_parameters"] )
            
            case "Data Collector":
                return render_template("data_collector.html")
    else:
        return(render_template("add_component_tab.html"))
    

################################################ Components ################################################

#control components though the components window
@app.route("/component_tab", methods=["POST", "GET"])
def add_components():
        #get input from user
        component_name = request.form["Name_of_component"]
        component["Name_of_component"]=request.form["Name_of_component"]
        button_clicked = request.form["submit_results"]
        match (button_clicked):
            #if user wants to add attributes to a component
            case "Add attribute":
                attributes.append(helperMethods.add_attributes(
                request.form["att_name"],
                request.form["att_description"],
                request.form["att_default_value"]
                )
                )

            #if user wants to save/add component to component's list
            case "Add component":
                #add last attribute
                attributes.append(helperMethods.add_attributes(
                request.form["att_name"],
                request.form["att_description"],
                request.form["att_default_value"]
                )
                )
                all_atts = attributes
                component["Component_attributes"]=all_atts #assign attributes to components
                helperMethods.add_to_json(component, "component") #add component to json
                attributes.clear()
                component_name=""
                #call create components method here
                
            case _:
                component_to_edit = helperMethods.get_component(request.form["edit_component"])
                allAttsNames = []
                for att in component_to_edit[0]["Component_attributes"]:
                    allAttsNames.append(att["name"])
                # print(component_to_edit)
                return render_template("edit_component.html", 
                                       compName=request.form["edit_component"], 
                                       all_components=allAttsNames, all_agents = helperMethods.get_components_by_name("agent"))
        return render_template("add_component_tab.html", 
                               compName=component_name, all_components=helperMethods.get_components_by_name("component"), 
                               all_agents = helperMethods.get_components_by_name("agent"))



############################################### Edit Component ###################################
# @app.route("/edit_component", methods=["POST"])
# def edit_component():
#     #get component to be edited
#     action = request.form["edit_component"]
#     match(action):
#         case("edit_component"):
#             component_to_edit = helperMethods.get_component(request.form["edit_component"])
#             allAttsNames = []
#             for att in component_to_edit[0]["Component_attributes"]:
#                 allAttsNames.append(att["name"])
#             print(component_to_edit)
#             return render_template("edit_component.html", compName=request.form["edit_component"], all_components=allAttsNames, all_agents = helperMethods.get_components_by_name("agent"))
#     return render_template("add_component_tab.html", compName=request.form["edit_component"], all_components=allAttsNames, all_agents = helperMethods.get_components_by_name("agent"))



############################################################AGENT ROUTES#############################################################

#control agents through the agents tab
@app.route("/agents", methods=["POST", "GET"])
def add_agent():
    agent_action = request.form["add_to_agent"]
    global comp_type
    name=request.form["agent_name"]
    match agent_action:
        case "Add Agent":
            agent["Name_of_agent"] = name
            agent["Type_of_agent"] = comp_type
            agent["Class_component_name"] = request.form["agent_class_componet_name"]
            components_to_add_by_name = (request.form.getlist("component_to_add")) #get  list of component the user wants to add to their agent
            components_summary = helperMethods.get_components_summary(components_to_add_by_name)#get component summary list
            agent["Components"].append(components_summary)
            helperMethods.add_to_json(agent,"agent")
            agent["Components"].clear()
            name=""
            #clear screen

        case "Simple":
            comp_type = "SIMPLE"
            # print(agent_action)

        case "Complex":
            comp_type = "COMPLEX"
            # print(agent_action)


    agents = helperMethods.read_json("agent")
    return render_template("add_agent_tab.html", 
                           agent_name=name,all_components=helperMethods.get_components_by_name("component"), 
                           all_agents=helperMethods.get_components_by_name("agent"), agent_type=comp_type)

######################################## Data Collector Tab #######################################################################################################################################################


@app.route("/dataCollector", methods=["POST","GET"])
def data_collector():
    
    # Get the data collector input value
    data_collector_input = request.form["dataCollector_inp1"]

    # Get the selected agents from the radio buttons
    selected_agents = request.form.getlist("selected_agents")

    # Perform further processing with the selected agents
    # For now, we'll just print them
    print("Data Collector Input:", data_collector_input)
    print("Selected Agents:", selected_agents)

    # You can add additional logic or processing here

    return render_template("datacollector.html", compName=data_collector_input, complex_agents=["Agent1", "Agent2", "Agent3"], all_components=["Component1", "Component2", "Component3"])







######################################## Systems Tab #######################################################################################################################################################
@app.route("/systems", methods=["POST","GET"])
def add_system():
    system = {
        "Name_of_system":"",
        "code": ""
    }
    dummyCode = ""
    if request.method=="POST":
        name=request.form["sys_name"]
        action=request.form["submit_code"]
        match(action):
            case "Create system":
                system["Name_of_system"] = request.form["sys_name"]
                # print ("system created")
                dummyCode = ("#dummy code will go here")
            case "Save system":
                #Write system to json
                system["code"]=request.form["editor_code"]
                
                helperMethods.add_to_json(system, "system")
                # print("system saved")
            case "Run":
                #print(dummyCode)
                return render_template("add_system_tab.html",
                           all_systems=helperMethods.get_components_by_name("system"), 
                           sys_name=name, sys_code =dummyCode)


###################################################### Model Routes ############################################3
@app.route("/model_type", methods=["GET", "POST"])
def add_model_type():
    if request.method=="POST":
        model_type = request.form["model_type"]
        chosen_model_type = model_type
        session["model_type"] = model_type

        if "input_parameters" not in session:
            session['input_parameters'] = []

        #print (chosen_model_type)
        return render_template("add_model_tab.html", view=1,
                               model_type=chosen_model_type,
                               input_params = session["input_parameters"])
    else:
        return render_template("setup_model.html")
    

@app.route("/model", methods=["GET", "POST"])
def add_model():

    # Logic
    # select type of model you are dealing with
    # enable input parameters button
    ##Input parameters
    # select add input parameters button
    # enter input parameters details
    # get input parameters and save them in input_parameters list
    # select save input parameters
    # save input_parameters list
    # enable class components button
    ##Class components
    # select class components button
    # add class components details (according to SIMPLE or COMPLEX agent and input parameters)
    # select add class component datails
    # add class components details
    # select save class components
    # enable add agents button
    ##Add agents
    # select agents from all agents list
    # get agents selected
    # save selected agents to agents list
    # select number of agents from input parameters
    # select save agent
    # add agent to agents list
    # save environment as GRIDWORLD if  model is COMPLEX, save it as DEFAULT if model is SIMPLE
    # enable add systems button
    ##Add systems
    # select system name from all systems list
    # add system ID
    # select system variables from input parameters list
    # select add system
    # select system name from all systems list
    # add system ID
    # select system variables from input parameters list
    # select save systems
    # save systems to all systems
    # save input parameters, class components, agents and systems to the models json file


    #Setup session
    new_model_name=""
    action = request.form["submit_action"]

    if "model_name" not in session:
        session['model_name'] = ""

    if "input_parameters" not in session:
        session['input_parameters'] = []


    if "model_agent" not in session:
        session["model_agent"] =  {
                "Name_of_agent": "",
                "number_of_agents": ""
            }
        
    if "model_agents" not in session:
        session['model_agents'] = []
    
    if "model_system" not in session:
        session["model_system"] = {
                "Name_of_system": "",
                "system_id": "",
                "system_variables": []
            }
        
    if "model_systems" not in session:
        session["model_systems"] = []
          
    if (session["model_type"] == "COMPLEX"):
        if "class_component" not in session:
            session['class_component'] = {
                "Name_of_agent": "",
                "Name_of_component":"",
                "component_atributes_names": []
            }

        if "class_components" not in session:
            session["class_components"] = []

    new_param = {
        "Name": "",
        "dataType": ""
    }

    chosen_model_type=session["model_type"]
    all_agents = helperMethods.get_components_by_name("agent")
    all_components = helperMethods.get_components_by_name("component")
    all_current_systems = helperMethods.get_components_by_name("system")
    agent_to_add_to_model=""
    system_to_add_to_model=""
    #create agent and component addition option

    state = (request.form.getlist("state"))


    if ((action in all_agents) and chosen_model_type=="COMPLEX"):
        state = (request.form.getlist("state"))

        if state[0]=="2":
            action="Add class component Name_of_agent"

        elif state[0]=="3":
            print("Agent chosen to be added to model is "+ action)
            print(f"Current agents are {session['model_agents']}")
            agent_to_add_to_model = action
            action="Add model agent"

    elif ((action in all_components) and session["model_type"]=="COMPLEX"):
        action="Add class component Name_of_component"
    elif (action in all_current_systems):
        system_to_add_to_model = action
        action = "Add system to model"
   

    match(action):
        case "Add parameter":
            new_param["Name"]=request.form["name"]
            new_param["dataType"] = request.form["data_type"]
            saved_input_params = copy.deepcopy(session["input_parameters"])

            if( new_param not in saved_input_params):
                saved_input_params.append(new_param)
                session["input_parameters"] = saved_input_params

            session["model_name"] = request.form["model_name"]
            return render_template("add_model_tab.html",
                                   view=1,
                                   input_params = session["input_parameters"],
                                   model_name=session["model_name"],
                                   model_type=session["model_type"])
        
        case "Save input parameters":
            new_param["Name"]=request.form["name"]
            new_param["dataType"] = request.form["data_type"]
            saved_input_params = copy.deepcopy(session["input_parameters"])

            if( new_param not in saved_input_params):
                saved_input_params.append(new_param)
                session["input_parameters"] = saved_input_params
            
            session["model_name"] = request.form["model_name"]
            agents = helperMethods.get_agents_by_type(chosen_model_type)
            components = helperMethods.get_components_by_name("component")
            return render_template("add_model_tab.html",
                                   view=2, 
                                   model_type=session["model_type"],
                                   model_name = session["model_name"],
                                   all_class_components = session["class_components"],
                                   all_components=components, 
                                   all_agents = agents,
                                   input_params = session["input_parameters"])
        
        case "Add class component Name_of_agent":
            current_class_component = copy.deepcopy(session["class_component"])
            current_class_component["Name_of_agent"] = request.form["submit_action"]
            print(current_class_component)
            session["class_component"] = current_class_component
            session["model_name"]  = request.form["model_name"]

                    
            return render_template("add_model_tab.html",
                                   view=2, 
                                   model_type=session["model_type"], 
                                   model_name = session["model_name"], 
                                   all_class_components = session['class_components'],
                                   all_components=all_components, 
                                   all_agents = helperMethods.get_agents_by_type(chosen_model_type), 
                                   input_params=session["input_parameters"])

        case "Add class component Name_of_component":
            current_class_component = copy.deepcopy(session["class_component"])
            current_class_component["Name_of_component"]=request.form["submit_action"]
            print(current_class_component)
            session["class_component"] = current_class_component
            session['model_name'] = request.form["model_name"]
            summary = helperMethods.get_components_summary([current_class_component["Name_of_component"]])

            return render_template("add_model_tab.html",
                                   view=2, 
                                   model_type=session["model_type"], 
                                   model_name = session["model_name"],
                                   all_class_components = session['class_components'],
                                   all_components=all_components, 
                                   all_agents = helperMethods.get_agents_by_type(chosen_model_type), 
                                   input_params=session['input_parameters'],
                                   error_message=f"Select {len(summary[0]['Names_of_component_atributes'])} parameter(s)")

        case "Add class component":
            current_class_component = copy.deepcopy(session["class_component"])
            print(f"Working with current class component {current_class_component}")
            session["model_name"] = request.form["model_name"]
            selected_params = request.form.getlist("params_to_add")
            session["class_component"]
            class_component_summary = helperMethods.get_components_summary([current_class_component["Name_of_component"]])
            att_summary = class_component_summary[0]["Names_of_component_atributes"]
            params_summary = helperMethods.param_summary(selected_params)

            if(len(selected_params)==len(att_summary)):
                current_class_component["component_atributes_names"] = params_summary
                print(current_class_component)
                saved_class_components = copy.deepcopy(session['class_components'])
                if( current_class_component not in saved_class_components):
                    saved_class_components.append(current_class_component)

                session['class_components'] = saved_class_components

                print (f"Saved class components in session are {session['class_components']}")

                return render_template("add_model_tab.html",
                                       view=2, 
                                       model_type=session["model_type"], 
                                       model_name = session['model_name'],
                                       all_class_components = session["class_components"],
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_agents_by_type(chosen_model_type), 
                                       input_params=session['input_parameters'])
            else:
                return render_template("add_model_tab.html",view=2, 
                                       mmodel_type=session["model_type"], 
                                       model_name = new_model_name, 
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_agents_by_type(chosen_model_type),
                                       input_params=session['input_parameters'],
                                       error_message=f"Pick {len(att_summary)} parameter(s)")
            
        case "Save class components":
            current_class_component = copy.deepcopy(session["class_component"])
            print(f"Working with current class component {current_class_component}")
            session["model_name"] = request.form["model_name"]
            selected_params = request.form.getlist("params_to_add")
            session["class_component"]
            class_component_summary = helperMethods.get_components_summary([current_class_component["Name_of_component"]])
            att_summary = class_component_summary[0]["Names_of_component_atributes"]
            params_summary = helperMethods.param_summary(selected_params)

            if(len(selected_params)==len(att_summary)):
                current_class_component["component_atributes_names"] = params_summary
                print(current_class_component)
                saved_class_components = copy.deepcopy(session['class_components'])
                if( current_class_component not in saved_class_components):
                    saved_class_components.append(current_class_component)

                session['class_components'] = saved_class_components

                print (f"Saved class components in session are {session['class_components']}")

                return render_template("add_model_tab.html",
                                       view=3, 
                                       model_type=session["model_type"], 
                                       model_name = session['model_name'],
                                       all_class_components = session["class_components"],
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_components_by_name("agent"), 
                                       input_params=session['input_parameters'])
            else:
                return render_template("add_model_tab.html",view=2, 
                                       mmodel_type=session["model_type"], 
                                       model_name = new_model_name, 
                                       all_components=all_components, 
                                       all_agents = helperMethods.get_agents_by_type(chosen_model_type),
                                       input_params=session['input_parameters'],
                                       error_message=f"Pick {len(att_summary)} parameter(s)")
 
            
            
        case "Add model agent":

            session["model_name"] = request.form["model_name"]
            print("preparing to add agent to model")
            current_model_agent = session["model_agent"]
            current_model_agent["Name_of_agent"] = agent_to_add_to_model
            session["model_agent"] = current_model_agent
            print(f"current session agent is {current_model_agent}")
            current_model_agents = copy.deepcopy(session["model_agents"])
            return render_template("add_model_tab.html",
                                   view=3,
                                   all_agents = helperMethods.get_components_by_name("agent"),
                                   input_params = session["input_parameters"],
                                   model_name = session["model_name"],
                                   current_model_agents = current_model_agents
                                   )
        
        case "Add agent to model":
            session['model_name'] = request.form['model_name']
            chosen_input_param = request.form["params_to_add"]
            params_summary = helperMethods.param_summary([chosen_input_param])
            print(f"Param to be added to session agent {params_summary}")

            current_model_agent = copy.deepcopy(session["model_agent"])
            current_model_agent["number_of_agents"]= params_summary[0]
            print(f"current model agent {current_model_agent}")

            current_model_agents = copy.deepcopy(session["model_agents"])
            
            if current_model_agent not in current_model_agents:
                current_model_agents.append(current_model_agent)
                session['model_agents'] = current_model_agents
            print(f"current saved model agents {current_model_agents}")
            # current_model_agent["number_of_agents"] = chosen_input_param[]
            return render_template("add_model_tab.html",
                                   view=3, 
                                   model_type=session["model_type"], 
                                   model_name = session['model_name'],
                                   model_agent = current_model_agent,
                                   current_model_agents = current_model_agents,
                                   all_agents = helperMethods.get_components_by_name("agent"), 
                                   input_params=session['input_parameters']
                                   )
        
        case "Save agents":
            session['model_name'] = request.form['model_name']
            chosen_input_param = request.form["params_to_add"]
            params_summary = helperMethods.param_summary([chosen_input_param])
            print(f"Param to be added to session agent {params_summary}")

            current_model_agent = copy.deepcopy(session["model_agent"])
            current_model_agent["number_of_agents"]= params_summary[0]
            print(f"current model agent {current_model_agent}")

            current_model_agents = copy.deepcopy(session["model_agents"])
            
            if current_model_agent not in current_model_agents:
                current_model_agents.append(current_model_agent)
                session['model_agents'] = current_model_agents
            print(f"current saved model agents {current_model_agents}")
            # current_model_agent["number_of_agents"] = chosen_input_param[]
            return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = session['model_name'],
                                   model_agent = current_model_agent,
                                   current_model_agents = current_model_agents,
                                   all_systems = helperMethods.get_components_by_name("system"),
                                   saved_systems = session["model_systems"],
                                   input_params=session['input_parameters']
                                   )
        
        case "Add system to model":
            session["model_name"] = request.form["model_name"]
            system_id = request.form["system_id"]
            current_model_system = copy.deepcopy(session["model_system"])
            current_model_system["Name_of_system"] = system_to_add_to_model
            current_model_system["system_id"] = system_id
            print (current_model_system)
            session["model_system"] = current_model_system
            return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = session['model_name'], 
                                   all_systems=all_current_systems, 
                                   system_id = current_model_system["system_id"],
                                   saved_systems = session["model_systems"],
                                   input_params=session["input_parameters"])
        
        case "Save System":
            if "system_ids" not in session:
                session["system_ids"] = []

            session["model_name"] = request.form["model_name"]
            system_id = request.form["system_id"]
            current_model_system = copy.deepcopy(session["model_system"])
            input_params = request.form.getlist("params_to_add")
            params_summary = helperMethods.param_summary(input_params)

            current_model_system["system_id"] = system_id
            current_model_system["system_variables"] = params_summary

            current_model_systems = copy.deepcopy(session["model_systems"])
            current_system_ids = copy.deepcopy(session['system_ids'])
            if current_model_system["system_id"] not in current_system_ids:
                print(current_system_ids)
                current_model_systems.append(current_model_system)
                current_system_ids.append(system_id)
                session["system_ids"] = current_system_ids
                session["model_systems"] = current_model_systems
                return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = session["model_name"],
                                   all_systems=all_current_systems, 
                                   saved_systems = session["model_systems"],
                                   input_params=session["input_parameters"])
            
            else:
               return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = session["model_name"],
                                   all_systems=all_current_systems, 
                                   saved_systems = current_model_systems,
                                   input_params=session["input_parameters"],
                                   error_message = f"System ID {system_id} already exists. Enter a new one"
                                   )

        
        case "Save systems and execute model":
            if "system_ids" not in session:
                session["system_ids"] = []

            session["model_name"] = request.form["model_name"]
            system_id = request.form["system_id"]
            current_model_system = copy.deepcopy(session["model_system"])
            input_params = request.form.getlist("params_to_add")
            params_summary = helperMethods.param_summary(input_params)

            current_model_system["system_id"] = system_id
            current_model_system["system_variables"] = params_summary

            current_model_systems = copy.deepcopy(session["model_systems"])
            current_system_ids = copy.deepcopy(session['system_ids'])
            if current_model_system["system_id"] not in current_system_ids:
                print(current_system_ids)
                current_model_systems.append(current_model_system)
                current_system_ids.append(system_id)
                session["system_ids"] = current_system_ids
                session["model_systems"] = current_model_systems
                complete_model = [
                {
                    "name_model":""
                },
                {
                    "input_parameters": []
                },
                {
                    "class_components": []
                },
                {
                    "Agents" : []
                },
                {
                    "environment": ""
                },
                {
                    "systems": []
                }
                ]
                # for i in session:
                #     print(i)
                for i in range(len(complete_model)):
                    match i:
                        case 0:
                            complete_model[0] = {
                                "name_model":session["model_name"]
                            }
                        case 1:
                            complete_model[1] = {
                                "input_parameters": session['input_parameters']
                            }
                        case 2:
                            complete_model[2] = {
                                "class_components" : session["class_components"]
                            }
                        case 3:
                             complete_model[3] = {
                                "Agents" : session["model_agents"]
                            }
                        case 4:
                            if session["model_type"] == "COMPLEX":
                                complete_model[4] = {
                                    "environment" : "GRIDWORLD"
                                }
                            else:
                                complete_model[4] = {
                                    "environment" : "SIMPLE"
                                }
                        case 5:
                            complete_model[5] = {
                                "systems": session["model_systems"]
                            }
                                

                helperMethods.add_to_json(complete_model, "model")
                
                    
                return render_template("execute_model_tab.html",
                                    input_params = session["input_parameters"] )
            
            else:
               return render_template("add_model_tab.html",
                                   view=4, 
                                   model_type=session["model_type"], 
                                   model_name = session["model_name"],
                                   all_systems=all_current_systems, 
                                   saved_systems = current_model_systems,
                                   input_params=session["input_parameters"],
                                   error_message = f"System ID {system_id} already exists. Enter a new one"
                                   )


    return render_template("add_model_tab.html",
                           view=1,
                           model_type=session["model_type"]
                           )

    
    # print(action)
    # match(action):
    #     #if user wants to add a parameter
    #     case ("Add input parameters"):
    #         view_section = "input parameters"     #change view to show only input parameter fields
        
    #     case ("Add class components"):
    #         view_section = "class components"

    #     case ("Add parameter"):
    #         new_param["Name"]=request.form["name"]
    #         new_param["dataType"] = request.form["data_type"]
    #         print(new_param)
    #         input_parameters.append(new_param)
    #         new_model_name = request.form["model_name"]
    #         return render_template("add_model_tab.html", model_name=new_model_name, view=view_section)
        
    #     case ("Save input parameters"):
    #         new_param["Name"]=request.form["name"]
    #         new_param["dataType"] = request.form["data_type"]
    #         print(new_param)
    #         input_parameters.append(new_param)
    #         model_input_parameters = modelhelperMethods.add_input_parameters(input_parameters)
    #         helperMethods.add_to_json(model_input_parameters, "model")
    #         input_parameters.clear()
    #         new_model_name=""
    #         return render_template("add_model_tab.html", model_name=new_model_name, view=view_section)




# @app.route("/model_setup", methods=["GET", "POST"])
# def model_setup():
#         print("in model setup")
#         if request.form["submit_action"]: #if user wants to move into the first step and add input parameters
#             print ("got into the model type")     
#             return render_template("add_model_tab.html", step=1, view=1)
#         else:
#             return render_template("add_model_tab.html", step=1, view=1)


# def run_me():
#         app.run(host='0.0.0.0', debug=True)

if __name__ == "__main__":
    app.secret_key="be gay, do crime"
    app.run(host='0.0.0.0', debug=True)