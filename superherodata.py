import pandas as pd
import nltk
import random
import re
import requests
import textwrap
import tkinter as tk

import botresponse as bot_response

from bs4 import BeautifulSoup
from io import BytesIO
from operator import itemgetter
from PIL import ImageTk, Image

heroes_df = pd.read_csv('superheroes_nlp_dataset.csv', index_col='name')
heroes_df_csv = pd.read_csv('superheroes_nlp_dataset.csv')


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
    name_version = re.compile(r"(.*) (\(.*\))")
    for x in range(1450):
        name = str(heroes_df_csv.at[x, 'name'])

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
            bot_response.menu_print(' ' + str(count + 1) + '. ' + hero)
        else:
            bot_response.menu_print(str(count + 1) + '. ' + hero)

        count += 1

    while choice < 1 or choice > count:
        bot_response.bot_print("Select an Entity. (1-" + str(count) + ")")

        try:
            choice = int(input())  # get user input

            if choice < 1 or choice > count:
                bot_response.bot_print("\nPlease choose a number between 1 and " + str(count) + "!")

        except ValueError:
            choice = -5  # set choice out of rangw as a failsafe to continue input loop
            bot_response.bot_print('\nInput must be an integer between 1 and ' + str(count) + '!')

    return hero_list[choice - 1]


# Takes in a list of tuples that have hero name and one attribute and asks the user which version of the hero the
# would like to select. use in the case multiple heroes exist for one name.
# returns a tuple with data of the hero the user selected
# input list must be of the form [(hero_name_1, attribute), (hero_name_2, attribute) ... (hero_name_n, attribute)]
def select_hero_from_tuple_list(hero_tup_list):
    count = 0
    choice = 0
    # print("\nMultiple entities exist. Please select one.")
    for hero in hero_tup_list:
        if count < 9:
            bot_response.menu_print(' ' + str(count+1) + '. ' + hero[0])
        else:
            bot_response.menu_print(str(count + 1) + '. ' + hero[0])

        count += 1

    while choice < 1 or choice > count:
        bot_response.bot_print("Select an Entity. (1-" + str(count) + ")")

        try:
            choice = int(input())  # get user input

            if choice < 1 or choice > count:
                bot_response.bot_print("\nPlease choose a number between 1 and " + str(count) + "!")

        except ValueError:
            choice = -5  # set choice out of rangw as a failsafe to continue input loop
            bot_response.bot_print('\nInput must be an integer between 1 and ' + str(count) + '!')

    return hero_tup_list[choice-1]


def get_hero_names(hero_name):
    hero_df_filter = heroes_df.filter(regex=hero_name, axis=0)
    filtered_list = hero_df_filter.index.values.tolist()

    if len(filtered_list) == 0:
        # work around for entering hero_name (version)
        if hero_name in heroes_df.index:
            return hero_name
        else:
            bot_response.bot_print("Entity " + hero_name + " not found. Did you mean one of these entities")
            temp_name = select_hero_from_tuple_list(did_you_mean_list(hero_name))
            # print(temp_name)
            temp_name = temp_name[0]
    elif len(filtered_list) == 1:
        temp_name = filtered_list[0]
    else:
        # print("Multiple", hero_name, "entities known:")
        bot_response.bot_print("Multiple " + hero_name + " entities known:")
        temp_name = select_hero_from_list(filtered_list)

    return temp_name


# prints text by wraping text to a set width, can be changed with variable text_width
# style idicates how text should be styled indicated
def print_textwrap(text, text_width=80, style=0):

    if style == 1:
        # style with the blue text for the bot
        bot_response.bot_print(textwrap.fill(text, width=text_width))
    if style == 2:
        bot_response.paragraph_print(textwrap.fill(text, width=text_width))
    else:
        print(textwrap.fill(text, width=text_width))


def get_real_name(hero_name):
    name_check = get_hero_names(hero_name)

    # get_hero_info(name_check, 'real_name', query='real name is')
    real_name = get_hero_info(name_check, 'real_name', option=1)

    if pd.isna(real_name):
        real_name = 'unknown'

    bot_response.bot_print('\n' + name_check + '\'s real name is ' + real_name + '\n')


