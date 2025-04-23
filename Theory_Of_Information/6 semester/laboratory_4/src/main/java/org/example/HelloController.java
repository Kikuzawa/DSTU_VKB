package org.example;

import java.io.File;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Random;
import java.util.Set;

import javafx.beans.property.SimpleIntegerProperty;
import javafx.collections.FXCollections;
import javafx.collections.ListChangeListener;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleGroup;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.stage.FileChooser;
import javafx.util.converter.IntegerStringConverter;

// Контроллер для управления интерфейсом циклического кода
public class HelloController {
    // Элементы интерфейса для ввода полинома
    @FXML
    private RadioButton polynomialInput;
    @FXML
    private RadioButton matrixInput;
    @FXML
    private TextField polynomialField;
    @FXML
    private TextField nParameterField;
    
    // Таблицы для отображения матриц
    @FXML
    private TableView<int[]> generatorMatrixTable;
    @FXML
    private TableView<int[]> parityCheckMatrixTable;
    
    // Текстовые области для ввода/вывода
    @FXML
    private TextArea inputText;
    @FXML
    private TextArea outputText;
    
    // Кнопки управления
    @FXML
    private Button initButton;
    @FXML
    private Button encodeButton;
    @FXML
    private Button decodeButton;
    @FXML
    private Button loadFileButton;
    @FXML
    private Button addRowButton;
    @FXML
    private Button removeRowButton;
    
    // Таблица синдромов
    @FXML
    private TableView<int[]> syndromeTable;
    
    // Области для вывода логов
    @FXML
    private TextArea errorCorrectionSteps;
    @FXML
    private TextArea processLog;
    
    // Флаги обработки
    @FXML
    private CheckBox blockProcessingCheckBox;
    @FXML
    private CheckBox randomErrorsCheckBox;
    @FXML
    private CheckBox detailedLoggingCheckBox;
    
    // Внутренние переменные
    private ToggleGroup inputTypeGroup;
    private CyclicCode cyclicCode;
    private ObservableList<int[]> matrixData;
    private ObservableList<int[]> syndromeData;
    private Random random = new Random();
    private long startTime;
    private long endTime;

    // Инициализация контроллера
    @FXML
    public void initialize() {
        // Инициализация данных матриц
        matrixData = FXCollections.observableArrayList();
        syndromeData = FXCollections.observableArrayList();
        generatorMatrixTable.setItems(matrixData);
        syndromeTable.setItems(syndromeData);
        
        // Настройка столбцов таблиц
        setupMatrixColumns(generatorMatrixTable);
        setupMatrixColumns(parityCheckMatrixTable);
        setupSyndromeTable();
        
        // Настройка переключателя типа ввода
        inputTypeGroup = new ToggleGroup();
        polynomialInput.setToggleGroup(inputTypeGroup);
        matrixInput.setToggleGroup(inputTypeGroup);
        
        // Обработчик изменения типа ввода
        inputTypeGroup.selectedToggleProperty().addListener((obs, oldVal, newVal) -> {
            updateInputEditability();
        });
        
        // Обработчик изменения параметра n
        nParameterField.textProperty().addListener((obs, oldVal, newVal) -> {
            if (!newVal.isEmpty() && matrixInput.isSelected()) {
                try {
                    int n = Integer.parseInt(newVal);
                    updateMatrixColumns(n);
                } catch (NumberFormatException e) {
                    // Игнорируем некорректный ввод
                }
            }
        });
        
        // Обработчик изменений в матрице
        matrixData.addListener((ListChangeListener<int[]>) change -> {
            if (matrixInput.isSelected() && !matrixData.isEmpty()) {
                updatePolynomialFromMatrix();
            }
        });
        
        // Начальная настройка доступности элементов
        updateInputEditability();
        
        // Отключаем кнопки кодирования/декодирования до инициализации
        encodeButton.setDisable(true);
        decodeButton.setDisable(true);
    }

