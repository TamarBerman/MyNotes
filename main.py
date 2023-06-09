from website import create_app
import pandas as pd
import csv


def open_csv():
    """open our CSV file for reading. if it doesn't exist open a new CSV file named 'data.csv'"""
    header_list = ['Name', 'WriteDate', 'Data']
    try:
        file = pd.read_csv("data.csv")
    except:
        with open("data.csv", 'w') as file:
            dw = csv.DictWriter(file, delimiter = ',',
                                fieldnames = header_list)
            dw.writeheader()

    df = pd.read_csv('data.csv')
    print(df)


open_csv()

app = create_app()
if __name__ == '__main__':
    app.run(debug = True)
