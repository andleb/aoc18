#ip 4

# test
seti 123 0 3
bani 3 456 3
eqri 3 72 3

000140
or
000040
#will go to eqri again if fail
addr 3 4 4

# clear 4 - go to 0 skipped else
seti 0 0 4

#A
#init state
[0,0,0,1,4,0]

# clears 3 - the result of prev check
seti 0 5 3

bori 3 65536 5
seti 5557974 2 3

bani 5 255 2
addr 3 2 3
bani 3 16777215 3
muli 3 65899 3
bani 3 16777215 3
gtir 256 5 2


#B
#does nothing unless *2 != 0
#then skip the next one
addr 2 4 4

#goto 18 - clear 2
addi 4 1 4

#skipped initially
[0, 0, 0, 1526130, 14, 65536]
# Go to target!
seti 27 9 4
[0, 0, 0, 1526130, 28, 65536]

#clear 2
seti 0 0 2

addi 2 1 1
muli 1 256 1
gtrr 1 5 1

#cond: *1 > 0
# *1 > *5
# (*2 + 1)*256 > *5
# *5 > 65356 if not skipped in seti 7 1 4
# *2 is cleared above!
# *5 <= (*2+13)
addr 1 4 4
addi 4 1 4

#triggered above: goto 27 - setr 2 2 5
seti 25 4 4

addi 2 1 2
#goto 18 ie addi 2 1 1
seti 17 6 4

#cond: *2 + *5 < 256
setr 2 2 5
# goto 8 ie bani 5 255 2 - part A2
#COND: *5 < 256
seti 7 1 4

#target: *4 == 28
eqrr 3 0 2
addr 2 4 4

# goto 6 - part A1
# bori 3 65536 5 without clearing 3!
# set 5 > 65536 FAIL
seti 5 7 4
