"""Main program Loop"""
from src.make_recording import run as make_recording
from src.open_recording import run as open_recording
from src.play_chirp import run as gen_chirp
from src.concatenate import run as concatenate
from src.correlate import run as correlate
from src.channel_script import run as estimate_channel
from src.decode_csv import run as decode_csv


options = {
    "1": "Make Recording",
    "2": "Open Recording",
    "3": "Generate chirp",
    "4": "Concatenate Recordings",
    "5": "Correlate Recordings",
    "6": "Decode csv",
    "7": "Estimate channel",
    "q": "Quit"
}

def get_option_with_prompt():
    print("Wapiti - Menu:")
    for (key, val) in options.items():
        print(key + ") " + val)

    option = input("Enter your choice: ")
    if option in options.keys():
        return option
    else:
        print("Invalid Input. Please try again\n")


def run():
    option = ""
    while(option != "q"):
        option = get_option_with_prompt()

        if (option == "1"):
            make_recording()
        elif (option == "2"):
            open_recording()
        elif (option == "3"):
            gen_chirp()
        elif (option == "4"):
           concatenate()
        elif (option == "5"):
            correlate()
        elif (option == "6"):
            decode_csv()
        elif (option == "7"):
            estimate_channel()

    print("Quitting")




if (__name__ == "__main__"):
    print("Team Wapiti - Audio Modem\n~~~~~~~~~~~~~~~~~~~~~~~\n")
    run()
