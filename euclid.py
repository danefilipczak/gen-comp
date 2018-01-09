import music21 as m21
import random
from copy import deepcopy



def bjorklund(pulses, steps, rotation=0):
    '''
            returns a list of binary values representing the attacks in a euclidean sequence, e.g. [1, 0, 1, 0, 1, 0, 0]
            arguments:
                pulses - the number of attacks to be spaced evenly 
                steps - the number of units over which the pulses will be evenly spread. has to be greater than pulses
                rotation - optionally rotate the rhythmic necklace

            note that these arguments mirror and were inspired by the notation for generating euclidean sequences in tidalcyles
    '''
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

    def rotate(l, n):
            return l[n:] + l[:n]
    build(level)
    # i = pattern.index(1)
    # pattern = pattern[i:] + pattern[0:i]
    

    

    return rotate(pattern[::-1], rotation)

def euclidize(stream, length, pulses, steps, rotation=0):
    '''
        Given an input stream, slice it along a specified bjorklund sequence,
        args:
        length - the total length of the bjorklund sequence in quarterlengths, useful for incomplete measures
        pulses, steps, rotation - bjorklund parameters (see above)
    '''
    euclidBinary = bjorklund(pulses, steps, rotation)
    #convert the binary into a list of quarter lengths
    euclidQuarterLengths = []
    for i in range(0, len(euclidBinary)):
        if euclidBinary[i] == 1:
            euclidQuarterLengths.append((length/steps)*i)

    return stream.sliceAtOffsets(euclidQuarterLengths, addTies=False, inPlace=True)

def makeRandomEuclidean(score_, measureLength):
    '''
        Given a score with parts, randomly chop it up into euclidean sequences based on either sixteenth notes or eighth note triplets
    '''
    score = deepcopy(score_)
    for p in score.parts:
        for m in p.recurse(streamsOnly=True):
            euclidize(m, measureLength, random.randint(5, 10), random.choice([16, 12]))

    return score


if __name__ == '__main__':
    ''' some test functions '''
    # print a bjorklund sequence
    print(bjorklund(5, 9, 1))

    s = m21.stream.Stream()
    n = m21.note.Note()
    n.duration.type = 'whole'
    s.append(n)
    #euclidize(s, 8, 12, 1).show()

    b = m21.corpus.parse('palestrina/Agnus_01.krn')
    euclid = makeRandomEuclidean(b, 8)
    b.show()
    euclid.show()

