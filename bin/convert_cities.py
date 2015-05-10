#! finalenv/bin/python

importantTokenIndices = [0, 1, 4, 5, 8, 14]
# GEONAME_ID = 0
# NAME = 1
# LATITUDE = 4
# LONGITUDE = 5
# COUNTRY_CODE = 8
# POPULATION = 14

with open('cities.csv', 'w') as outfile:
  with open('cities15000.txt') as infile:
    for line in infile:
      tokens = line.split('\t')
      if tokens[6] == 'P':
        writeTokens = []
        for num in importantTokenIndices:
          writeTokens.append(tokens[num])
        print writeTokens[1]
        outfile.write(','.join(writeTokens) + '\n')
