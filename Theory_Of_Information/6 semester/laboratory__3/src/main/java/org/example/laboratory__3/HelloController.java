package org.example.laboratory__3;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;

import org.example.laboratory__3.coding.BlockCoder;
import org.example.laboratory__3.coding.BlockInterleaver;
import org.example.laboratory__3.coding.ConvolutionalCoder;
import org.example.laboratory__3.utils.ImageUtils;
import org.example.laboratory__3.utils.ParallelProcessor;

import javafx.application.Platform;
import javafx.embed.swing.SwingFXUtils;
import javafx.fxml.FXML;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.control.RadioButton;
import javafx.scene.control.Slider;
import javafx.scene.control.TextArea;
import javafx.scene.control.ToggleGroup;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;

public class HelloController {
    @FXML private ImageView inputImageView;
    @FXML private ImageView outputImageView;
    @FXML private ImageView noisyImageView;
    @FXML private ImageView blockEncodedImageView;
    @FXML private ImageView blockEncodedWithErrorsImageView;
    @FXML private Slider errorRateSlider;
    @FXML private Label errorRateLabel;
    @FXML private ToggleGroup matrixTypeGroup;
    @FXML private TextArea matrixTextArea;
    @FXML private Label nLabel;
    @FXML private Label kLabel;
    @FXML private Label dminLabel;
    @FXML private Label tLabel;
    @FXML private TextArea polynomialsTextArea;
    @FXML private CheckBox verboseCheckBox;
    @FXML private CheckBox saveIntermediateImagesCheckBox;
    @FXML private TextArea logTextArea;
    @FXML private ProgressBar progressBar;
    @FXML private Label progressLabel;
    @FXML private VBox buttonContainer;

    private String inputImagePath;
    private String outputImagePath = "output_decoded.png";
    private String intermediateDataFile = "intermediate_data.txt";
    private BufferedImage inputImage;
    private AtomicReference<Double> errorRate = new AtomicReference<>(10.0);

    private BlockCoder blockCoder;
    private ConvolutionalCoder convCoder;
    private BlockInterleaver interleaver;

    @FXML
    public void initialize() {
        // Initialize coders with default constructors
        blockCoder = new BlockCoder();
        
        // Initialize convolutional coder with default parameters
        List<String> defaultPolynomials = Arrays.asList("111", "101"); // Example polynomials in binary
        convCoder = new ConvolutionalCoder(defaultPolynomials, 3); // Constraint length of 3
        
        interleaver = new BlockInterleaver();

        // Initialize error rate slider
        errorRateSlider.setMin(0);
        errorRateSlider.setMax(100);
        errorRateSlider.setValue(10);
        errorRateSlider.setMajorTickUnit(10);
        errorRateSlider.setMinorTickCount(1);
        errorRateSlider.setShowTickLabels(true);
        errorRateSlider.setShowTickMarks(true);

        // Initialize error rate
        errorRate = new AtomicReference<>(10.0); // 10% по умолчанию
        errorRateLabel.setText("Error Rate: 10%");

        // Add listener to error rate slider
        errorRateSlider.valueProperty().addListener((observable, oldValue, newValue) -> {
            double percentage = newValue.doubleValue();
            errorRate.set(percentage);
            errorRateLabel.setText(String.format("Error Rate: %.1f%%", percentage));
        });

        // Clear intermediate data file
        ImageUtils.clearIntermediateData(intermediateDataFile);
    }

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

