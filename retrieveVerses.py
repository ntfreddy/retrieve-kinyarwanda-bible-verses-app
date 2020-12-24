import codecs
import urllib.request
import re

booksDict = {
    "Itangiriro":"itangiriro",
    "Kuva":"kuva",
    "Abalewi":"abalewi",
    "Kubara":"kubara",
    "Gutegeka kwa kabiri":"gutegeka_kwa_kabiri",
    "Yosuwa":"yosuwa",
    "Abacamanza":"abacamanza",
    "Rusi":"rusi",
    "1 Samweli":"1_samweli",
    "2 Samweli":"2_samweli",
    "1 Abami":"1_abami",
    "2 Abami":"2_abami",
    "1 Ibyo ku Ngoma":"1_ibyo_ku_ngoma",
    "2 Ibyo ku Ngoma":"2_ibyo_ku_ngoma",
    "Ezira":"ezira",
    "Nehemiya":"nehemiya",
    "Esiteri":"esiteri",
    "Yobu":"yobu",
    "Zaburi":"zaburi",
    "Imigani":"imigani",
    "Umubwiriza":"umubwiriza",
    "Indirimbo ya Salomo":"indirimbo",
    "Yesaya":"yesaya",
    "Yeremiya":"yeremiya",
    "Amaganya":"amaganya",
    "Ezekiyeli":"ezekiyeli",
    "Daniyeli":"daniyeli",
    "Hoseya":"hoseya",
    "Yoweli":"yoweli",
    "Amosi":"amosi",
    "Obadiya":"obadiya",
    "Yona":"yona",
    "Mika":"mika",
    "Nahumu":"nahumu",
    "Habakuki":"habakuki",
    "Zefaniya":"zefaniya",
    "Hagayi":"hagayi",
    "Zekariya":"zekariya",
    "Malaki":"malaki",
    "Matayo":"matayo",
    "Mariko":"mariko",
    "Luka":"luka",
    "Yohana":"yohana",
    "Ibyakozwe n’Intumwa":"ibyakozwe_n_intumwa",
    "Abaroma":"abaroma",
    "1 Abakorinto":"1_abakorinto",
    "2 Abakorinto":"2_abakorinto",
    "Abagalatiya":"abagalatiya",
    "Abefeso":"abefeso",
    "Abafilipi":"abafilipi",
    "Abakolosayi":"abakolosayi",
    "1 Abatesalonike":"1_abatesalonike",
    "2 Abatesalonike":"2_abatesalonike",
    "1 Timoteyo":"1_timoteyo",
    "2 Timoteyo":"2_timoteyo",
    "Tito":"tito",
    "Filemoni":"filemoni",
    "Abaheburayo":"abaheburayo",
    "Yakobo":"yakobo",
    "1 Petero":"1_petero",
    "2 Petero":"2_petero",
    "1 Yohana":"1_yohana",
    "2 Yohana":"2_yohana",
    "3 Yohana":"3_yohana",
    "Yuda":"yuda",
    "Ibyahishuwe":"ibyahishuwe"
}

def parseText(text):
    semiColonResults = text.split(":")
    spaceResults = semiColonResults[0].split(" ")
    commaResults = semiColonResults[1].split(",")

    chapterStr = spaceResults[len(spaceResults) - 1]
    bookStr = " ".join(spaceResults[0:len(spaceResults) - 1])
    verses = []
    for commaUnit in commaResults:
        dashResults = commaUnit.split("-")

        for n in range(int(dashResults[0]),int(dashResults[len(dashResults) - 1])+1):
            verses.append(n)

    return {
        'book':booksDict[bookStr.strip()],
        'chapter': int(chapterStr.strip()),
        'verses':verses}

def retrieveVerse(content, verse):
    result = ""
    token = "cont-" + str(verse)
    occIndex = content.find(token)
    if occIndex > -1:
        verseStartIndex = content.find("style",occIndex, occIndex + 100)
        verseEndIndex = content.find("</div>",occIndex, occIndex + 500)
        if verseStartIndex > -1 and verseEndIndex > -1:
            result = content[verseStartIndex + 24:verseEndIndex-1]

        result = result.replace("&#8216;","‘")
        result = result.replace("&#8217;","’")
        result = result.replace("&#8220;","“")
        result = result.replace("&#8221;","”")

        result = result.replace("&#8216","‘")
        result = result.replace("&#8217","’")
        result = result.replace("&#8220","“")
        result = result.replace("&#8221","”")

        result = result.strip()
    return result

texts = {}
print("Starting ...................")
with open('./verses.txt', encoding='utf-8') as file:
    texts = [l.rstrip("\n") for l in file]

    for text in texts:
        textObject = parseText(text)
        book = textObject['book']
        chapter = textObject['chapter']
        verses = textObject['verses']
        urlName = "https://bibiliya.com/yera/" + book + "-" + str(chapter) + "/"
        print (text)
        x = urllib.request.urlopen(urlName)
        stream = x.read().decode("utf-8")

        for verse in verses:            
            printedVerse = retrieveVerse(stream,verse)
            print(printedVerse)

