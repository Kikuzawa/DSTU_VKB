using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;


namespace laboratory3
{
    internal class SysMatrix
    {
        
        int[,] matrix;
        int[,] sysmatrix;
        int[,] secondSysMatrix;
        int[,] result, identityMatrix;
        int n = 0, k = 0, dmin = 0, ro = 0;
        float t;
        String flag;
        String[,] infoTable;
        int[,] HsysTmatrix;

        String[,] errorTable;

       
        public SysMatrix(int[,] matrix, String flag)
        {
            this.matrix = matrix;
            sysmatrix = CopyMatrix(matrix);
            this.flag = flag;
            secondSysMatrix = CopyMatrix(matrix);
            SetSysMatrix(flag);
        }
        public void SetSysMatrix(String flag)
        {

            int rows = sysmatrix.GetLength(0);  // Количество строк
            int cols = sysmatrix.GetLength(1);  // Количество столбцов

            // Переменная для подсчета удаленных столбцов
            int deletedColsCount = 0;

            // Копируем исходную матрицу, чтобы не изменять её напрямую
            int[,] arrCopy = CopyMatrix(sysmatrix);

            // Проходим по каждому столбцу
            for (int colIndex = 0; colIndex < cols; colIndex++)
            {
                int onesCount = 0;
                int zerosCount = 0;

                // Считаем количество единиц и нулей в текущем столбце
                for (int rowIndex = 0; rowIndex < rows; rowIndex++)
                {
                    if (arrCopy[rowIndex, colIndex] == 1)
                        onesCount++;
                    else
                        zerosCount++;
                }

                // Если в столбце только одна единица, то перемещаем его в начало
                if (onesCount == 1 && zerosCount == rows - 1)
                {
                    // Удаляем текущий столбец и вставляем его в начало

                    sysmatrix = DeleteColumnAndInsertAtBeginning(sysmatrix, colIndex - deletedColsCount);


                    // Увеличиваем счетчик удаленных столбцов
                    deletedColsCount++;
                }
            }



            // Формируем итоговую систематическую матрицу
            identityMatrix = CreateIdentityMatrix(rows);

            result = RemoveDuplicateColumns(sysmatrix, identityMatrix);

            if (flag == "check")
            {
                this.sysmatrix = ConcatenateMatrices(result, identityMatrix);
                secondSysMatrix = ConcatenateMatrices(CreateIdentityMatrix(TransposeMatrix(result).GetLength(0)), TransposeMatrix(result));
                n = secondSysMatrix.GetLength(1);
                k = secondSysMatrix.GetLength(0);
                HsysTmatrix = TransposeMatrix(sysmatrix);
            }
            else
            {
                this.sysmatrix = ConcatenateMatrices(identityMatrix, result);
                secondSysMatrix = ConcatenateMatrices(TransposeMatrix(result), CreateIdentityMatrix(TransposeMatrix(result).GetLength(0)));
                n = sysmatrix.GetLength(1);
                k = sysmatrix.GetLength(0);
                HsysTmatrix = TransposeMatrix(secondSysMatrix);
            }

            SetErrorTable();



        }

        public static int[,] TransposeMatrix(int[,] matrix)
        {
            int rows = matrix.GetLength(0);
            int cols = matrix.GetLength(1);
            int[,] transposed = new int[cols, rows];

            for (int i = 0; i < rows; ++i)
            {
                for (int j = 0; j < cols; ++j)
                {
                    transposed[j, i] = matrix[i, j];
                }
            }

            return transposed;
        }

        public void SetErrorTable()
        {
            string[] errorVectors = GenerateErrorVectors();

            int[,] resultVectors = ComputeResultVectors(errorVectors);
            

            string[,] combinedMatrix = CombineMatrices(errorVectors, resultVectors);

            errorTable = combinedMatrix;

        }

        public string FindErrorVectorByResultVector(string resultVector)
        {
            // Перебираем все строки в комбинированной матрице
            for (int i = 0; i < errorTable.GetLength(0); ++i)
            {
                // Сравниваем значение второго столбца с искомым значением
                if (errorTable[i, 1].Equals(resultVector))
                {
                    // Если найдено совпадение, возвращаем значение из первого столбца
                    return errorTable[i, 0];
                }
            }

            // Если совпадений нет, возвращаем null
            return null;
        }

        public string FindInfoWordByCodeWord(string codeWord)
        {
            // Перебираем все строки в таблице
            for (int i = 0; i < infoTable.GetLength(0); ++i)
            {
                // Сравниваем значение второго столбца с искомым значением
                if (infoTable[i, 1].Equals(codeWord))
                {
                    // Если найдено совпадение, возвращаем значение из первого столбца
                    return infoTable[i, 0];
                }
            }

            // Если совпадений нет, возвращаем null
            return null;
        }