    // Настройка столбцов таблицы матрицы
    private void setupMatrixColumns(TableView<int[]> table) {
        table.getColumns().clear();
        int columnCount = 7; // Значение по умолчанию
        if (cyclicCode != null) {
            columnCount = cyclicCode.getN();
        }
        
        for (int i = 0; i < columnCount; i++) {
            final int columnIndex = i;
            TableColumn<int[], Integer> column = new TableColumn<>(String.valueOf(i));
            column.setPrefWidth(40);
            column.setMinWidth(40);
            column.setMaxWidth(40);
            column.setCellValueFactory(cellData -> {
                int[] row = cellData.getValue();
                if (row != null && columnIndex < row.length) {
                    return new SimpleIntegerProperty(row[columnIndex]).asObject();
                }
                return new SimpleIntegerProperty(0).asObject();
            });
            
            // Делаем ячейки редактируемыми
            column.setCellFactory(TextFieldTableCell.forTableColumn(new IntegerStringConverter()));
            column.setOnEditCommit(event -> {
                int[] row = event.getRowValue();
                if (row != null && columnIndex < row.length) {
                    row[columnIndex] = event.getNewValue();
                    if (matrixInput.isSelected()) {
                        updatePolynomialFromMatrix();
                    }
                }
            });
            
            table.getColumns().add(column);
        }
        table.setFixedCellSize(40);
        table.setEditable(true);
    }

    // Настройка таблицы синдромов
    private void setupSyndromeTable() {
        syndromeTable.getColumns().clear();
        
        // Столбец для позиции ошибки
        TableColumn<int[], Integer> positionColumn = new TableColumn<>("Позиция");
        positionColumn.setPrefWidth(60);
        positionColumn.setMinWidth(60);
        positionColumn.setMaxWidth(60);
        positionColumn.setCellValueFactory(cellData -> 
            new SimpleIntegerProperty(cellData.getValue()[0]).asObject());
        syndromeTable.getColumns().add(positionColumn);
        
        // Определяем количество символов в синдроме
        int syndromeLength = 3; // Значение по умолчанию
        if (cyclicCode != null) {
            syndromeLength = cyclicCode.getN() - cyclicCode.getK();
        }
        
        // Столбцы для синдрома
        for (int i = 0; i < syndromeLength; i++) {
            final int columnIndex = i + 1;
            TableColumn<int[], Integer> column = new TableColumn<>("S" + i);
            column.setPrefWidth(40);
            column.setMinWidth(40);
            column.setMaxWidth(40);
            column.setCellValueFactory(cellData -> 
                new SimpleIntegerProperty(cellData.getValue()[columnIndex]).asObject());
            syndromeTable.getColumns().add(column);
        }
        
        syndromeTable.setFixedCellSize(40);
        log("Таблица синдромов настроена с " + syndromeLength + " столбцами синдрома");
    }

    // Обновление столбцов матрицы при изменении n
    private void updateMatrixColumns(int n) {
        generatorMatrixTable.getColumns().clear();
        for (int i = 0; i < n; i++) {
            final int columnIndex = i;
            TableColumn<int[], Integer> column = new TableColumn<>(String.valueOf(i));
            column.setCellValueFactory(cellData -> 
                new SimpleIntegerProperty(cellData.getValue()[columnIndex]).asObject());
            
            // Делаем ячейки редактируемыми
            column.setCellFactory(TextFieldTableCell.forTableColumn(new IntegerStringConverter()));
            column.setOnEditCommit(event -> {
                int[] row = event.getRowValue();
                row[columnIndex] = event.getNewValue();
                if (matrixInput.isSelected()) {
                    updatePolynomialFromMatrix();
                }
            });
            
            generatorMatrixTable.getColumns().add(column);
        }
        
        // Обновляем существующие строки под новое количество столбцов
        for (int i = 0; i < matrixData.size(); i++) {
            int[] row = matrixData.get(i);
            int[] newRow = new int[n];
            System.arraycopy(row, 0, newRow, 0, Math.min(row.length, n));
            matrixData.set(i, newRow);
        }
    }

    // Обновление полинома из матрицы
    private void updatePolynomialFromMatrix() {
        if (matrixData.isEmpty()) return;
        
        try {
            int[][] matrix = matrixData.toArray(new int[0][]);
            CyclicCode tempCode = new CyclicCode(matrix);
            Polynomial g = tempCode.getGeneratorPolynomial();
            polynomialField.setText(g.toString());
        } catch (Exception e) {
            log("Ошибка при обновлении полинома из матрицы: " + e.getMessage());
        }
    }

    // Обновление доступности элементов ввода
    private void updateInputEditability() {
        boolean isPolynomialInput = polynomialInput.isSelected();
        
        // Устанавливаем доступность для ввода полинома
        polynomialField.setEditable(isPolynomialInput);
        nParameterField.setEditable(isPolynomialInput);
        
        // Устанавливаем доступность для ввода матрицы
        generatorMatrixTable.setEditable(!isPolynomialInput);
        addRowButton.setDisable(isPolynomialInput);
        removeRowButton.setDisable(isPolynomialInput);
        
        // Визуальная обратная связь для отключенного состояния
        polynomialField.setStyle(isPolynomialInput ? "" : "-fx-opacity: 0.7;");
        nParameterField.setStyle(isPolynomialInput ? "" : "-fx-opacity: 0.7;");
        generatorMatrixTable.setStyle(!isPolynomialInput ? "" : "-fx-opacity: 0.7;");
    }

