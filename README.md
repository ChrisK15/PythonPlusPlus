# 🐍 P++ (PythonPlusPlus)

## ☕📜 Target Language: JavaScript

## 🎓 Language Description and Goal:

The goal of this project is for me to gain non-leetcode experience working with Python. The language will be similar to the likes of Java and C++in terms of classes and syntax.

## 🚀 Key Features:

Objects + methods with class-based inheritance, subtyping, checking if a variable is initialized before use, checking if void is used as a value, checking that a function returning non-void always returns, non-S-expression-based syntax.

## ❌ Planned Restrictions:

No optimizations :(

## 📝 Concrete Syntax

```
- type ::= `int` | `boolean` | `void` | Built-in types classname class type; includes Object and String 
- comma_exp ::= [exp (`,` exp)*]
- primary_exp ::= `var` | `int` | Variables, strings, and integers are expressions
- `(` exp `)` | Parenthesized expressions
- `this` | Refers to my instance
- `true` | `false` | Booleans
- `println` `(` exp `)` | Prints something to the terminal
- `new` classname `(` comma_exp `)` | Creates a new object
- call_exp ::= primary_exp (`.` methodname `(` comma_exp `)`)*
- mult_exp ::= call_exp ((`*` | `/`) call_exp)*
- add_exp ::= mult_exp ((`+` | `-`) mult_exp)*
- exp ::= add_exp
- vardec ::= type var
- stmt ::= exp `;` | Expression statements
  - vardec `;` | Variable declaration
  - var `=` exp `;` | Assignment
  - `while` `(` exp `)` stmt | while loops
  - `break` `;` | break
  - `return` [exp] `;` | return, possibly void
  - `if` `(` exp `)` stmt [`else` stmt ] | if with optional else
  - `{` stmt* `}` | Block
- comma_vardec ::= [vardec (`,` vardec)*]
- methoddef ::= `def` type methodname `(` comma_vardec `)` `{` stmt* `}`
- constructor ::= `init` `(` comma_vardec `)` `{` [`super` `(` comma_exp `)` `;` ] stmt* `}`
- classdef ::= `class` classname [`extends` classname] `{` (vardec `;`)* constructor methoddef* `}`
- program ::= classdef* stmt+ | stmt+ is the entry point
```

## 🐶🐱 Example: Animals with a speak method

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

Animal cat;
Animal dog;
cat = new Cat();
dog = new Dog();
cat.speak();
dog.speak();
```

## 📝 How to Build
*Note: The following instructions will change as the project grows*
```shell
# Clone the repository
https://github.com/ChrisK15/PythonPlusPlus.git

# Navigate to project directory
cd PythonPlusPlus

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## 📚 Useful Commands
```shell
# Testing
poetry run pytest -v

# Testing with coverage report (Report is generated in terminal window)
poetry run pytest --cov=src --cov-report=term-missing

# Type checking (Haven't really found this super useful yet)
poetry run mypy src/ --explicit-package-bases

# Code formatting (Runs black and isort)
bash housekeeping.bash
```