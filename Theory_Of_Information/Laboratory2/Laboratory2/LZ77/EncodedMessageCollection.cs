namespace Laboratory2
{
    internal class EncodedMessage<T1, T2> : IAlgmEncoded<T1, T2>
    {
        private string extended;
        private T1 answer;
        private T2 data;
        private double compressionRatio;

        public T1 GetAnswer()
        {
            return answer;
        }

        public T2 GetData()
        {
            return data;
        }
        public override string ToString()
        {
            if (typeof(T1) == typeof(string))
            {
                return answer.ToString();
            }

            return base.ToString();
        }

        public double GetCompressionRatio()
        {
            return compressionRatio;
        }

        public EncodedMessage(T1 answer, T2 frequencies, double compressionRatio) : this(answer, frequencies, compressionRatio, string.Empty)
        {
        }
        public EncodedMessage(T1 answer, T2 frequencies, double compressionRatio, string extended)
        {
            this.answer = answer;
            this.data = frequencies;
            this.compressionRatio = compressionRatio;
            this.extended = extended;
        }
    }
}
