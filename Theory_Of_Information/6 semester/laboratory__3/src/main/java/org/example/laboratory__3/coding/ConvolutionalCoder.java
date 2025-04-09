package org.example.laboratory__3.coding;

import java.util.Arrays;
import java.util.List;

/**
 * Класс для реализации сверточного кодирования
 */
public class ConvolutionalCoder {
    private List<String> polynomials;
    private int constraintLength;
    private int[] registers;

    public ConvolutionalCoder(List<String> polynomials, int constraintLength) {
        this.polynomials = polynomials;
        this.constraintLength = constraintLength;
        this.registers = new int[constraintLength - 1];
    }

    /**
     * Сверточное кодирование
     */
    public String encode(String data) {
        if (data == null || data.isEmpty()) {
            return null;
        }

        // Инициализация регистров
        Arrays.fill(registers, 0);

        StringBuilder result = new StringBuilder();
        for (char bit : data.toCharArray()) {
            // Сдвиг регистров и добавление нового бита
            System.arraycopy(registers, 0, registers, 1, registers.length - 1);
            registers[0] = bit - '0';

            // Вычисление выходных битов для каждого полинома
            for (String polynomial : polynomials) {
                int output = 0;
                for (int i = 0; i < polynomial.length(); i++) {
                    if (polynomial.charAt(i) == '1' && i < registers.length + 1) {
                        output ^= (i == 0) ? (bit - '0') : registers[i - 1];
                    }
                }
                result.append(output);
            }
        }

        // Добавление нулей для завершения кодирования
        for (int i = 0; i < constraintLength - 1; i++) {
            System.arraycopy(registers, 0, registers, 1, registers.length - 1);
            registers[0] = 0;

            for (String polynomial : polynomials) {
                int output = 0;
                for (int j = 0; j < polynomial.length(); j++) {
                    if (polynomial.charAt(j) == '1' && j < registers.length + 1) {
                        output ^= (j == 0) ? 0 : registers[j - 1];
                    }
                }
                result.append(output);
            }
        }

        return result.toString();
    }

    /**
     * Декодирование методом Витерби
     */
    public String decode(String encodedData) {
        if (encodedData == null || encodedData.isEmpty()) {
            return null;
        }

        int numOutputs = polynomials.size();
        int numStates = 1 << (constraintLength - 1);
        int[] pathMetrics = new int[numStates];
        int[] pathHistory = new int[encodedData.length() / numOutputs];
        Arrays.fill(pathMetrics, Integer.MAX_VALUE);
        pathMetrics[0] = 0;

        // Декодирование
        for (int i = 0; i < encodedData.length(); i += numOutputs) {
            String receivedBits = encodedData.substring(i, Math.min(i + numOutputs, encodedData.length()));
            int[] newPathMetrics = new int[numStates];
            Arrays.fill(newPathMetrics, Integer.MAX_VALUE);

            for (int state = 0; state < numStates; state++) {
                for (int input = 0; input < 2; input++) {
                    int nextState = ((state << 1) | input) & (numStates - 1);
                    String outputBits = getOutputBits(state, input);
                    int hammingDistance = getHammingDistance(outputBits, receivedBits);
                    int newMetric = pathMetrics[state] + hammingDistance;

                    if (newMetric < newPathMetrics[nextState]) {
                        newPathMetrics[nextState] = newMetric;
                        pathHistory[i / numOutputs] = state;
                    }
                }
            }

            System.arraycopy(newPathMetrics, 0, pathMetrics, 0, numStates);
        }

        // Восстановление исходного сообщения
        StringBuilder result = new StringBuilder();
        int state = pathHistory[pathHistory.length - 1];
        for (int i = pathHistory.length - 1; i > 0; i--) {
            result.insert(0, state & 1);
            state = pathHistory[i - 1];
        }

        return result.toString();
    }

    /**
     * Получение выходных битов для заданного состояния и входного бита
     */
    private String getOutputBits(int state, int input) {
        StringBuilder output = new StringBuilder();
        int[] registers = new int[constraintLength];
        registers[0] = input;
        for (int i = 1; i < constraintLength; i++) {
            registers[i] = (state >> (i - 1)) & 1;
        }

        for (String polynomial : polynomials) {
            int outputBit = 0;
            for (int i = 0; i < polynomial.length(); i++) {
                if (polynomial.charAt(i) == '1' && i < registers.length) {
                    outputBit ^= registers[i];
                }
            }
            output.append(outputBit);
        }

        return output.toString();
    }

    /**
     * Вычисление расстояния Хэмминга между двумя строками
     */
    private int getHammingDistance(String s1, String s2) {
        int distance = 0;
        int minLength = Math.min(s1.length(), s2.length());
        for (int i = 0; i < minLength; i++) {
            if (s1.charAt(i) != s2.charAt(i)) {
                distance++;
            }
        }
        return distance + Math.abs(s1.length() - s2.length());
    }

    // Геттеры для доступа к параметрам кодирования
    public List<String> getPolynomials() {
        return polynomials;
    }

    public int getConstraintLength() {
        return constraintLength;
    }
} 