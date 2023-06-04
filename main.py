from website import create_app
import pandas as pd

import csv

headerList = ['Name', 'WriteDate', 'Data']

try:
    file = pd.read_csv("data.csv")
except:
    with open("data.csv", 'w') as file:
        dw = csv.DictWriter(file, delimiter=',',
                            fieldnames=headerList)
        dw.writeheader()

df = pd.read_csv('data.csv')
print(df)



app = create_app()
if __name__ == '__main__':
    app.run(debug = True)
