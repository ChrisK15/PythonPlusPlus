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