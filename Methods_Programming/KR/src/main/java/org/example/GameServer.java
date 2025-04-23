package org.example;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.ReentrantLock;
import java.util.Random;
import java.util.List;
import java.util.ArrayList;

/**
 * Класс, управляющий игровым сервером
 * Обрабатывает очередь игроков и управляет их входом/выходом с сервера
 */
public class GameServer {
    // Очередь игроков
    private final PlayerQueue playerQueue;
    // Карта активных игроков на сервере
    private final ConcurrentHashMap<String, Boolean> activePlayers;
    // Блокировка для синхронизации доступа к серверу
    private final ReentrantLock serverLock;
    // Максимальное количество игроков на сервере
    private final int serverCapacity;
    // Текущее количество игроков на сервере
    private int currentPlayers;
    // Генератор случайных чисел
    private final Random random;
    // Флаг состояния сервера
    private boolean isRunning;
    // Флаг заполненности сервера
    private boolean isFull;
    
    /**
     * Конструктор класса
     * @param capacity - максимальное количество игроков на сервере
     */
    public GameServer(int capacity) {
        this.playerQueue = new PlayerQueue();
        this.activePlayers = new ConcurrentHashMap<>();
        this.serverLock = new ReentrantLock();
        this.serverCapacity = capacity;
        this.currentPlayers = 0;
        this.random = new Random();
        this.isRunning = false;
        this.isFull = false;
    }
    
    /**
     * Запуск сервера
     */
    public void startServer() {
        serverLock.lock();
        try {
            if (!isRunning) {
                isRunning = true;
                System.out.println("Сервер запущен.");
                if (playerQueue.getQueueSize() > 0) {
                    System.out.println("В очереди " + playerQueue.getQueueSize() + " игроков. Начинаем их обработку.");
                }
                displayQueueState();
                processQueue();
            } else {
                System.out.println("Сервер уже запущен.");
            }
        } finally {
            serverLock.unlock();
        }
    }
    
    /**
     * Остановка сервера
     */
    public void stopServer() {
        serverLock.lock();
        try {
            if (isRunning) {
                isRunning = false;
                isFull = false;
                // Выгоняем всех игроков с сервера, но сохраняем очередь
                activePlayers.clear();
                currentPlayers = 0;
                System.out.println("Сервер остановлен. Все игроки удалены с сервера.");
                System.out.println("Очередь сохранена (" + playerQueue.getQueueSize() + " игроков в очереди).");
                displayQueueState();
            } else {
                System.out.println("Сервер уже остановлен.");
            }
        } finally {
            serverLock.unlock();
        }
    }
    
    /**
     * Проверка состояния сервера
     * @return true если сервер запущен, false если остановлен
     */
    public boolean isServerRunning() {
        return isRunning;
    }
    
    /**
     * Проверка заполненности сервера
     * @return true если сервер заполнен, false если есть свободные места
     */
    public boolean isServerFull() {
        return isFull;
    }
    
    /**
     * Отображение текущего состояния очереди и сервера
     */
    private void displayQueueState() {
        System.out.println("\n[LOG] Текущее состояние:");
        System.out.println("[LOG] Статус сервера: " + (isRunning ? "Запущен" : "Остановлен"));
        System.out.println("[LOG] Игроков на сервере: " + currentPlayers + "/" + serverCapacity);
        System.out.println("[LOG] Игроков в очереди: " + playerQueue.getQueueSize());
        System.out.println("[LOG] -------------------------\n");
    }
    
    /**
     * Метод обработки очереди
     * Проверяет возможность входа игроков на сервер
     */
    public void processQueue() {
        serverLock.lock();
        try {
            if (isRunning && !playerQueue.isEmpty() && currentPlayers < serverCapacity) {
                String playerId = playerQueue.getNextPlayer();
                if (playerId != null) {
                    activePlayers.put(playerId, true);
                    currentPlayers++;
                    System.out.println("Игрок " + playerId + " вошел на сервер. Игроков на сервере: " + currentPlayers);
                    displayQueueState();
                    
                    if (currentPlayers >= serverCapacity) {
                        isFull = true;
                        System.out.println("Сервер заполнен. Ожидание выхода игроков...");
                        displayQueueState();
                    }
                }
            }
        } finally {
            serverLock.unlock();
        }
    }
    
    /**
     * Метод выхода игрока с сервера
     * @param playerId - ID игрока, покидающего сервер
     */
    public void leaveServer(String playerId) {
        serverLock.lock();
        try {
            if (activePlayers.remove(playerId) != null) {
                currentPlayers--;
                isFull = false;
                System.out.println("Игрок " + playerId + " покинул сервер. Осталось игроков: " + currentPlayers);
                displayQueueState();
                // После выхода игрока проверяем очередь
                processQueue();
            }
        } finally {
            serverLock.unlock();
        }
    }
    
    /**
     * Метод выхода случайного игрока с сервера
     * @return true если игрок был удален, false если сервер пуст
     */
    public boolean leaveRandomPlayer() {
        serverLock.lock();
        try {
            if (currentPlayers > 0) {
                List<String> players = new ArrayList<>(activePlayers.keySet());
                String randomPlayer = players.get(random.nextInt(players.size()));
                leaveServer(randomPlayer);
                return true;
            }
            return false;
        } finally {
            serverLock.unlock();
        }
    }
    
    /**
     * Метод добавления игрока в очередь
     * @param playerId - ID игрока
     */
    public void joinQueue(String playerId) {
        playerQueue.joinQueue(playerId);
        if (!isRunning) {
            System.out.println("Сервер остановлен. Игрок добавлен в очередь и будет допущен на сервер после его запуска.");
        } else if (!isFull) {
            processQueue();
        }
        displayQueueState();
    }
    
    /**
     * Получение текущего количества игроков на сервере
     * @return количество игроков
     */
    public int getCurrentPlayers() {
        return currentPlayers;
    }
    
    /**
     * Получение текущего размера очереди
     * @return количество игроков в очереди
     */
    public int getQueueSize() {
        return playerQueue.getQueueSize();
    }
    
    /**
     * Получение списка игроков на сервере
     * @return список ID игроков
     */
    public List<String> getActivePlayers() {
        return new ArrayList<>(activePlayers.keySet());
    }
    
    /**
     * Продолжить обработку очереди
     */
    public void continueQueue() {
        if (isRunning) {
            processQueue();
        } else {
            System.out.println("Сервер остановлен. Невозможно продолжить обработку очереди.");
        }
    }

    public void print(){
        playerQueue.printQueue();
    }
} 