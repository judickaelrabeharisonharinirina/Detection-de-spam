# Rapport Final du Projet : Détection de Spam MLOps

## 1. Synthèse du Projet
Ce projet a permis de mettre en place une usine logicielle complète (Pipeline MLOps) pour un modèle de détection de spam. Partant d'un simple script de Machine Learning, nous avons abouti à une application Web sécurisée, auditée, signée et déployée de manière 100 % automatisée. 

Le modèle de classification (SVM) s'entraîne avec succès, enregistre ses performances dans MLflow, et se fait encapsuler dans une image Docker double-service (FastAPI + Streamlit).

---

## 2. Analyse Chronologique et Réalité du Terrain

Le développement de ce projet a été une aventure technique intense, marquée par des défis d'infrastructure majeurs. Voici la répartition réelle du temps investi :

| Composant / Étape | Durée Investie | Description & Challenge Clé |
| :--- | :--- | :--- |
| **Dataset & NLTK** | 1 jour | Nettoyage textuel, gestion des stop-words et tokenisation. |
| **Modélisation & Tracking** | 4 jours | Entraînement du modèle SVM et liaison avec **MLflow** et **MinIO** pour la persistance des artéfacts. |
| **Configuration Docker Hub** | 1 semaine | Création des dépôts, gestion des tags et mise en place des configurations de push. |
| **Pipeline Jenkins (CI/CD)** | **2 semaines** | Le plus gros défi du projet. Résolution des conflits de droits sous Windows/WSL2. |
| **Restructuration & Rapport** | 2 jours | Nettoyage de l'arborescence (suppression du dossier `Codes/`) et alignement des chemins. |

---

## 3. Les Grands Défis Techniques Résolus (Lessons Learned)

### Le Calvaire du Pipeline Jenkins sous Windows (2 semaines de troubleshooting)
Le principal point de friction a résidé dans la communication entre le conteneur Jenkins et le démon Docker de l'hôte Windows via le fichier de socket `/var/run/docker.sock`. 
* *Symptôme :* Erreurs répétées de type `permission denied` (Exit code 126) et images corrompues de 259 octets poussées sur Docker Hub dues à un contexte de build vide à cause d'encapsulations de conteneurs trop complexes.
* *Solution apportée :* Injection des privilèges maximum à l'intérieur du conteneur Jenkins en mode root (`docker exec -u 0 ... chmod 766 /var/run/docker.sock`). Cela a permis de débloquer les builds natifs en direct, garantissant que 100 % du code, du modèle et des dépendances système soient inclus dans l'image finale.

### La Restructuration de l'Arborescence
Initialement, le projet intégrait un sous-dossier `Codes/` qui alourdissait les chemins de maintenance. L'arborescence a été aplatie et standardisée pour correspondre aux standards actuels de l'industrie :
* Les configurations Docker résident désormais directement dans `docker/`.
* Les scripts applicatifs et de prédiction se situent dans `src/`.

---

## 4. Conclusion et Perspectives
Le pipeline est aujourd'hui **100 % fonctionnel**. À chaque commit sur la branche `main` du dépôt GitHub, Jenkins prend le relais, réentraîne le modèle, valide l'intégrité de la sécurité avec Trivy, appose une signature cryptographique Cosign et met à disposition l'image sur Docker Hub.

**Perspectives d'amélioration :**
1. Connecter l'alerte Prometheus (actuellement en *Connection Refused* si le serveur local est éteint) sur un cluster managé pour un monitoring de production en temps réel.
2. Mettre en place un mécanisme de détection du *Data Drift* (dérive des données) pour déclencher automatiquement le pipeline Jenkins lorsque le langage des spams évolue sur le web.
