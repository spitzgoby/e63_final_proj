importantTokenIndices = [1, 4, 5, 8]
# NAME = 1
# LATITUDE = 4
# LONGITUDE = 5
# COUNTRY_CODE = 8


with open('cities.csv', 'w') as outfile:
  with open('cities15000.txt') as infile:
    for line in infile:
      tokens = line.split('\t')

      # for this data set Beijing and its districts should be treated
      # as a single city, exclude districts
      if not (tokens[10] == '22' and tokens[8] == 'CN') or tokens[1] == 'Beijing':
        writeTokens = []
        for num in importantTokenIndices:
          # remove commas from city names
          writeTokens.append(tokens[num].replace(',', ''))
        print writeTokens[0]
        outfile.write(','.join(writeTokens) + '\n')
