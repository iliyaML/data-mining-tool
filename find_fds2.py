# -*- coding: utf-8 -*-
"""
Data Mining Programming Assignment
This script aims to discover approximate functional dependencies in a given 
data set.
"""
import sys
import time

def pprint(FDs):
    """Pretty print of discovered FDs
    """
    print('\nDiscovered FDs:')
    for fd in FDs:
        print(', '.join(fd[0]), " -> ", fd[1], ' with support ', fd[2])

def load_data(data_file_name):
    """Read data from data_file_name and return a list of lists, 
    where the first list (in the larger list) is the list of attribute names, 
    and the remaining lists correspond to the tuples (rows) in the file.
    """
    with open(data_file_name, 'r') as f:
        results = []
        for line in f:
                words = line.split(',')
                results.append(words[:])
    return results

def find_approximate_functional_dependencies(data_file_name, depth_limit, minimum_support):
    """Main function which you need to implement!
    
    The function discovers approximate functional dependencies in a given data
    
    Input:
        data_file_name - name of a CSV file with data 
        depth_limit - integer that limits the depth of search through the space of 
            domains of functional dependencies
        minimum_support - threshold for identifying adequately approximate FDs
        
    Output:
        FDs - a list of tuples. Each tuple represents a discovered FD.
        The first element of each tuple is a list containing LHS of discovered FD
        The second element of the tuple is a single attribute name, which is RHS of that FD
        The third element of the tuple is support for that FD
    
    Output example:
        [([A],C, 0.91), ([C, F],E, 0.97), ([A,B,C],D, 0.98), ([A, G, H],F, 0.92)]
        The above list represent the following FDs:
            A -> C, with support 0.91
            C, F -> E, with support 0.97 
            A, B, C -> D, with support 0.98
            A, G, H -> F, with support 0.92                   
    """
    #read input data:
    input_data = load_data(data_file_name)
    
    #Transform input_data (list of lists) into some better representation.
    #You need to decide what that representation should be.
    #Data transformation is optional!

    #--------Your code here! Optional! ----------#
    
    #Discover FDs with given minimum support and depth limit:
    first_row = input_data[0]
    total = len(input_data) - 1
    # print(total)
    first_row[-1] = first_row[-1].strip()
    dic = {k: v for v, k in enumerate(first_row)}
    #for i in dic:
        # print(str(i) + ' ' + str(dic[i]))
    first_row_set = set(first_row)
    output = [None] * depth_limit
    target = []
    output = []
    fds = cb(target, first_row, output, depth_limit)
    array_tuples = []
    for i in range(len(fds)):
        # print(fds[i])
        remaining = list(first_row_set - set(fds[i]))
        for x in range(len(remaining)):
            array_tuples.append((tuple(fds[i]), remaining[x]))
        # print(list(first_row_set - set(fds[i])))

    dict_fds = {}
    for i in range(len(array_tuples)):
        # print(array_tuples[i][0][0])
        dict_fds[array_tuples[i]] = {}
        # print(array_tuples[i])
    
    for i in dict_fds:
        attr = list(i[0])
        # attr.append(i[1])
        for x in input_data[1:]: # Go through each column in spreadsheet
            tmp = []
            for z in attr: # Find keys
                tmp.append(x[dic[z]].strip())

            val = x[dic[i[1]]].strip()

            tmp_tuple = tuple(tmp)
            # dict_fds[]
            # print(tmp_tuple)

            if tmp_tuple in dict_fds[i]:
                if val in dict_fds[i][tmp_tuple]:
                    dict_fds[i][tmp_tuple][val] = dict_fds[i][tmp_tuple][val] + 1
                else:
                    dict_fds[i][tmp_tuple][val] = 1
            else:
                dict_fds[i][tmp_tuple] = {}
                dict_fds[i][tmp_tuple][val] = 1

    result_dict = {}

    for i in dict_fds:
        # print('key: ' + str(i))
        # print('value: ' + str(dict_fds[i]))
        sum = 0
        for x in dict_fds[i]:
            # print('value inside value: ' + str(dict_fds[i][x]))
            maxi = max(dict_fds[i][x], key=dict_fds[i][x].get)
            sum = sum + dict_fds[i][x][maxi]
            # print('\tmax: ' + str(dict_fds[i][x][maxi]) + ' ' + str(maxi))
        
        prob = sum / total
        # print('max: ' + str(max(dict_fds[i], key=dict_fds[i].get)))
        # print('Prob: ' + str(prob))

        result_dict[i] = prob
        # print('------')
        # print('key' + str(i))
        # print(str(attr) + ' ' + str(dict_fds[i]))
    # print('\n')
    # print(dict_fds[(('A',), 'B')])

    # for i in result_dict:
    #     print(str(i) + ' => ' + str(result_dict[i]))

    print('--------------------------------------')

    #print(result_dict)
    FDs = []

    # for i in result_dict:
    #     print(str(i) + ' => ' + str(result_dict[i]))

    for i in result_dict:
        if result_dict[i] >= minimum_support:
            # print(str(i) + ' => ' + str(result_dict[i]))
            # print('\tFD: ' + str(list(i[0])))
            # print('\tval: ' + i[1])
            entry = (list(i[0]), i[1], result_dict[i])
            FDs.append(entry)
    
    #--------Your code here!---------------------#
    
    return FDs

def cb(target, data, output, depth):
    """
    Finding all possible keys of FDs
    """
    for i in range(len(data)):
        new_target = target[:]
        new_data = data[:]
        new_target.append(data[i])
        new_data = data[i+1:]
        
        if len(new_target) <= depth:
        #print(new_target)
            output.append(new_target)
            cb(new_target, new_data, output, depth)
    return output

if __name__ == '__main__':
    #parse command line arguments:
    if (len(sys.argv) < 3):
        print('Wrong number of arguments. Correct example:')
        print('python find_fds.py IndividualProjectTestSet1.csv 3 0.91')
    else:
        data_file_name = str(sys.argv[1])
        depth_limit = int(sys.argv[2])
        minimum_support = float(sys.argv[3])

        # Start timer
        start_time = time.time()

        FDs = find_approximate_functional_dependencies(data_file_name, depth_limit, minimum_support)

        # Stop timer
        stop_time = time.time()
        
        # Print you  findings:
        pprint(FDs)
        print('\nRuntime: %s seconds' % str(stop_time - start_time))