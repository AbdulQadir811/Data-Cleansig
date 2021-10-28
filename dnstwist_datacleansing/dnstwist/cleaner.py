import os
from datetime import datetime
import logging
import csv

logger = logging.getLogger("CLEANER_LOG")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('main_file.log')
formatter = logging.Formatter( "%(name)s,%(levelno)s,%(levelname)s,%(msg)s,%(module)s,%(funcName)s,%(lineno)s,%(exc_text)s,%(process)s,%(thread)s,%(threadName)s")
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



input_file_name = "input_file.txt"
output_file_name = "output.txt"

first_csv_name = "first_csv.csv"
second_csv_name = "second_csv.csv"




def get_dnstwist_output():

    try:
        try:
            input_read = open(input_file_name, "r")
            read = open(input_file_name, "r")
            nonempty_lines = [line.strip("\n") for line in read if line != "\n"]
            line_count = len(nonempty_lines)
            read.close()
            i =0

            for x in input_read:
                i = i + 1


                date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
                print("{}/{}  {} Processing...\nFor dnstwist progross Check output{}_{}.txt  ".format(i,line_count,x.strip(),i,date))
                cmd  = 'dnstwist ' + x.strip() + ' > output' + str(i) + '_' + date + '.txt'
                print ("cmd >>> ", cmd)
                os.system(cmd)
                file_name = 'output'+str(i)+'_'+date+'.txt'
                print("file name  >>> ",file_name)



                #print(file_name)
                remove_nonascii(file_name)
        except Exception as e:
            logger.exception("[!] error occurs in reading input file", exc_info=True)
    except Exception as e:
        logger.exception("[!] error occurs in get_dnstwist_output", exc_info=True)



def remove_nonascii(file_name):
    flag = False
    #csv_filename = "first_outputfile.csv"
    try:
        output_read = open(file_name, "r")
        try:
            for x in output_read:
                if "original*" in x:
                    flag =True
                if flag == True:
                    x = x.split()
                    #text =x[1].split(".")[0]

                    text = x[1]
                    if text.isascii():
                        write_csv(text,first_csv_name)

        except  Exception as e:
            logger.exception("[!] error occurs remove_nonascii loop", exc_info=True)

        remove_exctention(first_csv_name)
    except Exception as e:
        logger.exception("[!] error occurs in data_cleaning", exc_info=True)


def remove_exctention(csvfile_name):
    import pandas as pd
    try:
        df= pd.read_csv(csvfile_name)
        df4 =df
        df3 = df4['Name'].str.split(".").str[-1]
        unique_elements_list = df3.unique()
        print(unique_elements_list)
        for i in unique_elements_list:
            df["Name"] = df["Name"].apply(lambda x: x.replace("." +i, ""))

        df.to_csv(second_csv_name, index=False)
    except Exception as e:
        logger.exception("[!] error occured in remove_extention", exc_info=True)


def write_csv(data,csv_filename):
    try:
        with open(csv_filename, mode='a') as cleaned_file:
            cleaned_file_writer = csv.writer(cleaned_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            cleaned_file_writer.writerow([data])
    except Exception as e:
        logger.exception("[!] error occurs in write_csv", exc_info=True)


def write_header(csvfile_name):
    try:
        with open(csvfile_name, mode='w') as cleaned_file:
            cleaned_file_writer = csv.writer(cleaned_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            cleaned_file_writer.writerow(['Name'])
    except  Exception as e:
        logger.exception("[!] error occured in  writing_header  ", exc_info=True)


def main():

    logger.info(" >>>>>>> Start <<<<<<< TIME : {}".format(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")))
    write_header(first_csv_name)
    write_header(second_csv_name)
    get_dnstwist_output()

    logger.info(" >>>>>>> Finish <<<<<<< TIME : {}".format(datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")))

    #clean_data()


if __name__ == "__main__":
    main()