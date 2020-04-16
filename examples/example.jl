import JSON

open("fodo.json", "r") do file
    global data
    data = JSON.parse(file)
end

element_name = "Q1"
type, attributes = data["elements"][element_name]
length = attributes["length"]
println("The element $element_name is a $type and is $length meters long!")