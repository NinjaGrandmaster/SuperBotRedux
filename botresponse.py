import random

from colorama import Fore, Style


def rand_index(num):
    return random.randrange(num)


def help_menu():

    help_response_list = ['\nHere are my available functions.\n',
                          '\nTheses are the types of questions my creators enabled me to answer.\n',
                          '\nHere is what I can answer.\n',
                          '\nNo problem here are my capabilities.\n']

    index = rand_index(len(help_response_list))

    print(Fore.LIGHTCYAN_EX + help_response_list[index])

    print(Fore.LIGHTYELLOW_EX + "-------------------------HELP-----------------------------")
    print("| There are numerous ways in which you can use Super Bot!|")
    print("| You can type/enter input such as:                      |")
    print("|                                                        |")
    print("| what powers does (Heroname) have?                      |")
    print("| describe (Heroname)'s powers                           |")
    print("| what does (Heroname) look like?                        |")
    print("| what is (Heroname) occupation/job?                     |")
    print("| give me the history on a random hero.                  |")
    print("| who are (Heroname) relatives?                          |")
    print("| what is/tell me (Heroname) real name?                  |")
    print("| what is/tell me (Heroname) overall score?              |")
    print("| what is/tell me (Heroname) combat score?               |")
    print("| what are/tell me (Heroname) ability scores?            |")
    print("| what teams is (HeroName) on?                           |")
    print("| where was (Heroname) born?                             |")
    print("| is (Heroname) good or evil?                            |")
    print("| where is (Heroname) base?                              |")
    print("| how tall is (Heroname)?                                |")
    print("| how much does (Heroname) weigh?                        |")
    print("| what is (Heroname) backstory?                          |")
    print("| who weighs more (Heroname) or (Heroname)?              |")
    print("| start battle                                           |")
    print("| what is the latest superhero news?                     |")
    print("----------------------------------------------------------")
    print(Style.RESET_ALL)


def opening():
    welcome_msg = 'Hello I am superbot\nI know a lot about super heroes\nFeel free to ask me a question\n' \
                  'If you are new around here just ask me for help\n'

    print(Fore.LIGHTCYAN_EX + welcome_msg + Style.RESET_ALL)
