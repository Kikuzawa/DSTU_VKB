package org.example.laboratory__3;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.example.laboratory__3.coding.BlockCoder;
import org.example.laboratory__3.coding.BlockInterleaver;
import org.example.laboratory__3.coding.ConvolutionalCoder;
import org.example.laboratory__3.utils.ImageUtils;

import javafx.beans.property.DoubleProperty;
import javafx.beans.property.IntegerProperty;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.embed.swing.SwingFXUtils;
import javafx.fxml.FXML;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.RadioButton;
import javafx.scene.control.Slider;
import javafx.scene.control.TextArea;
import javafx.scene.control.ToggleGroup;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.stage.FileChooser;

public class HelloController {
    // Поля для элементов интерфейса
    @FXML private ImageView inputImageView;          // Изображение для ввода
    @FXML private ImageView blockEncodedImageView;   // Изображение после блочного кодирования
    @FXML private ImageView blockEncodedWithErrorsImageView; // Изображение с ошибками после кодирования
    @FXML private ImageView noisyImageView;          // Изображение с шумами без кодирования
    @FXML private ImageView outputImageView;         // Декодированное изображение
    @FXML private Slider errorRateSlider;            // Слайдер вероятности ошибки
    @FXML private Label errorRateLabel;              // Метка вероятности ошибки
    @FXML private Slider bitsPerPixelSlider;         // Слайдер количества битов на пиксель
    @FXML private Label bitsPerPixelLabel;           // Метка количества битов на пиксель
    @FXML private ToggleGroup matrixTypeGroup;       // Группа переключателей типа матрицы
    @FXML private TextArea matrixTextArea;           // Текстовая область для ввода матрицы
    @FXML private Label nLabel;                      // Метка параметра n
    @FXML private Label kLabel;                      // Метка параметра k
    @FXML private Label dminLabel;                   // Метка минимального расстояния
    @FXML private Label tLabel;                      // Метка корректирующей способности
    @FXML private TextArea polynomialsTextArea;      // Текстовая область для ввода полиномов
    @FXML private CheckBox verboseCheckBox;          // Флаг подробного вывода
    @FXML private TextArea logTextArea;              // Область для логов
    @FXML private CheckBox saveIntermediateImagesCheckBox; // Флаг сохранения промежуточных изображений
    @FXML private Label statusLabel;                 // Метка статуса декодирования
    @FXML private Label uncorrectedErrorsLabel;      // Метка количества неисправленных ошибок
    @FXML private Label imageMatchPercentLabel;      // Метка процента соответствия изображений
    @FXML private CheckBox multiThreadingCheckBox;   // Флаг многопоточности
    @FXML private javafx.scene.control.ProgressBar progressBar; // Индикатор прогресса
    @FXML private Label progressLabel;               // Метка прогресса

    // Пути к файлам и изображения
    private String inputImagePath;                    // Путь к входному изображению
    private String outputImagePath = "output_decoded.png"; // Путь к выходному изображению
    private String intermediateDataFile = "intermediate_data.txt"; // Файл с промежуточными данными
    private BufferedImage inputImage;                 // Входное изображение

    // Свойства для хранения значений
    private final DoubleProperty errorRate = new SimpleDoubleProperty(10.0); // Вероятность ошибки
    private final IntegerProperty bitsPerPixel = new SimpleIntegerProperty(1); // Биты на пиксель

    // Компоненты для кодирования
    private BlockCoder blockCoder;                    // Блочный кодер
    private ConvolutionalCoder convCoder;             // Сверточный кодер
    private BlockInterleaver interleaver;             // Блочный перемежитель

