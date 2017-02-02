
   This is my attempt at the popular Nand2Tetris course at coursera (and corresponding book "The Elements of Computing Systems, Buildling a Modern Computer from First Principles by Noam Nisan and Shimon Schocken").
   
   This comes down to buidling a computer from the very scratch, starting from NAND gates and going up and up until we finish with a game ("tetris").
   Some directories:
      hack - this is the lowest part that consists of all logic gates (and ALU unit) that are neccessary for our hardware simulation, it is assumed that programmers shouldn't really go lower than that because implementation of those chips is strictly related to physics and electrical engineering, we just assume that this contract is true.
         - Gates:
            - Implemented gates: 
               Elementary: Nand (provided, native), Not (+), And (+) , Or (+), Xor (+), Mux (+), Dmux (+)
               16-bit variants: Not16 (+), And16 (+), Or16 (+), Mux16 (+)
               Multi-way variants: Or8Way (+), Mux4Way16 (?), Mux8Way16 (+*), DMux4Way (+*), DMux8Way()
            - 
      

   Instructions:
      - yeye
