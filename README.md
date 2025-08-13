# 🐍 P++ (PythonPlusPlus)

## ☕📜 Target Language: JavaScript

## 🎓 Language Description and Goal:

The goal of this project is for me to gain non-leetcode experience working with Python and improve my understanding of object-oriented programming. The language will be similar to the likes of Java and C++ in terms of classes and syntax.

## 🚀 Key Features:

Objects + methods with class-based inheritance, subtyping, checking if a variable is initialized before use, checking if void is used as a value, checking that a function returning non-void always returns, non-S-expression-based syntax.

## ❌ Planned Restrictions:

No optimizations :(

## 📝 Concrete Syntax

```
- type ::= `int` | `boolean` | `void` | Built-in types classname class type; includes Object and String 
- comma_exp ::= [exp (`,` exp)*]
- primary_exp ::= 
    - `var` | `int` | Variables, strings, and integers are expressions
    - `(` exp `)` | Parenthesized expressions
    - `this` | Refers to my instance
    - `true` | `false` | Booleans
    - `println` `(` exp `)` | Prints something to the terminal
    - `new` classname `(` comma_exp `)` | Creates a new object
- call_exp ::= primary_exp (`.` methodname `(` comma_exp `)`)*
- mult_exp ::= call_exp ((`*` | `/`) call_exp)*
- add_exp ::= mult_exp ((`+` | `-`) mult_exp)*
- compare_exp ::= add_exp (('<' | '<=' | '>' | '>=') add_exp)*
- equality_exp ::= compare_exp (('==' | '!=') compare_exp)*
- exp ::= equality_exp
- vardec ::= type var `=` exp
- stmt ::= 
  - exp `;` | Expression statements
  - vardec `;` | Variable declaration
  - var `=` exp `;` | Assignment
  - `while` `(` exp `)` stmt | while loops
  - `break` `;` | break
  - `return` [exp] `;` | return, possibly void
  - `if` `(` exp `)` stmt [`else` stmt ] | if with optional else
  - `{` stmt* `}` | Block
- comma_params ::= [param (`,` param)*]
- param ::= type var
- methoddef ::= `def` type methodname `(` comma_params `)` `{` stmt* `}`
- constructor ::= `init` `(` comma_params `)` `{` [`super` `(` comma_exp `)` `;` ] stmt* `}`
- classdef ::= `class` classname [`extends` classname] `{` (param `;`)* constructor methoddef* `}`
- program ::= classdef* stmt+ | stmt+ is the entry point
```

## 🐶🐱 Example 1: Animals with a speak method

```
class Animal {
    init() {}
    def void speak() { return println(0); }
}

class Cat extends Animal {
    init() { super(); }
    def void speak() { return println(1); }
}

class Dog extends Animal {
    init() { super(); }
    def void speak() { return println(2); }
}

Animal cat = new Cat();
Animal dog = new Dog();
cat.speak();
dog.speak();
```

## ⚡ Example 2: Fizzbuzz (kind of)
Returns '1' if i is divisible by 3
Returns '0' if i is divisible by 5
Returns '10' if i is divisible by 3 and 5
```
class Solution {
    init() {}
    def void fizzbuzz(int i) {
        int x = i / 3;
        int floor_result = 0;
        while (x >= 1) {
            x = x - 1;
            floor_result = floor_result + 1;
        }
        int mod_result = i - (floor_result * 3);
        if (mod_result == 0) {
            x = i / 5;
            floor_result = 0;
            while (x >= 1) {
                x = x - 1;
                floor_result = floor_result + 1;
        }
        mod_result = i - (floor_result * 5);
        if (mod_result == 0) {
            return println(10);
        }
        }

        x = i / 3;
        floor_result = 0;
        while (x >= 1) {
            x = x - 1;
            floor_result = floor_result + 1;
        }
        mod_result = i - (floor_result * 3);
        if (mod_result == 0) {
            return println(1);
        }

        x = i / 5;
        floor_result = 0;
        while (x >= 1) {
            x = x - 1;
            floor_result = floor_result + 1;
        }
        mod_result = i - (floor_result * 5);
        if (mod_result == 0) {
            return println(0);
        }
    }
}

solution = new Solution();
solution.fizzbuzz(15);
```

## 📝 How to Build
```shell
# Make sure you are running Python3.13!

# Clone the repository
https://github.com/ChrisK15/PythonPlusPlus.git

# Navigate to project directory
cd PythonPlusPlus

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install CLI commands and dependancies
poetry install

# Run test files (and create your own)
ppp test_files/test.pp
```

## 📚 Useful Commands
```shell
# Testing
poetry run pytest -v

# Testing with coverage report (Report is generated in terminal window)
poetry run pytest --cov=src --cov-report=term-missing

# Type checking
poetry run mypy src/ --explicit-package-bases

# Code formatting (Runs black and isort)
bash housekeeping.bash

# Run PythonPlusPlus files
ppp "insert_file_path_here"
```
