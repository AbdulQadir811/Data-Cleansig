def alter_Upper(filename):
    f = open(filename, 'r',errors='ignore')
    data = f.read()
    print((data))
    f.close()
    print(data[8031:8080])

    for letter in data:
        pass

    # Write your logic here

filename="Text_File.txt"
alter_Upper(filename)