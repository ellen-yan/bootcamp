def seq_concat(a, b, **kwargs):
    # can have arbitrary keyword arguments:
    # python automatically converts keyworded arguments into a dictionary
    # Alternatively, if you don't want keyworded arguments (e.g. a list).
    # just use a single star; conventionally: *args
    """ Concatenate sequences."""
    seq = a + b

    for key in kwargs:
        seq += kwargs[key]

    return seq
