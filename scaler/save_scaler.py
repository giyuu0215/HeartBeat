import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

# Load the data
file_path = os.path.join(os.path.dirname(__file__), '../heart_disease_uci.csv')
df = pd.read_csv(file_path)

# Drop columns not useful for prediction (like 'id', 'dataset')
df = df.drop(['id', 'dataset'], axis=1)

# Fill missing values (if any)
def fill_missing(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
            df[col] = df[col].infer_objects(copy=False)  # Fix FutureWarning for each column
    return df

df = fill_missing(df)

# Encode categorical columns
cat_cols = df.select_dtypes(include=['object']).columns
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

# Features and target
y = df['num']
X = df.drop('num', axis=1)
# For this dataset, treat any value >0 in 'num' as heart disease (binary classification)
y = (y > 0).astype(int)

# Split and fit scaler as in the notebook
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
scaler.fit(X_train)

# Save the scaler in the scaler folder
os.makedirs('scaler', exist_ok=True)
joblib.dump(scaler, 'scaler/scaler.save')
