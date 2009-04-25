require 'json'
require 'sqlite3'
require 'FileUtils'

class Persistable
	def initialize()
		@dict = {}
	end
	def method_missing(meth,*args)
		if /=$/=~ (name=meth.id2name) then
			@dict[name[0...-1]] = (args.length<2 ? args[0] : args)
		else
			@dict[name]
		end
	end

	def to_json(*a)
		return @dict.to_json(*a)
	end

end

class PersistableContainer
	def initialize(filename, create_new=True)
		FileUtils.rm(filename) if create_new and File.file?(filename)

		@db = SQLite3::Database.new(filename)
	
		@db.execute("CREATE TABLE Data (Data)") if create_new
	end

	def persist(obj)
		@db.execute("INSERT INTO Data VALUES (:Data)", 
					":Data" => JSON.generate(obj))
		@db.commit
	end
end
