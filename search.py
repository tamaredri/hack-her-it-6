import string
from tkinter import Tk, Label
from PIL import ImageTk, Image
from protocols import create_suspicion_of_suffocation_from_a_foreign_body_protocol as cs
from voice_features import speak, listen


def find_protocol(sentence_with_protocol_name):
    pass


def search_current_state(current_state, protocol):
    pass  # todo: future implementation

_session_documentation = list()
def sent_speech(sentence):
    """
    this is the place to implement text-to-speach
    :param sentence:
    """
    _session_documentation.append(dict(
        type="Heally",
        value=sentence
    ))
    label = tk.Label(window, text=sentence, font=("Arial", 12))
    label.pack()
    window.update()
    speak(sentence)
    return sentence

def clean_sentence(sentence):
    """
    remove parenthesis from the sentence, return an array of words.
    :param sentence: string with parenthesis.
    :return: array of words.
    """
    punctuation = string.punctuation
    punctuation = str.maketrans("", "", punctuation)
    no_punctuation = sentence.translate(punctuation).lower()
    return no_punctuation.strip().split()


def get_common_word(array_a, array_b):
    """
    get the word that appears in both arrays
    :param array_a:
    :param array_b:
    :return:
    """
    for word in array_a:
        if word in array_b:
            return word
    return None


def get_speech(word_to_continue):
    """
    this is the place to implement speech-to-text
    :return:
    """
    sentence = clean_sentence(listen())  # list of words.
    answer = get_common_word(sentence, word_to_continue)  # get the answer if there is.

    while answer is None:
        sent_speech("sorry, tell me again")
        sentence = clean_sentence(listen())
        answer = get_common_word(sentence, word_to_continue)

    return answer

def report_to_client():
    performer_name = input("Enter the performer name\n")

    data_time_obj = datetime.now()
    _end_time = data_time_obj.time()
    report_dict = dict(
            start_time=_start_time,
            end_time=_end_time,
            duration=_end_time - _start_time,
            actions=[val if l == "device" else "=> " + val for t in _session_documentation for (l, val) in t.key()],
            performer=performer_name,
    )
    image = Image.open("C:\\Users\\menashe\\Downloads\\im.png")
    image = image.resize((100, 200))
    photo = ImageTk.PhotoImage(image)
    label = Label(window, image=photo)
    label.pack()
    with open("report.txt", "w") as f:
         for (key, val) in report_dict.keys():
            if not isinstance(val, list):
                f.write(f"{key}: {val}\n")
            else:
                f.write(f"session history:\n")
                f.writelines(val)


def process_protocol(protocol):
    current_node = protocol.root
    # until current_node holds a leaf value
    while len(current_node.edges) > 0:

        # say what is the current action to preform
        sent_speech(current_node.value)
        # get the path to the next action
        current_edge = current_node.edges[0]

        # there is one option to proceed
        if not current_node.is_decision_node:
            get_speech(["yes", "done", "finished", "next", "continue", "what is next", "what is next?"])
            pass

        # there are more than one option to proceed
        else:
            decision = get_speech([edge.value for edge in current_node.edges])
            # find the next node
            for edge in current_node.edges:
                if edge.value == decision:
                    current_edge = edge
                    break

        current_node = current_edge.next
    report_to_client()

from datetime import datetime
_start_time = None
def start_runnig():
    data_time_obj = datetime.now()
    _start_time = data_time_obj.time()
    process_protocol(cs.suspicion_of_suffocation_from_a_foreign_body())

import tkinter as tk
window = tk.Tk()
window.geometry("400x800")
image = Image.open("C:\\Users\\menashe\\Downloads\\logo.png")
image = image.resize((300, 140))
photo = ImageTk.PhotoImage(image)
label = Label(window, image=photo)
label.pack()
button = tk.Button(window, text="Start", command=start_runnig)
button.pack()
window.mainloop()

