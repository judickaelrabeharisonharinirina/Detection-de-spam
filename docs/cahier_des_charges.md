# Cahier des Charges : Système MLOps de Détection de Spam

## 1. Contexte et Objectifs
L'objectif de ce projet est de concevoir, d'automatiser et de déployer un modèle d'apprentissage automatique performant capable de classifier des messages textuels (Spam vs Ham). Ce projet s'inscrit dans une démarche MLOps stricte, visant à minimiser les interventions manuelles entre la phase d'entraînement et la mise en production.

## 2. Besoins Fonctionnels
* **Entraînement Automatisé :** Capacité à réentraîner le modèle à chaque modification du code ou des données.
* **Suivi des Métriques :** Centralisation des résultats d'entraînement pour comparer les versions du modèle (MLflow).
* **Interface Utilisateur :** Fournir une interface web minimaliste permettant de coller un texte et d'obtenir un verdict instantané (Streamlit).
* **API de Prédiction :** Mettre à disposition des applications tierces une API rapide (FastAPI).
* **Sécurité applicative :** Scanner l'image finale contre les vulnérabilités majeures avant toute livraison.

## 3. Besoins Techniques & Contraintes
* **Conteneurisation :** L'ensemble de l'application doit être packagé sous forme d'image Docker standardisée.
* **Sécurité et Intégrité :** L'image Docker doit être analysée par **Trivy** et signée numériquement par **Cosign** (Cryptographie Sigstore) avant d'être envoyée sur Docker Hub.
* **Gestion des environnements :** Isolation complète via des environnements virtuels Python (`venv`) au cours du cycle de build.
* **Compatibilité Système :** L'infrastructure doit pouvoir s'exécuter de manière transparente sur un environnement de développement Windows via Docker Desktop et WSL2.

## 4. Calendrier Prévisionnel Réel (Rétrospective)
* **Traitement du Dataset & Préparation :** 1 jour.
* **Développement de la logique ML (Modèle, Entraînement, intégration MLflow et stockage MinIO) :** 4 jours.
* **Mise en place et configuration de l'infrastructure Docker Hub :** 1 semaine.
* **Création, fiabilisation et résolution des bugs du Pipeline Jenkins (CI/CD) :** 2 semaines.
* **Restructuration finale selon les standards MLOps et documentation :** 2 jours.
