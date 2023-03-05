import argparse
import pandas
import os
import chardet

def convert(file: str):
    #detect type
    detector = chardet.UniversalDetector()
    text = open('in/' + file,'rb').read()
    print(chardet.detect(text))
    print(file)

    #set max rows
    pandas.options.display.max_rows = 9999

    #read file
    if file.startswith("lista_operacji"):
      df = pandas.read_csv('in/' + file, encoding="UTF-8", skiprows=26, skipfooter=0, sep=";", header=None, engine='python', names=['#Data operacji','#Opis operacji','#Konto','#Kategoria','#Kwota','#Remove1','#Remove2'], index_col=False)
      df = df.iloc[: , :-1]
      df = df.iloc[: , :-1]
      df['#Kwota'] = df['#Kwota'].str.replace("PLN", "")
    else:
      df = pandas.read_csv('in/' + file, encoding="cp1250", skiprows=37, skipfooter=5, sep=";", header=0, engine='python')


      #drops last column
      df = df.iloc[: , :-1]

      #remove whitespaces
      df['#Saldo po operacji'] = df['#Saldo po operacji'].str.replace(" ", "")
      

      #remove singular quotes '
      df['#Numer konta'] = df['#Numer konta'].str.replace(r"'", "")

      #remove extensive whitespaces
      try:
        df['#Tytuł'] = df['#Tytuł'].str.replace('\s+',' ',regex=True)
      except AttributeError:
        print("Ignoring atribute error") 
      df['#Nadawca/Odbiorca'] = df['#Nadawca/Odbiorca'].str.replace('\s+',' ',regex=True)
      

    #Remove white spaces
    df['#Kwota'] = df['#Kwota'].str.replace(" ", "")
    df['#Opis operacji'] = df['#Opis operacji'].str.replace('\s+',' ',regex=True)

    print(df.head(10))
    df.to_csv('out/'+file,encoding='utf-8',index=False,mode='w+')


if not os.path.exists("in/"):
  os.makedirs("in/") 

if not os.path.exists("out/"):
  os.makedirs("out/") 

#Check dir
in_entries = os.listdir('in/')

for entry in in_entries:
    convert(entry)
