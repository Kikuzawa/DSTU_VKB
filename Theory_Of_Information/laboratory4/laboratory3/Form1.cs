using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Windows.Forms;

namespace laboratory4
{
    public partial class Form1 : Form
    {


        private static CoderHuff Huff;
        String flag = "check";
        Dictionary<string, string> valueToBlockMap = new Dictionary<string, string>();
        SysMatrix startMatrix;
        SysMatrix endMatrix;
        int S = 0;



        string FlagModification = "defaultCode";

        public Form1()
        {
            Huff = new CoderHuff();
            InitializeComponent();

        }






        private void CreateNewTable()
        {


            foreach (DataGridViewRow row in dataGridICW.Rows)
            {
                object cellValue = row.Cells[0].Value; // Значение из первого столбца
                string key = cellValue != null ? cellValue.ToString() : ""; // Преобразуем только если не null

                cellValue = row.Cells[1].Value; // Значение из второго столбца
                string value = cellValue != null ? cellValue.ToString() : ""; // Преобразуем только если не null

                if (!valueToBlockMap.ContainsKey(key) && !string.IsNullOrEmpty(value)) // Проверяем, что оба значения не пусты
                {
                    valueToBlockMap[key] = value;
                }
            }
        }




        static List<string> SplitText(string text, int blockSize)
        {
            List<string> result = new List<string>();


            for (int i = 0; i < text.Length; i += blockSize)
            {
                if (i + blockSize <= text.Length)
                {
                    result.Add(text.Substring(i, blockSize));
                }
                else
                {
                    result.Add(text.Substring(i)); // Добавляем остаток строки
                }
            }

            return result;
        }






        private void radioButtonG_CheckedChanged(object sender, EventArgs e)
        {
            labelNameStartMatrix.Text = "G = ";
            labelNameStartSysMatrix.Text = "Gsys = ";
            labelNameEndSysMatrix.Text = "Hsys = ";
            flag = "born";
        }

        private void radioButtonH_CheckedChanged(object sender, EventArgs e)
        {
            labelNameStartMatrix.Text = "H = ";
            labelNameStartSysMatrix.Text = "Hsys = ";
            labelNameEndSysMatrix.Text = "Gsys = ";
            flag = "check";
        }

        private void GenerateMatrixButton_Click(object sender, EventArgs e)
        {

            int N = int.Parse(textNBox.Text);
            int K = int.Parse(textKBox.Text);

            dataGridStartMatrix.DataSource = SysMatrix.RandomMatrix(N, K);

            foreach (DataGridViewColumn column in dataGridStartMatrix.Columns)
            {
                column.Width = 30;
            }
        }



        private void button1_Click(object sender, EventArgs e)
        {
            DataTable matrix = new DataTable();
            matrix = (DataTable)dataGridStartMatrix.DataSource;
            startMatrix = new SysMatrix(SysMatrix.DataTableToMatrix(matrix), flag);


            dataGridStartSysMatrix.DataSource = SysMatrix.MatrixToDataTable(startMatrix.GetSysMatrix());
            dataGridEndSysMatrix.DataSource = SysMatrix.MatrixToDataTable(startMatrix.GetSecondMatrix());

            foreach (DataGridViewColumn column in dataGridStartSysMatrix.Columns)
            {
                column.Width = 30;
            }
            foreach (DataGridViewColumn column in dataGridEndSysMatrix.Columns)
            {
                column.Width = 30;
            }

            NBox.Text = startMatrix.GetN().ToString();
            KBox.Text = startMatrix.GetK().ToString();



            dataGridICW.DataSource = SysMatrix.MatrixToDataTable(startMatrix.SetInfoTable());
            dataGridICW.Columns[0].HeaderText = "i";
            dataGridICW.Columns[1].HeaderText = "c";
            dataGridICW.Columns[2].HeaderText = "W_h";

            foreach (DataGridViewColumn column in dataGridICW.Columns)
            {
                column.Width = 145;
            }

            DMinBox.Text = startMatrix.GetDmin().ToString();
            TBox.Text = startMatrix.GetT().ToString();
            PBox.Text = startMatrix.GetRo().ToString();

            CreateNewTable();





        }

