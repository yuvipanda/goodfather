require 'rexml/document'
include REXML

module Models
	def parse_templates(filepath)
		b = binding()
		source = File.new(filepath,'r').read()

		eval source, b

		return eval('templates',b)
	end
	def parse_model(filepath)
		b = binding()

		source = File.new(filepath,'r').read()

		eval source, b

		return eval('model', b)
	end

	class TemplateDef 

		attr_accessor :name, :fields, :collections
		
		def initialize(name, fields, collections)
			@name = name
			@fields = fields
			@collections = collections
		end
	end 

	class Template
		attr_accessor :name, :params

		def initialize(name, params={})
			@name = name
			@params = params
		end
	end

	class Type
		attr_accessor :name, :fields, :collections, :templates		
		
		def initialize(name, fields, collections, templates)
			@name = name
			@fields = fields
			@collections = collections
			@templates = templates
		end

		def expand_templates(template_definitions)
			@templates.each do |template|
				template_def = template_definitions[template.name]				
				template_def.fields.each { |field| 
											 expand_params(field[0],template.params)
											 expand_params(field[1],template.params)														   
											 @fields[field[0]] = field[1]
										 }
				template_def.collections.each { |collection| 
												expand_params(collection[0],template.params)
												expand_params(collection[1],template.params)
												@collections[collection[0]] = collection[1] 
											  }				
			end
		end

		def expand_params(text, params)
			params.each do |param|
				text.gsub!(param[0],param[1])
			end
		end



	end

	class Model
		attr_accessor :name, :types, :extension, :major_data_type

		def initialize(name, extension)
			@name = name
			@extension = extension
		end

		def expand_templates(template_definitions)
			@types.each do |type|
				type.expand_templates(template_definitions)
			end 
		end

	end
end  
