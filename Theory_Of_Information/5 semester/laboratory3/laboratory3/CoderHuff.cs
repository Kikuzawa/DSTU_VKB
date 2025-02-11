using Laboratory3;
using System;
using System.Collections.Generic;

namespace laboratory3
{
    internal class CoderHuff
    {
        Queue<HuffmanNode> queueTempNodes = new Queue<HuffmanNode>();

        List<HuffmanNode> listTempOrderedNodes = new List<HuffmanNode>();

        List<HuffmanNode> listFixedNodes = new List<HuffmanNode>();

        List<EncodedChar> listBinary = new List<EncodedChar>();

        String output;

        public String EncodeHaffman(String text)
        {
            string inputText = text;

            listTempOrderedNodes.Clear();
            queueTempNodes.Clear();
            listFixedNodes.Clear();
            listBinary.Clear();


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



            for (int i = 0; i < listFixedNodes.Count; i++)
            {

                if (listFixedNodes[i].NodeString.Length == 1)
                {
                    EncodedChar en = new EncodedChar();
                    en.Character = listFixedNodes[i].NodeString;
                    en.Binary = AnalyzeBinary(en.Character, listFixedNodes[listFixedNodes.Count - 1]);
                    listBinary.Add(en);
                }
            }

            input = inputText;
            output = "";
            while (input != "")
            {
                string txt = input.Substring(0, 1);
                input = input.Remove(0, 1);
                for (int i = 0; i < listBinary.Count; i++)
                {
                    if (listBinary[i].Character == txt) output = output + listBinary[i].Binary;
                }
            }

            return output;


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

        public String DecodeMethod(String text)
        {
            if (listFixedNodes.Count > 0)
            {
                string input = text;


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
                    return output;
                }
                else
                {
                    return "Unknown binary sequence detected. Make sure you've inputed the correct binary sequence according to the tree."
                        + "\n\n" + "Please note that binary numbers consists only number 0 and or 1";
                }
            }
            else
            {
                return "Please encode something to make the HuffmanTree for decoding process...";
            }
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
    }
}
