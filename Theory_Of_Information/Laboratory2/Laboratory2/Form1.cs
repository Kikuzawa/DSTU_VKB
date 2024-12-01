using NPOI.SS.Formula.Functions;
using NPOI.XSSF.Streaming.Values;
using Org.BouncyCastle.Utilities;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows.Forms;
using static NPOI.HSSF.Util.HSSFColor;
using static System.Net.Mime.MediaTypeNames;

namespace Laboratory2
{



    public partial class Form1 : Form
    {
        FileInfo FilePath;
        bool ExtendedAlgm = false;
        string text = "";
        List<int> ArrComp = new List<int>(); // for copmressed data 
        Dictionary<int, string> MapDic = new Dictionary<int, string>(); // dictionary
        Dictionary<int, string> MyDic = new Dictionary<int, string>(); // dictionary






        public Form1()
        {
            InitializeComponent();
            
        }

        private void ButtonLoadFile_Click(object sender, EventArgs e)
        {
            var FD = new OpenFileDialog();
            if (FD.ShowDialog() == DialogResult.OK)
            {
                FilePath = new FileInfo(FD.FileName);
            }
            loadTextBox.Text = FilePath.FullName;

        }

        //
        // =============================
        // Тут Блок по алгоритму Huffman
        // =============================
        //

        Queue<HuffmanNode> queueTempNodes = new Queue<HuffmanNode>();

        List<HuffmanNode> listTempOrderedNodes = new List<HuffmanNode>();

        List<HuffmanNode> listFixedNodes = new List<HuffmanNode>();

        List<EncodedChar> listBinary = new List<EncodedChar>();



        private void ButtonSelectFolderHaff_Click1(object sender, EventArgs e)
        {
            OpenFileDialog fileNameDialog = new OpenFileDialog();


            fileNameDialog.Filter = "TXT файл (*.txt)|*.txt";
            fileNameDialog.Title = "Введите имя файла";
            fileNameDialog.CheckFileExists = false;

            fileNameDialog.DefaultExt = ".txt";
            fileNameDialog.FileName = "outputTXT.txt";
            fileNameDialog.AddExtension = true;
            string filePath = "C:\\decode.txt";
            if (fileNameDialog.ShowDialog() == DialogResult.OK)
            {
                filePath = Path.Combine(fileNameDialog.FileName);

            }

            saveTextBoxHaffDecode.Text = filePath;

        }
        private void ButtonSelectFolderHaff_Click(object sender, EventArgs e)
        {
            OpenFileDialog fileNameDialog = new OpenFileDialog();
            fileNameDialog.Filter = "HS файл (*.hs)|*.hs";
            fileNameDialog.Title = "Введите имя файла";
            fileNameDialog.CheckFileExists = false;

            fileNameDialog.DefaultExt = ".hs";
            fileNameDialog.FileName = "outputHS.hs";
            fileNameDialog.AddExtension = true;
            string filePath = "C:\\code.hs";
            if (fileNameDialog.ShowDialog() == DialogResult.OK)
            {
                filePath = Path.Combine(fileNameDialog.FileName);

            }

            saveTextBoxHaffCode.Text = filePath;
        }

        private void ButtonHaffCode_Click(object sender, EventArgs e)
        {
            Huffman_tree_and_log();
        }

