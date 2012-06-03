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
        
    def delete(self):
        if self.parent is not None:
            self.parent._childs.remove(self)
            self.parent = None
        
        
        
class Attribute(Node):
    def __init__(self, name, value=None, namespace=None,shortns=None):
        super(Attribute, self).__init__()
        self.name = name
        self.value = value
        self.namespace = namespace
        self.shortns = shortns
        
    def __repr__(self):
        return "Attribute(%s, %s, %s)" % (self.namespace, self.name, str(self.value))
    
    def __iter__(self):
        yield self
        
    def render(self):
        if self.shortns:
            return '%s:%s="%s"' %(self.shortns,self.name, str(self.value))
        else:
            return '%s="%s"' %(self.name, str(self.value))
        
        
        
class Element(Node):
    def __init__(self, name, namespace=None):
        super(Element, self).__init__()
        self.name = name
        self._childs = []
        self.namespace = namespace
        self.xmlns = {}
        
    def add(self, child):
        child.parent = self
        self._childs.append(child)
        
    def __repr__(self):
        return "Element(%s, %s)" % (self.namespace,self.name)
    
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
        attrs = filter(isattribute, self._childs)
        nodes = filter(OR(istext, iselement), self._childs)
            
        if len(attrs) > 0:
            attrs_string = " "+" ".join([ a.render() for a in attrs])
        else:
            attrs_string = ""
        
        if len(nodes) > 0:
            nodes_string = "".join([n.render() for n in nodes])
            return "<%s%s>%s</%s>" %(self.name, attrs_string, nodes_string,self.name)
        else:
            return "<%s%s/>" % (self.name,attrs_string)
        
    def resolve_namespace(self, namespace):
        if self.xmlns.has_key(namespace):
            return self.xmlns[namespace]
        elif self.parent is not None:
            return self.parent.resolve_namespace(namespace)
        
        
def _get_name(node):
    if node.nodeName.count(":")>0:
        namespace, name = node.nodeName.split(":")
        return namespace, name
    else:
        return None, node.nodeName
    
def _parse_attribute(parent, node):
    ns, name = _get_name(node)
    value = node.childNodes[0].nodeValue
    
    full_ns = parent.resolve_namespace(ns)
    if full_ns is None:
        full_ns = ns
        
    attribute = Attribute(name=name, namespace=full_ns, value=value,shortns=ns)
    return attribute
        
def _parse_element(parent, node):
    ns, name = _get_name(node)
    element = Element(name, ns)
    
    #Parse attributes first, as it may contain important name spaces.
    for _,value in node._attrs.iteritems():
        attribute = _parse_attribute(element, value)
        element.add(attribute)
        if attribute.namespace == "xmlns":
            element.xmlns[attribute.name] = attribute.value
                
    for child in node.childNodes:
        if isinstance(child, minidom.Text):
            element.add(Text(child.nodeValue))
        else:
            child_element = _parse_element(element, child)
            element.add(child_element)
        
    
            
    #Unabr namespace, try parent first if this fails try local xmlns.
    if element.namespace is not None:
        fullns = None
        if parent is not None:
            fullns = parent.resolve_namespace(element.namespace)
        if fullns is None:
            fullns = element.xmlns.get(element.namespace)
        if fullns is not None:
            element.namespace = fullns
        
    return element
    
    

    
def parse(xml):
    document = minidom.parseString(xml)
    return _parse_element(None, document.childNodes[0])


# Filters

def OR(*methods):
    def inner(node):
        return any([ method(node) for method in methods])
    return inner

def AND(*methods):
    def inner(node):
        for method in methods:
            if method(node) == False:
                return False
        return True
    return inner

def istext(node):
    return isinstance(node,Text)

def isattribute(node):
    return isinstance(node, Attribute)

def iselement(node):
    return isinstance(node, Element)


def ischildof(parent):
    def inner(node):
        return node.parent==parent
    return inner    

def isnamed(*names):
    def inner(node):
        if not hasattr(node, "name"):
            return False
        for name in names:
            if node.name == name:
                return True
        return False
    return inner

def ns_is(*namespaces):
    def inner(node):
        if not hasattr(node, "namespace"):
            return False
        for namespace in namespaces:
            if node.namespace == namespace:
                return True
        return False
    return inner

def parent_is(method):
    def inner(node):
        return method(node.parent)
    return inner

#Utilities
def one(root, method):
    return filter(root,method)[0]

def delete(node):
    node.delete()

def attribute(element, name):
    return element.filter(AND(isattribute, isnamed(name), ischildof(element)))[0]

def value(node):
    if isinstance(node, Attribute):
        return node.value
    elif isinstance(node, Text):
        return node.value
    elif isinstance(node, Element):
        text_nodes = filter(AND(istext,ischildof(node)), node)
        return "".join( [text.value for text in text_nodes])

def write_to(string, path):
    with open(path,"w") as f:
        f.write(string)
        
def read_from(path):
    with open(path) as f:
        return f.read() 
    


    
        
    