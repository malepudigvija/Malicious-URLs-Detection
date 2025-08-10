"""import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset (Example dataset: URLs labeled as "malicious" or "safe")
data = pd.DataFrame({
    "url": [
        "http://free-money.com", "https://secure-bank.com", "http://hack-site.biz",
        "https://google.com", "http://malicious-site.com", "https://github.com"
    ],
    "label": [1, 0, 1, 0, 1, 0]  # 1 = Malicious, 0 = Safe
})
data = pd.read_csv('malicious_phish.csv')
label_mapping = {
    'benign': 0,
    'phishing': 1,
    'defacement': 2
}
data['label'] = data['type'].map(label_mapping)
data = data.drop(columns=['type'])



# Feature extraction using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["url"])
y = np.array(data["label"])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Save model and vectorizer
joblib.dump(model, "models/malicious_url_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("Model and vectorizer saved successfully!")"""


import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Load dataset
data = pd.read_csv('malicious_phish.csv').sample(n=2000, random_state=42)


# Convert type -> label
label_mapping = {
    'benign': 0,
    'phishing': 1,
    'defacement': 2
}
data['label'] = data['type'].map(lambda x: label_mapping.get(x, -1))
data = data[data['label'] != -1]  # Drop rows with unknown type
data = data.drop(columns=['type'])

print(f"Training on {len(data)} samples...")

# TF-IDF vectorization
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["url"])
y = np.array(data["label"])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=50, max_depth=20, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# Save model and vectorizer
joblib.dump(model, "models/malicious_url_model.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("✅ Model and vectorizer saved successfully!")


os.makedirs("static", exist_ok=True)

# Generate and save confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()
plt.title("Confusion Matrix")
plt.savefig("static/confusion_matrix.png")
plt.close()




