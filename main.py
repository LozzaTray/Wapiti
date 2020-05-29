"""Main program Loop"""
from src.make_recording import run as make_recording
from src.open_recording import run as open_recording
from src.encode_transmission import run as encode_transmission
from src.decode_transmission import run as decode_transmission
from src.correlate import run as correlate
from src.channel_estimator import run as estimate_channel
from src.simulate_channel import run as simulate_channel
from src.gen_standard_chirp import run as gen_standard_chirp


options = {
    "1": "Make Recording",
    "2": "Open Recording",
    "3": "Encode Transmission",
    "4": "Decode Transmission",
    "5": "Correlate Recordings",
    "6": "Estimate Channel",
    "7": "Simulate Channel",
    "8": "Generate Chirp",
    "q": "Quit"
}

def get_option_with_prompt():
    print("Wapiti - Menu:")
    for (key, val) in options.items():
        print(key + ") " + val)

    while (True):
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
            encode_transmission()
        elif (option == "4"):
           decode_transmission()
        elif (option == "5"):
            correlate()
        elif (option == "6"):
            estimate_channel()
        elif (option == "7"):
            simulate_channel()
        elif (option == "8"):
            gen_standard_chirp()

    print("Quitting")




if (__name__ == "__main__"):
    print("Team Wapiti - Audio Modem\n~~~~~~~~~~~~~~~~~~~~~~~\n")
    run()
