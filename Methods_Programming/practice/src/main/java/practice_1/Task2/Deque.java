package practice_1.Task2;

import lombok.extern.slf4j.Slf4j;

import java.util.Arrays;

@Slf4j
public class Deque<T> {

    private int rear;
    private int nItems;
    private final int maxSize;
    private final T[] dequeArray;
    private int front;

    @SuppressWarnings("unchecked")
    public Deque(int s) {
        maxSize = s;
        dequeArray = (T[]) new Object[maxSize];
        front = 0;
        rear = -1;
        nItems = 0;
    }

    public void insertRight(T value) {
        if (isFull()) {
            // Если дек полон, передвигаем front для перезаписи элемента
            front = (front + 1) % maxSize; // Сдвигаем front вперед, чтобы освободить место

            log.debug("Дек заполнен, новый front указатель = {}", front);
        }

        // Вставляем элемент в конец дека
        rear = (rear + 1) % maxSize; // Циклический переход

        log.debug("Новый задний индекс с формулой (rear + 1) % максимального размера = {}", rear);

        dequeArray[rear] = value;

        log.debug("Текущее состояние deque = {} rear = {} value = {}", Arrays.toString(dequeArray), rear, value);

        if (nItems < maxSize) {
            nItems++; // Увеличиваем количество элементов, если дек не полон
        }
    }

    public void insertLeft(T value) {
        if (isFull()) {
            // Если дек полон, передвигаем rear для перезаписи элемента
            rear = (rear - 1 + maxSize) % maxSize; // Сдвигаем rear назад, чтобы освободить место
            log.debug("Дек полный, новый rear указатель = {}", rear);
        }

        // Вставляем элемент в начало дека
        front = (front - 1 + maxSize) % maxSize; // Циклический переход

        log.debug("Новый front индекс с формулой (front - 1 + maxSize) и максимальный размер = {}", front);

        dequeArray[front] = value;

        log.debug("Текущее состояние deque = {} front = {} value = {}", Arrays.toString(dequeArray), front, value);

        if (nItems < maxSize) {
            nItems++; // Увеличиваем количество элементов, если дек не полон
        }
    }


    public T removeRight() {
        if (isEmpty()) {
            throw new IllegalStateException("Дек пуст");
        }
        T temp = dequeArray[rear];

        log.debug("Значение для удаления = {}, rear = {}, deque = {}", temp, rear, Arrays.toString(dequeArray));

        rear = (rear - 1 + maxSize) % maxSize;

        log.debug("Новый rear индекс с формулой (rear - 1 + maxsize) % Максимальный размер {}", rear);

        nItems--;

        log.debug("Количество nItems = {}", nItems);

        return temp;
    }

    public T removeLeft() {
        if (isEmpty()) {
            throw new IllegalStateException("дек пуст");
        }
        T temp = dequeArray[front];

        log.debug("Элемент для удаления = {}", temp);

        front = (front + 1) % maxSize;

        log.debug("Новый front индекс с формулой (front + 1) % maxSize {}", front);

        nItems--;
        return temp;
    }


    public boolean isEmpty() {
        return nItems == 0;
    }


    public boolean isFull() {
        return nItems == maxSize;
    }


    @Override
    public String toString() {
        if (isEmpty()) {
            return "[]";
        }

        StringBuilder sb = new StringBuilder();

        int count = 0;
        int current = front;

        while (count < nItems) {
            sb.append(dequeArray[current]).append(" ");
            current = (current + 1) % maxSize; // Циклический переход
            count++;
        }

        return sb.toString().trim();
    }
}
