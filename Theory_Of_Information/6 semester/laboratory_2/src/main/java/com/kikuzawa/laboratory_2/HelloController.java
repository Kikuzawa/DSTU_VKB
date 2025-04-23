package com.kikuzawa.laboratory_2;

import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.fxml.FXML;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.control.cell.TextFieldTableCell;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
import javafx.util.converter.DefaultStringConverter;

import java.util.*;


public class HelloController {
    public Button count_sum_button;
    public TableView<Polynomial> SumTable;
    public Button decode_button;
    public Button encode_button;
    public TextArea input_text;
    public TextArea encode_text;
    public TextArea decode_text;
    public TextField count_reg_text;
    public TextField count_sum_text;

    private final List<int[]> polynomials = new ArrayList<>();
    private String originalBinary = "";

    @FXML
    public void initialize() {
        // Настройка таблицы для сумматоров
        TableColumn<Polynomial, String> polyColumn = new TableColumn<>("Полиномы");
        polyColumn.setCellValueFactory(new PropertyValueFactory<>("polynomial"));
        SumTable.getColumns().add(polyColumn);

        // Инициализация таблицы
        SumTable.setItems(FXCollections.observableArrayList());
    }

    public void encode() {
        try {
            // Получение параметров из таблицы
            polynomials.clear();
            for (Polynomial poly : SumTable.getItems()) {
                String[] parts = poly.getPolynomial().split(",");
                int[] polynomial = new int[parts.length];
                for (int i = 0; i < parts.length; i++) {
                    polynomial[i] = Integer.parseInt(parts[i].trim());
                }
                polynomials.add(polynomial);
            }

            // Получение входных данных
            String inputData = input_text.getText().trim();

            // Определение типа входных данных
            String binary;
            if (inputData.matches("[01]+")) {
                binary = inputData + "0";
            } else {
                binary = textToBinary(inputData);
            }

            originalBinary = binary;
            String encoded = convolutionalEncode(binary, polynomials);

            // Удаление первых трех символов, если строка состоит только из '0' и '1'
            if (encoded.matches("[01]+")) {
                encoded = encoded.substring(3);
            }

            encode_text.setText(encoded);

        } catch (Exception e) {
            showError(e.getMessage());
        }
    }

    public void decode() {
        try {
            // Получение закодированных данных
            String encoded = "000" + encode_text.getText().trim();

            // Декодирование
            String decodedBits = viterbiDecode(encoded, polynomials);

            // Попытка преобразовать в текст
            try {
                String decoded = binaryToText(decodedBits);
                String originalText = binaryToText(originalBinary);
                String output = "Результат:\nТекст: " + decoded + "\nБиты: " + decodedBits.substring(0, decodedBits.length() - 1);;
                if (!decoded.equals(originalText)) {
                    output += "\n\nОбнаружены неисправленные ошибки!";
                }
                decode_text.setText(output);
            } catch (Exception e) {
                decode_text.setText(decodedBits);
            }

        } catch (Exception e) {
            showError(e.getMessage());
        }
    }

