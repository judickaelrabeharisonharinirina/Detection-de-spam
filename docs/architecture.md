# Architecture du Système de Détection de Spam (MLOps)

Ce document décrit l'architecture globale, les flux de données et l'infrastructure technique mis en œuvre pour le projet de détection de spam.

## 1. Vue d'ensemble de l'Infrastructure
L'écosystème repose sur une approche d'intégration et de déploiement continus (CI/CD) automatisée par Jenkins, combinée à un suivi rigoureux des expérimentations via MLflow.

* **Orchestrateur CI/CD :** Jenkins (s'exécutant dans un conteneur Docker sous un hôte Windows via WSL2).
* **Plateforme de Registre :** Docker Hub (`judickael040/spam_detection`).
* **Suivi et Registre de Modèles :** MLflow Tracking UI (configuré sur `http://localhost:5000`).
* **Serveur de Stockage d'Artéfacts :** MinIO (S3-compatible Object Storage).
* **Supervision / Métriques :** Prometheus & Grafana (collecte des métriques applicatives).
* **Déploiement Automatisé :** Ansible (Playbooks pour la gestion des conteneurs de production).

---

## 2. Pipeline de Données et Entraînement (ML Pipeline)
1. **Données :** Le dataset textuel est ingéré, nettoyé et pré-traité à l'aide de la librairie **NLTK** (téléchargement automatisé des ressources `stopwords`, `punkt`, etc.).
2. **Entraînement :** Exécution du script `src/predict.py` qui entraîne un modèle de classification (SVM/SVC via `scikit-learn`).
3. **Tracking :** Les paramètres, métriques de performance (Accuracy, F1-Score) et les fichiers du modèle final sont loggés en temps réel dans **MLflow** connecté au stockage d'artéfacts **MinIO**.

---

## 3. Pipeline CI/CD (Workflow Jenkins)

Le cycle de vie du code suit les étapes automatisées suivantes :
[ Code Push ] ➔ [ Git Clone ] ➔ [ Setup Env & Pip ] ➔ [ ML Training & MLflow ]
│
[ Deploy (Ansible) ] ◄─ [ Push & Sign ] ◄─ [ Trivy Scan ] ◄─ [ Docker Build ]

* **Gestion des Volumes & Sockets :** Pour l'environnement Windows, le socket Docker (`/var/run/docker.sock`) est partagé avec le conteneur Jenkins avec des permissions ajustées (`chmod 766`) pour permettre des builds natifs "Docker-in-Docker" sans friction de droits.

---

## 4. Architecture Applicative (Conteneur Final)
L'image finale poussée sur Docker Hub est basée sur `python:3.11-slim` et expose deux points d'entrée simultanés :
* **Backend (Port 8000) :** API REST développée avec **FastAPI** pour exposer les prédictions du modèle sous forme de points de terminaison HTTP.
* **Frontend (Port 8501) :** Interface graphique interactive développée avec **Streamlit** pour permettre aux utilisateurs de tester la détection de spam à la volée.
