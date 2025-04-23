package org.example;

import java.util.Arrays;

public class Polynomial {
    private final int[] coefficients;
    private final int degree;

    public Polynomial(int[] coefficients) {
        this.coefficients = Arrays.copyOf(coefficients, coefficients.length);
        this.degree = coefficients.length - 1;
    }

    public static Polynomial fromString(String str) {
        // Remove all whitespace and split by +
        String cleanStr = str.replaceAll("\\s+", "");
        String[] parts = cleanStr.split("\\+");
        
        // Find maximum degree
        int maxDegree = 0;
        for (String part : parts) {
            if (part.contains("x^")) {
                int degree = Integer.parseInt(part.split("\\^")[1]);
                maxDegree = Math.max(maxDegree, degree);
            } else if (part.contains("x")) {
                maxDegree = Math.max(maxDegree, 1);
            } else if (!part.isEmpty()) {
                maxDegree = Math.max(maxDegree, 0);
            }
        }

        int[] coeffs = new int[maxDegree + 1];
        for (String part : parts) {
            if (part.isEmpty()) continue;
            
            if (part.contains("x^")) {
                String[] split = part.split("x\\^");
                int coeff = split[0].isEmpty() ? 1 : Integer.parseInt(split[0]);
                int degree = Integer.parseInt(split[1]);
                coeffs[degree] = coeff;
            } else if (part.contains("x")) {
                String coeff = part.replace("x", "");
                coeffs[1] = coeff.isEmpty() ? 1 : Integer.parseInt(coeff);
            } else {
                coeffs[0] = Integer.parseInt(part);
            }
        }
        return new Polynomial(coeffs);
    }

    public Polynomial multiply(Polynomial other) {
        int[] result = new int[this.degree + other.degree + 1];
        for (int i = 0; i <= this.degree; i++) {
            for (int j = 0; j <= other.degree; j++) {
                result[i + j] ^= (this.coefficients[i] & other.coefficients[j]);
            }
        }
        return new Polynomial(result);
    }

    public Polynomial divide(Polynomial divisor) {
        int[] dividend = Arrays.copyOf(this.coefficients, this.coefficients.length);
        int[] quotient = new int[this.degree - divisor.degree + 1];
        
        for (int i = this.degree; i >= divisor.degree; i--) {
            if (dividend[i] == 1) {
                quotient[i - divisor.degree] = 1;
                for (int j = 0; j <= divisor.degree; j++) {
                    dividend[i - j] ^= divisor.coefficients[divisor.degree - j];
                }
            }
        }
        
        return new Polynomial(quotient);
    }

    public Polynomial mod(Polynomial divisor) {
        int[] dividend = Arrays.copyOf(this.coefficients, this.coefficients.length);
        
        for (int i = this.degree; i >= divisor.degree; i--) {
            if (dividend[i] == 1) {
                for (int j = 0; j <= divisor.degree; j++) {
                    dividend[i - j] ^= divisor.coefficients[divisor.degree - j];
                }
            }
        }
        
        int[] remainder = Arrays.copyOf(dividend, divisor.degree);
        return new Polynomial(remainder);
    }

    public int[] getCoefficients() {
        return Arrays.copyOf(coefficients, coefficients.length);
    }

    public int getDegree() {
        return degree;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = degree; i >= 0; i--) {
            if (coefficients[i] != 0) {
                if (sb.length() > 0) {
                    sb.append(" + ");
                }
                if (i == 0) {
                    sb.append(coefficients[i]);
                } else if (i == 1) {
                    sb.append(coefficients[i]).append("x");
                } else {
                    sb.append(coefficients[i]).append("x^").append(i);
                }
            }
        }
        return sb.toString();
    }
} 