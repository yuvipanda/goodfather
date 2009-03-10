Imports Microsoft.Scripting
Imports Microsoft.Scripting.Hosting
Imports IronPython.Hosting
Imports IronPython.Runtime
Imports Microsoft.Scripting.Runtime
Imports Microsoft.Scripting.Hosting.Providers.HostingHelpers
Public Class Processor
    Private _RequiresTemplates As New List(Of String)
    Private _Headers As New List(Of String)
    Private _MapFunction As Func(Of Object, IDictionary)
    Private _ReduceFunction As Func(Of KeyValuePair(Of String, Object), IList)

    Private _Scope As ScriptScope

    Private _Name As String
    Private _Description As String
    Private _Category As String
    Private _RequiresExtension As String
    Public ReadOnly Property Category() As String
        Get
            Return _Category
        End Get
    End Property
    Public ReadOnly Property Name() As String
        Get
            Return _Name
        End Get
    End Property
    Public ReadOnly Property Description() As String
        Get
            Return _Description
        End Get
    End Property
    Public ReadOnly Property Headers() As List(Of String)
        Get
            Return _Headers
        End Get
    End Property
    Public ReadOnly Property RequiresTemplates() As List(Of String)
        Get
            Return _RequiresTemplates
        End Get
    End Property
    Public ReadOnly Property RequiresExtension() As String
        Get
            Return _RequiresExtension
        End Get
    End Property
    Public Sub AddParameter(ByVal Name As String, ByVal Value As String)
        _Scope.SetVariable(Name, Value)
    End Sub
    Public Function Map(ByVal MainArgument As Object) As IDictionary
        Return _MapFunction(MainArgument)
    End Function

    Public Function Reduce(ByVal KeyValuePair As KeyValuePair(Of String, Object)) As IList
        Return _ReduceFunction(KeyValuePair)
    End Function

    Friend Sub New(ByVal Name As String, ByVal Description As String, ByVal Category As String, ByVal Headers As List(Of String), ByVal MapFunction As Func(Of Object, IDictionary), ByVal ReduceFunction As Func(Of KeyValuePair(Of String, Object), IList), ByVal RequiresTemplates As List(Of String), ByVal RequiresExtension As String, ByVal Scope As ScriptScope)
        _Category = Category
        _Name = Name
        _Description = Description
        _Headers = Headers
        _RequiresTemplates = RequiresTemplates
        _RequiresExtension = RequiresExtension
        _MapFunction = MapFunction
        _ReduceFunction = ReduceFunction
        _Scope = Scope

    End Sub
    Private Function SupportedExtensionForStore(ByVal Store As Models.Core.IDataStore) As String
        Return CType(Attribute.GetCustomAttribute(Store.GetType, GetType(Models.Core.SupportedExtensionAttribute)), Models.Core.SupportedExtensionAttribute).Extension
    End Function
    Public Function SupportsStore(ByVal Store As Models.Core.IDataStore) As Boolean
        Dim StoreExtension = SupportedExtensionForStore(Store)
        If RequiresExtension = Nothing Then
            Return RequiresTemplates.All(Function(t) Store.MajorDataTypeTemplates.Contains(t))
        ElseIf RequiresTemplates Is Nothing Then
            Return RequiresExtension = StoreExtension
        ElseIf Not (RequiresExtension = Nothing AndAlso RequiresTemplates Is Nothing) Then
            Return RequiresTemplates.All(Function(t) Store.MajorDataTypeTemplates.Contains(t)) AndAlso RequiresExtension = StoreExtension
        Else
            'This should never happen. Atleast one 'requires' should be specified.
            Throw New ArgumentException("Either RequiresTemplates or RequiresExtension should be specified.")
        End If
    End Function

    Private Shared _Engine As ScriptEngine = Python.CreateEngine

    Public Shared Function LoadProcessor(ByVal FilePath As String) As Processor
        Dim source = _Engine.CreateScriptSourceFromFile(FilePath)
        Dim compiledSource = source.Compile()
        Dim scope = _Engine.CreateScope()

        compiledSource.Execute(scope)

        Dim mapFunction = Function(x) CType(scope.GetVariable("map"), PythonFunction).Target.DynamicInvoke(x)
        Dim reduceFunction = Function(x) CType(scope.GetVariable("reduce"), PythonFunction).Target.DynamicInvoke(x)

        Dim name = scope.GetVariable(Of String)("name")
        Dim description = scope.GetVariable(Of String)("description")
        Dim category = scope.GetVariable(Of String)("category")
        Dim headers = scope.GetVariable(Of IEnumerable)("headers").Cast(Of String).ToList

        Dim requiresTemplates As IEnumerable, requiresTemplatesList As IList(Of String)
        Dim requiresExtension As String
        If (scope.TryGetVariable(Of IEnumerable)("requirestemplates", requiresTemplates) = False) Then
            requiresExtension = scope.GetVariable(Of String)("requiresextension")
        Else
            requiresTemplatesList = requiresTemplates.Cast(Of String).ToList
        End If
        Dim processor = New Processor(name, description, category, headers, mapFunction, reduceFunction, requiresTemplatesList, requiresExtension, scope)
        Return processor
    End Function

    Public Function Process(ByVal Data As Models.Core.IDataStore) As ResultSet
        Dim results As New List(Of IList)
        Dim intermediateDict As New Dictionary(Of String, Object)

        For Each d In Data.Data
            'Map
            Dim mappedKeys = Map(d)

            'Partition
            For Each mappedkvp In mappedKeys
                If intermediateDict.ContainsKey(mappedkvp.Key) Then
                    intermediateDict(mappedkvp.Key).Add(mappedkvp.Value)
                Else
                    Dim valuesList As New List(Of Object)
                    valuesList.Add(mappedkvp.Value)
                    intermediateDict.Add(mappedkvp.Key, valuesList)
                End If
            Next
        Next

        'Reduce
        For Each imkvp In intermediateDict
            results.Add(Reduce(imkvp))
        Next

        'Return ResultSet
        Return New ResultSet(Headers, results)
    End Function

End Class
