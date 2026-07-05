import streamlit as st
import requests
import os

# Récupération dynamique de l'URL de l'API (géré via Docker ou Ansible)
# Si la variable n'est pas définie, on utilise localhost par défaut
print("DEBUG: Lancement du script...") # <--- Ajoute ça
API_URL = os.getenv("FASTAPI_API_URL", "http://127.0.0.1:8000")
print(f"DEBUG: URL de l'API = {API_URL}")
st.title("Spam Detection")
st.write("Entrer vos message")

# Champ de saisie utilisateur
user_input = st.text_area("Message à analyser :", height=150)

if st.button("Analyser le message"):
    if user_input.strip() == "":
        st.warning("Veuiller entrer un texte avant d'appuyer")
    else:
        # Utilisation de l'URL dynamique configurée plus haut
        url = f"{API_URL}/predict"
        payload = {"text": user_input}
        try:
            with st.spinner("Analyse en cours..."):
                response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result["prediction"]
                proba = result["probability_spam"] * 100
                
                # Affichage des résultats (harmonisé avec le label "Spam" / "Not spam" de ton FastAPI)
                if prediction == "Spam":
                    st.error(f"Ce message est une SPAM attention (probabilité : {proba:.2f}%)")
                else:
                    st.success(f"Aucun SPAM alors c'est bien (Probabilité de spam : {proba:.2f}%)")
                    
                st.info(f"Modèle utilisé : {result['model']} | Seuil : {result['threshold']}")
            else:
                st.error(f"Erreur lors de la communication avec l'API de prédiction. Code : {response.status_code}")
        except Exception as e:
            st.error(f"Impossible de se connecter à l'API ({url}). Vérifie qu'elle est bien lancée. Erreur : {e}")