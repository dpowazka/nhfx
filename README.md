nhfx
====

Regular data formats like JSON or YMAL map naturally to objects, but XML was designed 
as a "document" format and is has some clunky elements like mixed elements, 
repetition of tags, white spaces that change content. 

Example of problematic mixed XML:
<airport>
	Description 1
	<code type="iata">WAWA</code>
	Description 2
	<code type="icao">WAW</code>
	<name>Chopin</name>
</airport> 

Without XSD it would be hard to write general maper that would detect that code
element is repeated, and should be represented as list. Second issue is text 
elements between tags and fact that their relation to tag elements matter.
Consider following example (from http://www.w3schools.com/schema/schema_complex_mixed.asp)
 
<letter>
  Dear Mr.<name>John Smith</name>.
  Your order <orderid>1032</orderid>
  will be shipped on <shipdate>2001-07-13</shipdate>.
</letter>    

In my opinion Python at the moment lacks good support for XML format. At the 
time of writing only one library - lxml, supports most of XSD specification and 
all major Python soap libraries are suspended.

The idea is that, the some problem was already solved for HTML by jquery. We 
could adopt it in pythonic way, by represting XML DOM in consistent way as a tree
structure, where child points to parent and parent has list o childs. Such tree
could be easily traversed in recursive way and flattened to list. 

Translation to list is important for searching for elements, which is usually the most 
complicated operation. Searching in lists is easily done with filter command. 

Example code:

root = parse(xml)
filter(lambda element: element.name == "Item", root.childs())
filter(lambda element: element.name == "Item" and element.parent.name=="Layer", root.childs())

Implementing features like xpath would be only a matter of providing of single 
fuction.
 
filter(xpath("Layer\Item"), root.childs()) 



  

