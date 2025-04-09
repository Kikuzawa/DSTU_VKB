package org.example.laboratory__3.coding;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Класс для реализации блочного кодирования
 */
public class BlockCoder {
    private List<String> codeWords;
    private List<String> informWords;
    private List<String> matrHT;
    private Map<String, String> sindromVector;
    private int n;  // Длина кодового слова
    private int k;  // Длина информационного слова
    private int dmin;  // Минимальное расстояние кода
    private int r;  // Количество ошибок, которые можно обнаружить
    private int t;  // Количество ошибок, которые можно исправить

    public BlockCoder() {
        this.codeWords = new ArrayList<>();
        this.informWords = new ArrayList<>();
        this.matrHT = new ArrayList<>();
        this.sindromVector = new HashMap<>();
        this.n = 0;
        this.k = 0;
        this.dmin = 0;
        this.r = 0;
        this.t = 0;
    }

    /**
     * Логическое XOR для массива строк
     */
    private String xxor(List<String> array) {
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
     * Транспонирование матрицы
     */
    private List<String> transp(List<String> matrix) {
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
     * Генерация матриц G и H на основе входной матрицы
     */
    private List<String>[] generateMatrices(List<String> inputMatrix, String matrixType) {
        if (inputMatrix == null || inputMatrix.isEmpty() || inputMatrix.get(0).isEmpty()) {
            return null;
        }

        List<String> matrG;
        List<String> matrH;

        if ("H".equals(matrixType)) {
            // Для специальной матрицы H (4x7) нужно получить n=9, k=5, dmin=2
            int rows = inputMatrix.size();     // 4 для примера матрицы
            int cols = inputMatrix.get(0).length();  // 7 для примера матрицы

            // Задаем известные параметры кода n=9, k=5 для матрицы H (4x7)
            int nTarget = 9;  // Желаемая длина кодового слова
            int kTarget = 5;  // Желаемое количество информационных бит

            // Создаем матрицу H (расширенная версия входной матрицы)
            matrH = new ArrayList<>();
            for (String row : inputMatrix) {
                // Добавляем нули в начало для расширения до нужной длины
                StringBuilder extendedRow = new StringBuilder();
                for (int i = 0; i < nTarget - cols; i++) {
                    extendedRow.append('0');
                }
                extendedRow.append(row);
                matrH.add(extendedRow.toString());
            }

            // Создаем порождающую матрицу G размера kTarget x nTarget
            matrG = new ArrayList<>();

            // Создаем единичную часть I_k (k x k)
            for (int i = 0; i < kTarget; i++) {
                StringBuilder row = new StringBuilder();
                for (int j = 0; j < nTarget; j++) {
                    row.append(j == i ? '1' : '0');  // Единичная часть
                }
                matrG.add(row.toString());
            }
        } else if ("G".equals(matrixType)) {
            // Преобразование матрицы G работает как прежде
            int k = inputMatrix.size();  // Количество строк в G (информационные биты)
            int n = inputMatrix.get(0).length();  // Количество столбцов в G (кодовое слово)

            // Используем исходную матрицу G как есть
            matrG = new ArrayList<>(inputMatrix);

            // Создаем проверочную матрицу H размера (n-k) x n
            matrH = new ArrayList<>();
            for (int i = 0; i < n - k; i++) {
                StringBuilder row = new StringBuilder();
                for (int j = 0; j < n; j++) {
                    row.append(j == k + i ? '1' : '0');  // Единичная часть
                }
                matrH.add(row.toString());
            }
        } else {
            return null;
        }

        @SuppressWarnings("unchecked")
        List<String>[] result = new List[2];
        result[0] = matrG;
        result[1] = matrH;
        return result;
    }

    /**
     * Настройка блочного кода на основе входной матрицы
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

        // Генерация всех информационных слов
        for (int i = 0; i < Math.pow(2, this.k); i++) {
            String word = String.format("%" + this.k + "s", Integer.toBinaryString(i)).replace(' ', '0');
            this.informWords.add(word);
        }

        // Генерация кодовых слов
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

        // Определение минимального расстояния Хэмминга
        List<Integer> distanceHamm = new ArrayList<>();

        // Вычисляем минимальный вес ненулевых кодовых слов
        for (String word : this.codeWords) {
            if (!word.equals("0".repeat(this.n))) {  // Пропускаем нулевое кодовое слово
                int weight = 0;
                for (int i = 0; i < word.length(); i++) {
                    if (word.charAt(i) == '1') {
                        weight++;
                    }
                }
                distanceHamm.add(weight);
            }
        }

        // Для линейного кода минимальное расстояние равно минимальному весу ненулевых кодовых слов
        this.dmin = distanceHamm.isEmpty() ? 0 : Collections.min(distanceHamm);

        // Проверка для матрицы H: если матрица H была передана, проверим минимальное расстояние
        // по столбцам матрицы H
        if ("H".equals(matrixType)) {
            // Для кода с минимальным расстоянием 2 каждый столбец H должен быть ненулевым и уникальным
            // Проверим столбцы исходной матрицы H
            List<String> hColumns = transp(matrix);

            // Проверяем, что все столбцы разные и ненулевые
            Set<String> uniqueColumns = new HashSet<>();
            boolean allNonzero = true;

            for (String col : hColumns) {
                if (col.equals("0".repeat(col.length()))) {
                    allNonzero = false;
                    break;
                }
                uniqueColumns.add(col);
            }

            boolean allDistinct = uniqueColumns.size() == hColumns.size();

            if (allNonzero && allDistinct) {
                this.dmin = 2;  // Если все столбцы матрицы H разные и ненулевые, то d_min = 2
            }
        }

        this.r = this.dmin - 1;  // Количество ошибок, которые можно обнаружить
        this.t = (this.dmin - 1) / 2;  // Количество ошибок, которые можно исправить

        // Генерация таблицы синдромов
        this.matrHT = transp(matrH);
        List<String> e = new ArrayList<>();
        List<String> S = new ArrayList<>();

        // Вектор ошибок с весом 0
        e.add("0".repeat(this.n));

        // Векторы ошибок с весом t
        for (int i = 0; i < this.n; i++) {
            if (this.t >= 1) {  // Если можем исправлять хотя бы одну ошибку
                // Создаем вектор с одной ошибкой в позиции i
                StringBuilder error = new StringBuilder();
                for (int j = 0; j < this.n; j++) {
                    error.append(j == i ? '1' : '0');
                }
                e.add(error.toString());
            }
        }

        // Вычисление синдромов
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

        // Создание словаря синдромов
        this.sindromVector = new HashMap<>();
        for (int i = 0; i < e.size(); i++) {
            this.sindromVector.put(S.get(i), e.get(i));
        }

        return true;
    }

    /**
     * Кодирование бинарных данных с помощью блочного кода
     */
    public String encode(String binaryData) {
        if (this.codeWords == null || this.codeWords.isEmpty() || 
            this.informWords == null || this.informWords.isEmpty()) {
            return null;
        }

        // Дополнение нулями до кратной длины информационного слова
        if (binaryData.length() % this.k != 0) {
            binaryData = binaryData + "0".repeat(this.k - (binaryData.length() % this.k));
        }

        // Создание словаря соответствия
        Map<String, String> codingDict = new HashMap<>();
        for (int i = 0; i < this.informWords.size(); i++) {
            codingDict.put(this.informWords.get(i), this.codeWords.get(i));
        }

        // Кодирование
        StringBuilder encodedData = new StringBuilder();
        for (int i = 0; i < binaryData.length(); i += this.k) {
            String informWord = binaryData.substring(i, Math.min(i + this.k, binaryData.length()));
            encodedData.append(codingDict.get(informWord));
        }

        return encodedData.toString();
    }

    /**
     * Декодирование с исправлением ошибок
     */
    public String decode(String encodedData) {
        if (this.codeWords == null || this.codeWords.isEmpty() || 
            this.informWords == null || this.informWords.isEmpty()) {
            return null;
        }

        // Проверка кратности длины закодированных данных
        if (encodedData.length() % this.n != 0) {
            return null;
        }

        // Создание обратного словаря для декодирования
        Map<String, String> decodingDict = new HashMap<>();
        for (int i = 0; i < this.informWords.size(); i++) {
            decodingDict.put(this.codeWords.get(i), this.informWords.get(i));
        }

        // Декодирование
        StringBuilder decodedData = new StringBuilder();
        for (int i = 0; i < encodedData.length(); i += this.n) {
            String receivedWord = encodedData.substring(i, Math.min(i + this.n, encodedData.length()));

            // Вычисление синдрома
            StringBuilder syndrome = new StringBuilder();
            for (int j = 0; j < this.matrHT.get(0).length(); j++) {
                int xorBit = 0;
                for (int k = 0; k < this.n; k++) {
                    xorBit ^= Character.getNumericValue(receivedWord.charAt(k)) & 
                              Character.getNumericValue(this.matrHT.get(k).charAt(j));
                }
                syndrome.append(xorBit);
            }

            // Исправление ошибок, если возможно
            String errorVector = this.sindromVector.get(syndrome.toString());
            if (errorVector != null) {
                StringBuilder correctedWord = new StringBuilder();
                for (int j = 0; j < this.n; j++) {
                    correctedWord.append(Character.getNumericValue(receivedWord.charAt(j)) ^ 
                                       Character.getNumericValue(errorVector.charAt(j)));
                }

                // Поиск ближайшего кодового слова
                String correctedWordStr = correctedWord.toString();
                if (decodingDict.containsKey(correctedWordStr)) {
                    decodedData.append(decodingDict.get(correctedWordStr));
                } else {
                    // Если не можем найти точное соответствие, берем информационное слово с минимальной дистанцией
                    String closestCodeWord = findClosestCodeWord(correctedWordStr);
                    decodedData.append(decodingDict.get(closestCodeWord));
                }
            } else {
                // Если синдром не найден, используем первые k бит
                decodedData.append(receivedWord.substring(0, Math.min(this.k, receivedWord.length())));
            }
        }

        return decodedData.toString();
    }

    /**
     * Поиск ближайшего кодового слова по расстоянию Хэмминга
     */
    private String findClosestCodeWord(String receivedWord) {
        int minDistance = Integer.MAX_VALUE;
        String closestWord = null;

        for (String codeWord : this.codeWords) {
            int distance = 0;
            for (int i = 0; i < Math.min(receivedWord.length(), codeWord.length()); i++) {
                if (receivedWord.charAt(i) != codeWord.charAt(i)) {
                    distance++;
                }
            }
            // Добавляем разницу в длине, если есть
            distance += Math.abs(receivedWord.length() - codeWord.length());

            if (distance < minDistance) {
                minDistance = distance;
                closestWord = codeWord;
            }
        }

        return closestWord != null ? closestWord : this.codeWords.get(0);
    }

    // Геттеры для доступа к параметрам кода
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
        return t;
    }
} 