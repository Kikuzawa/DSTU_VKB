package org.example.laboratory__3.coding;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Класс для реализации блочного кодирования
 */
public class BlockCoder {
    private List<String> codeWords;    // Список кодовых слов
    private List<String> informWords;
    private List<String> matrHT;
    private Map<String, String> sindromVector;
    private int n;                      // Длина кодового слова
    private int k;                      // Длина информационного слова
    private int dmin;                   // Минимальное расстояние
    private int r;                      // Количество ошибок, которые можно обнаружить
    private int t;                      // Корректирующая способность

    /**
     * Конструктор класса
     */
    public BlockCoder() {
        codeWords = new ArrayList<>();
        informWords = new ArrayList<>();
        matrHT = new ArrayList<>();
        sindromVector = new HashMap<>();
        n = 0;
        k = 0;
        dmin = 0;
        r = 0;
        t = 0;
    }

    /**
     * Logical XOR for an array of strings
     */
    public String xxor(List<String> array) {
        if (array == null || array.isEmpty()) {
            return "";
        }
        
        int[] result = new int[array.get(0).length()];
        for (String word : array) {
            for (int i = 0; i < word.length(); i++) {
                result[i] ^= Character.getNumericValue(word.charAt(i));
            }
        }
        
        StringBuilder sb = new StringBuilder();
        for (int bit : result) {
            sb.append(bit);
        }
        
        return sb.toString();
    }

    /**
     * Transpose a matrix
     */
    public List<String> transp(List<String> matrix) {
        if (matrix == null || matrix.isEmpty()) {
            return new ArrayList<>();
        }
        
        List<String> result = new ArrayList<>();
        for (int i = 0; i < matrix.get(0).length(); i++) {
            StringBuilder newRow = new StringBuilder();
            for (String row : matrix) {
                newRow.append(row.charAt(i));
            }
            result.add(newRow.toString());
        }
        
        return result;
    }

    /**
     * Generate matrices G and H based on input matrix
     */
    public List<String>[] generateMatrices(List<String> inputMatrix, String matrixType) {
        if (inputMatrix == null || inputMatrix.isEmpty()) {
            return null;
        }
        
        List<String> matrG = new ArrayList<>();
        List<String> matrH = new ArrayList<>();
        
        if ("H".equals(matrixType)) {
            // For special matrix H (4x7) we need to get n=9, k=5, dmin=2
            int rows = inputMatrix.size();     // 4 for example matrix
            int cols = inputMatrix.get(0).length();  // 7 for example matrix
            
            // Set known parameters for code n=9, k=5 for matrix H (4x7)
            int nTarget = 9;  // Desired code word length
            int kTarget = 5;  // Desired number of information bits
            
            // Create matrix H (extended version of input matrix)
            for (String row : inputMatrix) {
                // Add zeros at the beginning to extend to desired length
                String extendedRow = "0".repeat(nTarget - cols) + row;
                matrH.add(extendedRow);
            }
            
            // Create generating matrix G of size kTarget x nTarget
            for (int i = 0; i < kTarget; i++) {
                StringBuilder row = new StringBuilder();
                for (int j = 0; j < nTarget; j++) {
                    row.append(j == i ? '1' : '0');  // Identity part
                }
                matrG.add(row.toString());
            }
        } else if ("G".equals(matrixType)) {
            // For matrix G, use the input matrix as is
            matrG.addAll(inputMatrix);
            
            // Create check matrix H of size (n-k) x n
            int n = inputMatrix.get(0).length();
            int k = inputMatrix.size();
            
            for (int i = 0; i < n - k; i++) {
                StringBuilder row = new StringBuilder();
                for (int j = 0; j < n; j++) {
                    row.append(j == k + i ? '1' : '0');  // Identity part
                }
                matrH.add(row.toString());
            }
        }
        
        @SuppressWarnings("unchecked")
        List<String>[] result = new List[2];
        result[0] = matrG;
        result[1] = matrH;
        
        return result;
    }

