$filename = $args[0]
echo $filename

$data = Get-DataStore $args[0]

$r = $procs.GRShared.SourcesCount.Process($data)

$tsvname = $filename + ".tsv"

echo "Shit" > $tsvname

Write-ResultSet $r $tsvname

rscript .\GRSharedLeaderBoard.r --args $tsvname
& ($tsvname)
