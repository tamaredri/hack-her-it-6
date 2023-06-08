from Edge import Edge
from Node import Node
from Protocol import Protocol


def pain_treatment():
    #preform medical advice
    medical_advice_node = Node("Medical advice in case of need for unusual doses", False)
    monitoring_to_advice = Edge(medical_advice_node, None)

    #preform monitoring
    monitoring_node = Node('''Continue monitoring or treatment while being evacuated to the hospital
Repeat pain assessment every 5-10 minutes
Treat according to the findings and the pharmacological indications''', False)
    nausea_to_monitoring = Edge(monitoring_node, "no")
    pramin_to_monitoring = Edge(monitoring_node, None)
    monitoring_node.add_edge(monitoring_to_advice)

    #preform pramin
    pramin_node = Node('''Consider IV pramin
Consider giving Durumikum I''', False)
    nausea_to_pramin = Edge(pramin_node, "yes")
    pramin_node.add_edge(pramin_to_monitoring)

    #decision node- nausea
    nausea_node = Node("Does the patient suffer from nausea, hallucinations or restlessness?", True)
    paracetamol_to_nausea = Edge(nausea_node, None)
    opthalgin_to_nausea = Edge(nausea_node, None)
    morphine_to_nausea = Edge(nausea_node, None)
    nausea_node.add_edge(nausea_to_monitoring)
    nausea_node.add_edge(nausea_to_pramin)

    #preform paracetamol
    paracetamol_node = Node("Paracetamol or Opthalgin PO", False)
    mild_pain_to_paracetamol = Edge(paracetamol_node, "mild pain")
    paracetamol_node.add_edge(paracetamol_to_nausea)

    #preform opthalgin
    opthalgin_node = Node("Opthalgin or Tramdex PO", False)
    moderate_pain_to_opthalgin = Edge(opthalgin_node, "moderate pain")
    opthalgin_node.add_edge(opthalgin_to_nausea)

    #preform morphine
    morphine_node = Node("Morphine or fentanyl combined with IV ketamine or IN/IM fentanyl", False)
    strong_pain_to_morphine = Edge(morphine_node, "strong pain")
    morphine_node.add_edge(morphine_to_nausea)

    #preform assessment
    assessment_node = Node("Assess the intensity of the pain", True)
    first_aid_to_assessment = Edge(assessment_node, None)
    assessment_node.add_edge(mild_pain_to_paracetamol)
    assessment_node.add_edge(moderate_pain_to_opthalgin)
    assessment_node.add_edge(strong_pain_to_morphine)

    #preform first aid
    first_aid_node = Node("Give initial treatment to reduce pain if possible", False)
    priorities_to_first_aid = Edge(first_aid_node, None)
    first_aid_node.add_edge(first_aid_to_assessment)

    #preform priorities
    priorities_node = Node("Perform a C-B-A assessment and treat accordingly - in order of priority", False)
    priorities_node.add_edge(priorities_to_first_aid)

    return Protocol(priorities_node)