        private void ProcessModidicationCode()
        {
            clearModification();

            switch (flag)
            {
                case "born":
                    ProcessModificationCodeWithBorn();
                    break;
                case "check":
                    ProcessModificationCodeWithCheck();
                    break;

            }


        }

        private void SysNormMatrix()
        {
            dataGridView2.DataSource = SysMatrix.MatrixToDataTable(endMatrix.GetSysMatrix());
            dataGridView4.DataSource = SysMatrix.MatrixToDataTable(endMatrix.GetSecondMatrix());

            foreach (DataGridViewColumn column in dataGridView2.Columns)
            {
                column.Width = 30;
            }
            foreach (DataGridViewColumn column in dataGridView4.Columns)
            {
                column.Width = 30;
            }

            textBox5.Text = endMatrix.GetN().ToString();
            textBox4.Text = endMatrix.GetK().ToString();

            textBox6.Text = endMatrix.GetN().ToString();
            textBox11.Text = endMatrix.GetK().ToString();



            dataGridView1.DataSource = SysMatrix.MatrixToDataTable(endMatrix.SetInfoTable());
            dataGridView1.Columns[0].HeaderText = "i";
            dataGridView1.Columns[1].HeaderText = "c";
            dataGridView1.Columns[2].HeaderText = "W_h";

            foreach (DataGridViewColumn column in dataGridView1.Columns)
            {
                column.Width = 145;
            }

            textBox3.Text = endMatrix.GetDmin().ToString();
            textBox2.Text = endMatrix.GetT().ToString();
            textBox1.Text = endMatrix.GetRo().ToString();

            textBox10.Text = endMatrix.GetDmin().ToString();
            textBox9.Text = endMatrix.GetT().ToString();
            textBox8.Text = endMatrix.GetRo().ToString();
        }
        private void ProcessModificationCodeWithCheck()
        {
            switch (FlagModification)
            {
                case "defaultCode":
                    endMatrix = new SysMatrix(startMatrix.GetSecondMatrix(), "born");
                    testDataSource(startMatrix.GetSysMatrix());
                    SysNormMatrix();
                    break;
                case "shortCode":
                    endMatrix = new SysMatrix(GetShortCode(startMatrix.GetSecondMatrix(), S), "born");
                    SysNormMatrix();
                    break;
                case "extensionCode":
                    endMatrix = new SysMatrix(GetExtensionCode(startMatrix.GetSysMatrix(), S), "check");
                    break;
                case "perforationCode":
                    endMatrix = new SysMatrix(GetPerforationCode(startMatrix.GetSysMatrix(), S), "check");
                    SysNormMatrix();
                    break;
                case "replenishmentCode":
                    endMatrix = new SysMatrix(GetReplenishmentCode(startMatrix.GetSecondMatrix(), S), "born");
                    break;

            }
        }

        private void ProcessModificationCodeWithBorn()
        {

            switch (FlagModification)
            {
                case "defaultCode":
                    endMatrix = new SysMatrix(startMatrix.GetSysMatrix(), "born");
                    testDataSource(startMatrix.GetSysMatrix());
                    SysNormMatrix();
                    break;
                case "shortCode":
                    endMatrix = new SysMatrix(GetShortCode(startMatrix.GetSysMatrix(), S), "born");
                    SysNormMatrix();
                    break;
                case "extensionCode":
                    endMatrix = new SysMatrix(GetExtensionCode(startMatrix.GetSecondMatrix(), S), "check");
                    break;
                case "perforationCode":
                    endMatrix = new SysMatrix(GetPerforationCode(startMatrix.GetSecondMatrix(), S), "check");
                    SysNormMatrix();
                    break;
                case "replenishmentCode":
                    endMatrix = new SysMatrix(GetReplenishmentCode(startMatrix.GetSysMatrix(), S), "born");
                    break;
            }


        }

        private int[,] GetShortCode(int[,] matrix, int S)
        {

            string input = textBox7.Text.Trim(); // Получаем текст из TextBox и обрезаем лишние пробелы

            // Разбиваем строку на подстроки по пробелу и преобразуем каждую подстроку в целое число
            int[] numbers = input.Split(' ')
                                 .Select(x => int.Parse(x) - 1)
                                 .ToArray();

            Array.Sort(numbers);

            matrix = RemoveRowsAndColumnsShort(matrix, numbers);


            testDataSource(matrix);
            return matrix;
        }

