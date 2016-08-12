import sys
import os
import argparse
from random import randint
import numpy as np
from numpy import genfromtxt
import h5py

NUM_CLASSES = 2

def splitCsv(args):
    numItems = 0
    with open(args.csv, 'r') as csvFile:
        for line in csvFile:
            numItems += 1
    testValues = randomSplit(args.s.split('/'), numItems)

    csvFile = open(args.csv, 'r')
    headers = map(str.strip, getHeaders(args, csvFile))
    labelNdx = headers.index(args.label)
    classes = {}

    # Input values for training
    trainin = open(args.name + 'trainin.csv', 'w')
    trainout = open(args.name + 'trainout.csv', 'w')

    # Files for testing model accuracy
    testin = open(args.name + 'testin.csv', 'w')
    testout = open(args.name + 'testout.csv', 'w')

    ndx = 0
    for line in csvFile:
        if (not line.strip()):
            continue

        columes = map(str.strip, line.split(args.d))

        columeNdx = 0
        inputLine = ''
        outputLine = ''
        for colume in columes:
            if (columeNdx != labelNdx):
                inputLine += colume + ','
            else:
                if (isInt(headers[columeNdx])):
                    outputLine += str(colume)
                else:
                    if colume in classes:
                        outputLine += str(classes[colume])
                    else:
                        classes[colume] = len(classes)
                        outputLine += str(classes[colume])
                
            columeNdx += 1

        inputLine = inputLine[:-1] #remove last ,

        if (ndx in testValues):
            testin.write(inputLine + '\n')
            testout.write(outputLine + '\n')
        else:
            trainin.write(inputLine + '\n')
            trainout.write(outputLine + '\n')

        ndx += 1

    print 'Generated csv files from ' + str(ndx) + ' items.'
    print 'Classes: '+ str(classes)

    trainin.close()
    trainout.close()
    testin.close()
    testout.close()
    csvFile.close()

    return len(headers)

def genHdf5(args, numFeatures):
    trainFeatures = genfromtxt(args.name + 'trainin.csv', delimiter=args.d)
    trainOutput = genfromtxt(args.name + 'trainout.csv', delimiter=args.d)

    testFeatures = genfromtxt(args.name + 'testin.csv', delimiter=args.d)
    testOutput = genfromtxt(args.name + 'testout.csv', delimiter=args.d)

    trainTargets = np.zeros((len(trainOutput), NUM_CLASSES))
    testTargets = np.zeros((len(testOutput), NUM_CLASSES))

    for count, target in enumerate(trainOutput):
        trainTargets[count][target]=1

    for count, target in enumerate(testOutput):
        testTargets[count][target]=1

    trainData = {}
    testData = {}

    trainData['input'] = np.reshape(trainFeatures, (len(trainOutput),1,1,numFeatures-1))
    trainData['output'] = trainTargets

    testData['input'] = np.reshape(testFeatures, (len(testOutput),1,1,numFeatures-1))
    testData['output'] = testTargets

    with h5py.File('train.hdf5', 'w') as f:
        f['data'] = trainData['input'].astype(np.float32)
        f['label'] = trainData['output'].astype(np.float32)

    with h5py.File('test.hdf5', 'w') as f:
        f['data'] = testData['input'].astype(np.float32)
        f['label'] = testData['output'].astype(np.float32)

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def randomSplit(splitRatio, numValues):
    trainPercent = splitRatio[0]
    testPercent = splitRatio[1]
    print 'Performing random ' + str(trainPercent) + '/' + str(testPercent) + ' split of data.'

    numTestValues = int(float(testPercent)/100 * numValues)
    testValues = set()

    while(len(testValues) < numTestValues):
        testValues.add(randint(0, numValues))

    return testValues

def getHeaders(args, csvFile):
    if (args.header == ''):
        return csvFile.readline().split(args.d)
    else:
        headersFile = open(args.header, 'r')
        headers = headersFile.readline().rstrip('\r\n').split(args.d)
        headersFile.close()
        return headers

def validateArgs(args):
    if not os.path.isfile(args.csv):
        print 'Invalid CSV file provided. Exiting.'
        sys.exit(-1)
    if (args.header != ''):
        if not os.path.isfile(args.header):
            print 'Invalid header file provided. Exiting.'
            sys.exit(-1) 
    if ((int(args.s.split('/')[0]) + int(args.s.split('/')[1])) != 100):
        print 'Invalid split value. Exiting.'
        sys.exit(-1)

def main(argv):
      parser = argparse.ArgumentParser()
  
      parser.add_argument('csv', help='CSV to convert.')
      parser.add_argument('--header', default='', help='File containing csv header. Will use first line of CSV if not provided.')
      parser.add_argument('--label', required=True, help='Label for colume being used as truth value.')
      parser.add_argument('--name', default='', help='Name to add to beginning of the files generated. Optional.')
      parser.add_argument('-d', default=',', help='Demilimeter for csv. Defaults to \',\'.')    
      parser.add_argument('-s', default='80/20', help='Train to split ratio. Defaults to 80/20.')
  
      args = parser.parse_args()
      validateArgs(args)

      numFeatures = splitCsv(args)
      genHdf5(args, numFeatures)
  
      print('Done.')
  
if __name__ == '__main__':
    main(sys.argv)