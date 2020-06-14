import pandas as pd
import nltk
import re

from operator import itemgetter

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


def did_you_mean_list(unkown_name, suggestions=5):
    distances = []
    name_version = re.compile("(.*) (\(.*\))")
    for x in range(1450):
        name = str(df_csv.at[x, 'name'])

        if name_version.match(name):
            # extract only the name if it is formatted like this Batman (1966)
            temp_name = name_version.search(name).group(1)
            ed = nltk.edit_distance(unkown_name, temp_name)
            distances.append((name, ed))
            # print(type(name), type(temp.group(1)))
        else:
            # calculate edit distance
            ed = nltk.edit_distance(unkown_name, name)
            # store names with edit distance
            distances.append((name, ed))

    # sort array of name, edit distance tuples and get first value as a suggestion
    distances.sort(key=itemgetter(1))
    # return first value in list as suggestion
    return distances[:suggestions]


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



