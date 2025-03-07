package com.kikuzawa.laboratory_1;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.TextFormatter;

import java.util.*;

/**
 * Контроллер для работы с вычислениями в конечном поле.
 * Обрабатывает математические выражения и выполняет операции по модулю.
 */
public class HelloController {

    // UI компоненты для взаимодействия с пользователем
    @FXML
    public TextField exBpx; // Поле для ввода математического выражения
    @FXML
    public TextField modBox; // Поле для ввода модуля вычислений
    @FXML
    public TextArea logBox; // Текстовое поле для отображения логов вычислений
    @FXML
    public TextField resultBox; // Поле для вывода результата вычисления
    @FXML
    public Button runButton; // Кнопка запуска вычислений

    /**
     * Инициализация контроллера и настройка обработчиков событий.
     */
    @FXML
    public void initialize() {
        // Добавляем фильтр для поля exBpx
        exBpx.setTextFormatter(new TextFormatter<>(change -> {
            if (change.getText().contains("^")) {
                return null; // Отклоняем изменение, если введен символ ^
            }
            return change;
        }));

        // Добавляем фильтр для поля modBox
        modBox.setTextFormatter(new TextFormatter<>(change -> {
            if (change.getText().contains("^")) {
                return null; // Отклоняем изменение, если введен символ ^
            }
            return change;
        }));

        // Добавляем обработчик события для кнопки "Выполнить"
        runButton.setOnAction(event -> {
            try {
                // Очищаем лог перед началом новых вычислений
                logBox.clear();

                // Получаем выражение и модуль из текстовых полей
                String expression = exBpx.getText().trim();
                int mod = Integer.parseInt(modBox.getText().trim());

                // Проверяем, является ли модуль простым числом
                if (!isPrime(mod)) {
                    logBox.appendText("Ошибка: Модуль должен быть простым числом.\n\n");
                    return; // Прерываем выполнение, если модуль не простой
                }

                // Логируем входные данные для отладки
                logBox.appendText("Введенное выражение: " + expression + "\n");
                logBox.appendText("Модуль: " + mod + "\n\n");

                // Вычисляем результат выражения в поле
                int result = evaluateExpression(expression, mod);

                // Выводим результат в поле результата
                resultBox.setText(String.valueOf(result));

                // Логируем итоговый результат
                logBox.appendText("-------------------------------------------\n");
                logBox.appendText("Итоговый результат: " + result + "\n\n");
            } catch (NumberFormatException e) {
                logBox.appendText("Ошибка: Некорректный ввод модуля.\n\n");
            } catch (ArithmeticException e) {
                logBox.appendText("Ошибка: " + e.getMessage() + "\n\n");
            } catch (Exception e) {
                logBox.appendText("Ошибка: " + e.getMessage() + "\n\n");
            }
        });
    }

    /**
     * Вычисляет математическое выражение в конечном поле по модулю mod.
     * Использует алгоритм парсинга с помощью двух стеков для чисел и операторов.
     *
     * @param expression выражение для вычисления
     * @param mod       модуль вычислений
     * @return результат вычисления
     */
    private int evaluateExpression(String expression, int mod) {
        Stack<Integer> values = new Stack<>();  // Стек для хранения чисел
        Stack<Character> ops = new Stack<>();    // Стек для хранения операторов
        char[] tokens = expression.toCharArray(); // Разбиваем выражение на токены

        // Обрабатываем каждый символ в выражении
        for (int i = 0; i < tokens.length; i++) {
            if (tokens[i] == ' ') continue;

            // Обработка чисел
            if (tokens[i] >= '0' && tokens[i] <= '9') {
                StringBuilder sb = new StringBuilder();
                while (i < tokens.length && tokens[i] >= '0' && tokens[i] <= '9')
                    sb.append(tokens[i++]);
                int num = Integer.parseInt(sb.toString()) % mod;
                values.push(num);
                logBox.appendText("Добавлено число в стек: " + num + "\n");
                i--;
            }

            // Обработка скобок и операторов
            else if (tokens[i] == '(') {
                ops.push(tokens[i]);
                logBox.appendText("Добавлена открывающая скобка в стек операций\n");
            }
            else if (tokens[i] == ')') {
                while (ops.peek() != '(') {
                    char op = ops.pop();
                    logBox.appendText("Обрабатываемая операция: " + op + "\n");
                    values.push(applyOp(op, values.pop(), values.pop(), mod));
                }
                ops.pop(); // Убираем '(' из стека
                logBox.appendText("Убрана открывающая скобка из стека операций\n");
            }
            else if (tokens[i] == '+' || tokens[i] == '-' ||
                    tokens[i] == '*' || tokens[i] == '/') {
                while (!ops.empty() && hasPrecedence(tokens[i], ops.peek())) {
                    char op = ops.pop();
                    logBox.appendText("Обрабатываемая операция: " + op + "\n");
                    values.push(applyOp(op, values.pop(), values.pop(), mod));
                }
                ops.push(tokens[i]);
                logBox.appendText("Добавлена операция в стек: " + tokens[i] + "\n");
            }
        }

        // Обработка оставшихся операторов
        while (!ops.empty()) {
            char op = ops.pop();
            logBox.appendText("Обрабатываемая операция: " + op + "\n");
            values.push(applyOp(op, values.pop(), values.pop(), mod));
        }

        // Получаем финальный результат
        int result = values.pop();
        logBox.appendText("Результат вычисления: " + result + "\n");
        return result;
    }

