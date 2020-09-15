import sys
import os
import requests
import urllib.request
from termcolor import colored, cprint
# PARAMETER CHECK
if(len(sys.argv) < 2):
    cprint(f"Usage: {sys.argv[0]} <DIGIT-CODE> [FIRST-PAGE [LAST-PAGE]]", "yellow")
    exit()
elif(not sys.argv[1].isdigit()):
    cprint(f"ERROR! \"{sys.argv[1]}\" contains other characters than only numbers!", "red")
    exit()
elif(len(sys.argv) == 3):
    if(not sys.argv[2].isdigit() or int(sys.argv[2]) < 1):
        cprint(f"ERROR! \"{sys.argv[2]}\" contains other characters than only numbers or is lower than 1!", "red")
        exit()
elif(len(sys.argv) == 4):
    if(not sys.argv[2].isdigit() or not sys.argv[3].isdigit() or int(sys.argv[2]) < 1 or int(sys.argv[3]) < 1):
        cprint(f"ERROR! \"{sys.argv[2]}\" or \"{sys.argv[3]}\" contains other characters than only numbers or is lower than 1!", "red")
        exit()
    else:
        if(int(sys.argv[2]) > int(sys.argv[3])):
            cprint(f"ERROR! {{FIRST-PAGE}}({sys.argv[2]}) is bigger than {{LAST-PAGE}}({sys.argv[3]})!", "red")
            exit()
elif(len(sys.argv) > 4):
    cprint(f"Usage: {sys.argv[0]} <DIGIT-CODE> [FIRST-PAGE [LAST-PAGE]]", "yellow")
# Variables
create_dir = os.getcwd() + "/" + sys.argv[1]
url = "https://nhentai.net/g/" + str(sys.argv[1]) + "/"


def Main():
    CreateDirectory()


def CreateDirectory():
    if(not os.path.exists(create_dir)):
        try:
            os.mkdir(create_dir)
        except OSError:
            cprint(f"ERROR! Creating directory '{create_dir}' failed!", "red")
            exit()
        else:
            cprint(f"Directory '{create_dir}' created successfully.", "green")
    else:
        cprint(f"Directory '{create_dir}' already exists.", "green")
    RequestPage()


def RequestPage():
    response = requests.get(url)
    if(response.status_code < 400):
        cprint(f"{url} Connection etablished({response.status_code}).", "green")
        GetPageCount(response.text)
    else:
        cprint(f"{url} Connection failed!({response.status_code})", "red")


def GetPageCount(html_source):
    page_num_address = html_source.find("num_pages")
    add_num_address = False
    page_count = ""
    while html_source[page_num_address] != ",":
        if(html_source[page_num_address] == ":"):
            add_num_address = True
        if(add_num_address and html_source[page_num_address] != ":"):
            page_count += html_source[page_num_address]
        page_num_address += 1
    cprint(f"Number of pages: {page_count}", "white")
    RequestSpecificPage(int(page_count))


def RequestSpecificPage(page_count):
    if(len(sys.argv) == 2):
        page_min = 1
        page_cur = 1
        page_max = page_count
    elif(len(sys.argv) == 3):
        page_min = int(sys.argv[2])
        page_cur = page_min
        page_max = page_count
    else:
        page_min = int(sys.argv[2])
        page_cur = page_min
        page_max = int(sys.argv[3])
        if(page_max > page_count):
            page_max = page_count
    i = 1
    j = int(page_max) - int(page_min) + 1
    while page_cur <= page_max:
        page_response = requests.get(url + str(page_cur))
        if(page_response.status_code < 400):
            cprint(f"{url + str(page_cur)} Connection etablished.({page_response.status_code})", "green")
            img_src = GetImageSource(page_response.text)
            cprint(f"Downloading image from {img_src} {i}/{j}", "white")
            output_img_name = str(page_cur)
            urllib.request.urlretrieve(
                img_src, create_dir + "/" + output_img_name + ".jpg")
            cprint(f"Image {page_cur} out of {page_max} downloaded! \"{create_dir}/{output_img_name}.jpg\"", "green")
        else:
            cprint(f"{url + str(i)} Image download failed!({page_response.status_code})", "red")
        page_cur += 1
        i += 1
    cprint(f"Finished! Downloaded files can be found in \"{create_dir}\"", "yellow")


def GetImageSource(html):
    string_start = html.find("https://i.")
    image_src = ""
    while html[string_start] != "\"":
        image_src += html[string_start]
        string_start += 1
    return image_src


Main()
