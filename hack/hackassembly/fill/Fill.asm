// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Screen is 256 by 512 and starts at @SCREEN

// Variable initialization
@8192
D=A
@size // set the range of screen restricted memory addresses ((512*256)/16), divided by 16 because each memory location contains 16 pixels
M=D

//@i
//M=0
//@COLOR_BLACK
//0; JEQ

@state
M=0

@IDLE
0; JEQ

(IDLE)
   @KBD
   D=M

   // If no key pressed then go to color screen directly
   @COLOR_SCREEN
   D; JEQ

   // If key pressed then change state
   D=1
   @COLOR_SCREEN
   0; JEQ

(COLOR_SCREEN)
   @state
   M=D-M // set state comparison value 0 if nothing changed
   D=M

   @IDLE // if state comparison == 0 then go back to loop
   D; JEQ

   @i // reset loop counter before executing any loops
   M=0
   
   @COLOR_BLACK
   D; JGT // state changes to 1 thus we need to render black screen

   @state // button was freed thus we need to white-color the screen and reset the status
   M=0
   @COLOR_WHITE
   D; JLT

(COLOR_BLACK)
   @i // get iterator
   D=M
   @SCREEN // get screen start in memory and shift the pointer by iterator
   A=A+D
   M=-1 // set values to 0xffff (black)

   @i // increase iterator
   D=M+1
   M=D

   @size // get size and calculate difference between size and current iterator
   D=M-D

   @IDLE // if difference < 0 then go back to idle because rendering is finished
   D; JLE

   @COLOR_BLACK // else continue the loop because there are still some pixels to color
   0; JEQ


(COLOR_WHITE)
   @i // get iterator
   D=M
   @SCREEN // get screen start in memory and shift the pointer by iterator
   A=A+D
   M=0 // set values to 0x0000 (white)

   @i // increase iterator
   D=M+1
   M=D

   @size // get size and calculate difference between size and current iterator
   D=M-D

   @IDLE // if difference < 0 then go back to idle because rendering is finished
   D; JLE

   @COLOR_WHITE // else continue the loop because there are still some pixels to color
   0; JEQ



