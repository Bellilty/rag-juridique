"""
API FastAPI pour l'assistant juridique RAG
===========================================

Cette API expose les fonctionnalités RAG via des endpoints HTTP.

Endpoints disponibles :
- GET /health : Vérifie que l'API fonctionne
- GET /ask : Pose une question à l'assistant juridique
- GET /stats : Statistiques sur l'index

Comment lancer l'API ?
    uvicorn src.api:app --reload --port 8000

Puis tester :
    http://localhost:8000/ask?query=What+is+GDPR
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from dotenv import load_dotenv

# Import de nos modules
from src.embeddings import EmbeddingManager
from src.retrieval import RAGRetriever, estimate_cost

# Charge les variables d'environnement
load_dotenv()

# ============================================================================
# Configuration de l'application FastAPI
# ============================================================================

app = FastAPI(
    title="Assistant Juridique RAG",
    description="API locale pour poser des questions sur des documents juridiques",
    version="1.0.0",
    docs_url="/docs",  # Documentation Swagger automatique
    redoc_url="/redoc"  # Documentation ReDoc alternative
)

# Configuration CORS (pour pouvoir appeler l'API depuis un navigateur)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifie les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Variables globales (chargées au démarrage)
# ============================================================================

retriever: Optional[RAGRetriever] = None
embedding_manager: Optional[EmbeddingManager] = None
startup_error: Optional[str] = None

# ============================================================================
# Modèles Pydantic pour la validation des données
# ============================================================================

class QueryRequest(BaseModel):
    """Modèle pour une requête de question."""
    query: str = Field(..., description="La question à poser", min_length=3)
    k: int = Field(3, description="Nombre de chunks à utiliser comme contexte", ge=1, le=10)
    model: str = Field("gpt-4o-mini", description="Modèle OpenAI à utiliser")

class QueryResponse(BaseModel):
    """Modèle pour la réponse."""
    query: str
    answer: str
    sources: List[str]
    num_chunks_used: int
    model: str
    tokens_used: dict
    estimated_cost: dict

class StatsResponse(BaseModel):
    """Modèle pour les statistiques."""
    total_chunks: int
    total_vectors: int
    sources: List[str]
    index_loaded: bool

class HealthResponse(BaseModel):
    """Modèle pour le health check."""
    status: str
    message: str
    index_loaded: bool

# ============================================================================
# Événements de démarrage et arrêt
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Fonction exécutée au démarrage de l'API.
    Charge l'index FAISS et les chunks en mémoire.
    """
    global retriever, embedding_manager, startup_error
    
    print("\n" + "="*80)
    print("🚀 Démarrage de l'API Assistant Juridique RAG")
    print("="*80 + "\n")
    
    try:
        # Vérifie la clé API
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Clé API OpenAI manquante dans le fichier .env")
        
        # Initialise le gestionnaire d'embeddings
        embedding_manager = EmbeddingManager(api_key=api_key)
        
        # Vérifie si l'index existe
        if not embedding_manager.index_exists():
            startup_error = "Index FAISS non trouvé. Lance 'python src/embeddings.py' pour créer l'index."
            print(f"⚠️  {startup_error}")
            return
        
        # Charge l'index et les chunks
        index, chunks = embedding_manager.load_index()
        
        # Initialise le retriever
        retriever = RAGRetriever(index, chunks, api_key=api_key)
        
        print("✅ API prête à recevoir des requêtes!")
        print(f"📚 {len(chunks)} chunks chargés en mémoire")
        print(f"🔗 Documentation : http://localhost:8000/docs")
        print("="*80 + "\n")
        
    except Exception as e:
        startup_error = f"Erreur au démarrage : {str(e)}"
        print(f"❌ {startup_error}")
        print("="*80 + "\n")

@app.on_event("shutdown")
async def shutdown_event():
    """Fonction exécutée à l'arrêt de l'API."""
    print("\n" + "="*80)
    print("👋 Arrêt de l'API")
    print("="*80 + "\n")

# ============================================================================
# Endpoints de l'API
# ============================================================================