        public int[,] GetHSysTmatrix()
        {
            return HsysTmatrix;
        }
        private static string[,] CombineMatrices(string[] errorVectors, int[,] resultVectors)
        {
            int numRows = errorVectors.Length;
            int numCols = 2; // Два столбца: один для errorVectors, другой для resultVectors

            string[,] combinedMatrix = new string[numRows, numCols];
            
            for (int i = 0; i < numRows; ++i)
            {
                combinedMatrix[i, 0] = errorVectors[i]; // Сохраняем строку из errorVectors в первый столбец

                // Формируем строку из resultVectors для текущей строки
                StringBuilder resultVectorAsString = new StringBuilder();
                for (int j = 0; j < resultVectors.GetLength(1); ++j)
                    resultVectorAsString.Append(resultVectors[i, j]);

                combinedMatrix[i, 1] = resultVectorAsString.ToString(); // Сохраняем сформированную строку во второй столбец

               
            }

            return combinedMatrix;
        }

        private string[] GenerateErrorVectors()
        {

            string[] errorVectors = new string[n + 1];
            StringBuilder sb1 = new StringBuilder(new string('0', n));
            errorVectors[0] = sb1.ToString();
            for (int i = 1; i < n + 1; ++i)
            {
                StringBuilder sb = new StringBuilder(new string('0', n));
                sb[n - i] = '1';
                errorVectors[i] = sb.ToString();
            }

            return errorVectors;
        }

        public string VectorAddMod2(string strVec1, string strVec2)
        {
            

            // Результирующая строка
            StringBuilder result = new StringBuilder();

            // Проходим по каждому символу в строках
            for (int i = 0; i < strVec1.Length; i++)
            {
                char a = strVec1[i];
                char b = strVec2[i];

                // Выполняем XOR для текущего символа
                int xorResult = (a - '0') ^ (b - '0');

                // Добавляем результат в результирующую строку
                result.Append(xorResult);
            }

            return result.ToString();
        }

        private int[,] ComputeResultVectors(string[] errorVectors)
        {
            int numRows = errorVectors.Length;
            int numCols = HsysTmatrix.GetLength(1);

            int[,] resultVectors = new int[numRows, numCols];

            for (int i = 0; i < numRows; ++i)
            {
                int[] currentVector = ConvertToIntArray(errorVectors[i]);
                MultiplyAndStore(currentVector, ref resultVectors, i);
            }

            return resultVectors;
        }

        private int[] ConvertToIntArray(string vectorStr)
        {
            int[] vector = new int[vectorStr.Length];
            for (int i = 0; i < vectorStr.Length; ++i)
                vector[i] = vectorStr[i] == '1' ? 1 : 0;

            return vector;
        }

        private void MultiplyAndStore(int[] currentVector, ref int[,] resultVectors, int rowIndex)
        {
            for (int col = 0; col < HsysTmatrix.GetLength(1); ++col)
            {
                int sum = 0;
                for (int k = 0; k < HsysTmatrix.GetLength(0); ++k)
                    sum += currentVector[k] * HsysTmatrix[k, col];

                resultVectors[rowIndex, col] = sum % 2; // Операция по модулю 2
            }
        }
        public bool[] StringToBoolArray(string v)
        {
            return v.Select(c => c == '1').ToArray();
        }

        public String GetErrorS(string vector)
        {
            // Создаем результатирующий синдром
            bool[] v = StringToBoolArray(vector);

            // Получаем размеры матрицы
            int m = HsysTmatrix.GetLength(0); // Количество строк
            int n = HsysTmatrix.GetLength(1); // Количество столбцов

            // Инициализация синдрома с правильной длиной
            bool[] syndrome = new bool[n]; // Длина синдрома равна числу столбцов в матрице

            for (int j = 0; j < n; ++j)
            {
                for (int i = 0; i < m; ++i)
                {
                    syndrome[j] ^= v[i] & Convert.ToBoolean(HsysTmatrix[i, j]);
                }
            }

            string sindrom = string.Join("", syndrome.Select(bit => bit ? "1" : "0"));

            return sindrom;
        }


        public int[,] GetSecondMatrix() { return secondSysMatrix; }

