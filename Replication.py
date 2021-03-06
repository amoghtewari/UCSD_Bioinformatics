"""
We start sliding the window at position 0 of Text, but where should we stop?
In general, the final k-mer of a string of length n begins at position n-k;
for example, the final 3-mer of "GACCATACTG", which has length 10, begins at
position 10 - 3 = 7. This observation implies that the window should slide
between position 0 and position len(Text)-len(Pattern).

input:    pattern - sequence of base pattern we are searching for
          ex: "GCGATCGCG"
          text- the full base sequence string
          ex: "GCG"
output:   the number of times Pattern appears in Text
          ex: 2
"""
def PatternCount(Pattern, Text):
    count = 0
    # determine index value we can stop checking for pattern (see explaination above)
    for i in range(len(Text)-len(Pattern)+1):
        # can access characters in text string Text[start index: up to but not including end index]
        if Text[i:i+len(Pattern)] == Pattern:
            count = count+1
    return count


#Text = "GACCATCAAAACTGATAAACTACTTAAAAATCAGT"
#Pattern = "AAA"
#print(PatternCount(Pattern, Text))
"""
input:    text- full base sequence string
          ex: "CGATATATCCATAG"
          k or k-mer is the length of pattern we are searching for (ex: 3-mer "ATA")
          ex: 3
output:   Count is a dictionary that stores results of PatternCount
          ex: {0: 1, 1: 1, 2: 3, 3: 2, 4: 3, 5: 2, 6: 1, 7: 1, 8: 1, 9: 1, 10: 3, 11: 1}
"""
def CountDict(Text, k):
    Count = {}
    # same range as range(len(Text)-len(Pattern)+1) above because k == len(Pattern)
    for i in range(len(Text)-k+1):
        # flexible creation of pattern so we don't have to hardcode it directly into PatternCount
        Pattern = Text[i:i+k]
        Count[i] = PatternCount(Pattern, Text)
    return Count

"""
input:    list- list returned from FrequentWords
output:   list with no duplicate FrequentWords
"""
def RemoveDuplicates(Items):
    ItemsNoDuplicates = []
    for i in Items:
        # append to new list if input item not in new list
        if i not in ItemsNoDuplicates:
            ItemsNoDuplicates.append(i)
    return ItemsNoDuplicates

"""
input:text- full base sequence string
      ex: "ACGTTGCATGTCGCATGATGCATGAGAGCT"
      k or k-mer is the length of pattern we are searching for (ex: 3-mer "ATA")
      ex: 4
output: list of frequent patterns
        ex: GCAT CATG GCAT CATG GCAT CATG

complexity of this algorithm as O(|Text|2 · k)
"""
def FrequentWords(Text, k):
    # initialize empty list
    FrequentPatterns = []
    # store Count dictionary that stores result of PatternCount (the number of a times a pattern appears in the text)
    Count = CountDict(Text, k)
    # Count.values() returns a list of all the values in the in Count dictionary
    # max(Count.values()) returns the maximum value in the Count dictionary
    m = max(Count.values())
    # loop through Count dictionary
    for i in Count:
        # if the number of times the pattern appears in text == max value
        if Count[i] == m:
            # push the text pattern string into the FrequentPatterns list
            FrequentPatterns.append(Text[i:i+k])
    # avoid duplicate frequent words
    FrequentPatternsNoDuplicates = RemoveDuplicates(FrequentPatterns)
    return FrequentPatternsNoDuplicates

# Text = "ACGTTGCATGTCGCATGATGCATGAGAGCT"
# k = 4
# print(FrequentWords(Text,k))

"""
input: Pattern - DNA string pattern
       ex: Pattern = 'ATGATCAAG'
output: The reverse complement of a DNA string Pattern is the string formed by
        taking the complementary nucleotide of each nucleotide in Pattern, then
        reversing the resulting string
       ex: 'ACCGGGTTTT'
"""
def ReverseComplement(Pattern):
    # transform string into list
    input_list = list(Pattern)
    # create list to store complimentary string
    comp_list = []
    # loop through list and transform each nucleotide in DNA to its complimentary nucleotide
    for char in input_list:
        if char == 'A':
            comp_list.append('T')
        elif char == 'T':
            comp_list.append('A')
        elif char == 'C':
            comp_list.append('G')
        elif char == 'G':
            comp_list.append('C')
        else:
            print('Unable to determine nucleotide compliment')

    # reverse compliment list
    comp_list.reverse()
    # transform reversed compliment list back into a string
    revComp = ''.join(comp_list)
    # return reversed compliment string
    return revComp

#Pattern = 'GATTACA'
#print(ReverseComplement(Pattern))

"""
However, before concluding that we have found the DnaA box of Vibrio cholerae,
the careful bioinformatician should check if there are other short regions in the
Vibrio cholerae genome with multiple occurrences of "ATGATCAAG" (or "CTTGATCAT").
After all, maybe these strings occur as repeats throughout the entire Vibrio
cholerae genome, rather than just in the ori region.
"""

"""
input: Pattern-  DNA string pattern
       ex: Pattern = 'ATAT'
       Genome- entire genome string pattern
       ex: Genome = 'GATATATGCATATACTT'
output: All starting positions in Genome where Pattern appears as a substring
       ex: 1 3 9
"""
def PatternMatching(Pattern, Genome):
    # create empty list for result
    positions = []
    # determine index value we can stop checking for pattern
    for i in range(len(Genome)-len(Pattern)+1):
        # if we find the pattern within the genome, append starting position of
        # pattern to positions list
        if Genome[i:i+len(Pattern)] == Pattern:
            positions.append(i)
    result = ' '.join(str(number) for number in positions)
    return result

# Pattern = 'ATAT'
# Genome = 'GATATATGCATATACTT'
#Pattern = 'CTTGATCAT'
#input_file = open("input.txt")
#Genome = input_file.read()
#print(PatternMatching(Pattern, Genome))

