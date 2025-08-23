from termcolor import colored

def colored_text(text):
    print(colored(f"{text}", "green"))

colored_text("Привет из контейнера!")