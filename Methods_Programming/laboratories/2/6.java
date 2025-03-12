
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Collectors;

public class SuperSum {
static int[] countPartitions(int[] numbers) {
        Map<Integer, Long> countMap = Arrays.stream(numbers)
                .boxed()
                .collect(Collectors.groupingBy(n -> n, Collectors.counting()));

        int[] results = new int[numbers.length];

        for (var i = 0; i < numbers.length; i++) {
            int number = numbers[i];
            int count = 0;

            for (Map.Entry<Integer, Long> entry : countMap.entrySet()) {
                var x = entry.getKey();
                var y = number - x;

                // Избегаем дублирования
                if (y < x) {
                    continue;
                }

                var xCount = entry.getValue();

                if (x == y) {
                    // Если x и y одинаковые, то выбираем 2 из countMap[x]
                    count += xCount * (xCount - 1) / 2;
                } else if (countMap.containsKey(y)) {
                    // Если x и y разные, то просто перемножаем их количества
                    count += xCount * countMap.get(y);
                }
            }

            results[i] = count;
        }

        return results;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] numbers = new int[n];

        for (int i = 0; i < n; i++) {
            numbers[i] = scanner.nextInt();
        }

        int[] partitions = countPartitions(numbers);

        for (int result : partitions) {
            System.out.println(result);
        }

        scanner.close();
    }
}