"""
Although most bacteria have circular genomes, we have thus far assumed that
genomes were linear, a reasonable simplifying assumption because the length of
the window is much shorter than the length of the genome. This time, because we
are sliding a giant window, we should account for windows that “wrap around” the
end of Genome. To do so, we will define a string ExtendedGenome as Genome+Genome[0:n//2]
"""
def SymbolArray(Genome, symbol):
    array = {}
    n = len(Genome)
    ExtendedGenome = Genome + Genome[0:n//2]
    print(ExtendedGenome)
    for i in range(n):
        array[i] = PatternCount(symbol, ExtendedGenome[i:i+(n//2)])
    return array

# Genome = "GATATATGCATATACTT"
# ExtendedGenome = GATATATGCATATACTTGATATATG
# symbol = "C"
# print(SymbolArray(Genome, symbol))

"""
We observe that when we slide a window one symbol to the right, the number of
occurrences of symbol in the window does not change much, and so regenerating
the entire array from scratch is inefficient

We can view this sliding of the window as simply removing the first symbol from
the window (C) and adding a new symbol to the end (A). Thus, when shifting the
window right by one symbol, the number of occurrences of C in the window decreased
by 1 and increased by 0. Once we compute that array[0] is equal to 8, we automatically
know that array[1] is equal to 7 because the next symbol A does not equal C.

Input:  Strings Text and Pattern
Output: The number of times Pattern appears in Text
"""

def FasterSymbolArray(Genome, symbol):
    array = {}
    n = len(Genome)                                     # n = 8
    ExtendedGenome = Genome + Genome[0:n//2]            # ExtendedGenome = AAAAGGGGAAAA
    array[0] = PatternCount(symbol, Genome[0:n//2])     # {0: 4}
    for i in range(1, n):                               # from 1 up to but not including 8
        array[i] = array[i-1]                           # array[1] = array[0] so array[1] = {0: 4}
        # if previous index matches symbol, subtract one
        if ExtendedGenome[i-1] == symbol:               # if ExtendedGenome[0] == A
            array[i] = array[i]-1                           # array[1] = 4 - 1 = 3 so array[1] = {0: 3}
        # if next index matches symbol, add one
        if ExtendedGenome[i+(n//2)-1] == symbol:        # if ExtendedGenome[4] == A
            array[i] = array[i]+1                           # array[1] = {0: 4}
    return array

# Genome = "AAAAGGGG"
# symbol = "A"
# print(FasterSymbolArray(Genome, symbol))

"""
We will keep track of the difference between the total number of occurrences of G
and the total number of occurrences of C that we have encountered so far in
Genome by using a skew array

Every time we encounter a G, Skew[i] is equal to Skew[i-1]+1
Every time we encounter a C, Skew[i] is equal to Skew[i-1]-1
Otherwise, Skew[i] is equal to Skew[i-1]
"""

def Skew(Genome):
    skew = {}
    n = len(Genome)
    skew[0] = 0
    for i in range(1, n + 1):
        skew[i] = skew[i-1]
        if Genome[i - 1] == 'C':
            skew[i] = skew[i] - 1
        elif Genome[i - 1] == 'G':
            skew[i] = skew[i] + 1
    return skew

# Genome = "GAGCCACCGCGATA"
# print(Skew(Genome))

"""
Minimum Skew Problem:  Find a position in a genome where the skew diagram attains a minimum.
 Input: A DNA string Genome. 
 ex: TAAAGACTGCCGAGAGGCCAACACGAGTGCTAGAACGAGGGGCGTAAACGCGGGTCCGAT
 Output: All integer(s) i minimizing Skew[i] among all values of i (from 0 to len(Genome)).
 ex: 11 24
"""
def MinimumSkew(Genome):
    positions = []
    skew = Skew(Genome)
    n = len(Genome)
    minimum = 0
    for i in range(0, n + 1):
        if skew[i] < minimum:
            minimum = skew[i]
    for i in range(0, n + 1):
        if skew[i] == minimum:
            positions.append(i)
    return positions


# Genome = "CATTCCAGTACTTCGATGATGGCGTGAAGA"
# print(MinimumSkew(Genome))

"""
The discovery of these approximate 9-mers makes sense biologically, since DnaA
can bind not only to “perfect” DnaA boxes but to their slight modifications as well

Hamming distance = the total number of mismatches between the 2 strings

Hamming Distance Problem:  Compute the Hamming distance between two strings.
 Input: Two strings of equal length.
  Output: The Hamming distance between these strings.
"""

def HammingDistance(p, q):
    count = 0
    n = len(p)
    for i in range(0, n):
        if p[i] != q[i]:
            count += 1
    return count

# p = "CTTGAAGTGGACCTCTAGTTCCTCTACAAAGAACAGGTTGACCTGTCGCGAAG"
# q = "ATGCCTTACCTAGATGCAATGACGGACGTATTCCTTTTGCCTCAACGGCTCCT"
# print(HammingDistance(p, q))

""""
Approximate Pattern Matching Problem:  Find all approximate occurrences of a pattern in a string.
    Input: Strings Pattern and Text along with an integer d
    Output: All starting positions where Pattern appears as a substring of Text
    with at most d mismatches
"""

def ApproximatePatternMatching(Pattern, Text, d):
    # create empty list for result
    positions = []
    # determine index value we can stop checking for pattern
    for i in range(0, len(Text)-len(Pattern)+1):
        # if we find the pattern within the genome, append starting position of
        # pattern to positions list
        if HammingDistance(Text[i:i + len(Pattern)], Pattern) <= d:
            positions.append(i)
    positions = sorted(positions)
    output = []
    for position in positions:
        output.append(str(position))
    # print(" ".join(output))
    return positions

# Pattern = "CTCGATTCAC"
# Text = "TCGTATGTGTTTCGTTCGGCTCTTTGACGGGCCGGCGTTGTTTCGACTGCGGGCATTGCTCCGGCTGCGTTGATAGACGGAAGGGACTTACAGGGGACACATCGGAGCGGCCTACAACTTGGAACATAGTGCGGTTTTGGATAGCACCAGGTGAGTTCAGTGGGAGGGGTGGGGTACTTCTCAATATTTTGGGTGCATTGTAGCGTCTTAACAAACGATCGAAGGATTGGGGGGTTATCCTAAGGTCCATCGCACTAAGGAACGAGCAGCTCTTTAACTTAGAAACCAGTTGACGTTGTCGAGAAGGCCTGCCATGCTTGAAAACAGGGGGGTGTCTGGAAAAACTGAGCTACCTCCATCCAGTAACGGATCTGCAGCTATACGAGCAGAAGAGAATCCGGCTGGAATCCCAGTCCCCTAGAGATGCAGTTACTCACTCAGGAGATGTCAAGGCAAGCTGGTTTTATACGCCAATGGTGTCGCTGTAGTACGAGAGGTGTGCTTCTTGGCTTCAGCCACCCTCCAATTCCCTCCAGATAAACGGATCGCCACTTCAAATTGTCACTTACTGGTCCAGTTGACCGGCATGTATTCTAGCATACTTGGAGGAGAGAAGCAATCACCAAGGCACATCTGATCAGCCAGTACGCCGTTAGAGTCCTTAATATCATATAGCTTGGACGCTAGACGTTACGCTAATCCCTCTCACCTTGCTGGGCAGTCTACCTGGCGACTGGAAACGAGGACCCGCCACTCACCGCTCAAATGGTGACTGAAACGGTGGCCAGTCGCAGGTACCCTCTACCCATACTAGCAGCCTAACGGACAACCATTCAAAAATTAGAGACGGGTTAATAGACCAAAGTACTGCGGCACCTAGACCGAATCGCACATAATGTTTGCCCTGTCGATCCCCTGCACTTAACCCATTCTTCCCGCGGGTAGTTTGCGGCTGACTACGCTCGCCGCTAGTTATCTCCCCGGTTGTCCATATTGCGGGGAAGATCCATAGGGCTAGACGCCGCAACTCGTAGGTACTAGAGACTGCAATGCTCGCGCGGTGTCAAGGAGGTTCTTTTTTCGCTCATTGAGCAAGTGGGTGATCGAGATCCAAGTTCGATCCGGGCGCCATTAAGCTTCGGAGCGGGCGAGCTAGCGCTGTCATGGGCGCCAGATGTGGTCTCTGTTCAATCCCAGGTTATGCGATGGTATAACATCTTTTCACCGAGGGGGGTTGCGTCCGGCGTATTGGAATGATGGGGGATTCTAAGGGTATTAGGTGGACAATAACCGGCACGACGCGAACGCCATGTAATAAAAATGGATGACGATCAAGTTAACCCCGGCCAGAGGCGTCAAGTATAGACGAAGACTCATGGCGGTGATCTTTCCAAGTACTCCCAACCTGGCAGTATAAAGACCCCAGTATCGGTATACAACGGCCACGGAACGGCTCTATATATACCTCACTCATTGATGAACCCACAGGACTCTTCCAGTCATGATTCCGACGGCCGCCCGTGCATAGACACGAGCCAAAGCGAGCGATGTTAGCCTGTCGATGCTTCGAACTGATTACGCGCAACCGCCGCGCGGTCTGGATCAGACTTGGCTACCAAGGTAGCTGTTCTCGGTGAACAAGCAAATTGTCAGTGAGTCAACCGCCGATAATTAACGTAAATTCTCCGTTTGCATAGCGCATGGCTCAATCTCCTCTCCACTCTCTGTAGAGGAAACCATGCCCTAATGCGTCCGGGTTAGCTGCTGTGGCCGAATCGGGCTATTGCTAGCCTAACCAGATAAGCACGCTAAACTCGACGTCCCAGGGGGATCACAGTGAGACTCGCGGTCCCATTGTTATGCGCGTAGTGGCGTTTAGGTGTTAATCAAACTTCCAGGGAAGCCGCTATAACAACCCACAGTCACAGCGAATCAATTGAGTTAGGCTCTTGACGACCACAAGACAGGTAGTTATGATTCGCGCGCGGCTCCTGTATCCGTGCAAATGCGAGAAATCAAGATGATCGTTACTGACTGCCGGACCATTGGTACCCCATTCGTCGGTTGAGTGTAGTTCAGGTAAGCGCTGTTGGGGAAAAAACAGTACTCCTGTTGCGAATCCAGGTCTATAGCATCCAGTTTAGACAGAACTAGGGGCCATGTATGCTGGGCAATGGGGCAGTACCGAGGGAGCATAGGAAGAGGCGACTTTGTCCCGCACCAGCGCACAGCATTTATGAACTTTGCAGGCAAGAAGAACACAAACGACACTATCATCTCGTGCTAGGACAAGCGGTACAAATCTGTAAGCGACGCTCTGTCGCATACCCAATGGAAGATCCGGTGGTAGGATAATAGACCGTAGCAAAATGTGAAACAGTGGAACTCCTAACGGCGGAGGCTTAACATACAACCTAGAACGCTGCCCACTCCTGTCGGCTTCTTACATGGGAACAGGGACCTCCTCAACGGCAATGCTTCTCACGGGCGCCCTATACATACAGAGCATTCTCAAAAAGACGTGCTAAGCATGTCGTTGCCCGGCTTATCGCCTATTTATTAAAGCTCTTCACTCACAGGGAAACGGGTTTGCTTGCCCCGCTATAGCGCCTACTGGCCTCCTTCTGCCGTCGCCCGGTGTACACTAGTTCTTGTGGCATCCAGAGTAGGGGTTTGCAGTTATATGCTGCGGCCAGTCTGCGGTCACAGTAAGCCCATAGTCGTGGACAGCCGGAATATTTTCTACCAAAAGTCACTGTCTGAAAAGCTAGCAATAAACTCATTGTGGAGCCTAACTGCCTGCCCCCAGTAAGAGCAGAGGTATTTGTTCTAACAGTTCGAGTAAACTCTTAGTCAGCAAATGATTTGCGTCAAGCGCCCATCATAAGGTTTTAGTGCGAAAGTTTTCCGTGTGACCTTCATATGGAATTTTTGTGAGACCGGGCGGTCGCGAATTGAAGCTCACGGATTCATGTGCTGCGGCACGAGACCCCAGGATCTTGATAACCCTTGTCGCCATTCGAGTTTCCTGTAGTGCGAGGGCATAAAGCTCGCGGAGGCCCAGACGGCGGTCAGATAACTAACGCACCGGATTAGACGAACACCAAAGTACCACGAGCCGCTATCAACGTCGGCTATGTATCCTATTTTACTCTCGCGCGAGGATCTTTTATTAAGCGCAACGCATGGCGCGGTCTGCCAGGCCACTAATCATCAAAGTGACAGCACGGAGCGCTAGTCGATAATACAGCCCACACAGCCAGGGCGCAAAATCGAAGTGAGGACTCGGGTTCGTCACCTGTGTCAACCCATATATGGCTGTTGGCTCTCAACGTACGGTCTTCAAGCGCCGGGACTATAGATCCGTAATGTCTACCTAGTTTCAGTGCAGTTCCGCTGCGTTTACAACTCAGAGGCGGGTCTCCTGGCATTGACTAGCGTAAACGATCAGCTGCAGTTTCCATAGTATTTGTCTCCGCAGTGGAACAAGTAGTTCCCTTAAGACGTACAACAGTCAGCCCCTCGAGATCGCAGCCGGTCGACGGAGACAACTAATGTCCTCAATGTCCTGCGGGGATCCCAGTGCTCCCGTGGTGGGACTCAAGTGGATCCGCGCATACACCCTGTCACACTCTATCGTTTCAAATACGCGCTCGCCTAATTACACGGACCATAACATGTGTGGTATAAGCCGTAAGCAATCATGTGTCCCATGCGAGGGACAGTTTAAGCCACATGATAATCGACGACTCTATCAAAGGAATAGAACACTGATGACATCCTACATGATGACCAAAGGGACTGCACAATGAGCCTATACCAGCCCGACCCCGATCGAAGTACTGGCTAGTCCTCTGCTTGACGATCTGGGCGTTTACGGATCCTAACTTAAATGCCGAGTGTAAAATTTCATAGATGAACGGGTTACTACACCTGCTCATTTTGATAGCTGGTGAGTATCAGGACTCGGAGACGCGTCACCAATTGATATTTCGAGATCCCGTTCGTATAACCGAGGGCGACAACTATGCGCGGGTTGTTAGGGGTTCTGCAATCCGCCGTATCGGTTATCAACTCGGGAGACAGTTCGTTATGCTTGTAAGTTGACGTATTAGACTTCAGCATTTGCACCGTATTGACCACTGTGCTCTTTTCCGTGAGAGACTGCCGAAAACGATCTGGAGCTTTACCCAGTGCCTGGTATTCTAGCCTAAGGTGCTGCTTCGAAACACAGCGTATGACGGGTCTAGTTCCATTGATCCGCAGCCGTCCACCTGTACCATCCTCGGCTCGGCTTTACCGTGCGGTCTTACTGTTTCGGAGCTCATCATAACCTAACTTATCCCTCGAATGACGCGCACTGACATCATATCACAAGGTATCCAGAAATCGGAAACAACCTTGTAACAGCTGACTTCGGTTCCAGCCGACCTTGATCGTAGGACGTGCACCGAAGCGAAGCAACGGTTATAGACCGGACGGTGACGTCACGCGAATACGCACTGACCGCGTTGGGGTACGGATCGCCTGTCCTTTTTAGGGATCCCCGATATTGTCAGGGTGCAGAGGATGAGGTTGCGCTCACCTGTTGACATGTTAGGACTCCTTAAGGCCGCTGGTATATCAACAAGATATGTAGACCCTATTGTCTCCACGCGTCGAAGCCGTTAAATTATTGTGGTCCCGTACGTCCATCTCAAGTAGGGCTGAACGAACGATGTTATGGGTAAGACGCTGGGGTAAAAGTATTGTGCACTGACGTCATATAGGCCGGGCAGTGGCTGCTAGTATGGCATGAATCCTCGCTATTTATGGTCGAAGCCGATGCTAAGGCCACCAATGCTTCCGTGATTATTGGATTTTAGGCGCTTTGTAGTGCCGGCACTAGACTTGGGAAGATGTACATCAAACAATCGCCGTAGATCTTCGGGACATAGCACGTTGCCCTATGTATTCCTTCAGCGTTAAGGGAACCAGACAAAATGCCTACCCATCGACATACATCGTATCGTGACTAACCAAAACGTCGATGTTAAGTCAGACTTGCATTAAACGGCATATGTGCCTCCAAGAAATCTAGAGGCGCATCGACTCGCCATTTGAGGACTCCAGCGCGCGATAGGTGGCCAGCAACGCTAATTGTAGCTCGCCAATGGCGCGAAATGCTGGGGTCCATCTTGTAAATGTGCCACACTGGATAGTACCTAAGGTTTCATAACTCAACCAGGGAAGACCACGGCACCGGCACTCCAAAATCACATATAGGGAGACCTACAATTCTGTGGGCTAATGGTCCTCGTTACTATCAACAGGATACACCGTTATGAGTTCCGCCCGTATCTACGGTGGTCCGGTGTGAACAATCATCCCATCCCGTAGGGTCGGCCAAACGAGTCTCAGACAGGCCCCTGCCGCCGCTGATCTCTGGTCGAGATCTTCTTATCCGATGCAGGTACATAGACCCAACTCTGAACCACGTCGCATTTGTCTTTTGATGTACGGTGATTGGCGGTACACGTATTCACATAAATGATACCGACACTTCTGATACTAGACGCAGCAGGTTTTAACCTGTTCGTCGCTCGTCGAACTTGCAAGCACTTCCCTAAGACGACTCACTATAGCCACCTACGCGTCAATTATGCCCTCCTTCGCGCCTCCGCAATGAGTGTTCTTTTTCGCTCCGAGAAAAGGTCATGATCCAGAGGGGCGGCCCGTCAAGACCCAGCATGGTGGCCCTCGTTGTCGAGACAGGAGTTGGGAATCCCACCCGTATTTCGTTAGGATGATTCCGGCACCTAACTTGAAATCTGACCCATGTGGTACTCATGACCGCCTGCGCCGTATACACACAGCGGGACGTGGATCCAAGGCGTACTGAGATATGCTTAAAGAAGGAATAGTATCGTGGTTGGCATATACGTGATAACTCCAGGGGGCGGCGCAATGATTACGATGACCTAACGTGGTTGGCCATCAATGGTCTGCTAAGATGACCAAGTCGGGAACCTTTTATTTTCTTCGGAAGATCGCAAAGCTTTTTGAACATATACAGTCCATATACCCAAACGACCTCCGGACGGCTTGGAGGTCGAACAGCAGTCCAGATGGAAGTATATGTGAAAAAAGCTCAAAGTTAGCGTTTTGGAACCTGGGTAAGGGCATCTGAGTATGCCTCTGTGCATCTAGCCTGGTTGGGCACAGTGACAGCGAGCTGTACCACGTTCACGGTAGATTGCTCACTCGATTCAGGTGTAATATGGGGCCCCGGCTGCTCCGAAACTTTGACGCGCCCTCGATTGGCAGTCGTTGACGACCGGTGAACTAAATAGTAAATGTACCGATCGACCTAGCTCAAGCTGAGCGGCATTGAGAATCAACTGTCAATCTCCACCGTCAGAGTATTCGCAGGATTACATGACCGTAGCTGGCTTTGCAACGCGCTAGTGTGCCTTTAGCAAGCCTAGTTGTTTTTGGACCGTCGCCCTCGGCATCTGGTGCTCTTGTAGAGACTCGACTCATCACGGACCAAATCCAAAGCTGTATGTACTTTTGGCGAGTGTTCCGCAGCACACGACATCGTAAGGTAATCCCTCACATGGATCGGGCGGAAGTATCACCCACGACCTGCTTCACACTGTGAGTACTGGTACTTCTCTTTGCAGATATAAAGAGTATGACTGACTCAGCTCACGTCTTCAGTAGGATCACGCCAAGACTTGGGTGAGGATATATCACACGATGAACCAATTCACTCAGTCAGGGCGAATTCAGCGAAGGATATAAATATTGGCTATTCTCTACAGCCGCGAATGTGCGCGCGGGCCAGCTGTACTATTCCTGAGGTCCAACAAGATCTACGGTCTCCCGTCCGTCTGGTGAATACCAGACGTGATCGCCGACCACGTTATGTCTGCAAGAATTAAAGACCCTTCTATCATCCTTATCTGTGCACTCATAGACACTGCCCAAGTGCTTATGCGTTGGATCTTTGCAGTCAGTCAATAATCAATTTAAAGGCGGCTGGTGGATAACACGTAGCTTCCCTCCCGATGAGAATGTTCAATACCGTCCGCTTAATTCATGGTATATTGTAGCCCGGTTATTGTCAGACACAGCATGCTAAATCACGACCTTTTCAACGATGACTCACATACCAAACTCTAAAGCTCGGTACCGGGCACCGCAAGAGGGGTGGGTGTCATCAAGACGATCATCAGAGTCATGCACAGGGCAATGCACCATGTCCTTTGCTAAGTCAGTGGCGGGTCATCACATCCTGCGTGCCAATGGCCACAATTTCCCCACGTCTCACTTAGAAATGCCTGTTAGTAGCGGCGTTAGAGCCAGAACCGAACGTAGTTACAGAACCAAAAAATGTGGACGTTAGCATTAATTACCTAATACCGGTGCTTGACGTGTATGATCCTACGTTCCTACACTGGAAAATACTGCGCGTATAGGAGCTTTAATGTAATCGAGGTCACGTCGGACTGGAGCTGTCACTCGAGGCGTCTACAAATTTACTAGAGTAAGTCTACGTCCCCTAGCTCCGATACCAAAAAAAGATGTCGTGACACCAGCCACGGGAGGAGGCGTGGTAGTACACTTGAAGTAGGTATACGCCCGCAACGCCTCAGAGGAAGGTAGCCAATGACACGAATGAAGGTGCTGGGACTGTAAACGTGTCGAGAGCCATCATAGTTTCTTTTGATATACACGGGGTGGCCGGGTGATTAATCTTGGATTAACCAGTTAACGTATCCGAAACCGATCTGGTGGGTCCTATTCTAAGACTGGCCCTAACCTTACAGCTACTCCAGGATCCAGGCGGTTCGAAGTAAGTCCAAACTCGTTATAGTCTGTTTGCCGAGACTTCGCCTCAGAGAGGCCATTGATTGAAATGTTACACCCTGACATAAACATGCATCCACGGAATAGGGGCGCAGTTCGTCAAGCCCCGGATCCGCGACGAGACCGGCAGTCCAGTATCGTCACCCTAGGATAATCCCGACGGGAACGGGAAGGCCGAACTAAGACTGGAGGATCCTTGACGGATTCAACTGCTGTCGAATGAGCTTTCGGATGCCAATTGCTACCCCAGCCAGGACCCATTTATGAAGGGGCGTAGCGAGACGCGATGGGTGTGGTATCATTTTCTGAATGGTAAGCATGACGGCCGCACAAGTAATCGCGCGTGTTCTGGTCTAACGGCGCTCGTCAATTCTTCTCCTCTCGTGAGGGTATTTTATCAATCCATCAACACATGCACCATTCTTGGACGCGTCACGTGGGCTTTAAATCCAACGTCCGCGAACCACCTCCTGTACCGAAGGATAACTCTCCAATAAAGTGCTTCGCTAGGTTCCGTCCAGTTAGCTTTACGGAGATTATTAATTTCGGAGTGGTATCCACCAGGCGCTTGTACGTCTCCACTCAAGCTCTCAGGTGCGAACCTGAGACGTAGTTTAGATAGCGGACCTATTATTCATCGGGTGGGTATCACTAATTCGCGGTTCCTGTTGATCTCCTAACCGTTTTGAATATTCAAGCCCACTATAGGCTAGCGTACGATGTCAGGCAATAGCAGGCTAGGAAAGTTCTCATCAGTGTTTACTAGGAGACATACTTGCTTTATTACCTGGCTAACGAATCTGCCGGTCAGACGTACAACTCCACATGTGCAATCTACACCAGTATTGATACTTTCCGCGCCCGTCCATGCGGGCCCCAGTAACTCATCGGGAATCATCTTAGTAATGTGCCGATTATCCCGAAACGGAGGTGGTTTGGTATGAGGTTGCACCGTTGCAGCGAGTCGAATCTCTAAGGTTAGGCAAAAGCGTGGTCTGTCAATAGTCAGTTACATAAGCGCGACTCCCATGTGTCGGTGGAACCCTGGCAACTTTATCTACGAAACCCGCTTCCGACTGGTCACAGGTTTGTGTTACTGCATTGGGGAACCACCAGCCAGGCTATCCCATCGAACCTGATAACTTCTACTGCCGAACATGGTTTATGGTTCTAGAGGCGAGGACGTACAGCCGTAGAAAATGAAGCAGGCCTACTTCGGCCCTATATAACACCCGAGTCGGATAGCTTCACAGCGACTGCCGTCGCAACATTCGCGAGCCGCGTGTATAGTGACAATACCAGCATAAGTCGGCTATCCACTTTTCTACAGTTGCGAAGGCTAGGTCCCCTAGCATTTCTAAGATCAACATATCGGGTGAGGGATACTACGACTTAGGGTGTCGTGTCGCAGAATGCCTCTAGATGGATGTTGCGATTCGACAAATCCCACAGGGTCGGCATAAGACATTATGTCACAATTCGCCGACCGCAACCGTGTAACTTACTGGGGTTCTGCTGCAACTCGTTTCTACGAGTGTATCGAGTCTGCACGATCTCGTCTATGCTGATCTGAATGTGCGGTGACAACCGACTCGTGGTTGTTCAGAGGGGAGCGCCCCAAATCTAGGATTGCACCTGATGTGACTGTAGTTTGCGGCTATGGCCACATTTGGTTGGGCTCCGCGAGGTGTTCAGTACCGGCACTCGGCTCGGGGCTAGGAGGCGTGTCTGGGGGGGCGGATCTTTCTGTTTTGCCCTGAACACAGAGAGAGCGGAATAGTGATAGTCCGTGCGAATTGCATGGGGGGCAATTCAAGTGTAAAACGATCTTCGGCACTTAGCCGTGGGATTGAAAGGTTGACGTGTCTTGGGGCACTTGCCAACTATGGCGCTTTGTTACTGTGGACTGTTTGAGAGACTAGAGGGTTCGATACGTATCTCGGCGTTTTAACGCTGAGCAGCAGTATTGACTTCCCGACAGGGACCTATTCGTGATACAGGGCGGGCTTTATTAAATAGCACCCTTTTCTGTACGGTCTAAACGGTTCCTGACAGCCTACCCACTACTTTATGAAGCCCACCCTAGCTATACAGGCTGTATTACGGAGTGAAGATTTTCCCTAAGGATCAGTTCAGCTAACTCAGCTCCCCGGGGGCGGATCTGTTCTGCTCTGGATTCCTGTTAATTTTGGGCTACACCACCATACGATATGTGGAAGAGATTACACAAGTCAGGACGTAGAGGTTAAATTATGAAAACCTCATAGGACATGAGCTACCAGCGGACCCGTAGGGCAGGACAATACCTACAGTAGCGCAGGTAACTAGGGTTCAAGCATAATCGGGATATTAACCCAGTAAACAGGTTTTTAACCCATGTTATATCCAGCTTATAATACCGGTCACGTCTAGTGCCGCCGAGAATAAAGCCAACAACATGATGTCCTCACTAATATTACTTGATGCGGCGCGGGAGAGTCTCGCACCTAATCGACCGGGTCTTTAGCAAGATTGAAAGATAAGAAAGCCCACACTGAATGCCGCAAGCAACTCGTTTGCCGGTTTAGGCAGTTTATCAAACGGGGTAGCCTTATGTGGCCCCTCGACGGACACGGGAAAGTGAGCATTGCTAAACATACTCGGGCCGCTTATATAACTGCTTCAGTGTAGGTAGATTCCAACATGTTTTCTACCCGCCCACAATTCAATTGCCATAAATGCGCACAAAACCTAGAGAGCCGACTCGGTGCCAGCGCGAACTGCGTTTCGCGACTACGCGATCGGAATGCGCAATCACCGCCGTAGACGGCCTTCCCCTCCTTTCCAAGCAGGGTCACATGCTCGCACGAGTCATACTTTTCGCGACTCTTGCCAACTAGGTGTAAATGCAATACTTACGGCTAGTCGAACCTAAGTACACAAACAATTTTCGCCAGCCGCTGGCCTGCTTCGCCAACTGCTGCGAGACAGCTTTCCAGGGAGCTCAAATGCATAGTCCTACAAGGAGTCCCATAACAGTATAGCAGTCAGCACTCCCCGTCCGAAGAACTCATCCAATTTGCAGACGAGCGCGAAATATACGGGCCATGATTCCTGTGGGAGCTGGATCGAAGCGTTGAAGTCCTGGGCTTAACCTATAGCGTCTGCGTCCCCAGGTGGGCCGCTTGAAGATTGTGTACACCTTCCAGACGACGACGTTAAGGTGGTCTTTTTCCACCACAATGAGTTGGAATGCATAGGTACCAAGCTACTAAGAAGTCGGATCACGCTGTCCTATACCATTCACTGGTTAAAGTTAGGCTAGTTTGTGAACGACTCAGATCTCCGAGGAAGTGCCACACGCGTGCCAATTCTTTAATCTTGAGTAAGATCTAATTTCGAGACAAGGGAGGTCCCGGATTCTCTTCTGAGAAGTATATTGTACTAGCTTAGTACCGCGCATGACCCAGATAGGAAGGCAACGCAGGATACCCGTGACCGAGATGTCTGTATAGAGAACGGGTCCAACGTGGTATGACAATGTCTCTGGGGATAGTGATAATCGGCGTATCCTCTGCAGCGCCGTGACCCCCGTCACTTTAGGAATCGTCTTGCAATTTCTACTTCACGCGGGTTTTGCCAGAGCAAAAGGAACGAATATATTGAGCTTCCATAATATCATTCTAACTGTATGCTAGCTCGTCCTGGATAGGAAACGAGAGTTAACCTAATTTTGCGCGTCCAGGTCATCTTAAGCGTTCCTGCTAGACGAAGATGGAATGTCGTAAGCGAGTGGCGTCGCAGCGACGAGGTTGCAACTAGGAGGGTAATGTGGGGAATACAAAGGAATCGACCTCTAGCTCGTTCTAGGGCCACTCACTACTGGAGGGGGCAATTAGGGCATCTCCAATTGTGCTATCGGAGAGGGGCATGTAGAAAGGAGTAAGTGGCCAGCGCAGATACGATGGTACCACTCGACAGTTCATCTAATATGCGGTAGACACGCTACATAAAATGTGGTCCGCTTCGCTAATCGCACCCCAAACGGATCGAGCAGCCCCGTAAGAGGTGAGTACAGGTCACATGAATAGATCGTAGACTCTATCGATTGTACCTTATTGCCTAGTACCCGCTTCCTAGAGGTTCGTGCCAAAATCTTGCGTACTGAGAACCGTGGTCTCATGTAAGTCTTACTTCCGATCAGTAGTTGCGTCCTGCCTTCACTAAAAACGGTATTCGTCAAGTAGCGTACAGCGTGCTGGTGAAAGTGACAGGTTCCATAACCGTCGAGATTCTTTTGCAGAAGTACCGGTTTTAATGGTGGCATGGAAACTTCTCATGTGGAGTTCAACTACATATTATCCCAGAGCTTACTCCAACGACATATCGCCTATCGGCTGGGTTGCATGCTAAGCACGCAGCTACTCATTGAAACCTCCATTCAGTTCGCAGGGTGATGGGATCTAGTACAGGCGTCCTACGCTGTGCTACCCTGTACTCTGCGTAGAACTCCAGACCCAGCTCGCCAGTTGTCCCGAGAAATTAGTCCCAGTAGGACTTACCCCTTGATAACTAGTGTTACGGTTGCGAGAGGTCAATTACACTTTGCAACTGAGCTTACGACGTATCCCACTATCTGTATGCCTCGGCAATCCTAGTGTTCGACCACTCTGCAAAAAACTTGCAAACACGAGCTCTGTGTGGGGCGACAAAATGATCAAAAGCAGTTCCTATTTTGTAGGCTGCATCAATATCTAAATAATCTGACCGCTGATAACTATGTAAGTTAATAGTCCACTATCGTTATCTCCTCCTCAGAATCGCAAGACCGCCCGCGCTGCGTCTGAAGAACGTTCGGCTACAACGCATGCTCTCAACTACTCTGTATGCCTCTTTCTTAGATCTGAGCGGCGTCGGGCACCCGGGTCAAGACTATACAACGCCGCAGCTCCCGTTACAATCTTCTTATTACCAGTGTAGGGTAGGGAACGCCGATGCATAACGCAAGGCTGTGCGTCGTGAGCTCCATCCAAGTTTGAGCACTCGAACCCGCGTGGATGCCGTCCCTTAGGCCGTATGTCTCAACAAGATGATTTTCGACAGAACTTGTGATGATGCAAACCAAATGTAAGCCGACACCGATAAAGTACAGTTTGAGGTGCTGTGTTGATGCCATCGTGTCTTTCCGCCCATCGTCACAAAAGGCGTTAAGTGGCCCCGTTAGTGGGGAGCCACCTGCATGTATGACTTCTCTTGAGGGGTATCTTCCTCTTCTAAGGGGAGCTCTATGTCCCCGGGATGTGCACCCAACCAGGCAATCACGTTTCACTCCTCTTCCAAGGCTTAGCCTGAGTACCACATGTTCTTCTCTACAACACCATCTGGCCGCAGATGTGATCATAGTTAGGAAGCCAAAAATGCGCCTATCGTGGTATGGCTCAGTTATGCGTACGCAATGTCCACGAATGCTAGAGGGTTCAGATCTTTTTGGAGCTGTGTGATTGTGAGCAATAGCTCGCTCTGTGTGCCCCTCCACGGATGGCCCCTGCATCGCCATACCTTTTTTTATGTTCACAACATCCCACTTGAAGGCTCAAAAGGCTTAAAACACATGGAATACGTAGATTGTTCCAGGGCGCGCGTTGTAAGCCTCACAGAGTTACATAACAGAGGTCGGGTCAGCCGGGAAGTTAGAGGGAGGAGATCCGCCGAAAAACCGATATCCCCAGAGGAGCCCCTCGGAGGCCTCGTATTTGGTCGGATATTAGGGCTGTGTGGTTATAAACGGCAAGCGGAGGTGATTCGCGACCAACAGCATAAGACACCGATGCTGAAGACCACAACGCCCTTTAGATTTATTATGCGCCGTCCAGGCGTGTTTCGGAAGCTATGCTCCCCTAACAACGCCTCTTACTCTGTTAAACACCAGGGTTAGTGTGCGTGAAAGGTCGCGGCCGACGCCCCGCTAAGTTTGAGATCCGCAGATACAGCTCAGTCAGACTAAGCGATTGCAAATGTCTGGCTACTGCTCTCCCACTTGTATTCTACCCCAGCTGACGTGGGGTTCATATTACACATAGGGTCTATAGACCACTCTATGGTGTTGTTCCAAGGAAAGATTCAGAAGTGCGCTAAGGAACTGGAGACGTTAACCTTCTTTGCTCAGCTAAGCTATTTATTCGCCGATGTGACGTACTCGTGTCCAGCCTTCGCTTCCCAAATCTACCTCTCCAGGGAAACCTACAATTACGGTCACCAGCCGTCTCTCGCGCACTCCCGTCCCAACACTAGAGAACCGGTCCTAGGCGTGTTTTTCCACCGCGGACTTTCGCCGCGTAGACATTTGTTTGGCGCCTCCAACCTCTCCCGTCAGACTACTTGAGAATACATGGGAAGAGGACCTGTCGGACTTCGCGCGCCGGTTGAACCAGCCTACCACTATATTTCATCAACACCCGAGGATGGCTAAAAAGCAGCCCATGAACAAAGCCCGGTCGTAACGGATAGAAGTATCGCACATTGACCCGTCAGTGGATGTCGTTGTCTCGAATATCATATTTGGCAAAGAGTTTAATTTTATGGACATTGCAACGCGTATCGTTACTGGAAGGGACTGGGGAATCAATAGGCTGTCCTAACTACATAAATACACAGGTAGTAGTGAATACCAAGTCTATTCGGTTCGCATTTGATCCGCCCGAACGAGACAATGGGCGATGCGCGGGAATATCTATATAAACCTTTAGGTGAGGCATCAGTAGATATCGCCCTTGCACCACTTTATCTGCCCCTGATTATTGGGGCGTAAGGTTGGCAAACTCTGGCTCCCACAGTCTGCCGAAGATCCAGATTATTTTTTGTCATGACAGATCTGTGATTTCCCCTAAGGTCAACATCGTTGCGAACAGTATTTCCCTCGGACGATGATAAGGGCAGTGAGCAGAACAATTAACGTAGAAGTTATGCACGGAGTCCAGATTCATATTCATCTCTGCTTAATCTGCCAGCGAGTTACTGTAAAGCCGTTGAACGTGCAGCCTGCGGTTCCACGCTCCCTCCACGGCAGTATATGGGCTAATATGACTTAGGATAGCCAGTCTTCCTACCCCAGTTTTCCTTCGAAGCTTGCCGGACGATCATCCCAGCAGCAGGATAAATATAACGCCAACCAAAGTGGGGACAGTCTAAGATTATGCACGCTAGCGGAGCTCTCCCAGAAAAATGGGAGGATATTGCAGTGTTACTTGCTTCCTTCACAACCTCTATGGAAATGCCATAGATCCCTACTCGGCTTTCTTCGGTTTTTGATGCCATACAAGGGCTTGGATACTACGGGAGTTGCCCGGATCCGCTTGCTACATCCCGCAACACTAGCGACCTAACTCCTGGGCTCCCTCACTTTTATTAACACCCAATGTGGTGGCCAGTCTGGCGCAACGTAGCGGAGGAGGAAGCAGTCTTTGGTCGATGCGGACTCCTGGGGGACTCCTAGGTAATAATTGGACTGGTAAATGTCTGGTGGGTTACCTCGGGCACGATGGCCTGCTAGCTAGGGGGCATTGCTACAGCTGCCCGGGCTACACGATGTGAAAGAGCTAACACGCAAGAATTTTCACTGGGGATATACTAGAATGAGCACTCAGCTTCTGCTTGTTTTGGTGGTCTACACTATGACAGCCCCGACGTACGGCGCTGACGCATGTTTCACGCTTAAACGTGCCCACTGAATGGGGCCGATATCGGGGCCCGTGAGAAAAGCATGAAAAACAGTCAACGTATGTAGCAGGGCTGCTAGCCGTTGATAGTCCGTATGAAATGCACGACGTTGCCGGGTCTGCCGCACATGGAGAGACTATGGGAAATGGACAGCAATCGATCGGGGCTTTAAAAAATCTACAGTACCGGCGAATAAATATGTGATATCGCGAATAGGGGAATGGAATTGTGGGTGTCCGTGGACCGGCCTAACCAACTTACTTGTACCAAGGCAGAGACCGATCAAAGGGAAAACCCTACGACAGACCTACACCCGTGATTGCGCGCAATGTGCAGATAAGGCTGCTACCCAGGTTGAAGGTATCATGCGACGACCGATTGGACACTGTACTCACTTTAGGGACATGCCTGGCAGACAATACAGAAGGACGAGGTGTCGCAACGGTCCCTTGTAGTTCCTAACTCGATTCAC"
# d = 5
# ApproximatePatternMatching(Pattern, Text, d)


def ApproximatePatternCount(Pattern, Text, d):
    count = len(ApproximatePatternMatching(Pattern, Text, d))
    return count

# Pattern = "AA"
# Text = "TACGCATTACAAAGCACA"
# d = 1
# print(ApproximatePatternCount(Pattern, Text, d))

def ApproximatePatternMatching(Pattern, Text, d):
    # create empty list for result
    positions = []
    # determine index value we can stop checking for pattern
    for i in range(0, len(Text)-len(Pattern)+1):
        # if we find the pattern within the genome, append starting position of
        # pattern to positions list
        if HammingDistance(Text[i:i + len(Pattern)], Pattern) <= d:
            positions.append(i)
    positions = sorted(positions)
    output = []
    for position in positions:
        output.append(str(position))
    # print(" ".join(output))
    return positions

"""
Our goal is to generate the d-neighborhood Neighbors(Pattern, d), the set of all
k-mers whose Hamming distance from Pattern does not exceed d.
"""
def Neighbors(Pattern, d):
    if d == 0:
        return [Pattern]
    if len(Pattern) == 1:
        return set(['A', 'C', 'T', 'G'])
    neighborhood = set()
    all_neighbors = Neighbors(Pattern[1:], d)
    for string in all_neighbors:
        if HammingDistance(Pattern[1:], string) < d:
            for char in ['A', 'C', 'T', 'G']:
                neighborhood.add(char + string)
        else:
            neighborhood.add(Pattern[0] + string)
    return sorted(list(neighborhood))

# Pattern = "ACGT"
# d = 3
# print(len(neighbors(pattern, d)))

"""
Frequent Words with Mismatches Problem: Find the most frequent k-mers with mismatches in a string.
     Input: A string Text as well as integers k and d. (You may assume k ≤ 12 and d ≤ 3.)
     Output: All most frequent k-mers with up to d mismatches in Text.
"""
def FrequentWordsWithMismatches(Text, k, d):
    most_freq_kmers = []
    counts = {}
    for i in range(0, len(Text) - k + 1):
        neighborhood = Neighbors(Text[i: i + k], d)
        for kmer in neighborhood:
            if kmer not in counts:
                counts[kmer] = 1
            else:
                counts[kmer] += 1
    best_count = 0
    for kmer in counts:
        if counts[kmer] > best_count:
            most_freq_kmers = [kmer]
            best_count = counts[kmer]
        elif counts[kmer] == best_count:
            most_freq_kmers.append(kmer)
    print(" ".join(most_freq_kmers))
    return most_freq_kmers

# Text = "CACGCACGTGTGAGTGTGTCAGAAGATGTGTCGAGTGTGAGGAGGAGGTCTGTTGTGAGAGACACGAGATGTGAGAGAGAGGAGTGTGTCAGACACGGAGGAGCACGAGATGTCACGGAGAGAGAGGAGAGAGAGGTCTGTGTCGTCCACGAGATGTGAGAGATGTCACGAGAAGACACGCACGTGTCACGTGTGAGGTCGAGCACGTGTCACGTGTGTCGTCCACGGAGGTCAGATGTGAGTGTGTCAGAAGAGAGTGTTGTGTCCACGAGAAGAGTCTGTGAGCACGCACGGTCTGTGAGGAGAGAGAGGTCGAGTGTAGACACGGAGGAGGTCGAGAGAGTCAGAGTCCACGAGAAGAAGAAGAGAGAGATGTCACGAGA"
# k = 7
# d = 3
# FrequentWordsWithMismatches(Text, k, d)
