# import yaml
# import pandas as pd

# def process_multiline_answer(str_data):
#     str_list = [x.strip() for x in str_data.replace('*', '').split('\n')]
#     str_list = list(filter(None, str_list))
#     return '\n'.join(str_list)

# def process_multiline_example(str_data):
#     str_list = [x.strip() for x in str_data.replace('*', '').split('\n')]
#     str_list = list(filter(None, str_list))
#     return '\n- '.join(str_list)

# class literal_unicode(str):
#         pass

# def literal_unicode_representer(dumper, data):
#     return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


# # yaml.add_representer(folded_unicode, folded_unicode_representer)
# yaml.add_representer(literal_unicode, literal_unicode_representer)

# def create_data_files(nlu_data, rules_data, stories_data, domain_data):
#     with open("./data/nlu.yml", "w") as outfile:
#         yaml.dump(
#             nlu_data,
#             outfile,
#             default_flow_style=False,
#             encoding="utf-8",
#             allow_unicode=True,
#             sort_keys=False
#         )

#     with open("./data/rules.yml", "w") as outfile:
#         yaml.safe_dump(
#             rules_data,
#             outfile,
#             default_flow_style=False,
#             encoding="utf-8",
#             allow_unicode=True,
#             sort_keys=False
#         )
#     with open("./data/stories.yml", "w") as outfile:
#         yaml.safe_dump(
#             stories_data,
#             outfile,
#             default_flow_style=False,
#             encoding="utf-8",
#             allow_unicode=True,
#             sort_keys=False
#         )
#     with open("./domain.yml", "w") as outfile:
#         yaml.dump(
#             domain_data,
#             outfile,
#             default_flow_style=False,
#             encoding="utf-8",
#             allow_unicode=True,
#             sort_keys=False,
#         )
        
# def create_new_files(df):
    
    
#     # df = df[:6]
    
#     # NLU file
#     with open('./data/nlu.yml') as f:
#         nlu_dict = yaml.full_load(f)
    
#         nlu_dt = nlu_dict["nlu"]

#         # Extract 'intent' key values containing "ques_"

#         filtered_nlu = [entry for entry in nlu_dt if "ques_" not in entry["intent"]]

#         result_list = []

#         for index,row in df.iterrows():
#             ques = row["Questions"].strip("'").strip('"').strip()
#             ques = process_multiline_example(ques)
#             result_dict = {
#                         'intent': f"ques_{int(index)}",
#                         'examples': f"- {ques}\n"
#                     }
#             #print((result_dict))

#             result_list.append(result_dict)

#         filtered_nlu += result_list

#         # Applying the function to examples values
#         for item in filtered_nlu:
#             examples = item.get('examples')
#             if examples:
#                 examples = literal_unicode(examples)
#                 item['examples'] = examples

#         nlu_data = {"version": "3.0", "nlu": []}
#         nlu_dict["nlu"] = filtered_nlu
    
#     # Domain file
#     with open('./domain.yml') as f:
#         domain_dict = yaml.full_load(f)

#         new_dict = {}
        
#         fil_dom_int = [entry for entry in domain_dict["intents"] if "ques_" not in entry]
#         fil_dom_data = {intent: value for intent, value in domain_dict["responses"].items() if "utter_ans_" not in intent}

#         for index, row in df.iterrows():
#             fil_dom_int.append(f"ques_{int(index)}")

#             ans = row["Answers"].strip("'").strip('"').strip()
#             ans = process_multiline_answer(ans)
#             new_dict[f"utter_ans_{int(index)}"] = [{"text": (f"{ans}\n")}]
            
#         fil_dom_data.update(new_dict)

#         domain_dict["responses"] = fil_dom_data
#         domain_dict["intents"] = fil_dom_int

#         for key,value in domain_dict["responses"].items():
#             for item in value:
#                     item['text'] = literal_unicode(f"{item['text']}")
                    
#      # Rules file
#     with open('./data/rules.yml') as f:
#         rules_dict = yaml.full_load(f)
        
#         rules_dt = rules_dict["rules"]
        
#         filtered_rules_dict = [entry for entry in rules_dt if not entry['rule'].startswith('rule_')]
        
#         new_rules = []

#         for index, row in df.iterrows():
#             new_rules.append(
#                 {
#                     "rule": f"rule_{index}",
#                     "steps": [{"intent": f"ques_{index}"},{"action": f"utter_ans_{index}"}]
#                 })
#         filtered_rules_dict += new_rules
#         rules_dt = filtered_rules_dict
        
#         rules_dict["rules"] = rules_dt
    
#     # Story file
#     with open('./data/stories.yml') as f:
#         story_dict = yaml.full_load(f)
        
#         story_dt = story_dict["stories"]
        
#         filtered_story_dict = [entry for entry in story_dt if not entry['story'].startswith('story_')]
        
#         new_stories = []

#         for index, row in df.iterrows():
#             new_stories.append(
#                 {
#                     "story": f"story_{index}",
#                     "steps": [{"intent": f"ques_{index}"}, {"action": f"utter_ans_{index}"}]
#                 })

#         filtered_story_dict += new_stories
#         story_dt = filtered_story_dict
#         story_dict["stories"] = story_dt
    
#     create_data_files(nlu_data = nlu_dict,
#                       rules_data = filtered_rules_dict,
#                       stories_data = filtered_story_dict,
#                       domain_data = domain_dict)


# def main():
#     # df = pd.read_csv("./data/new_update_dataset.csv")
#     # df = pd.read_excel("/home/user/Workstation/ibas-chat-operator/data/final_dataset.xlsx")
#     df = pd.read_excel("/home/tanjim/workstation/ibas-project/source/final_dataset.xlsx")