    // Запуск таймера
    private void startTimer() {
        startTime = System.nanoTime();
    }

    // Остановка таймера
    private void stopTimer() {
        endTime = System.nanoTime();
    }

    // Получение прошедшего времени
    private String getElapsedTime() {
        long elapsedNanos = endTime - startTime;
        return String.format("%.3f мс", elapsedNanos / 1_000_000.0);
    }

    // Логирование подробной информации
    private void logDetailed(String message) {
        if (detailedLoggingCheckBox.isSelected()) {
            log(message);
        }
    }

    // Обработчик нажатия кнопки инициализации
    @FXML
    protected void onInitButtonClick() {
        try {
            startTimer();
            if (polynomialInput.isSelected()) {
                // Инициализация из полинома
                String polynomialStr = polynomialField.getText().trim();
                int n = Integer.parseInt(nParameterField.getText().trim());
                
                if (polynomialStr.isEmpty()) {
                    throw new IllegalArgumentException("Полином не может быть пустым");
                }
                
                log("Инициализация циклического кода с полиномом: " + polynomialStr);
                log("Параметр n: " + n);
                
                Polynomial g = Polynomial.fromString(polynomialStr);
                logDetailed("Распознанные коэффициенты полинома: " + Arrays.toString(g.getCoefficients()));
                logDetailed("Степень порождающего полинома: " + g.getDegree());
                
                cyclicCode = new CyclicCode(g, n);
                log("Циклический код успешно инициализирован");
                
                // Обновление таблицы порождающей матрицы
                matrixData.clear();
                int[][] generatorMatrix = cyclicCode.getGeneratorMatrix();
                logDetailed("\nГенерация порождающей матрицы:");
                for (int i = 0; i < generatorMatrix.length; i++) {
                    logDetailed("Строка " + i + ": " + Arrays.toString(generatorMatrix[i]));
                    matrixData.add(generatorMatrix[i]);
                }
                log("Порождающая матрица обновлена");
            } else {
                // Инициализация из матрицы
                if (matrixData.isEmpty()) {
                    throw new IllegalArgumentException("Порождающая матрица не может быть пустой");
                }
                
                log("Инициализация циклического кода из порождающей матрицы");
                int[][] generatorMatrix = matrixData.toArray(new int[0][]);
                logDetailed("\nВходная порождающая матрица:");
                for (int i = 0; i < generatorMatrix.length; i++) {
                    logDetailed("Строка " + i + ": " + Arrays.toString(generatorMatrix[i]));
                }
                
                cyclicCode = new CyclicCode(generatorMatrix);
                log("Циклический код успешно инициализирован");
            }
            
            // Обновление проверочной матрицы
            logDetailed("\n=== Получение проверочной матрицы ===");
            logDetailed("1. Получаем порождающий полином g(x):");
            Polynomial g = cyclicCode.getGeneratorPolynomial();
            logDetailed("   g(x) = " + g);
            logDetailed("   Коэффициенты: " + Arrays.toString(g.getCoefficients()));
            
            logDetailed("\n2. Находим проверочный полином h(x):");
            logDetailed("   h(x) = (x^n - 1) / g(x)");
            logDetailed("   где n = " + cyclicCode.getN());
            Polynomial h = cyclicCode.getParityCheckPolynomial();
            logDetailed("   h(x) = " + h);
            logDetailed("   Коэффициенты: " + Arrays.toString(h.getCoefficients()));
            
            logDetailed("\n3. Строим проверочную матрицу H:");
            logDetailed("   H имеет размер (n-k) x n = " + (cyclicCode.getN() - cyclicCode.getK()) + " x " + cyclicCode.getN());
            logDetailed("   Строки H - это циклические сдвиги проверочного полинома");
            
            int[][] parityCheckMatrix = cyclicCode.getParityCheckMatrix();
            logDetailed("\nПолученная проверочная матрица:");
            for (int i = 0; i < parityCheckMatrix.length; i++) {
                logDetailed("Строка " + i + ": " + Arrays.toString(parityCheckMatrix[i]));
            }
            
            parityCheckMatrixTable.getItems().clear();
            for (int[] row : parityCheckMatrix) {
                parityCheckMatrixTable.getItems().add(row);
            }
            log("Проверочная матрица обновлена");
            
            // Обновление таблицы синдромов
            updateSyndromeTable();
            log("Таблица синдромов обновлена");
            
            // Включаем кнопки кодирования/декодирования
            encodeButton.setDisable(false);
            decodeButton.setDisable(false);
            
            stopTimer();
            log("\nИнициализация циклического кода успешно завершена");
            log("Общее время инициализации: " + getElapsedTime());
        } catch (Exception e) {
            showError("Ошибка инициализации", e.getMessage());
            log("Ошибка при инициализации: " + e.getMessage());
        }
    }

