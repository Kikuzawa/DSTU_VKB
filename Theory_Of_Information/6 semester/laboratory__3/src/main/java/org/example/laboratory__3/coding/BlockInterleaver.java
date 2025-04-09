package org.example.laboratory__3.coding;

import java.util.ArrayList;
import java.util.List;

/**
 * Класс для реализации блочного перемежения
 */
public class BlockInterleaver {
    private int rows;
    private int cols;
    
    public BlockInterleaver(int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
    }
    
    public BlockInterleaver() {
        this(10, 10);
    }
    
    /**
     * Set dimensions of the interleaver
     */
    public void setDimensions(int rows, int cols) {
        this.rows = rows;
        this.cols = cols;
    }
    
    /**
     * Перемежение данных
     */
    public String interleave(String data) {
        if (data == null || data.isEmpty()) {
            return null;
        }

        // Дополнение нулями до кратной длины блока
        int blockSize = rows * cols;
        if (data.length() % blockSize != 0) {
            data = data + "0".repeat(blockSize - (data.length() % blockSize));
        }

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < data.length(); i += blockSize) {
            String block = data.substring(i, Math.min(i + blockSize, data.length()));
            result.append(interleaveBlock(block));
        }

        return result.toString();
    }
    
    /**
     * Обратное перемежение данных
     */
    public String deinterleave(String data) {
        if (data == null || data.isEmpty()) {
            return null;
        }

        // Дополнение нулями до кратной длины блока
        int blockSize = rows * cols;
        if (data.length() % blockSize != 0) {
            data = data + "0".repeat(blockSize - (data.length() % blockSize));
        }

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < data.length(); i += blockSize) {
            String block = data.substring(i, Math.min(i + blockSize, data.length()));
            result.append(deinterleaveBlock(block));
        }

        return result.toString();
    }
    
    /**
     * Перемежение одного блока данных
     */
    private String interleaveBlock(String block) {
        if (block.length() != rows * cols) {
            return null;
        }

        // Создание матрицы
        List<List<Character>> matrix = new ArrayList<>();
        for (int i = 0; i < rows; i++) {
            List<Character> row = new ArrayList<>();
            for (int j = 0; j < cols; j++) {
                row.add(block.charAt(i * cols + j));
            }
            matrix.add(row);
        }

        // Чтение по столбцам
        StringBuilder result = new StringBuilder();
        for (int j = 0; j < cols; j++) {
            for (int i = 0; i < rows; i++) {
                result.append(matrix.get(i).get(j));
            }
        }

        return result.toString();
    }
    
    /**
     * Обратное перемежение одного блока данных
     */
    private String deinterleaveBlock(String block) {
        if (block.length() != rows * cols) {
            return null;
        }

        // Создание матрицы
        List<List<Character>> matrix = new ArrayList<>();
        for (int i = 0; i < rows; i++) {
            List<Character> row = new ArrayList<>();
            for (int j = 0; j < cols; j++) {
                row.add('0');
            }
            matrix.add(row);
        }

        // Заполнение матрицы по столбцам
        int index = 0;
        for (int j = 0; j < cols; j++) {
            for (int i = 0; i < rows; i++) {
                matrix.get(i).set(j, block.charAt(index++));
            }
        }

        // Чтение по строкам
        StringBuilder result = new StringBuilder();
        for (List<Character> row : matrix) {
            for (char c : row) {
                result.append(c);
            }
        }

        return result.toString();
    }
    
    /**
     * Calculate optimal dimensions for given data length
     */
    public int[] calculateDimensions(int dataLength) {
        // Find nearest square
        int squareSize = (int) Math.ceil(Math.sqrt(dataLength));
        
        // Dimension options
        List<int[]> dims = new ArrayList<>();
        for (int r = 1; r < squareSize * 2; r++) {
            int c = (int) Math.ceil((double) dataLength / r);
            dims.add(new int[]{r, c, r * c - dataLength});
        }
        
        // Choose option with minimum necessary padding
        dims.sort((a, b) -> Integer.compare(a[2], b[2]));
        int[] bestDims = dims.get(0);
        
        return new int[]{bestDims[0], bestDims[1]};
    }
    
    // Getters
    public int getRows() {
        return rows;
    }
    
    public int getCols() {
        return cols;
    }
} 