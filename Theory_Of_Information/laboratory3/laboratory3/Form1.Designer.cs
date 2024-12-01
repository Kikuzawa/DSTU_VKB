namespace laboratory3
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
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.testBox = new System.Windows.Forms.TextBox();
            this.testButton = new System.Windows.Forms.Button();
            this.testButton2 = new System.Windows.Forms.Button();
            this.radioButtonH = new System.Windows.Forms.RadioButton();
            this.radioButtonG = new System.Windows.Forms.RadioButton();
            this.textNBox = new System.Windows.Forms.TextBox();
            this.textKBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.dataGridStartMatrix = new System.Windows.Forms.DataGridView();
            this.labelNameStartMatrix = new System.Windows.Forms.Label();
            this.GenerateMatrixButton = new System.Windows.Forms.Button();
            this.dataGridStartSysMatrix = new System.Windows.Forms.DataGridView();
            this.labelNameStartSysMatrix = new System.Windows.Forms.Label();
            this.dataGridEndSysMatrix = new System.Windows.Forms.DataGridView();
            this.labelNameEndSysMatrix = new System.Windows.Forms.Label();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.dataGridErrorInfi = new System.Windows.Forms.DataGridView();
            this.label8 = new System.Windows.Forms.Label();
            this.dataGridHSysT = new System.Windows.Forms.DataGridView();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.button1 = new System.Windows.Forms.Button();
            this.groupBox4 = new System.Windows.Forms.GroupBox();
            this.label7 = new System.Windows.Forms.Label();
            this.PBox = new System.Windows.Forms.TextBox();
            this.label6 = new System.Windows.Forms.Label();
            this.TBox = new System.Windows.Forms.TextBox();
            this.label5 = new System.Windows.Forms.Label();
            this.DMinBox = new System.Windows.Forms.TextBox();
            this.dataGridICW = new System.Windows.Forms.DataGridView();
            this.label4 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.KBox = new System.Windows.Forms.TextBox();
            this.NBox = new System.Windows.Forms.TextBox();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.textBox10 = new System.Windows.Forms.TextBox();
            this.button2 = new System.Windows.Forms.Button();
            this.textBox9 = new System.Windows.Forms.TextBox();
            this.textBox8 = new System.Windows.Forms.TextBox();
            this.textBox7 = new System.Windows.Forms.TextBox();
            this.textBox6 = new System.Windows.Forms.TextBox();
            this.textBox5 = new System.Windows.Forms.TextBox();
            this.textBox4 = new System.Windows.Forms.TextBox();
            this.textBox3 = new System.Windows.Forms.TextBox();
            this.textBox2 = new System.Windows.Forms.TextBox();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridStartMatrix)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridStartSysMatrix)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridEndSysMatrix)).BeginInit();
            this.groupBox1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridErrorInfi)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridHSysT)).BeginInit();
            this.groupBox2.SuspendLayout();
            this.groupBox4.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridICW)).BeginInit();
            this.groupBox3.SuspendLayout();
            this.SuspendLayout();
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(6, 19);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(266, 149);
            this.textBox1.TabIndex = 0;
            this.textBox1.Text = "aabbccdababba";
            // 
            // testBox
            // 
            this.testBox.Location = new System.Drawing.Point(6, 174);
            this.testBox.Multiline = true;
            this.testBox.Name = "testBox";
            this.testBox.Size = new System.Drawing.Size(266, 70);
            this.testBox.TabIndex = 1;
            // 
            // testButton
            // 
            this.testButton.Location = new System.Drawing.Point(83, 575);
            this.testButton.Name = "testButton";
            this.testButton.Size = new System.Drawing.Size(75, 23);
            this.testButton.TabIndex = 2;
            this.testButton.Text = "Код";
            this.testButton.UseVisualStyleBackColor = true;
            this.testButton.Click += new System.EventHandler(this.testButton_Click);
            // 
            // testButton2
            // 
            this.testButton2.Location = new System.Drawing.Point(382, 575);
            this.testButton2.Name = "testButton2";
            this.testButton2.Size = new System.Drawing.Size(75, 23);
            this.testButton2.TabIndex = 3;
            this.testButton2.Text = "Декод";
            this.testButton2.UseVisualStyleBackColor = true;
            this.testButton2.Click += new System.EventHandler(this.testButton2_Click);
            // 
            // radioButtonH
            // 
            this.radioButtonH.AutoSize = true;
            this.radioButtonH.Checked = true;
            this.radioButtonH.Location = new System.Drawing.Point(20, 31);
            this.radioButtonH.Name = "radioButtonH";
            this.radioButtonH.Size = new System.Drawing.Size(33, 17);
            this.radioButtonH.TabIndex = 4;
            this.radioButtonH.TabStop = true;
            this.radioButtonH.Text = "H";
            this.radioButtonH.UseVisualStyleBackColor = true;
            this.radioButtonH.CheckedChanged += new System.EventHandler(this.radioButtonH_CheckedChanged);
            // 
            // radioButtonG
            // 
            this.radioButtonG.AutoSize = true;
            this.radioButtonG.Location = new System.Drawing.Point(113, 31);
            this.radioButtonG.Name = "radioButtonG";
            this.radioButtonG.Size = new System.Drawing.Size(33, 17);
            this.radioButtonG.TabIndex = 5;
            this.radioButtonG.Text = "G";
            this.radioButtonG.UseVisualStyleBackColor = true;
            this.radioButtonG.CheckedChanged += new System.EventHandler(this.radioButtonG_CheckedChanged);
            // 
            // textNBox
            // 
            this.textNBox.Location = new System.Drawing.Point(73, 79);
            this.textNBox.Name = "textNBox";
            this.textNBox.Size = new System.Drawing.Size(100, 20);
            this.textNBox.TabIndex = 6;
            this.textNBox.Text = "7";
            // 
            // textKBox
            // 
            this.textKBox.Location = new System.Drawing.Point(73, 106);
            this.textKBox.Name = "textKBox";
            this.textKBox.Size = new System.Drawing.Size(100, 20);
            this.textKBox.TabIndex = 7;
            this.textKBox.Text = "4";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(17, 109);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(43, 13);
            this.label1.TabIndex = 8;
            this.label1.Text = "Строки";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(17, 80);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(51, 13);
            this.label2.TabIndex = 9;
            this.label2.Text = "Столбцы";
            // 
            // dataGridStartMatrix
            // 
            this.dataGridStartMatrix.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridStartMatrix.Location = new System.Drawing.Point(212, 31);
            this.dataGridStartMatrix.Name = "dataGridStartMatrix";
            this.dataGridStartMatrix.Size = new System.Drawing.Size(253, 133);
            this.dataGridStartMatrix.TabIndex = 5;
            // 
            // labelNameStartMatrix
            // 
            this.labelNameStartMatrix.AutoSize = true;
            this.labelNameStartMatrix.Location = new System.Drawing.Point(179, 93);
            this.labelNameStartMatrix.Name = "labelNameStartMatrix";
            this.labelNameStartMatrix.Size = new System.Drawing.Size(27, 13);
            this.labelNameStartMatrix.TabIndex = 11;
            this.labelNameStartMatrix.Text = "H = ";
            // 
            // GenerateMatrixButton
            // 
            this.GenerateMatrixButton.Location = new System.Drawing.Point(16, 164);
            this.GenerateMatrixButton.Name = "GenerateMatrixButton";
            this.GenerateMatrixButton.Size = new System.Drawing.Size(71, 23);
            this.GenerateMatrixButton.TabIndex = 12;
            this.GenerateMatrixButton.Text = "Создать ";
            this.GenerateMatrixButton.UseVisualStyleBackColor = true;
            this.GenerateMatrixButton.Click += new System.EventHandler(this.GenerateMatrixButton_Click);
            // 
            // dataGridStartSysMatrix
            // 
            this.dataGridStartSysMatrix.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridStartSysMatrix.Location = new System.Drawing.Point(55, 19);
            this.dataGridStartSysMatrix.Name = "dataGridStartSysMatrix";
            this.dataGridStartSysMatrix.Size = new System.Drawing.Size(253, 133);
            this.dataGridStartSysMatrix.TabIndex = 13;
            // 
            // labelNameStartSysMatrix
            // 
            this.labelNameStartSysMatrix.AutoSize = true;
            this.labelNameStartSysMatrix.Location = new System.Drawing.Point(7, 81);
            this.labelNameStartSysMatrix.Name = "labelNameStartSysMatrix";
            this.labelNameStartSysMatrix.Size = new System.Drawing.Size(42, 13);
            this.labelNameStartSysMatrix.TabIndex = 14;
            this.labelNameStartSysMatrix.Text = "Hsys = ";
            // 
            // dataGridEndSysMatrix
            // 
            this.dataGridEndSysMatrix.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridEndSysMatrix.Location = new System.Drawing.Point(55, 173);
            this.dataGridEndSysMatrix.Name = "dataGridEndSysMatrix";
            this.dataGridEndSysMatrix.Size = new System.Drawing.Size(253, 133);
            this.dataGridEndSysMatrix.TabIndex = 16;
            // 
            // labelNameEndSysMatrix
            // 
            this.labelNameEndSysMatrix.AutoSize = true;
            this.labelNameEndSysMatrix.Location = new System.Drawing.Point(7, 237);
            this.labelNameEndSysMatrix.Name = "labelNameEndSysMatrix";
            this.labelNameEndSysMatrix.Size = new System.Drawing.Size(42, 13);
            this.labelNameEndSysMatrix.TabIndex = 18;
            this.labelNameEndSysMatrix.Text = "Gsys = ";
            // 
            // groupBox1
            // 
            this.groupBox1.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.groupBox1.Controls.Add(this.dataGridErrorInfi);
            this.groupBox1.Controls.Add(this.dataGridStartSysMatrix);
            this.groupBox1.Controls.Add(this.label8);
            this.groupBox1.Controls.Add(this.labelNameEndSysMatrix);
            this.groupBox1.Controls.Add(this.dataGridHSysT);
            this.groupBox1.Controls.Add(this.labelNameStartSysMatrix);
            this.groupBox1.Controls.Add(this.dataGridEndSysMatrix);
            this.groupBox1.Location = new System.Drawing.Point(554, 46);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(329, 637);
            this.groupBox1.TabIndex = 19;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Матрицы и Ошибки";
            // 
            // dataGridErrorInfi
            // 
            this.dataGridErrorInfi.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridErrorInfi.Location = new System.Drawing.Point(10, 454);
            this.dataGridErrorInfi.Name = "dataGridErrorInfi";
            this.dataGridErrorInfi.Size = new System.Drawing.Size(298, 177);
            this.dataGridErrorInfi.TabIndex = 23;
            // 
            // label8
            // 
            this.label8.AutoSize = true;
            this.label8.Location = new System.Drawing.Point(7, 366);
            this.label8.Name = "label8";
            this.label8.Size = new System.Drawing.Size(46, 13);
            this.label8.TabIndex = 19;
            this.label8.Text = "HsysT =";
            // 
            // dataGridHSysT
            // 
            this.dataGridHSysT.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridHSysT.Location = new System.Drawing.Point(55, 312);
            this.dataGridHSysT.Name = "dataGridHSysT";
            this.dataGridHSysT.Size = new System.Drawing.Size(253, 133);
            this.dataGridHSysT.TabIndex = 19;
            // 
            // groupBox2
            // 
            this.groupBox2.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.groupBox2.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.groupBox2.Controls.Add(this.button1);
            this.groupBox2.Controls.Add(this.textNBox);
            this.groupBox2.Controls.Add(this.radioButtonH);
            this.groupBox2.Controls.Add(this.GenerateMatrixButton);
            this.groupBox2.Controls.Add(this.radioButtonG);
            this.groupBox2.Controls.Add(this.labelNameStartMatrix);
            this.groupBox2.Controls.Add(this.textKBox);
            this.groupBox2.Controls.Add(this.dataGridStartMatrix);
            this.groupBox2.Controls.Add(this.label1);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Location = new System.Drawing.Point(60, 46);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(488, 213);
            this.groupBox2.TabIndex = 20;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "Начальная матрица";
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(93, 164);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(98, 23);
            this.button1.TabIndex = 13;
            this.button1.Text = "Инициализация";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // groupBox4
            // 
            this.groupBox4.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.groupBox4.Controls.Add(this.label7);
            this.groupBox4.Controls.Add(this.PBox);
            this.groupBox4.Controls.Add(this.label6);
            this.groupBox4.Controls.Add(this.TBox);
            this.groupBox4.Controls.Add(this.label5);
            this.groupBox4.Controls.Add(this.DMinBox);
            this.groupBox4.Controls.Add(this.dataGridICW);
            this.groupBox4.Controls.Add(this.label4);
            this.groupBox4.Controls.Add(this.label3);
            this.groupBox4.Controls.Add(this.KBox);
            this.groupBox4.Controls.Add(this.NBox);
            this.groupBox4.Location = new System.Drawing.Point(60, 265);
            this.groupBox4.Name = "groupBox4";
            this.groupBox4.Size = new System.Drawing.Size(475, 423);
            this.groupBox4.TabIndex = 22;
            this.groupBox4.TabStop = false;
            this.groupBox4.Text = "Таблица информационных и кодовых слов";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Location = new System.Drawing.Point(351, 23);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(25, 13);
            this.label7.TabIndex = 10;
            this.label7.Text = "p = ";
            // 
            // PBox
            // 
            this.PBox.Location = new System.Drawing.Point(378, 19);
            this.PBox.Name = "PBox";
            this.PBox.Size = new System.Drawing.Size(51, 20);
            this.PBox.TabIndex = 9;
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(275, 23);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(22, 13);
            this.label6.TabIndex = 8;
            this.label6.Text = "t = ";
            // 
            // TBox
            // 
            this.TBox.Location = new System.Drawing.Point(298, 19);
            this.TBox.Name = "TBox";
            this.TBox.Size = new System.Drawing.Size(51, 20);
            this.TBox.TabIndex = 7;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(179, 22);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(43, 13);
            this.label5.TabIndex = 6;
            this.label5.Text = "Dmin = ";
            // 
            // DMinBox
            // 
            this.DMinBox.Location = new System.Drawing.Point(222, 19);
            this.DMinBox.Name = "DMinBox";
            this.DMinBox.Size = new System.Drawing.Size(51, 20);
            this.DMinBox.TabIndex = 5;
            // 
            // dataGridICW
            // 
            this.dataGridICW.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dataGridICW.Location = new System.Drawing.Point(7, 57);
            this.dataGridICW.Name = "dataGridICW";
            this.dataGridICW.Size = new System.Drawing.Size(458, 349);
            this.dataGridICW.TabIndex = 4;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(100, 22);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(25, 13);
            this.label4.TabIndex = 3;
            this.label4.Text = "k = ";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(13, 22);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(25, 13);
            this.label3.TabIndex = 2;
            this.label3.Text = "n = ";
            // 
            // KBox
            // 
            this.KBox.Location = new System.Drawing.Point(122, 19);
            this.KBox.Name = "KBox";
            this.KBox.Size = new System.Drawing.Size(51, 20);
            this.KBox.TabIndex = 1;
            // 
            // NBox
            // 
            this.NBox.Location = new System.Drawing.Point(35, 19);
            this.NBox.Name = "NBox";
            this.NBox.Size = new System.Drawing.Size(52, 20);
            this.NBox.TabIndex = 0;
            // 
            // groupBox3
            // 
            this.groupBox3.Anchor = System.Windows.Forms.AnchorStyles.None;
            this.groupBox3.Controls.Add(this.textBox10);
            this.groupBox3.Controls.Add(this.button2);
            this.groupBox3.Controls.Add(this.textBox9);
            this.groupBox3.Controls.Add(this.textBox8);
            this.groupBox3.Controls.Add(this.textBox7);
            this.groupBox3.Controls.Add(this.textBox6);
            this.groupBox3.Controls.Add(this.textBox5);
            this.groupBox3.Controls.Add(this.textBox4);
            this.groupBox3.Controls.Add(this.textBox3);
            this.groupBox3.Controls.Add(this.textBox2);
            this.groupBox3.Controls.Add(this.textBox1);
            this.groupBox3.Controls.Add(this.testBox);
            this.groupBox3.Controls.Add(this.testButton);
            this.groupBox3.Controls.Add(this.testButton2);
            this.groupBox3.Location = new System.Drawing.Point(889, 49);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(546, 628);
            this.groupBox3.TabIndex = 21;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "Ввод / Вывод";
            // 
            // textBox10
            // 
            this.textBox10.Location = new System.Drawing.Point(278, 371);
            this.textBox10.Multiline = true;
            this.textBox10.Name = "textBox10";
            this.textBox10.Size = new System.Drawing.Size(262, 79);
            this.textBox10.TabIndex = 14;
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(239, 575);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(75, 23);
            this.button2.TabIndex = 13;
            this.button2.Text = "Перенос";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // textBox9
            // 
            this.textBox9.Location = new System.Drawing.Point(276, 19);
            this.textBox9.Multiline = true;
            this.textBox9.Name = "textBox9";
            this.textBox9.Size = new System.Drawing.Size(260, 103);
            this.textBox9.TabIndex = 11;
            // 
            // textBox8
            // 
            this.textBox8.Location = new System.Drawing.Point(6, 416);
            this.textBox8.Multiline = true;
            this.textBox8.Name = "textBox8";
            this.textBox8.Size = new System.Drawing.Size(266, 144);
            this.textBox8.TabIndex = 10;
            // 
            // textBox7
            // 
            this.textBox7.Location = new System.Drawing.Point(276, 286);
            this.textBox7.Multiline = true;
            this.textBox7.Name = "textBox7";
            this.textBox7.Size = new System.Drawing.Size(262, 79);
            this.textBox7.TabIndex = 9;
            // 
            // textBox6
            // 
            this.textBox6.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.textBox6.Location = new System.Drawing.Point(278, 456);
            this.textBox6.Multiline = true;
            this.textBox6.Name = "textBox6";
            this.textBox6.Size = new System.Drawing.Size(260, 104);
            this.textBox6.TabIndex = 8;
            // 
            // textBox5
            // 
            this.textBox5.Location = new System.Drawing.Point(276, 205);
            this.textBox5.Multiline = true;
            this.textBox5.Name = "textBox5";
            this.textBox5.Size = new System.Drawing.Size(262, 75);
            this.textBox5.TabIndex = 7;
            // 
            // textBox4
            // 
            this.textBox4.Location = new System.Drawing.Point(276, 129);
            this.textBox4.Multiline = true;
            this.textBox4.Name = "textBox4";
            this.textBox4.Size = new System.Drawing.Size(262, 70);
            this.textBox4.TabIndex = 6;
            // 
            // textBox3
            // 
            this.textBox3.Location = new System.Drawing.Point(6, 331);
            this.textBox3.Multiline = true;
            this.textBox3.Name = "textBox3";
            this.textBox3.Size = new System.Drawing.Size(266, 79);
            this.textBox3.TabIndex = 5;
            // 
            // textBox2
            // 
            this.textBox2.Location = new System.Drawing.Point(6, 250);
            this.textBox2.Multiline = true;
            this.textBox2.Name = "textBox2";
            this.textBox2.Size = new System.Drawing.Size(266, 75);
            this.textBox2.TabIndex = 4;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1484, 711);
            this.Controls.Add(this.groupBox4);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.MinimumSize = new System.Drawing.Size(1500, 750);
            this.Name = "Form1";
            this.Text = "Laboratory3";
            ((System.ComponentModel.ISupportInitialize)(this.dataGridStartMatrix)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridStartSysMatrix)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridEndSysMatrix)).EndInit();
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridErrorInfi)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridHSysT)).EndInit();
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox4.ResumeLayout(false);
            this.groupBox4.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.dataGridICW)).EndInit();
            this.groupBox3.ResumeLayout(false);
            this.groupBox3.PerformLayout();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.TextBox testBox;
        private System.Windows.Forms.Button testButton;
        private System.Windows.Forms.Button testButton2;
        private System.Windows.Forms.RadioButton radioButtonH;
        private System.Windows.Forms.RadioButton radioButtonG;
        private System.Windows.Forms.TextBox textNBox;
        private System.Windows.Forms.TextBox textKBox;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.DataGridView dataGridStartMatrix;
        private System.Windows.Forms.Label labelNameStartMatrix;
        private System.Windows.Forms.Button GenerateMatrixButton;
        private System.Windows.Forms.DataGridView dataGridStartSysMatrix;
        private System.Windows.Forms.Label labelNameStartSysMatrix;
        private System.Windows.Forms.DataGridView dataGridEndSysMatrix;
        private System.Windows.Forms.Label labelNameEndSysMatrix;
        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.GroupBox groupBox4;
        private System.Windows.Forms.DataGridView dataGridICW;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox KBox;
        private System.Windows.Forms.TextBox NBox;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.TextBox DMinBox;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.TextBox PBox;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.TextBox TBox;
        private System.Windows.Forms.TextBox textBox2;
        private System.Windows.Forms.TextBox textBox3;
        private System.Windows.Forms.DataGridView dataGridHSysT;
        private System.Windows.Forms.Label label8;
        private System.Windows.Forms.DataGridView dataGridErrorInfi;
        private System.Windows.Forms.TextBox textBox4;
        private System.Windows.Forms.TextBox textBox7;
        private System.Windows.Forms.TextBox textBox6;
        private System.Windows.Forms.TextBox textBox5;
        private System.Windows.Forms.TextBox textBox8;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.TextBox textBox9;
        private System.Windows.Forms.TextBox textBox10;
        private System.Windows.Forms.Button button1;
    }
}

