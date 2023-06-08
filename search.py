from protocols import create_suspicion_of_suffocation_from_a_foreign_body_protocol as cs
from voice_features import speak, get_speech_

def search_current_state(current_state, protocol):
    pass  # todo: future implementation

_session_documentation = list()
def sent_speech(sentence):
    """
    this is the place to implement text-to-speach
    :param sentence:
    """
    _session_documentation.append(dict(
        type="device",
        value=sentence
    ))
    label = tk.Label(window, text=sentence, font=("Arial", 12))
    label.pack()
    window.update()
    speak(sentence)
    return sentence

def get_speech():
    """
    this is the place to implement speech-to-text
    :return:
    """
    text = get_speech_()
    _session_documentation.append(dict(
        type="user",
        value=text
    ))
    label = tk.Label(window, text=text, font=("Arial", 12))
    label.pack()
    window.update()
    return text


def report_to_client():
    performer_name = input("Enter the performer name\n")

    data_time_obj = datetime.now()
    _end_time = data_time_obj.time()
    report_dict = dict(
        start_time=_start_time,
        end_time=_end_time,
        duration=_end_time-_start_time,
        actions=[],
        performer=performer_name,
    )
    import pandas as pd
    return

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
            while get_speech().lower() in \
                    ["yes", "done", "finished", "next", "continue", "what is next", "what is next?"]:  # TODO: allow a wider range of responses
                pass
        # there are more than one option to proceed
        else:
            decision = get_speech()
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
window.geometry("400x300")
label = tk.Label(window, text="Hello Heally!", font=("Arial", 40))
label.pack()
button = tk.Button(window, text="Heally Go!", command=start_runnig)
button.pack()
window.mainloop()

