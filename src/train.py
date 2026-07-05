import pandas as pd 
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as  sns
import os

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# 1. Chargement du dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.abspath(os.path.join(BASE_DIR, '../Assets/Dataset/spam.csv'))
data = pd.read_csv(DATASET_PATH)

# 2. Nettoyage des données
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)
data['Category'] = data['Category'].replace(["ham","spam"], ["Not spam","Spam"])

def nettoyage(texte):
    if not isinstance(texte, str):
        return ""
    
    texte = texte.lower()
    mots = word_tokenize(texte)
    
    table_ponctuation = str.maketrans('', '', string.punctuation)
    mots = [m.translate(table_ponctuation) for m in mots]
    mots = [m for m in mots if m != '']
    
    mots_vides = set(stopwords.words('english'))
    mots = [m for m in mots if m not in mots_vides]
    
    lemmatiseur = WordNetLemmatizer()
    mots_propres = [lemmatiseur.lemmatize(m) for m in mots]
    
    return " ".join(mots_propres)

data['mess_clean'] = data['Message'].apply(nettoyage)
    
# 3. Séparation et Vectorisation (TF-IDF)
x = data["mess_clean"]
y = data["Category"]

X_train_text, X_test_text, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

vector = TfidfVectorizer(stop_words='english')
X_train = vector.fit_transform(X_train_text)
X_test = vector.transform(X_test_text)

# 4. Visualisation PCA (Sauvegarde du graphique)
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y_train)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_train.toarray())

plt.figure(figsize=(12,8))
sns.scatterplot(
    x=X_pca[:,0],
    y=X_pca[:,1],
    hue=y_train,
    palette=['blue','red'],
    s=60,
    alpha=0.8
)

plt.title("Projection PCA des messages TF-IDF")
plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.2f}% variance)")
plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.2f}% variance)")
plt.tight_layout()

nom_dossier = "Figure"
if not os.path.exists(nom_dossier):
    os.makedirs(nom_dossier)
chemin_enregistrement = os.path.join(nom_dossier, "scatter.png")
plt.savefig(chemin_enregistrement, dpi=300, bbox_inches='tight')
plt.close() # Ferme la figure pour libérer la mémoire

# 5. Entraînement du modèle (Régression Logistique)
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# 6. Évaluation
y_pred = log_reg.predict(X_test)
conf = confusion_matrix(y_test, y_pred)