def get_superpowers(hero_name):
    # regex to extract powers from string containing them
    # string of the form is ['Agility', 'Audio Control', 'Cold Resistance', 'Danger Sense', 'Electrokinesis]

    name_check = get_hero_names(hero_name)
    powers_string = get_hero_info(name_check, 'superpowers', option=1)

    powers_list = string_list_convert(powers_string)

    powers_list_size = len(powers_list)

    print()

    if powers_list_size == 1:

        bot_response.bot_print(name_check + '\'s power is ' + powers_list[0])

    elif powers_list_size == 2:

        bot_response.bot_print(name_check + '\'s powers are ' + powers_list[0] + ' and ' + powers_list[1])

    elif powers_list_size > 2:

        # get last power to add an 'and' before it in the list of powers before being displayed
        last_power = powers_list.pop()
        concat_string = ', '.join(powers_list) + ', and ' + last_power

        powers_out_string = name_check + '\'s powers are ' + concat_string

        print_textwrap(powers_out_string, text_width=100, style=1)

    else:

        bot_response.bot_print(name_check + ' has no powers')

    print()


def get_powers_decription(hero_name):
    missing_data_text = 'Powers description not available in data banks'

    name_check = get_hero_names(hero_name)

    powers_text = get_hero_info(name_check, 'powers_text', option=1)

    # check for nan pandas value, which means missing field within the superhero data set csv
    # NOTE: this is different than a an empty string and must be checked separately
    if pd.isna(powers_text):
        powers_text = missing_data_text

    # strip white space from beginning and end of string. Need to do this to check for empty string
    powers_text = powers_text.strip()

    # check for empty string
    if not powers_text:
        powers_text = missing_data_text

    # print powers description
    print()
    print_textwrap(powers_text, text_width=100, style=2)
    print()


def get_overall_score(hero_name):
    name_check = get_hero_names(hero_name)

    o_score = get_hero_info(name_check, 'overall_score', option=1)

    inf_unicode = "\u221E"  # unicode of the infinity symbol

    if o_score == inf_unicode:
        print('\n' + name_check + ' has an infinite overall score!!!\n')
    elif o_score == '-':
        print('\nInsufficient data to compute an overall score for entity ' + name_check + '\n')
    else:
        print('\n' + name_check + '\'s overall score is ' + o_score + '\n ')


def get_combat_score(hero_name):
    name_check = get_hero_names(hero_name)

    c_score = get_hero_info(name_check, 'combat_score', option=1)

    print('\n' + name_check + '\'s combat score is ' + str(c_score) + '\n')


def get_teams(hero_name):
    name_check = get_hero_names(hero_name)
    get_hero_info(name_check, 'teams', query='is part of the')

    team_list_string = get_hero_info(name_check, 'teams', option=1)
    # extract teams from the string retrieved from the data set
    team_list = string_list_convert(team_list_string)

    print(team_list)

    team_list_size = len(team_list)

    if team_list_size == 0:
        print('\n' + name_check + ' is not a part of a team\n')
    elif team_list_size == 1:
        print('\n' + name_check + '\'s team is the ' + team_list[0] + '\n')
    elif team_list_size == 2:
        print('\n' + name_check + ' is on teams ' + team_list[0] + ' and ' + team_list[1] + '\n')
    else:
        # get last power to add an 'and' before it in the list of powers before being displayed
        last_team = team_list.pop()
        concat_string = ', '.join(team_list) + ', and ' + last_team

        team_out_string = name_check + '\'s teams are ' + concat_string

        print()
        print_textwrap(team_out_string, text_width=100)
        print()


def get_alignment(hero_name):
    name_check = get_hero_names(hero_name)

    alignment = get_hero_info(name_check, 'alignment', option=1)

    print()
    if pd.isna(alignment):
        print(name_check + '\'s alignment is unknown\n')
    else:
        print(name_check + ' is considered to be ' + alignment, '\n')


def get_birth_place(hero_name):
    name_check = get_hero_names(hero_name)

    birth_place = get_hero_info(name_check, 'place_of_birth', option=1)

    if pd.isna(birth_place):
        birth_place = 'unknown'

    print()
    print(name_check + ' \'s place of bith is ' + birth_place + '\n')


