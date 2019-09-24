

input_data = "/scratch1/NOT_BACKED_UP/dbuchan/interpro/derived/word2vec_input_E.dat"

G100 = 0
G200 = 0
G300 = 0
G400 = 0
G500 = 0

with open(input_data, "r") as id:
    for line in id:
        if 'G100' in line:
            G100+=1
        if 'G200' in line:
            G200+=1
        if 'G300' in line:
            G300+=1
        if 'G400' in line:
            G400+=1
        if 'G500' in line:
            G500+=1

print('G100', G100)
print('G200', G200)
print('G300', G300)
print('G400', G400)
print('G500', G500)
