## Overview:
   This is my attempt at the popular Nand2Tetris course at coursera (and corresponding book *"The Elements of Computing Systems, Buildling a Modern Computer from First Principles"* by Noam Nisan and Shimon Schocken), feel free to visit original nand2tetris page at www.nand2tetris.org.
   
   This essentially comes down to buidling a computer from the very scratch, starting from NAND and DFF gates and going up and up until we finish with a game ("tetris"). The computer is called 'hack' and for details I strongly suggest taking a look at the course or book itself. Almost all of these lower-level gates and chips have corresponding *.tst files that were provided by course staff to make sure that what we implemented works as intended. In the later parts you can also find some compliers, OS, virtual machines etc. etc. - generally all the fun stuff in simplified versions. *.out & *.cmp files are also part of the tests. Most of the runnables also contain theirs own 'readme' unless I forgot / was too lazy to write it.

   It's worth noting that everything is a little simplified but apparently only simplified as much as possible but this complex enough to make sure that students can grasp all required concepts.

## Directory explanation:
   - **'tools'** - all of these were provided by the course staff, those are Java applications that help/allow the simulation of logic gates and chips written in this custom HDL (Hardware Description Language).
   - **'hack'** - this is the lowest part that represents a complete computer (based on Harvard Architecture) and consists of all logic gates and chips (ie. ALU unit, CPU unit etc.) that are neccessary for our hardware simulation, it is assumed that programmers shouldn't really go lower than that because implementation of those chips is strictly related to physics and electrical engineering, it is advised to just assume that this contract is true and so I did.
      Also, this part is a bit different directory wise from the course one because I wanted to make it a little more meaningful and potentially expand a few gates here and there (not sure if I'll actually pursue that idea).
      - **'gates'** and **'memory'** - implemented elementary gates / chips: 
         Elementary: Nand (provided, native), Not, And, Or, Xor, Mux, Dmux
         16-bit variants: Not16, And16, Or16, Mux16
         Multi-way variants: Or8Way, Mux4Way16, Mux8Way16, DMux4Way, DMux8Way
         Mathunit: Add16, ALU, HalfAdder, FullAdder, Inc16
         Memory: Bit, Register, RAM8 ... RAM16K
      - **'hackassembly'** has two basic programs written in hack assembly
      - **'mathunit'** - ALU chip and all supporting chips
      - **'CPU'** - containes the biggest and final chip - CPU.hdl and Computer.hdl, this is the pinnacle of the hardware part. I didn't put too much effort here, I was basing my solutions on existing ones because I didn't feel like implementing this part would contribute much to my understanding
   - **'hack_assembler'** - this is a hack assembler, it basically transforms Hack Assembly into Hack binary code that is runnable by our newly made computer, it's written in Python thus to run it you require Python 3.5+ interpreter. This is basically my own version of the assembler that is already provided in tools.
      

## Instructions:
   - One day, when part 2 is finished.
