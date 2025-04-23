package org.example;

import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Класс, реализующий очередь игроков
 * Использует потокобезопасную очередь LinkedBlockingQueue
 */
public class PlayerQueue {
    // Потокобезопасная очередь (класс блокирующей очереди на связанных узлах) для хранения ID игроков
    private final LinkedBlockingQueue<String> queue;
    // Блокировка для синхронизации доступа к очереди
    private final ReentrantLock lock;
    
    /**
     * Конструктор класса
     * Инициализирует очередь и блокировку
     */
    public PlayerQueue() {
        this.queue = new LinkedBlockingQueue<>();
        this.lock = new ReentrantLock();
    }
    
    /**
     * Добавление игрока в очередь
     * @param playerId - уникальный идентификатор игрока
     * @return позиция игрока в очереди
     */
    public int joinQueue(String playerId) {
        lock.lock();
        try {
            queue.put(playerId);
            System.out.println("Игрок " + playerId + " встал в очередь. Позиция: " + queue.size());

            return queue.size();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return -1;
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * Получение следующего игрока из очереди
     * @return ID следующего игрока или null, если очередь пуста
     */
    public String getNextPlayer() {
        lock.lock();
        try {
            return queue.poll();
        } finally {
            lock.unlock();
        }
    }
    
    /**
     * Проверка пуста ли очередь
     * @return true если очередь пуста, false в противном случае
     */
    public boolean isEmpty() {
        return queue.isEmpty();
    }
    
    /**
     * Получение текущего размера очереди
     * @return количество игроков в очереди
     */
    public int getQueueSize() {
        return queue.size();
    }

    public void printQueue() {
        System.out.println("Текущее состояние очереди: " + queue);
    }
} 