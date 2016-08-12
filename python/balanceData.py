import sys
import os
import argparse

'''
Duplicates the class that is being overweighted. Short term fix to unbalanced datasets.
'''
def balance(args):
    with open(args.csv) as csvFile:
        headers = csvFile.readline()
        headerNdx = headers.split(',').index(args.label)

        print str.rstrip(headers)
        for line in csvFile:
            columns = line.split(args.d)

            if (columns[headerNdx] == args.u):
                for ndx in range(int(args.w)):
                    print str.rstrip(line)
            else:
                print str.rstrip(line)


def validateArgs(args):
    if not os.path.isfile(args.csv):
        print 'Invalid CSV file provided. Exiting.'
        sys.exit(-1)

def main(argv):
      parser = argparse.ArgumentParser()
  
      parser.add_argument('csv', help='CSV to balance')
      parser.add_argument('--label', required=True, help='Label for column being used as truth value.')
      parser.add_argument('-d', default=',', help='Demilimeter for csv. Defaults to \',\'.')   
      parser.add_argument('-u', default='1', help='The value of the unbalanced class. Defaults to 1.')
      parser.add_argument('-w', default='14', help='Number of times to multiply the unbalanced class.') # In my case I have 1 to 14 positive to negative samples
  
      args = parser.parse_args()
      validateArgs(args)

      balance(args)
  
if __name__ == '__main__':
    main(sys.argv)