    public void init_sum_table() {
        try {
            int columnCount = Integer.parseInt(count_reg_text.getText());

            // Проверка на ограничение количества регистров
            if (columnCount > 10) {
                showError("Количество регистров не должно превышать 10.");
                return;
            }

            // Остальной код инициализации таблицы
            SumTable.getItems().clear();
            SumTable.getColumns().clear();

            int rowCount = Integer.parseInt(count_sum_text.getText());

            // Создаем динамические столбцы
            for (int i = 0; i < columnCount; i++) {
                TableColumn<Polynomial, String> column = new TableColumn<>("R " + (i + 1));
                final int colIndex = i;

                // Устанавливаем фабрику ячеек для редактирования
                column.setCellFactory(TextFieldTableCell.forTableColumn(new DefaultStringConverter()));

                // Обработчик событий для сохранения изменений
                column.setOnEditCommit(event -> {
                    Polynomial polynomial = event.getRowValue();
                    String[] parts = polynomial.getPolynomial().split(",");

                    // Проверяем длину массива и расширяем его при необходимости
                    if (parts.length <= colIndex) {
                        String[] newParts = new String[Math.max(colIndex + 1, columnCount)];
                        System.arraycopy(parts, 0, newParts, 0, parts.length);
                        Arrays.fill(newParts, parts.length, newParts.length, "");
                        parts = newParts;
                    }

                    parts[colIndex] = event.getNewValue().trim();
                    polynomial.setPolynomial(String.join(",", parts));
                });

                // Привязка данных к столбцу с отображением "-" для пустых значений
                column.setCellValueFactory(cellData -> {
                    Polynomial polynomial = cellData.getValue();
                    if (polynomial == null) return new SimpleStringProperty("");

                    String[] parts = polynomial.getPolynomial().split(",");

                    // Расширяем массив если нужно
                    if (parts.length <= colIndex) {
                        String[] newParts = new String[Math.max(colIndex + 1, columnCount)];
                        System.arraycopy(parts, 0, newParts, 0, parts.length);
                        Arrays.fill(newParts, parts.length, newParts.length, "");
                        parts = newParts;
                    }

                    String value = parts[colIndex].trim();
                    return new SimpleStringProperty(value.isEmpty() ? "-" : value);
                });

                SumTable.getColumns().add(column);
            }

            // Создаем динамические строки с корректным размером массива
            for (int i = 0; i < rowCount; i++) {
                String[] values = new String[columnCount];
                Arrays.fill(values, "");
                Polynomial polynomial = new Polynomial(String.join(",", values));
                SumTable.getItems().add(polynomial);
            }

            // Включаем возможность редактирования таблицы
            makeTableEditable();

        } catch (NumberFormatException e) {
            showError("Пожалуйста, введите корректные числовые значения.");
        }
    }

    private void makeTableEditable() {
        SumTable.setEditable(true);
        for (TableColumn<Polynomial, ?> column : SumTable.getColumns()) {
            column.setEditable(true);
        }
    }


    private String textToBinary(String text) {
        StringBuilder binary = new StringBuilder();
        for (char c : text.toCharArray()) {
            binary.append(String.format("%8s", Integer.toBinaryString(c)).replace(' ', '0'));
        }
        return binary.toString();
    }

    private String binaryToText(String binary) {
        StringBuilder text = new StringBuilder();
        for (int i = 0; i < binary.length(); i += 8) {
            String byteString = binary.substring(i, Math.min(i + 8, binary.length()));
            text.append((char) Integer.parseInt(byteString, 2));
        }
        return text.toString();
    }

    private String convolutionalEncode(String inputBits, List<int[]> polynomials) {
        if (inputBits.isEmpty()) {
            return "";
        }

        int maxRegister = polynomials.stream()
                .flatMapToInt(Arrays::stream)
                .max()
                .orElse(0);

        int[] registers = new int[maxRegister + 1];
        StringBuilder encoded = new StringBuilder();

        for (char bit : inputBits.toCharArray()) {
            System.arraycopy(registers, 0, registers, 1, registers.length - 1);
            registers[0] = Character.getNumericValue(bit);

            for (int[] poly : polynomials) {
                int xor = 0;
                for (int idx : poly) {
                    xor ^= registers[idx];
                }
                encoded.append(xor);
            }
        }

        return encoded.toString();
    }