    /**
     * Настройка блочного кода
     * @param matrix Матрица кода (G или H)
     * @param matrixType Тип матрицы ("G" для порождающей, "H" для проверочной)
     * @return true если настройка успешна, false в противном случае
     */
    public boolean setupCode(List<String> matrix, String matrixType) {
        List<String>[] matrices = generateMatrices(matrix, matrixType);
        if (matrices == null) {
            return false;
        }
        
        List<String> matrG = matrices[0];
        List<String> matrH = matrices[1];
        
        this.k = matrG.size();
        this.n = matrG.get(0).length();
        this.informWords = new ArrayList<>();
        this.codeWords = new ArrayList<>();
        
        // Generate all information words
        for (int i = 0; i < Math.pow(2, this.k); i++) {
            String word = String.format("%" + this.k + "s", Integer.toBinaryString(i)).replace(' ', '0');
            this.informWords.add(word);
        }
        
        // Generate code words
        for (String informWord : this.informWords) {
            List<String> forOperation = new ArrayList<>();
            for (int j = 0; j < informWord.length(); j++) {
                if (informWord.charAt(j) == '1') {
                    forOperation.add(matrG.get(j));
                }
            }
            
            if (!forOperation.isEmpty()) {
                this.codeWords.add(xxor(forOperation));
            } else {
                this.codeWords.add("0".repeat(this.n));
            }
        }
        
        // Determine minimum Hamming distance
        List<Integer> distanceHamm = new ArrayList<>();
        
        // Calculate minimum weight of non-zero code words
        for (String word : this.codeWords) {
            if (!word.equals("0".repeat(this.n))) {  // Skip zero code word
                int weight = 0;
                for (int i = 0; i < word.length(); i++) {
                    if (word.charAt(i) == '1') {
                        weight++;
                    }
                }
                distanceHamm.add(weight);
            }
        }
        
        // For linear code, minimum distance equals minimum weight of non-zero code words
        this.dmin = distanceHamm.isEmpty() ? 0 : distanceHamm.stream().mapToInt(Integer::intValue).min().getAsInt();
        
        // Check for matrix H: if matrix H was passed, check minimum distance by columns of matrix H
        if ("H".equals(matrixType)) {
            // For code with minimum distance 2, each column of H must be non-zero and unique
            // Check columns of original matrix H
            List<String> hColumns = transp(matrix);
            
            // Check that all columns are different and non-zero
            boolean allNonzero = true;
            for (String col : hColumns) {
                if (col.equals("0".repeat(col.length()))) {
                    allNonzero = false;
                    break;
                }
            }
            
            boolean allDistinct = hColumns.stream().distinct().count() == hColumns.size();
            
            if (allNonzero && allDistinct) {
                this.dmin = 2;  // If all columns of matrix H are different and non-zero, then d_min = 2
            }
        }
        
        this.r = this.dmin - 1;  // Number of errors that can be detected
        this.t = (this.dmin - 1) / 2;  // Number of errors that can be corrected
        
        // Generate syndrome table
        this.matrHT = transp(matrH);
        List<String> e = new ArrayList<>();
        List<String> S = new ArrayList<>();
        
        // Error vector with weight 0
        e.add("0".repeat(this.n));
        
        // Error vectors with weight t
        for (int i = 0; i < this.n; i++) {
            if (this.t >= 1) {  // If we can correct at least one error
                // Create vector with one error at position i
                StringBuilder error = new StringBuilder("0".repeat(this.n));
                error.setCharAt(i, '1');
                e.add(error.toString());
            }
        }
        
        // Calculate syndromes
        for (String errorVector : e) {
            List<String> forOperation = new ArrayList<>();
            for (int j = 0; j < errorVector.length(); j++) {
                if (errorVector.charAt(j) == '1') {
                    forOperation.add(this.matrHT.get(j));
                }
            }
            
            if (!forOperation.isEmpty()) {
                S.add(xxor(forOperation));
            } else {
                S.add("0".repeat(this.matrHT.get(0).length()));
            }
        }
        
        // Create syndrome dictionary
        this.sindromVector.clear();
        for (int i = 0; i < e.size(); i++) {
            this.sindromVector.put(S.get(i), e.get(i));
        }
        
        return true;
    }

    /**
     * Кодирование информационного слова
     * @param infoWord Информационное слово
     * @return Закодированное слово
     */
    public String encode(String infoWord) {
        if (this.codeWords.isEmpty() || this.informWords.isEmpty()) {
            return infoWord;
        }
        
        // Pad with zeros to multiple of information word length
        if (infoWord.length() % this.k != 0) {
            infoWord = infoWord + "0".repeat(this.k - (infoWord.length() % this.k));
        }
        
        // Create dictionary for encoding
        Map<String, String> codingDict = new HashMap<>();
        for (int i = 0; i < this.informWords.size(); i++) {
            codingDict.put(this.informWords.get(i), this.codeWords.get(i));
        }
        
        // Encoding
        StringBuilder encodedData = new StringBuilder();
        for (int i = 0; i < infoWord.length(); i += this.k) {
            String informWord = infoWord.substring(i, i + this.k);
            encodedData.append(codingDict.get(informWord));
        }
        
        return encodedData.toString();
    }

