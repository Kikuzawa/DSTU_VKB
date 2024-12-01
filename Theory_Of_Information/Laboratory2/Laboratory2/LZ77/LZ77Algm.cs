
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;


namespace Laboratory2
{
    public static class LZ77Algm
    {
        static bool ExtendedAlgm = false;
        public static IAlgmEncoded<List<LZ77CodeBlock>> Encode(string source, bool extended)
        {
            ExtendedAlgm = extended;
            return Encode(source);
        }
        /// <summary>
        /// String compression using the LZ77 algorithm
        /// </summary>
        /// <param name="inputString">Source string</param>
        /// <returns>Compressed (encoded) string</returns>
        public static IAlgmEncoded<List<LZ77CodeBlock>> Encode(string inputString)
        {
            List<LZ77CodeBlock> result = new List<LZ77CodeBlock>();
            StringBuilder searchBuffer = new StringBuilder();
            StringBuilder establishingBuffer = new StringBuilder(inputString);
            StringBuilder extended = new StringBuilder(string.Empty);

            int currentLengthSubString = 0;
            //Кодирование идет до тех пор пока учреждающий буфер (establishingBuffer) не окажется пуст
            while (establishingBuffer.Length > 0)
            {
                int positionInBuffer = -1;
                //Ищем в searchBuffer максимальную подстроку, имеющую вхождение в establishingBuffer
                
                while (true)
                {
                    int previousPositionInBuffer = positionInBuffer;

                    if (establishingBuffer.Length < currentLengthSubString + 1)
                        positionInBuffer = -1;
                    else
                        positionInBuffer = searchBuffer.IndexOf(establishingBuffer.Substring(0, currentLengthSubString + 1));

                    if (positionInBuffer < 0)
                    {
                        //Если подстроки не найдено возвращаем текущее значение начала этой строки
                        //по умолчанию -1
                        positionInBuffer = previousPositionInBuffer;
                        break;
                    }
                    else
                    {
                        currentLengthSubString++;
                    }
                }

                //Если строки(символа) не было найдено, то заносим в буффер новый элемент
                if (positionInBuffer < 0)
                {
                    char nextChar = establishingBuffer[0];

                    searchBuffer.Append(nextChar);
                    establishingBuffer.Remove(0, 1);

                    var codeblock = new LZ77CodeBlock(0, 0, nextChar);
                    if (ExtendedAlgm)
                    {
                        extended.Append(searchBuffer.ToString() + "\t\t " + establishingBuffer.ToString() + "\t\t " + codeblock + "\n");
                    }
                    
                    result.Add(codeblock); //указываем на него метку
                }
                else
                {
                    Console.WriteLine(searchBuffer + " - " + positionInBuffer);
                    int offset = searchBuffer.Length;
                    int length = currentLengthSubString;

                    //Если длина найденной подстроки равна количеству элементов буффера
                    //то последний символ это символ конца строки
                    if (currentLengthSubString == establishingBuffer.Length)
                        establishingBuffer.Append('$');
                    char nextChar = establishingBuffer[currentLengthSubString];

                    string subInEstablish = establishingBuffer.Substring(0, currentLengthSubString+1);
                    establishingBuffer.Remove(0, length+1);
                    searchBuffer.Append(subInEstablish);

                    var codeblock = new LZ77CodeBlock(offset, length, nextChar);
                    if (ExtendedAlgm)
                    {
                        extended.Append(searchBuffer.ToString() + "\t\t " + establishingBuffer.ToString() + "\t\t " + codeblock + "\n");
                    }
                    result.Add(codeblock);
                }

                currentLengthSubString = 0;
            }

            return new EncodedMessage<List<LZ77CodeBlock>>(result, CalculateCompressionRatio(inputString, result), extended.ToString());
        }