    /**
     * Инициализация контроллера
     */
    @FXML
    public void initialize() {
        // Инициализация компонентов
        blockCoder = new BlockCoder();
        convCoder = new ConvolutionalCoder();
        interleaver = new BlockInterleaver();

        // Настройка слушателя слайдера вероятности ошибки
        errorRateSlider.valueProperty().addListener((obs, oldVal, newVal) -> {
            errorRate.set(newVal.doubleValue());
            errorRateLabel.setText(String.format("%.0f%%", errorRate.get()));
        });

        // Настройка слушателя слайдера битов на пиксель
        bitsPerPixelSlider.valueProperty().addListener((obs, oldVal, newVal) -> {
            bitsPerPixel.set(newVal.intValue());
            bitsPerPixelLabel.setText(String.format("%d", bitsPerPixel.get()));
        });
        
        // Установка начального значения метки
        bitsPerPixelLabel.setText(String.format("%d", bitsPerPixel.get()));

        // Очистка файла с промежуточными данными
        ImageUtils.clearIntermediateData(intermediateDataFile);
        
        // Инициализация индикаторов статуса
        updateStatus("Ожидание декодирования", false);
        resetErrorCounters();
    }
    
    /**
     * Обновление индикатора статуса
     * @param message Сообщение о статусе
     * @param success Успешность операции
     */
    private void updateStatus(String message, boolean success) {
        statusLabel.setText(success ? "✅ " + message : "❌ " + message);
        statusLabel.setStyle(success ? "-fx-text-fill: green;" : "-fx-text-fill: red;");
    }
    
    /**
     * Обновление статистики ошибок
     * @param corrected Количество исправленных ошибок
     * @param uncorrected Количество неисправленных ошибок
     */
    private void updateErrorStats(int corrected, int uncorrected) {
        uncorrectedErrorsLabel.setText("Неисправлено ошибок: " + uncorrected);
    }

    /**
     * Обработчик нажатия кнопки загрузки изображения
     */
    @FXML
    protected void onLoadImageButtonClick() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Image File");
        fileChooser.getExtensionFilters().addAll(
            new FileChooser.ExtensionFilter("Image Files", "*.png", "*.jpg", "*.jpeg", "*.bmp"),
            new FileChooser.ExtensionFilter("All Files", "*.*")
        );

