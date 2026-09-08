import pandas as pd
df1 = pd.read_csv("churnguard_data.csv")
df1.drop(columns=['customerID'],inplace=True)
df1.drop_duplicates(inplace=True)
df1['gender'] = df1['gender'].str.strip()
df1['PaymentMethod'] = df1['PaymentMethod'].str.strip()
df1['Churn']=df1['Churn'].str.strip().str.title()
df1['PhoneService'] = df1['PhoneService'].str.strip().str.title()
df1['PaperlessBilling'] = df1['PaperlessBilling'].str.strip().str.title()
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
print(df1.head())
print(len(df1))
print(df1.shape)
print(df1.isnull().sum())