        private void Huffman_tree_and_log()
        {
            string inputText;
            using (StreamReader reader = new StreamReader(loadTextBox.Text))
            {
                inputText = reader.ReadToEnd();
            }

            listTempOrderedNodes.Clear();
            queueTempNodes.Clear();
            listFixedNodes.Clear();
            listBinary.Clear();
            listBoxNodeList.Items.Clear();

            string input = inputText;
            while (input != "")
            {
                string txt = input.Substring(0, 1);
                input = input.Remove(0, 1);

                if (listTempOrderedNodes.Count > 0)
                {
                    bool valid = false;
                    for (int i = 0; i < listTempOrderedNodes.Count; i++)
                    {
                        if (listTempOrderedNodes[i].NodeString == txt)
                        {
                            listTempOrderedNodes[i].Frequency += 1;
                            valid = true;
                            break;
                        }
                    }
                    if (!valid) NewNode(txt);
                }
                else NewNode(txt);
            }

            RefreshOrder();


            while (queueTempNodes.Count > 1)
            {
                HuffmanNode leftNode = queueTempNodes.Dequeue();
                HuffmanNode rightNode = queueTempNodes.Dequeue();
                HuffmanNode newParent = new HuffmanNode();
                newParent.NodeString = leftNode.NodeString + rightNode.NodeString;
                newParent.Frequency = leftNode.Frequency + rightNode.Frequency;
                newParent.Left = leftNode;
                newParent.Right = rightNode;
                queueTempNodes.Enqueue(newParent);
                listFixedNodes.Add(newParent);
                RefreshOrder();
            }

            dataGridViewEncodedChars.Rows.Clear();

            for (int i = 0; i < listFixedNodes.Count; i++)
            {
                listBoxNodeList.Items.Add("Node\t\t: " + listFixedNodes[i].NodeString);
                listBoxNodeList.Items.Add("Frequency\t: " + listFixedNodes[i].Frequency);

                if (listFixedNodes[i].Left != null) listBoxNodeList.Items.Add("Left\t\t: " + listFixedNodes[i].Left.NodeString);
                else listBoxNodeList.Items.Add("Left\t\t: " + "Null");
                if (listFixedNodes[i].Right != null) listBoxNodeList.Items.Add("Right\t\t: " + listFixedNodes[i].Right.NodeString);
                else listBoxNodeList.Items.Add("Right\t\t: " + "Null");

                listBoxNodeList.Items.Add("");

                if (listFixedNodes[i].NodeString.Length == 1)
                {
                    EncodedChar en = new EncodedChar();
                    en.Character = listFixedNodes[i].NodeString;
                    en.Binary = AnalyzeBinary(en.Character, listFixedNodes[listFixedNodes.Count - 1]);
                    listBinary.Add(en);
                    dataGridViewEncodedChars.Rows.Add(en.Character, en.Binary);
                }
            }

            input = inputText;
            string output = "";
            while (input != "")
            {
                string txt = input.Substring(0, 1);
                input = input.Remove(0, 1);
                for (int i = 0; i < listBinary.Count; i++)
                {
                    if (listBinary[i].Character == txt) output = output + listBinary[i].Binary;
                }
            }

            textBoxOutput.Text = output;

            using (StreamWriter writer = new StreamWriter(saveTextBoxHaffCode.Text, false))
            {
                writer.Write(output);
            }




        }

        private void ButtonHaffDecode_Click(object sender, EventArgs e)
        {
            string fileName = saveTextBoxHaffDecode.Text;

            if (!fileName.Equals(""))
            {
                DecodeMethod();
            }
            else
            {
                MessageBox.Show("Ошибка, выберите файл для сохранения");
            }


        }




        private void dataGridHaffDecode_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void dataGridHaffCode_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }



        public void RefreshOrder()
        {
            int value = 1;
            if (queueTempNodes.Count > 0)
            {
                listTempOrderedNodes.Clear();
                while (queueTempNodes.Count != 0) listTempOrderedNodes.Add(queueTempNodes.Dequeue());
            }
            while (queueTempNodes.Count < listTempOrderedNodes.Count)
            {
                for (int i = 0; i < listTempOrderedNodes.Count; i++)
                {
                    if (listTempOrderedNodes[i].Frequency == value) queueTempNodes.Enqueue(listTempOrderedNodes[i]);
                }
                value++;
            }
        }

        public void NewNode(string p)
        {
            HuffmanNode node = new HuffmanNode();
            node.NodeString = p;
            node.Frequency = 1;
            node.Left = null;
            node.Right = null;
            listFixedNodes.Add(node);
            listTempOrderedNodes.Add(node);
        }

        public string AnalyzeBinary(string txt, HuffmanNode parent)
        {
            HuffmanNode helper = parent;
            string returnValue = "";
            bool valid = true;
            while ((helper.Left != null || helper.Right != null) && valid)
            {
                if (helper.Left.NodeString.Contains(txt))
                {
                    helper = helper.Left; valid = true; returnValue = returnValue + "0";
                }
                else if (helper.Right.NodeString.Contains(txt))
                {
                    helper = helper.Right; valid = true; returnValue = returnValue + "1";
                }
                else valid = false;
            }
            if (valid) return returnValue;
            else return "error";
        }