    private String viterbiDecode(String encodedBits, List<int[]> polynomials) {
        if (encodedBits.isEmpty()) {
            return "";
        }

        int nOutputs = polynomials.size();
        int maxRegister = polynomials.stream()
                .flatMapToInt(Arrays::stream)
                .max()
                .orElse(0);

        int nStates = (int) Math.pow(2, maxRegister);
        Map<String, Double> pathMetrics = new HashMap<>();
        Map<String, List<String>> paths = new HashMap<>();

        pathMetrics.put("0".repeat(maxRegister), 0.0);
        paths.put("0".repeat(maxRegister), new ArrayList<>());

        // Список для хранения истории шагов
        List<DecodingStep> decodingHistory = new ArrayList<>();

        // Добавляем начальные параметры в историю
        decodingHistory.add(new DecodingStep(
                "Начальные параметры",
                "Количество состояний: " + nStates,
                "Длина закодированной последовательности: " + encodedBits.length() + " бит",
                "Количество шагов: " + (encodedBits.length() / nOutputs),
                "",
                0,
                0.0,
                ""
        ));

        for (int step = 0; step < encodedBits.length() / nOutputs; step++) {
            String currentBits = encodedBits.substring(step * nOutputs, (step + 1) * nOutputs);
            Map<String, Double> newMetrics = new HashMap<>();
            Map<String, List<String>> newPaths = new HashMap<>();

            for (String state : pathMetrics.keySet()) {
                if (pathMetrics.get(state) == Double.POSITIVE_INFINITY) {
                    continue;
                }

                for (String inputBit : List.of("0", "1")) {
                    String nextState = inputBit + state.substring(0, state.length() - 1);
                    int[] tmpRegisters = new int[maxRegister + 1];
                    tmpRegisters[0] = Integer.parseInt(inputBit);

                    // Преобразуем символы состояния в целые числа
                    char[] stateChars = state.toCharArray();
                    for (int i = 0; i < stateChars.length; i++) {
                        tmpRegisters[i + 1] = Character.getNumericValue(stateChars[i]);
                    }

                    StringBuilder expected = new StringBuilder();
                    for (int[] poly : polynomials) {
                        int xor = 0;
                        for (int idx : poly) {
                            xor ^= tmpRegisters[idx];
                        }
                        expected.append(xor);
                    }

                    int metric = 0;
                    for (int i = 0; i < currentBits.length(); i++) {
                        if (currentBits.charAt(i) != expected.charAt(i)) {
                            metric++;
                        }
                    }

                    double totalMetric = pathMetrics.get(state) + metric;
                    if (totalMetric < newMetrics.getOrDefault(nextState, Double.POSITIVE_INFINITY)) {
                        newMetrics.put(nextState, totalMetric);
                        List<String> newPath = new ArrayList<>(paths.get(state));
                        newPath.add(inputBit);
                        newPaths.put(nextState, newPath);

                        // Добавляем шаг в историю
                        decodingHistory.add(new DecodingStep(
                                "Шаг " + (step + 1),
                                currentBits,
                                state,
                                nextState,
                                expected.toString(),
                                metric,
                                totalMetric,
                                "✔ Обновление метрики"
                        ));
                    } else {
                        decodingHistory.add(new DecodingStep(
                                "Шаг " + (step + 1),
                                currentBits,
                                state,
                                nextState,
                                expected.toString(),
                                metric,
                                totalMetric,
                                "✖ Метрика хуже текущей"
                        ));
                    }
                }
            }

            pathMetrics = newMetrics;
            paths = newPaths;
        }

        // Добавляем финальные метрики состояний в историю
        decodingHistory.add(new DecodingStep(
                "Финальные метрики состояний",
                "",
                "",
                "",
                "",
                0,
                0.0,
                ""
        ));

        for (String state : pathMetrics.keySet()) {
            decodingHistory.add(new DecodingStep(
                    state,
                    "Метрика: " + pathMetrics.get(state),
                    "Путь: " + paths.get(state),
                    "",
                    "",
                    0,
                    0.0,
                    ""
            ));
        }

        // Добавляем выбранный путь в историю
        String finalState = pathMetrics.entrySet().stream()
                .min(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse("");

        List<String> resultPath = paths.get(finalState);
        decodingHistory.add(new DecodingStep(
                "Выбранный путь",
                finalState,
                "Метрика: " + pathMetrics.get(finalState),
                "Путь: " + resultPath,
                "",
                0,
                0.0,
                ""
        ));

        // Показываем историю в новом окне
        showDecodingHistory(decodingHistory);

        return String.join("", resultPath);
    }

    public void fillTable() {
        SumTable.getItems().clear();
        SumTable.getColumns().clear();

        // Create columns
        for (int i = 0; i < 3; i++) {
            TableColumn<Polynomial, String> column = new TableColumn<>("R " + (i + 1));
            final int colIndex = i;

            column.setCellFactory(TextFieldTableCell.forTableColumn(new DefaultStringConverter()));
            column.setOnEditCommit(event -> {
                Polynomial polynomial = event.getRowValue();
                String[] parts = polynomial.getPolynomial().split(",");

                if (parts.length <= colIndex) {
                    String[] newParts = new String[Math.max(colIndex + 1, 3)];
                    System.arraycopy(parts, 0, newParts, 0, parts.length);
                    Arrays.fill(newParts, parts.length, newParts.length, "");
                    parts = newParts;
                }

                parts[colIndex] = event.getNewValue().trim();
                polynomial.setPolynomial(String.join(",", parts));
            });

            column.setCellValueFactory(cellData -> {
                Polynomial polynomial = cellData.getValue();
                if (polynomial == null) return new SimpleStringProperty("");

                String[] parts = polynomial.getPolynomial().split(",");
                if (parts.length <= colIndex) {
                    String[] newParts = new String[Math.max(colIndex + 1, 3)];
                    System.arraycopy(parts, 0, newParts, 0, parts.length);
                    Arrays.fill(newParts, parts.length, newParts.length, "");
                    parts = newParts;
                }

                String value = parts[colIndex].trim();
                return new SimpleStringProperty(value.isEmpty() ? "-" : value);
            });

            SumTable.getColumns().add(column);
        }

        // Add rows with specified values
        SumTable.getItems().add(new Polynomial("1,2"));
        SumTable.getItems().add(new Polynomial("2,3"));
        SumTable.getItems().add(new Polynomial("1,2,3"));

        makeTableEditable();
    }

    public static class DecodingStep {
        private final String step;
        private final String currentBits;
        private final String state;
        private final String nextState;
        private final String expected;
        private final int metric;
        private final double totalMetric;
        private final String status;

        public DecodingStep(String step, String currentBits, String state, String nextState, String expected, int metric, double totalMetric, String status) {
            this.step = step;
            this.currentBits = currentBits;
            this.state = state;
            this.nextState = nextState;
            this.expected = expected;
            this.metric = metric;
            this.totalMetric = totalMetric;
            this.status = status;
        }
        // Геттеры
        public String getStep() { return step; }
        public String getCurrentBits() { return currentBits; }
        public String getState() { return state; }
        public String getNextState() { return nextState; }
        public String getExpected() { return expected; }
        public int getMetric() { return metric; }
        public double getTotalMetric() { return totalMetric; }
        public String getStatus() { return status; }
    }

    private void showError(String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle("Ошибка");
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }

    private void showDecodingHistory(List<DecodingStep> decodingHistory) {
        Stage historyStage = new Stage();
        historyStage.setTitle("История декодирования");

        TableView<DecodingStep> historyTable = new TableView<>();
        historyTable.setColumnResizePolicy(TableView.CONSTRAINED_RESIZE_POLICY);

        // Столбцы таблицы
        TableColumn<DecodingStep, String> stepColumn = new TableColumn<>("Шаг/Параметр");
        stepColumn.setCellValueFactory(new PropertyValueFactory<>("step"));

        TableColumn<DecodingStep, String> currentBitsColumn = new TableColumn<>("Полученные биты");
        currentBitsColumn.setCellValueFactory(new PropertyValueFactory<>("currentBits"));

        TableColumn<DecodingStep, String> stateColumn = new TableColumn<>("Состояние");
        stateColumn.setCellValueFactory(new PropertyValueFactory<>("state"));

        TableColumn<DecodingStep, String> nextStateColumn = new TableColumn<>("Следующее состояние");
        nextStateColumn.setCellValueFactory(new PropertyValueFactory<>("nextState"));

        TableColumn<DecodingStep, String> expectedColumn = new TableColumn<>("Ожидаемые биты");
        expectedColumn.setCellValueFactory(new PropertyValueFactory<>("expected"));

        TableColumn<DecodingStep, Integer> metricColumn = new TableColumn<>("Метрика шага");
        metricColumn.setCellValueFactory(new PropertyValueFactory<>("metric"));

        TableColumn<DecodingStep, Double> totalMetricColumn = new TableColumn<>("Общая метрика");
        totalMetricColumn.setCellValueFactory(new PropertyValueFactory<>("totalMetric"));

        TableColumn<DecodingStep, String> statusColumn = new TableColumn<>("Статус");
        statusColumn.setCellValueFactory(new PropertyValueFactory<>("status"));

        historyTable.getColumns().addAll(stepColumn, currentBitsColumn, stateColumn, nextStateColumn, expectedColumn, metricColumn, totalMetricColumn, statusColumn);
        historyTable.setItems(FXCollections.observableArrayList(decodingHistory));

        Scene scene = new Scene(new StackPane(historyTable), 1000, 600);
        historyStage.setScene(scene);
        historyStage.show();
    }



    // Класс для представления строки в таблице
    public static class Polynomial {
        private final SimpleStringProperty polynomial;

        public Polynomial(String polynomial) {
            this.polynomial = new SimpleStringProperty(polynomial);
        }

        public String getPolynomial() {
            return polynomial.get();
        }

        public void setPolynomial(String polynomial) {
            this.polynomial.set(polynomial);
        }

    }
}