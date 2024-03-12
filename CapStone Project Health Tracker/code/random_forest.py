import pandas as pd
import numpy as np
df = pd.read_csv('C:/Users/russel/Desktop/Assignments and Projects/CapStone Project Health Tracker/data/medical_records.csv')
cd = df.sample(n= 1000, random_state= 42)
dd = df.sample(n =1000, random_state= 42)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
cd['medical_conditions_encoded'] = encoder.fit_transform(cd['medical_conditions'])
cd['allergies_encoded'] = encoder.fit_transform(cd['allergies'])
cd['medications_encoded'] = encoder.fit_transform(cd['medications'])

ss= cd.drop(['patient_id', 'name', 'date_of_birth', 'gender','medical_conditions','allergies', 'last_appointment_date','medications'], axis= 1)
x = ss.drop('medications_encoded', axis= 1)
y = cd['medications_encoded']
xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size= 0.4, random_state= 42)
reg = RandomForestRegressor(n_estimators= 500, random_state= 42)
reg.fit(xTrain, yTrain)

string1 = input("Enter 3 medical conditions : ")
string2 = input("Enter 3 allergies : ")

combined_strings = [string1, string2]
encoder = LabelEncoder()
encoder.fit(combined_strings)

# Transform the input strings
x1 = encoder.transform([string1])[0]
x2 = encoder.transform([string2])[0]

for index, i in cd.iterrows():
    if i['medical_conditions'] == string1:
        x1 = i['medical_conditions_encoded']
        break
for index, i in cd.iterrows():
    if i['allergies'] == string2:
        x2 = i['allergies_encoded']
        break

ans = reg.predict([[x1,x2]])
print(x1, x2, ans)
rounded_values = np.round(ans)
for index, row in cd.iterrows():
    # Check if the value in the 'medication_n' column is equal to x
    if row['medications_encoded'] == rounded_values:
        # If the condition is true, print the value in the 'medication' column
        print(row['medications'])