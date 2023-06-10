from Edge import Edge
from Node import Node
from Protocol import Protocol


def suspicion_of_suffocation_from_a_foreign_body():
    # leaf - perform cpr
    cpr_node = Node("Consider transition to full CPR", False)
    heimlich_to_cpr_edge = Edge(cpr_node, None)

    # perform heimlich
    heimlich_monitoring_node = Node('''Continue performing the Heimlich maneuver or abdominal presses.
Consider performing a laryngoscopy.
Continue monitoring.''', False)
    heimlich_monitoring_node.add_edge(heimlich_to_cpr_edge)

    # option two - there is improvement.
    evacuate_node = Node('''Refer the sitting patient to the nearest hospital.
Continue monitoring and treatment during the evacuation.''', False)

    # decision node - improvement
    improvement_decision_node_2 = Node('''Check, was there an improvement?
    Yes or No?''', True)
    id_2_edge_no = Edge(heimlich_monitoring_node, "no")
    id_2_edge_yes = Edge(evacuate_node, "yes")

    # add option edge to decision node.
    improvement_decision_node_2.add_edge(id_2_edge_no)
    improvement_decision_node_2.add_edge(id_2_edge_yes)

    # heimlich
    heimlich_node = Node("Perform the Heimlich maneuver or abdominal presses.", False)
    # 2 resuscitation
    resuscitation_node = Node("Perform two mouth to mouth resuscitation", False)
    # connect to improvement 2
    to_improvement_2_edge = Edge(improvement_decision_node_2, None)

    # add edge to nodes
    heimlich_node.add_edge(to_improvement_2_edge)
    resuscitation_node.add_edge(to_improvement_2_edge)

    # decision node - improvement 2
    improvement_decision_node_1 = Node('''Check, was there an improvement?
Yes or No?''', True)

    # create decision edges
    id_1_edge_yes = Edge(improvement_decision_node_2, "yes")
    id_1_edge_no = Edge(heimlich_node, "no")

    # add option edge to decision node.
    improvement_decision_node_1.add_edge(id_1_edge_no)
    improvement_decision_node_1.add_edge(id_1_edge_yes)

    # create conscious decision tree

    # massages node
    massages_node = Node("Perform thirty massages", False)
    massages_to_resuscitation_edge = Edge(resuscitation_node, None)
    massages_node.add_edge(massages_to_resuscitation_edge)

    # cough node
    cough_node = Node("Approach the patient and encourage a cough", False)
    cough_to_improvement_1_edge = Edge(improvement_decision_node_1, None)
    cough_node.add_edge(cough_to_improvement_1_edge)

    conscious_decision_node = Node('''Check, is the patient conscious?
    Yes or No?''', True)

    conscious_edge_no = Edge(massages_node, "no")
    conscious_edge_yes = Edge(cough_node, "yes")

    conscious_decision_node.add_edge(conscious_edge_no)
    conscious_decision_node.add_edge(conscious_edge_yes)

    return Protocol(conscious_decision_node)