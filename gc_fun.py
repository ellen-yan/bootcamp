# Try block
try:
    import gc_content
    have_gc = True
except ImportError as e:
    have_gc = False
finally:
    # Do whatever is necessary like closing files
    pass

seq = "ACGTAGCTACGTTACTATCAGCCTCAGTCAGCATG"

if have_gc:
    print(gc_content.gc(seq))
else:
    print(seq.count('G') + seq.count('C'))
