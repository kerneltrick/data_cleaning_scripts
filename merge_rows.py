import csv

# CONFIGURATION
input_file_name = "./datasets_for_rname_change.csv"
output_file_name = "./countries_without_duplicates.csv"
country_name_matches = [
("bolivia", "bolivia (plurinational state of)"),
("brunei", "brunei darussalam"),
("central african rep.", "central african republic"),
("democratic people’s republic of korea", "south korea"),
("lao people’s democratic republic", "laos"),
("rep. of korea", "north korea"),
("viet nam", "vietnam"),
("rep. of moldova", "moldova"),
("russian federation", "russia"),
("north macedonia", "macedonia"),
("türkiye", "turkey"),
("united kingdom of great britain and northern ireland", "united kingdom"),
("united states of america", "united states"),
("dominican rep.", "dominican republic"),
("venezuela (bolivarian republic of)", "venezuela"),
("iran (islamic rep. of)", "iran"),
("state of palestine", "palestine"),
("syrian arab rep.", "syria"),
("eswatini", "swaziland"),
("united rep. of tanzania", "tanzania"),
("gambia", "the gambia"),
("congo", "republic of the congo"),
("czech republic", "czechia"),
("cote d'ivoire", "cote d'ivoire"),
("guinea-bissau", "guinea bissau"),
("yemen arab republic", "people's republic of yemen")
("St. Kitts and Nevis", "Saint Kitts and Nevis")
]

replacements = {
"Cote d'Ivoire":"Cote D'Ivoire", # Change d to D
"Rep. of Korea":"North Korea",
"Republic of the Congo":"Congo",
"Serbia and Kosovo: S/RES/1244 (1999)":"Serbia and Kosovo",
"The Gambia":"Gambia",
"United Rep. of Tanzania":"Tanzania",
"Syrian Arab Rep.": "Syria",
"People's Republic of Yemen": "Yemen",
"Yemen Arab Republic": "Yemen",
"Türkiye": "Turkey",
"United States of America": "United States",
"Venezuela (Bolivarian Republic of)": "Venezuela",
"Viet Nam": "Vietnam",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"Czech Republic": "Czechia",
"Eswatini": "Swaziland",
"Guinea Bissau": "Guinea-Bissau",
"Democratic Republic of the Congo": "Dem. Rep. of the Congo",
}


# READ IN CSV
countries_with_duplicates = []
with open(input_file_name) as f:
    row_reader = csv.reader(f)
    for row in row_reader:
        countries_with_duplicates.append(row)

# VALUES WE CONSIDER TO BE EMPTY CELLS
NA = ["NA"]

# MERGE TWO ROWS 
def merge_rows(row_1, row_2):
    new_row = []
    for cell_1, cell_2 in zip(row_1, row_2):
        if cell_1 not in NA:
            new_row.append(cell_1)
        elif cell_2 not in NA:
            new_row.append(cell_2)
        else:
            new_row.append("NA")
    return new_row

# CHECK TWO ROWS ARE REALLY THE SAME COUNTRY
def country_match(country_name_1, country_name_2, country_matches):
    if country_name_1.lower() == country_name_2.lower():
        return country_name_1:
    for matches in country_matches:
        if country_name_1.lower() in matches and country_name_2.lower() in matches:
            return True
    return None 

# BUILD NEW TABLE WITHOUT DUPLICATE ROWS
print("Number of countries before duplicate removal:", len(countries_with_duplicates))
countries_without_duplicates = []
i = 0
processed = {}
while i < len(countries_with_duplicates):
    row_1 = countries_with_duplicates[i]
    country_name_1 = row_1[1]
    year_1 = row_1[0]
    print(i)
    if year_1 not in processed:
        processed[year_1] = []
    if country_name_1 in processed[year_1]:
        i += 1
        continue
    processed[year_1].append(country_name_1)
    j = i + 1
    found = False
    while j < len(countries_with_duplicates):
        row_2 = countries_with_duplicates[j]
        country_name_2 = row_2[1]
        year_2 = row_2[0]
        if country_match(country_name_1, country_name_2, country_name_matches) and year_1 == year_2:
            row_1 = merge_rows(row_1, row_2)
            processed[year_1].append(country_name_2)
        j += 1
    countries_without_duplicates.append(row_1)
    i += 1

for i in range(len(countries_without_duplicates)):
    country_name = countries_without_duplicates[i][1]
    if country_name in replacements.keys():
        countries_without_duplicates[i][1] = replacements[country_name]

# WRITE OUT TO CSV
print("Number of countries after removing duplicates:", len(countries_without_duplicates))
with open(output_file_name, "w") as f:
    writer = csv.writer(f)
    for row in countries_without_duplicates:
        if row:
            writer.writerow(row)
