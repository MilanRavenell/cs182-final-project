from graphics import *
import os
import time

def print_grid(taxiloc, destination, hasPassenger):
    """
    Print the grid of boxes.
    """
    pos = [' '] * 27
    hash_function = {}
    hash_function[(0,0)] = 0
    hash_function[(1,0)] = 1
    hash_function[(2,0)] = 2
    hash_function[(0,1)] = 3
    hash_function[(1,1)] = 4
    hash_function[(2,1)] = 5
    hash_function[(0,2)] = 6
    hash_function[(1,2)] = 7
    hash_function[(2,2)] = 8

    if taxiloc:
        pos[hash_function[taxiloc]] = 'T'
    if destination:
        pos[hash_function[destination] + 9] = 'D'
    if hasPassenger:
        pos[hash_function[taxiloc] + 18] = 'P'

    print "___________________"
    print "|%s %s %s|%s %s %s|%s %s %s|" % (pos[6], pos[15], pos[24], pos[7], pos[16], pos[25], pos[8], pos[17], pos[26])
    print "___________________"
    print "|%s %s %s|%s %s %s|%s %s %s|" % (pos[3], pos[12], pos[21], pos[4], pos[13], pos[22], pos[5], pos[14], pos[23])
    print "___________________"
    print "|%s %s %s|%s %s %s|%s %s %s|" % (pos[0], pos[9], pos[18], pos[1], pos[10], pos[19], pos[2], pos[11], pos[20])
    print "___________________"

print_grid((1,2), (2,2), True)
time.sleep(1.5)
os.system('clear')