        public void DecodeMethod()
        {
            if (listFixedNodes.Count > 0)
            {
                string input;
                using (StreamReader reader = new StreamReader(loadTextBox.Text))
                {
                    input = reader.ReadToEnd();
                }

                string output = "";
                HuffmanNode root = new HuffmanNode();
                for (int i = 0; i < listFixedNodes.Count; i++)
                {
                    if (root.NodeString.Length < listFixedNodes[i].NodeString.Length) root = listFixedNodes[i];
                }
                int repetition = input.Length;
                bool finished = false;
                HuffmanNode helper = new HuffmanNode();
                helper = root;
                for (int j = 0; j < repetition; j++)
                {
                    finished = false;
                    string biner = "";
                    if (input != "") biner = input.Substring(0, 1);
                    if (biner == "0" && helper.Left != null)
                    {
                        helper = helper.Left;
                        input = input.Remove(0, 1);
                    }
                    else if (biner == "1" && helper.Right != null)
                    {
                        helper = helper.Right;
                        input = input.Remove(0, 1);
                    }
                    if (helper.Left == null && helper.Right == null)
                    {
                        output = output + helper.NodeString;
                        helper = root;
                        finished = true;
                    }
                }
                if (finished)
                {
                    textBoxOutput.Text = output;
                    using (StreamWriter writer = new StreamWriter(saveTextBoxHaffDecode.Text, false))
                    {
                        writer.Write(output);
                    }
                }
                else
                {
                    textBoxOutput.Text = "Unknown binary sequence detected. Make sure you've inputed the correct binary sequence according to the tree."
                        + "\n\n" + "Please note that binary numbers consists only number 0 and or 1";
                }
            }
            else
            {
                textBoxOutput.Text = "Please encode something to make the HuffmanTree for decoding process...";
            }
        }

        private void textBoxOutput_TextChanged(object sender, EventArgs e)
        {

        }
        //
        // =============================
        // Тут Блок по алгоритму LZ77
        // =============================
        //

        private void button1_Click(object sender, EventArgs e)
        {

        }

        private void button2_Click(object sender, EventArgs e)
        {
            String inputText;
            ExtendedAlgm = false;
            using (StreamReader reader = new StreamReader(loadTextBox.Text))
            {
                inputText = reader.ReadToEnd();
            }

            TextAfterDecoding.Text = string.Empty;
            var Lz = LZ77Algm.Encode(inputText, ExtendedAlgm);
            EncodedText.Text = Lz.ToString();
            CompressionRatio.Text = Lz.GetCompressionRatio().ToString();

            ExtendedAlgm = false;

        }

        private void EncodeClicButton_Click(object sender, EventArgs e)
        {
            TextAfterDecoding.Text = string.Empty;
            var Lz = LZ77Algm.Encode(TextForEncoding.Text, ExtendedAlgm);
            EncodedText.Text = Lz.ToString();
            CompressionRatio.Text = Lz.GetCompressionRatio().ToString();
            
            
        }

        private void ExtendedEncodeClicButton_Click(object sender, EventArgs e)
        {
            ExtendedAlgm = true;
            EncodeClicButton_Click(sender, e);
            ExtendedAlgm = false;
        }

        private void DecodeClicButton_Click(object sender, EventArgs e)
        {
            try
            {
                var Lz = LZ77Algm.Decode(EncodedText.Text);
                TextAfterDecoding.Text = Lz.GetAnswer();
            } catch (Exception ex) {
            
                TextAfterDecoding.Text = "Ошибка: " + ex;
            }
        }

