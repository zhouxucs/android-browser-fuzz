import tornado.ioloop
import tornado.web
import random
import os

TYPEDARRAY_TYPES = ['Array', 'Int8Array', 'Uint8Array', 'Uint8ClampedArray', 'Int16Array', 'Uint16Array', 'Int32Array', 'Uint32Array', 'Float32Array', 'Float64Array']

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        page = generate_page()
        self.write(page)

def make_app():
    return tornado.web.Application([
        (r"/fuzzyou", MainHandler),
    ])

def rand_num():
    divisor = random.randrange(0x8) + 1
    dividend = (0x100000000) / divisor
    if random.randrange(3) == 0:
        addend = random.randrange(10)
        addend -= 5
        dividend += addend
    return dividend

def generate_assignment():
    vtype = random.choice(TYPEDARRAY_TYPES)
    return "var arr2 = new %s(arr1);" % vtype

def generate_var():
    vtype = random.choice(TYPEDARRAY_TYPES)
    vlen = rand_num()
    return "var arr1 = new %s(%d); " % (vtype, vlen)

def generate_js():
    js = ""
    js += "   try { " + generate_var() + " } catch(e) {console.log(e)} "

    js += "   try { " + generate_assignment() + " } catch(e){ console.log(e)} "
    return js

def generate_page():
    js = generate_js()
    page = """
<html>
<script>
%s
</script>
</html>
""" % js
    return page

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
