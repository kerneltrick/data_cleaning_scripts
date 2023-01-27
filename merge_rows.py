import csv

# CONFIGURATION
input_file_name = "./datasets_for_rname_change.csv"
output_file_name = "./countries_without_duplicates.csv"
country_name_matches = [
("czech republic", "czechia")
]

# READ IN CSV
countries_with_duplicates = []
with open(input_file_name) as f:
    row_reader = csv.reader(f)
    for row in row_reader:
        countries_with_duplicates.append(row)

# VALUES WE CONSIDER TO BE EMPTY CELLS
NA = ["NA"]

print("Number of countries before duplicate removal:", len(countries_with_duplicates))

# MERGE TWO ROWS 
def merge_rows(row_1, row_2):
    new_row = []
    for cell_1, cell_2 in zip(row_1, row_1):
        if cell_1 not in NA:
            new_row.append(cell_1)
        elif cell_2 not in NA:
            new_row.append(cell_2)
        else:
            new_row.append("NA")

# CHECK TWO ROWS ARE REALLY THE SAME COUNTRY
def country_match(country_name_1, country_name_2, country_matches):
    for matches in country_name_matches:
        if country_name_1.lower() in matches and country_name_2.lower() in matches:
            return True
    return False

# BUILD NEW TABLE WITHOUT DUPLICATE ROWS
countries_without_duplicates = []
i = 0
while i < len(countries_with_duplicates):
    row_1 = countries_with_duplicates[i]
    country_name_1 = row_1[1]
    year_1 = row_1[0]
    j = i 
    found = False
    while j < len(countries_with_duplicates) and not found:
        row_2 = countries_with_duplicates[j]
        country_name_2 = row_2[1]
        year_2 = row_2[0]
        if country_name_1 == country_name_2:
            pass
        elif country_match(country_name_1, country_name_2, country_name_matches) and year_1 == year_2:
            countries_without_duplicates.append(merge_rows(row_1, row_2))
            found = True
            print("Found duplicates:", country_name_1, country_name_2)
            if j == i + 1:
                 i += 1
        j += 1
    if not found:
       countries_without_duplicates.append(row_1)
    i += 1

# WRITE OUT TO CSV
print("Number of countries after removing duplicates:", len(countries_without_duplicates))
with open(output_file_name, "w") as f:
    writer = csv.writer(f)
    for row in countries_without_duplicates:
        if row:
            writer.writerow(row)
