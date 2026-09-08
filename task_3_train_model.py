import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler
df1 = pd.read_csv("churnguard_data.csv")
df1.drop(columns=['customerID'],inplace=True)
df1.drop_duplicates(inplace=True)
for col in ['gender', 'PaymentMethod']:
    df1[col] = df1[col].str.strip()
for col in ['Churn', 'PhoneService', 'PaperlessBilling']:
    df1[col] = df1[col].str.strip().str.title()
df1['Contract'] = df1['Contract'].map({'month to month': 'Month-to-month', 'one year': 'One year', 'two year': 'Two year', 'Monthly': 'Month-to-month',
                                       '1 year': 'One year', '2 year': 'Two year','Month-to-month': 'Month-to-month', 'One year': 'One year', 'Two year': 'Two year',
                                       'Two Year': 'Two year','One Year': 'One year', 'month-to-month':'Month-to-month'})
df1['InternetService'] = df1['InternetService'].map({'DSL': 'DSL', 'Fiber optic' : 'Fiber optic', 'No': 'No', 'DSl': 'DSL', 'dsl':'DSL',
                                                     'fiber optic': 'Fiber optic', 'FiberOptic': 'Fiber optic', 'Dsl': 'DSL', 'NO':'No',
                                                     'no': 'No'})
df1['InternetService']=df1['InternetService'].fillna('No')
df1['TotalCharges'] = pd.to_numeric(df1['TotalCharges'], errors='coerce')
df1=df1[df1['TotalCharges']>0]
df1 = df1[(df1['MonthlyCharges'] >= 10) & (df1['MonthlyCharges'] <= 200)]
df1['MonthlyCharges']=df1['MonthlyCharges'].fillna(df1['MonthlyCharges'].mean())
df1['TotalCharges']=df1['TotalCharges'].fillna(df1['TotalCharges'].mean())
df1['tenure']=df1['tenure'].fillna(df1['tenure'].median()).round(2)
df1['Churn']=df1['Churn'].map({'Yes':1, 'No':0})
df1 = pd.get_dummies(
    df1,
    columns=['gender', 'PhoneService', 'InternetService', 'Contract', 'PaperlessBilling', 'PaymentMethod'],
    drop_first=True
)
X = df1.drop(columns=['Churn'])
y = df1['Churn']
X_test, X_train, y_test, y_train = train_test_split(X,y,test_size=0.2, random_state=42)
scaler=StandardScaler()
scaler.fit_transform(X_train)
scaler.transform(X_test)
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
y_pred_train = lr.predict(X_train)
y_pred_test=lr.predict(X_test)
print("Model training completed")
print("Model accuracy on testing set: ", accuracy_score(y_test, y_pred_test))
print(classification_report(y_test, y_pred_test,target_names=['Stay','Churn']))
