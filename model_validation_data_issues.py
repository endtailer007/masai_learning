import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Step 1: build the DataFrame from the inlined sample rows above
df1 = pd.read_csv("/content/transactions_sample.csv")

n_samples = len(df1)
n_classes = df1["Class"].nunique()
n_samples_in_class1 = int((df1["Class"] == 1).sum())
n_samples_in_class_0 = int((df1["Class"] == 0).sum())
# Step 2: implement the manual class-weight formula
def compute_class_weight(n_samples, n_classes, n_samples_in_class):
    # TODO: n_samples / (n_classes * n_samples_in_class)
    return n_samples / (n_classes * n_samples_in_class)

# Step 3: compute weights for each class — your code here
class_weight_1 = compute_class_weight(n_samples, n_classes, n_samples_in_class1)
class_weight_0 = compute_class_weight(n_samples, n_classes, n_samples_in_class_0)
print(f"Class weight for class 1: {class_weight_1}")
print(f"Class weight for class 0: {class_weight_0}")

# Step 4: stratified train/test split (test_size=0.25, random_state=42)
# TODO

# Step 5: fit StandardScaler on training data only, transform both sets
# TODO

# Step 6: train baseline LogisticRegression and class_weight='balanced' LogisticRegression
# TODO

# Step 7: compute and print accuracy, precision, recall, F1 for the fraud class for both models
# TODO

if __name__ == "__main__":
    pass