@app.get("/", response_model=dict)
async def root():
    """
    Endpoint racine - Informations sur l'API.
    """
    return {
        "name": "Assistant Juridique RAG",
        "version": "1.0.0",
        "description": "Posez des questions sur des documents juridiques",
        "endpoints": {
            "/health": "Vérifier l'état de l'API",
            "/ask": "Poser une question (GET avec param ?query=...)",
            "/ask_post": "Poser une question (POST avec JSON)",
            "/stats": "Voir les statistiques de l'index",
            "/docs": "Documentation Swagger",
            "/redoc": "Documentation ReDoc"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check - Vérifie que l'API fonctionne.
    
    Returns:
        Status de l'API et de l'index
    """
    if startup_error:
        return HealthResponse(
            status="warning",
            message=startup_error,
            index_loaded=False
        )
    
    if retriever is None:
        return HealthResponse(
            status="error",
            message="Retriever non initialisé",
            index_loaded=False
        )
    
    return HealthResponse(
        status="ok",
        message="API opérationnelle",
        index_loaded=True
    )

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Retourne des statistiques sur l'index FAISS.
    
    Returns:
        Statistiques sur les chunks et l'index
    """
    if retriever is None:
        raise HTTPException(
            status_code=503,
            detail=startup_error or "Index non chargé"
        )
    
    # Récupère les sources uniques
    sources = list(set(chunk['source'] for chunk in retriever.chunks))
    
    return StatsResponse(
        total_chunks=len(retriever.chunks),
        total_vectors=retriever.index.ntotal,
        sources=sources,
        index_loaded=True
    )

@app.get("/ask", response_model=QueryResponse)
async def ask_question(
    query: str = Query(..., description="La question à poser", min_length=3),
    k: int = Query(3, description="Nombre de chunks de contexte", ge=1, le=10),
    model: str = Query("gpt-4o-mini", description="Modèle OpenAI (gpt-4o-mini ou gpt-3.5-turbo)")
):
    """
    Pose une question à l'assistant juridique (méthode GET).
    
    Args:
        query: La question à poser
        k: Nombre de chunks à utiliser comme contexte (1-10)
        model: Modèle OpenAI à utiliser
    
    Returns:
        Réponse de l'assistant avec sources et coût estimé
    
    Example:
        GET /ask?query=What+is+GDPR&k=3&model=gpt-4o-mini
    """
    if retriever is None:
        raise HTTPException(
            status_code=503,
            detail=startup_error or "Index non chargé. Lance 'python src/embeddings.py' d'abord."
        )
    
    try:
        # Lance la recherche RAG
        result = retriever.ask(query, k=k, model=model)
        
        # Calcule le coût estimé
        cost = estimate_cost(result['tokens_used'], model)
        result['estimated_cost'] = cost
        
        return QueryResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement : {str(e)}"
        )

@app.post("/ask_post", response_model=QueryResponse)
async def ask_question_post(request: QueryRequest):
    """
    Pose une question à l'assistant juridique (méthode POST).
    
    Args:
        request: Requête JSON avec query, k, et model
    
    Returns:
        Réponse de l'assistant avec sources et coût estimé
    
    Example:
        POST /ask_post
        {
            "query": "What is GDPR?",
            "k": 3,
            "model": "gpt-4o-mini"
        }
    """
    if retriever is None:
        raise HTTPException(
            status_code=503,
            detail=startup_error or "Index non chargé"
        )
    
    try:
        # Lance la recherche RAG
        result = retriever.ask(request.query, k=request.k, model=request.model)
        
        # Calcule le coût estimé
        cost = estimate_cost(result['tokens_used'], request.model)
        result['estimated_cost'] = cost
        
        return QueryResponse(**result)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement : {str(e)}"
        )

# ============================================================================
# Point d'entrée pour lancer l'API directement
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n🚀 Lancement de l'API FastAPI...")
    print("📖 Documentation : http://localhost:8000/docs\n")
    
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Recharge automatiquement lors des modifications
    )