        /// <summary>
        /// Calculation of the compression ratio
        /// </summary>
        /// <param name="sourceString">Source string</param>
        /// <param name="compressionString">Compressed (encoded) string</param>
        /// <returns>Compression ratio</returns>
        private static double CalculateCompressionRatio(string sourceString, List<LZ77CodeBlock> compressionString)
        {
            //Считаем что в стандартной кодировке один символ = 8бит
            double countBitsSourceString = 8 * sourceString.Length;

            double countBitsCompressionString = 0;
            foreach (LZ77CodeBlock compression in compressionString)
            {
                int countBitsOffset = Convert.ToString(compression.Offset, 2).Length;
                int countBitsLength = Convert.ToString(compression.Length, 2).Length;
                int countBitsChar = 8;

                countBitsCompressionString += countBitsOffset + countBitsOffset + countBitsChar;
            }

            return Math.Round(countBitsSourceString / countBitsCompressionString, 3);
        }

        private static List<LZ77CodeBlock> ParseEncodedString(string encodedString)
        {
            List<LZ77CodeBlock> encodedStringParsed = new List<LZ77CodeBlock>();
            // вид кодового блока:
            //({0},{1},{2})...({0},{1},{2})
            //парсит всю строку на блоки
            //globalCode - проверяет всю строку, подходит ли она для декодирования
            Regex globalCode = new Regex(@"(?=^)(([(](\d+)([,])(\d+)([,])(.|\n|\r|\t)[)])|(\s)|(\n)|(\r))+(?=$)");
            Regex regex = new Regex(@"([(](\d+)([,])(\d+)([,])(.|\n|\r|\t)[)])"); //регулярка кодового блока
            Regex intRegex = new Regex(@"\d+"); //регулярка цыфры
            if (!globalCode.IsMatch(encodedString))
            {
                throw new CodingException();
            }

            MatchCollection matches = regex.Matches(encodedString);
            foreach (Match match in matches)
            {
                string codeBlock = match.Value;

                MatchCollection matchesBlock = intRegex.Matches(codeBlock);
                encodedStringParsed.Add(new LZ77CodeBlock(int.Parse(matchesBlock[0].Value), int.Parse(matchesBlock[1].Value), codeBlock[codeBlock.Length - 2]));
            }

            return encodedStringParsed;
        }

        /// <summary>
        /// Decoding strings compressed by the LZ77 algorithm
        /// </summary>
        /// <param name="encodedString">Compressed (encoded) string</param>
        /// <returns>Decoded string</returns>
        public static IAlgmEncoded<string> Decode(string encodedString)
        {
            var encodedStringParsed = ParseEncodedString(encodedString);

            StringBuilder resultDecoding = new StringBuilder(string.Empty);

            foreach (LZ77CodeBlock codeBlock in encodedStringParsed)
            {

                if (codeBlock.Length > 0)
                {
                    int start = resultDecoding.Length - codeBlock.Offset;
                    for (int i = 0; i <= codeBlock.Length - 1; i++)
                        resultDecoding.Append(resultDecoding[start + i]);
                }
                resultDecoding.Append(codeBlock.NextChar);
            }

            if (resultDecoding.Length > 0 && resultDecoding[resultDecoding.Length - 1].Equals('$'))
                resultDecoding.Remove(resultDecoding.Length - 1, 1);

            var decodedString = resultDecoding.ToString();
            return new EncodedMessage<string>(decodedString, CalculateCompressionRatio(decodedString, encodedStringParsed));
        }
    }

    public static class StreamHelper
    {
        public static int FindPosition(Stream stream, byte[] pattern)
        {
            using (var reader = new BinaryReader(stream))
            {
                var buffer = new byte[4096];
                int bytesRead;
                int position = 0;

                do
                {
                    bytesRead = reader.Read(buffer, 0, buffer.Length);
                    for (int i = 0; i < bytesRead && i < pattern.Length; i++)
                    {
                        bool match = true;
                        for (int j = 0; j < pattern.Length && i + j < bytesRead; j++)
                        {
                            if (buffer[i + j] != pattern[j])
                            {
                                match = false;
                                break;
                            }
                        }
                        if (match && position + pattern.Length <= bytesRead)
                        {
                            return position;
                        }
                    }
                    position += bytesRead;
                } while (bytesRead == buffer.Length);

                return -1;
            }
        }
    }


}