    @FXML
    protected void onSetupBlockCodeButtonClick() {
        try {
            String[] matrixRows = matrixTextArea.getText().trim().split("\n");
            List<String> matrix = new ArrayList<>(Arrays.asList(matrixRows));

            // Check matrix
            String matrixType = ((RadioButton)matrixTypeGroup.getSelectedToggle()).getText().startsWith("G") ? "G" : "H";

            if (matrix.isEmpty()) {
                throw new IllegalArgumentException("Matrix is empty");
            }

            for (String row : matrix) {
                if (!row.matches("[01]+")) {
                    throw new IllegalArgumentException("Matrix must contain only 0s and 1s");
                }
            }

            // Setup block code
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

    @FXML
    protected void onSetupConvolutionalCodeButtonClick() {
        try {
            String[] polyLines = polynomialsTextArea.getText().trim().split("\n");
            List<String> polynomials = new ArrayList<>();

            for (String line : polyLines) {
                if (!line.trim().isEmpty()) {
                    // Remove all whitespace and split by commas
                    String[] values = line.trim().replaceAll("\\s+", "").split(",");
                    
                    // Convert array of values to a single polynomial
                    StringBuilder polyBuilder = new StringBuilder();
                    for (String value : values) {
                        if (value.matches("^[0-9]+$")) {
                            // Convert decimal to binary
                            int decimalValue = Integer.parseInt(value);
                            String binaryValue = Integer.toBinaryString(decimalValue);
                            polyBuilder.append(binaryValue);
                        } else {
                            log("Warning: Invalid polynomial value '" + value + "'. Only decimal numbers are allowed.", true);
                        }
                    }
                    
                    // Add the polynomial if it's not empty
                    if (polyBuilder.length() > 0) {
                        polynomials.add(polyBuilder.toString());
                    }
                }
            }

            if (polynomials.isEmpty()) {
                throw new IllegalArgumentException("No valid polynomials could be converted");
            }

            // Create a new convolutional coder with the specified polynomials
            convCoder = new ConvolutionalCoder(polynomials, 3); // Using constraint length of 3

            log("Convolutional code setup: " + polynomials.size() + " polynomials");
            StringBuilder sb = new StringBuilder("Polynomials: ");
            for (int i = 0; i < polynomials.size(); i++) {
                sb.append(polynomials.get(i));
                if (i < polynomials.size() - 1) {
                    sb.append(", ");
                }
            }
            log(sb.toString());

        } catch (Exception e) {
            log("Error setting up convolutional code: " + e.getMessage(), true);
        }
    }

    /**
     * Save intermediate image if the checkbox is selected
     * @param image The image to save
     * @param stageNumber The stage number
     * @param stageName The name of the processing stage
     * @return true if the image was saved, false otherwise
     */
    private boolean saveIntermediateImage(BufferedImage image, int stageNumber, String stageName) {
        if (saveIntermediateImagesCheckBox.isSelected() && image != null) {
            try {
                String fileName = String.format("intermediate_%02d_%s.png", stageNumber, stageName);
                ImageUtils.saveImage(image, fileName);
                log("Saved intermediate image: " + fileName);
                return true;
            } catch (Exception e) {
                log("Error saving intermediate image: " + e.getMessage(), true);
                return false;
            }
        }
        return false;
    }

    @FXML
    private void onRunCascadeCodingButtonClick() {
        if (inputImage == null) {
            showError("Please load an image first");
            return;
        }

        // Reset progress
        progressBar.setProgress(0);
        progressLabel.setText("0%");

        // Save original image as intermediate
        saveIntermediateImage(inputImage, 0, "original");

        long startTime = System.currentTimeMillis();
        long stageStartTime, stageEndTime;
        
        // Общее количество этапов для расчета прогресса
        final int totalStages = 12; // 0-11 этапы
        final AtomicInteger currentStage = new AtomicInteger(0);
        
        // Функция для обновления прогресса
        Runnable updateProgress = () -> {
            double progress = (double) currentStage.get() / totalStages;
            Platform.runLater(() -> {
                progressBar.setProgress(progress);
                progressLabel.setText(String.format("%.0f%%", progress * 100));
            });
        };
        
        // 1. Convert image to binary
        stageStartTime = System.currentTimeMillis();
        log("1. Converting image to binary...");
        List<String> binaryRows = ImageUtils.imageToBinary(inputImage);
        stageEndTime = System.currentTimeMillis();
        log(String.format("Binary conversion completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        saveIntermediateData("Binary data:", binaryRows.subList(0, Math.min(3, binaryRows.size())));
        currentStage.incrementAndGet();
        updateProgress.run();

        // Display binary image
        BufferedImage binaryImage = ImageUtils.binaryToImage(binaryRows, inputImage.getHeight(), inputImage.getWidth());
        saveIntermediateImage(binaryImage, 2, "binary");
        currentStage.incrementAndGet();
        updateProgress.run();

        // 2. Block encoding
        stageStartTime = System.currentTimeMillis();
        log("2. Block encoding...");
        List<String> encodedBlockRows = new ArrayList<>();
        
        for (String row : binaryRows) {
            StringBuilder encodedRow = new StringBuilder();
            int blockLength = blockCoder.getN(); // Get the block length (n)
            int infoLength = blockCoder.getK(); // Get the information length (k)
            
            // Process the row in blocks of length k (information length)
            for (int i = 0; i < row.length(); i += infoLength) {
                // Get a block of length k, padding with zeros if necessary
                String infoBlock = row.substring(i, Math.min(i + infoLength, row.length()));
                if (infoBlock.length() < infoLength) {
                    infoBlock = infoBlock + "0".repeat(infoLength - infoBlock.length());
                }
                
                try {
                    // Encode the information block
                    String encodedBlock = blockCoder.encode(infoBlock);
                    encodedRow.append(encodedBlock);
                } catch (IllegalArgumentException e) {
                    log("Warning: Block encoding error: " + e.getMessage(), true);
                    // If encoding fails, pad with zeros
                    encodedRow.append("0".repeat(blockLength));
                }
            }
            
            encodedBlockRows.add(encodedRow.toString());
        }
        
        stageEndTime = System.currentTimeMillis();
        log(String.format("Block encoding completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        saveIntermediateData("Block encoded data:", encodedBlockRows.subList(0, Math.min(3, encodedBlockRows.size())));

        // Display block encoded image
        BufferedImage blockEncodedImage = ImageUtils.binaryToImage(encodedBlockRows, inputImage.getHeight(), inputImage.getWidth());
        blockEncodedImageView.setImage(SwingFXUtils.toFXImage(blockEncodedImage, null));
        log("Block encoded image displayed");
        saveIntermediateImage(blockEncodedImage, 3, "block_encoded");
        currentStage.incrementAndGet();
        updateProgress.run();

        // 3. Interleaving
        stageStartTime = System.currentTimeMillis();
        log("3. Interleaving...");
        List<String> interleavedRows = new ArrayList<>();
        for (String row : encodedBlockRows) {
            int[] dims = interleaver.calculateDimensions(row.length());
            interleaver.setDimensions(dims[0], dims[1]);
            String interleavedRow = interleaver.interleave(row);
            interleavedRows.add(interleavedRow);
        }
        stageEndTime = System.currentTimeMillis();
        log(String.format("Interleaving completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        saveIntermediateData("Interleaved data:", interleavedRows.subList(0, Math.min(3, interleavedRows.size())));

        // Display interleaved image
        BufferedImage interleavedImage = ImageUtils.binaryToImage(interleavedRows, inputImage.getHeight(), inputImage.getWidth());
        saveIntermediateImage(interleavedImage, 4, "interleaved");
        currentStage.incrementAndGet();
        updateProgress.run();

        // 4. Convolutional encoding
        stageStartTime = System.currentTimeMillis();
        log("4. Convolutional encoding...");
        List<String> convEncodedRows = ParallelProcessor.processParallelWithProgress(
            interleavedRows,
            row -> convCoder.encode(row),
            completed -> {
                // Обновляем прогресс внутри этапа
                double stageProgress = (double) completed / interleavedRows.size();
                double totalProgress = (currentStage.get() + stageProgress) / totalStages;
                Platform.runLater(() -> {
                    progressBar.setProgress(totalProgress);
                    progressLabel.setText(String.format("%.0f%%", totalProgress * 100));
                });
                return null;
            }
        );
        stageEndTime = System.currentTimeMillis();
        log(String.format("Convolutional encoding completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        saveIntermediateData("Convolutional encoded data:", convEncodedRows.subList(0, Math.min(3, convEncodedRows.size())));

        // Display convolutional encoded image
        BufferedImage convEncodedImage = ImageUtils.binaryToImage(convEncodedRows, inputImage.getHeight(), inputImage.getWidth());
        saveIntermediateImage(convEncodedImage, 5, "conv_encoded");
        currentStage.incrementAndGet();
        updateProgress.run();

        // 5. Introduce errors to encoded data
        stageStartTime = System.currentTimeMillis();
        log("5. Introducing errors to encoded data...");
        List<String> noisyEncodedRows = new ArrayList<>();
        double errorProbability = errorRate.get() / 100.0; // Convert percentage to probability
        for (String row : convEncodedRows) {
            noisyEncodedRows.add(ImageUtils.introduceErrors(row, errorProbability));
        }
        stageEndTime = System.currentTimeMillis();
        log(String.format("Error introduction completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        log(String.format("Using error probability: %.2f%%", errorRate.get()));
        saveIntermediateData("Noisy encoded data:", noisyEncodedRows.subList(0, Math.min(3, noisyEncodedRows.size())));

        // Display noisy encoded image
        BufferedImage noisyEncodedImage = ImageUtils.binaryToImage(noisyEncodedRows, inputImage.getHeight(), inputImage.getWidth());
        blockEncodedWithErrorsImageView.setImage(SwingFXUtils.toFXImage(noisyEncodedImage, null));
        log("Noisy encoded image displayed");
        saveIntermediateImage(noisyEncodedImage, 6, "noisy_encoded");
        currentStage.incrementAndGet();
        updateProgress.run();

        // Create noisy image by decoding the noisy encoded data without error correction
        log("Creating noisy image by decoding noisy encoded data without error correction...");
        List<String> noisyDecodedRows = new ArrayList<>();
        
        // 6. Deinterleaving without error correction
        for (int i = 0; i < noisyEncodedRows.size(); i++) {
            String row = noisyEncodedRows.get(i);
            
            // Calculate optimal dimensions for this row
            int[] dims = interleaver.calculateDimensions(row.length());
            
            // Set dimensions and deinterleave
            interleaver.setDimensions(dims[0], dims[1]);
            String deinterleavedRow = interleaver.deinterleave(row);
            
            noisyDecodedRows.add(deinterleavedRow);
        }
        
        // 7. Block decoding without error correction
        List<String> noisyBlockDecodedRows = new ArrayList<>();
        for (String row : noisyDecodedRows) {
            StringBuilder decodedRow = new StringBuilder();
            int blockLength = blockCoder.getN(); // Get the block length (n)
            int infoLength = blockCoder.getK(); // Get the information length (k)
            
            // Process the row in blocks of length n
            for (int i = 0; i < row.length(); i += blockLength) {
                // Get a block of length n, padding with zeros if necessary
                String block = row.substring(i, Math.min(i + blockLength, row.length()));
                if (block.length() < blockLength) {
                    block = block + "0".repeat(blockLength - block.length());
                }
                
                // Just take the first k bits without error correction
                decodedRow.append(block.substring(0, Math.min(infoLength, block.length())));
            }
            
            noisyBlockDecodedRows.add(decodedRow.toString());
        }
        
        // Create noisy image from decoded data without error correction
        BufferedImage noisyImage = ImageUtils.binaryToImage(noisyBlockDecodedRows, inputImage.getHeight(), inputImage.getWidth());
        noisyImageView.setImage(SwingFXUtils.toFXImage(noisyImage, null));
        log("Noisy image displayed (decoded without error correction)");
        saveIntermediateImage(noisyImage, 7, "noisy");
        currentStage.incrementAndGet();
        updateProgress.run();

        // --- Decoding with error correction ---
        log("Starting decoding process with error correction...");

        // 8. Convolutional decoding (Viterbi)
        stageStartTime = System.currentTimeMillis();
        log("8. Convolutional decoding...");
        List<String> convDecodedRows = ParallelProcessor.processParallelWithProgress(
            noisyEncodedRows,
            row -> {
                // Apply Viterbi decoding to correct errors
                String decoded = convCoder.decode(row);
                return decoded;
            },
            completed -> {
                // Обновляем прогресс внутри этапа
                double stageProgress = (double) completed / noisyEncodedRows.size();
                double totalProgress = (currentStage.get() + stageProgress) / totalStages;
                Platform.runLater(() -> {
                    progressBar.setProgress(totalProgress);
                    progressLabel.setText(String.format("%.0f%%", totalProgress * 100));
                });
                return null;
            }
        );
        stageEndTime = System.currentTimeMillis();
        log(String.format("Convolutional decoding completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        saveIntermediateData("Convolutional decoded data:", convDecodedRows.subList(0, Math.min(3, convDecodedRows.size())));

        // Display convolutional decoded image
        BufferedImage convDecodedImage = ImageUtils.binaryToImage(convDecodedRows, inputImage.getHeight(), inputImage.getWidth());
        saveIntermediateImage(convDecodedImage, 8, "conv_decoded");
        currentStage.incrementAndGet();
        updateProgress.run();

        // 9. Deinterleaving
        stageStartTime = System.currentTimeMillis();
        log("9. Deinterleaving...");
        List<String> deinterleavedRows = new ArrayList<>();
        for (int i = 0; i < convDecodedRows.size(); i++) {
            String row = convDecodedRows.get(i);
            
            // Calculate optimal dimensions for this row
            int[] dims = interleaver.calculateDimensions(row.length());
            log("Row " + i + " deinterleaving dimensions: " + dims[0] + "x" + dims[1]);
            
            // Set dimensions and deinterleave
            interleaver.setDimensions(dims[0], dims[1]);
            String deinterleavedRow = interleaver.deinterleave(row);
            
            // Log the first few characters for debugging
            if (i < 3) {
                log("Row " + i + " first 20 chars before deinterleaving: " + 
                    (row.length() > 20 ? row.substring(0, 20) + "..." : row));
                log("Row " + i + " first 20 chars after deinterleaving: " + 
                    (deinterleavedRow.length() > 20 ? deinterleavedRow.substring(0, 20) + "..." : deinterleavedRow));
            }
            
            deinterleavedRows.add(deinterleavedRow);
        }
        stageEndTime = System.currentTimeMillis();
        log(String.format("Deinterleaving completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        saveIntermediateData("Deinterleaved data:", deinterleavedRows.subList(0, Math.min(3, deinterleavedRows.size())));

        // Display deinterleaved image
        BufferedImage deinterleavedImage = ImageUtils.binaryToImage(deinterleavedRows, inputImage.getHeight(), inputImage.getWidth());
        saveIntermediateImage(deinterleavedImage, 9, "deinterleaved");
        currentStage.incrementAndGet();
        updateProgress.run();

        // 10. Block decoding
        stageStartTime = System.currentTimeMillis();
        log("10. Block decoding...");
        List<String> decodedRows = new ArrayList<>();
        
        for (String row : deinterleavedRows) {
            StringBuilder decodedRow = new StringBuilder();
            int blockLength = blockCoder.getN(); // Get the block length (n)
            int infoLength = blockCoder.getK(); // Get the information length (k)
            
            // Process the row in blocks of length n
            for (int i = 0; i < row.length(); i += blockLength) {
                // Get a block of length n, padding with zeros if necessary
                String block = row.substring(i, Math.min(i + blockLength, row.length()));
                if (block.length() < blockLength) {
                    block = block + "0".repeat(blockLength - block.length());
                }
                
                try {
                    // Decode the block and get only the information bits
                    String decodedBlock = blockCoder.decode(block);
                    decodedRow.append(decodedBlock.substring(0, Math.min(infoLength, decodedBlock.length())));
                } catch (IllegalArgumentException e) {
                    log("Warning: Block decoding error: " + e.getMessage(), true);
                    // If decoding fails, use the first k bits of the original block
                    decodedRow.append(block.substring(0, Math.min(infoLength, block.length())));
                }
            }
            
            decodedRows.add(decodedRow.toString());
        }
        
        stageEndTime = System.currentTimeMillis();
        log(String.format("Block decoding completed in %.2f seconds", (stageEndTime - stageStartTime) / 1000.0));
        saveIntermediateData("Decoded data:", decodedRows.subList(0, Math.min(3, decodedRows.size())));

        // Display block decoded image
        BufferedImage blockDecodedImage = ImageUtils.binaryToImage(decodedRows, inputImage.getHeight(), inputImage.getWidth());
        saveIntermediateImage(blockDecodedImage, 10, "block_decoded");
        currentStage.incrementAndGet();
        updateProgress.run();

        // 11. Convert back to image and display in output image view
        stageStartTime = System.currentTimeMillis();
        log("11. Converting decoded data back to image...");
        
        // Ensure the decoded data has the correct length
        for (int i = 0; i < decodedRows.size(); i++) {
            String decodedRow = decodedRows.get(i);
            
            // If the decoded row is shorter than expected, pad with zeros
            int expectedLength = 24 * inputImage.getWidth(); // 24 bits per pixel
            if (decodedRow.length() < expectedLength) {
                decodedRow = decodedRow + "0".repeat(expectedLength - decodedRow.length());
                decodedRows.set(i, decodedRow);
            }
            // If the decoded row is longer than expected, truncate
            else if (decodedRow.length() > expectedLength) {
                decodedRow = decodedRow.substring(0, expectedLength);
                decodedRows.set(i, decodedRow);
            }
        }
        
        // Create decoded image
        BufferedImage decodedImage = new BufferedImage(inputImage.getWidth(), inputImage.getHeight(), BufferedImage.TYPE_INT_RGB);
        
        // Process each row of binary data
        for (int y = 0; y < inputImage.getHeight(); y++) {
            String binaryRow = decodedRows.get(y);
            
            // Process each pixel (24 bits per pixel - 8 for each RGB component)
            for (int x = 0; x < inputImage.getWidth(); x++) {
                int pixelIndex = x * 24;
                
                // Extract RGB values from binary string
                int r = Integer.parseInt(binaryRow.substring(pixelIndex, pixelIndex + 8), 2);
                int g = Integer.parseInt(binaryRow.substring(pixelIndex + 8, pixelIndex + 16), 2);
                int b = Integer.parseInt(binaryRow.substring(pixelIndex + 16, pixelIndex + 24), 2);
                
                // Create RGB color
                int rgb = (r << 16) | (g << 8) | b;
                
                // Set pixel in the image
                decodedImage.setRGB(x, y, rgb);
            }
        }
        
        // Display decoded image
        outputImageView.setImage(SwingFXUtils.toFXImage(decodedImage, null));
        log("Decoded image displayed");
        
        // Save decoded image as intermediate
        saveIntermediateImage(decodedImage, 11, "final");
        currentStage.incrementAndGet();
        updateProgress.run();
        
        // Save decoded image
        try {
            ImageUtils.saveImage(decodedImage, outputImagePath);
            log("Decoded image saved to: " + outputImagePath);
        } catch (Exception e) {
            log("Error saving decoded image: " + e.getMessage(), true);
        }
        
        stageEndTime = System.currentTimeMillis();
        log(String.format("Image conversion completed in %.2f seconds", (stageEndTime - startTime) / 1000.0));
        
        // Print total processing time
        long totalTime = System.currentTimeMillis() - startTime;
        log(String.format("Total processing time: %.2f seconds", totalTime / 1000.0));
        log("Cascade coding completed successfully!");
        
        // Устанавливаем прогресс-бар на 100% в конце
        Platform.runLater(() -> {
            progressBar.setProgress(1.0);
            progressLabel.setText("100%");
        });
    }

    @FXML
    protected void onClearLogButtonClick() {
        clearLog();
    }

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
                String logContent = logTextArea.getText();
                if (logContent != null && !logContent.isEmpty()) {
                    java.nio.file.Files.writeString(file.toPath(), logContent);
                    log("Log saved to: " + file.getName());
                } else {
                    log("No log content to save", true);
                }
            } catch (IOException e) {
                log("Error saving log: " + e.getMessage(), true);
            }
        }
    }

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

    private void log(String message) {
        log(message, false);
    }

    private void log(String message, boolean isError) {
        String prefix = isError ? "ERROR: " : "";
        Platform.runLater(() -> {
            try {
                logTextArea.appendText(prefix + message + "\n");
                logTextArea.setScrollTop(Double.MAX_VALUE);
            } catch (Exception e) {
                System.err.println("Error updating log: " + e.getMessage());
            }
        });
    }

    private void clearLog() {
        Platform.runLater(() -> {
            try {
                logTextArea.clear();
            } catch (Exception e) {
                System.err.println("Error clearing log: " + e.getMessage());
            }
        });
    }

    private void saveIntermediateData(String header, List<String> data) {
        ImageUtils.saveIntermediateData(header, intermediateDataFile);
        for (int i = 0; i < data.size(); i++) {
            String row = data.get(i);
            int displayLength = Math.min(100, row.length());
            ImageUtils.saveIntermediateData(
                String.format("Row %d (first %d bits): %s...",
                    i, displayLength, row.substring(0, displayLength)),
                intermediateDataFile
            );
        }
    }

    private void showError(String message) {
        log(message, true);
    }
}