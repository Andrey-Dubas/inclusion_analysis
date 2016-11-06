# inclusion analyzer

## overview

a program analyzes your project and warns you about cyclic includes:

a basic usecase of usage:

### inclusion_analysis/inclusion_analizer.py -f main.cpp -d ./

where main.cpp is a file to analyze (you probably want it to be c/cpp file, but you might as well put there a header), ./ is a directory where resize all your project's headers

in case any cyclic includes detected, you'll see print like:

path: main.cpp -> cycle.h
cycle: cycle2.h -> cycle1.h -> cycle.h

where path is a path from root file (the one you put as parameter) to a start of cycle
      cycle is a list of files that form a cycle
