package org.example;


/* 14
Мультиплеерная очередь
Игроки ждут своей очереди для входа на сервер. Реализуйте систему, которая пускает их в порядке подключения.
*/
import java.util.Scanner;
import java.util.List;

/**
 * Главный класс для управления системой очереди игроков
 */
public class Main {
    private static final Scanner scanner = new Scanner(System.in);
    private static int playerCounter = 0;

    public static void main(String[] args) {
        // Создаем сервер с максимальной вместимостью 4 игрока
        GameServer server = new GameServer(4);

        boolean running = true;
        while (running) {
            displayMenu();
            int choice = getIntInput("Выберите действие: ");

            switch (choice) {
                case 1:
                    startServer(server);
                    break;
                case 2:
                    stopServer(server);
                    break;
                case 3:
                    addPlayerToQueue(server);
                    break;
                case 4:
                    removeSpecificPlayer(server);
                    break;
                case 5:
                    removeRandomPlayer(server);
                    break;
                case 6:
                    displayCurrentState(server);
                    break;
                case 7:
                    continueQueue(server);
                    break;
                case 0:
                    running = false;
                    System.out.println("Программа завершена.");
                    break;
                default:
                    System.out.println("Неверный выбор. Попробуйте снова.");
            }
            server.print();
        }

        scanner.close();
    }
    
    /**
     * Отображение меню действий
     */
    private static void displayMenu() {
        System.out.println("\n=== Меню управления сервером ===");
        System.out.println("1. Запустить сервер");
        System.out.println("2. Остановить сервер");
        System.out.println("3. Добавить игрока в очередь");
        System.out.println("4. Удалить конкретного игрока с сервера");
        System.out.println("5. Удалить случайного игрока с сервера");
        System.out.println("6. Показать текущее состояние");
        System.out.println("7. Продолжить обработку очереди");
        System.out.println("0. Завершить программу");
    }
    
    /**
     * Запуск сервера
     */
    private static void startServer(GameServer server) {
        server.startServer();
    }
    
    /**
     * Остановка сервера
     */
    private static void stopServer(GameServer server) {
        server.stopServer();
    }
    
    /**
     * Добавление нового игрока в очередь
     */
    private static void addPlayerToQueue(GameServer server) {
        if (server.isServerFull()) {
            System.out.println("Сервер заполнен. Игрок добавлен в очередь и будет допущен после освобождения места.");
        }
        String playerId = "Игрок_" + playerCounter++;
        server.joinQueue(playerId);
    }
    
    /**
     * Удаление конкретного игрока с сервера
     */
    private static void removeSpecificPlayer(GameServer server) {
        if (!server.isServerRunning()) {
            System.out.println("Сервер остановлен. Невозможно удалить игрока.");
            return;
        }
        
        List<String> activePlayers = server.getActivePlayers();
        if (activePlayers.isEmpty()) {
            System.out.println("На сервере нет игроков.");
            return;
        }
        
        System.out.println("\nТекущие игроки на сервере:");
        for (int i = 0; i < activePlayers.size(); i++) {
            System.out.println((i + 1) + ". " + activePlayers.get(i));
        }
        
        int playerNumber = getIntInput("Выберите номер игрока для удаления: ");
        if (playerNumber > 0 && playerNumber <= activePlayers.size()) {
            server.leaveServer(activePlayers.get(playerNumber - 1));
        } else {
            System.out.println("Неверный номер игрока.");
        }
    }
    
    /**
     * Удаление случайного игрока с сервера
     */
    private static void removeRandomPlayer(GameServer server) {
        if (!server.isServerRunning()) {
            System.out.println("Сервер остановлен. Невозможно удалить игрока.");
            return;
        }
        
        if (!server.leaveRandomPlayer()) {
            System.out.println("На сервере нет игроков.");
        }
    }
    
    /**
     * Отображение текущего состояния сервера и очереди
     */
    private static void displayCurrentState(GameServer server) {
        System.out.println("\n=== Текущее состояние ===");
        System.out.println("Статус сервера: " + (server.isServerRunning() ? "Запущен" : "Остановлен"));
        System.out.println("Состояние сервера: " + (server.isServerFull() ? "Заполнен" : "Есть свободные места"));
        System.out.println("Игроков на сервере: " + server.getCurrentPlayers() + "/4");
        System.out.println("Игроков в очереди: " + server.getQueueSize());
        
        List<String> activePlayers = server.getActivePlayers();
        if (!activePlayers.isEmpty()) {
            System.out.println("\nАктивные игроки на сервере:");
            for (int i = 0; i < activePlayers.size(); i++) {
                System.out.println((i + 1) + ". " + activePlayers.get(i));
            }
        }
        System.out.println("=======================\n");
    }
    
    /**
     * Получение целочисленного ввода от пользователя
     */
    private static int getIntInput(String prompt) {
        while (true) {
            try {
                System.out.print(prompt);
                return Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Пожалуйста, введите число.");
            }
        }
    }

    /**
     * Продолжить обработку очереди
     */
    private static void continueQueue(GameServer server) {
        server.continueQueue();
    }
}