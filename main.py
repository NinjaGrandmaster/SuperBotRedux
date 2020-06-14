import superherodata as sd
import sys

if __name__ == '__main__':

    info = 'superpowers'
    query = "Testing"

    while True:
        userinput = input("Enter a Hero name: ")

        if userinput == "exit":
            print("Goodbye")
            sys.exit(0)

        hero_name = sd.get_hero_names(userinput)
        sd.get_hero_info(hero_name, info, query)
        test_str01 = sd.get_hero_info(hero_name, info, option=1)
        print(test_str01, type(test_str01))
