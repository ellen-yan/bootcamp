import os

if os.path.isfile('mastery.txt'):
    print('Sorry, file exists.')
else:
    with open('mastery.txt', 'w') as f:
        f.write('This is my file.\n')
        f.write('There are many like it, but this one is mine.\n')
        f.write('I must master my file like I must master my life.\n')

with open('gimme_phi.txt', 'w') as f:
    f.write('The golden ratio is ')
    f.write('{phi:.8f}'.format(phi=1.61803398875))

# Multiple files can be open in the with block
with open('data/1OLG.pdb', 'r') as f, open('atoms_chain_A.txt', 'w') as f_out:
    # Put the ATOM lines from chain A in new file
    for line in f:
        if len(line) > 21 and line[:4] == 'ATOM' and line[21] == 'A':
            f_out.write(line)
# Context management: file automatically closes even if there's an error
# when we exit
with open('data/1OLG.pdb', 'r') as f:
    for i, line in enumerate(f):
        print(line.rstrip())
        if i >= 10:
            break

    print('In the with block, is the file closed?', f.closed)

print('Out of the with block, is the file closed?', f.closed)
