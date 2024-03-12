import pandas as pd
df = pd.read_csv('C:/Users/russel/Desktop/Assignments and Projects/CapStone Project Health Tracker/data/medical_records.csv')
from sklearn.preprocessing import LabelEncoder
small_df = df.sample(n=1000, random_state=42)
targets = df.sample(n=1000, random_state=42)

le_conditions = LabelEncoder()
le_allergies = LabelEncoder()
le_medications = LabelEncoder()
small_df['conditions_n'] = le_conditions.fit_transform(small_df['medical_conditions'])
small_df['allergiess_n'] = le_allergies.fit_transform(small_df['allergies'])
targets['medications_n'] = le_medications.fit_transform(small_df['medications'])

small_dfs = small_df.drop(['patient_id', 'name', 'date_of_birth', 'last_appointment_date', 'gender','medical_conditions','allergies','medications'], axis='columns')
target = targets.drop(['patient_id', 'name', 'date_of_birth', 'last_appointment_date', 'gender','medical_conditions','allergies','medications'], axis='columns')

from sklearn import tree
model = tree.DecisionTreeClassifier()
model.fit(small_dfs, target)
string1 = input("Enter 3 medical conditions : ")
string2 = input("Enter 3 allergies : ")

encoder = LabelEncoder()
encoder.fit([string1, string2])
x1 = encoder.transform([string1])[0]
x2 = encoder.transform([string2])[0]

for index, i in small_df.iterrows():
    if i['medical_conditions'] == string1:
        x1 = i['conditions_n']
        break
for index, i in small_df.iterrows():
    if i['allergies'] == string2:
        x2 = i['allergies_n']
        break

score = model.score(small_dfs, target)
x = model.predict([[x1,x2]])
print(score)
for index, row in targets.iterrows():
    if row['medications_n'] == x:
        print("The Medications are :", row['medications'])