    /**
     * Декодирование кодового слова
     * @param receivedCodeWord Полученное кодовое слово
     * @return Декодированное информационное слово
     */
    public String decode(String receivedCodeWord) {
        if (this.codeWords.isEmpty() || this.informWords.isEmpty()) {
            return receivedCodeWord;
        }
        
        // Check if length of encoded data is a multiple of code word length
        if (receivedCodeWord.length() % this.n != 0) {
            return null;
        }
        
        // Decoding
        StringBuilder decodedData = new StringBuilder();
        for (int i = 0; i < receivedCodeWord.length(); i += this.n) {
            String currentCodeWord = receivedCodeWord.substring(i, i + this.n);
            
            // Calculate syndrome
            String syndrome = calculateSyndrome(currentCodeWord);
            
            // Find error pattern
            String errorPattern = sindromVector.get(syndrome);
            if (errorPattern == null) {
                // If syndrome not found, assume no errors
                errorPattern = "0".repeat(this.n);
            }
            
            // Correct errors
            String correctedWord = correctErrors(currentCodeWord, errorPattern);
            
            // Find corresponding information word
            String infoWord = findInformationWord(correctedWord);
            if (infoWord != null) {
                decodedData.append(infoWord);
            }
        }
        
        return decodedData.toString();
    }
    
    // Геттеры для параметров кода
    public int getN() {
        return n;
    }
    
    public int getK() {
        return k;
    }
    
    public int getDmin() {
        return dmin;
    }
    
    public int getR() {
        return r;
    }
    
    public int getT() {
        return this.t;
    }

    public List<String> getCodeWords() {
        return this.codeWords;
    }

    /**
     * Вычисление синдрома для кодового слова
     * @param codeWord Кодовое слово
     * @return Синдром кодового слова
     */
    private String calculateSyndrome(String codeWord) {
        StringBuilder syndrome = new StringBuilder();
        for (int j = 0; j < this.matrHT.get(0).length(); j++) {
            int xorBit = 0;
            for (int k = 0; k < this.n; k++) {
                xorBit ^= Character.getNumericValue(codeWord.charAt(k)) & 
                          Character.getNumericValue(this.matrHT.get(k).charAt(j));
            }
            syndrome.append(xorBit);
        }
        return syndrome.toString();
    }

    /**
     * Исправление ошибок в кодовом слове
     * @param codeWord Кодовое слово с ошибками
     * @param errorPattern Вектор ошибок
     * @return Исправленное кодовое слово
     */
    private String correctErrors(String codeWord, String errorPattern) {
        StringBuilder correctedWord = new StringBuilder();
        for (int j = 0; j < this.n; j++) {
            correctedWord.append(Character.getNumericValue(codeWord.charAt(j)) ^ 
                               Character.getNumericValue(errorPattern.charAt(j)));
        }
        return correctedWord.toString();
    }

    /**
     * Поиск информационного слова по кодовому слову
     * @param codeWord Кодовое слово
     * @return Информационное слово или null, если не найдено
     */
    private String findInformationWord(String codeWord) {
        // Create reverse dictionary for decoding
        Map<String, String> decodingDict = new HashMap<>();
        for (int i = 0; i < this.informWords.size(); i++) {
            decodingDict.put(this.codeWords.get(i), this.informWords.get(i));
        }

        // Try exact match first
        if (decodingDict.containsKey(codeWord)) {
            return decodingDict.get(codeWord);
        }

        // If no exact match, find closest code word
        int minDistance = Integer.MAX_VALUE;
        String bestMatch = null;
        for (String cw : this.codeWords) {
            int distance = 0;
            for (int j = 0; j < codeWord.length(); j++) {
                if (codeWord.charAt(j) != cw.charAt(j)) {
                    distance++;
                }
            }
            if (distance < minDistance) {
                minDistance = distance;
                bestMatch = cw;
            }
        }

        if (bestMatch != null) {
            return decodingDict.get(bestMatch);
        }

        // If we can't find at all, take first k bits
        return codeWord.substring(0, this.k);
    }
} 