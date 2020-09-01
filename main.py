import botresponse as br
import superherodata as sd

import sys
import re


def check_name_possessiveness(hero_name):

    # check if user entered name in a possessive form and get name without the 's or ' if they did
    if name_possessive_form.match(hero_name):
        return name_possessive_form.search(hero_name).group(1)

    return hero_name


if __name__ == '__main__':

    # checks if word/name ends with 's or ', such as Batman's, Abraxas',
    name_possessive_form = re.compile(r'(.*)(\'s|\')')

    # recognize capital names regex, requires that a heroes name be the only capitalized word(s) in question
    capital_words = re.compile(r'\b([A-Z0-9\'][-a-zA-Z0-9]+\s?)\b')

    # decision tree regular expressions
    real_name = re.compile(r'([wW]hat is|[tT]ell me)?(.*) real name')
    superpowers = re.compile(r'([wW])hat powers does (.*) have')
    decribe_powers = re.compile(r'[Dd]escribe (.*) powers')
    overall_score = re.compile(r'([wW]hat is|[tT]ell me)?(.*) overall score\??')
    combat_score = re.compile(r'([wW]hat is|[tT]ell me)?(.*) combat score\??')
    hero_image = re.compile(r'[wW]hat does (.*) look like')
    ability_scores = re.compile(r'([wW]hat are|[tT]ell me)?(.*) ability scores?\??')
    # teams = re.compile(r'what teams (.*)')
    teams = re.compile(r'([wW]hich|[wW]hat) teams? is (.*) (on|a part of)\??')
    birthplace = re.compile(r'[wW]here was (.*) born')
    base_location = re.compile(r'[wW]here is (.*) base')

    # good_or_bad = re.compile(r'[iI]s (.*) (good|bad|evil)|(good or bad)|(good or evil)')

    alignment = re.compile(r'[iI]s (.*) (good or evil|evil or good|bad or good|good or bad)(.*)')

    height = re.compile(r'[hH]ow tall is (.*)')
    ending_quest = re.compile(r'(.*)\?')  # used to remove a trailing ? from the height regex
    weight = re.compile(r'(([hH]ow much does)|([wW]hat does)) (.*) weigh\??')
    hero_history = re.compile(r'[wW]hat is (.*) backstory?')
    occupation = re.compile(r'[wW]hat is (.*) (occupation|job)(.*)')
    relatives = re.compile(r'[wW]ho (are|is) (.*) (relatives|family)(.*)')
    # extract names when input such as Who weighs more Batman or Superman is detected
    weight_compare = re.compile(r'((.*)(weighs more)(.+)\bor\b(.+))\b(.*)')
    battle_1v1 = re.compile(r'([sS]tart [bB]attle)|([bB]attle)')
    latest_news = re.compile(r'(.*)latest(\ssuperhero)?\snews')
    random_hero_story = \
        re.compile(r'(.*)((history|backstory) of a random (hero|superhero))(.*)|(.*)(random (history|backstory))(.*)'
                   r'|(.*)random (.*)(history|backstory)(.*)')

    help_menu = re.compile(r'(.*)help(.*)')

    br.opening()  # display welcome message/bot opening speech

    while True:
        user_input = input("> ")

        if user_input == "exit":
            br.closing()
            sys.exit(0)

        # decision tree
        if real_name.match(user_input):

            name = real_name.search(user_input).group(2).strip()
            name = check_name_possessiveness(name)

            sd.get_real_name(name)

        elif superpowers.match(user_input):

            name = superpowers.search(user_input).group(2)

            sd.get_superpowers(name)

        elif decribe_powers.match(user_input):

            name = decribe_powers.search(user_input).group(1)
            name = check_name_possessiveness(name)

            sd.get_powers_description(name)

        elif overall_score.match(user_input):

            name = overall_score.search(user_input).group(2).strip()
            name = check_name_possessiveness(name)

            sd.get_overall_score(name)

        elif combat_score.match(user_input):

            name = combat_score.search(user_input).group(2).strip()
            name = check_name_possessiveness(name)

            sd.get_combat_score(name)

        elif hero_image.match(user_input):

            name = hero_image.search(user_input).group(1)

            sd.get_hero_image(name)

        elif ability_scores.match(user_input):

            name = ability_scores.search(user_input).group(2).strip()
            name = check_name_possessiveness(name)

            sd.get_ability_scores(name)

        elif teams.match(user_input):
            name = teams.search(user_input).group(2).strip()
            name = check_name_possessiveness(name)

            sd.get_teams(name)

        elif birthplace.match(user_input):
            name = birthplace.search(user_input).group(1)
            name = check_name_possessiveness(name)
            sd.get_birth_place(name)

        elif base_location.match(user_input):
            name = base_location.search(user_input).group(1)
            name = check_name_possessiveness(name)

            sd.get_base(name)

        elif alignment.match(user_input):
            name = alignment.search(user_input).group(1)

            sd.get_alignment(name)

        elif height.match(user_input):
            name = height.search(user_input).group(1)

            if ending_quest.match(name):
                name = ending_quest.search(name).group(1)
            # name = check_name_possessiveness(name)

            sd.get_height(name)

        elif weight.match(user_input):
            name = weight.search(user_input).group(4)

            sd.get_weight(name)

        elif hero_history.match(user_input):
            name = hero_history.search(user_input).group(1)
            name = check_name_possessiveness(name)

            sd.get_hero_history(name)

        elif occupation.match(user_input):
            name = occupation.search(user_input).group(1)
            name = check_name_possessiveness(name)

            sd.get_occupation(name)

        elif relatives.match(user_input):
            name = relatives.search(user_input).group(2)
            name = check_name_possessiveness(name)

            sd.get_relatives(name)

        elif weight_compare.match(user_input):
            names = weight_compare.search(user_input)

            # remove white spaces from the start and end of hero names
            hero1 = names.group(4).strip()
            hero2 = names.group(5).strip()

            sd.weight_comparison(hero1, hero2)

        elif battle_1v1.match(user_input):

            sd.battle_1v1()

        elif latest_news.match(user_input):

            print()
            sd.get_news()

        elif random_hero_story.match(user_input):

            sd.get_random_history()

        elif help_menu.match(user_input):

            br.help_menu()

        else:
            br.input_error_response()

        br.general_response()  # random bot dialog
