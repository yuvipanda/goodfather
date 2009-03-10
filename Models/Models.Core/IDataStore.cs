using System;
using System.Collections.Generic;

namespace Models.Core
{
    public interface IDataStore
    {        
        List<string> MajorDataTypeTemplates { get; }

        System.Collections.IList Data { get; }

        void Load(string FileName);
        void Save(string FileName);
    }
}
