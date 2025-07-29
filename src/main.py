import json
import os
from datetime import datetime
from typing import TypedDict, List, Dict
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# --- CHARGEMENT DES DONNÉES ET CLÉS API ---

load_dotenv()

if not os.getenv("OPENAI_API_KEY") or not os.getenv("TAVILY_API_KEY"):
    print("Erreur : Assurez-vous d'avoir un fichier .env avec vos clés OPENAI_API_KEY et TAVILY_API_KEY.")
    exit()

try:
    with open('data/images_EST-1.json', 'r', encoding='utf-8') as f:
        images_data = json.load(f)
    with open('data/weather_info.json', 'r', encoding='utf-8') as f:
        weather_data = json.load(f)
except FileNotFoundError as e:
    print(f"Erreur : Le fichier {e.filename} est introuvable.")
    exit()

# --- DÉFINITION DES OUTILS ---

@tool
def get_scene_and_detection_data(image_id: str) -> dict:
    """Récupère les métadonnées et les détections d'une image spécifique."""
    return images_data["images"].get(image_id, {"error": f"Image ID {image_id} non trouvé."})

@tool
def get_weather_conditions(photoset_id: str, timestamp_str: str) -> dict:
    """Récupère les conditions météorologiques pour un chantier à un moment donné."""
    weather_info = weather_data["weather_infos"].get(photoset_id)
    if not weather_info:
        return {"error": f"Photoset ID {photoset_id} non trouvé"}
    shooting_time = datetime.strptime(timestamp_str, '%Y:%m:%d %H:%M:%S')
    closest_hour_str = shooting_time.strftime('%Y-%m-%dT%H:00')
    try:
        idx = weather_info["airquality"]["hourly"]["time"].index(closest_hour_str)
        return {
            "uv_index": weather_info["airquality"]["hourly"]["uv_index"][idx],
            "pm10": weather_info["airquality"]["hourly"]["pm10"][idx],
            "grass_pollen": weather_info["airquality"]["hourly"]["grass_pollen"][idx],
        }
    except (ValueError, IndexError):
        return {"error": f"Heure non trouvée pour le chantier {photoset_id}"}

search_tool = TavilySearchResults(max_results=2, name="tavily_search_results_json")

# ---DÉFINITION DE L'ÉTAT DU GRAPHE ---

class GraphState(TypedDict):
    image_id: str
    photoset_id: str
    image_timestamp: str
    detections: List[Dict]
    weather_conditions: Dict
    identified_risks_with_context: str
    report: str

# --- DÉFINITION DES AGENTS (NŒUDS DU GRAPHE) ---

llm = ChatOpenAI(model="gpt-4o", temperature=0)

def data_analyst_node(state: GraphState):
    """Agent chargé de collecter les données brutes."""
    print("--- 🕵️ Analyste de Données ---")
    image_id = state['image_id']
    scene_data = get_scene_and_detection_data.invoke({"image_id": image_id})
    if scene_data.get("error"):
        print(f"Erreur: {scene_data.get('error')}")
        return
    photoset_id = scene_data['photoset_id']
    timestamp = scene_data['image_shooting']
    detections = scene_data['detections']
    weather_conditions = get_weather_conditions.invoke({
        "photoset_id": str(photoset_id), 
        "timestamp_str": timestamp
    })
    print("Données collectées avec succès.")
    return {
        "photoset_id": photoset_id,
        "image_timestamp": timestamp,
        "detections": detections,
        "weather_conditions": weather_conditions
    }

