package org.example.laboratory__3.coding;

import java.util.ArrayList;
import java.util.List;

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
     * Interleave binary data
     */
    public String interleave(String binaryData) {
        // Check that data length doesn't exceed interleaver size
        if (binaryData.length() > this.rows * this.cols) {
            throw new IllegalArgumentException("Data length (" + binaryData.length() + 
                   ") exceeds interleaver size (" + this.rows * this.cols + ")");
        }
        
        // Pad data with zeros if needed
        String paddedData = binaryData;
        int paddingNeeded = this.rows * this.cols - binaryData.length();
        if (paddingNeeded > 0) {
            paddedData = binaryData + "0".repeat(paddingNeeded);
        }
        
        // Fill interleaver matrix by rows
        List<String> matrix = new ArrayList<>();
        for (int i = 0; i < this.rows; i++) {
            String row = paddedData.substring(i * this.cols, (i + 1) * this.cols);
            matrix.add(row);
        }
        
        // Read by columns
        StringBuilder interleavedData = new StringBuilder();
        for (int j = 0; j < this.cols; j++) {
            for (int i = 0; i < this.rows; i++) {
                if (j < matrix.get(i).length()) {
                    interleavedData.append(matrix.get(i).charAt(j));
                }
            }
        }
        
        return interleavedData.toString();
    }
    
    /**
     * Deinterleave binary data
     */
    public String deinterleave(String interleavedData) {
        // Check that data length matches interleaver size
        int expectedLength = this.rows * this.cols;
        if (interleavedData.length() != expectedLength) {
            throw new IllegalArgumentException("Data length (" + interleavedData.length() + 
                   ") doesn't match interleaver size (" + expectedLength + ")");
        }
        
        // Fill interleaver matrix by columns
        char[][] matrix = new char[this.rows][this.cols];
        for (int i = 0; i < this.rows; i++) {
            for (int j = 0; j < this.cols; j++) {
                matrix[i][j] = '0';
            }
        }
        
        int idx = 0;
        for (int j = 0; j < this.cols; j++) {
            for (int i = 0; i < this.rows; i++) {
                if (idx < interleavedData.length()) {
                    matrix[i][j] = interleavedData.charAt(idx);
                    idx++;
                }
            }
        }
        
        // Read by rows
        StringBuilder deinterleavedData = new StringBuilder();
        for (int i = 0; i < this.rows; i++) {
            for (int j = 0; j < this.cols; j++) {
                deinterleavedData.append(matrix[i][j]);
            }
        }
        
        return deinterleavedData.toString();
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