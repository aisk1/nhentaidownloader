#!/usr/bin/env python3
import sys
import os
import requests
import urllib.request
from termcolor import colored, cprint

# PARAMETER CHECK
if("-h" in sys.argv or "--help" in sys.argv):
    cprint(f"Script to download nhentai images without torrent.", "white")
    cprint(f"Usage: {sys.argv[0]} <DIGIT-CODE> [FIRST-PAGE [LAST-PAGE]]",
           "yellow")
    cprint(f"Examples:", "blue")
    cprint(f"- To download all pages:")
    cprint(f"python3 nhentaidownloader.py 175769", "green")
    cprint(f"- To download all pages from page 18:")
    cprint(f"python3 nhentaidownloader.py 175769 18", "green")
    cprint(f"- To download pages from 18 to 21:")
    cprint(f"python3 nhentaidownloader.py 175769 18 21", "green")
    cprint(f"- To download only page 18:")
    cprint(f"python3 nhentaidownloader.py 175769 18 18", "green")
    exit()
elif(len(sys.argv) < 2 or len(sys.argv) > 4):
    cprint(f"ERROR! Too many or too little arguments!", "red")
    cprint(
        f"Usage: {sys.argv[0]} <DIGIT-CODE> [FIRST-PAGE [LAST-PAGE]]",
        "yellow")
    cprint(f"Get help:", "white")
    cprint(f"{sys.argv[0]} --help", "yellow")
    cprint(f"{sys.argv[0]} -h", "yellow")
    exit()
else:
    arg_digit = 1
    while arg_digit < len(sys.argv):
        if(not sys.argv[arg_digit].isdigit()):
            cprint(f"ERROR! \"{sys.argv[arg_digit]}\" is not a number!", "red")
            cprint(
                f"Usage: {sys.argv[0]} <DIGIT-CODE> [FIRST-PAGE [LAST-PAGE]]",
                "yellow")
            cprint(f"Get help:", "white")
            cprint(f"{sys.argv[0]} --help", "yellow")
            cprint(f"{sys.argv[0]} -h", "yellow")
            exit()
        arg_digit += 1


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
        cprint(f"{url} Connection etablished.({response.status_code})", "green")
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
            cprint(
                f"{url + str(page_cur)} Connection etablished.({page_response.status_code})",
                "green")
            img_src = GetImageSource(page_response.text)
            cprint(f"Downloading image from {img_src} {i}/{j}", "white")
            extension = "." + img_src[-3] + img_src[-2] + img_src[-1]
            output_img_name = str(page_cur)
            var0 = "0" * (len(str(page_count)) - len(str(output_img_name)))
            urllib.request.urlretrieve(
                img_src, create_dir + "/" + var0 + output_img_name + extension)
            cprint(
                f"Image {page_cur} out of {page_max} downloaded! \"{create_dir}/{var0}{output_img_name}.jpg\"",
                "green")
        else:
            cprint(
                f"{url + str(i)} Image download failed!({page_response.status_code})",
                "red")
        page_cur += 1
        i += 1
    cprint(
        f"Finished! Downloaded files can be found in \"{create_dir}\"",
        "yellow")


def GetImageSource(html):
    string_start = html.find("https://i.")
    image_src = ""
    while html[string_start] != "\"":
        image_src += html[string_start]
        string_start += 1
    return image_src


Main()