def get_base(hero_name):
    name_check = get_hero_names(hero_name)

    base_location = get_hero_info(name_check, 'base', option=1)

    if pd.isna(base_location):
        base_location = 'unknown'

    print()
    print(name_check + '\'s base(s): ' + base_location + '\n')


def get_height(hero_name):
    name_check = get_hero_names(hero_name)

    height = get_hero_info(name_check, 'height', option=1)

    print()
    if height == '-':
        print(name_check + '\'s height is unknown\n')
    else:
        # array of the format ["6'4", 'dot', '193', 'cm']
        # index 0 has height in ft, index 2 had height in cm
        height_array = height.split()

        print(name_check + '\'s height is ' + height_array[0] + ' (' + height_array[2] + ' cm)\n')


def get_weight(hero_name):
    name_check = get_hero_names(hero_name)

    weight = get_hero_info(name_check, 'weight', option=1)

    print()
    if weight == '-':
        print(name_check + '\'s weight is unknown\n')
    else:
        # array of the format ['198', 'lb', 'dot', '89', 'kg']
        # index 0 has height in ft, index 2 had height in cm
        weight_array = weight.split()

        print(name_check + '\'s weighs ' + weight_array[0] + ' lb (' + weight_array[3] + ' kg)\n')


# only pick option 1 if you know for sure the name(s) being passed in exist in the data set, other wise leave option as
# 0
def get_hero_history(hero_name, option=0):

    if option == 1:
        name_check = hero_name
    else:
        name_check = get_hero_names(hero_name)

    history_text = get_hero_info(name_check, 'history_text', option=1)

    # If back story is not contained in the hero data set csv set history as unknown
    if pd.isna(history_text):
        history_text = 'Backstory unknown for ' + name_check

    print()
    print_textwrap(history_text, text_width=100)
    print()


def get_occupation(hero_name):
    name_check = get_hero_names(hero_name)

    occupations = get_hero_info(name_check, 'occupation', option=1)

    if pd.isna(occupations):
        occupations = 'unknown'

    print(name_check, 'occupation(s)', occupations)


def get_relatives(hero_name):
    name_check = get_hero_names(hero_name)

    relatives = get_hero_info(name_check, 'relatives', option=1)

    if pd.isna(relatives):
        relatives = 'unknown'

    print(name_check, 'relative(s)')
    print_textwrap(relatives, text_width=100)
    print()


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
    # print(scores)
    print('\n---', name_check, '---')
    print('Intelligence:', scores[0])
    print('Strength:', scores_list[1])
    print('Speed:', scores_list[2])
    print('Durability:', scores_list[3])
    print('Power:', scores_list[4], '\n')


def weight_comparison(hero1, hero2):
    hero1_name = get_hero_names(hero1)
    hero2_name = get_hero_names(hero2)

    # gets weighs as string in the form 158 lb • 71 kg
    hero1_weight_raw = get_hero_info(hero1_name, 'weight', option=1)
    hero2_weight_raw = get_hero_info(hero2_name, 'weight', option=1)

    # split the weighs string to get value for comparison
    weight_list1 = hero1_weight_raw.split()
    weight_list2 = hero2_weight_raw.split()

    # get the first value in the weight lists for comparison
    hero1_weight = weight_list1[0]
    hero2_weight = weight_list2[0]

    if hero1_weight == '-' or hero2_weight == '-':
        print("Cannot compare " + hero1_name + " ("
              + hero1_weight_raw + ") and " + hero2_name + " (" + hero2_weight_raw + ")")

    elif int(hero1_weight) > int(hero2_weight):
        print(hero1_name + " (" + hero1_weight_raw + ") weighs more than " + hero2_name + " (" + hero2_weight_raw + ")")

    elif int(hero1_weight) < int(hero2_weight):
        print(hero2_name + " (" + hero2_weight_raw + ") weighs more than " + hero1_name + " (" + hero1_weight_raw + ")")

    else:
        print(hero1_name + " (" + hero1_weight_raw + ") and "
              + hero2_name + " (" + hero2_weight_raw + ") weigh the same.")


