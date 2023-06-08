from protocols import create_suspicion_of_suffocation_from_a_foreign_body_protocol as cs
from voice_features import speak, get_speech_

def search_current_state(current_state, protocol):
    pass  # todo: future implementation


def sent_speech(sentence):
    """
    this is the place to implement text-to-speach
    :param sentence:
    """
    speak(sentence)

def get_speech():
    """
    this is the place to implement speech-to-text
    :return:
    """
    return get_speech_()


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


process_protocol(cs.suspicion_of_suffocation_from_a_foreign_body())
