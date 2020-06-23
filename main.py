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
    real_name = re.compile(r'(.*) real name')
    superpowers = re.compile(r'(w|W)hat powers does (.*) have')
    overall_score = re.compile(r'(.*) overall score')
    combat_score = re.compile(r'(.*) combat score')
    hero_image = re.compile(r'[wW]hat does (.*) look like')
    ability_scores = re.compile(r'(.*) ability scores')
    # teams = re.compile(r'what teams (.*)')
    teams = re.compile(r'(.*) teams')
    birthplace = re.compile(r'where was (.*) born')
    good_or_bad = re.compile(r'is (.*) (good|bad|evil)|(good or bad)|(good or evil)')
    base_location = re.compile(r'where is (.*) base')
    height = re.compile(r'how tall is (.*)')
    weight = re.compile(r'((how much does)|(what does)) (.*) weigh\??')
    hero_history = re.compile(r'what is (.*) backstory?')

    while True:
        userinput = input("> ")

        if userinput == "exit":
            print("Goodbye")
            sys.exit(0)

        # decision tree
        if real_name.match(userinput):

            name = real_name.search(userinput).group(1)
            name = check_name_possessiveness(name)

            sd.get_real_name(name)

        elif superpowers.match(userinput):

            name = superpowers.search(userinput).group(2)

            sd.get_superpowers(name)

        elif overall_score.match(userinput):

            name = overall_score.search(userinput).group(1)
            name = check_name_possessiveness(name)

            sd.get_overall_score(name)

        elif combat_score.match(userinput):

            name = combat_score.search(userinput).group(1)
            name = check_name_possessiveness(name)

            sd.get_combat_score(name)

        elif hero_image.match(userinput):

            name = hero_image.search(userinput).group(1)

            sd.get_hero_image(name)

        elif ability_scores.match(userinput):

            name = ability_scores.search(userinput).group(1)
            name = check_name_possessiveness(name)

            sd.get_ability_scores(name)

        elif teams.match(userinput):
            name = teams.search(userinput).group(1)
            name = check_name_possessiveness(name)

            sd.get_teams(name)

        elif birthplace.match(userinput):
            name = birthplace.search(userinput).group(1)
            name = check_name_possessiveness(name)
            sd.get_birth_place(name)

        elif base_location.match(userinput):
            name = base_location.search(userinput).group(1)
            name = check_name_possessiveness(name)

            sd.get_base(name)

        elif height.match(userinput):
            name = height.search(userinput).group(1)
            # name = check_name_possessiveness(name)

            sd.get_height(name)

        elif weight.match(userinput):
            name = weight.search(userinput).group(4)

            sd.get_weight(name)

        elif hero_history.match(userinput):
            name = hero_history.search(userinput).group(1)
            name = check_name_possessiveness(name)

            sd.get_hero_history(name)
            print("Hello There", name)

        else:
            print('Error processing input')

