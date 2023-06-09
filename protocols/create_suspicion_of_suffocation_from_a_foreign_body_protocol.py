from Edge import Edge
from Node import Node
from Protocol import Protocol


def suspicion_of_suffocation_from_a_foreign_body():
    # leaf - perform cpr
    cpr_node = Node("Consider transition to full CPR", False)
    heimlich_to_cpr_edge = Edge(cpr_node, None)

    # perform heimlich
    heimlich_monitoring_node = Node('''so, you should continue performing
    the Heimlich maneuver or abdominal presses.
    you should consider performing a laryngoscopy.
    either way, continue monitoring.''', False)
    heimlich_monitoring_node.add_edge(heimlich_to_cpr_edge)

    # option two - there is improvement.
    evacuate_node = Node('''good, you have to refer
    him or her to the nearest hospital.
    make sure he is sited
    during the evacuation,
    and continue monitoring him.
    When you arrive to the hospital,
    it is required to apply 
    a report about the incident.''', False)

    # decision node - improvement
    improvement_decision_node_2 = Node('''Has your patient's 
    condition improved?''', True)
    id_2_edge_no = Edge(heimlich_monitoring_node, "no")
    id_2_edge_yes = Edge(evacuate_node, "yes")

    # add option edge to decision node.
    improvement_decision_node_2.add_edge(id_2_edge_no)
    improvement_decision_node_2.add_edge(id_2_edge_yes)

    # heimlich
    heimlich_node = Node('''now, you can either
    perform the Heimlich maneuver
    or apply abdominal presses.''', False)
    # 2 resuscitation
    resuscitation_node = Node('''Perform two
    mouth to mouth
    resuscitation''', False)
    # connect to improvement 2
    to_improvement_2_edge = Edge(improvement_decision_node_2, None)

    # add edge to nodes
    heimlich_node.add_edge(to_improvement_2_edge)
    resuscitation_node.add_edge(to_improvement_2_edge)

    # decision node - improvement 2
    improvement_decision_node_1 = Node('''Has your patient's 
    condition improved?''', True)

    # create decision edges
    id_1_edge_yes = Edge(improvement_decision_node_2, "yes")
    id_1_edge_no = Edge(heimlich_node, "no")

    # add option edge to decision node.
    improvement_decision_node_1.add_edge(id_1_edge_no)
    improvement_decision_node_1.add_edge(id_1_edge_yes)

    # create conscious decision tree

    # massages node
    massages_node = Node("Perform thirty heart massages", False)
    massages_to_resuscitation_edge = Edge(resuscitation_node, None)
    massages_node.add_edge(massages_to_resuscitation_edge)

    # cough node
    cough_node = Node('''address the patient 
    and try to make 
    him or her cough
    ''', False)
    cough_to_improvement_1_edge = Edge(improvement_decision_node_1, None)
    cough_node.add_edge(cough_to_improvement_1_edge)

    conscious_decision_node = Node('''Start by checking
     if your patient is conscious.
     Is he?''', True)

    conscious_edge_no = Edge(massages_node, "no")
    conscious_edge_yes = Edge(cough_node, "yes")

    conscious_decision_node.add_edge(conscious_edge_no)
    conscious_decision_node.add_edge(conscious_edge_yes)

    return Protocol(conscious_decision_node)