#     create_new_files(df)
#     print("curated")

# if __name__ == "__main__":
#     yaml.add_representer(literal_unicode, literal_unicode_representer)
#     main()






import yaml
import pandas as pd

def process_multiline_answer(str_data):
    str_list = [x.strip() for x in str_data.replace('*', '').split('\n')]
    str_list = list(filter(None, str_list))
    return '\n'.join(str_list)

def process_multiline_example(str_data):
    str_list = [x.strip() for x in str_data.replace('*', '').split('\n')]
    str_list = list(filter(None, str_list))
    return '\n- '.join(str_list)

class literal_unicode(str):
        pass

def literal_unicode_representer(dumper, data):
    return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


# yaml.add_representer(folded_unicode, folded_unicode_representer)
yaml.add_representer(literal_unicode, literal_unicode_representer)

def create_data_files(nlu_data, rules_data, stories_data, domain_data):
    with open("./data/nlu.yml", "w") as outfile:
        yaml.dump(
            nlu_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False
        )

    with open("./data/rules.yml", "w") as outfile:
        yaml.safe_dump(
            rules_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False
        )
    with open("./data/stories.yml", "w") as outfile:
        yaml.safe_dump(
            stories_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False
        )
    with open("./domain.yml", "w") as outfile:
        yaml.dump(
            domain_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False,
        )
        
def create_new_files(df):
    
    
    # df = df[:10]
    
    # NLU file
    with open('./data/nlu.yml') as f:
        nlu_dict = yaml.full_load(f)
    
        nlu_dt = nlu_dict["nlu"]

        # Extract 'intent' key values containing "ques_"

        filtered_nlu = [entry for entry in nlu_dt if "ques_" not in entry["intent"]]

        result_list = []

        for index,row in df.iterrows():
            ques = row["Questions"].strip("'").strip('"').strip()
            ques = process_multiline_example(ques)
            result_dict = {
                        'intent': f"ques_{int(index)}",
                        'examples': f"- {ques}\n"
                    }
            #print((result_dict))

            result_list.append(result_dict)

        filtered_nlu += result_list

        # Applying the function to examples values
        for item in filtered_nlu:
            examples = item.get('examples')
            if examples:
                examples = literal_unicode(examples)
                item['examples'] = examples

        nlu_data = {"version": "3.0", "nlu": []}
        nlu_dict["nlu"] = filtered_nlu
    
    # Domain file
    with open('./domain.yml') as f:
        domain_dict = yaml.full_load(f)

        new_dict = {}
        
        fil_dom_int = [entry for entry in domain_dict["intents"] if "ques_" not in entry]
        fil_dom_data = {intent: value for intent, value in domain_dict["responses"].items() if "utter_ans_" not in intent}

        for index, row in df.iterrows():
            fil_dom_int.append(f"ques_{int(index)}")

            ans = row["Answers"].strip("'").strip('"').strip()
            ans = process_multiline_answer(ans)
            new_dict[f"utter_ans_{int(index)}"] = [{"text": (f"{ans}\n")}]
            
        fil_dom_data.update(new_dict)

        domain_dict["responses"] = fil_dom_data
        domain_dict["intents"] = fil_dom_int

        for key,value in domain_dict["responses"].items():
            for item in value:
                    item['text'] = literal_unicode(f"{item['text']}")
                    
    # Rules file
    with open('./data/rules.yml') as f:
        rules_dict = yaml.full_load(f)
        
        rules_dt = rules_dict["rules"]
        
        filtered_rules_dict = [entry for entry in rules_dt if not entry['rule'].startswith('rule_')]
        
        new_rules = []

        for index, row in df.iterrows():
            new_rules.append(
                {
                    "rule": f"rule_{index}",
                    "steps": [{"intent": f"ques_{index}"},{"action": f"utter_ans_{index}"}]
                })
        filtered_rules_dict += new_rules
        rules_dt = filtered_rules_dict
        
        rules_dict["rules"] = rules_dt
    
    # Story file
    with open('./data/stories.yml') as f:
        story_dict = yaml.full_load(f)
        
        story_dt = story_dict["stories"]
        
        filtered_story_dict = [entry for entry in story_dt if not entry['story'].startswith('story_')]
        
        new_stories = []

        for index, row in df.iterrows():
            new_stories.append(
                {
                    "story": f"story_{index}",
                    "steps": [{"intent": f"ques_{index}"}, {"action": f"utter_ans_{index}"}]
                })

        filtered_story_dict += new_stories
        story_dt = filtered_story_dict
        story_dict["stories"] = story_dt

    
    create_data_files(nlu_data = nlu_dict,
                      rules_data = rules_dict,
                      stories_data = story_dict,
                      domain_data = domain_dict)


def main():
    # df = pd.read_csv("./data/new_update_dataset.csv")
    # df = pd.read_csv("new_update_dataset.csv")
    # df = pd.read_excel("/home/tanjim/workstation/ibas-project/source/final_dataset.xlsx")
    # df = pd.read_excel("/media/robin/Documents/PersonalWorks/ibas_project/source/Final-updated-dataset.xlsx")   # Use it after creating new curator file
    df = pd.read_excel("/media/robin/Documents/PersonalWorks/ibas_project/source/final_dataset_old.xlsx")

    create_new_files(df)
    print("curated")

if __name__ == "__main__":
    yaml.add_representer(literal_unicode, literal_unicode_representer)
    main()