        // Функция для удаления столбцов из первой матрицы, которые совпадают со столбцами второй матрицы
        private static int[,] RemoveDuplicateColumns(int[,] firstMatrix, int[,] secondMatrix)
        {
            int rowsFirst = firstMatrix.GetLength(0);
            int colsFirst = firstMatrix.GetLength(1);
            int colsSecond = secondMatrix.GetLength(1);

            List<int> columnsToKeep = new List<int>(Enumerable.Range(0, colsFirst)); // Изначально предполагаем, что все столбцы будут сохранены
            HashSet<int> usedColumns = new HashSet<int>(); // Набор использованных столбцов второй матрицы

            // Перебираем столбцы первой матрицы
            for (int colFirst = 0; colFirst < colsFirst; colFirst++)
            {
                // Сравниваем текущий столбец первой матрицы с каждым столбцом второй матрицы
                for (int colSecond = 0; colSecond < colsSecond; colSecond++)
                {
                    if (usedColumns.Contains(colSecond)) continue; // Пропускаем уже использованные столбцы второй матрицы

                    bool match = true;

                    for (int row = 0; row < rowsFirst; row++)
                    {
                        if (firstMatrix[row, colFirst] != secondMatrix[row, colSecond])
                        {
                            match = false;
                            break;
                        }
                    }

                    if (match)
                    {
                        columnsToKeep.Remove(colFirst); // Если нашли совпадение, удаляем столбец из списка для сохранения
                        usedColumns.Add(colSecond); // Отмечаем, что столбец второй матрицы был использован
                        break; // Прерываем дальнейшую проверку для данного столбца
                    }
                }
            }

            // Создаем новую матрицу с нужными столбцами
            int newCols = columnsToKeep.Count;
            int[,] result = new int[rowsFirst, newCols];

            for (int i = 0; i < rowsFirst; i++)
            {
                for (int j = 0; j < newCols; j++)
                {
                    result[i, j] = firstMatrix[i, columnsToKeep[j]];
                }
            }

            return result;
        }

        // Функция для копирования матрицы
        private static int[,] CopyMatrix(int[,] matrix)
        {
            int rows = matrix.GetLength(0);
            int cols = matrix.GetLength(1);
            int[,] copy = new int[rows, cols];

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    copy[i, j] = matrix[i, j];
                }
            }

