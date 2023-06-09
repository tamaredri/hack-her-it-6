import string
import string
l=[]
from PIL import ImageTk, Image
from sentence_transformers import SentenceTransformer
import torch
from torch import nn

from protocols.pain_treatment import pain_treatment
from voice_features import speak, listen
from protocols.create_suspicion_of_suffocation_from_a_foreign_body_protocol \
    import suspicion_of_suffocation_from_a_foreign_body
from protocols.threatening_cessation_of_breathing \
    import threatening_cessation_of_breathing


def find_protocol():
    protocol = get_complex_speech(
        ['impending respiratory arrest', 'suspicion of suffocation from a foreign body', 'pain treatment'])
    protocol_function = get_protocol_func(protocol)
    #sent_speech("your protocol is " + protocol[1] + ". ok?")
    #answer = get_complex_speech(["yes", "no"])


    #while answer[1] == "no":
    #    sent_speech("So, tell me again, what is your situation?")
    #    protocol = get_complex_speech(
    #        ['impending respiratory arrest', 'suspicion of suffocation from a foreign body', 'pain treatment'])
    #    protocol_function = get_protocol_func(protocol)
    #    sent_speech("your protocol is " + protocol[1] + ". ok?")
    #    answer = get_complex_speech(["yes", "no"])

    return protocol_function()


def get_protocol_func(protocol):
    protocol_function = {
        'impending respiratory arrest': threatening_cessation_of_breathing,
        'suspicion of suffocation from a foreign body': suspicion_of_suffocation_from_a_foreign_body,
        'pain treatment': pain_treatment
    }.get(protocol[1])
    return protocol_function


def search_current_state(current_state, protocol):
    pass  # todo: future implementation



_session_documentation = list()
#_labels_list = list()
#def show_labels(label, new_text):
#    _labels_list.append(label)
#    if len(_labels_list) > 3:
#        _labels_list.pop(0).config(text=new_text)

import tkinter as tk

window = tk.Tk()
window.geometry("800x800")
label = tk.Label(window, text='', font=("Arial", 20))
text = ''

def sent_speech(sentence):
    """
    this is the place to implement text-to-speach
    :param sentence:
    """
    _session_documentation.append(dict(
        type="Heally",
        value=sentence
    ))
    #label = tk.Label(window, text=sentence, font=("Arial", 20))
    label.config(text=text+'\n'+sentence)
    #show_labels(label, sentence)
    #label.pack()
    speak(sentence)
    l.append(label)

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
            #label = tk.Label(window, text=word, font=("Arial", 20))
            #show_labels(label)
            #label.pack()

            _session_documentation.append(dict(
                type="user",
                value=word
            ))
            return word
    return None


def get_complex_speech(sentence_to_continue):
    """
    this is the place to implement speech-to-text
    :return:
    """
    model = SentenceTransformer('whaleloops/phrase-bert')
    new_sentence = listen(5)  # list of words.
    new_sentence = model.encode(new_sentence)

    maximum = [-1, '']
    cos_sim = nn.CosineSimilarity(dim=0)

    for sentence in sentence_to_continue:
        encoded_sentence = model.encode(sentence)
        cos_val = cos_sim(torch.tensor(new_sentence), torch.tensor(encoded_sentence))
        if cos_val > maximum[0]:
            maximum = [cos_val, sentence]
    print(maximum[1])
    return maximum


def get_simple_speech(word_to_continue):
    sentence = clean_sentence(listen(4))  # list of words.new_sentence = listen() # list of words.
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
            actions=[val if l == "Heally" else "=> " + val for t in _session_documentation for (l, val) in t.key()],
            performer=performer_name,
    )
    #image = tk.Image.open("C:\\Users\\menashe\\Downloads\\im.png")
    #image = image.resize((100, 200))
    #photo = ImageTk.PhotoImage(image)
    #label = tk.Label(window, image=photo)
    #label.pack()
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
            get_simple_speech(["yeah","yes", "done", "ok","okay", "finished", "next", "continue", "what is next","did","good"])
            pass

        # there are more than one option to proceed
        else:
            decision = get_simple_speech([edge.value for edge in current_node.edges])
            # find the next node
            for edge in current_node.edges:
                if edge.value == decision:
                    current_edge = edge
                    '''label = tk.Label(window, text=decision, font=("Arial", 20))
                    show_labels(label)
                    label.pack()'''
                    _session_documentation.append(
                        dict(
                            type="user",
                            value=decision
                        )
                    )
                    break

        current_node = current_edge.next
    sent_speech(current_node.value)
    sent_speech("Good job, your protocol is finished. Thank you for making our world a better place!")

from datetime import datetime
_start_time = None
def start_runnig():
    button.destroy()
    data_time_obj = datetime.now()
    _start_time = data_time_obj.time()
    #label = tk.Label(window, text="what is your situation?",font=("Arial", 20))
    #show_labels(label)
    #label.pack()
    sent_speech("Hello Paramedic, tell me what happened?")
    process_protocol(find_protocol())

#image = Image.open("C:\\Users\\menashe\\Downloads\\logo.png")
#image = image.resize((300, 140))
#photo = ImageTk.PhotoImage(image)
#label = tk.Label(window, image=photo)
#label.pack()
button = tk.Button(window, text="Start", command=start_runnig)
button.pack()
window.mainloop()
process_protocol(find_protocol())
