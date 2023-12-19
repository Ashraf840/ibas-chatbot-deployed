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

def calculate_max_last_digit():
    
    with open('./data/nlu.yml') as f:
        data = yaml.full_load(f)
        
        intent_values = [item['intent'] for item in data["nlu"]]
        s = "ques_"
        last_digits = [int(intt[5:]) for intt in intent_values if s in str(intt)]
        max_last_digit = max(last_digits)

        return max_last_digit 

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
    
    print("Successfully printed df:", df)
    max_last_digit = calculate_max_last_digit()
    
    dff = df[max_last_digit:]
    df_diff = len(df)-len(dff)
    
    with open('./data/nlu.yml') as f:
        data = yaml.full_load(f)
        
        result_list = []

        for index, row in dff.iterrows():
            ques = row["Questions"].strip("'").strip('"').strip()
            ques = process_multiline_example(ques)
            result_dict = {
                'intent': f"ques_{int(index+max_last_digit + 1 - df_diff)}",
                'examples': f"- {ques}\n"
            }
            #print((result_dict))

            result_list.append(result_dict)
            #print(result_list)

        data["nlu"] += result_list
        #print(nlu_dict)

        # Applying the function to examples values
        for item in data["nlu"]:
            examples = item.get('examples')
            if examples:
                examples = literal_unicode(examples)
                item['examples'] = examples

        nlu_data = {"version": "3.0", "nlu": []}
        nlu_data["nlu"] = data["nlu"]
    
    # Domain file
    with open('./domain.yml') as f:
        domain_dict = yaml.full_load(f)

        new_dict = {}

        for index, row in dff.iterrows():
            domain_dict["intents"].append(f"ques_{int(index + max_last_digit + 1 - df_diff)}")

            ans = row["Answers"].strip("'").strip('"').strip()
            ans = process_multiline_answer(ans)
            new_dict[f"utter_ans_{int(index+max_last_digit + 1 - df_diff)}"] = [{"text": (f"{ans}\n")}]

        # Create a new dictionary to store the merged result
        merged_dict = {}

        # Iterate over dict1
        for key, value in domain_dict["responses"].items():
            merged_dict[key] = value
            if key == f"utter_ans_{max_last_digit}":
                merged_dict.update(new_dict)

        domain_dict["responses"] = merged_dict

        for key,value in domain_dict["responses"].items():
            for item in value:
                    item['text'] = literal_unicode(f"{item['text']}")
                    
    # Rules file
    with open('./data/rules.yml') as f:
        rules_dict = yaml.full_load(f)

        new_rules = []

        for index, row in dff.iterrows():
            new_rules.append(
                {
                    "rule": f"rule_{index+max_last_digit+1 - df_diff}",
                    "steps": [{"intent": f"ques_{index+max_last_digit+1 - df_diff}"},{"action": f"utter_ans_{index+max_last_digit+1 - df_diff}"}]
                })
        rules_dict["rules"] += new_rules
        
    # Stories file
    with open('./data/stories.yml') as f:
        story_dict = yaml.full_load(f)

        new_stories = []

        for index, row in dff.iterrows():
            new_stories.append(
                {
                    "story": f"story_{index+max_last_digit+1 - df_diff}",
                    "steps": [{"intent": f"ques_{index+max_last_digit+1 - df_diff}"}, {"action": f"utter_ans_{index+max_last_digit+1 - df_diff}"}]
                })

        story_dict["stories"] += new_stories
        
    
    
    create_data_files(nlu_data = data,
                      rules_data = rules_dict,
                      stories_data = story_dict,
                      domain_data = domain_dict)

def main():
    # df = pd.read_csv("./data/new_update_dataset.csv")
    df = pd.read_excel("./data/ibas_final_dataset.xlsx", sheet_name="Sheet1")

    create_new_files(df)

if __name__ == "__main__":
    yaml.add_representer(literal_unicode, literal_unicode_representer)
    main()
