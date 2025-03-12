package practice_1.Task1;

import java.util.Arrays;

class Main {
    public static void main(String[] args) {
        Queue<Integer> queue = new Queue<>(5);
        int[] elementsToInsert1 = {1, 2, 3, 4, 5, 40};
        System.out.println("Элементы для добавления: " + Arrays.toString(elementsToInsert1));
        for (var element : elementsToInsert1) {
            queue.insert(element);
        }
        System.out.println("Содержимое: " + queue);
        System.out.print("Извлекаем элементы: ");
        for (int i = 0; i < 3; i++) {
            System.out.print(queue.remove() + " ");
        }
        System.out.println("\nСодержимое: " + queue);
        System.out.println("Первый элемент: " + queue.peekFront());
        int[] elementsToInsert2 = {105, 106, 107, 108};
        System.out.println("Элементы для добавления: " + Arrays.toString(elementsToInsert2));
        for (var element : elementsToInsert2) {
            queue.insert(element);
        }
        System.out.println("Содержимое: " + queue);
        System.out.print("Извлечение и вывод всех элементов: ");
        while (!queue.isEmpty()) {
            var n = queue.remove();
            System.out.print(n + " ");
        }
        System.out.println("\n" + "Содержимое: " + queue);
        int[] elementsToInsert3 = {44, 55, 66, 88};
        System.out.println("Элементы для добавления: " + Arrays.toString(elementsToInsert3));
        for (var element : elementsToInsert3) {
            queue.insert(element);
        }
        System.out.println("Содержимое: " + queue);
        System.out.println("Удалили:" + Arrays.toString(queue.remove_n(2)));
        System.out.println(queue);
    }
}

