package org.example;

import java.util.Arrays;

/**
 * Класс для работы с циклическими кодами
 * Реализует операции кодирования, декодирования и исправления ошибок
 */
public class CyclicCode {
    // Порождающий полином кода
    private final Polynomial generatorPolynomial;
    // Длина кодового слова
    private final int n;
    // Длина информационного слова
    private final int k;
    // Порождающая матрица кода
    private final int[][] generatorMatrix;
    // Проверочная матрица кода
    private final int[][] parityCheckMatrix;

    /**
     * Конструктор циклического кода из порождающего полинома
     * @param generatorPolynomial порождающий полином
     * @param n длина кодового слова
     */
    public CyclicCode(Polynomial generatorPolynomial, int n) {
        this.generatorPolynomial = generatorPolynomial;
        this.n = n;
        this.k = n - generatorPolynomial.getDegree();
        
        // Строим порождающую матрицу
        this.generatorMatrix = constructGeneratorMatrix();
        // Строим проверочную матрицу
        this.parityCheckMatrix = constructParityCheckMatrix();
    }

    /**
     * Конструктор циклического кода из порождающей матрицы
     * @param generatorMatrix порождающая матрица
     * @throws IllegalArgumentException если матрица не соответствует циклическому коду
     */
    public CyclicCode(int[][] generatorMatrix) {
        this.generatorMatrix = generatorMatrix;
        this.n = generatorMatrix[0].length;
        this.k = generatorMatrix.length;
        
        // Преобразуем порождающую матрицу в полином
        this.generatorPolynomial = matrixToPolynomial(generatorMatrix);
        // Проверяем, что матрица соответствует циклическому коду
        int[][] expectedGeneratorMatrix = constructGeneratorMatrix();
        if (!Arrays.deepEquals(expectedGeneratorMatrix, generatorMatrix)) {
            throw new IllegalArgumentException("Неверная порождающая матрица: строки должны быть циклическими сдвигами порождающего полинома");
        }
        this.parityCheckMatrix = constructParityCheckMatrix();
    }

    /**
     * Строит порождающую матрицу кода
     * @return порождающая матрица
     */
    private int[][] constructGeneratorMatrix() {
        int[][] matrix = new int[k][n];
        int[] coeffs = generatorPolynomial.getCoefficients();
        
        // Первая строка - коэффициенты порождающего полинома с нулями
        for (int i = 0; i < coeffs.length; i++) {
            matrix[0][i] = coeffs[i];
        }
        
        // Последующие строки - циклические сдвиги первой строки
        for (int i = 1; i < k; i++) {
            // Сдвигаем предыдущую строку вправо на одну позицию
            matrix[i][0] = matrix[i-1][n-1];
            for (int j = 1; j < n; j++) {
                matrix[i][j] = matrix[i-1][j-1];
            }
        }
        
        return matrix;
    }

    /**
     * Строит проверочную матрицу кода
     * @return проверочная матрица
     */
    private int[][] constructParityCheckMatrix() {
        int[][] matrix = new int[n - k][n];
        int[] coeffs = generatorPolynomial.getCoefficients();
        
        // Первая строка - коэффициенты порождающего полинома в обратном порядке
        for (int i = 0; i < coeffs.length; i++) {
            matrix[0][i] = coeffs[coeffs.length - 1 - i];
        }
        
        // Последующие строки - циклические сдвиги первой строки
        for (int i = 1; i < n - k; i++) {
            // Сдвигаем предыдущую строку вправо на одну позицию
            matrix[i][0] = matrix[i-1][n-1];
            for (int j = 1; j < n; j++) {
                matrix[i][j] = matrix[i-1][j-1];
            }
        }
        
        return matrix;
    }

    /**
     * Преобразует порождающую матрицу в полином
     * @param matrix порождающая матрица
     * @return порождающий полином
     */
    private Polynomial matrixToPolynomial(int[][] matrix) {
        int[] coeffs = new int[matrix[0].length - matrix.length + 1];
        for (int i = 0; i < coeffs.length; i++) {
            coeffs[i] = matrix[0][i];
        }
        return new Polynomial(coeffs);
    }

