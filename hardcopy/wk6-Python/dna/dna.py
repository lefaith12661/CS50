import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    # open the CSV file and read its contents into memory
    csv_file = open(sys.argv[1])
    data = csv.DictReader(csv_file)

    # TODO: Read DNA sequence file into a variable
    # open the TXT file and read its contents into memory
    with open(sys.argv[2]) as txt_file:
        sequence = txt_file.read()

    # TODO: Find longest match of each STR in DNA sequence
    strs = data.fieldnames[1:]  # skips first column with names
    dict_counts = {}
    for sub_sequence in strs:
        dict_counts[sub_sequence] = longest_match(sequence, sub_sequence)

    # TODO: Check database for matching profiles
    for row in data:
        if all(dict_counts[sub_sequence] == int(row[sub_sequence]) for sub_sequence in dict_counts):
            print(row["name"])
            csv_file.close()
            return
    print("no match")
    csv_file.close()


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
