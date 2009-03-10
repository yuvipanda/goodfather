Imports IronPython.Runtime
Imports System.IO
Imports System.Data
Public Enum OutputFormat
    TSV
    CSV
    NativeR
    NativePython
    XML
End Enum
Public Class ResultSet
    Private _Data As DataTable

    Public Sub New(ByVal Headers As List(Of String), ByVal Data As IList)
        _Data = New DataTable()
        For Each header In Headers
            _Data.Columns.Add(header, GetType(Object))
        Next

        For Each datum In Data
            Dim dr = _Data.NewRow
            Dim i = 0
            For Each item In datum
                dr(i) = item
                i += 1
            Next
            _Data.Rows.Add(dr)
        Next
    End Sub

    Private Function ToFixedFormatRecord(ByVal List As IEnumerable) As String
        Dim sb As New Text.StringBuilder
        For Each item In List
            Select Case item.GetType.FullName
                Case GetType(DateTime).FullName
                    sb.AppendFormat("{0}" & vbTab, item.ToString("s")) 'HACK: vbTab shouldn't be used here. Figure out why \t isn't working.
                Case Else
                    sb.AppendFormat("'{0}'" & vbTab, item.ToString.Replace("'", "\'"))
            End Select
        Next
        Return sb.ToString
    End Function
    Private Sub ToTSV(ByVal FilePath As String)
        Dim sr As New StreamWriter(FilePath)
        sr.WriteLine(ToFixedFormatRecord(_Data.Columns.Cast(Of DataColumn).Select(Function(dc) dc.ColumnName)))

        For Each dr As DataRow In _Data.Rows
            sr.WriteLine(ToFixedFormatRecord(dr.ItemArray))
        Next
        sr.Close()
    End Sub
    Private Sub ToCSV(ByVal FilePath As String)
        'Stub.
    End Sub
    Private Sub ToXML(ByVal FilePath As String)
        'Stub
    End Sub
    Private Sub ToNativeR(ByVal FilePath As String)
        'Stub
    End Sub
    Private Sub ToNativePython(ByVal FilePath As String)
        'Stub
    End Sub
    Public Sub WriteToFile(ByVal FilePath As String, ByVal Format As OutputFormat)
        Select Format
            Case OutputFormat.TSV
                ToTSV(FilePath)
            Case OutputFormat.CSV
                ToCSV(FilePath)
            Case OutputFormat.XML
                ToXML(FilePath)
            Case OutputFormat.NativeR
                ToNativeR(FilePath)
            Case OutputFormat.NativePython
                ToNativePython(FilePath)
        End Select
    End Sub
End Class
