import json, os, nltk
from collections import defaultdict

def handle_punc(ls):
    new_ls = []
    for item in ls:
        if "-" in item:
            new_ls.append(item.replace("-", " "))
            new_ls.append(item.replace("-", ""))
        else:
            new_ls.append(item)
    new_ls_2 = []
    for item in new_ls:
        if "," in item:
            item_ls = item.split(",")
            for i in item_ls:
                i = i.strip()
                if i.startswith("and "):
                    i = i[4:]
                if len(i) > 0:
                    new_ls_2.append(i.strip())
        else:
            new_ls_2.append(item)
    return new_ls_2

def get_traits(filename):
    with open(filename, "r") as f:
        traits = [line.lower().strip() for line in f]
        traits = handle_punc(traits)
    return traits

majors = defaultdict(list)
def get_majors(filename):
    with open(filename, "r") as f:
        for line in f:
            if "Major_Category" not in line:
                line = line.lower().split(",")
                cat = line[2].strip().replace("&","and")+ " major"
                maj = line[1].strip().replace(";",",").replace('"','')
                if cat != "na":
                    majors[cat].append(maj)
    for cat,ms in majors.items():
        majors[cat] = handle_punc(ms)
    return majors

def insert_major_categories(dummy):
    return list(majors.keys())

def insert_major_items(cat):
    return majors[cat]

def get_jobs(filename):
    with open(filename, "r") as f:
        prev_digit = False
        jobs = []
        for line in f:
            if prev_digit and len(line.strip()) > 0:
                jobs.append(line.lower().strip())
                prev_digit = False
            if line.strip().isdigit():
                prev_digit = True
        jobs = handle_punc(jobs)
    return jobs

def get_dict_from_list(filename, append):
    d = {}
    with open(filename, "r") as f:
        for line in f:
            if line.isupper():
                if append is not None and len(append) > 0:
                    category = '_'+line.lower().strip()+" "+append
                else:
                    category = '_' + line.lower().strip()
                d[category] = []
            elif len(line.strip()) > 0:
                d[category].append(line.lower().strip())
    return d

def get_dict_from_list_without_underscore(filename):
    d = {}
    with open(filename, "r") as f:
        for line in f:
            if line.isupper():
                category = line.lower().strip()
                d[category] = []
            elif len(line.strip()) > 0:
                d[category].append(line.lower().strip())
    return d

class Ontology(dict):

    def __init__(self, reg_dict=None):
        if reg_dict:
            for key in reg_dict:
                self[key] = reg_dict[key]
        else:
            self["ontology"] = {}
            self["expressions"] = {}
        dict.__init__(self)

    def add(self, parent, children):
        self["ontology"][parent] = children

    def put(self, parent, func, arg):
        self["ontology"][parent] = func(arg)

    def merge_dict(self, parent, func, arg, arg2):
        if arg2 is not None:
            dict = func(arg, arg2)
        else:
            dict = func(arg)
        if parent is not None:
            self["ontology"][parent] = []
            for key,value in dict.items():
                self["ontology"][key] = handle_punc(value)
                self["ontology"][parent].append(key)
        else:
            for key, value in dict.items():
                self["ontology"][key] = handle_punc(value)

    def add_dict(self, d):
        for key,val in d.items():
            self["ontology"][key] = val

    def add_expressions(self, e):
        self["expressions"] = e

    def lemmatize(self, ignore):
        lemmatizer = nltk.stem.WordNetLemmatizer()
        lemmatizer.lemmatize('initialize')
        lemmatized_ontology = {}
        keys = ["ontology","expressions"]
        for key in keys:
            lemmatized_ontology[key] = {}
            ont = self[key]
            for k, l in ont.items():
                if k in ignore:
                    lemmatized_ontology[key][k] = l
                    continue
                lemmatized_ontology[key][k] = []
                for e in l:
                    lemmas = set()
                    for pos in 'a', 'r', 'v', 'n':
                        lemma = lemmatizer.lemmatize(e, pos=pos)
                        lemmas.add(lemma)
                    if len(lemmas) == 1:
                        if lemma not in lemmatized_ontology[key][k]:
                            lemmatized_ontology[key][k].extend([lemma])
                    else:
                        lemmatized_ontology[key][k].extend([l for l in lemmas if l != e and l not in lemmatized_ontology[key][k]])
        return lemmatized_ontology

    def display(self):
        print(json.dumps(self,indent=4))

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self,f,indent=4)

if __name__ == '__main__':
    PATH = "data"

    ont = Ontology()

    file = open(os.path.join("data","_manual_ontology.json"), "r")
    manual_ont = json.load(file)

    ont.add_dict(manual_ont["ontology"])
    ont.add_expressions(manual_ont["expressions"])

    ont.add("_personality", ["_positive trait","_negative trait","_neutral trait"])
    ont.put("_positive trait", get_traits, os.path.join(PATH,"positive_trait.txt"))
    ont.put("_negative trait", get_traits, os.path.join(PATH,"negative_trait.txt"))
    ont.put("_neutral trait", get_traits, os.path.join(PATH,"neutral_trait.txt"))
    ont.add('_emotions', ["_emotions pos", "_emotions neg"])

    majors = get_majors(os.path.join(PATH,"college_major.csv"))
    ont.put("_major", insert_major_categories, None)
    for cat in majors:
        ont.put(cat, insert_major_items, cat)

    ont.merge_dict("_job", get_dict_from_list, os.path.join(PATH,"job_list.txt"), "job")
    ont.merge_dict("_job department", get_dict_from_list, os.path.join(PATH, "job_act.txt"), "department")
    ont.merge_dict("_job location", get_dict_from_list, os.path.join(PATH, "job_loc.txt"), "location")
    ont.merge_dict("_job sensitive", get_dict_from_list, os.path.join(PATH, "job_sens.txt"), "job")
    ont.merge_dict("_old_life stage", get_dict_from_list, os.path.join(PATH, "life_stage.txt"), "stage")
    ont.merge_dict("_school subject", get_dict_from_list, os.path.join(PATH, "school_subjects.txt"), "subject")
    ont.merge_dict("_school club", get_dict_from_list, os.path.join(PATH, "clubs.txt"), "club")
    ont.merge_dict("_location", get_dict_from_list, os.path.join(PATH, "locations.txt"), "")
    ont.merge_dict("_names", get_dict_from_list, os.path.join(PATH, "names.txt"), "names")
    ont.merge_dict("_animals", get_dict_from_list, os.path.join(PATH, "animals.txt"), "animal")
    ont.merge_dict("_adjectives", get_dict_from_list, os.path.join(PATH, "adjectives.txt"), "adj")
    ont.merge_dict("_emotions pos", get_dict_from_list, os.path.join(PATH, "emotions_pos.txt"), "")
    ont.merge_dict("_emotions neg", get_dict_from_list, os.path.join(PATH, "emotions_neg.txt"), "")
    ont.merge_dict(None, get_dict_from_list_without_underscore, os.path.join(PATH, "adj_pos.txt"), None)
    ont.merge_dict(None, get_dict_from_list_without_underscore, os.path.join(PATH, "adj_neg.txt"), None)

    ont = Ontology(ont.lemmatize(ignore=['_positive adj','_negative adj','_female names', '_male names']))

    #ont.display()

    ont.save("../_common.json")