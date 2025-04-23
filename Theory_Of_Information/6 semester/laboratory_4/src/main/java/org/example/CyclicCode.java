package org.example;

import java.util.Arrays;

public class CyclicCode {
    private final Polynomial generatorPolynomial;
    private final int n;
    private final int k;
    private final int[][] generatorMatrix;
    private final int[][] parityCheckMatrix;

    public CyclicCode(Polynomial generatorPolynomial, int n) {
        this.generatorPolynomial = generatorPolynomial;
        this.n = n;
        this.k = n - generatorPolynomial.getDegree();
        
        // Construct generator matrix
        this.generatorMatrix = constructGeneratorMatrix();
        this.parityCheckMatrix = constructParityCheckMatrix();
    }

    public CyclicCode(int[][] generatorMatrix) {
        this.generatorMatrix = generatorMatrix;
        this.n = generatorMatrix[0].length;
        this.k = generatorMatrix.length;
        
        // Convert generator matrix to polynomial
        this.generatorPolynomial = matrixToPolynomial(generatorMatrix);
        // Validate that provided generator matrix matches canonical cyclic shifts
        int[][] expectedGeneratorMatrix = constructGeneratorMatrix();
        if (!Arrays.deepEquals(expectedGeneratorMatrix, generatorMatrix)) {
            throw new IllegalArgumentException("Invalid generator matrix: rows must be cyclic shifts of the generator polynomial");
        }
        this.parityCheckMatrix = constructParityCheckMatrix();
    }

    private int[][] constructGeneratorMatrix() {
        int[][] matrix = new int[k][n];
        int[] coeffs = generatorPolynomial.getCoefficients();
        
        // First row is the generator polynomial coefficients padded with zeros
        for (int i = 0; i < coeffs.length; i++) {
            matrix[0][i] = coeffs[i];
        }
        
        // Subsequent rows are cyclic shifts of the first row
        for (int i = 1; i < k; i++) {
            // Shift the previous row right by one position
            matrix[i][0] = matrix[i-1][n-1];
            for (int j = 1; j < n; j++) {
                matrix[i][j] = matrix[i-1][j-1];
            }
        }
        
        return matrix;
    }

    private int[][] constructParityCheckMatrix() {
        int[][] matrix = new int[n - k][n];
        int[] coeffs = generatorPolynomial.getCoefficients();
        
        // First row is the generator polynomial coefficients in reverse order
        for (int i = 0; i < coeffs.length; i++) {
            matrix[0][i] = coeffs[coeffs.length - 1 - i];
        }
        
        // Subsequent rows are cyclic shifts of the first row
        for (int i = 1; i < n - k; i++) {
            // Shift the previous row right by one position
            matrix[i][0] = matrix[i-1][n-1];
            for (int j = 1; j < n; j++) {
                matrix[i][j] = matrix[i-1][j-1];
            }
        }
        
        return matrix;
    }

    private Polynomial matrixToPolynomial(int[][] matrix) {
        int[] coeffs = new int[matrix[0].length - matrix.length + 1];
        for (int i = 0; i < coeffs.length; i++) {
            coeffs[i] = matrix[0][i];
        }
        return new Polynomial(coeffs);
    }

    public int[] encode(int[] message) {
        if (message.length != k) {
            throw new IllegalArgumentException("Message length must be equal to k");
        }

        // Convert message to polynomial
        Polynomial messagePoly = new Polynomial(message);
        
        // Multiply by x^(n-k)
        int[] shifted = new int[n];
        System.arraycopy(message, 0, shifted, n - k, k);
        Polynomial shiftedPoly = new Polynomial(shifted);
        
        // Calculate remainder
        Polynomial remainder = shiftedPoly.mod(generatorPolynomial);
        
        // Construct codeword
        int[] codeword = new int[n];
        System.arraycopy(message, 0, codeword, 0, k);
        int[] remainderCoeffs = remainder.getCoefficients();
        System.arraycopy(remainderCoeffs, 0, codeword, k, remainderCoeffs.length);
        
        return codeword;
    }

    public int[] decode(int[] received) {
        if (received.length != n) {
            throw new IllegalArgumentException("Received word length must be equal to n");
        }

        // Calculate syndrome
        Polynomial receivedPoly = new Polynomial(received);
        Polynomial syndrome = receivedPoly.mod(generatorPolynomial);
        
        // Find error pattern
        int[] errorPattern = findErrorPattern(syndrome);
        
        // Correct errors
        int[] corrected = new int[n];
        for (int i = 0; i < n; i++) {
            corrected[i] = received[i] ^ errorPattern[i];
        }
        
        // Extract message
        int[] message = new int[k];
        System.arraycopy(corrected, 0, message, 0, k);
        
        return message;
    }

    private int[] findErrorPattern(Polynomial syndrome) {
        // This is a simplified version. In a real implementation,
        // you would use a more sophisticated error pattern finding algorithm
        int[] errorPattern = new int[n];
        int[] syndromeCoeffs = syndrome.getCoefficients();
        
        if (syndromeCoeffs.length == 0) {
            return errorPattern; // No errors
        }
        
        // For simplicity, assume single error
        for (int i = 0; i < n; i++) {
            int[] testPattern = new int[n];
            testPattern[i] = 1;
            Polynomial testSyndrome = new Polynomial(testPattern).mod(generatorPolynomial);
            if (Arrays.equals(testSyndrome.getCoefficients(), syndromeCoeffs)) {
                errorPattern[i] = 1;
                break;
            }
        }
        
        return errorPattern;
    }

    public Polynomial getGeneratorPolynomial() {
        return generatorPolynomial;
    }

    public int[][] getGeneratorMatrix() {
        return generatorMatrix;
    }

    public int[][] getParityCheckMatrix() {
        return parityCheckMatrix;
    }

    public int getN() {
        return n;
    }

    public int getK() {
        return k;
    }

    public int[] calculateSyndrome(int[] receivedWord) {
        if (receivedWord.length != n) {
            throw new IllegalArgumentException("Received word length must be " + n);
        }
        
        // Calculate syndrome by multiplying received word with parity check matrix
        int[] syndrome = new int[n - k];
        for (int i = 0; i < n - k; i++) {
            for (int j = 0; j < n; j++) {
                syndrome[i] ^= (receivedWord[j] * parityCheckMatrix[i][j]);
            }
        }
        
        return syndrome;
    }

    public Polynomial getParityCheckPolynomial() {
        // Создаем полином x^n - 1
        int[] xnCoeffs = new int[n + 1];
        xnCoeffs[0] = 1; // -1
        xnCoeffs[n] = 1; // x^n
        Polynomial xnMinus1 = new Polynomial(xnCoeffs);
        
        // Делим x^n - 1 на порождающий полином
        return xnMinus1.divide(generatorPolynomial);
    }
} 