            return copy;
        }

        // Функция для создания единичной матрицы
        private static int[,] CreateIdentityMatrix(int size)
        {
            int[,] identity = new int[size, size];

            for (int i = 0; i < size; i++)
            {
                identity[i, i] = 1;
            }

            return identity;
        }


        public string[,] GetErrorTable()
        {
            return errorTable;
        }

        // Функция для удаления столбца и вставки его в начало
        private static int[,] DeleteColumnAndInsertAtBeginning(int[,] matrix, int columnIndex)
        {
            int rows = matrix.GetLength(0);
            int cols = matrix.GetLength(1);

            // Создаем новую матрицу с тем же количеством столбцов
            int[,] result = new int[rows, cols];

            // Заполняем результат новыми значениями
            for (int i = 0; i < rows; i++)
            {
                // Сначала копируем элемент из удаленного столбца в первый столбец новой матрицы
                result[i, 0] = matrix[i, columnIndex];

                // Затем копируем остальные элементы
                for (int j = 1; j < cols; j++)
                {
                    if (j <= columnIndex)
                        result[i, j] = matrix[i, j - 1]; // Элементы до удаленного столбца смещаются на один влево
                    else
                        result[i, j] = matrix[i, j];     // Оставшиеся элементы остаются на своих местах
                }
            }

            return result;
        }

        // Функция для объединения двух матриц горизонтально
        private static int[,] ConcatenateMatrices(int[,] left, int[,] right)
        {
            int rows = left.GetLength(0);
            int leftCols = left.GetLength(1);
            int rightCols = right.GetLength(1);

            int[,] result = new int[rows, leftCols + rightCols];

            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < leftCols; j++)
                {
                    result[i, j] = left[i, j];
                }

                for (int j = 0; j < rightCols; j++)
                {
                    result[i, j + leftCols] = right[i, j];
                }
            }

            return result;
        }

        // Метод для доступа к элементам матрицы
        
        public int[,] GetSysMatrix() { return sysmatrix; }

        public int GetN()
        {
            return n;
        }

        public int GetK()
        {
            return k;
        }

        public int GetDmin()
        {

            return dmin;
        }

        public float GetT()
        {

            return t;
        }

        public int GetRo()
        {
            return ro;
        }

        public String[,] SetInfoTable()
        {

            int[,] G;
            if (flag == "check")
            {
                G = secondSysMatrix;
            }
            else
            {
                G = sysmatrix;
            }
            // Создаем таблицу для хранения всех возможных вариантов
            String[,] table = new String[(1 << k), 3]; // Таблица размером 2^k на 3

            // Заполняем таблицу
            for (int i = 0; i < (1 << k); ++i)
            {
                // Информационное слово i
                string infoWord = Convert.ToString(i, 2).PadLeft(k, '0');

                // Кодовое слово c
                StringBuilder codeWord = new StringBuilder();
                for (int col = 0; col < n; ++col)
                {
                    int bit = 0;
                    for (int row = 0; row < k; ++row)
                    {
                        if ((infoWord[row] == '1') && (G[row, col] == 1))
                            bit ^= 1;
                    }
                    codeWord.Append(bit);
                }

                // Количество единиц в кодовом слове Wh

                int weightH = codeWord.ToString().Count(ch => ch == '1');

                // Добавляем данные в таблицу
                table[i, 0] = infoWord;
                table[i, 1] = codeWord.ToString();
                table[i, 2] = weightH.ToString();
            }

            infoTable = table;
            dmin = GetMinNonZeroValue();
            t = (dmin - 1) / 2;
            ro = dmin - 1;

            return infoTable;
        }


        public int GetMinNonZeroValue()
        {
            int minValue = int.MaxValue;

            for (int i = 0; i < infoTable.GetLength(0); i++)
            {
                int currentValue;
                if (int.TryParse(infoTable[i, 2], out currentValue) && currentValue > 0)
                {
                    minValue = Math.Min(minValue, currentValue);
                }
            }

            return minValue == int.MaxValue ? -1 : minValue;
        }



        public static DataTable MatrixToDataTable(int[,] matrix)
        {
            // Определение размеров матрицы
            int rows = matrix.GetLength(0);
            int cols = matrix.GetLength(1);

            // Создание таблицы
            DataTable table = new DataTable();

            // Добавление столбцов
            for (int i = 0; i < cols; i++)
            {
                table.Columns.Add($"{i + 1}", typeof(int));
            }

            // Заполнение строк данными
            for (int i = 0; i < rows; i++)
            {
                DataRow row = table.NewRow();
                for (int j = 0; j < cols; j++)
                {
                    row[j] = matrix[i, j];
                }
                table.Rows.Add(row);
            }

            return table;
        }

        public static string IntroduceError(string input)
        {
            Random random = new Random();
            int position = random.Next(0, input.Length);

            char[] chars = input.ToCharArray();
            chars[position] = chars[position] == '0' ? '1' : '0';

            return new string(chars);
        }


        public static int[,] DataTableToMatrix(DataTable table)
        {
            // Определение размеров таблицы
            int rows = table.Rows.Count;
            int cols = table.Columns.Count;

            // Создание матрицы
            int[,] matrix = new int[rows, cols];

            // Заполнение матрицы данными из таблицы
            for (int i = 0; i < rows; i++)
            {
                for (int j = 0; j < cols; j++)
                {
                    matrix[i, j] = Convert.ToInt32(table.Rows[i][j]);
                }
            }

            return matrix;
        }

        public static DataTable shuffleTable(DataTable inputTable, int shuffleIterations)
        {
            int index;
            System.Random rnd = new Random();

            for (int i = 0; i < shuffleIterations; i++)
            {
                index = rnd.Next(0, inputTable.Rows.Count - 1);
                inputTable.Rows.Add(inputTable.Rows[index].ItemArray);
                inputTable.Rows.RemoveAt(index);
            }
            return inputTable;
        }

        public static DataTable RandomMatrix(int N, int K)
        {
            Random random = new Random();

        // Create DataTable
        DataTable matrixTable = new DataTable();

            // Add columns
            for (int i = 0; i < N; i++)
            {
                matrixTable.Columns.Add($"{i + 1}", typeof(int));
            }

            // Add rows
            for (int i = 0; i < K; i++)
            {
                DataRow row = matrixTable.NewRow();
                for (int j = 0; j < N; j++)
                {
                    if (i == j)
                    {
                        row[j] = 1;
                    }
                    else
                    {
                        if (j < K)
                        {
                            row[j] = 0;
                        }
                        else { row[j] = random.Next(2); }
                    }


                }
                matrixTable.Rows.Add(row);
            }

            return shuffleTable(matrixTable, 5);
        }

        public static DataTable MatrixToDataTable(string[,] matrix)
        {// Определение размеров матрицы
            int rows = matrix.GetLength(0);
            int cols = matrix.GetLength(1);

            // Создание таблицы
            DataTable table = new DataTable();

            // Добавление столбцов
            for (int i = 0; i < cols; i++)
            {
                table.Columns.Add($"{i + 1}");
            }

            // Заполнение строк данными
            for (int i = 0; i < rows; i++)
            {
                DataRow row = table.NewRow();
                for (int j = 0; j < cols; j++)
                {
                    row[j] = matrix[i, j];
                }
                table.Rows.Add(row);
            }

            return table;
        }
    }
}
