// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Initialize RAM[2] (output placement) to 0
@2
M=0
// Get RAM[1] value
@1
D=M
// Save RAM[1] value to 'n' variable, this will be our loop border
@n
M=D-1 // subtract 1 because we'll start counting from 0 instead of 1
// Initialize i as 0 
@i
M=0
// Initialize outcome variable
@outcome
M=0

@n
D=M
@ADDER
D; JGE

// Jump to infinite loop to prevent CPU from executing malicious code
@END
0; JEQ



(ADDER)
   @0   // Fetch RAM[0] value that will be multiplier
   D=M
   @outcome // Fetch and add multipler to current outcome
   M=M+D
   @i     // Fetch and increase loop current count
   M=M+1
   D=M

   // Check if adder should continue
   @n
   D=M-D
   @ADDER
   D; JGE

   // If adder finished then move @outcome to RAM[2] location to match program description
   @outcome
   D=M
   @2
   M=D

   // Jump to infinite loop to prevent CPU from executing malicious code
   @END
   0; JEQ


(END)
   @END
   0; JEQ
