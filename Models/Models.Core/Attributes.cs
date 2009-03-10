using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Models.Core
{
    [global::System.AttributeUsage(AttributeTargets.Class, Inherited = false, AllowMultiple = false)]
    public sealed class SupportedExtensionAttribute : Attribute
    {
        private string _Extension;

        public SupportedExtensionAttribute(string Extension)
        {
            _Extension = Extension;            
        }

        public string Extension
        {
            get { return _Extension; }
        }
    }

    [global::System.AttributeUsage(AttributeTargets.Class, Inherited = false, AllowMultiple = true)]
    public sealed class TemplateAttribute : Attribute
    {
        private string _Name;

        public TemplateAttribute(string Name)
        {
            _Name = Name;
        }

        public string Name
        {
            get { return _Name; }
        }
    }


}
