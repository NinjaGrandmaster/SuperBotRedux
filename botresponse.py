import random

from colorama import Fore, Style


def rand_index(num):
    return random.randrange(num)


# prints text as light cyan. This method should only be used to display bot dialog.
def bot_print(text):
    print(Fore.LIGHTCYAN_EX + text + Style.RESET_ALL)


# prints text as light blue
def paragraph_print(text):
    print(Fore.LIGHTBLUE_EX + text + Style.RESET_ALL)


# prints passed in text as light yellow
def menu_print(text):
    print(Fore.LIGHTYELLOW_EX + text + Style.RESET_ALL)


def help_menu():

    help_response_list = ['\nHere are my available functions.',
                          '\nTheses are the types of questions my creators enabled me to answer.',
                          '\nHere is what I can answer.',
                          '\nNo problem here are my capabilities.']

    index = rand_index(len(help_response_list))

    # print(Fore.LIGHTCYAN_EX + help_response_list[index])
    bot_print(help_response_list[index])

    print(Fore.LIGHTYELLOW_EX)
    print("-------------------------HELP-----------------------------")
    print("| There are numerous ways in which you can use Super Bot!|")
    print("| You can type/enter input such as:                      |")
    print("|                                                        |")
    print("| what powers does (Heroname) have?                      |")
    print("| describe (Heroname)'s powers                           |")
    print("| what does (Heroname) look like?                        |")
    print("| what is (Heroname) occupation/job?                     |")
    print("| tell me the history of a random superhero              |")
    print("| who are (Heroname) relatives?                          |")
    print("| what is/tell me (Heroname) real name?                  |")
    print("| what is/tell me (Heroname) overall score?              |")
    print("| what is/tell me (Heroname) combat score?               |")
    print("| what are/tell me (Heroname) ability scores?            |")
    print("| what teams is (Heroname) on?                           |")
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


def closing():

    closing_response = ['Goodbye',
                        'See you next time',
                        'Thanks for stopping by. Have a nice day',
                        'Time for a nap',
                        'Systems shutting down']

    index = rand_index(len(closing_response))

    bot_print('\n' + closing_response[index] + '\n')


def input_error_response():

    error_response_list = ['Error Processing input',
                           'Sorry, I did not understand your input',
                           'Sorry, I am still learning to process human input can you repeat your input.',
                           'I did not understand input, please check the spelling of your input.',
                           'Input Error. Type help me to see examples of valid input']

    index = rand_index(len(error_response_list))

    bot_print('\n' + error_response_list[index] + '\n')


def general_response():

    general_dialog = ['How else may I assist you?',
                      'Hope this information was useful',
                      'Interesting information don\'t you think',
                      'Dispatching additional recon drones']

    index = rand_index(len(general_dialog))

    bot_print('\n' + general_dialog[index] + '\n')
