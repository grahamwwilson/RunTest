# runTestArgs.py
from argparse import ArgumentParser

# See https://stackoverflow.com/questions/26785952/python-argparse-as-a-function

def getArgs(argv=None):
# Set command line configurable parameters. Do python3 program.py -h to see this in action.
    parser = ArgumentParser(description="Calculate Wald-Wolfowitz Run Test p-value")
    parser.add_argument("-f", "--file", type=str, default="TestData/Residuals.dat", help="Input file")
    parser.add_argument("-i", "--info", type=int, default=0, help="Verbosity level (0, 1, 2)")   
         
    args=parser.parse_args(argv)
    print('(runTestArgs.getArgs     ) Found argument list: ',args)
    
    return args
    
def showArgs(filename, infolevel):
# Check these are what we want
    print('(runTestArgs.ShowArgs    ) Program has set')
    print('file:   ',filename)
    print('info:   ',infolevel)
    return
        
def getArguments(argv=None):
# Do 2 things at once.
# i)   set defaults and parse them using getArgs above
# ii)  set values for our program

    args = getArgs(argv)

    print('(runTestArgs.getArguments) Assigning arguments to program variables')
    
    filename  = args.file
    infolevel = args.info
   
    return filename, infolevel
