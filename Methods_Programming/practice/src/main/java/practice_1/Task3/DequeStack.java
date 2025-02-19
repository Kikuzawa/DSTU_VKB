package practice_1.Task3;

import lombok.extern.slf4j.Slf4j;
import practice_1.Task2.Deque;

@Slf4j
class DequeStack<T> implements StackOperations<T> {
    private final Deque<T> deque;

    public DequeStack(int size) {
        deque = new Deque<>(size);
    }

    @Override
    public void push(T j) {
        if (isFull()) {
            throw new IllegalStateException("Стек заполнен. Не удается добавить новый элемент " + j);
        }
        deque.insertRight(j);

        log.debug("Вставленный элемент в правом углу = {}, обновленный заголовок = {}", j, deque);
    }

    @Override
    public T pop() {
        if (!isEmpty()) {

            var value = deque.removeRight();

            log.debug("RУдален элемент в правом углу = {}, обновлен deque = {}", value, deque);

            return value;
        }
        throw new IllegalStateException("Стек пуст. Невозможно выполнить операцию pop.");
    }

    @Override
    public T peek() {
        if (!isEmpty()) {
            var value = deque.removeRight();
            deque.insertRight(value);

            log.debug("Последний элемент deque = {}, deque = {}", value, deque);

            return value;
        }
        throw new IllegalStateException("Стек пуст. Не удается выполнить peek операцию.");
    }

    @Override
    public boolean isEmpty() {
        return deque.isEmpty();
    }

    @Override
    public boolean isFull() {
        return deque.isFull();
    }

    @Override
    public String toString() {
        return deque.toString();
    }
}