        File file = fileChooser.showOpenDialog(inputImageView.getScene().getWindow());
        if (file != null) {
            inputImagePath = file.getAbsolutePath();
            inputImage = ImageUtils.loadImage(inputImagePath);
            if (inputImage != null) {
                Image image = SwingFXUtils.toFXImage(inputImage, null);
                inputImageView.setImage(image);
                log("Image loaded: " + file.getName());
                log(String.format("Size: %dx%d", inputImage.getWidth(), inputImage.getHeight()));
            } else {
                log("Error loading image", true);
            }
        }
    }

    /**
     * Обработчик нажатия кнопки сохранения изображения
     */
    @FXML
    protected void onSaveImageButtonClick() {
        if (outputImageView.getImage() == null) {
            log("No output image to save", true);
            return;
        }

        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Save Image File");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("PNG files (*.png)", "*.png")
        );

        File file = fileChooser.showSaveDialog(outputImageView.getScene().getWindow());
        if (file != null) {
            try {
                BufferedImage image = SwingFXUtils.fromFXImage(outputImageView.getImage(), null);
                ImageUtils.saveImage(image, file.getAbsolutePath());
                log("Image saved: " + file.getName());
            } catch (Exception e) {
                log("Error saving image: " + e.getMessage(), true);
            }
        }
    }

    /**
     * Обработчик нажатия кнопки настройки блочного кода
     */
    @FXML
    protected void onSetupBlockCodeButtonClick() {
        try {
            String[] matrixRows = matrixTextArea.getText().trim().split("\n");
            List<String> matrix = new ArrayList<>(Arrays.asList(matrixRows));

            // Проверка типа матрицы
            String matrixType = ((RadioButton)matrixTypeGroup.getSelectedToggle()).getText().startsWith("G") ? "G" : "H";

            if (matrix.isEmpty()) {
                throw new IllegalArgumentException("Matrix is empty");
            }

            for (String row : matrix) {
                if (!row.matches("[01]+")) {
                    throw new IllegalArgumentException("Matrix must contain only 0s and 1s");
                }
            }

            // Настройка блочного кода
            boolean result = blockCoder.setupCode(matrix, matrixType);

            if (result) {
                nLabel.setText(String.valueOf(blockCoder.getN()));
                kLabel.setText(String.valueOf(blockCoder.getK()));
                dminLabel.setText(String.valueOf(blockCoder.getDmin()));
                tLabel.setText(String.valueOf(blockCoder.getT()));

                log(String.format("Block code setup: (%d, %d)", blockCoder.getN(), blockCoder.getK()));
                log(String.format("dmin = %d, t = %d", blockCoder.getDmin(), blockCoder.getT()));
            } else {
                log("Error setting up block code", true);
            }
        } catch (Exception e) {
            log("Error setting up block code: " + e.getMessage(), true);
        }
    }

    /**
     * Обработчик нажатия кнопки настройки сверточного кода
     */
    @FXML
    protected void onSetupConvolutionalCodeButtonClick() {
        try {
            String[] polyLines = polynomialsTextArea.getText().trim().split("\n");
            List<int[]> polynomials = new ArrayList<>();

            for (String line : polyLines) {
                if (!line.trim().isEmpty()) {
                    String[] indices = line.split(",");
                    int[] poly = new int[indices.length];
                    for (int i = 0; i < indices.length; i++) {
                        poly[i] = Integer.parseInt(indices[i].trim());
                    }
                    polynomials.add(poly);
                }
            }

            if (polynomials.isEmpty()) {
                throw new IllegalArgumentException("No polynomials specified");
            }

            convCoder.setPolynomials(polynomials);
            convCoder.setVerbose(verboseCheckBox.isSelected());

            log("Convolutional code setup: " + polynomials.size() + " polynomials");
            StringBuilder sb = new StringBuilder("Polynomials: ");
            for (int[] poly : polynomials) {
                sb.append(Arrays.toString(poly)).append(" ");
            }
            log(sb.toString());

        } catch (Exception e) {
            log("Error setting up convolutional code: " + e.getMessage(), true);
        }
    }

    /**
     * Обработчик нажатия кнопки запуска каскадного кодирования
     */
    @FXML
    protected void onRunCascadeCodingButtonClick() {
        if (inputImage == null) {
            updateStatus("Сначала загрузите изображение", false);
            return;
        }
        
        if (blockCoder == null || blockCoder.getCodeWords() == null || blockCoder.getCodeWords().isEmpty()) {
            updateStatus("Сначала настройте блочный код", false);
            return;
        }

        try {
            // Clear only intermediate data file
            ImageUtils.clearIntermediateData(intermediateDataFile);

            long startTime = System.currentTimeMillis();
            log("Начало каскадного кодирования...");
            log(String.format("Вероятность ошибки: %.2f%%", errorRate.get()));
            log(String.format("Битов затронуто на пиксель: %d", 25 - bitsPerPixel.get()));
            log(String.format("Многопоточность: %s", multiThreadingCheckBox.isSelected() ? "включена" : "выключена"));

            // 1. Convert image to binary data
            long stageStartTime = System.currentTimeMillis();
            log("1. Преобразование изображения в бинарные данные...");
            List<String> binaryRows = ImageUtils.imageToBinary(inputImage);
            saveIntermediateData("Бинарные данные изображения:", binaryRows.subList(0, Math.min(3, binaryRows.size())));
            long stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));

            // 2. Block encoding
            stageStartTime = System.currentTimeMillis();
            log("2. Блочное кодирование...");
            List<String> encodedBlockRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded block encoding
                int numThreads = Runtime.getRuntime().availableProcessors();
                log("Используется многопоточность: " + numThreads + " потоков");
                
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < binaryRows.size(); j += numThreads) {
                            String row = binaryRows.get(j);
                            String encodedRow = blockCoder.encode(row);
                            synchronized (results[threadId]) {
                                results[threadId].add(encodedRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < binaryRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        encodedBlockRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded block encoding
                for (String row : binaryRows) {
                    String encodedRow = blockCoder.encode(row);
                    encodedBlockRows.add(encodedRow);
                }
            }
            
            saveIntermediateData("Блочно закодированные данные:", encodedBlockRows.subList(0, Math.min(3, encodedBlockRows.size())));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));
            
            // Display encoded image
            BufferedImage encodedImage = ImageUtils.binaryToImage(encodedBlockRows, inputImage.getHeight(), inputImage.getWidth());
            blockEncodedImageView.setImage(SwingFXUtils.toFXImage(encodedImage, null));

            // 3. Interleaving
            stageStartTime = System.currentTimeMillis();
            log("3. Перемежение...");
            List<String> interleavedRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded interleaving
                int numThreads = Runtime.getRuntime().availableProcessors();
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < encodedBlockRows.size(); j += numThreads) {
                            String row = encodedBlockRows.get(j);
                            int[] dims = interleaver.calculateDimensions(row.length());
                            interleaver.setDimensions(dims[0], dims[1]);
                            String interleavedRow = interleaver.interleave(row);
                            synchronized (results[threadId]) {
                                results[threadId].add(interleavedRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < encodedBlockRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        interleavedRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded interleaving
                for (String row : encodedBlockRows) {
                    int[] dims = interleaver.calculateDimensions(row.length());
                    interleaver.setDimensions(dims[0], dims[1]);
                    String interleavedRow = interleaver.interleave(row);
                    interleavedRows.add(interleavedRow);
                }
            }
            
            saveIntermediateData("Перемеженные данные:", interleavedRows.subList(0, Math.min(3, interleavedRows.size())));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));

            // 4. Convolutional encoding
            stageStartTime = System.currentTimeMillis();
            log("4. Сверточное кодирование...");
            List<String> convEncodedRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded convolutional encoding
                int numThreads = Runtime.getRuntime().availableProcessors();
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < interleavedRows.size(); j += numThreads) {
                            String row = interleavedRows.get(j);
                            String convEncodedRow = convCoder.convolutionalEncode(row);
                            synchronized (results[threadId]) {
                                results[threadId].add(convEncodedRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < interleavedRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        convEncodedRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded convolutional encoding
                for (String row : interleavedRows) {
                    String convEncodedRow = convCoder.convolutionalEncode(row);
                    convEncodedRows.add(convEncodedRow);
                }
            }
            
            saveIntermediateData("Сверточно закодированные данные:", convEncodedRows.subList(0, Math.min(3, convEncodedRows.size())));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));

            // 5. Introduce errors
            stageStartTime = System.currentTimeMillis();
            log("5. Внесение ошибок...");
            List<String> noisyRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded error introduction
                int numThreads = Runtime.getRuntime().availableProcessors();
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < convEncodedRows.size(); j += numThreads) {
                            String row = convEncodedRows.get(j);
                            // Invert the slider value (25 - slider value)
                            int bitsToAffect = 25 - bitsPerPixel.get();
                            String noisyRow = ImageUtils.introduceErrorsPerPixel(row, errorRate.get() / 100.0, bitsToAffect);
                            synchronized (results[threadId]) {
                                results[threadId].add(noisyRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < convEncodedRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        noisyRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded error introduction
                for (String row : convEncodedRows) {
                    // Invert the slider value (25 - slider value)
                    int bitsToAffect = 25 - bitsPerPixel.get();
                    String noisyRow = ImageUtils.introduceErrorsPerPixel(row, errorRate.get() / 100.0, bitsToAffect);
                    noisyRows.add(noisyRow);
                }
            }
            
            saveIntermediateData("Зашумленные данные:", noisyRows.subList(0, Math.min(3, noisyRows.size())));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));
            
            // Display encoded image with errors
            BufferedImage encodedWithErrorsImage = ImageUtils.binaryToImage(noisyRows, inputImage.getHeight(), inputImage.getWidth());
            blockEncodedWithErrorsImageView.setImage(SwingFXUtils.toFXImage(encodedWithErrorsImage, null));

            // Create noisy image without coding
            List<String> noisyUnencodedRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded error introduction for unencoded image
                int numThreads = Runtime.getRuntime().availableProcessors();
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < binaryRows.size(); j += numThreads) {
                            String row = binaryRows.get(j);
                            // Invert the slider value (25 - slider value)
                            int bitsToAffect = 25 - bitsPerPixel.get();
                            String noisyRow = ImageUtils.introduceErrorsPerPixel(row, errorRate.get() / 100.0, bitsToAffect);
                            synchronized (results[threadId]) {
                                results[threadId].add(noisyRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < binaryRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        noisyUnencodedRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded error introduction for unencoded image
                for (String row : binaryRows) {
                    // Invert the slider value (25 - slider value)
                    int bitsToAffect = 25 - bitsPerPixel.get();
                    String noisyRow = ImageUtils.introduceErrorsPerPixel(row, errorRate.get() / 100.0, bitsToAffect);
                    noisyUnencodedRows.add(noisyRow);
                }
            }
            
            BufferedImage noisyImage = ImageUtils.binaryToImage(noisyUnencodedRows, inputImage.getHeight(), inputImage.getWidth());
            noisyImageView.setImage(SwingFXUtils.toFXImage(noisyImage, null));

            // --- Decoding ---
            log("--- Начало декодирования ---");

            // 6. Convolutional decoding
            stageStartTime = System.currentTimeMillis();
            log("6. Сверточное декодирование...");
            List<String> convDecodedRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded convolutional decoding
                int numThreads = Runtime.getRuntime().availableProcessors();
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < noisyRows.size(); j += numThreads) {
                            String row = noisyRows.get(j);
                            String convDecodedRow = convCoder.viterbiDecode(row);
                            synchronized (results[threadId]) {
                                results[threadId].add(convDecodedRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < noisyRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        convDecodedRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded convolutional decoding
                for (String row : noisyRows) {
                    String convDecodedRow = convCoder.viterbiDecode(row);
                    convDecodedRows.add(convDecodedRow);
                }
            }
            
            saveIntermediateData("Сверточно декодированные данные:", convDecodedRows.subList(0, Math.min(3, convDecodedRows.size())));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));

            // 7. Deinterleaving
            stageStartTime = System.currentTimeMillis();
            log("7. Обратное перемежение...");
            List<String> deinterleavedRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded deinterleaving
                int numThreads = Runtime.getRuntime().availableProcessors();
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < convDecodedRows.size(); j += numThreads) {
                            String row = convDecodedRows.get(j);
                            int[] dims = interleaver.calculateDimensions(row.length());
                            interleaver.setDimensions(dims[0], dims[1]);
                            String deinterleavedRow = interleaver.deinterleave(row);
                            synchronized (results[threadId]) {
                                results[threadId].add(deinterleavedRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < convDecodedRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        deinterleavedRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded deinterleaving
                for (int i = 0; i < convDecodedRows.size(); i++) {
                    String row = convDecodedRows.get(i);
                    int[] dims = interleaver.calculateDimensions(row.length());
                    interleaver.setDimensions(dims[0], dims[1]);
                    String deinterleavedRow = interleaver.deinterleave(row);
                    deinterleavedRows.add(deinterleavedRow);
                }
            }
            
            saveIntermediateData("Обратно перемеженные данные:", deinterleavedRows.subList(0, Math.min(3, deinterleavedRows.size())));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));

            // 8. Block decoding
            stageStartTime = System.currentTimeMillis();
            log("8. Блочное декодирование...");
            List<String> decodedRows = new ArrayList<>();
            
            if (multiThreadingCheckBox.isSelected()) {
                // Multi-threaded block decoding
                int numThreads = Runtime.getRuntime().availableProcessors();
                Thread[] threads = new Thread[numThreads];
                List<String>[] results = new List[numThreads];
                
                for (int i = 0; i < numThreads; i++) {
                    final int threadId = i;
                    results[i] = new ArrayList<>();
                    
                    threads[i] = new Thread(() -> {
                        for (int j = threadId; j < deinterleavedRows.size(); j += numThreads) {
                            String row = deinterleavedRows.get(j);
                            String decodedRow = blockCoder.decode(row);
                            if (decodedRow.length() < binaryRows.get(j).length()) {
                                decodedRow += "0".repeat(binaryRows.get(j).length() - decodedRow.length());
                            } else if (decodedRow.length() > binaryRows.get(j).length()) {
                                decodedRow = decodedRow.substring(0, binaryRows.get(j).length());
                            }
                            synchronized (results[threadId]) {
                                results[threadId].add(decodedRow);
                            }
                        }
                    });
                    threads[i].start();
                }
                
                // Wait for all threads to complete
                for (Thread thread : threads) {
                    try {
                        thread.join();
                    } catch (InterruptedException e) {
                        log("Прерывание потока: " + e.getMessage(), true);
                    }
                }
                
                // Combine results
                for (int i = 0; i < deinterleavedRows.size(); i++) {
                    int threadId = i % numThreads;
                    int index = i / numThreads;
                    if (index < results[threadId].size()) {
                        decodedRows.add(results[threadId].get(index));
                    }
                }
            } else {
                // Single-threaded block decoding
                for (int i = 0; i < deinterleavedRows.size(); i++) {
                    String row = deinterleavedRows.get(i);
                    String decodedRow = blockCoder.decode(row);
                    if (decodedRow.length() < binaryRows.get(i).length()) {
                        decodedRow += "0".repeat(binaryRows.get(i).length() - decodedRow.length());
                    } else if (decodedRow.length() > binaryRows.get(i).length()) {
                        decodedRow = decodedRow.substring(0, binaryRows.get(i).length());
                    }
                    decodedRows.add(decodedRow);
                }
            }
            
            saveIntermediateData("Блочно декодированные данные:", decodedRows.subList(0, Math.min(3, decodedRows.size())));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));

            // 9. Convert binary data back to image and display decoded image
            stageStartTime = System.currentTimeMillis();
            log("9. Преобразование бинарных данных в изображение...");
            BufferedImage decodedImage = ImageUtils.binaryToImage(decodedRows, inputImage.getHeight(), inputImage.getWidth());
            outputImageView.setImage(SwingFXUtils.toFXImage(decodedImage, null));
            stageEndTime = System.currentTimeMillis();
            log(String.format("Этап завершен за %.2f секунд", (stageEndTime - stageStartTime) / 1000.0));

            // Save the result
            ImageUtils.saveImage(decodedImage, outputImagePath);
            
            // Compare original and decoded images
            boolean imagesMatch = compareImages(inputImage, decodedImage);
            int correctedErrors = countCorrectedErrors(binaryRows, decodedRows);
            int uncorrectedErrors = countUncorrectedErrors(binaryRows, decodedRows);
            
            // Update status indicators
            if (imagesMatch) {
                updateStatus("Декодирование успешно", true);
            } else {
                updateStatus("Декодирование не полностью успешно", false);
            }
            updateErrorCountersWithLabels(correctedErrors, uncorrectedErrors);
            
            long endTime = System.currentTimeMillis();
            double totalTime = (endTime - startTime) / 1000.0;
            log("Каскадное кодирование успешно завершено!");
            log(String.format("Общее время выполнения: %.2f секунд", totalTime));
            log("Декодированное изображение сохранено как: " + outputImagePath);
            log("Промежуточные данные сохранены в: " + intermediateDataFile);
            log(String.format("Неисправлено ошибок: %d", uncorrectedErrors));

        } catch (Exception e) {
            log("Ошибка при каскадном кодировании: " + e.getMessage(), true);
            e.printStackTrace();
            updateStatus("Ошибка при кодировании", false);
        }
    }
    
    /**
     * Сравнение двух изображений
     * @param img1 Первое изображение
     * @param img2 Второе изображение
     * @return true если изображения идентичны, false в противном случае
     */
    private boolean compareImages(BufferedImage img1, BufferedImage img2) {
        if (img1.getWidth() != img2.getWidth() || img1.getHeight() != img2.getHeight()) {
            return false;
        }
        
        for (int y = 0; y < img1.getHeight(); y++) {
            for (int x = 0; x < img1.getWidth(); x++) {
                int rgb1 = img1.getRGB(x, y);
                int rgb2 = img2.getRGB(x, y);
                
                // Extract RGB components
                int r1 = (rgb1 >> 16) & 0xFF;
                int g1 = (rgb1 >> 8) & 0xFF;
                int b1 = rgb1 & 0xFF;
                
                int r2 = (rgb2 >> 16) & 0xFF;
                int g2 = (rgb2 >> 8) & 0xFF;
                int b2 = rgb2 & 0xFF;
                
                // Check if all RGB components match
                if (r1 != r2 || g1 != g2 || b1 != b2) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    /**
     * Подсчет исправленных ошибок
     * @param original Исходные данные
     * @param decoded Декодированные данные
     * @return Количество исправленных ошибок
     */
    private int countCorrectedErrors(List<String> original, List<String> decoded) {
        int count = 0;
        
        for (int i = 0; i < Math.min(original.size(), decoded.size()); i++) {
            String origRow = original.get(i);
            String decodedRow = decoded.get(i);
            
            // Count bits that were different in the noisy image but corrected in the decoded image
            for (int j = 0; j < Math.min(origRow.length(), decodedRow.length()); j++) {
                if (origRow.charAt(j) != decodedRow.charAt(j)) {
                    count++;
                }
            }
        }
        
        return count;
    }
    
    /**
     * Подсчет неисправленных ошибок
     * @param original Исходные данные
     * @param decoded Декодированные данные
     * @return Количество неисправленных ошибок
     */
    private int countUncorrectedErrors(List<String> original, List<String> decoded) {
        int count = 0;
        
        for (int i = 0; i < Math.min(original.size(), decoded.size()); i++) {
            String origRow = original.get(i);
            String decodedRow = decoded.get(i);
            
            // Count bits that are still different in the decoded image
            for (int j = 0; j < Math.min(origRow.length(), decodedRow.length()); j++) {
                if (origRow.charAt(j) != decodedRow.charAt(j)) {
                    count++;
                }
            }
        }
        
        return count;
    }

    /**
     * Обработчик нажатия кнопки очистки лога
     */
    @FXML
    protected void onClearLogButtonClick() {
        clearLog();
    }

    /**
     * Обработчик нажатия кнопки сохранения лога
     */
    @FXML
    protected void onSaveLogButtonClick() {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Save Log File");
        fileChooser.getExtensionFilters().add(
            new FileChooser.ExtensionFilter("Text files (*.txt)", "*.txt")
        );

        File file = fileChooser.showSaveDialog(logTextArea.getScene().getWindow());
        if (file != null) {
            try {
                java.nio.file.Files.writeString(file.toPath(), logTextArea.getText());
                log("Log saved to: " + file.getName());
            } catch (IOException e) {
                log("Error saving log: " + e.getMessage(), true);
            }
        }
    }

    /**
     * Обработчик нажатия кнопки открытия файла с промежуточными данными
     */
    @FXML
    protected void onOpenIntermediateDataButtonClick() {
        File file = new File(intermediateDataFile);
        if (file.exists()) {
            try {
                java.awt.Desktop.getDesktop().open(file);
            } catch (IOException e) {
                log("Error opening intermediate data file: " + e.getMessage(), true);
            }
        } else {
            log("Intermediate data file does not exist. Run cascade coding first.", true);
        }
    }

    /**
     * Добавление сообщения в лог
     * @param message Сообщение для добавления
     */
    private void log(String message) {
        log(message, false);
    }

    /**
     * Добавление сообщения в лог с указанием типа
     * @param message Сообщение для добавления
     * @param isError true если это сообщение об ошибке
     */
    private void log(String message, boolean isError) {
        String prefix = isError ? "ERROR: " : "";
        logTextArea.appendText(prefix + message + "\n");
        logTextArea.setScrollTop(Double.MAX_VALUE); // Прокрутка вниз
    }

    /**
     * Очистка лога
     */
    private void clearLog() {
        logTextArea.clear();
    }

    /**
     * Сохранение промежуточных данных
     * @param header Заголовок данных
     * @param data Список данных для сохранения
     */
    private void saveIntermediateData(String header, List<String> data) {
        ImageUtils.saveIntermediateData(header, intermediateDataFile);
        for (int i = 0; i < data.size(); i++) {
            String row = data.get(i);
            ImageUtils.saveIntermediateData(
                String.format("Row %d (first 100 bits): %s...",
                    i, row.substring(0, Math.min(100, row.length()))),
                intermediateDataFile
            );
        }
    }

    /**
     * Сброс счетчиков ошибок
     */
    private void resetErrorCounters() {
        uncorrectedErrorsLabel.setText("0");
        imageMatchPercentLabel.setText("0%");
    }

    /**
     * Обновление счетчиков ошибок с метками
     * @param correctedErrors Количество исправленных ошибок
     * @param uncorrectedErrors Количество неисправленных ошибок
     */
    private void updateErrorCountersWithLabels(int correctedErrors, int uncorrectedErrors) {
        uncorrectedErrorsLabel.setText(String.valueOf(uncorrectedErrors));
        
        // Calculate image match percentage based on RGB pixel matching
        if (inputImage != null && outputImageView.getImage() != null) {
            BufferedImage decodedImage = SwingFXUtils.fromFXImage(outputImageView.getImage(), null);
            double matchPercent = calculateImageMatchPercentage(inputImage, decodedImage);
            imageMatchPercentLabel.setText(String.format("%.2f%%", matchPercent));
        }
    }

    /**
     * Вычисление процента соответствия изображений
     * @param original Исходное изображение
     * @param decoded Декодированное изображение
     * @return Процент соответствия
     */
    private double calculateImageMatchPercentage(BufferedImage original, BufferedImage decoded) {
        if (original.getWidth() != decoded.getWidth() || original.getHeight() != decoded.getHeight()) {
            return 0.0;
        }

        int totalPixels = original.getWidth() * original.getHeight();
        int matchingPixels = 0;

        for (int y = 0; y < original.getHeight(); y++) {
            for (int x = 0; x < original.getWidth(); x++) {
                int rgb1 = original.getRGB(x, y);
                int rgb2 = decoded.getRGB(x, y);
                
                // Extract RGB components
                int r1 = (rgb1 >> 16) & 0xFF;
                int g1 = (rgb1 >> 8) & 0xFF;
                int b1 = rgb1 & 0xFF;
                
                int r2 = (rgb2 >> 16) & 0xFF;
                int g2 = (rgb2 >> 8) & 0xFF;
                int b2 = rgb2 & 0xFF;
                
                // Check if all RGB components match
                if (r1 == r2 && g1 == g2 && b1 == b2) {
                    matchingPixels++;
                }
            }
        }

        return (matchingPixels * 100.0) / totalPixels;
    }
}