Pysh
====

# Syntactic Interoperability between Python and Bash

The goal of this project is to make a new linux shell that 
gives all the tools built into bash, but with a syntactic facelift
to look like Python. This enables development of elegant scripting
languages, as well as simple scripting right in the terminal.

## Syntax:

+ Use backticks to explicitly move to a bash context
+ When in a bash context, python variables can be used like they are bash variables with a `$`
+ To spread the output of a bash command into a list, prepend the bash context with `*`
+ To export a python variable into bash, call the `ex` function with the variable name
+ To source a file and add it to your environment, use the `source` command with the filname.

Some examples include:
```
# For-loop over all the files in a directory
readme_file = ""
for filename in *`ls -l`:
  print(f'File of {filename} has a size of {`stat -c %s $filename` / 2e20} GB`)
  if `test -x $filename`: # check if executable
    bash $filename # Execute the filename if present
  if filename == '.env':
    source(filename)
  if filename.startswith('README'):
    cat $filename | var readme_file
```

## Typical bash functionality is supported:
Things like:
+ Command history
+ Reverse-search
+ Pipes and I/O Redirection

I've also added a special new bash command `var` that reads from stdin and assignes to the specified python variable.

Ex. `cat $filename > var file_contents` Makes a new variable called `file_contents` with a value of the contents of the file `$filename`

## Interoperability

### Variable interoperability:

Variables declared in python and bash are readily available in each context. Meaning, variables
declared in python can be accessed in bash, and variables declared in bash are accessable in python.

However, because python and bash have different primitive types, some conversions must be made. The following chart outlines the implicit conversions, or how to nicely convert between types between the two languages.

| Python Type | Bash Type    |
| ----------- | -----------  |
| string      | string       |
| int         | string       |
| float       | string       |
| array       | array        |
| dict        | dict         |

### Explicit Conversion:
Since Bash does not have support for ints and floats, I've added to bash's syntax with an `int` and `float` function allowing for that conversion explicitly.
Ex.
```
`num_lines=int(wc -l myfile.txt)`
```

#### Python Type Hints for implicit conversion.

Declaring variables with types via python's type hints allows for implicit conversion of types
between python and bash. This includes both variables, as well as arguments to functions and their return values.

### Function interoperability.

Functions declared in python are callable in bash. Similarly, any user-defined functions in bash are runnable in python. However, don't forget about the implicit type conversions that will happen between the two languages. Note that calling a bash function from python will involve converting all arguments to strings before they are passed in. Similarly, the returned value will obey the typical conversion outlined in the chart above.

<!-- 
NOTE: Needs revisited once I have interoperability between python and bash arrays working nicely.

## Bash's `test` operator.

The one exception to the interoperability is bash's `test` operator, since it uses square brackets which are typically reserved for list declarations in python. To call the `test` operator in bash, please call `test` directly.

Ex.
```
if `test -x some-executable.sh`:
  print("This file is executable!")
```

### Explicit vanilla bash usage.

Since the `test` exception does technically break bash's syntax, we need a way to explicitly
run code as vanilla bash to allow for running bash scripts that use the bracket `test` syntax. There are two ways to do this:
+ Any script explicitly declared with a shebang will run with the vanilla execution environment specified in the shebang. In other words, any bash script with a `#!/bin/bash` at the top of the file will execute in a vanilla bash context.
+ running bash commands with triple backticks will execute in explicit bash mode. -->
