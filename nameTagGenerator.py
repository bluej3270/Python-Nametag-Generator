import copy
import csv
from bs4 import BeautifulSoup

# Author: Kellan Clapp
# Assignment:  CS336 Assignment #7
# Created: 11/2/2024
# Description: Generates nametags Using nametags10template.html and the data from registrant_data.csv

with open("nametags10template.html") as fp:
    # Parse the whole Template with Beautiful Soup 4
    soup = BeautifulSoup(fp, "html.parser")

    # find and extract the paper element from the template file, which contains the page element
    page = soup.find("div", {"class": "paper"})
    page.extract()

    # find and extract the row element from the page element
    row = page.find("div", {"class": "row"})
    row.extract()

    #find and extract the left and right nametag from the page element
    nametag = row.find("div", {"class": "nametag"})
    nametag.extract()

    with open("registrant_data.csv") as data:
        # Convert CSV to DictReader
        reader = csv.DictReader(data)

        max_pagecount = 10 # Number of nametags that fit on a page
        pagecount = 0 # Number of nametags on the current page
        current_page = copy.deepcopy(page)

        max_rowcount = 2 # Number of nametags that fit on a row
        rowcount = 0 # Number of nametags on the current row
        current_row = copy.deepcopy(row)

        isLeft = True # Start with a left tag

        nametags = BeautifulSoup("", "html.parser")
        nametags.append(current_page)
        current_page.find("div", {"class": "page"}).append(current_row)

        # Make a nametag for each person
        for data_row in reader:
            # If there are already max_pagecount tags on the page, create a new one
            if pagecount >= max_pagecount:
                current_page = copy.deepcopy(page)
                nametags.append(current_page)
                pagecount = 0

            # If there are already max_rowcount tags on the row, create a new one
            if rowcount >= max_rowcount:
                current_row = copy.deepcopy(row)
                current_page.find("div", {"class": "page"}).append(current_row)
                rowcount = 0

            current_tag = copy.deepcopy(nametag)

            # Fill nametag with data
            current_tag.find("span", {"class": "firstname"}).string = data_row["firstname"]
            current_tag.find("span", {"class": "lastname"}).string = data_row["lastname"]
            current_tag.find("span", {"class": "position"}).string = data_row["position"]
            current_tag.find("span", {"class": "company"}).string = data_row["company"]
            current_tag.find("span", {"class": "city"}).string = data_row["city"]
            current_tag.find("span", {"class": "state"}).string = data_row["state"]

            # Add the nametag and count it
            current_row.append(current_tag)
            rowcount += 1
            pagecount += 1

        # Insert pages into body div
        soup.find("div", {"class": "body"}).append(nametags)

        # Print to file
        with open("nametags10gen.html", "w") as output:
            output.write(soup.prettify(formatter="html5"))