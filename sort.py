import os

MIN_LEN_OF_CAPTCHA = 1
MAX_LEN_OF_CAPTCHA = 6
FILE_NAME_PREFIX = "ranair_"

with open(FILE_NAME_PREFIX + "output.csv", 'w') as output_file:
    captcha_list = []
    for file_counter in range ( MIN_LEN_OF_CAPTCHA, MAX_LEN_OF_CAPTCHA + 1 ):
        file_name = FILE_NAME_PREFIX + str(file_counter) + ".csv"
        csv_file = open(file_name, 'r')
        csv_file.readline()
        for line in csv_file:
            line = line[:-1]
            captcha_list.append(line)
        csv_file.close()   
    captcha_list = sorted(captcha_list)
    output_file.write ( FILE_NAME_PREFIX[:-1] + "\n" )
    # print (*captcha_list, sep = "\n")
    for item in captcha_list:
        output_file.write ( item + "\n" )
    output_file.close ()