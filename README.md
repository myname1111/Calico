# Calico
My own custom programming language Calico
### Table of Contents:
* [Table of Contents](#table-of-contents)
* [Introduction](#introduction)
* [Getting Started](#getting-started)
* [Changelog](#changelog)
* [Building Calico](#building-calico)
* [TODO](#todo)
## Introduction
Calico is a custom language i made in mid 2021 and is still developing. This idea was first proposed in 2020? 2019? i forgot. Calico has borrowed a lot of thigs from python so it is reasonably easy .

Currently Calico supports(V0.2):
- Simple arithmetic
- Tuples
- Function calls
- Print input builtins
- Multi-line code
- Strings
- Comparison operators
- Bools
- If else elif statements
- Func def
- While loops
## Getting started
### Hello world
For most languages hello world is simple, and calico is one of them. 

First we are introduced to the print function. it prints out everything in it. `print`

Next we are introduced to str. It's not a class, classes are supported in the next version `"Hello world!"`

```
print("hello world")
```
### Math
Math in Calico is the same as any other language.
### If's, Else's, Elif's
Calico handels if's like any other language

syntax: 
```
if CONDITION CODE
```

calico handels code blocks with brackets 
```
{
  a = 1 + 2
}
```

elifs are the same as 
```
else {
  if ...
}
```
example of if's 
```
if {
  a > b
} {
  print(a)
}
```
### Multi-line code
Calico handels Multi-line Code using `;`. 

exemples of multi-line code
```
a = 1;
b = 2;
if {
  a > b
} {
  print("a is more than b")
} else {
  print("a is more than b")
}
```
### Functions
#### Defining functions
Lets say we have a simple function foo. this function will print out `"Foo bar"` everytime we call it

to define this function we type the keyword `method` the type the function name `foo`\
then we we type an empty tuple
after that we call the print method to print `"Foo bar"` to the console

It should look like this
```
method foo() {
  print("Foo bar")
}
```
#### Calling functions
before callicng your custom function, there are a few builtin methods you shpuld learn

print, prints
input, get input from user
int, turns str to int
get_prec, gets the floating point precision
set_prec, sets the floating point precision

to call a custom function first type the name of the function,/
then write a tuple with all of the parameters of the function

example
```
foo()
```
### While loops
syntax `WHILE CONDITION CODE`\
example
```
a = 0;
while {
  a < 10
} {
  print(a);
  a = a + 1
}
```
## Changelog
### Calico V 0.2.1:
    -fix multi call bug
    -fix rounding error
    -fix bug with recursion
    -build using cx_freeze instead of pyinstaller
### Calico V 0.2:
    -Added compare
    -Added bools
    -Added if else elif
    -Added func def
    -differentiate from pythons
    -OPTIMIZE
    -Added while loop
### Calico V 0.1:
    -The birth of Calico
    -Added Simple arithmetic
    -Added Tuple
    -Added function call
    -Added Print input builtins
    -Added support multi-line output
    -Added strings
## Building Calico
Requiremts
- ply
- sys
- copy
- time
- decimal

### Building
```
cd PATH\Calico\Calico
python setup.py build # use bdist_msi if you want a windows installer
```
## TODO
### TODO V0.3:
    -add for
    -add tuple getitem
    -add string getitem
    -add string oper
    -add class
    -add try
    -add str builtins
    -add exp oper
    -add sqrt oper
    -add include
    -add OOP
    -add list
