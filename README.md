# truth-table
creates latex code for a filled truth table from the propositional and propositional formula

For now, there is a command line interface only.

**Manual:**

  1. create object TTable([prop variables], [prop formula])  
  2. object.print_latex() to get the latex code
  
Be sure to put the parenthesis in the propositional formula

Ex:
```
test = TTable(['a', 'b', 'c'], ["(a and b)", "(a implies c)"])
test.print_latex()
```
