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
        return String.format("%" + bits + "s", Integer.toBinaryString(n)).replace(' ', '0');
    }
    
    /**
     * Convert a binary string to an integer
     */
    public static int binaryToInt(String binaryStr) {
        return Integer.parseInt(binaryStr, 2);
    }
    
    /**
     * Convert a pixel (RGB) to a binary string
     */
    public static String pixelToBinary(int r, int g, int b) {
        return intToBinary(r, 8) + intToBinary(g, 8) + intToBinary(b, 8);
    }
    
    /**
     * Convert a binary string to a pixel (RGB)
     */
    public static int[] binaryToPixel(String binaryStr) {
        if (binaryStr.length() != 24) { // RGB = 3 channels of 8 bits each
            throw new IllegalArgumentException("Binary string length must be 24 bits for RGB pixel");
        }
        
        int r = binaryToInt(binaryStr.substring(0, 8));
        int g = binaryToInt(binaryStr.substring(8, 16));
        int b = binaryToInt(binaryStr.substring(16, 24));
        
        return new int[]{r, g, b};
    }
    
    /**
     * Introduce random errors in a binary string with given probability
     */
    public static String introduceErrors(String binaryStr, double errorRate) {
        Random random = new Random();
        StringBuilder result = new StringBuilder(binaryStr);
        
        for (int i = 0; i < result.length(); i++) {
            if (random.nextDouble() < errorRate) {
                result.setCharAt(i, result.charAt(i) == '0' ? '1' : '0');
            }
        }
        
        return result.toString();
    }
    
    /**
     * Convert an image to a list of binary strings (one per row)
     */
    public static List<String> imageToBinary(BufferedImage img) {
        List<String> binaryRows = new ArrayList<>();
        int width = img.getWidth();
        int height = img.getHeight();
        
        for (int y = 0; y < height; y++) {
            StringBuilder row = new StringBuilder();
            for (int x = 0; x < width; x++) {
                int rgb = img.getRGB(x, y);
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
     */
    public static BufferedImage binaryToImage(List<String> binaryRows, int height, int width) {
        BufferedImage img = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        
        for (int y = 0; y < height && y < binaryRows.size(); y++) {
            String row = binaryRows.get(y);
            int pixelsInRow = row.length() / 24;
            
            for (int x = 0; x < width && x < pixelsInRow; x++) {
                String pixelBinary = row.substring(x * 24, (x + 1) * 24);
                int[] rgb = binaryToPixel(pixelBinary);
                int rgbValue = (rgb[0] << 16) | (rgb[1] << 8) | rgb[2];
                img.setRGB(x, y, rgbValue);
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
     * Introduce errors per pixel in a binary string
     */
    public static String introduceErrorsPerPixel(String binaryStr, double errorRate, int bitsPerPixel) {
        Random random = new Random();
        StringBuilder result = new StringBuilder(binaryStr);
        int pixelCount = binaryStr.length() / bitsPerPixel;
        
        for (int i = 0; i < pixelCount; i++) {
            if (random.nextDouble() < errorRate) {
                // Choose a random bit within the pixel
                int bitPos = i * bitsPerPixel + random.nextInt(bitsPerPixel);
                if (bitPos < result.length()) {
                    result.setCharAt(bitPos, result.charAt(bitPos) == '0' ? '1' : '0');
                }
            }
        }
        
        return result.toString();
    }
} 