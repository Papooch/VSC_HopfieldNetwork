import numpy as np

def readMatrixText(filename):
   """
   Returns a list of matrices of 0s and 1s with dimensions specified in the input file.

   Parameters
   ----------
   @param filename:  Path of the input file \n 
   @returns: List of numpy 2D arrays
   """
   f = open(filename, "r")

   # TODO: Exception checking needed
   line = f.readline().rstrip()
   values = line.split(" ")
   rowCount = int(values[0])
   colCount = int(values[1])

   #lineNumber = 0 # TODO: variable to keep track of lines read

   #print(values)

   line = f.readline().rstrip()
   symbols = line.split(" ")

   #print(symbols)

   matrix = np.zeros([rowCount, colCount], dtype=int)
   matrices = []

   # TODO: MAJOR!! Exception checking!!!!!!!!
   while True:
      line = f.readline().rstrip()
      if ";" in line:

         for row in range(rowCount):
            line = "".join(f.readline().split())
            if len(line) != colCount:
               # TODO: Raise exception
               pass

            # replace symbols for 1 and 0 and turn them into integers
            line = line.replace(symbols[0], "0").replace(symbols[1], "1")
            line = [int(symbol) for symbol in line]

            matrix[row] = line

         matrices.append(matrix.copy())
      else:
         break
   
   f.close()
   #print(matrices)
   return matrices

def writeMatrixText(filename, matrices, symbols=["0", "1"]):
   """
   Writes matrices in file of specified format, if the file does not exist it is created.

   Parameters
   ----------
   @param filename: Path of the output file \n 
   @param matrices: List of matrices to be saved \n
   @param symbols: List of two substitute symbols for 0 and 1 respectively \n
   @returns: True if succeeded
   """
   #TODO: Exception checking

   f = open(filename, "w")
   f.write("%d %d\n" %(len(matrices[0]), len(matrices[0][0])))
   f.write(symbols[0] + " " + symbols[1] + "\n")
   for matrix in matrices:
      f.write(";\n")
      for line in matrix:
         line = "".join(str(i) for i in line)
         line = line.replace("0", symbols[0]).replace("1", symbols[1])
         f.write(line + "\n")

   return True


def readMatrixTextMultipleFiles(filelist):
   matrices = []
   for filename in filelist:
      matrices.extend(readMatrixText(filename))
   return matrices


if __name__ == "__main__":
   mats = readMatrixTextMultipleFiles(["input/in1.txt", "input/in2.txt"])   
   print(mats)
   writeMatrixText("output/out4.txt", mats, ["0", "1"])