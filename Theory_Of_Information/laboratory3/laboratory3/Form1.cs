using System;
using System.Collections.Generic;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace laboratory3
{
    public partial class Form1 : Form
    {


        private static CoderHuff Huff;
        String flag = "check";
        Dictionary<string, string> valueToBlockMap = new Dictionary<string, string>();
        SysMatrix newMatrix;
        String textHuff;
        String textHaus;
        String textHausWithError;
        String output;
        int count = 0;
        public Form1()
        {
            Huff = new CoderHuff();
            InitializeComponent();
            
        }

        public string CheckLengthAndAddZeros(string input, int i)
        {
            int length = input.Length;

            // Проверяем, кратна ли длина строки i
            if (length % i != 0)
            {
                // Если нет, добавляем недостающие нули
                int missingZeros = i - (length % i);
                count = missingZeros;
                if (count > 0) {
                    string il = "";
                testBox.Text = testBox.Text + il.PadRight(missingZeros, '0'); }
                input = input.PadRight(length + missingZeros, '0');
            }

            return input;
        }


        private void testButton_Click(object sender, EventArgs e)
        {

            textHuff = "";


            textHaus = "";
            textHausWithError = "";
            output = "";
            testBox.Clear();
            textBox2.Clear();
            textBox3.Clear();
            textBox8.Clear();


           
            Huff = new CoderHuff();


            textHuff = Huff.EncodeHaffman(textBox1.Text);

          
            testBox.Text = textHuff;






            textHaus = DoubleEncodeHaffman(testBox.Text, newMatrix.GetK());
            textBox2.Text = textHaus;
            textHausWithError = DoubleEncodeHaffman2(testBox.Text, newMatrix.GetK());
            textBox3.Text = textHausWithError;

            output = textHausWithError.Replace(" ", "");
            textBox8.Text = output;

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
        private String DoubleEncodeHaffman(String Text, int k)
        {

            StringBuilder sb = new StringBuilder();
            List<string> blocks = SplitText(Text, k);

            foreach (string block in blocks)
            {
                try
                {


                    String blockNew = CheckLengthAndAddZeros(block, k);
                    
                    sb.Append(valueToBlockMap[blockNew] + " ");

                }
                catch { }

            }


            return sb.ToString();
        }

        private String DoubleEncodeHaffman2(String Text, int k)
        {

            StringBuilder sb = new StringBuilder();
            List<string> blocks = SplitText(Text, k);

            foreach (string block in blocks)
            {
                try
                {
                    String blockNew = CheckLengthAndAddZeros(block, k);
                    sb.Append(SysMatrix.IntroduceError(valueToBlockMap[blockNew]) + " ");
                }
                catch { }

            }


            return sb.ToString();
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


        private void testButton2_Click(object sender, EventArgs e)
        {
            textBox5.Clear();
            textBox7.Clear();
            textBox10.Clear();
            textBox4.Clear();
            textBox6.Clear();
            String inputText = textBox9.Text;


            StringBuilder sb2 = new StringBuilder();
            List<string> blocks = SplitText(inputText, newMatrix.GetN());

            foreach (string block in blocks)
            {
                try
                {
                    sb2.Append(block + " ");
                }
                catch { }

            }

            sb2.Remove(sb2.Length - 1, 1);




            String inputS = sb2.ToString();



            String[] input = inputS.Split();

            for (int i = 0; i < input.Length; i++)
            {
                String v = input[i];
                try
                {
                    string S = newMatrix.GetErrorS(v);
                    textBox4.AppendText(S + " ");
                    string ee = newMatrix.FindErrorVectorByResultVector(S);
                    textBox5.AppendText(ee + " ");
                    string c = newMatrix.VectorAddMod2(v, ee);
                    textBox7.AppendText(c + " ");
                    string encode = newMatrix.FindInfoWordByCodeWord(c);
                    
                    textBox10.AppendText(encode);
                }
                catch { }
            }

            if (count != 0) { textBox6.Text = Huff.DecodeMethod(textBox10.Text.Remove(textBox10.Text.Length - count)); }
            else { textBox6.Text = Huff.DecodeMethod(textBox10.Text); }



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
           

        private void button2_Click(object sender, EventArgs e)
        {
            textBox9.Text = output;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            DataTable matrix = new DataTable();
            matrix = (DataTable)dataGridStartMatrix.DataSource;
            newMatrix = new SysMatrix(SysMatrix.DataTableToMatrix(matrix), flag);


            dataGridStartSysMatrix.DataSource = SysMatrix.MatrixToDataTable(newMatrix.GetSysMatrix());
            dataGridEndSysMatrix.DataSource = SysMatrix.MatrixToDataTable(newMatrix.GetSecondMatrix());

            foreach (DataGridViewColumn column in dataGridStartSysMatrix.Columns)
            {
                column.Width = 30;
            }
            foreach (DataGridViewColumn column in dataGridEndSysMatrix.Columns)
            {
                column.Width = 30;
            }

            NBox.Text = newMatrix.GetN().ToString();
            KBox.Text = newMatrix.GetK().ToString();



            dataGridICW.DataSource = SysMatrix.MatrixToDataTable(newMatrix.SetInfoTable());
            dataGridICW.Columns[0].HeaderText = "i";
            dataGridICW.Columns[1].HeaderText = "c";
            dataGridICW.Columns[2].HeaderText = "W_h";

            foreach (DataGridViewColumn column in dataGridICW.Columns)
            {
                column.Width = 145;
            }

            DMinBox.Text = newMatrix.GetDmin().ToString();
            TBox.Text = newMatrix.GetT().ToString();
            PBox.Text = newMatrix.GetRo().ToString();

            CreateNewTable();

            dataGridHSysT.DataSource = SysMatrix.MatrixToDataTable(newMatrix.GetHSysTmatrix());

            foreach (DataGridViewColumn column in dataGridHSysT.Columns)
            {
                column.Width = 30;
            }

            dataGridErrorInfi.DataSource = SysMatrix.MatrixToDataTable(newMatrix.GetErrorTable());
        }

       
    }
}
