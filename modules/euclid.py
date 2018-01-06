def bjorklund(pulses, steps, rotation=0):
    steps = int(steps)
    pulses = int(pulses)
    if pulses > steps:
        raise ValueError  # pulses has to be less than steps!

    pattern = []    
    counts = []
    remainders = []
    divisor = steps - pulses
    remainders.append(pulses)
    level = 0
    while True:
        counts.append(divisor / remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level = level + 1
        if remainders[level] <= 1:
            break
    counts.append(divisor)
    
    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)         
        else:
            for i in range(0, int(counts[level])):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)
    
    build(level)
    # i = pattern.index(1)
    # pattern = pattern[i:] + pattern[0:i]
    

    def rotate(l, n):
        return l[n:] + l[:n]

    return rotate(pattern[::-1], rotation)