    // Обновление таблицы синдромов
    private void updateSyndromeTable() {
        if (cyclicCode == null) return;
        
        syndromeData.clear();
        int n = cyclicCode.getN();
        int syndromeLength = n - cyclicCode.getK();
        
        // Перестраиваем столбцы таблицы синдромов
        syndromeTable.getColumns().clear();
        
        // Столбец для позиции ошибки
        TableColumn<int[], Integer> positionColumn = new TableColumn<>("Позиция");
        positionColumn.setPrefWidth(60);
        positionColumn.setMinWidth(60);
        positionColumn.setMaxWidth(60);
        positionColumn.setCellValueFactory(cellData -> 
            new SimpleIntegerProperty(cellData.getValue()[0]).asObject());
        syndromeTable.getColumns().add(positionColumn);
        
        // Столбцы для синдрома
        for (int i = 0; i < syndromeLength; i++) {
            final int columnIndex = i + 1;
            TableColumn<int[], Integer> column = new TableColumn<>("S" + i);
            column.setPrefWidth(40);
            column.setMinWidth(40);
            column.setMaxWidth(40);
            column.setCellValueFactory(cellData -> 
                new SimpleIntegerProperty(cellData.getValue()[columnIndex]).asObject());
            syndromeTable.getColumns().add(column);
        }
        
        // Заполняем таблицу синдромами
        for (int i = 0; i < n; i++) {
            int[] error = new int[n];
            error[i] = 1;
            int[] syndrome = cyclicCode.calculateSyndrome(error);
            
            int[] row = new int[syndromeLength + 1];
            row[0] = i;
            System.arraycopy(syndrome, 0, row, 1, syndromeLength);
            syndromeData.add(row);
        }
        
        log("Таблица синдромов обновлена с " + syndromeLength + " символами синдрома");
    }

    // Обработчик добавления строки в матрицу
    @FXML
    protected void onAddRowButtonClick() {
        int[] newRow = new int[7];
        matrixData.add(newRow);
        log("Добавлена новая строка в порождающую матрицу");
    }

    // Обработчик удаления строки из матрицы
    @FXML
    protected void onRemoveRowButtonClick() {
        if (!matrixData.isEmpty()) {
            matrixData.remove(matrixData.size() - 1);
            log("Удалена последняя строка из порождающей матрицы");
        }
    }

