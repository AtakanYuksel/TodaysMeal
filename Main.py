from bs4 import BeautifulSoup
import requests
import datetime
import re

source = requests.get("https://extranet.tedas.gov.tr/Home/TumYemekListesi").text
soup = BeautifulSoup(source, "lxml")

today = datetime.datetime.now().strftime("%d.%m.%Y")
tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")

offset_today = 0
offset_tomorrow = 0
if today[0] == "0":
    offset_today = 1
if tomorrow[0] == "0":
    offset_tomorrow = 1

meal_today = soup.select("tr[data-gununtarihi='{date}']".format(date=str(today)[offset_today:]))
meal_tomorrow = soup.select("tr[data-gununtarihi='{date}']".format(date=str(tomorrow)[offset_tomorrow:]))

try:
    meal_today = str(str(meal_today).split("<td>")[2])
    meal_today = re.findall("\>[^a-z;]{3,}\<", meal_today)
    print("{date} TARİHLİ YEMEK".format(date=today))
    for i in meal_today:
        print(i[1:-2])
except IndexError:
    print("{date} TARİHLİ YEMEK BULUNAMADI.".format(date=today))

print()

try:
    meal_tomorrow = str(str(meal_tomorrow).split("<td>")[2])
    meal_tomorrow = re.findall("\>[^a-z]{3,30}\<", meal_tomorrow)
    print("{date} TARİHLİ YEMEK".format(date=tomorrow))
    for i in meal_tomorrow:
         print(i[1:-2])
except IndexError:
    print("{date} TARİHLİ YEMEK BULUNAMADI.".format(date=tomorrow))

print("\n")
input("ÇIKMAK İÇİN HERHANGİ TUŞA BAS...")
