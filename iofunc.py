import numpy as np

def readMatrixText(filename):
   f = open(filename, "r")

   # TODO: Exception checking needed
   line = f.readline().rstrip()
   values = line.split(" ")
   rowCount = int(values[0])
   colCount = int(values[1])

   lineNumber = 0 #variable to keep track of lines read

   #print(values)

   line = f.readline().rstrip()
   symbol0, symbol1 = line.split(" ")

   #print(symbols)

   matrix = np.zeros([rowCount, colCount], dtype=int)
   matrices = []

   # TODO: MAJOR!! Exception checking!!!!!!!!
   while True:
      line = f.readline().rstrip()
      if ";" in line:

         for row in range(rowCount):
            line = f.readline().rstrip()
            if len(line) != colCount:
               # TODO: Raise exception
               pass

            # replace symbols for 1 and 0 and turn them into integers
            line = line.replace(symbol0, "0").replace(symbol1, "1")
            line = [int(symbol) for symbol in line]

            matrix[row] = line

         matrices.append(matrix.copy())
      else:
         break
   
   f.close()
   print(matrices)
   return matrices   

if __name__ == "__main__":
   readMatrixText("input/in1.txt")