codon = 'UAG'

if codon == 'AUG':
    print('This codon is the start codon.')
else:
    if codon == 'UAA' or codon == 'UAG' or codon == 'UGA':
        print('This codon is a stop codon.')
    else:
        print('This codon is not the start or the stop codon.')
