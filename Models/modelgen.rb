require 'erb'
require 'Models'

include Models

if ARGV.length == 0 then
	puts "Usage: modelgen.rb <generator> <model> <output>"
	exit
end

generatorFile = ARGV[0]
modelFile = ARGV[1]
outputFile = ARGV[2]

fin = File.open(generatorFile,'r')

eb = ERB.new(fin.read)
model = Models.parse_model(modelFile)

templates = Models.parse_templates('Templates.rdef')

model.expand_templates(templates)

fout = File.open(outputFile,'w')
fout.write(eb.result(binding()))