def battle_1v1():

    print('Welcome to battle simulator')

    hero1_name = input('Enter first hero: ').strip()
    hero1_name = get_hero_names(hero1_name)
    print(hero1_name, 'ready for battle\n')

    hero2_name = input('Enter second hero: ').strip()
    hero2_name = get_hero_names(hero2_name)
    print(hero2_name, 'ready for battle\n')

    print('Simulating', hero1_name, 'vs.', hero2_name)

    # get combat scores of the heroes
    hero1_cs = get_hero_info(hero1_name, 'combat_score', option=1)
    hero2_cs = get_hero_info(hero2_name, 'combat_score', option=1)

    # print(hero1_name, '-', hero1_cs, 'vs.', hero2_name, '-', hero2_cs)

    # Compare combat scores
    if int(hero1_cs) > int(hero2_cs):
        # get a random power from the wining hero
        power = random_power(hero1_name)

        # check if the winning hero had any powers
        if not power:
            print(hero1_name, 'defeats', hero2_name)
        else:
            print(hero1_name, 'defeats', hero2_name, 'using', power)

    elif int(hero1_cs) < int(hero2_cs):
        # get a random power from the wining hero
        power = random_power(hero2_name)

        # check if the winning hero had any powers
        if not power:
            print(hero2_name, 'defeats', hero1_name)
        else:
            print(hero2_name, 'defeats', hero1_name, 'using', power)

    else:
        print(hero1_name, 'and', hero2_name, 'are evenly matched')

    print('Battle Over \n')


# get the superpowers or heroes from the data set which are stored as a string in the following form
# ['Agility', 'Audio Control', 'Cryokinesis', 'Electrokinesis', 'Endurance', 'Enhanced Hearing']
def random_power(hero_name):
    list_item_regex = re.compile(r'\'([a-zA-Z\s\-/]+)\'')
    # get string containing powers
    powers_string = get_hero_info(hero_name, 'superpowers', option=1)
    # extract all powers which are surrounded by '' as a list
    powers_list = list_item_regex.findall(powers_string)

    # if hero has no powers return empty string else return a random power
    if not powers_list:
        # print('No powers')
        return ''
    else:
        random_index = random.randrange(len(powers_list))

        return powers_list[random_index]


# get news articles from superherohype website
def get_news():
    # list to contain news articles
    filtered_news = []

    # use beautifulsoup to find superhero news articles
    web_request = requests.get('https://www.superherohype.com/news')
    soup = BeautifulSoup(web_request.content, features='lxml')
    latest_news = soup.find_all('a')

    for news in latest_news:
        links = news.get('href')
        title = news.get('title')
        title = title

        # tuple containing article title and article url
        news_tuple = (title, links)

        # if the article does have a title and is not already in the list add it to list
        if title and news_tuple not in filtered_news:
            filtered_news.append(news_tuple)

    user_input = 'yes'

    while user_input == 'yes':

        num_articles = len(filtered_news)  # get number of avaliable articles

        if num_articles > 5:
            # print 5 articles from list
            for i in range(5):
                print(filtered_news[i][0])
                print(filtered_news[i][1], '\n')

            filtered_news = filtered_news[5:]  # remove the 5 already displayed articles from list

            # show user the remaining articles and ask if they want to see more
            print('Articles Remaining:', len(filtered_news))
            user_input = input('Would you like to see more news? > ')
            print()

        elif num_articles == 0:
            print("No articles available\n")
            break

        else:
            # if there are less than 5 news articles print all
            for i in range(len(filtered_news)):
                print(filtered_news[i][0])
                print(filtered_news[i][1], '\n')

            print("End of available articles\n")
            break


def get_random_history():
    index = random.randint(0, 1450)  # random index of a superhero

    name = heroes_df_csv.at[index, 'name']  # get name of hero

    # dsisplay history
    print('\nThis is the history of', name)
    get_hero_history(name, option=1)


# converts strings that contain list items from the data set to a python list. samples of the strings are
# ['Agility', 'Audio Control', 'Cold Resistance', 'Danger Sense', 'Electrokinesis] - superpowers
# ['Teen Titans', 'New Teen Titans', 'Justice League', 'Outlaws'] - teams
def string_list_convert(list_string):
    # string of the form is ['Agility', 'Audio Control', 'Cold Resistance', 'Danger Sense', 'Electrokinesis]
    list_item_regex = re.compile(r'\'([a-zA-Z\s\-/.]+)\'')

    # extract all powers which are surrounded by '' as a list
    powers_list = list_item_regex.findall(list_string)

    return powers_list