        private int[,] RemoveRowsAndColumnsShort(int[,] matrix, int[] indices)
        {
            // Определяем размеры новой матрицы после удаления строк и столбцов
            int newRowsCount = matrix.GetLength(0) - indices.Length;
            int newColsCount = matrix.GetLength(1) - indices.Length;

            if (newRowsCount <= 0 || newColsCount <= 0)
                throw new ArgumentException("Нельзя удалить все строки или столбцы.");

            // Создаем новую матрицу для хранения результата
            int[,] resultMatrix = new int[newRowsCount, newColsCount];

            // Массивы для отслеживания индексов оставшихся строк и столбцов
            bool[] rowsToKeep = new bool[matrix.GetLength(0)];
            bool[] colsToKeep = new bool[matrix.GetLength(1)];

            for (int i = 0; i < rowsToKeep.Length; ++i)
                rowsToKeep[i] = true;
            for (int j = 0; j < colsToKeep.Length; ++j)
                colsToKeep[j] = true;

            foreach (var index in indices)
            {
                rowsToKeep[index] = false;
                colsToKeep[index] = false;
            }

            // Копируем данные из старой матрицы в новую
            int rowIndex = 0;
            int colIndex = 0;
            for (int i = 0; i < matrix.GetLength(0); ++i)
            {
                if (!rowsToKeep[i])
                    continue;

                colIndex = 0;
                for (int j = 0; j < matrix.GetLength(1); ++j)
                {
                    if (!colsToKeep[j])
                        continue;

                    resultMatrix[rowIndex, colIndex++] = matrix[i, j];
                }
                rowIndex++;
            }


            return resultMatrix;
        }

        private int[,] GetExtensionCode(int[,] matrix, int S)
        {
            matrix = TransformMatrix(AddRowOfOnesToTop(matrix));


            testDataSource(matrix);
            int rows = matrix.GetLength(0);  // количество строк
            int cols = matrix.GetLength(1);  // количество столбцов

            textBox11.Text = rows.ToString();
            textBox6.Text = cols.ToString();

            return matrix;
        }

        private void clearModification()
        {
            dataGridView4.DataSource = null;
            dataGridView2.DataSource = null;
            dataGridView1.DataSource = null;
            textBox1.Text = "";
            textBox4.Text = "";
            textBox5.Text = "";
            textBox3.Text = "";
            textBox2.Text = "";
            textBox6.Text = "";
            textBox11.Text = "";
            textBox10.Text = "";
            textBox9.Text = "";
            textBox8.Text = "";

        }
        static int[,] TransformMatrix(int[,] originalMatrix)
        {
            // Получаем размеры оригинальной матрицы
            int rows = originalMatrix.GetLength(0);  // количество строк
            int cols = originalMatrix.GetLength(1);  // количество столбцов

            // Создаем новую матрицу с одним дополнительным столбцом слева
            int[,] newMatrix = new int[rows, cols + 1];

            // Проходим по каждой строке
            for (int i = 0; i < rows; ++i)
            {
                // Подсчитываем количество единиц в текущей строке
                int onesCount = 0;
                for (int j = 0; j < cols; ++j)
                    if (originalMatrix[i, j] == 1)
                        onesCount++;

                // Определяем, будет ли добавлен 0 или 1
                int toInsert = (onesCount % 2 == 0) ? 0 : 1;

                // Заполняем первый столбец новым значением
                newMatrix[i, 0] = toInsert;

                // Копируем остальную часть строки
                for (int j = 0; j < cols; ++j)
                    newMatrix[i, j + 1] = originalMatrix[i, j];
            }

            return newMatrix;
        }

        private int[,] GetPerforationCode(int[,] matrix, int S)
        {
            string input = textBox7.Text.Trim(); // Получаем текст из TextBox и обрезаем лишние пробелы

            // Разбиваем строку на подстроки по пробелу и преобразуем каждую подстроку в целое число
            int[] numbers = input.Split(' ')
                                 .Select(x => int.Parse(x) - 1)
                                 .ToArray();

            Array.Sort(numbers);

            matrix = RemoveRowsAndColumnsPerforation(matrix, numbers);


            testDataSource(matrix);
            return matrix;
        }

