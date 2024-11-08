import requests
from  bs4 import BeautifulSoup

### Helper
def extractDetailsFromUrl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    rows = table.findChildren('tr')
    
    # Details to return 
    messageArray = []
    max_x_coord = 0
    max_y_coord = 0
    
    # skip first row (header)
    for i in range (1, len(rows)):
        
        # find all span contents per row
        spanElems = rows[i].find_all('span')
        contentsList = [x.contents[0] for x in spanElems]
        
        # convert string to int
        contentsList[0] = int(contentsList[0])
        contentsList[2] = int(contentsList[2])

        # max text rows and columns
        if contentsList[0] > max_x_coord: 
            max_x_coord = contentsList[0]
        if contentsList[2] > max_y_coord: 
            max_y_coord = contentsList[2]
        
        messageArray.append(contentsList)
        
    return [messageArray, max_x_coord, max_y_coord]

def messageArrayToString(messageArray):
    message = ""
    for row in messageArray:
        for elem in row:
            message += elem
        message += "\n"
    return message

def mapCoordsToArray(codeMap,xMax, yMax):
    # xcoords = columns  from Left to Right
    # ycoords = rows from Bottom to Top
    messageArray = [[' ' for cols in range(xMax+1)] for rows in range(yMax+1)]
    for info in codeMap:
        messageArray[yMax-info[2]][info[0]] = info[1]
    
    return messageArray


### Main
smolUrl = "https://docs.google.com/document/u/0/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub?pli=1"
bigUrl = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    

url = bigUrl
 
[codeMap, max_x_coord, max_y_coord] = extractDetailsFromUrl(url)
messageArray = mapCoordsToArray(codeMap, max_x_coord, max_y_coord)
message = messageArrayToString(messageArray)

f = open("hiddenMessage.txt", "w", encoding="utf-8")
f.write(message)
f.close()
