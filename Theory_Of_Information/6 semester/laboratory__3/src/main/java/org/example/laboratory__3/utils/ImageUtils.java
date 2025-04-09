package org.example.laboratory__3.utils;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import javax.imageio.ImageIO;

public class ImageUtils {
    
    /**
     * Load an image from a file and convert it to a BufferedImage
     */
    public static BufferedImage loadImage(String filePath) {
        try {
            return ImageIO.read(new File(filePath));
        } catch (IOException e) {
            System.err.println("Error loading image: " + e.getMessage());
            return null;
        }
    }
    
    /**
     * Save a BufferedImage to a file
     */
    public static boolean saveImage(BufferedImage img, String filePath) {
        try {
            return ImageIO.write(img, "png", new File(filePath));
        } catch (IOException e) {
            System.err.println("Error saving image: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * Convert an integer to a binary string of specified length
     */
    public static String intToBinary(int n, int bits) {
        // Ensure the number is non-negative and within range
        n = Math.max(0, Math.min(n, (1 << bits) - 1));
        return String.format("%" + bits + "s", Integer.toBinaryString(n)).replace(' ', '0');
    }
    
    /**
     * Convert a binary string to an integer
     */
    public static int binaryToInt(String binaryStr) {
        if (binaryStr == null || binaryStr.isEmpty()) {
            return 0;
        }
        try {
            return Integer.parseInt(binaryStr, 2);
        } catch (NumberFormatException e) {
            System.err.println("Error parsing binary string: " + binaryStr);
            return 0;
        }
    }
    
    /**
     * Convert a pixel (RGB) to a binary string
     */
    public static String pixelToBinary(int r, int g, int b) {
        // Ensure RGB values are within valid range
        r = Math.max(0, Math.min(255, r));
        g = Math.max(0, Math.min(255, g));
        b = Math.max(0, Math.min(255, b));
        
        return intToBinary(r, 8) + intToBinary(g, 8) + intToBinary(b, 8);
    }
    
    /**
     * Convert a binary string to a pixel (RGB)
     */
    public static int[] binaryToPixel(String binaryStr) {
        if (binaryStr == null || binaryStr.length() != 24) {
            System.err.println("Invalid binary string length for RGB pixel: " + 
                             (binaryStr == null ? "null" : binaryStr.length()));
            return new int[]{0, 0, 0};
        }
        
        try {
            int r = binaryToInt(binaryStr.substring(0, 8));
            int g = binaryToInt(binaryStr.substring(8, 16));
            int b = binaryToInt(binaryStr.substring(16, 24));
            
            // Ensure RGB values are within valid range
            r = Math.max(0, Math.min(255, r));
            g = Math.max(0, Math.min(255, g));
            b = Math.max(0, Math.min(255, b));
            
            return new int[]{r, g, b};
        } catch (Exception e) {
            System.err.println("Error converting binary to pixel: " + e.getMessage());
            return new int[]{0, 0, 0};
        }
    }
    
    /**
     * Convert an image to a list of binary strings (one per row)
     * Each pixel is represented as a 24-bit information word (8 bits each for R,G,B)
     */
    public static List<String> imageToBinary(BufferedImage img) {
        List<String> binaryRows = new ArrayList<>();
        int width = img.getWidth();
        int height = img.getHeight();
        
        for (int y = 0; y < height; y++) {
            StringBuilder row = new StringBuilder();
            for (int x = 0; x < width; x++) {
                int rgb = img.getRGB(x, y);
                // Маскируем альфа-канал и получаем только RGB компоненты
                rgb = rgb & 0x00FFFFFF;
                int r = (rgb >> 16) & 0xFF;
                int g = (rgb >> 8) & 0xFF;
                int b = rgb & 0xFF;
                row.append(pixelToBinary(r, g, b));
            }
            binaryRows.add(row.toString());
        }
        
        return binaryRows;
    }
    
    /**
     * Convert a list of binary strings back to an image
     * Each 24-bit information word represents a pixel (8 bits each for R,G,B)
     */
    public static BufferedImage binaryToImage(List<String> binaryRows, int height, int width) {
        BufferedImage img = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        
        for (int y = 0; y < height && y < binaryRows.size(); y++) {
            String row = binaryRows.get(y);
            int expectedLength = width * 24; // 24 bits per pixel (8 bits each for R,G,B)
            
            // Ensure row has correct length
            if (row.length() < expectedLength) {
                row = row + "0".repeat(expectedLength - row.length());
            } else if (row.length() > expectedLength) {
                row = row.substring(0, expectedLength);
            }
            
            for (int x = 0; x < width; x++) {
                try {
                    String pixelBinary = row.substring(x * 24, (x + 1) * 24);
                    int[] rgb = binaryToPixel(pixelBinary);
                    
                    // Проверка на допустимые значения RGB
                    rgb[0] = Math.max(0, Math.min(255, rgb[0]));
                    rgb[1] = Math.max(0, Math.min(255, rgb[1]));
                    rgb[2] = Math.max(0, Math.min(255, rgb[2]));
                    
                    // Устанавливаем альфа-канал в 255 (полностью непрозрачный)
                    int rgbValue = (255 << 24) | (rgb[0] << 16) | (rgb[1] << 8) | rgb[2];
                    img.setRGB(x, y, rgbValue);
                } catch (Exception e) {
                    System.err.println("Error processing pixel at (" + x + ", " + y + "): " + e.getMessage());
                    // Set to black in case of error
                    img.setRGB(x, y, 0xFF000000); // Black with full opacity
                }
            }
        }
        
        return img;
    }
    
    /**
     * Save intermediate data to a file
     */
    public static void saveIntermediateData(String data, String filename) {
        try {
            java.io.FileWriter writer = new java.io.FileWriter(filename, true);
            writer.write(data + "\n");
            writer.close();
        } catch (IOException e) {
            System.err.println("Error saving intermediate data: " + e.getMessage());
        }
    }
    
    /**
     * Clear intermediate data file
     */
    public static void clearIntermediateData(String filename) {
        try {
            java.io.FileWriter writer = new java.io.FileWriter(filename, false);
            writer.write("");
            writer.close();
        } catch (IOException e) {
            System.err.println("Error clearing intermediate data: " + e.getMessage());
        }
    }
    
    /**
     * Introduce random errors in a binary string with given probability
     * Errors are introduced per pixel (24-bit information word)
     */
    public static String introduceErrors(String binaryStr, double errorRate) {
        if (errorRate <= 0) return binaryStr;
        if (errorRate >= 1) {
            // Инвертируем все биты
            StringBuilder result = new StringBuilder(binaryStr);
            for (int i = 0; i < result.length(); i++) {
                result.setCharAt(i, result.charAt(i) == '0' ? '1' : '0');
            }
            return result.toString();
        }

        Random random = new Random();
        StringBuilder result = new StringBuilder(binaryStr);
        
        // Вносим ошибки с учетом структуры пикселей (24 бита на пиксель)
        int pixelCount = binaryStr.length() / 24;
        
        // Рассчитываем ожидаемое количество ошибок
        int expectedErrors = (int)(pixelCount * errorRate);
        
        // Создаем массив индексов пикселей
        List<Integer> pixelIndices = new ArrayList<>();
        for (int i = 0; i < pixelCount; i++) {
            pixelIndices.add(i);
        }
        
        // Перемешиваем индексы
        for (int i = pixelIndices.size() - 1; i > 0; i--) {
            int j = random.nextInt(i + 1);
            int temp = pixelIndices.get(i);
            pixelIndices.set(i, pixelIndices.get(j));
            pixelIndices.set(j, temp);
        }
        
        // Вносим ошибки в случайные биты выбранных пикселей
        for (int i = 0; i < expectedErrors; i++) {
            if (i >= pixelIndices.size()) break;
            
            int pixelIndex = pixelIndices.get(i);
            int startBit = pixelIndex * 24;
            
            // Выбираем случайный бит в пикселе
            int bitOffset = random.nextInt(24);
            int bitPos = startBit + bitOffset;
            
            if (bitPos < result.length()) {
                // Инвертируем бит
                result.setCharAt(bitPos, result.charAt(bitPos) == '0' ? '1' : '0');
            }
        }
        
        return result.toString();
    }
    
    /**
     * Introduce errors per pixel in a binary string
     */
    public static String introduceErrorsPerPixel(String binaryStr, double errorRate, int bitsPerPixel) {
        Random random = new Random();
        StringBuilder result = new StringBuilder(binaryStr);
        int pixelCount = binaryStr.length() / bitsPerPixel;
        
        for (int i = 0; i < pixelCount; i++) {
            if (random.nextDouble() < errorRate) {
                // Выбираем случайный бит в пикселе
                int bitPos = i * bitsPerPixel + random.nextInt(bitsPerPixel);
                if (bitPos < result.length()) {
                    result.setCharAt(bitPos, result.charAt(bitPos) == '0' ? '1' : '0');
                }
            }
        }
        
        return result.toString();
    }
} 