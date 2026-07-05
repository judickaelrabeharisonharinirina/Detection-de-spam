import os
import pickle
import pandas as pd
from train import *
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, make_scorer
import nltk

# --- CONFIGURATION INITIALE ---
nltk.download('stopwords')
nltk.download('punkt')

# 1. Configuration Stockage MLflow
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "masoud"
os.environ["AWS_SECRET_ACCESS_KEY"] = "Strong#Pass#2022"
os.environ["MLFLOW_S3_IGNORE_TLS"] = "true"

mlflow.set_tracking_uri("file:///var/jenkins_home/workspace/spam-detection-pipeline/mlruns")
mlflow.set_experiment("Spam_Detection")

# 2. Définition des modèles à benchmarquer
models = {
    'LogisticRegression': LogisticRegression(class_weight='balanced', max_iter=1000),
    'SVM': SVC(kernel='linear', class_weight='balanced', probability=True),
    'MultinomialNB': MultinomialNB(),
    'RandomForest': RandomForestClassifier(n_estimators=100, class_weight='balanced'),
}

# 3. Entraînement et Tracking de base
for name, clf in models.items():
    with mlflow.start_run(run_name=name):
        pipeline = Pipeline([
            ('clf', clf),
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        # Calcul des métriques
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, pos_label='Spam', zero_division=0) 
        rec = recall_score(y_test, y_pred, pos_label='Spam', zero_division=0)
        f1 = f1_score(y_test, y_pred, pos_label='Spam', zero_division=0)
        
        # Logs MLflow
        mlflow.log_param("model_type", name)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("f1_score", f1)
        
        # Artefacts
        report = classification_report(y_test, y_pred)
        report_path = f"report_{name}.txt"
        with open(report_path, "w") as f:
            f.write(report)
        mlflow.log_artifact(report_path)
        
        if os.path.exists("Figure/scatter.png"):
            mlflow.log_artifact("Figure/scatter.png")
            
        mlflow.sklearn.log_model(
            pipeline, 
            artifact_path=f"model_{name}",
            skops_trusted_types=["scipy.sparse._csr.csr_matrix"]
        )

# 4. Optimisation par Grid Search (Logistic Regression)
with mlflow.start_run(run_name="LogisticRegression_GridSearch"):    
    param_grid = {
        'clf__C': [0.01, 0.1, 1, 10],
        'clf__class_weight': [None, 'balanced'],
    }
    
    pipeline_grid = Pipeline([
        ('clf', LogisticRegression(max_iter=1000, solver='liblinear')),
    ])
    
    scorer = make_scorer(recall_score, pos_label='Spam')
    grid = GridSearchCV(pipeline_grid, param_grid, scoring=scorer, cv=5)
    grid.fit(X_train, y_train)
    
    mlflow.log_params(grid.best_params_)
    mlflow.log_metric("best_recall_score", grid.best_score_)
    mlflow.sklearn.log_model(grid.best_estimator_, artifact_path="best_grid_model")

# 5. Entraînement final sur le dataset complet & Sauvegarde du Pipeline
X_full = pd.concat([X_train_text, X_test_text])
y_full = pd.concat([y_train, y_test])

models_dir = os.path.join("..", "models")
os.makedirs(models_dir, exist_ok=True)

final_model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', LogisticRegression(C=1, class_weight='balanced', max_iter=1000))
])

final_model.fit(X_full, y_full)

model_path = os.path.join(models_dir, "logreg_spam_pipeline.pkl")
with open(model_path, 'wb') as f:
    pickle.dump(final_model, f)

print('Pipeline final entraîné et sauvegardé avec succès. Fin du tracking MLflow.')
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

try:
    registry = CollectorRegistry()
    
    # Déclaration de la métrique
    metric_recall = Gauge('spam_model_recall', 'Meilleur score recall du GridSearch', registry=registry)
    
    # Dynamique : On récupère le vrai score calculé par ton GridSearch juste au-dessus !
    metric_recall.set(grid.best_score_) 
    
    # Envoi à la Pushgateway

# Modifie cette ligne à la fin de ton fichier :
    push_to_gateway('localhost:9091', job='spam_detection_pipeline', registry=registry)
    print("Métriques envoyées à la Prometheus Pushgateway avec succès.")
except Exception as e:
    print(f"Erreur lors de l'envoi vers Prometheus : {e}")
# =====================================================================


print('Pipeline final entraîné et sauvegardé avec succès. Fin du tracking MLflow.')