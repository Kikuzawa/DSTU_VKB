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
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import javafx.util.converter.IntegerStringConverter;

public class HelloController {
    @FXML
    private RadioButton polynomialInput;
    @FXML
    private RadioButton matrixInput;
    @FXML
    private TextField polynomialField;
    @FXML
    private TextField nParameterField;
    @FXML
    private TableView<int[]> generatorMatrixTable;
    @FXML
    private TableView<int[]> parityCheckMatrixTable;
    @FXML
    private TextArea inputText;
    @FXML
    private TextArea outputText;
    @FXML
    private VBox polynomialInputBox;
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
    @FXML
    private TableView<int[]> syndromeTable;
    @FXML
    private TextArea errorCorrectionSteps;
    @FXML
    private TextArea processLog;
    @FXML
    private CheckBox blockProcessingCheckBox;
    @FXML
    private CheckBox randomErrorsCheckBox;
    @FXML
    private Button clearLogsButton;
    @FXML
    private CheckBox detailedLoggingCheckBox;

    private ToggleGroup inputTypeGroup;
    private CyclicCode cyclicCode;
    private ObservableList<int[]> matrixData;
    private ObservableList<int[]> syndromeData;
    private Random random = new Random();
    private long startTime;
    private long endTime;

    @FXML
    public void initialize() {
        // Initialize matrix data
        matrixData = FXCollections.observableArrayList();
        syndromeData = FXCollections.observableArrayList();
        generatorMatrixTable.setItems(matrixData);
        syndromeTable.setItems(syndromeData);
        
        // Setup matrix columns
        setupMatrixColumns(generatorMatrixTable);
        setupMatrixColumns(parityCheckMatrixTable);
        setupSyndromeTable();
        
        // Setup input type toggle
        inputTypeGroup = new ToggleGroup();
        polynomialInput.setToggleGroup(inputTypeGroup);
        matrixInput.setToggleGroup(inputTypeGroup);
        
        // Add listener for input type changes
        inputTypeGroup.selectedToggleProperty().addListener((obs, oldVal, newVal) -> {
            updateInputEditability();
        });
        
        // Add listener for n parameter changes
        nParameterField.textProperty().addListener((obs, oldVal, newVal) -> {
            if (!newVal.isEmpty() && matrixInput.isSelected()) {
                try {
                    int n = Integer.parseInt(newVal);
                    updateMatrixColumns(n);
                } catch (NumberFormatException e) {
                    // Ignore invalid input
                }
            }
        });
        
        // Add listener for matrix changes
        matrixData.addListener((ListChangeListener<int[]>) change -> {
            if (matrixInput.isSelected() && !matrixData.isEmpty()) {
                updatePolynomialFromMatrix();
            }
        });
        
        // Initial editability setup
        updateInputEditability();
        
        // Disable encode/decode buttons until initialization
        encodeButton.setDisable(true);
        decodeButton.setDisable(true);
    }

    private void setupMatrixColumns(TableView<int[]> table) {
        table.getColumns().clear();
        for (int i = 0; i < 7; i++) {
            final int columnIndex = i;
            TableColumn<int[], Integer> column = new TableColumn<>(String.valueOf(i));
            column.setPrefWidth(40); // Устанавливаем фиксированную ширину столбца
            column.setMinWidth(40);
            column.setMaxWidth(40);
            column.setCellValueFactory(cellData -> 
                new SimpleIntegerProperty(cellData.getValue()[columnIndex]).asObject());
            
            // Make cells editable
            column.setCellFactory(TextFieldTableCell.forTableColumn(new IntegerStringConverter()));
            column.setOnEditCommit(event -> {
                int[] row = event.getRowValue();
                row[columnIndex] = event.getNewValue();
                if (matrixInput.isSelected()) {
                    updatePolynomialFromMatrix();
                }
            });
            
            table.getColumns().add(column);
        }
        table.setFixedCellSize(40); // Устанавливаем фиксированную высоту строки
        table.setEditable(true);
    }

    private void setupSyndromeTable() {
        syndromeTable.getColumns().clear();
        
        // Добавляем столбец для позиции ошибки
        TableColumn<int[], Integer> positionColumn = new TableColumn<>("Position");
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
        
        // Добавляем столбцы для синдрома
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
        log("Syndrome table setup with " + syndromeLength + " syndrome columns");
    }

