def mean(values):
    """Compute the mean of a sequence of numbers."""
    return sum(values)/len(values)

def median(values):
    """Compute the median of a sequence of numbers."""
    return sorted(values)[len(values)//2]
