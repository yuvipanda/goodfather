$script:models = @{}

function Create-Type( [Type] $type)
{
    return [Activator]::CreateInstance($type, [Reflection.BindingFlags]::CreateInstance,$null,$null,$null)
}

function Get-SupportedExtension([Type] $StoreType)
{
	return [Attribute]::GetCustomAttribute($StoreType, [Models.Core.SupportedExtensionAttribute]).Extension
}

function Setup-Runtime
{
    Add-Type -path (Join-Path $PsScriptRoot Processors.dll)
    
    $modelsAssembly = [Reflection.Assembly]::LoadFrom((Join-Path $PsScriptRoot Models.dll))
    
    $modeltypes = ($modelsAssembly.GetExportedTypes() | where { $_.GetInterfaces() | where {$_.Name -eq "IDataStore"} } )
    foreach($mt in $modeltypes) 
	{ 	
		$ext = Get-SupportedExtension($mt)
		$script:models.Add($ext, $mt)	
	}
}


function Get-DataStore($filepath)
{
    $filepath = (Resolve-Path $filepath)
        
    $ext = (new-object IO.FileInfo $filepath).Extension.Trim(".")    
    $store = Create-Type($script:models[$ext])
    $store.Load($filepath)
    return $store
}

function Filter-DataStore([Models.Core.IDataStore] $datastore, [ScriptBlock] $filter, [Models.Core.IDataStore] $outs)
{	    
	$newstore = Create-Type($datastore.GetType())
	foreach ($d in $datastore.Data) { 
    if ($filter.InvokeReturnAsIs($d))
    {
    $newstore.Data.Add($d) 
    echo $d.Name
    }
    echo $d.Name
    }
	return $newstore.Data
	#return $newstore	
}

function Get-Processor($filepath)
{
	return [Processors.Processor]::LoadProcessor((Resolve-Path $filepath))
}

function Write-ResultSet([Processors.ResultSet] $resultset, $filepath, $format)
{
	$filepath = (Resolve-Path $filepath) #To support file paths like ..\hi.tsv, etc

	$outputformat = [Processors.OutputFormat]::TSV #If nothing is specified for format, assume TSV
	if ($format -eq "CSV")
	{
		$outputformat = [Processors.OutputFormat]::CSV
	}
	#TODO: Add more format options as they are supported. CSV, btw, is not yet supported ;)

	$resultset.WriteToFile($filepath,$outputformat)
}

function Run-Processor([Processors.Processor] $processor, [Models.Core.IDataStore] $datastore)
{
	return $processor.Process($datastore)
}

Export-ModuleMember Setup-Runtime
Export-ModuleMember Get-DataStore
Export-ModuleMember Filter-DataStore
Export-ModuleMember Get-Processor
Export-ModuleMember Write-ResultSet
Export-ModuleMember Run-Processor
Export-ModuleMember Create-Type
