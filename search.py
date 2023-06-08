import string
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
    protocol_function = {
        'impending respiratory arrest': threatening_cessation_of_breathing,
        'suspicion of suffocation from a foreign body': suspicion_of_suffocation_from_a_foreign_body,
        'pain treatment': pain_treatment
    }.get(protocol[1])
    speak("your protocol is " + protocol[1])
    return protocol_function()


def search_current_state(current_state, protocol):
    pass  # todo: future implementation


def sent_speech(sentence):
    """
    this is the place to implement text-to-speach
    :param sentence:
    """
    speak(sentence)


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
            get_simple_speech(["yes", "done", "ok", "finished", "next", "continue", "what is next", "what is next?"])
            pass

        # there are more than one option to proceed
        else:
            decision = get_simple_speech([edge.value for edge in current_node.edges])
            # find the next node
            for edge in current_node.edges:
                if edge.value == decision:
                    current_edge = edge
                    break

        current_node = current_edge.next
    sent_speech(current_node.value)
    sent_speech("good job, your protocol is finished")


speak("what is your situation?")
process_protocol(find_protocol())
