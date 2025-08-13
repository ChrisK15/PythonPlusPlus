class Solution {
    constructor() {}
    fizzbuzz(i) {
        let x = i / 3;
        let floor_result = 0;
        while (x >= 1) {
            x = x - 1;
            floor_result = floor_result + 1;
        }
        let mod_result = i - floor_result * 3;
        if (mod_result == 0) {
            x = i / 5;
            floor_result = 0;
            while (x >= 1) {
                x = x - 1;
                floor_result = floor_result + 1;
            }
            mod_result = i - floor_result * 5;
            if (mod_result == 0) {
                return console.log(10);
            }
        }
        x = i / 3;
        floor_result = 0;
        while (x >= 1) {
            x = x - 1;
            floor_result = floor_result + 1;
        }
        mod_result = i - floor_result * 3;
        if (mod_result == 0) {
            return console.log(1);
        }
        x = i / 5;
        floor_result = 0;
        while (x >= 1) {
            x = x - 1;
            floor_result = floor_result + 1;
        }
        mod_result = i - floor_result * 5;
        if (mod_result == 0) {
            return console.log(0);
        }
    }
}
solution = new Solution();
solution.fizzbuzz(15);