    // Обработчик загрузки файла
    @FXML
    protected void onLoadFileButtonClick() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Выберите входной файл");
        File file = fileChooser.showOpenDialog(null);
        if (file != null) {
            try {
                String content = new String(Files.readAllBytes(file.toPath()), StandardCharsets.UTF_8);
                inputText.setText(content);
                log("Файл успешно загружен: " + file.getName());
                log("Содержимое файла: " + content);
            } catch (IOException e) {
                showError("Ошибка загрузки файла", e.getMessage());
                log("Ошибка при загрузке файла: " + e.getMessage());
            }
        }
    }

    // Получение матрицы из таблицы
    private int[][] getMatrixFromTable(TableView<int[]> table) {
        ObservableList<int[]> data = table.getItems();
        int[][] matrix = new int[data.size()][];
        for (int i = 0; i < data.size(); i++) {
            matrix[i] = data.get(i);
        }
        return matrix;
    }

    // Обновление таблицы матрицы
    private void updateMatrixTable(TableView<int[]> table, int[][] matrix) {
        ObservableList<int[]> data = FXCollections.observableArrayList();
        for (int[] row : matrix) {
            data.add(row);
        }
        table.setItems(data);
    }

    // Парсинг входных данных
    private int[] parseInput(String input) {
        // Удаляем все пробелы
        input = input.replaceAll("\\s+", "");
        
        // Проверяем, является ли вход бинарной строкой
        if (input.matches("[01]+")) {
            int[] result = new int[input.length()];
            for (int i = 0; i < input.length(); i++) {
                result[i] = input.charAt(i) - '0';
            }
            return result;
        }
        
        // Если не бинарная строка, конвертируем текст в бинарную строку
        StringBuilder binaryString = new StringBuilder();
        for (char c : input.toCharArray()) {
            String binary = Integer.toBinaryString(c);
            binary = String.format("%8s", binary).replace(' ', '0');
            binaryString.append(binary);
        }
        
        int[] result = new int[binaryString.length()];
        for (int i = 0; i < binaryString.length(); i++) {
            result[i] = binaryString.charAt(i) - '0';
        }
        return result;
    }

    // Форматирование выходных данных
    private String formatOutput(int[] bits) {
        StringBuilder result = new StringBuilder();
        for (int bit : bits) {
            result.append(bit);
        }
        return result.toString();
    }

    // Обработка блоков данных
    private int[] processBlocks(int[] input, boolean isEncoding) {
        if (!blockProcessingCheckBox.isSelected()) {
            return input;
        }

        int blockSize = isEncoding ? cyclicCode.getK() : cyclicCode.getN();
        int totalBlocks = (int) Math.ceil((double) input.length / blockSize);
        int[] result = new int[totalBlocks * (isEncoding ? cyclicCode.getN() : cyclicCode.getK())];
        
        log("Обработка блоками:");
        log("  - Размер блока: " + blockSize);
        log("  - Количество блоков: " + totalBlocks);

        for (int i = 0; i < totalBlocks; i++) {
            int start = i * blockSize;
            int end = Math.min(start + blockSize, input.length);
            int[] block = new int[blockSize];
            System.arraycopy(input, start, block, 0, end - start);
            
            log("  Блок " + (i + 1) + ":");
            log("    - Начальная позиция: " + start);
            log("    - Конечная позиция: " + end);
            log("    - Данные блока: " + Arrays.toString(block));

            int[] processedBlock;
            if (isEncoding) {
                processedBlock = cyclicCode.encode(block);
                log("    - Закодированный блок: " + Arrays.toString(processedBlock));
            } else {
                processedBlock = cyclicCode.decode(block);
                log("    - Декодированный блок: " + Arrays.toString(processedBlock));
            }

            System.arraycopy(processedBlock, 0, result, i * processedBlock.length, processedBlock.length);
        }

        return result;
    }

    // Внесение случайных ошибок
    private int[] introduceRandomErrors(int[] codeword) {
        int[] corrupted = codeword.clone();
        
        // Для циклического кода (7,4) максимальное количество исправляемых ошибок - 1
        int maxCorrectableErrors = 1;
        int errorCount = random.nextInt(maxCorrectableErrors) + 1;
        
        log("\nВносятся случайные ошибки:");
        log("Количество ошибок: " + errorCount);
        log("Максимальное количество исправляемых ошибок: " + maxCorrectableErrors);
        
        // Генерируем уникальные позиции для ошибок
        Set<Integer> errorPositions = new HashSet<>();
        while (errorPositions.size() < errorCount) {
            int position = random.nextInt(codeword.length);
            errorPositions.add(position);
        }
        
        // Вносим ошибки в выбранные позиции
        for (int position : errorPositions) {
            corrupted[position] = 1 - corrupted[position];
            log("Ошибка в позиции " + position + ": " + codeword[position] + " -> " + corrupted[position]);
        }
        
        log("Искаженное сообщение: " + Arrays.toString(corrupted));
        return corrupted;
    }

    // Конвертация бинарной строки в ASCII
    private String binaryToAscii(String binary) {
        int byteCount = binary.length() / 8;
        byte[] bytes = new byte[byteCount];
        for (int i = 0; i < byteCount; i++) {
            String byteStr = binary.substring(i * 8, (i + 1) * 8);
            bytes[i] = (byte) Integer.parseInt(byteStr, 2);
        }
        return new String(bytes, StandardCharsets.UTF_8);
    }

    // Обработчик кодирования
    @FXML
    protected void onEncodeButtonClick() {
        try {
            startTimer();
            String messageStr = inputText.getText().trim();
            if (messageStr.isEmpty()) {
                throw new IllegalArgumentException("Сообщение не может быть пустым");
            }
            
            log("\nНачало процесса кодирования");
            log("Входной текст: " + messageStr);
            
            // Конвертация текста в бинарную строку
            byte[] messageBytes = messageStr.getBytes(StandardCharsets.UTF_8);
            StringBuilder binaryString = new StringBuilder();
            logDetailed("\nКонвертация текста в бинарную строку (UTF-8):");
            for (int i = 0; i < messageBytes.length; i++) {
                int val = messageBytes[i] & 0xFF;
                String binary = String.format("%8s", Integer.toBinaryString(val)).replace(' ', '0');
                binaryString.append(binary);
                logDetailed("Байт " + i + ": " + val + " -> Бинарный " + binary);
            }
            
            // Конвертация бинарной строки в массив целых чисел
            int[] message = new int[binaryString.length()];
            for (int i = 0; i < binaryString.length(); i++) {
                message[i] = binaryString.charAt(i) - '0';
            }
            log("Бинарное сообщение: " + binaryString);
            
            if (blockProcessingCheckBox.isSelected()) {
                // Обработка блоками
                int blockSize = cyclicCode.getK();
                StringBuilder encodedMessage = new StringBuilder();
                log("\nНачало блочного кодирования с размером блока: " + blockSize);
                
                for (int i = 0; i < message.length; i += blockSize) {
                    int[] block = Arrays.copyOfRange(message, i, Math.min(i + blockSize, message.length));
                    logDetailed("\nКодирование блока " + (i/blockSize + 1) + ":");
                    logDetailed("Исходный блок: " + Arrays.toString(block));
                    
                    int[] codeword = cyclicCode.encode(block);
                    logDetailed("Закодированный блок: " + Arrays.toString(codeword));
                    
                    // Внесение случайных ошибок, если выбрано
                    if (randomErrorsCheckBox.isSelected()) {
                        codeword = introduceRandomErrors(codeword);
                    }
                    
                    for (int bit : codeword) {
                        encodedMessage.append(bit);
                    }
                }
                
                String encodedBinary = encodedMessage.toString();
                outputText.setText(encodedBinary);
                
                log("\nИтоговое закодированное сообщение:");
                log("Бинарный вид: " + encodedBinary);
                logDetailed("Текстовое представление:");
                String asciiRepresentation = binaryToAscii(encodedBinary);
                logDetailed("Текст: " + asciiRepresentation);
                for (int i = 0; i < encodedBinary.length(); i += 8) {
                    if (i + 8 <= encodedBinary.length()) {
                        String byteStr = encodedBinary.substring(i, i + 8);
                        int ascii = Integer.parseInt(byteStr, 2);
                        logDetailed("Байт " + (i/8 + 1) + ": " + byteStr + " -> ASCII " + ascii + " -> Символ '" + (char)ascii + "'");
                    }
                }
            } else {
                // Обработка всего сообщения целиком
                int[] codeword = cyclicCode.encode(message);
                
                // Внесение случайных ошибок, если выбрано
                if (randomErrorsCheckBox.isSelected()) {
                    codeword = introduceRandomErrors(codeword);
                }
                
                log("\nКодирование завершено:");
                log("Исходное сообщение: " + Arrays.toString(message));
                logDetailed("Закодированное слово: " + Arrays.toString(codeword));
                
                StringBuilder binaryOutput = new StringBuilder();
                for (int bit : codeword) {
                    binaryOutput.append(bit);
                }
                outputText.setText(binaryOutput.toString());
                
                log("\nИтоговое закодированное сообщение:");
                log("Бинарный вид: " + binaryOutput);
                logDetailed("Текстовое представление:");
                String asciiRepresentation = binaryToAscii(binaryOutput.toString());
                logDetailed("Текст: " + asciiRepresentation);
                for (int i = 0; i < binaryOutput.length(); i += 8) {
                    if (i + 8 <= binaryOutput.length()) {
                        String byteStr = binaryOutput.substring(i, i + 8);
                        int ascii = Integer.parseInt(byteStr, 2);
                        logDetailed("Байт " + (i/8 + 1) + ": " + byteStr + " -> ASCII " + ascii + " -> Символ '" + (char)ascii + "'");
                    }
                }
            }
            
            stopTimer();
            log("Общее время кодирования: " + getElapsedTime());
        } catch (Exception e) {
            showError("Ошибка кодирования", e.getMessage());
            log("Ошибка при кодировании: " + e.getMessage());
        }
    }

    // Обработчик декодирования
    @FXML
    protected void onDecodeButtonClick() {
        try {
            startTimer();
            String codewordStr = inputText.getText().trim();
            if (codewordStr.isEmpty()) {
                throw new IllegalArgumentException("Кодовое слово не может быть пустым");
            }
            
            log("\nНачало процесса декодирования");
            log("Входное кодовое слово: " + codewordStr);
            
            // Конвертация бинарной строки в массив целых чисел
            int[] codeword = new int[codewordStr.length()];
            for (int i = 0; i < codewordStr.length(); i++) {
                codeword[i] = codewordStr.charAt(i) - '0';
            }
            
            if (blockProcessingCheckBox.isSelected()) {
                // Обработка блоками
                int blockSize = cyclicCode.getN();
                StringBuilder decodedMessage = new StringBuilder();
                log("\nНачало блочного декодирования с размером блока: " + blockSize);
                
                for (int i = 0; i < codeword.length; i += blockSize) {
                    int[] block = Arrays.copyOfRange(codeword, i, Math.min(i + blockSize, codeword.length));
                    logDetailed("\nДекодирование блока " + (i/blockSize + 1) + ":");
                    logDetailed("Полученный блок: " + Arrays.toString(block));
                    
                    // Отображение информации о декодировании
                    displayDecodingInfo(block);
                    
                    // Расчет синдрома
                    int[] syndrome = cyclicCode.calculateSyndrome(block);
                    logDetailed("Синдром: " + Arrays.toString(syndrome));
                    
                    // Проверка на наличие ошибок
                    boolean hasError = false;
                    for (int s : syndrome) {
                        if (s != 0) {
                            hasError = true;
                            break;
                        }
                    }
                    
                    if (hasError) {
                        logDetailed("Обнаружена ошибка в блоке " + (i/blockSize + 1));
                        logDetailed("Позиции ошибок: " + Arrays.toString(syndrome));
                    } else {
                        logDetailed("Ошибок в блоке " + (i/blockSize + 1) + " не обнаружено");
                    }
                    
                    int[] message = cyclicCode.decode(block);
                    logDetailed("Декодированный блок: " + Arrays.toString(message));
                    
                    for (int bit : message) {
                        decodedMessage.append(bit);
                    }
                }
                
                // Конвертация бинарной строки обратно в текст
                String binaryString = decodedMessage.toString();
                String resultText = binaryToAscii(binaryString);
                outputText.setText(resultText);
                log("\nИтоговое декодированное сообщение: " + resultText);
            } else {
                // Обработка всего сообщения целиком
                log("\nДекодирование одиночного блока:");
                logDetailed("Полученное кодовое слово: " + Arrays.toString(codeword));
                
                // Отображение информации о декодировании
                displayDecodingInfo(codeword);
                
                // Расчет синдрома
                int[] syndrome = cyclicCode.calculateSyndrome(codeword);
                logDetailed("Синдром: " + Arrays.toString(syndrome));
                
                // Проверка на наличие ошибок
                boolean hasError = false;
                for (int s : syndrome) {
                    if (s != 0) {
                        hasError = true;
                        break;
                    }
                }
                
                if (hasError) {
                    logDetailed("Обнаружена ошибка в кодовом слове");
                    logDetailed("Позиции ошибок: " + Arrays.toString(syndrome));
                } else {
                    logDetailed("Ошибок в кодовом слове не обнаружено");
                }
                
                int[] message = cyclicCode.decode(codeword);
                logDetailed("Декодированное сообщение: " + Arrays.toString(message));
                
                // Конвертация бинарной строки обратно в текст
                StringBuilder binaryStringBuilder = new StringBuilder();
                for (int bit : message) {
                    binaryStringBuilder.append(bit);
                }
                String resultText = binaryToAscii(binaryStringBuilder.toString());
                outputText.setText(resultText);
                log("\nИтоговое декодированное сообщение: " + resultText);
            }
            
            stopTimer();
            log("Общее время декодирования: " + getElapsedTime());
        } catch (Exception e) {
            showError("Ошибка декодирования", e.getMessage());
            log("Ошибка при декодировании: " + e.getMessage());
        }
    }

    // Обработчик очистки логов
    @FXML
    protected void onClearLogsButtonClick() {
        processLog.clear();
        errorCorrectionSteps.clear();
        log("Логи очищены");
    }

    // Поиск паттерна ошибки
    private int[] findErrorPattern(Polynomial syndrome) {
        int[] errorPattern = new int[cyclicCode.getN()];
        int[] syndromeCoeffs = syndrome.getCoefficients();
        
        if (syndromeCoeffs.length == 0) {
            log("  - Ошибки не обнаружены (синдром равен нулю)");
            return errorPattern;
        }
        
        log("  - Поиск паттерна ошибки...");
        for (int i = 0; i < cyclicCode.getN(); i++) {
            int[] testPattern = new int[cyclicCode.getN()];
            testPattern[i] = 1;
            Polynomial testSyndrome = new Polynomial(testPattern).mod(cyclicCode.getGeneratorPolynomial());
            if (Arrays.equals(testSyndrome.getCoefficients(), syndromeCoeffs)) {
                errorPattern[i] = 1;
                log("  - Ошибка найдена в позиции " + i);
                break;
            }
        }
        
        return errorPattern;
    }

    // Отображение информации о декодировании
    private void displayDecodingInfo(int[] received) {
        Polynomial receivedPoly = new Polynomial(received);
        Polynomial syndrome = receivedPoly.mod(cyclicCode.getGeneratorPolynomial());
        
        // Обновление информации о синдроме
        StringBuilder syndromeInfo = new StringBuilder();
        syndromeInfo.append("Синдром: ").append(syndrome).append("\n");
        syndromeInfo.append("Коэффициенты синдрома: ").append(Arrays.toString(syndrome.getCoefficients())).append("\n");
        syndromeInfo.append("Длина синдрома: ").append(syndrome.getDegree() + 1);
        
        // Подробное описание шагов исправления ошибок
        StringBuilder stepsInfo = new StringBuilder();
        stepsInfo.append("=== Процесс декодирования ===\n\n");
        
        // Шаг 1: Расчет синдрома
        stepsInfo.append("1. Расчет синдрома:\n");
        stepsInfo.append("   - Полученное слово: ").append(Arrays.toString(received)).append("\n");
        stepsInfo.append("   - Полином полученного слова: ").append(receivedPoly).append("\n");
        stepsInfo.append("   - Генераторный полином: ").append(cyclicCode.getGeneratorPolynomial()).append("\n");
        stepsInfo.append("   - Синдром = полученное слово mod генераторный полином\n");
        stepsInfo.append("   - Результат: ").append(syndrome).append("\n\n");
        
        // Шаг 2: Анализ синдрома
        stepsInfo.append("2. Анализ синдрома:\n");
        boolean hasError = false;
        for (int coeff : syndrome.getCoefficients()) {
            if (coeff != 0) {
                hasError = true;
                break;
            }
        }
        if (hasError) {
            stepsInfo.append("   - Обнаружена ошибка (синдром не равен нулю)\n");
            stepsInfo.append("   - Коэффициенты синдрома: ").append(Arrays.toString(syndrome.getCoefficients())).append("\n");
        } else {
            stepsInfo.append("   - Ошибок не обнаружено (синдром равен нулю)\n");
        }
        stepsInfo.append("\n");
        
        // Шаг 3: Поиск позиции ошибки
        stepsInfo.append("3. Поиск позиции ошибки:\n");
        if (hasError) {
            int[] errorPattern = findErrorPattern(syndrome);
            int errorPosition = -1;
            for (int i = 0; i < errorPattern.length; i++) {
                if (errorPattern[i] == 1) {
                    errorPosition = i;
                    break;
                }
            }
            if (errorPosition != -1) {
                stepsInfo.append("   - Ошибка найдена в позиции: ").append(errorPosition).append("\n");
                stepsInfo.append("   - Паттерн ошибки: ").append(Arrays.toString(errorPattern)).append("\n");
            } else {
                stepsInfo.append("   - Позиция ошибки не найдена\n");
            }
        } else {
            stepsInfo.append("   - Пропуск (ошибок не обнаружено)\n");
        }
        stepsInfo.append("\n");
        
        // Шаг 4: Исправление ошибки
        stepsInfo.append("4. Исправление ошибки:\n");
        if (hasError) {
            int[] corrected = received.clone();
            int[] errorPattern = findErrorPattern(syndrome);
            for (int i = 0; i < corrected.length; i++) {
                if (errorPattern[i] == 1) {
                    corrected[i] = 1 - corrected[i];
                }
            }
            stepsInfo.append("   - Исходное слово: ").append(Arrays.toString(received)).append("\n");
            stepsInfo.append("   - Исправленное слово: ").append(Arrays.toString(corrected)).append("\n");
        } else {
            stepsInfo.append("   - Пропуск (ошибок не обнаружено)\n");
        }
        stepsInfo.append("\n");
        
        // Шаг 5: Извлечение информационных битов
        stepsInfo.append("5. Извлечение информационных битов:\n");
        int k = cyclicCode.getK();
        int[] message = new int[k];
        if (hasError) {
            int[] corrected = received.clone();
            int[] errorPattern = findErrorPattern(syndrome);
            for (int i = 0; i < corrected.length; i++) {
                if (errorPattern[i] == 1) {
                    corrected[i] = 1 - corrected[i];
                }
            }
            System.arraycopy(corrected, 0, message, 0, k);
        } else {
            System.arraycopy(received, 0, message, 0, k);
        }
        stepsInfo.append("   - Информационные биты: ").append(Arrays.toString(message)).append("\n");
        
        errorCorrectionSteps.setText(stepsInfo.toString());
    }

    // Логирование сообщений
    private void log(String message) {
        processLog.appendText(message + "\n");
    }

    // Отображение ошибок
    private void showError(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
} 