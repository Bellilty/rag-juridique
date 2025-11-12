"""
Interface Gradio pour l'Assistant Juridique RAG
===============================================

Interface utilisateur simple et élégante pour interagir avec l'API FastAPI.

Usage :
    python ui.py
"""

import gradio as gr
import requests
from typing import Tuple
import json


# Configuration de l'API
API_URL = "http://localhost:8000"


def check_api_status() -> str:
    """Vérifie si l'API est accessible."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("index_loaded"):
                return "✅ API opérationnelle"
            else:
                return "⚠️ API démarrée mais index non chargé"
        else:
            return "❌ API non accessible"
    except Exception as e:
        return f"❌ Erreur : {str(e)}"


def get_stats() -> str:
    """Récupère les statistiques de l'index."""
    try:
        response = requests.get(f"{API_URL}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            stats = f"""
📊 **Statistiques de l'index**

• **Nombre total de chunks :** {data['total_chunks']}
• **Vecteurs dans l'index :** {data['total_vectors']}
• **Documents sources :** {len(data['sources'])}

**Sources disponibles :**
"""
            for source in data['sources']:
                stats += f"\n  • {source}"
            
            return stats
        else:
            return "❌ Impossible de récupérer les statistiques"
    except Exception as e:
        return f"❌ Erreur : {str(e)}"


def ask_question(question: str, num_chunks: int, model: str) -> Tuple[str, str, str]:
    """
    Pose une question à l'API et retourne la réponse formatée.
    
    Args:
        question: La question à poser
        num_chunks: Nombre de chunks de contexte (k)
        model: Modèle OpenAI à utiliser
        
    Returns:
        Tuple (réponse, sources, métadonnées)
    """
    if not question or not question.strip():
        return "⚠️ Veuillez poser une question", "", ""
    
    try:
        # Appel à l'API
        response = requests.get(
            f"{API_URL}/ask",
            params={
                "query": question,
                "k": num_chunks,
                "model": model
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Formate la réponse
            answer = f"💬 **Réponse :**\n\n{data['answer']}"
            
            # Formate les sources
            sources_list = list(set(data['sources']))  # Déduplique
            sources = "📚 **Sources utilisées :**\n\n"
            for i, source in enumerate(sources_list, 1):
                sources += f"{i}. {source}\n"
            
            # Formate les métadonnées
            cost = data['estimated_cost']
            metadata = f"""
🔢 **Métadonnées :**

• **Modèle :** {data['model']}
• **Chunks utilisés :** {data['num_chunks_used']}
• **Tokens :** {data['tokens_used']['total']} (input: {data['tokens_used']['prompt']}, output: {data['tokens_used']['completion']})
• **Coût estimé :** ${cost['total_cost_usd']:.6f} USD

💰 **Détail des coûts :**
• Input : ${cost['input_cost_usd']:.6f}
• Output : ${cost['output_cost_usd']:.6f}
"""
            
            return answer, sources, metadata
            
        elif response.status_code == 503:
            return "❌ L'API n'est pas prête. Vérifie que l'index est créé.", "", ""
        else:
            return f"❌ Erreur {response.status_code} : {response.text}", "", ""
            
    except requests.exceptions.Timeout:
        return "⏱️ La requête a pris trop de temps. Réessaye.", "", ""
    except requests.exceptions.ConnectionError:
        return "❌ Impossible de se connecter à l'API. Est-elle lancée ? (uvicorn src.api:app --reload)", "", ""
    except Exception as e:
        return f"❌ Erreur : {str(e)}", "", ""


def create_interface():
    """Crée l'interface Gradio."""
    
    # Vérifie le statut de l'API au démarrage
    api_status = check_api_status()
    
    # Thème personnalisé
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
    )
    
    with gr.Blocks(theme=theme, title="Assistant Juridique RAG") as demo:
        
        # En-tête
        gr.Markdown("""
# 🤖 Assistant Juridique RAG
### Posez vos questions sur les documents juridiques français

Cet assistant utilise le **RAG (Retrieval-Augmented Generation)** pour répondre à vos questions
en se basant sur les documents juridiques indexés (Constitution française, Droit du travail, etc.).
""")
        
        # Statut de l'API
        with gr.Row():
            status_text = gr.Markdown(f"**Statut de l'API :** {api_status}")
            refresh_btn = gr.Button("🔄 Rafraîchir le statut", size="sm")
        
        gr.Markdown("---")
        
        # Zone principale
        with gr.Row():
            with gr.Column(scale=2):
                # Zone de question
                question_input = gr.Textbox(
                    label="📝 Votre question",
                    placeholder="Ex: Quels sont les pouvoirs du Président de la République ?",
                    lines=3
                )
                
                # Paramètres avancés
                with gr.Accordion("⚙️ Paramètres avancés", open=False):
                    num_chunks = gr.Slider(
                        minimum=1,
                        maximum=10,
                        value=3,
                        step=1,
                        label="Nombre de chunks de contexte (k)",
                        info="Plus élevé = plus de contexte mais réponse potentiellement moins précise"
                    )
                    
                    model_choice = gr.Radio(
                        choices=["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"],
                        value="gpt-4o-mini",
                        label="Modèle OpenAI",
                        info="gpt-4o-mini recommandé (meilleur rapport qualité/prix)"
                    )
                
                # Boutons
                with gr.Row():
                    submit_btn = gr.Button("🚀 Poser la question", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ Effacer", size="lg")
                
                # Exemples de questions
                gr.Examples(
                    examples=[
                        ["Qu'est-ce que la Constitution française ?"],
                        ["Quels sont les pouvoirs du Président de la République ?"],
                        ["Qu'est-ce que le droit du travail ?"],
                        ["Quelle est la devise de la République française ?"],
                        ["Comment est organisé le Parlement français ?"],
                        ["Qu'est-ce que la Déclaration des Droits de l'Homme ?"],
                    ],
                    inputs=question_input,
                    label="💡 Exemples de questions"
                )
            
            with gr.Column(scale=3):
                # Réponse
                answer_output = gr.Markdown(label="Réponse")
                
                # Sources et métadonnées
                with gr.Row():
                    with gr.Column():
                        sources_output = gr.Markdown(label="Sources")
                    with gr.Column():
                        metadata_output = gr.Markdown(label="Métadonnées")
        
        gr.Markdown("---")
        
        # Statistiques de l'index
        with gr.Accordion("📊 Statistiques de l'index", open=False):
            stats_output = gr.Markdown(get_stats())
            stats_refresh_btn = gr.Button("🔄 Rafraîchir les statistiques")
        
        # Footer
        gr.Markdown("""
---
### 📚 Comment ça marche ?

1. **Tu poses une question** sur un sujet juridique
2. **L'API recherche** les passages pertinents dans les documents indexés avec FAISS
3. **Le LLM génère** une réponse basée uniquement sur ces passages
4. **Les sources sont citées** pour vérifier les informations

💡 **Astuce :** Plus ta question est précise, meilleure sera la réponse !

⚠️ **Important :** L'assistant répond uniquement basé sur les documents indexés. 
Si l'information n'est pas dans les documents, il le dira.
""")
        
        # Actions des boutons
        submit_btn.click(
            fn=ask_question,
            inputs=[question_input, num_chunks, model_choice],
            outputs=[answer_output, sources_output, metadata_output]
        )
        
        clear_btn.click(
            fn=lambda: ("", "", "", ""),
            inputs=[],
            outputs=[question_input, answer_output, sources_output, metadata_output]
        )
        
        refresh_btn.click(
            fn=lambda: f"**Statut de l'API :** {check_api_status()}",
            inputs=[],
            outputs=[status_text]
        )
        
        stats_refresh_btn.click(
            fn=get_stats,
            inputs=[],
            outputs=[stats_output]
        )
    
    return demo


if __name__ == "__main__":
    print("\n" + "="*80)
    print("  🚀 Lancement de l'interface Gradio pour l'Assistant Juridique RAG")
    print("="*80 + "\n")
    
    # Vérifie que l'API est accessible
    print("🔍 Vérification de l'API...")
    status = check_api_status()
    print(f"   {status}\n")
    
    if "❌" in status:
        print("⚠️  L'API n'est pas accessible !")
        print("   Lance-la d'abord avec : uvicorn src.api:app --reload\n")
        print("   Puis relance cette interface.\n")
        exit(1)
    
    # Lance l'interface
    demo = create_interface()
    
    print("✅ Interface prête !\n")
    print("📖 L'interface s'ouvrira automatiquement dans ton navigateur")
    print("   URL locale : http://localhost:7860")
    print("\n💡 Pour arrêter : Ctrl+C\n")
    print("="*80 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Met à True pour avoir un lien public temporaire
        show_error=True
    )

