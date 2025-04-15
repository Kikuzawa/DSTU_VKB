package org.example.laboratory__3.coding;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class ConvolutionalCoder {
    private List<int[]> polynomials;
    private boolean verbose;
    
    public ConvolutionalCoder() {
        this.polynomials = new ArrayList<>();
        this.verbose = false;
    }
    
    /**
     * Set polynomials for convolutional coding
     */
    public void setPolynomials(List<int[]> polynomials) {
        this.polynomials = polynomials;
    }
    
    /**
     * Set verbose mode for debugging
     */
    public void setVerbose(boolean verbose) {
        this.verbose = verbose;
    }
    
    /**
     * Convolutional encoding
     */
    public String convolutionalEncode(String inputBits) {
        if (this.polynomials.isEmpty()) {
            return null;
        }
        
        if (inputBits.isEmpty()) {
            return "";
        }
        
        // Find maximum register size
        int maxRegister = 0;
        for (int[] poly : this.polynomials) {
            for (int idx : poly) {
                if (idx > maxRegister) {
                    maxRegister = idx;
                }
            }
        }
        
        // Initialize registers
        int[] registers = new int[maxRegister + 1];
        
        // Encoding
        StringBuilder encoded = new StringBuilder();
        for (int i = 0; i < inputBits.length(); i++) {
            // Shift registers and insert new bit
            System.arraycopy(registers, 0, registers, 1, registers.length - 1);
            registers[0] = Character.getNumericValue(inputBits.charAt(i));
            
            // Calculate output bits
            for (int[] poly : this.polynomials) {
                int xor = 0;
                for (int idx : poly) {
                    xor ^= registers[idx];
                }
                encoded.append(xor);
            }
        }
        
        return encoded.toString();
    }
    
    /**
     * Viterbi algorithm for decoding
     */
    public String viterbiDecode(String encodedBits) {
        if (this.polynomials.isEmpty()) {
            return null;
        }
        
        if (encodedBits.isEmpty()) {
            return "";
        }
        
        final int nOutputs = this.polynomials.size();
        
        // Find maximum register size
        int maxRegister = 0;
        for (int[] poly : this.polynomials) {
            for (int idx : poly) {
                if (idx > maxRegister) {
                    maxRegister = idx;
                }
            }
        }
        
        final int nStates = (int) Math.pow(2, maxRegister);
        final List<String> states = new ArrayList<>();
        for (int i = 0; i < nStates; i++) {
            states.add(String.format("%" + maxRegister + "s", Integer.toBinaryString(i)).replace(' ', '0'));
        }
        
        if (this.verbose) {
            System.out.println("\n" + "═".repeat(50));
            System.out.println("Starting decoding. Parameters:");
            System.out.println("Number of states: " + nStates);
            System.out.println("Encoded sequence length: " + encodedBits.length() + " bits");
            System.out.println("Number of steps: " + encodedBits.length() / nOutputs);
        }
        
        // Initialize path metrics
        Map<String, Double> pathMetrics = new HashMap<>();
        for (String state : states) {
            pathMetrics.put(state, Double.POSITIVE_INFINITY);
        }
        pathMetrics.put("0".repeat(maxRegister), 0.0);
        
        Map<String, List<String>> paths = new HashMap<>();
        for (String state : states) {
            paths.put(state, new ArrayList<>());
        }
        
        // Process each step
        for (int step = 0; step < encodedBits.length() / nOutputs; step++) {
            final String currentBits = encodedBits.substring(step * nOutputs, (step + 1) * nOutputs);
            
            final Map<String, Double> newMetrics = new HashMap<>();
            final Map<String, List<String>> newPaths = new HashMap<>();
            
            for (String state : states) {
                newMetrics.put(state, Double.POSITIVE_INFINITY);
                newPaths.put(state, new ArrayList<>());
            }
            
            if (this.verbose) {
                System.out.println("\n" + "─".repeat(50));
                System.out.println("Step " + (step + 1) + ". Received bits: " + currentBits);
            }
            
            for (String state : states) {
                if (pathMetrics.get(state) == Double.POSITIVE_INFINITY) {
                    continue;
                }
                
                if (this.verbose) {
                    System.out.println("\nState: " + state + " (metric: " + pathMetrics.get(state) + ")");
                }
                
                for (char inputBit : new char[]{'0', '1'}) {
                    // Calculate next state
                    String nextState = inputBit + state.substring(0, state.length() - 1);
                    
                    // Create temporary registers for output calculation
                    int[] tmpRegisters = new int[maxRegister + 1];
                    tmpRegisters[0] = Character.getNumericValue(inputBit);
                    for (int i = 0; i < state.length(); i++) {
                        tmpRegisters[i + 1] = Character.getNumericValue(state.charAt(i));
                    }
                    
                    // Calculate expected output bits
                    StringBuilder expected = new StringBuilder();
                    for (int[] poly : this.polynomials) {
                        int xor = 0;
                        for (int idx : poly) {
                            xor ^= tmpRegisters[idx];
                        }
                        expected.append(xor);
                    }
                    final String expectedStr = expected.toString();
                    
                    // Calculate Hamming metric
                    int metric = 0;
                    for (int i = 0; i < currentBits.length(); i++) {
                        if (currentBits.charAt(i) != expectedStr.charAt(i)) {
                            metric++;
                        }
                    }
                    
                    final double totalMetric = pathMetrics.get(state) + metric;
                    
                    if (this.verbose) {
                        System.out.println("  Input: " + inputBit + " -> State: " + nextState);
                        System.out.println("  Expected: " + expectedStr + " vs Actual: " + currentBits);
                        System.out.println("  Step metric: " + metric + ", Total metric: " + totalMetric);
                    }
                    
                    if (totalMetric < newMetrics.get(nextState)) {
                        newMetrics.put(nextState, totalMetric);
                        List<String> newPath = new ArrayList<>(paths.get(state));
                        newPath.add(String.valueOf(inputBit));
                        newPaths.put(nextState, newPath);
                        
                        if (this.verbose) {
                            System.out.println("  ✔ Metric updated");
                        }
                    } else if (this.verbose) {
                        System.out.println("  ✖ Metric worse than current");
                    }
                }
            }
            
            pathMetrics = newMetrics;
            paths = newPaths;
        }
        
        if (this.verbose) {
            System.out.println("\n" + "═".repeat(50));
            System.out.println("Final state metrics:");
            Map<String, List<String>> finalPaths = paths;
            pathMetrics.entrySet().stream()
                    .sorted(Map.Entry.comparingByValue())
                    .forEach(entry -> System.out.println(entry.getKey() + ": " + entry.getValue() + " → " + finalPaths.get(entry.getKey())));
        }
        
        // Find state with minimum metric
        String finalState = pathMetrics.entrySet().stream()
                .min(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse("0".repeat(maxRegister));
        
        List<String> finalPath = paths.get(finalState);
        StringBuilder result = new StringBuilder();
        for (String bit : finalPath) {
            result.append(bit);
        }
        
        if (this.verbose) {
            System.out.println("\n" + "═".repeat(50));
            System.out.println("Selected path: " + finalPath);
            System.out.println("Final metric: " + pathMetrics.get(finalState));
            System.out.println("Decoding result: " + result);
        }
        
        return result.substring(0, encodedBits.length() / this.polynomials.size());
    }
} 