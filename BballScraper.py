import string
from bs4 import BeautifulSoup
import urllib
import requests
import pandas as pd


webpage = "https://www.basketball-reference.com/players/"

last = input("Enter a player's last name: ")
first = input("Enter a player's first name: ")
name = first + " " + last

FirstLetter = last[0:1]

webpage += FirstLetter
webpage = webpage.lower()

page = requests.get(webpage)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

#Get the table of all players with the same last intial
table = soup.find('table', attrs={'class':'sortable stats_table'})

#Gets each row and makes it iterable
rows = table.find('tbody').find_all('tr')

#This nested for loop will get the extension needed for the specific player's page
addon = ""
for row in rows:
    cols = row.find_all('th')
    for col in cols:
        if name in str(col):
            add_on = col.find("a")
            addon = add_on['href'][10:]

#This gets us to the player's individual page
webpage += addon
page = requests.get(webpage)
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

#This finds the row of the selected player
body = soup.find('div', attrs={'class': 'table_wrapper',  'id':'all_per_game'}).find('tbody')
#print(body)
rows = soup.find('div', attrs={'class': 'table_wrapper', 'id': 'all_per_game'}).find('tbody').findAll('tr')
#print(rows)

#This gets the season and ppg from all seasons the player has played
ppg = []
years = []
rebs = []
for row in rows:
    #This checks if they didn't play that year. If so, a ppg of 0 is assigned
    #print(row.findAll('td'))
    if row.find('td', attrs={'data-stat': 'pts_per_g'}) == None:
        tdd = "0"
        other = row.find('td').contents[0]
        reb = "0"
    else:
        tdd = row.find('td', attrs={'data-stat': 'pts_per_g'}).contents[0]
        other = row.find('th', attrs={'data-stat': 'season'}).find('a').contents[0]
        reb = row.find('td', attrs={'data-stat': 'trb_per_g'}).contents[0]
    # This checks if the stat is bolded on the webpage, meaning it was a league leading stat.
    # If it is, this nested if statement (done so to avoid doing str.name, which throws an error) extracts the value
    if tdd != "0":
        if tdd.name == 'strong':
            tdd = tdd.contents[0]
    word = other + ": " + tdd
    years.append(other)
    ppg.append(tdd)
    rebs.append(reb)
    #print(word)
career = soup.find('div', attrs={'class': 'table_wrapper',  'id':'all_per_game'}).find('tfoot').find('td', attrs={'data-stat': 'pts_per_g'}).contents[0]
#print("Career: " +  career)
#s = pd.DataFrame([ppg, reb], index=years, columns=["Pts","Rebs"])
s = pd.DataFrame({"Pts": ppg, "Rpg": rebs}, index=years)
print(s)
print("Career: " + career)