    /**
     * Кодирует информационное слово
     * @param message информационное слово
     * @return кодовое слово
     * @throws IllegalArgumentException если длина сообщения не равна k
     */
    public int[] encode(int[] message) {
        if (message.length != k) {
            throw new IllegalArgumentException("Длина сообщения должна быть равна k");
        }

        // Преобразуем сообщение в полином
        Polynomial messagePoly = new Polynomial(message);
        
        // Умножаем на x^(n-k)
        int[] shifted = new int[n];
        System.arraycopy(message, 0, shifted, n - k, k);
        Polynomial shiftedPoly = new Polynomial(shifted);
        
        // Вычисляем остаток
        Polynomial remainder = shiftedPoly.mod(generatorPolynomial);
        
        // Строим кодовое слово
        int[] codeword = new int[n];
        System.arraycopy(message, 0, codeword, 0, k);
        int[] remainderCoeffs = remainder.getCoefficients();
        System.arraycopy(remainderCoeffs, 0, codeword, k, remainderCoeffs.length);
        
        return codeword;
    }

    /**
     * Декодирует кодовое слово
     * @param received принятое слово
     * @return декодированное сообщение
     * @throws IllegalArgumentException если длина принятого слова не равна n
     */
    public int[] decode(int[] received) {
        if (received.length != n) {
            throw new IllegalArgumentException("Длина принятого слова должна быть равна n");
        }

        // Вычисляем синдром
        Polynomial receivedPoly = new Polynomial(received);
        Polynomial syndrome = receivedPoly.mod(generatorPolynomial);
        
        // Находим паттерн ошибки
        int[] errorPattern = findErrorPattern(syndrome);
        
        // Исправляем ошибки
        int[] corrected = new int[n];
        for (int i = 0; i < n; i++) {
            corrected[i] = received[i] ^ errorPattern[i];
        }
        
        // Извлекаем сообщение
        int[] message = new int[k];
        System.arraycopy(corrected, 0, message, 0, k);
        
        return message;
    }

    /**
     * Находит паттерн ошибки по синдрому
     * @param syndrome синдром ошибки
     * @return паттерн ошибки
     */
    private int[] findErrorPattern(Polynomial syndrome) {
        // Упрощенная версия. В реальной реализации
        // используется более сложный алгоритм поиска паттерна ошибки
        int[] errorPattern = new int[n];
        int[] syndromeCoeffs = syndrome.getCoefficients();
        
        if (syndromeCoeffs.length == 0) {
            return errorPattern; // Ошибок нет
        }
        
        // Для простоты предполагаем одиночную ошибку
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

    /**
     * Получает порождающий полином
     * @return порождающий полином
     */
    public Polynomial getGeneratorPolynomial() {
        return generatorPolynomial;
    }

    /**
     * Получает порождающую матрицу
     * @return порождающая матрица
     */
    public int[][] getGeneratorMatrix() {
        return generatorMatrix;
    }

    /**
     * Получает проверочную матрицу
     * @return проверочная матрица
     */
    public int[][] getParityCheckMatrix() {
        return parityCheckMatrix;
    }

    /**
     * Получает длину кодового слова
     * @return длина кодового слова
     */
    public int getN() {
        return n;
    }

    /**
     * Получает длину информационного слова
     * @return длина информационного слова
     */
    public int getK() {
        return k;
    }

    /**
     * Вычисляет синдром принятого слова
     * @param receivedWord принятое слово
     * @return синдром
     * @throws IllegalArgumentException если длина принятого слова не равна n
     */
    public int[] calculateSyndrome(int[] receivedWord) {
        if (receivedWord.length != n) {
            throw new IllegalArgumentException("Длина принятого слова должна быть равна " + n);
        }
        
        // Вычисляем синдром умножением принятого слова на проверочную матрицу
        int[] syndrome = new int[n - k];
        for (int i = 0; i < n - k; i++) {
            for (int j = 0; j < n; j++) {
                syndrome[i] ^= (receivedWord[j] * parityCheckMatrix[i][j]);
            }
        }
        
        return syndrome;
    }

    /**
     * Получает проверочный полином
     * @return проверочный полином
     */
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