import superherodata as sd
import sys
import re

if __name__ == '__main__':

    # checks if word/name ends with 's or ', such as Batman's, Abraxas',
    name_possessive_form = re.compile(r'(.*)(\'s|\')')

    # decision tree regular expressions
    real_name = re.compile(r'(.*) real name')
    superpowers = re.compile(r'(w|W)hat powers does (.*) have')
    overall_score = re.compile(r'(.*) overall score')
    combat_score = re.compile(r'(.*) combat score')
    hero_image = re.compile(r'[wW]hat does (.*) look like')

    while True:
        userinput = input("> ")

        if userinput == "exit":
            print("Goodbye")
            sys.exit(0)

        # decision tree
        if real_name.match(userinput):

            name = real_name.search(userinput).group(1)
            # check if user entered name in a possessive form and get name without the 's or ' if they did
            if name_possessive_form.match(name):
                name = name_possessive_form.search(name).group(1)
            sd.get_real_name(name)
        elif superpowers.match(userinput):
            name = superpowers.search(userinput).group(2)
            sd.get_superpowers(name)
        elif overall_score.match(userinput):
            name = overall_score.search(userinput).group(1)
            if name_possessive_form.match(name):
                name = name_possessive_form.search(name).group(1)
            sd.get_overall_score(name)
        elif combat_score.match(userinput):
            name = combat_score.search(userinput).group(1)
            if name_possessive_form.match(name):
                name = name_possessive_form.search(name).group(1)
            sd.get_combat_score(name)
        elif hero_image.match(userinput):
            name = hero_image.search(userinput).group(1)
            sd.get_hero_image(name)
            print("Hello There", name)
