I am currently conducting research on model checking using z3. Currently in the process of encoding a simple problem and deriving reusable code that can be implemented into more broad problems.

My current problem is as follows: 

process Inc: while true do if x < 200 then x := x + 1 od

process Inc: while true do if x > 0 then x := x - 1 od

process Inc: while true do if x = 200 then x := 0 od