    /**
     * Находит обратный элемент числа в конечном поле по модулю mod.
     * Использует расширенный алгоритм Евклида для нахождения мультипликативного обратного.
     *
     * @param a    число, для которого ищем обратное
     * @param mod  модуль поля
     * @return     обратный элемент или 0 если он не существует
     */
    public int inverse(int a, int mod) {
        if (mod == 0) {
            logBox.appendText("Ошибка: Модуль не может быть равен 0.\n");
            throw new ArithmeticException("Модуль не может быть равен 0.");
        }

        logBox.appendText("\n====== НАЧАЛО ВЫЧИСЛЕНИЯ ОБРАТНОГО ЭЛЕМЕНТА ======\n");
        logBox.appendText("Ищем x такой, что (" + a + " * x) ≡ 1 mod " + mod + "\n");

        int m0 = mod;
        int t, q;
        int x0 = 0, x1 = 1;

        logBox.appendText("Инициализация:\n");
        logBox.appendText("m0 = " + m0 + ", x0 = " + x0 + ", x1 = " + x1 + "\n");

        // Специальный случай для модуля 1
        if (mod == 1) {
            logBox.appendText("Модуль равен 1, возвращаем 0\n");
            logBox.appendText("====== КОНЕЦ ВЫЧИСЛЕНИЯ ======\n\n");
            return 0;
        }

        int step = 1;
        // Реализация расширенного алгоритма Евклида
        while (a > 1) {
            logBox.appendText("\n--- Шаг " + step++ + " ---");
            logBox.appendText("\na = " + a + ", mod = " + mod);

            q = a / mod; // Находим частное
            logBox.appendText("\nВычисляем q = a / mod = " + q);

            t = mod; // Сохраняем текущий mod
            mod = a % mod; // Обновляем mod
            a = t; // Обновляем a
            logBox.appendText("\nОбмен значений: новый a = " + a + ", новый mod = " + mod);

            t = x0;
            x0 = x1 - q * x0; // Вычисляем новое x0
            x1 = t; // Обновляем x1
            logBox.appendText("\nОбновляем коэффициенты: x0 = x1 - q*x0 = " + x0 + ", x1 = " + x1);
        }

        logBox.appendText("\n\nВыход из цикла, a = " + a);
        if (x1 < 0) {
            logBox.appendText("\nКорректируем x1 (" + x1 + ") путем добавления m0: ");
            x1 += m0;
            logBox.appendText("новый x1 = " + x1);
        }

        logBox.appendText("\nОбратный элемент: " + x1);
        logBox.appendText("\nПроверка: (" + a + " * " + x1 + ") mod " + m0 + " = " + (a * x1 % m0));
        logBox.appendText("\n====== КОНЕЦ ВЫЧИСЛЕНИЯ ======\n\n");

        return x1;
    }

    /**
     * Определяет приоритет операторов для правильного порядка вычислений.
     *
     * @param op1 первая операция
     * @param op2 вторая операция
     * @return true если op1 имеет приоритет над op2
     */
    public static boolean hasPrecedence(char op1, char op2) {
        if (op2 == '(' || op2 == ')')
            return false;
        if ((op1 == '*' || op1 == '/') && (op2 == '+' || op2 == '-'))
            return false;
        return true;
    }

    // Функция для применения операций
    public int applyOp(char op, int b, int a, int mod) {
        int result = 0;
        switch (op) {
            case '+':
                result = (a + b) % mod;
                break;
            case '-':
                result = (a - b + mod) % mod;
                break;
            case '*':
                result = (a * b) % mod;
                break;
            case '/':
                if (b == 0) {
                    logBox.setText("Ошибка: Деление на ноль невозможно.\n");
                    resultBox.setText("Ошибка");
                    throw new ArithmeticException("Деление на ноль невозможно.");
                }
                int inv = inverse(b, mod);
                result = (a * inv) % mod;
                break;
        }
        logBox.appendText("Применена операция: " + a + " " + op + " " + b + " = " + result + " (mod " + mod + ")\n");
        return result;
    }

    /**
     * Проверяет, является ли число простым.
     *
     * @param n число для проверки
     * @return true, если число простое, иначе false
     */
    private boolean isPrime(int n) {
        if (n <= 1) {
            return false;
        }
        if (n <= 3) {
            return true;
        }
        if (n % 2 == 0 || n % 3 == 0) {
            return false;
        }
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) {
                return false;
            }
        }
        return true;
    }


}