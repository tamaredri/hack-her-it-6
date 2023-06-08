from Edge import Edge
from Node import Node
from Protocol import Protocol
from protocols.pain_treatment import pain_treatment


def injured_by_a_poisonous_animal():
    #preform medical advice
    medical_advice_node = Node("Medical advice in case of need for unusual doses", False)
    monitoring_to_advice = Edge(medical_advice_node, None)

    # preform monitoring
    monitoring_node = Node('''Continue monitoring or treatment while quickly evacuating to the nearest hospital
Re-evaluate metrics every 10 minutes
Do a full ECG
Treat according to the findings''', False)
    pain_treatment_protocol_to_monitoring = Edge(monitoring_node, "no")
    pain_to_monitoring = Edge(monitoring_node, "no")
    monitoring_node.add_edge(monitoring_to_advice)

    # preform pain protocol
    pain_protocol_node = pain_treatment().root
    protocol_dec_to_pain_protocol = Edge(pain_protocol_node, "yes")

    dec_prot = Node('''The pain protocol must be followed.
Would you like to switch to it?''', True)
    pain_to_pain_protocol = Edge(dec_prot, "yes")
    dec_prot.add_edge(pain_treatment_protocol_to_monitoring)
    dec_prot.add_edge(protocol_dec_to_pain_protocol)




    #decision node- pain
    pain_node = Node("Does the patient feel pain?", True)
    actions_to_pain = Edge(pain_node, None)
    pain_node.add_edge(pain_to_monitoring)
    pain_node.add_edge(pain_to_pain_protocol)

    #preform action
    action_node = Node('''Keep the victim away from the danger zone.
Perform a C-B-A assessment and treat accordingly - in order of priority.
Lay the victim in full rest, including 4 limbs.
Set up an intravenous or breast infusion, not in the affected limb, and consider the need for fluid infusion.
Remove jewelry from the affected limb, and perform local cleaning or disinfection such as rinsing with water.
Try to get an accurate description of the snake or scorpion or take a picture of it.
If possible, mark the bite or bite area.''', False)
    action_node.add_edge(actions_to_pain)

    return Protocol(action_node)