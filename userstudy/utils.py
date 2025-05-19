import numpy as np
import csv


def choose_imgs(input_list, target_num):
    
    N = len(input_list)
    output = []
    while len(output) < target_num:
        idxs = np.random.permutation(N)[0:2]
        idxs = sorted(idxs)
        if( idxs not in output ):
            output.append([ input_list[i] for i in idxs ])

    return output



def CommaString_to_IntArray(input):
    
    output = input.split(',')
    output = [int(i) for i in output]
    
    return output

def IntArray_to_CommaString(input):
    
    output = ""
    for x in input:
        output += str(x) + ","

    output = output[:-1] # delete last comma

    return output


def save_csv(output_filename, header, data):

    with open(output_filename, 'w+') as file:
        print(f"Save {output_filename}")
        writer = csv.writer(file)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)

def load_csv(input_filename):
    
    with open(input_filename, 'r') as f:
        print(f"Load {input_filename}")
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row)

    header = data[0]
    data = data[1:]
    
    return data, header