        static int[,] AddRowOfOnesToTop(int[,] originalMatrix)
        {
            // Получаем размеры оригинальной матрицы
            int rows = originalMatrix.GetLength(0);  // количество строк
            int cols = originalMatrix.GetLength(1);  // количество столбцов

            // Создаем новую матрицу с одной дополнительной строкой
            int[,] newMatrix = new int[rows + 1, cols];

            // Заполняем первую строку единицами
            for (int j = 0; j < cols; ++j)
                newMatrix[0, j] = 1;

            // Копируем содержимое оригинальной матрицы начиная со второй строки новой матрицы
            for (int i = 0; i < rows; ++i)
                for (int j = 0; j < cols; ++j)
                    newMatrix[i + 1, j] = originalMatrix[i, j];

            return newMatrix;
        }

        private int[,] RemoveRowsAndColumnsPerforation(int[,] matrix, int[] indices)
        {
            // Определяем размеры новой матрицы после удаления строк и столбцов
            int newRowsCount = matrix.GetLength(0) - indices.Length;
            int newColsCount = matrix.GetLength(1) - indices.Length;

            if (newRowsCount <= 0 || newColsCount <= 0)
                throw new ArgumentException("Нельзя удалить все строки или столбцы.");

            // Создаем новую матрицу для хранения результата
            int[,] resultMatrix = new int[newRowsCount, newColsCount];

            // Массивы для отслеживания индексов оставшихся строк и столбцов
            bool[] rowsToKeep = new bool[matrix.GetLength(0)];
            bool[] colsToKeep = new bool[matrix.GetLength(1)];

            for (int i = 0; i < rowsToKeep.Length; ++i)
                rowsToKeep[i] = true;
            for (int j = 0; j < colsToKeep.Length; ++j)
                colsToKeep[j] = true;

            foreach (var index in indices)
            {
                rowsToKeep[index] = false;
                colsToKeep[matrix.GetLength(1) - matrix.GetLength(0) + index] = false;
            }

            // Копируем данные из старой матрицы в новую
            int rowIndex = 0;
            int colIndex = 0;
            for (int i = 0; i < matrix.GetLength(0); ++i)
            {
                if (!rowsToKeep[i])
                    continue;

                colIndex = 0;
                for (int j = 0; j < matrix.GetLength(1); ++j)
                {
                    if (!colsToKeep[j])
                        continue;

                    resultMatrix[rowIndex, colIndex++] = matrix[i, j];
                }
                rowIndex++;
            }


            return resultMatrix;
        }

        private int[,] GetReplenishmentCode(int[,] matrix, int S)
        {
            matrix = AddRowOfOnesToTop(matrix);

            testDataSource(matrix);
            int rows = matrix.GetLength(0);  // количество строк
            int cols = matrix.GetLength(1);  // количество столбцов

            textBox11.Text = rows.ToString();
            textBox6.Text = cols.ToString();
            return matrix;
        }



        private void dataGridICW_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void radioButton5_CheckedChanged(object sender, EventArgs e)
        {
            FlagModification = "replenishmentCode";
            label11.Text = "Gadd";
            label10.Text = "Hadd";
            label21.Text = "Gadd";
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            FlagModification = "defaultCode";
            label11.Text = "Gsys";
            label10.Text = "Hsys";
            label21.Text = "";
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            FlagModification = "shortCode";
            label11.Text = "Gs";
            label10.Text = "Hs";
            label21.Text = "Gs";
        }

        private void radioButton3_CheckedChanged(object sender, EventArgs e)
        {
            FlagModification = "extensionCode";
            label11.Text = "Hext";
            label10.Text = "Gext";
            label21.Text = "Hext";
        }

        private void radioButton4_CheckedChanged(object sender, EventArgs e)
        {
            FlagModification = "perforationCode";
            label11.Text = "Hp";
            label10.Text = "Gp";
            label21.Text = "Hp";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            ProcessModidicationCode();
        }

        private void textBox7_TextChanged(object sender, EventArgs e)
        {

        }

        private void testDataSource(int[,] matrix)
        {
            dataGridView3.DataSource = SysMatrix.MatrixToDataTable(matrix);

            foreach (DataGridViewColumn column in dataGridView3.Columns)
            {
                column.Width = 30;
            }
        }
    }
}
