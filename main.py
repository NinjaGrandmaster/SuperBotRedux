import superherodata as sd
import sys
import re

if __name__ == '__main__':

    info = 'superpowers'
    query = "Testing"

    test_name = "Batman's"
    print(test_name)
    temp = test_name.replace("'s", '')
    print(temp)

    # regular expressions
    real_name = re.compile(r'(.*) real name')
    # checks if word/name ends with 's or ', such as Batman's, Abraxas',
    name_possessive_form = re.compile(r'(.*)(\'s|\')')
    superpowers = re.compile(r'(w|W)hat powers does (.*) have')

    while True:
        userinput = input("> ")

        if userinput == "exit":
            print("Goodbye")
            sys.exit(0)
        '''
        hero_name = sd.get_hero_names(userinput)
        sd.get_hero_info(hero_name, info, query)
        test_str01 = sd.get_hero_info(hero_name, info, option=1)
        print(test_str01, type(test_str01))
        '''

        # decision tree
        if real_name.match(userinput):

            name = real_name.search(userinput).group(1)
            # check if user entered name in a possessive form and get name without the 's or ' if they did
            if name_possessive_form.match(name):
                name = name_possessive_form.search(name).group(1)

            sd.get_real_name(name)

        if superpowers.match(userinput):
            name = superpowers.search(userinput).group(2)
            sd.get_superpowers(name)
            print("Hello There", name)
