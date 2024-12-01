using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Laboratory2
{
    public class CodingException : Exception
    {
        public CodingException()
            : base("Error in coding!") { }
        public CodingException(string message)
            : base(message) { }
    }
}