    private void updateMatrixColumns(int n) {
        generatorMatrixTable.getColumns().clear();
        for (int i = 0; i < n; i++) {
            final int columnIndex = i;
            TableColumn<int[], Integer> column = new TableColumn<>(String.valueOf(i));
            column.setCellValueFactory(cellData -> 
                new SimpleIntegerProperty(cellData.getValue()[columnIndex]).asObject());
            
            // Make cells editable
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
        
        // Update existing rows to match new column count
        for (int i = 0; i < matrixData.size(); i++) {
            int[] row = matrixData.get(i);
            int[] newRow = new int[n];
            System.arraycopy(row, 0, newRow, 0, Math.min(row.length, n));
            matrixData.set(i, newRow);
        }
    }

    private void updatePolynomialFromMatrix() {
        if (matrixData.isEmpty()) return;
        
        try {
            int[][] matrix = matrixData.toArray(new int[0][]);
            CyclicCode tempCode = new CyclicCode(matrix);
            Polynomial g = tempCode.getGeneratorPolynomial();
            polynomialField.setText(g.toString());
        } catch (Exception e) {
            log("Error updating polynomial from matrix: " + e.getMessage());
        }
    }

    private void updateInputEditability() {
        boolean isPolynomialInput = polynomialInput.isSelected();
        
        // Set editability for polynomial input
        polynomialField.setEditable(isPolynomialInput);
        nParameterField.setEditable(isPolynomialInput);
        
        // Set editability for matrix input
        generatorMatrixTable.setEditable(!isPolynomialInput);
        addRowButton.setDisable(isPolynomialInput);
        removeRowButton.setDisable(isPolynomialInput);
        
        // Visual feedback for disabled state
        polynomialField.setStyle(isPolynomialInput ? "" : "-fx-opacity: 0.7;");
        nParameterField.setStyle(isPolynomialInput ? "" : "-fx-opacity: 0.7;");
        generatorMatrixTable.setStyle(!isPolynomialInput ? "" : "-fx-opacity: 0.7;");
    }

    private void startTimer() {
        startTime = System.nanoTime();
    }

    private void stopTimer() {
        endTime = System.nanoTime();
    }

    private String getElapsedTime() {
        long elapsedNanos = endTime - startTime;
        return String.format("%.3f мс", elapsedNanos / 1_000_000.0);
    }

    private void logDetailed(String message) {
        if (detailedLoggingCheckBox.isSelected()) {
            log(message);
        }
    }

    @FXML
    protected void onInitButtonClick() {
        try {
            startTimer();
            if (polynomialInput.isSelected()) {
                String polynomialStr = polynomialField.getText().trim();
                int n = Integer.parseInt(nParameterField.getText().trim());
                
                if (polynomialStr.isEmpty()) {
                    throw new IllegalArgumentException("Polynomial cannot be empty");
                }
                
                log("Initializing cyclic code with polynomial: " + polynomialStr);
                log("Parameter n: " + n);
                
                Polynomial g = Polynomial.fromString(polynomialStr);
                logDetailed("Parsed polynomial coefficients: " + Arrays.toString(g.getCoefficients()));
                logDetailed("Degree of generator polynomial: " + g.getDegree());
                
                cyclicCode = new CyclicCode(g, n);
                log("Cyclic code initialized successfully");
                
                // Update generator matrix table
                matrixData.clear();
                int[][] generatorMatrix = cyclicCode.getGeneratorMatrix();
                logDetailed("\nGenerating generator matrix:");
                for (int i = 0; i < generatorMatrix.length; i++) {
                    logDetailed("Row " + i + ": " + Arrays.toString(generatorMatrix[i]));
                    matrixData.add(generatorMatrix[i]);
                }
                log("Generator matrix updated");
            } else {
                // Initialize from matrix input
                if (matrixData.isEmpty()) {
                    throw new IllegalArgumentException("Generator matrix cannot be empty");
                }
                
                log("Initializing cyclic code from generator matrix");
                int[][] generatorMatrix = matrixData.toArray(new int[0][]);
                logDetailed("\nInput generator matrix:");
                for (int i = 0; i < generatorMatrix.length; i++) {
                    logDetailed("Row " + i + ": " + Arrays.toString(generatorMatrix[i]));
                }
                
                cyclicCode = new CyclicCode(generatorMatrix);
                log("Cyclic code initialized successfully");
            }
            
            // Update parity check matrix
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
                logDetailed("Row " + i + ": " + Arrays.toString(parityCheckMatrix[i]));
            }
            
            parityCheckMatrixTable.getItems().clear();
            for (int[] row : parityCheckMatrix) {
                parityCheckMatrixTable.getItems().add(row);
            }
            log("Parity check matrix updated");
            
            // Update syndrome table
            updateSyndromeTable();
            log("Syndrome table updated");
            
            // Enable encode/decode buttons
            encodeButton.setDisable(false);
            decodeButton.setDisable(false);
            
            stopTimer();
            log("\nCyclic code initialization completed successfully");
            log("Total initialization time: " + getElapsedTime());
        } catch (Exception e) {
            showError("Initialization Error", e.getMessage());
            log("Error during initialization: " + e.getMessage());
        }
    }