def safety_expert_node(state: GraphState):
    """Agent expert en sécurité qui identifie les risques et cherche les réglementations."""
    print("--- Expert en Sécurité ---")
    context_for_expert = f"""
    Données d'analyse :
    1. Détections : {json.dumps(state['detections'], indent=2)}
    2. Météo : {json.dumps(state['weather_conditions'])}
    """
    
    prompt = ChatPromptTemplate.from_messages([
    ("system", """Tu es un expert en sécurité sur les chantiers, pragmatique et direct.
    Ta mission est d'identifier les risques immédiats et concrets basés sur les données fournies, en suivant ces priorités :

    **Priorité 1 : Analyser les risques Météo.**
    - Si l'indice UV (`uv_index`) est supérieur à 6 : Identifier un risque d'exposition solaire.
    - Si les particules fines (`pm10`) sont supérieures à 50 µg/m³ : Identifier un risque respiratoire lié à la pollution.
    - Si le pollen (`grass_pollen`) est supérieur à 50 grains/m³ : Identifier un risque d'allergie pour le personnel sensible.

    **Priorité 2 : Analyser les risques liés aux détections.**
    - Cherche les interactions dangereuses entre personnes et machines.
    - Analyse spécifiquement les données de non-port des EPI (`no_ppe`).

    Pour chaque risque identifié :
    1.  **Titre du Risque**: Donne un titre clair et percutant.
    2.  **Justification**: Explique POURQUOI c'est un risque en te basant précisément sur les données.
    3.  **Recommandation**: Propose une action immédiate et concrète.
    4.  **Réglementation**: Utilise l'outil de recherche pour trouver une source pertinente.

    Structure ta réponse finale en texte clair.
    """),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
    
    expert_agent = create_openai_tools_agent(llm, [search_tool], prompt)
    agent_executor = AgentExecutor(agent=expert_agent, tools=[search_tool], verbose=True)
    result = agent_executor.invoke({"input": context_for_expert})
    print("Analyse de l'expert terminée.")
    return {"identified_risks_with_context": result['output']}

def report_generator_node(state: GraphState):
    """Agent qui rédige le rapport final en Markdown."""
    print("--- ✍️ Rédacteur de Rapport ---")
    
    context_for_writer = f"""
    # Informations de Base
    - **ID Image**: {state['image_id']}
    - **Date/Heure**: {state['image_timestamp']}
    - **ID Chantier**: {state['photoset_id']}
    - **Météo**: {json.dumps(state['weather_conditions'])}

    # Analyse de l'Expert
    {state['identified_risks_with_context']}
    """

    report_prompt = f"""Tu es un rédacteur technique. Ta seule mission est de prendre les informations brutes ci-dessous et de les formater en un rapport Markdown propre et professionnel.

    **Consignes de formatage :**
    - Le titre principal doit être `# Rapport d'Analyse de Risques`.
    - Crée une section `## 1. Contexte de l'Analyse`.
    - Crée une section `## 2. Risques Identifiés et Recommandations`.
    - Dans la section 2, chaque risque identifié par l'expert doit être un sous-titre de niveau 3 (ex: `### Risque 1: ...`).
    - Les points "Justification", "Recommandation" et "Source Réglementaire" doivent être en gras.

    Ne modifie pas le contenu de l'analyse de l'expert, contente-toi de le structurer. Ne rajoute aucun commentaire personnel.

    **Informations à formater :**
    {context_for_writer}
    """
    
    final_report = llm.invoke([HumanMessage(content=report_prompt)]).content
    print("Rapport généré.")
    return {"report": final_report}

# ---CONSTRUCTION ET EXÉCUTION DU GRAPHE ---

print("--- Construction du système d'analyse ---")
workflow = StateGraph(GraphState)
workflow.add_node("data_analyst", data_analyst_node)
workflow.add_node("safety_expert", safety_expert_node)
workflow.add_node("report_generator", report_generator_node)
workflow.set_entry_point("data_analyst")
workflow.add_edge("data_analyst", "safety_expert")
workflow.add_edge("safety_expert", "report_generator")
workflow.add_edge("report_generator", END)
app = workflow.compile()

# Lancement de l'analyse
image_id_to_analyze = "660909540_4807b3cf-c44c-425b-8147-ac83497cc831.jpg"
inputs = {"image_id": image_id_to_analyze}
final_state = app.invoke(inputs)

print("\n\n---  RAPPORT FINAL ---")
print(final_state['report'])