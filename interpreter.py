from parse import SyntaxTree
data = '''
    fun fact(x,y){
     z = x+y;
     send z
    }
    fun seen(z){
     z=2;
     send z
    }
    var hello=y;
    var forget;
    hello = x>y || x<y;
    if hello+3 > 5+4 || forget
    {
        var x = 3
        var y = true;
    }
    elif y==3
    {
        while z==3
        {
            x++;
            y++;
            out("hello", x+y);
        }
    }
'''
builder = SyntaxTree()
builder.build(data)
