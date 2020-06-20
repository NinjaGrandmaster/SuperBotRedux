import pandas as pd
import nltk
import re
import requests
import tkinter as tk

from io import BytesIO
from operator import itemgetter
from PIL import ImageTk, Image

heroes_df = pd.read_csv('superheroes_nlp_dataset.csv', index_col='name')
df_csv = pd.read_csv('superheroes_nlp_dataset.csv')


# option 0: print info with query statement, option 1: return the retrieved data
# hero_name is a name, info is he attribute, such as weight or realname, of the hero you want
def get_hero_info(hero_name, info, query='', option=0):

    hero_data = heroes_df.loc[hero_name, info]

    if option == 0:
        print(hero_name, query, hero_data)
    elif option == 1:
        return hero_data


# if a name is not recognized or misspelled generate suggestions of names from the data set
def did_you_mean_list(unkown_name, num_of_sugg=5):
    suggestions = []
    name_version = re.compile("(.*) (\(.*\))")
    for x in range(1450):
        name = str(df_csv.at[x, 'name'])

        if name_version.match(name):
            # extract only the name if it is formatted like this Batman (1966)
            temp_name = name_version.search(name).group(1)
            ed = nltk.edit_distance(unkown_name, temp_name)
            suggestions.append((name, ed))
            # print(type(name), type(temp.group(1)))
        else:
            # calculate edit distance
            ed = nltk.edit_distance(unkown_name, name)
            # store names with edit distance
            suggestions.append((name, ed))

    # sort array of name, edit distance tuples and get first value as a suggestion
    suggestions.sort(key=itemgetter(1))
    # return suggestions list
    return suggestions[:num_of_sugg]


# gets a value from a list
def select_hero_from_list(hero_list):
    count = 0
    choice = 0
    # print("\nMultiple entities exist. Please select one.")
    for hero in hero_list:
        if count < 9:
            print("", count + 1, ". ", hero)
        else:
            print(count + 1, ". ", hero)

        count += 1

    while choice < 1 or choice > count:
        print("Select an Entity. (1-" + str(count) + ")")
        # choice = int(input("\nWhich  did you mean?(1-" + str(count) + "): "))
        choice = int(input())
        if choice < 1 or choice > count:
            print("\nPlease choose a number between", 1, "and", str(count) + "!")

    return hero_list[choice - 1]


# Takes in a list of tuples that have hero name and one attribute and asks the user which version of the hero the
# would like to select. use in the case multiple heroes exist for one name.
# returns a tuple with data of the hero the user selected
# input list must be of the form [(hero_name_1, attribute), (hero_name_2, attribute) ... (hero_name_n, attribute)]
def select_hero_from_tuple_list(hero_tup_list):
    count = 0
    choice = 0
    # print("\nMultiple entities exist. Please select one.")
    for i in hero_tup_list:
        if count < 9:
            print("", count + 1, ". ", i[0])
        else:
            print(count + 1, ". ", i[0])

        count += 1

    while choice < 1 or choice > count:
        print("Select an Entity. (1-" + str(count) + ")")
        # choice = int(input("\nWhich  did you mean?(1-" + str(count) + "): "))
        choice = int(input())
        if choice < 1 or choice > count:
            print("\nPlease choose a number between", 1, "and", str(count) + "!")

    return hero_tup_list[choice-1]


def get_hero_names(hero_name):
    hero_df_filter = heroes_df.filter(regex=hero_name, axis=0)
    filtered_list = hero_df_filter.index.values.tolist()

    if len(filtered_list) == 0:
        # work around for entering hero_name (version)
        if hero_name in heroes_df.index:
            return hero_name
        else:
            print("Name not found. Did you mean one of these entities")
            temp_name = select_hero_from_tuple_list(did_you_mean_list(hero_name))
            # print(temp_name)
            temp_name = temp_name[0]
    elif len(filtered_list) == 1:
        temp_name = filtered_list[0]
    else:
        print("Multiple", hero_name, "entities known:")
        temp_name = select_hero_from_list(filtered_list)

    return temp_name


def get_real_name(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'real_name', query='real name is')


def get_superpowers(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'superpowers', query='powers')


def get_overall_score(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'overall_score', query='overall score')


def get_combat_score(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'combat_score', query='combat score')


def get_teams(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'teams', query='is part of the')


def get_alignment(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'alignment', query='alignment is')


def get_birth_place(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'place_of_birth', query='birth place is')


def get_base(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'base', query='base location')


def get_height(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'height', query='is')


def get_weight(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'weight', query='weighs')


def get_hero_image(hero_name):
    name_check = get_hero_names(hero_name)
    image_url = get_hero_info(name_check, 'img', option=1)
    # print('Extension_part', image_url, type(image_url))

    if not pd.isna(image_url):
        root = tk.Tk()
        full_image_url = "https://www.superherodb.com" + image_url
        response = requests.get(full_image_url)
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
        panel = tk.Label(root, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        panel2 = tk.Label(root, justify=tk.LEFT, padx=10, text=name_check).pack(side="top")
        root.mainloop()
    else:
        print('No images of', name_check, 'exist')


def get_ability_scores(hero_name):
    name_check = get_hero_names(hero_name)

    scores = heroes_df.loc[name_check, 'intelligence_score':'power_score']
    scores_list = scores.tolist()
    print(scores)
    print('\n---', name_check, '---')
    print('Intelligence:', scores[0])
    print('Strength:', scores_list[1])
    print('Speed:', scores_list[2])
    print('Durability:', scores_list[3])
    print('Power:', scores_list[4], '')
