#nhfx - new hope for xml
from xml.dom import minidom

class Node(object):
    def __init__(self):
        self.parent = None
        
    def __iter__(self):
        raise NotImplementedError("Node.__iter__")
    
    def render(self):
        raise NotImplementedError("Node.render")
        
        
        
class Text(Node):
    def __init__(self, value=None):
        super(Text,self).__init__()
        self.value = value
        
    def __repr__(self):
        return "Text(%s)" % str(self.value)
    
    def __iter__(self):
        yield self
        
    def render(self):
        if self.value is None:
            return ""
        else:
            return self.value
        
        
        
class Attribute(Node):
    def __init__(self, name, value=None):
        super(Attribute, self).__init__()
        self.name = name
        self.value = value
        
    def __repr__(self):
        return "Attribute(%s, %s)" % (self.name, str(self.value))
    
    def __iter__(self):
        yield self
        
    def render(self):
        return '%s="%s"' %(self.name, str(self.value))
        
        
        
class Element(Node):
    def __init__(self, name):
        super(Element, self).__init__()
        self.name = name
        self._childs = []
        
    def add(self, child):
        child.parent = self
        self._childs.append(child)
        
    def __repr__(self):
        return "Element(%s)" % self.name
    
    def __iter__(self):
        yield self
        for child in self._childs:
            for node in child:
                yield node
                
    def delete(self):
        if self.parent is not None:
            self.parent._childs.remove(self)
            self.parent = None
            
        return self
    
    def render(self):
        attrs = filter(attributes, self._childs)
        nodes = filter(OR(texts, elements), self._childs)
            
        if len(attrs) > 0:
            attrs_string = " "+" ".join([ a.render() for a in attrs])
        else:
            attrs_string = ""
        
        if len(nodes) > 0:
            nodes_string = "".join([n.render() for n in nodes])
            return "<%s%s>%s</%s>" %(self.name, attrs_string, nodes_string,self.name)
        else:
            return "<%s%s/>" % (self.name,attrs_string)
        
        
        
def parse(xml):
    def read(node):
        if isinstance(node, minidom.Text):
            return Text(node.nodeValue)
        elif isinstance(node, minidom.Attr):
            return Attribute(node.nodeName,node.childNodes[0].nodeValue)
        elif isinstance(node,minidom.Element):
            element = Element(node.nodeName) 
            for child in node.childNodes:
                element.add(read(child))
            for _,value in node._attrs.iteritems():
                element.add(read(value))
        
            return element
        
        else:
            raise node
    #----------------------------------
    document = minidom.parseString(xml)
    return read(document.childNodes[0])


# Filters

def OR(*methods):
    def inner(node):
        return any([ method(node) for method in methods])
    return inner

def AND(*args):
    def inner(node):
        return all([ method(node) for method in args])
    return inner

def texts(node):
    return isinstance(node,Text)

def attributes(node):
    return isinstance(node, Attribute)

def elements(node):
    return isinstance(node, Element)


def childof(parent):
    def inner(node):
        return node.parent==parent
    return inner    

def named(name):
    def inner(node):
        return hasattr(node, "name") and node.name == name
    return inner

def parent_is(method):
    def inner(node):
        return method(node.parent)
    return inner

#Utilities
def one(root, method):
    return root.filter(method)[0]

def delete(node):
    node.delete()

def attribute(element, name):
    return element.filter(AND(attributes, named(name), childof(element)))[0]

def value(node):
    if isinstance(node, Attribute):
        return node.value
    elif isinstance(node, Text):
        return node.value
    elif isinstance(node, Element):
        text_nodes = node.filter(AND(texts,childof(node)))
        return "".join( [text.value for text in text_nodes])

def write_to(string, path):
    with open(path,"w") as f:
        f.write(string)

def example1():
    root = parse(open("tests/69.xml").read())
    assets = root.filter(named("asset_name"))
    for asset in assets:
        text = one(asset, texts)
        text.value = text.value.split("\\")[-1]
    print root.render()
    


    
        
    