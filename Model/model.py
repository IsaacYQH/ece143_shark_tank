# %%
import pandas as pd

# Load the dataset
df = pd.read_csv('Shark Tank US dataset.csv')
print(f'{df.shape[0]} samples found after data cleaning!')# Drop rows with missing 'Got Deal' values
features_orig = ['Industry','Pitchers Gender','Pitchers State', 'Multiple Entrepreneurs', 'Original Ask Amount', 'Original Offered Equity', 'Valuation Requested', 'Got Deal']
df = df.dropna(subset=features_orig)
print(f'{df.shape[0]} kept valid samples after data cleaning!')

# %%
from sklearn.preprocessing import StandardScaler

# Have Company Website or not
df["Company Website Bool"] = df["Company Website"]
df["Company Website Bool"] = df["Company Website Bool"].apply(lambda x: False if pd.isna(x) else True)
df["Pitchers State Bool"] = df["Pitchers State"]
top_us_states_by_gdp_short = [
    "CA",  # California
    "TX",  # Texas
    "NY",  # New York
    "FL",  # Florida
    "IL",  # Illinois
    "PA",  # Pennsylvania
    "OH",  # Ohio
    "GA",  # Georgia
    "NJ",  # New Jersey
    "WA",  # Washington
]

df["Pitchers State Bool"] = df["Pitchers State Bool"].apply(lambda x: True if x in top_us_states_by_gdp_short else False)
# Feature selection
try:
    features_orig.remove('Got Deal')
    features_orig.remove('Pitchers State')
except:
    pass    
features = features_orig+['Company Website Bool', 'Pitchers State Bool']
print(features)
X = df[features]
y = df['Got Deal']

# One-hot encode categorical features
X = pd.get_dummies(X, columns=['Industry', 'Pitchers Gender'])
# Standardize numeric features
scaler = StandardScaler()
numeric_features = ['Original Ask Amount', 'Original Offered Equity', 'Valuation Requested']
X[numeric_features] = scaler.fit_transform(X[numeric_features])

print(X.columns)
print(f'{len(X.columns)} features after one-hot encoding!')

# %%
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Sample data (replace with your actual data)
# X, y = your_data_features, your_data_labels
# Train-test split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=62)

model = LogisticRegressionCV(Cs=np.arange(0.01,0.1,0.01) , cv=10, max_iter=1000, random_state=0)
model.fit(X_train, y_train)
# Predictions and evaluation
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)

from pprint import pprint
print(model.C_.item())
# print(pd.DataFrame(list(zip(list(X.columns),list(model.coef_.flatten())))))
print(f"Validation Accuracy: {accuracy:.2f}")
# print("Confusion Matrix:\n", confusion_matrix(y_val, y_pred))
# print("Classification Report:\n", classification_report(y_val, y_pred))
print("Top 10 features by absolute coefficient:")
pprint(sorted(list(zip(list(X.columns),list(model.coef_.flatten()))), key=lambda x: abs(x[1]), reverse=True)[:10])





