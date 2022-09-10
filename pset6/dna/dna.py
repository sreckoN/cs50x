from sys import argv
from cs50 import get_string


def main():

    person_dict = {}
    matched_dna_patterns = []

    if len(argv) != 3: 
        print("Error")
        exit(1)

    csv_file = open(argv[1], 'r')
    for data_row, row in enumerate(csv_file):
        rows = row.strip().split(',')
        if (data_row == 0):
            dna_patterns = rows[1:]
        else:
            person_dict[rows[0]] = [int(dna_counts) for dna_counts in rows[1:]]

    dna_sequence = open(argv[2], 'r').read()
    
    for i in range(len(dna_patterns)):
        matched_dna_patterns.append(maximum_occurances(dna_sequence, dna_patterns[i]))
        
    for name, data in person_dict.items():
        if data == matched_dna_patterns:
            print(name)
            exit(0)
    
    print('No match')
    
    
def maximum_occurances(dna_seq, dna_pattern):
    temp_dna_pattern = [0] * len(dna_seq)
    for x in range(len(dna_seq) - len(dna_pattern), -1, -1):
        if dna_seq[x: x + len(dna_pattern)] == dna_pattern:
            if x + len(dna_pattern) > len(dna_seq) - 1:
                temp_dna_pattern[x] = 1
            else:
                temp_dna_pattern[x] = 1 + temp_dna_pattern[x + len(dna_pattern)]
    return max(temp_dna_pattern)


main()
