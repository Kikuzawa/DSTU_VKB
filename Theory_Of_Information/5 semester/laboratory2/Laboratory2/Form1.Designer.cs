using System;

namespace Laboratory2
{
    partial class Form1
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.ButtonLoadFile = new System.Windows.Forms.Button();
            this.loadTextBox = new System.Windows.Forms.TextBox();
            this.openFileDialog = new System.Windows.Forms.OpenFileDialog();
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPageHaffman = new System.Windows.Forms.TabPage();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.textBoxOutput = new System.Windows.Forms.RichTextBox();
            this.ButtonSelectFolderHaffDecode1 = new System.Windows.Forms.Button();
            this.ButtonHaffDecode = new System.Windows.Forms.Button();
            this.saveTextBoxHaffDecode = new System.Windows.Forms.TextBox();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.dataGridViewEncodedChars = new System.Windows.Forms.DataGridView();
            this.Character = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.Binary = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.listBoxNodeList = new System.Windows.Forms.ListBox();
            this.ButtonSelectFolderHaffCode = new System.Windows.Forms.Button();
            this.ButtonHaffCode = new System.Windows.Forms.Button();
            this.saveTextBoxHaffCode = new System.Windows.Forms.TextBox();
            this.tabPageLZ77 = new System.Windows.Forms.TabPage();
            this.EncodedText = new System.Windows.Forms.RichTextBox();
            this.TextAfterDecoding = new System.Windows.Forms.TextBox();
            this.TextForEncoding = new System.Windows.Forms.TextBox();
            this.CompressionRatio = new System.Windows.Forms.TextBox();
            this.ClearAllClicButton = new System.Windows.Forms.Button();
            this.groupBox5 = new System.Windows.Forms.GroupBox();
            this.DecodeClicButton = new System.Windows.Forms.Button();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.ExtendedEncodeClicButton = new System.Windows.Forms.Button();
            this.EncodeFromFileClicButton = new System.Windows.Forms.Button();
            this.EncodeClicButton = new System.Windows.Forms.Button();
            this.tabPageLZ78 = new System.Windows.Forms.TabPage();
            this.ButtonRunLZ78 = new System.Windows.Forms.Button();
            this.dataGridLZ78 = new System.Windows.Forms.DataGridView();
            this.SaveFileLZ78 = new System.Windows.Forms.Button();
            this.ButtonSelectFolderLZ78 = new System.Windows.Forms.Button();
            this.saveTextBoxLZ78 = new System.Windows.Forms.TextBox();
            this.tabPageLZW = new System.Windows.Forms.TabPage();
            this.label3 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.button4 = new System.Windows.Forms.Button();
            this.button3 = new System.Windows.Forms.Button();
            this.dataGridViewLZWnew = new System.Windows.Forms.DataGridView();
            this.dataGridView2 = new System.Windows.Forms.DataGridView();
            this.dataGridViewTextBoxColumn3 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewTextBoxColumn4 = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.sChar = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.code = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.dataGridViewLZWold = new System.Windows.Forms.DataGridView();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.screen = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.saveFileDialog = new System.Windows.Forms.SaveFileDialog();
            this.columnChar = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.columnBinary = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.columChar = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.columBinary = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.groupBox1.SuspendLayout();
            this.tabControl1.SuspendLayout();
            this.tabPageHaffman.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.groupBox2.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewEncodedChars)).BeginInit();
            this.tabPageLZ77.SuspendLayout();
            this.groupBox5.SuspendLayout();
            this.groupBox4.SuspendLayout();
            this.tabPageLZ78.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridLZ78)).BeginInit();
            this.tabPageLZW.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewLZWnew)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView2)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewLZWold)).BeginInit();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.ButtonLoadFile);
            this.groupBox1.Controls.Add(this.loadTextBox);
            this.groupBox1.Location = new System.Drawing.Point(13, 13);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(1159, 77);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Загрузка файла";
            // 
            // ButtonLoadFile
            // 
            this.ButtonLoadFile.Location = new System.Drawing.Point(1051, 32);
            this.ButtonLoadFile.Name = "ButtonLoadFile";
            this.ButtonLoadFile.Size = new System.Drawing.Size(92, 23);
            this.ButtonLoadFile.TabIndex = 1;
            this.ButtonLoadFile.Text = "Выбрать файл";
            this.ButtonLoadFile.UseVisualStyleBackColor = true;
            this.ButtonLoadFile.Click += new System.EventHandler(this.ButtonLoadFile_Click);
            // 
            // loadTextBox
            // 
            this.loadTextBox.Location = new System.Drawing.Point(16, 34);
            this.loadTextBox.Name = "loadTextBox";
            this.loadTextBox.ReadOnly = true;
            this.loadTextBox.Size = new System.Drawing.Size(1019, 20);
            this.loadTextBox.TabIndex = 0;
            // 
            // openFileDialog
            // 
            this.openFileDialog.FileName = "openFileDialog";
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPageHaffman);
            this.tabControl1.Controls.Add(this.tabPageLZ77);
            this.tabControl1.Controls.Add(this.tabPageLZ78);
            this.tabControl1.Controls.Add(this.tabPageLZW);
            this.tabControl1.Location = new System.Drawing.Point(13, 113);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(1159, 636);
            this.tabControl1.TabIndex = 1;
            // 
            // tabPageHaffman
            // 
            this.tabPageHaffman.Controls.Add(this.groupBox3);
            this.tabPageHaffman.Controls.Add(this.groupBox2);
            this.tabPageHaffman.Location = new System.Drawing.Point(4, 22);
            this.tabPageHaffman.Name = "tabPageHaffman";
            this.tabPageHaffman.Size = new System.Drawing.Size(1151, 610);
            this.tabPageHaffman.TabIndex = 0;
            this.tabPageHaffman.Text = "Хаффман";
            this.tabPageHaffman.UseVisualStyleBackColor = true;
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.textBoxOutput);
            this.groupBox3.Controls.Add(this.ButtonSelectFolderHaffDecode1);
            this.groupBox3.Controls.Add(this.ButtonHaffDecode);
            this.groupBox3.Controls.Add(this.saveTextBoxHaffDecode);
            this.groupBox3.Location = new System.Drawing.Point(585, 12);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(554, 582);
            this.groupBox3.TabIndex = 0;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Декодирование";
            // 
            // textBoxOutput
            // 
            this.textBoxOutput.Location = new System.Drawing.Point(7, 71);
            this.textBoxOutput.Margin = new System.Windows.Forms.Padding(2);
            this.textBoxOutput.Name = "textBoxOutput";
            this.textBoxOutput.Size = new System.Drawing.Size(541, 498);
            this.textBoxOutput.TabIndex = 11;
            this.textBoxOutput.Text = "";
            this.textBoxOutput.TextChanged += new System.EventHandler(this.textBoxOutput_TextChanged);
            // 
            // ButtonSelectFolderHaffDecode1
            // 
            this.ButtonSelectFolderHaffDecode1.Location = new System.Drawing.Point(378, 33);
            this.ButtonSelectFolderHaffDecode1.Name = "ButtonSelectFolderHaffDecode1";
            this.ButtonSelectFolderHaffDecode1.Size = new System.Drawing.Size(75, 23);
            this.ButtonSelectFolderHaffDecode1.TabIndex = 1;
            this.ButtonSelectFolderHaffDecode1.Text = "Обзор";
            this.ButtonSelectFolderHaffDecode1.UseVisualStyleBackColor = true;
            this.ButtonSelectFolderHaffDecode1.Click += new System.EventHandler(this.ButtonSelectFolderHaff_Click1);
            // 
            // ButtonHaffDecode
            // 
            this.ButtonHaffDecode.Location = new System.Drawing.Point(459, 33);
            this.ButtonHaffDecode.Name = "ButtonHaffDecode";
            this.ButtonHaffDecode.Size = new System.Drawing.Size(89, 23);
            this.ButtonHaffDecode.TabIndex = 1;
            this.ButtonHaffDecode.Text = "Декодировать";
            this.ButtonHaffDecode.UseVisualStyleBackColor = true;
            this.ButtonHaffDecode.Click += new System.EventHandler(this.ButtonHaffDecode_Click);
            // 
            // saveTextBoxHaffDecode
            // 
            this.saveTextBoxHaffDecode.Location = new System.Drawing.Point(7, 36);
            this.saveTextBoxHaffDecode.Name = "saveTextBoxHaffDecode";
            this.saveTextBoxHaffDecode.ReadOnly = true;
            this.saveTextBoxHaffDecode.Size = new System.Drawing.Size(365, 20);
            this.saveTextBoxHaffDecode.TabIndex = 0;
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.dataGridViewEncodedChars);
            this.groupBox2.Controls.Add(this.listBoxNodeList);
            this.groupBox2.Controls.Add(this.ButtonSelectFolderHaffCode);
            this.groupBox2.Controls.Add(this.ButtonHaffCode);
            this.groupBox2.Controls.Add(this.saveTextBoxHaffCode);
            this.groupBox2.Location = new System.Drawing.Point(12, 12);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(554, 582);
            this.groupBox2.TabIndex = 0;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Кодирование";
            // 
            // dataGridViewEncodedChars
            // 
            this.dataGridViewEncodedChars.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewEncodedChars.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.Character,
            this.Binary});
            this.dataGridViewEncodedChars.Location = new System.Drawing.Point(271, 71);
            this.dataGridViewEncodedChars.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridViewEncodedChars.Name = "dataGridViewEncodedChars";
            this.dataGridViewEncodedChars.RowTemplate.Height = 24;
            this.dataGridViewEncodedChars.Size = new System.Drawing.Size(277, 498);
            this.dataGridViewEncodedChars.TabIndex = 6;
            // 
            // Character
            // 
            this.Character.HeaderText = "Char";
            this.Character.Name = "Character";
            this.Character.Width = 50;
            // 
            // Binary
            // 
            this.Binary.HeaderText = "Binary";
            this.Binary.Name = "Binary";
            this.Binary.Width = 300;
            // 
            // listBoxNodeList
            // 
            this.listBoxNodeList.FormattingEnabled = true;
            this.listBoxNodeList.Location = new System.Drawing.Point(7, 71);
            this.listBoxNodeList.Margin = new System.Windows.Forms.Padding(2);
            this.listBoxNodeList.Name = "listBoxNodeList";
            this.listBoxNodeList.Size = new System.Drawing.Size(253, 498);
            this.listBoxNodeList.TabIndex = 4;
            // 
            // ButtonSelectFolderHaffCode
            // 
            this.ButtonSelectFolderHaffCode.Location = new System.Drawing.Point(378, 33);
            this.ButtonSelectFolderHaffCode.Name = "ButtonSelectFolderHaffCode";
            this.ButtonSelectFolderHaffCode.Size = new System.Drawing.Size(75, 23);
            this.ButtonSelectFolderHaffCode.TabIndex = 1;
            this.ButtonSelectFolderHaffCode.Text = "Обзор";
            this.ButtonSelectFolderHaffCode.UseVisualStyleBackColor = true;
            this.ButtonSelectFolderHaffCode.Click += new System.EventHandler(this.ButtonSelectFolderHaff_Click);
            // 
            // ButtonHaffCode
            // 
            this.ButtonHaffCode.Location = new System.Drawing.Point(459, 33);
            this.ButtonHaffCode.Name = "ButtonHaffCode";
            this.ButtonHaffCode.Size = new System.Drawing.Size(89, 23);
            this.ButtonHaffCode.TabIndex = 1;
            this.ButtonHaffCode.Text = "Закодировать";
            this.ButtonHaffCode.UseVisualStyleBackColor = true;
            this.ButtonHaffCode.Click += new System.EventHandler(this.ButtonHaffCode_Click);
            // 
            // saveTextBoxHaffCode
            // 
            this.saveTextBoxHaffCode.Location = new System.Drawing.Point(7, 36);
            this.saveTextBoxHaffCode.Name = "saveTextBoxHaffCode";
            this.saveTextBoxHaffCode.ReadOnly = true;
            this.saveTextBoxHaffCode.Size = new System.Drawing.Size(365, 20);
            this.saveTextBoxHaffCode.TabIndex = 0;
            // 
            // tabPageLZ77
            // 
            this.tabPageLZ77.Controls.Add(this.EncodedText);
            this.tabPageLZ77.Controls.Add(this.TextAfterDecoding);
            this.tabPageLZ77.Controls.Add(this.TextForEncoding);
            this.tabPageLZ77.Controls.Add(this.CompressionRatio);
            this.tabPageLZ77.Controls.Add(this.ClearAllClicButton);
            this.tabPageLZ77.Controls.Add(this.groupBox5);
            this.tabPageLZ77.Controls.Add(this.groupBox4);
            this.tabPageLZ77.Location = new System.Drawing.Point(4, 22);
            this.tabPageLZ77.Name = "tabPageLZ77";
            this.tabPageLZ77.Size = new System.Drawing.Size(1151, 610);
            this.tabPageLZ77.TabIndex = 1;
            this.tabPageLZ77.Text = "LZ77";
            this.tabPageLZ77.UseVisualStyleBackColor = true;
            // 
            // EncodedText
            // 
            this.EncodedText.Location = new System.Drawing.Point(364, 141);
            this.EncodedText.Name = "EncodedText";
            this.EncodedText.Size = new System.Drawing.Size(428, 415);
            this.EncodedText.TabIndex = 7;
            this.EncodedText.Text = "";
            // 
            // TextAfterDecoding
            // 
            this.TextAfterDecoding.Location = new System.Drawing.Point(798, 141);
            this.TextAfterDecoding.Multiline = true;
            this.TextAfterDecoding.Name = "TextAfterDecoding";
            this.TextAfterDecoding.Size = new System.Drawing.Size(331, 415);
            this.TextAfterDecoding.TabIndex = 5;
            // 
            // TextForEncoding
            // 
            this.TextForEncoding.Location = new System.Drawing.Point(12, 141);
            this.TextForEncoding.Multiline = true;
            this.TextForEncoding.Name = "TextForEncoding";
            this.TextForEncoding.Size = new System.Drawing.Size(345, 415);
            this.TextForEncoding.TabIndex = 4;
            // 
            // CompressionRatio
            // 
            this.CompressionRatio.Location = new System.Drawing.Point(976, 44);
            this.CompressionRatio.Multiline = true;
            this.CompressionRatio.Name = "CompressionRatio";
            this.CompressionRatio.Size = new System.Drawing.Size(130, 43);
            this.CompressionRatio.TabIndex = 3;
            // 
            // ClearAllClicButton
            // 
            this.ClearAllClicButton.Location = new System.Drawing.Point(626, 44);
            this.ClearAllClicButton.Name = "ClearAllClicButton";
            this.ClearAllClicButton.Size = new System.Drawing.Size(105, 43);
            this.ClearAllClicButton.TabIndex = 2;
            this.ClearAllClicButton.Text = "Очистить";
            this.ClearAllClicButton.UseVisualStyleBackColor = true;
            this.ClearAllClicButton.Click += new System.EventHandler(this.ClearAllClicButton_Click);
            // 
            // groupBox5
            // 
            this.groupBox5.Controls.Add(this.DecodeClicButton);
            this.groupBox5.Location = new System.Drawing.Point(437, 14);
            this.groupBox5.Name = "groupBox5";
            this.groupBox5.Size = new System.Drawing.Size(170, 100);
            this.groupBox5.TabIndex = 1;
            this.groupBox5.TabStop = false;
            this.groupBox5.Text = "Декодирование";
            // 
            // DecodeClicButton
            // 
            this.DecodeClicButton.Location = new System.Drawing.Point(31, 30);
            this.DecodeClicButton.Name = "DecodeClicButton";
            this.DecodeClicButton.Size = new System.Drawing.Size(112, 43);
            this.DecodeClicButton.TabIndex = 0;
            this.DecodeClicButton.Text = "Декодировать";
            this.DecodeClicButton.UseVisualStyleBackColor = true;
            this.DecodeClicButton.Click += new System.EventHandler(this.DecodeClicButton_Click);
            // 
            // groupBox4
            // 
            this.groupBox4.Controls.Add(this.ExtendedEncodeClicButton);
            this.groupBox4.Controls.Add(this.EncodeFromFileClicButton);
            this.groupBox4.Controls.Add(this.EncodeClicButton);
            this.groupBox4.Location = new System.Drawing.Point(12, 14);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(405, 100);
            this.groupBox4.TabIndex = 0;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "Кодирование";
            // 
            // ExtendedEncodeClicButton
            // 
            this.ExtendedEncodeClicButton.Location = new System.Drawing.Point(274, 30);
            this.ExtendedEncodeClicButton.Name = "ExtendedEncodeClicButton";
            this.ExtendedEncodeClicButton.Size = new System.Drawing.Size(110, 43);
            this.ExtendedEncodeClicButton.TabIndex = 2;
            this.ExtendedEncodeClicButton.Text = "Подробное декодирование";
            this.ExtendedEncodeClicButton.UseVisualStyleBackColor = true;
            this.ExtendedEncodeClicButton.Click += new System.EventHandler(this.ExtendedEncodeClicButton_Click);
            // 
            // EncodeFromFileClicButton
            // 
            this.EncodeFromFileClicButton.Location = new System.Drawing.Point(144, 30);
            this.EncodeFromFileClicButton.Name = "EncodeFromFileClicButton";
            this.EncodeFromFileClicButton.Size = new System.Drawing.Size(113, 43);
            this.EncodeFromFileClicButton.TabIndex = 1;
            this.EncodeFromFileClicButton.Text = "Закодировать из файла";
            this.EncodeFromFileClicButton.UseVisualStyleBackColor = true;
            this.EncodeFromFileClicButton.Click += new System.EventHandler(this.button2_Click);
            // 
            // EncodeClicButton
            // 
            this.EncodeClicButton.Location = new System.Drawing.Point(16, 30);
            this.EncodeClicButton.Name = "EncodeClicButton";
            this.EncodeClicButton.Size = new System.Drawing.Size(110, 43);
            this.EncodeClicButton.TabIndex = 0;
            this.EncodeClicButton.Text = "Закодировать";
            this.EncodeClicButton.UseVisualStyleBackColor = true;
            this.EncodeClicButton.Click += new System.EventHandler(this.EncodeClicButton_Click);
            // 
            // tabPageLZ78
            // 
            this.tabPageLZ78.Controls.Add(this.ButtonRunLZ78);
            this.tabPageLZ78.Controls.Add(this.dataGridLZ78);
            this.tabPageLZ78.Controls.Add(this.SaveFileLZ78);
            this.tabPageLZ78.Controls.Add(this.ButtonSelectFolderLZ78);
            this.tabPageLZ78.Controls.Add(this.saveTextBoxLZ78);
            this.tabPageLZ78.Location = new System.Drawing.Point(4, 22);
            this.tabPageLZ78.Name = "tabPageLZ78";
            this.tabPageLZ78.Size = new System.Drawing.Size(1151, 610);
            this.tabPageLZ78.TabIndex = 2;
            this.tabPageLZ78.Text = "LZ78";
            this.tabPageLZ78.UseVisualStyleBackColor = true;
            // 
            // ButtonRunLZ78
            // 
            this.ButtonRunLZ78.Location = new System.Drawing.Point(12, 536);
            this.ButtonRunLZ78.Name = "ButtonRunLZ78";
            this.ButtonRunLZ78.Size = new System.Drawing.Size(102, 23);
            this.ButtonRunLZ78.TabIndex = 9;
            this.ButtonRunLZ78.Text = "Кодирование";
            this.ButtonRunLZ78.UseVisualStyleBackColor = true;
            // 
            // dataGridLZ78
            // 
            this.dataGridLZ78.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridLZ78.Location = new System.Drawing.Point(12, 11);
            this.dataGridLZ78.Name = "dataGridLZ78";
            this.dataGridLZ78.Size = new System.Drawing.Size(1126, 517);
            this.dataGridLZ78.TabIndex = 8;
            // 
            // SaveFileLZ78
            // 
            this.SaveFileLZ78.Location = new System.Drawing.Point(1063, 534);
            this.SaveFileLZ78.Name = "SaveFileLZ78";
            this.SaveFileLZ78.Size = new System.Drawing.Size(75, 23);
            this.SaveFileLZ78.TabIndex = 7;
            this.SaveFileLZ78.Text = "Сохранить";
            this.SaveFileLZ78.UseVisualStyleBackColor = true;
            // 
            // ButtonSelectFolderLZ78
            // 
            this.ButtonSelectFolderLZ78.Location = new System.Drawing.Point(982, 534);
            this.ButtonSelectFolderLZ78.Name = "ButtonSelectFolderLZ78";
            this.ButtonSelectFolderLZ78.Size = new System.Drawing.Size(75, 23);
            this.ButtonSelectFolderLZ78.TabIndex = 6;
            this.ButtonSelectFolderLZ78.Text = "Обзор";
            this.ButtonSelectFolderLZ78.UseVisualStyleBackColor = true;
            // 
            // saveTextBoxLZ78
            // 
            this.saveTextBoxLZ78.Location = new System.Drawing.Point(120, 536);
            this.saveTextBoxLZ78.Name = "saveTextBoxLZ78";
            this.saveTextBoxLZ78.ReadOnly = true;
            this.saveTextBoxLZ78.Size = new System.Drawing.Size(846, 20);
            this.saveTextBoxLZ78.TabIndex = 5;
            // 
            // tabPageLZW
            // 
            this.tabPageLZW.Controls.Add(this.label3);
            this.tabPageLZW.Controls.Add(this.label2);
            this.tabPageLZW.Controls.Add(this.label1);
            this.tabPageLZW.Controls.Add(this.button4);
            this.tabPageLZW.Controls.Add(this.button3);
            this.tabPageLZW.Controls.Add(this.dataGridViewLZWnew);
            this.tabPageLZW.Controls.Add(this.dataGridView2);
            this.tabPageLZW.Controls.Add(this.dataGridViewLZWold);
            this.tabPageLZW.Controls.Add(this.textBox1);
            this.tabPageLZW.Controls.Add(this.screen);
            this.tabPageLZW.Controls.Add(this.button1);
            this.tabPageLZW.Location = new System.Drawing.Point(4, 22);
            this.tabPageLZW.Name = "tabPageLZW";
            this.tabPageLZW.Size = new System.Drawing.Size(1151, 610);
            this.tabPageLZW.TabIndex = 3;
            this.tabPageLZW.Text = "LZW";
            this.tabPageLZW.UseVisualStyleBackColor = true;
            this.tabPageLZW.Click += new System.EventHandler(this.tabPageLZW_Click);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(881, 57);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(94, 13);
            this.label3.TabIndex = 15;
            this.label3.Text = "Таблица пакетов";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(589, 345);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(90, 13);
            this.label2.TabIndex = 14;
            this.label2.Text = "Старый словарь";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(589, 60);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(86, 13);
            this.label1.TabIndex = 13;
            this.label1.Text = "Новый словарь";
            this.label1.Click += new System.EventHandler(this.label1_Click);
            // 
            // button4
            // 
            this.button4.Location = new System.Drawing.Point(416, 21);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(88, 42);
            this.button4.TabIndex = 12;
            this.button4.Text = "Сохр. Таблицу пакетов";
            this.button4.UseVisualStyleBackColor = true;
            this.button4.Click += new System.EventHandler(this.button4_Click);
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(313, 21);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(97, 42);
            this.button3.TabIndex = 11;
            this.button3.Text = "Сохр. Словари";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // dataGridViewLZWnew
            // 
            this.dataGridViewLZWnew.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewLZWnew.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.columnChar,
            this.columnBinary});
            this.dataGridViewLZWnew.Location = new System.Drawing.Point(525, 75);
            this.dataGridViewLZWnew.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridViewLZWnew.Name = "dataGridViewLZWnew";
            this.dataGridViewLZWnew.RowTemplate.Height = 24;
            this.dataGridViewLZWnew.Size = new System.Drawing.Size(214, 262);
            this.dataGridViewLZWnew.TabIndex = 9;
            // 
            // dataGridView2
            // 
            this.dataGridView2.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridView2.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.dataGridViewTextBoxColumn3,
            this.dataGridViewTextBoxColumn4,
            this.sChar,
            this.code});
            this.dataGridView2.Location = new System.Drawing.Point(751, 75);
            this.dataGridView2.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridView2.Name = "dataGridView2";
            this.dataGridView2.RowTemplate.Height = 24;
            this.dataGridView2.Size = new System.Drawing.Size(388, 515);
            this.dataGridView2.TabIndex = 8;
            // 
            // dataGridViewTextBoxColumn3
            // 
            this.dataGridViewTextBoxColumn3.HeaderText = "text";
            this.dataGridViewTextBoxColumn3.Name = "dataGridViewTextBoxColumn3";
            this.dataGridViewTextBoxColumn3.Width = 50;
            // 
            // dataGridViewTextBoxColumn4
            // 
            this.dataGridViewTextBoxColumn4.HeaderText = "fChar";
            this.dataGridViewTextBoxColumn4.Name = "dataGridViewTextBoxColumn4";
            this.dataGridViewTextBoxColumn4.Width = 50;
            // 
            // sChar
            // 
            this.sChar.HeaderText = "sChar";
            this.sChar.Name = "sChar";
            // 
            // code
            // 
            this.code.HeaderText = "code";
            this.code.Name = "code";
            // 
            // dataGridViewLZWold
            // 
            this.dataGridViewLZWold.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridViewLZWold.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.columChar,
            this.columBinary});
            this.dataGridViewLZWold.Location = new System.Drawing.Point(525, 360);
            this.dataGridViewLZWold.Margin = new System.Windows.Forms.Padding(2);
            this.dataGridViewLZWold.Name = "dataGridViewLZWold";
            this.dataGridViewLZWold.RowTemplate.Height = 24;
            this.dataGridViewLZWold.Size = new System.Drawing.Size(214, 230);
            this.dataGridViewLZWold.TabIndex = 7;
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(44, 360);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(460, 230);
            this.textBox1.TabIndex = 2;
            // 
            // screen
            // 
            this.screen.Location = new System.Drawing.Point(44, 75);
            this.screen.Multiline = true;
            this.screen.Name = "screen";
            this.screen.Size = new System.Drawing.Size(460, 262);
            this.screen.TabIndex = 1;
            this.screen.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(44, 31);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(98, 23);
            this.button1.TabIndex = 0;
            this.button1.Text = "Закодировать";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click_1);
            // 
            // columnChar
            // 
            this.columnChar.HeaderText = "Char";
            this.columnChar.Name = "columnChar";
            this.columnChar.Width = 50;
            // 
            // columnBinary
            // 
            this.columnBinary.HeaderText = "Binary";
            this.columnBinary.Name = "columnBinary";
            this.columnBinary.Width = 300;
            // 
            // columChar
            // 
            this.columChar.HeaderText = "Char";
            this.columChar.Name = "columChar";
            this.columChar.Width = 50;
            // 
            // columBinary
            // 
            this.columBinary.HeaderText = "Binary";
            this.columBinary.Name = "columBinary";
            this.columBinary.Width = 300;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1184, 761);
            this.Controls.Add(this.tabControl1);
            this.Controls.Add(this.groupBox1);
            this.Name = "Form1";
            this.Text = "Laboratory 2";
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.tabControl1.ResumeLayout(false);
            this.tabPageHaffman.ResumeLayout(false);
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewEncodedChars)).EndInit();
            this.tabPageLZ77.ResumeLayout(false);
            this.tabPageLZ77.PerformLayout();
            this.groupBox5.ResumeLayout(false);
            this.groupBox4.ResumeLayout(false);
            this.tabPageLZ78.ResumeLayout(false);
            this.tabPageLZ78.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridLZ78)).EndInit();
            this.tabPageLZW.ResumeLayout(false);
            this.tabPageLZW.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewLZWnew)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridView2)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridViewLZWold)).EndInit();
            this.ResumeLayout(false);

        }

        private void tabPageLZW_Click(object sender, EventArgs e)
        {
            throw new NotImplementedException();
        }



        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button ButtonLoadFile;
        private System.Windows.Forms.TextBox loadTextBox;
        private System.Windows.Forms.OpenFileDialog openFileDialog;
        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPageHaffman;
        private System.Windows.Forms.TabPage tabPageLZ77;
        private System.Windows.Forms.TabPage tabPageLZ78;
        private System.Windows.Forms.TabPage tabPageLZW;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Button ButtonHaffCode;
        private System.Windows.Forms.Button ButtonHaffDecode;
        private System.Windows.Forms.SaveFileDialog saveFileDialog;
        private System.Windows.Forms.Button ButtonRunLZ78;
        private System.Windows.Forms.DataGridView dataGridLZ78;
        private System.Windows.Forms.Button SaveFileLZ78;
        private System.Windows.Forms.Button ButtonSelectFolderLZ78;
        private System.Windows.Forms.TextBox saveTextBoxLZ78;
        private System.Windows.Forms.Button ButtonSelectFolderHaffCode;
        private System.Windows.Forms.TextBox saveTextBoxHaffCode;
        private System.Windows.Forms.Button ButtonSelectFolderHaffDecode1;
        private System.Windows.Forms.TextBox saveTextBoxHaffDecode;
        private System.Windows.Forms.ListBox listBoxNodeList;
        private System.Windows.Forms.DataGridView dataGridViewEncodedChars;
        private System.Windows.Forms.DataGridViewTextBoxColumn Character;
        private System.Windows.Forms.DataGridViewTextBoxColumn Binary;
        private System.Windows.Forms.RichTextBox textBoxOutput;
        private System.Windows.Forms.GroupBox groupBox5;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.Button EncodeFromFileClicButton;
        private System.Windows.Forms.Button EncodeClicButton;
        private System.Windows.Forms.TextBox TextAfterDecoding;
        private System.Windows.Forms.TextBox TextForEncoding;
        private System.Windows.Forms.TextBox CompressionRatio;
        private System.Windows.Forms.Button ClearAllClicButton;
        private System.Windows.Forms.Button DecodeClicButton;
        private System.Windows.Forms.Button ExtendedEncodeClicButton;
        private System.Windows.Forms.RichTextBox EncodedText;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.TextBox screen;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.DataGridView dataGridViewLZWold;
        private System.Windows.Forms.DataGridView dataGridView2;
        private System.Windows.Forms.DataGridViewTextBoxColumn dataGridViewTextBoxColumn3;
        private System.Windows.Forms.DataGridViewTextBoxColumn dataGridViewTextBoxColumn4;
        private System.Windows.Forms.DataGridViewTextBoxColumn sChar;
        private System.Windows.Forms.DataGridViewTextBoxColumn code;
        private System.Windows.Forms.DataGridView dataGridViewLZWnew;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button button4;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.DataGridViewTextBoxColumn columnChar;
        private System.Windows.Forms.DataGridViewTextBoxColumn columnBinary;
        private System.Windows.Forms.DataGridViewTextBoxColumn columChar;
        private System.Windows.Forms.DataGridViewTextBoxColumn columBinary;
    }
}

