#
# Converts Social Security XML file into a CSV containing years and earnings data
#
import csv
import xml.etree.ElementTree as ET

#
# parse through the earnings elements, create rows
#
def parseEarnings(element):
	rows = []

	for child in element:
		if child.tag.endswith("Earnings"):
			year = child.attrib.get("startYear")
			medicareEarnings = int(child[0].text)
			ficaEarnings = int(child[1].text)
			row = { "year": year, "medicareEarnings": medicareEarnings, "ficaEarnings": ficaEarnings}
			rows.append(row)
	return rows

#
# Parse the SSN XML file
#
tree = ET.parse('myinputfile.xml')
root = tree.getroot()
rows = []

#
# Pull the year, medicare earnings and FICA earnings from the XML tree
#
for child in root:
	#print child.tag, child.attrib
	if child.tag.endswith("EarningsRecord"):
		#print("Got it!")
		rows = parseEarnings(child)
		
#
# Convert the saved earnings data into a CSV file 
#
fieldnames = ['Year', 'Medicare Earnings', 'FICA Earnings']
with open('earnings.csv', 'wb') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for row in rows:
		data = { "Year": row.get("year"), 
			"Medicare Earnings": row.get("medicareEarnings"), 
			"FICA Earnings": row.get("ficaEarnings") }
		writer.writerow(data)