from Edge import Edge
from Node import Node
from Protocol import Protocol


def threatening_cessation_of_breathing():
    #leaf- go to the hospital
    hosp_node = Node("Go to the hospital urgently and report to the emergency medical center", False)
    recuronium_to_hosp_edge = Edge(hosp_node, None)
    quick_trach_to_hosp_edge = Edge(hosp_node, None)

    #preform recuronium
    recuronium_node = Node('''Consider giving IV recuronium
Consider giving duromix or ketamine to maintain sedation
Consider giving opiates for pain management''', False)
    recuronium_node.add_edge(recuronium_to_hosp_edge)
    tubus_to_recuronium = Edge(recuronium_node, None)

    #prefrom quick trach
    quick_trach_node = Node("Consider doing a quick trach", False)
    quick_trach_node.add_edge(quick_trach_to_hosp_edge)

    #decision node- chest rises
    chest_rises = Node("Does the chest rise? Yes or No?", True)
    chest_rises_to_hosp_edge = Edge(hosp_node, "yes")
    chest_not_rises_to_hosp_edge = Edge(quick_trach_node, "no")
    airway_to_chest_rises = Edge(chest_rises, None)

    chest_rises.add_edge(chest_not_rises_to_hosp_edge)
    chest_rises.add_edge(chest_rises_to_hosp_edge)


    #preform tubus
    tubus_node = Node('''Verify the location of the bus
Determined Tubus
Continue the breath, consider connecting to the breath''', False)
    tubus_node.add_edge(tubus_to_recuronium)

    #preform airway
    airway_node = Node('''Consider inserting a supraglottic airway
Breathe using a bellows and mask''', False)
    airway_node.add_edge(airway_to_chest_rises)

    #decision node- intubation success
    intubation_success_node = Node("Was intubation successful?", True)
    intubation_was_successful = Edge(tubus_node, "yes")
    intubation_was_not_successful = Edge(airway_node, "no")
    intubation_to_intubation_success = Edge(intubation_success_node, None)

    intubation_success_node.add_edge(intubation_was_not_successful)
    intubation_success_node.add_edge(intubation_was_successful)

    #preform intubation
    intubation_node = Node('''Perform intubation
Up to 3 attempts, with at least one of them using BOUGIE''', False)
    sedation_to_intubation = Edge(intubation_node, None)
    intubation_node.add_edge(intubation_to_intubation_success)

    #preform sedation
    sedation_node = Node("Sedate with IV Etomidate and/or Duramicom and/or Ketamine", False)
    peroxygenation_to_sedation = Edge(sedation_node, None)
    sedation_node.add_edge(sedation_to_intubation)

    #preform Peroxygenation
    peroxygenation_node = Node("Perform passive or active peroxygenation", False)
    peroxygenation_node.add_edge(peroxygenation_to_sedation)

    return Protocol(peroxygenation_node)

