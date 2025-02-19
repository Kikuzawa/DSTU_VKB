package practice_1.Task1;

import lombok.extern.slf4j.Slf4j;

import java.util.Arrays;

@Slf4j
public class Queue<T> {
    private final int maxSize;
    private final T[] queArray;
    private int front;
    private int rear;
    private int nItems;

    @SuppressWarnings("unchecked")
    public Queue(int s) {
        maxSize = s;
        // Приведение типа для создания массива нужного типа
        queArray = (T[]) new Object[maxSize];
        front = 0;
        rear = -1;
        nItems = 0;
    }

    /**
     * Вставка элемента в конец очереди.
     * @param j значение, которое мы хотим вставить.
     */
    public void insert(T j) {
        if (isFull()) {
            front = (front + 1) % maxSize; // Смещаем front вперёд при переполнении
            log.debug("Очередь заполнена, новый передний индекс {}", front);
        }
        rear = (rear + 1) % maxSize; // Циклическое обновление rear
        log.debug("Новый задний указатель {}", rear);

        queArray[rear] = j;

        log.debug("Новый вид массива в очереди: {}", Arrays.toString(queArray));

        if (nItems < maxSize) {
            nItems++; // Увеличиваем только если не переполнено
        }
    }

    /**
     * Извлечение элемента в начале очереди.
     * @return возвращает первый элемент очереди.
     */
    public T remove() {
        T temp = queArray[front]; // Выборка элемента

        log.debug("Удаление элемента {} из очереди: {}", temp, Arrays.toString(queArray));

        front = (front + 1) % maxSize; // Циклический перенос front

        log.debug("Новый передний индекс {}", front);

        nItems--; // Уменьшение количества элементов
        return temp;
    }

    /**
     * Удаление n элементов из начала очереди.
     * @param n количество элементов в очереди, которое мы хотим удалить.
     * @return возвращает массив элементов, которые мы хотим удалить.
     */
    @SuppressWarnings("unchecked")
    public T[] remove_n(int n) {
        int actualRemove = Math.min(n, nItems); // Удаляем меньшее из n или текущего количества элементов

        // Для создания массива типа T используем generic метод
        T[] removedElements = (T[]) new Object[actualRemove];

        for (int i = 0; i < actualRemove; i++) {
            removedElements[i] = queArray[front]; // Копирование удаляемого элемента
            front++;
            if (front == maxSize) { // Циклический перенос
                front = 0;
            }
            nItems--; // Уменьшение количества элементов
        }
        return removedElements;
    }

    /**
     * Чтение элемента в начале очереди.
     * @return возвращает первый элемент из очереди.
     */
    public T peekFront() {
        return queArray[front];
    }

    //--------------------------------------------------------------
    public boolean isEmpty() {
        return (nItems == 0);
    }

    /**
     * Метод для проверки, полная ли очередь.
     * @return возвращает true, если очередь заполнена, в ином случае false.
     */
    public boolean isFull() {
        return (nItems == maxSize);
    }

    /**
     * Метод геттер для получения количества элементов в очереди.
     * @return возвращает целое число - количество
     */
    public int size() {
        return nItems;
    }

    /**
     * Метод для вывода количества элементов в очереди, учитывая циклическое поведение.
     * Очередь — циклическая (при достижении конца массива индекс переходит в начало).
     */
    @Override
    public String toString() {
        if (isEmpty()) { // Проверяем, пуста ли очередь
            return "[]";
        }

        StringBuilder sb = new StringBuilder();

        int count = nItems; // Количество элементов в очереди
        int index = front; // Начинаем с позиции front

        log.debug("Текущий шаг построения строки = {}\n" +
                "new_index = {}\n" +
                "count= {}\n\n", sb, index, count);

        while (count > 0) {
            sb.append(queArray[index]).append(" "); // Добавляем текущий элемент
            index = (index + 1) % maxSize; // Переходим к следующему индексу (с учётом цикличности)
            count--; // Уменьшаем количество оставшихся элементов

            log.debug("Текущий шаг построения строки = {}\n" +
                    "new_index = {}\n" +
                    "count = {}\n\n", sb, index, count);

        }

        return sb.toString().trim(); // Убираем лишний пробел в конце
    }
}