    private void updateSyndromeTable() {
        if (cyclicCode == null) return;
        
        syndromeData.clear();
        int n = cyclicCode.getN();
        int syndromeLength = n - cyclicCode.getK(); // Количество символов в синдроме
        
        for (int i = 0; i < n; i++) {
            int[] error = new int[n];
            error[i] = 1;
            int[] syndrome = cyclicCode.calculateSyndrome(error);
            
            // Создаем строку для таблицы: [позиция, s0, s1, ..., sn-k-1]
            int[] row = new int[syndromeLength + 1]; // +1 для позиции
            row[0] = i; // Позиция ошибки
            System.arraycopy(syndrome, 0, row, 1, syndromeLength);
            syndromeData.add(row);
        }
        
        log("Syndrome table updated with " + syndromeLength + " syndrome symbols");
    }

    @FXML
    protected void onAddRowButtonClick() {
        int[] newRow = new int[7];
        matrixData.add(newRow);
        log("Added new row to generator matrix");
    }

    @FXML
    protected void onRemoveRowButtonClick() {
        if (!matrixData.isEmpty()) {
            matrixData.remove(matrixData.size() - 1);
            log("Removed last row from generator matrix");
        }
    }

    @FXML
    protected void onLoadFileButtonClick() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Select Input File");
        File file = fileChooser.showOpenDialog(null);
        if (file != null) {
            try {
                String content = new String(Files.readAllBytes(file.toPath()), StandardCharsets.UTF_8);
                inputText.setText(content);
                log("File loaded successfully: " + file.getName());
                log("File content: " + content);
            } catch (IOException e) {
                showError("Error loading file", e.getMessage());
                log("Error loading file: " + e.getMessage());
            }
        }
    }

    private int[][] getMatrixFromTable(TableView<int[]> table) {
        ObservableList<int[]> data = table.getItems();
        int[][] matrix = new int[data.size()][];
        for (int i = 0; i < data.size(); i++) {
            matrix[i] = data.get(i);
        }
        return matrix;
    }

    private void updateMatrixTable(TableView<int[]> table, int[][] matrix) {
        ObservableList<int[]> data = FXCollections.observableArrayList();
        for (int[] row : matrix) {
            data.add(row);
        }
        table.setItems(data);
    }

    private int[] parseInput(String input) {
        // Remove all whitespace
        input = input.replaceAll("\\s+", "");
        
        // Check if input is binary string (only 0s and 1s)
        if (input.matches("[01]+")) {
            int[] result = new int[input.length()];
            for (int i = 0; i < input.length(); i++) {
                result[i] = input.charAt(i) - '0';
            }
            return result;
        }
        
        // If not binary, treat as text and convert to binary using ASCII
        StringBuilder binaryString = new StringBuilder();
        for (char c : input.toCharArray()) {
            String binary = Integer.toBinaryString(c);
            // Pad with leading zeros to make 8 bits
            binary = String.format("%8s", binary).replace(' ', '0');
            binaryString.append(binary);
        }
        
        int[] result = new int[binaryString.length()];
        for (int i = 0; i < binaryString.length(); i++) {
            result[i] = binaryString.charAt(i) - '0';
        }
        return result;
    }

    private String formatOutput(int[] bits) {
        StringBuilder result = new StringBuilder();
        for (int bit : bits) {
            result.append(bit);
        }
        return result.toString();
    }

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

    private int[] introduceRandomErrors(int[] codeword) {
        int[] corrupted = codeword.clone();
        
        // Для циклического кода (7,4) максимальное количество исправляемых ошибок - 1
        int maxCorrectableErrors = 1;
        int errorCount = random.nextInt(maxCorrectableErrors) + 1; // 1 ошибка
        
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
            corrupted[position] = 1 - corrupted[position]; // Инвертируем бит
            log("Ошибка в позиции " + position + ": " + codeword[position] + " -> " + corrupted[position]);
        }
        
        log("Искаженное сообщение: " + Arrays.toString(corrupted));
        return corrupted;
    }

    private String binaryToAscii(String binary) {
        int byteCount = binary.length() / 8;
        byte[] bytes = new byte[byteCount];
        for (int i = 0; i < byteCount; i++) {
            String byteStr = binary.substring(i * 8, (i + 1) * 8);
            bytes[i] = (byte) Integer.parseInt(byteStr, 2);
        }
        return new String(bytes, StandardCharsets.UTF_8);
    }

    @FXML
    protected void onEncodeButtonClick() {
        try {
            startTimer();
            String messageStr = inputText.getText().trim();
            if (messageStr.isEmpty()) {
                throw new IllegalArgumentException("Message cannot be empty");
            }
            
            log("\nEncoding process started");
            log("Input text: " + messageStr);
            
            // Convert text to binary using UTF-8
            byte[] messageBytes = messageStr.getBytes(StandardCharsets.UTF_8);
            StringBuilder binaryString = new StringBuilder();
            logDetailed("\nConverting text to binary (UTF-8):");
            for (int i = 0; i < messageBytes.length; i++) {
                int val = messageBytes[i] & 0xFF;
                String binary = String.format("%8s", Integer.toBinaryString(val)).replace(' ', '0');
                binaryString.append(binary);
                logDetailed("Byte " + i + ": " + val + " -> Binary " + binary);
            }
            
            // Convert binary string to int array
            int[] message = new int[binaryString.length()];
            for (int i = 0; i < binaryString.length(); i++) {
                message[i] = binaryString.charAt(i) - '0';
            }
            log("Binary message: " + binaryString);
            
            if (blockProcessingCheckBox.isSelected()) {
                int blockSize = cyclicCode.getK();
                StringBuilder encodedMessage = new StringBuilder();
                log("\nStarting block encoding with block size: " + blockSize);
                
                for (int i = 0; i < message.length; i += blockSize) {
                    int[] block = Arrays.copyOfRange(message, i, Math.min(i + blockSize, message.length));
                    logDetailed("\nEncoding block " + (i/blockSize + 1) + ":");
                    logDetailed("Original block: " + Arrays.toString(block));
                    
                    int[] codeword = cyclicCode.encode(block);
                    logDetailed("Encoded block: " + Arrays.toString(codeword));
                    
                    // Introduce random errors if checkbox is selected
                    if (randomErrorsCheckBox.isSelected()) {
                        codeword = introduceRandomErrors(codeword);
                    }
                    
                    for (int bit : codeword) {
                        encodedMessage.append(bit);
                    }
                }
                
                String encodedBinary = encodedMessage.toString();
                outputText.setText(encodedBinary);
                
                log("\nFinal encoded message:");
                log("Binary: " + encodedBinary);
                logDetailed("ASCII representation:");
                String asciiRepresentation = binaryToAscii(encodedBinary);
                logDetailed("Text: " + asciiRepresentation);
                for (int i = 0; i < encodedBinary.length(); i += 8) {
                    if (i + 8 <= encodedBinary.length()) {
                        String byteStr = encodedBinary.substring(i, i + 8);
                        int ascii = Integer.parseInt(byteStr, 2);
                        logDetailed("Byte " + (i/8 + 1) + ": " + byteStr + " -> ASCII " + ascii + " -> Character '" + (char)ascii + "'");
                    }
                }
            } else {
                int[] codeword = cyclicCode.encode(message);
                
                // Introduce random errors if checkbox is selected
                if (randomErrorsCheckBox.isSelected()) {
                    codeword = introduceRandomErrors(codeword);
                }
                
                log("\nEncoding complete:");
                log("Original message: " + Arrays.toString(message));
                logDetailed("Encoded codeword: " + Arrays.toString(codeword));
                
                StringBuilder binaryOutput = new StringBuilder();
                for (int bit : codeword) {
                    binaryOutput.append(bit);
                }
                outputText.setText(binaryOutput.toString());
                
                log("\nFinal encoded message:");
                log("Binary: " + binaryOutput);
                logDetailed("ASCII representation:");
                String asciiRepresentation = binaryToAscii(binaryOutput.toString());
                logDetailed("Text: " + asciiRepresentation);
                for (int i = 0; i < binaryOutput.length(); i += 8) {
                    if (i + 8 <= binaryOutput.length()) {
                        String byteStr = binaryOutput.substring(i, i + 8);
                        int ascii = Integer.parseInt(byteStr, 2);
                        logDetailed("Byte " + (i/8 + 1) + ": " + byteStr + " -> ASCII " + ascii + " -> Character '" + (char)ascii + "'");
                    }
                }
            }
            
            stopTimer();
            log("Total encoding time: " + getElapsedTime());
        } catch (Exception e) {
            showError("Encoding Error", e.getMessage());
            log("Error during encoding: " + e.getMessage());
        }
    }

    @FXML
    protected void onDecodeButtonClick() {
        try {
            startTimer();
            String codewordStr = inputText.getText().trim();
            if (codewordStr.isEmpty()) {
                throw new IllegalArgumentException("Codeword cannot be empty");
            }
            
            log("\nDecoding process started");
            log("Input codeword: " + codewordStr);
            
            // Convert binary string to int array
            int[] codeword = new int[codewordStr.length()];
            for (int i = 0; i < codewordStr.length(); i++) {
                codeword[i] = codewordStr.charAt(i) - '0';
            }
            
            if (blockProcessingCheckBox.isSelected()) {
                int blockSize = cyclicCode.getN();
                StringBuilder decodedMessage = new StringBuilder();
                log("\nStarting block decoding with block size: " + blockSize);
                
                for (int i = 0; i < codeword.length; i += blockSize) {
                    int[] block = Arrays.copyOfRange(codeword, i, Math.min(i + blockSize, codeword.length));
                    logDetailed("\nDecoding block " + (i/blockSize + 1) + ":");
                    logDetailed("Received block: " + Arrays.toString(block));
                    
                    // Display decoding info for current block
                    displayDecodingInfo(block);
                    
                    // Calculate syndrome
                    int[] syndrome = cyclicCode.calculateSyndrome(block);
                    logDetailed("Syndrome: " + Arrays.toString(syndrome));
                    
                    // Check for errors
                    boolean hasError = false;
                    for (int s : syndrome) {
                        if (s != 0) {
                            hasError = true;
                            break;
                        }
                    }
                    
                    if (hasError) {
                        logDetailed("Error detected in block " + (i/blockSize + 1));
                        logDetailed("Error positions: " + Arrays.toString(syndrome));
                    } else {
                        logDetailed("No errors detected in block " + (i/blockSize + 1));
                    }
                    
                    int[] message = cyclicCode.decode(block);
                    logDetailed("Decoded block: " + Arrays.toString(message));
                    
                    for (int bit : message) {
                        decodedMessage.append(bit);
                    }
                }
                
                // Convert binary back to text using UTF-8
                String binaryString = decodedMessage.toString();
                String resultText = binaryToAscii(binaryString);
                outputText.setText(resultText);
                log("\nFinal decoded message: " + resultText);
            } else {
                log("\nDecoding single block:");
                logDetailed("Received codeword: " + Arrays.toString(codeword));
                
                // Display decoding info
                displayDecodingInfo(codeword);
                
                // Calculate syndrome
                int[] syndrome = cyclicCode.calculateSyndrome(codeword);
                logDetailed("Syndrome: " + Arrays.toString(syndrome));
                
                // Check for errors
                boolean hasError = false;
                for (int s : syndrome) {
                    if (s != 0) {
                        hasError = true;
                        break;
                    }
                }
                
                if (hasError) {
                    logDetailed("Error detected in codeword");
                    logDetailed("Error positions: " + Arrays.toString(syndrome));
                } else {
                    logDetailed("No errors detected in codeword");
                }
                
                int[] message = cyclicCode.decode(codeword);
                logDetailed("Decoded message: " + Arrays.toString(message));
                
                // Convert binary back to text using UTF-8
                StringBuilder binaryStringBuilder = new StringBuilder();
                for (int bit : message) {
                    binaryStringBuilder.append(bit);
                }
                String resultText = binaryToAscii(binaryStringBuilder.toString());
                outputText.setText(resultText);
                log("\nFinal decoded message: " + resultText);
            }
            
            stopTimer();
            log("Total decoding time: " + getElapsedTime());
        } catch (Exception e) {
            showError("Decoding Error", e.getMessage());
            log("Error during decoding: " + e.getMessage());
        }
    }

    @FXML
    protected void onClearLogsButtonClick() {
        processLog.clear();
        errorCorrectionSteps.clear();
        log("Logs cleared");
    }

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

    private void displayDecodingInfo(int[] received) {
        Polynomial receivedPoly = new Polynomial(received);
        Polynomial syndrome = receivedPoly.mod(cyclicCode.getGeneratorPolynomial());
        
        // Обновляем информацию о синдроме
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

    private void log(String message) {
        processLog.appendText(message + "\n");
    }

    private void showError(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
} 