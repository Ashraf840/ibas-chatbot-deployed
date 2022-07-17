import numpy as np
import pandas as pd
import json
import yaml


def process_by_group(data_df):
    grouped_df = data_df.groupby("Type")

    qa_dict = {}
    for name, group in grouped_df:
        # name = name.replace("/", "_")
        print(name)
        # data = dict(zip([x for x in data_df["প্রশ্ন"]], [x for x in data_df["উত্তর"]]))
        # # json.dump(qa_dict, open('qa.json', 'w', encoding='utf-8'))
        # with open(f"{name}.yml", "w", encoding="utf8") as outfile:
        #     yaml.dump(data, outfile, default_flow_style=False)


def create_data_files(nlu_data, rules_data, stories_data, domain_data):
    with open(f"./data/nlu.yml", "w") as outfile:
        yaml.dump(
            nlu_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False
        )

    with open(f"./data/rules.yml", "w") as outfile:
        yaml.safe_dump(
            rules_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False
        )
    with open(f"./data/stories.yml", "w") as outfile:
        yaml.safe_dump(
            stories_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False
        )
    with open(f"./domain.yml", "w") as outfile:
        yaml.dump(
            domain_data,
            outfile,
            default_flow_style=False,
            encoding="utf-8",
            allow_unicode=True,
            sort_keys=False,
        )


def process_multiline_example(str_data):
    str_list = [x.strip() for x in str_data.replace('*', '').split('\n')]
    return '\n- '.join(str_list)


def process_multiline_answer(str_data):
    str_list = [x.strip() for x in str_data.replace('*', '').split('\n')]
    return '\n'.join(str_list)


def main():
    # data_df = pd.read_csv("chatbot-training-data - curated_data.tsv", sep="\t")
    # data_df = pd.read_excel('MOF-IBAS++__Chatbot__RFP.xlsx', sheet_name='Y1-chatbot-training-data')
    data_df = pd.read_excel('MOF-IBAS++__Chatbot__RFP.xlsx', sheet_name='Y1-doer-questions')

    # data_df["Type"] = data_df["Type"].fillna("Miscellaneous")q
    data_df.fillna("", inplace=True)

    print(data_df.columns)

    nlu_data = {"version": "3.0", "nlu": []}
    rules_data = {"version": "3.0", "rules": []}
    stories_data = {"version": "3.0", "stories": []}
    domain_data = {
        "version": "3.0",
        "intents": [],
        "responses": {},
        "session_config": {
            "session_expiration_time": 60,
            "carry_over_slots_to_new_session": True,
        },
    }

    for index, row in data_df.iterrows():
        ques = row["Ques _Agrani Doer Banking"].strip("'").strip('"').strip()
        ans = row["Ans"].strip("'").strip('"').strip()
        ques = process_multiline_example(ques)
        ans = process_multiline_answer(ans)

        if not (len(ques) > 0 and len(ans) > 0):
            continue

        domain_data["intents"].append(f"ques_{index}")
        domain_data["responses"][f"utter_ans_{index}"] = [{"text": literal_unicode(f"{ans}\n")}]
        nlu_data["nlu"].append({
            "intent": f"ques_{index}",
            "metadata": {"intent_type": row['Type']},
            "examples": literal_unicode(f"- {ques}\n")
        })

        rules_data["rules"].append(
            {
                "rule": f"rule_{index}",
                "steps": [{"intent": f"ques_{index}"}, {"action": f"utter_ans_{index}"}],
            }
        )
        stories_data["stories"].append(
            {
                "story": f"story_{index}",
                "steps": [{"intent": f"ques_{index}"}, {"action": f"utter_ans_{index}"}],
            }
        )

    create_data_files(nlu_data=nlu_data,
                      rules_data=rules_data,
                      stories_data=stories_data,
                      domain_data=domain_data)


if __name__ == "__main__":
    # class folded_unicode(str):
    #     pass

    class literal_unicode(str):
        pass


    #
    # def folded_unicode_representer(dumper, data):
    #     return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='>')

    def literal_unicode_representer(dumper, data):
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')


    # yaml.add_representer(folded_unicode, folded_unicode_representer)
    yaml.add_representer(literal_unicode, literal_unicode_representer)

    main()
