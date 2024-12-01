using Laboratory2;
using System.Collections.Generic;
using System.Text;

namespace Laboratory2
{
    internal class EncodedMessage<T> : IAlgmEncoded<T>
    {
        private string extended;
        private T answer;
        private double compressionRatio;

        public T GetAnswer()
        {
            return answer;
        }

        public override string ToString()
        {
            // В некоторых алгоритмах выхлопной ответ выглядит где то как строка
            // где то как массив "своих" объектов
            StringBuilder stringBuilder = new StringBuilder(extended);

            if (typeof(T).Name == typeof(List<>).Name)
            {
                var m = (IEnumerable<object>)answer;
                foreach (var item in m)
                {
                    stringBuilder.Append(item.ToString());
                }

                return stringBuilder.ToString();
            }
            else if (typeof(T) == typeof(string))
            {
                return answer.ToString();
            }

            return base.ToString();
        }

        public double GetCompressionRatio()
        {
            return compressionRatio;
        }

        public EncodedMessage(T answer, double compressionRatio) : this(answer, compressionRatio, string.Empty)
        {
        }

        public EncodedMessage(T answer, double compressionRatio, string extended)
        {
            this.answer = answer;
            this.compressionRatio = compressionRatio;
            this.extended = extended;
        }
    }
}
