class Animal {
    constructor() {}
    speak() {
        return console.log(0);
    }
}
class Cat extends Animal {
    constructor() {
        super();
    }
    speak() {
        return console.log(1);
    }
}
class Dog extends Animal {
    constructor() {
        super();
    }
    speak() {
        return console.log(2);
    }
}
let cat = new Cat();
let dog = new Dog();
cat.speak();
dog.speak();