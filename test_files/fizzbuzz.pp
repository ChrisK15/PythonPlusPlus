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