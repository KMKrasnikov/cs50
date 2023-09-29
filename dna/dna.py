import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py databases/small.csv(large.csv) sequences/(1 to 20).txt")
    # TODO: Read database file into a variable
    database = {}
    db_list = []
    # Read datebase into memory from file
    with open(sys.argv[1], "r") as file:
        reader = csv.reader(file)
        for row in reader:
            db = row[0]
            # Create first row in dictionary
            if database == {}:
                database[db] = row[1:]
            # Create second row and change value to integer
            else:
                database[db] = list(map(int, row[1:]))
            # Create list of value
            db_list.append(db)
    # TODO: Read DNA sequence file into a variable
    # Read datebase into memory from file
    with open(sys.argv[2], "r") as file_dna:
        dna_person = file_dna.readline()

    # TODO: Find longest match of each STR in DNA sequence
    match = []
    for i in database[db_list[0]]:
        match.append(longest_match(dna_person, i))

    # TODO: Check database for matching profiles
    for key, value in database.items():
        if match == value:
            print(f"{key}")
            break
        if key == db_list[len(db_list) - 1] and match != key:
            print("No match")


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
