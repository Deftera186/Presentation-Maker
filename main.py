from bs4 import BeautifulSoup as bs
from Data import Data
from Presentation_Maker import Presentation_Maker
import os, sys
import time

def Menu():
    if sys.platform == "win32": # windows
        os.system('cls')
    else:
        os.system('clear') # linux
    print("""\u001b[32;1m
  _____                          _        _   _               __  __       _
 |  __ \                        | |      | | (_)             |  \/  |     | |
 | |__) | __ ___  ___  ___ _ __ | |_ __ _| |_ _  ___  _ __   | \  / | __ _| | _____ _ __
 |  ___/ r'__/ _ \/ __|/ _ \ '_ \| __/ _` | __| |/ _ \| r'_ \  | |\/| |/ _` | |/ / _ \ '__|
 | |   | | |  __/\__ \  __/ | | | || (_| | |_| | (_) | | | | | |  | | (_| |   <  __/ |
 |_|   |_|  \___||___/\___|_| |_|\__\__,_|\__|_|\___/|_| |_| |_|  |_|\__,_|_|\_\___|_|
\u001b[0m""")


Menu()
name = input("\u001b[31;1mPlease enter a name:\u001b[0m\n")
start_time = time.time()
print("\u001b[36;1mObtains the Data...\n\u001b[0m")
data = Data()

html_code = data.find(name)
if html_code == None:
    input("\u001b[31mNo such page exists on Wikipedia!\n\u001b[0m")
    raise SystemExit

elif html_code == False:
    input("\u001b[31mYou have to be more specific in the name!\n\u001b[0m")
    raise SystemExit

extracted_data = f'*{name}*'

i = 1
Headers = 0
# How many entries are there in the table of contents?
max_s = len(bs(html_code, 'lxml').find_all('span', class_='tocnumber'))

print("\u001b[36;1mArranges the information...\n\u001b[0m")
# Extract the text from the source code
for a in bs(html_code, 'lxml').find_all(['p', 'span', 'li']):
    # Headers will be between "*"
    if a.has_attr('class') and a['class'][0] == 'mw-headline':
        extracted_data += "*" + a.text + " *\n"
        Headers += 1
    if a.name == 'li':
        # If the values are part of the table of contents, ignore them
        if i <= max_s:
            i += 1
        else:
            extracted_data += a.text + "\n"
    if a.name == 'p':
        extracted_data += a.text + "\n"

# Delete numbers between '[]'
a = extracted_data.find('[')
while a != -1:
    extracted_data = extracted_data[:a] + extracted_data[(a + 3):]
    a = extracted_data.find('[')

# Delete '[]'
extracted_data = extracted_data.replace("[", "")
extracted_data = extracted_data.replace("]", "")

# Deleting unimportant information
extracted_data = extracted_data[:extracted_data.find("ראו גם")]
print("\u001b[36;1m")
#  Downloading image for each title
try:
    images_paths = data.Images(Headers, name)
except BaseException:
    images_paths = []
print("\u001b[36;1mMaking the Presentation...\n\u001b[0m")
# Prepare the presentation
present = Presentation_Maker()
image = 0

NOT_ALLOWED = ['קישורים חיצוניים', 'הערות שוליים', 'גלריית תמונות', 'לקריאה נוספת', 'גלריית תמונות']

while len(extracted_data) > 1:
    # Finding the title
    a = extracted_data.find("*")
    b = extracted_data.find("*", a + 1)
    title = extracted_data[a + 1:b]

    # Deleting the title from the data
    extracted_data = extracted_data[b + 1:]

    # The body of the text will be up to the new title
    c = extracted_data.find("*")
    if c != -1:
        body = extracted_data[:c]
        extracted_data = extracted_data[c:]

    # If there is no new title, the remaining text is the body.
    elif c == -1:
        body = extracted_data
        extracted_data = ""
    ls = body.split()
    slides_for_body = [" ".join(ls[i:i + 42]) for i in range(0, len(ls), 42)]
    for text in slides_for_body:
        if text != '' and title not in NOT_ALLOWED:
            present.add_slide(title, [text])
    try:
        present.add_image_slide(images_paths[image])
    except BaseException:
        pass
    image += 1

present.save_prs(name)
Menu()
print("--- %s seconds ---" % (time.time() - start_time))
input()
