from nhfx.xquery import *

ops = parse(read_from("ops.xml"))

print one(isnamed("aircraft"),ops)
print filter(ns_is("http://flightdataservices.com/ops.xsd"), ops)
print filter(isattribute, ops)