        private void ClearAllClicButton_Click(object sender, EventArgs e)
        {
            TextAfterDecoding.Text = null;
            TextForEncoding.Text = null;
            CompressionRatio.Text = null;
            EncodedText.Text = null;

            //byte byteValue = 9;
            //byte[] bytes = BitConverter.GetBytes(byteValue);
            //string bitString = string.Join("", bytes.Select(b => Convert.ToString(b, 2).PadLeft(8, '0')));
            //EncodedText.Text += bitString;



        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            try
            {
                using (StreamReader reader = new StreamReader(loadTextBox.Text))
                {
                    text = reader.ReadToEnd();
                }

                screen.Text = text;
            }
             catch
            {
                MessageBox.Show("Выберите файл!");
            }

            dataGridView2.Rows.Clear();
            dataGridViewLZWold.Rows.Clear();
            dataGridViewLZWnew.Rows.Clear();





            string curChar = ""; // current char
            int sizeDic = 128, check = 0, newDicIndex = 0;
            int checkBreak = 0;

            



            for (int indxTxt = 0; indxTxt < text.Length; indxTxt++)
            {
                curChar += text[indxTxt];
                


                while (curChar.Length > 1 /* at least 2 char */|| indxTxt + 1 == text.Length /*last char */)
                {

                    for (int indexDic = 128; indexDic <= sizeDic; indexDic++)
                    {
                        string compChar = "";
                        if (MapDic.Count != 0 && indexDic != sizeDic)

                            compChar = MapDic[indexDic]; // get data from dictionary to compare 

                        if (MapDic.Count == 0) // dictionary is empty


                            check = 1;

                        else

                            if (compChar == curChar)
                        {
                            indxTxt++;

                            if (indxTxt + 1 < text.Length)

                                curChar += text[indxTxt]; // take the nxt char to save it in dictionary
                            else
                                curChar += " "; // the end of text

                            check = 0;
                            newDicIndex = indexDic;

                        }
                        else if (compChar != curChar) // current char is not in dictionary
                            check = 1;


                    }
                    if (check == 1)
                    {
                        
                        indxTxt--; // back one char
                        if (curChar.Length > 1)
                        {
                            if (curChar[curChar.Length - 1] != ' ')
                            {
                                MapDic.Add(sizeDic, curChar); // add new data
                                
                                
                                sizeDic++;
                            }
                        }

                        else
                        {
                            
                            ArrComp.Add((int)curChar[0]); // take the asscii for one char 

                            checkBreak = 1;
                            break;

                        }
                        if (curChar.Length > 1)
                        {
                            
                                if (curChar.Length == 2)
                            {
                                try
                                {
                                    MyDic.Add((int)text[indxTxt], text[indxTxt].ToString());
                                } catch { }
                                
                                dataGridView2.Rows.Add(curChar, curChar.Substring(0, curChar.Length - 1), curChar[curChar.Length-1], (int)text[indxTxt]);
                                ArrComp.Add((int)text[indxTxt]); // get th value of data0
                            }
                            else
                            {
                                dataGridView2.Rows.Add(curChar, curChar.Substring(0, curChar.Length -1 ), curChar[curChar.Length-1], newDicIndex);
                                ArrComp.Add(newDicIndex);
                            }


                }
                        
                        curChar = "";
                        check = 0;

                    }
                }
                if (checkBreak == 1)
                    break;
                
            }
            // compressing
            for (int indexDic = 0; indexDic < ArrComp.Count; indexDic++) 

                textBox1.Text += ArrComp[indexDic] + " ";

            for (int indexDic = 0; indexDic < MyDic.Count; indexDic++)
            {
                var key = MyDic.Keys.ElementAt(indexDic);
                var value = MyDic[key];

                dataGridViewLZWold.Rows.Add(value, key);
            }

            for (int indexDic = 0; indexDic < MapDic.Count; indexDic++)
            {
                var key = MapDic.Keys.ElementAt(indexDic);
                var value = MapDic[key];

                dataGridViewLZWnew.Rows.Add(value, key);
            }
            





            MapDic.Clear();
            ArrComp.Clear();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }
        private void PrintDictionaryContents(Dictionary<int, string> dict, string title)
        {
            string result = title + Environment.NewLine + string.Join(Environment.NewLine, dict.Select(x => $"{x.Key}: {x.Value}"));
            textBox1.AppendText(result);
            textBox1.AppendText(Environment.NewLine);
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void button3_Click(object sender, EventArgs e)
        {
            ExportDataGridViewToCSV(dataGridViewLZWold, "LZW_old.csv");
            ExportDataGridViewToCSV(dataGridViewLZWnew, "LZW_new.csv");
        }

        private void button4_Click(object sender, EventArgs e)
        {
            ExportDataGridViewToCSV(dataGridView2, "LZW_trace.csv");
        }
        private void ExportDataGridViewToCSV(DataGridView dataGridView, string fileName)
        {
            try
            {

                OpenFileDialog fileNameDialog = new OpenFileDialog();


                fileNameDialog.Filter = "CSV файл (*.csv)|*.csv";
                fileNameDialog.Title = "Введите имя файла";
                fileNameDialog.CheckFileExists = false;

                fileNameDialog.DefaultExt = ".csv";
                fileNameDialog.FileName = fileName;
                fileNameDialog.AddExtension = true;
                string filePath = "";
                if (fileNameDialog.ShowDialog() == DialogResult.OK)
                {
                    filePath = Path.Combine(fileNameDialog.FileName);

                }


                // Получаем заголовки и данные из DataGridView
                var columns = dataGridView.Columns.Cast<DataGridViewColumn>().Select(c => c.Name);
                var rows = dataGridView.Rows.Cast<DataGridViewRow>()
                    .Where(row => row.Cells.Count > 0)
                    .Select(r => r.Cells.Cast<DataGridViewCell>().Select(c => c.Value?.ToString() ?? ""));

                // Создаем файл
              
                using (StreamWriter writer = new StreamWriter(filePath))
                {
                    // Записываем заголовки
                    writer.WriteLine(string.Join(",", columns));

                    // Записываем данные
                    foreach (var row in rows)
                    {
                        writer.WriteLine(string.Join(",", row));
                    }
                }

                MessageBox.Show($"Данные успешно экспортированы в файл {Path.GetFileName(filePath)}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Произошла ошибка при экспорте данных: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

    }



}
