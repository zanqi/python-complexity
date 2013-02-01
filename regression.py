# Routines to help in timing the execution of
# various code fragments or routines, and to
# infer a good formula for the resulting runtimes.

import math
import scipy.linalg
import string
import sys
import timeit

def make_input_list(input_spec,growth_factor):
    """
    Generate a list of dictionaries that each has an instance of
    input value(s) within the given range.
    Each range's upper and lower value is a *string* that can be evaluted;
    each string may depend on earlier variable values 
    Values increment by factor of growth_factor from min to max
    Example:
       make_input_list("1<=n<=1000", 10) 
         returns [{n:1},{n:10},{n:100}...]
       make_input_list("1<=n<=1000;1<=m<=1000;min(n,m)<=k<=max(n,m)", 10)
         returns [{n:1,m:1,k:1},{n:1,m:10,k:1},{n:1,m:10,k:10}...]
    """
    def lg(x):
        return math.log(x, 2)

    var_list = []
    spec_list = string.split(input_spec,";")
    D = {}
    D['lg'] = lg
    D['sqrt'] = math.sqrt
    D_list = [D]
    for input_range in spec_list:
        spec_parts = string.split(input_range,"<=")
        assert len(spec_parts)==3
        lower_spec = spec_parts[0]
        var_name = spec_parts[1]
        upper_spec = spec_parts[2]

        assert len(var_name)==1
        var_list.append(var_name)

        new_D_list = []
        for D in D_list:
            val = eval(lower_spec,D)
            while val <= eval(upper_spec,D):
                new_D = D.copy()
                new_D[var_name] = val
                new_D_list.append(new_D)
                val *= growth_factor
        D_list = new_D_list
    # for D in D_list: print D
    return (var_list,D_list)

def fit(var_list,input_list,run_times,f_list):
    """
    Perform least-squares fit: x*f(input) = run_time.
    Given:
        list of variable names
        list of sample dicts for various parameter sets
        list of corresponding run times
        list of functions to be considered for fit
            these are *strings*, e.g. "n","n**2","min(n,m)",etc.
    prints:
        coefficients for each function in f_list
    """
    print "var_list",var_list
    print "Function list:",f_list
    print "run times:",
    for i in range(len(input_list)):
        print
        for v in var_list:
            print v,"= %6s"%input_list[i][v],
        print ": %8f"%run_times[i],"microseconds",
        # print "  n = %(n)6s"%input_list[i],run_times[i],"microseconds"
    print
    rows = len(run_times)
    cols = len(f_list)
    A = [ [0 for j in range(cols)] for i in range(rows) ]
    for i in range(rows):
        D = input_list[i]
        for j in range(cols):
            A[i][j] = float(eval(f_list[j],D))
    b = run_times
    # print "A:"
    # print A
    # print "b:"
    # print b

    # (x,resids,rank,s) = scipy.linalg.lstsq(A,b)
    (x,resids,rank,s) = fit2(A,b)

    print "Coefficients trained by the data:"
    for j in range(cols):
        sign = ''
        if x[j]>0 and j>0: 
            sign="+"
        elif x[j]>0:
            sign = " "
        print "%s%g*%s"%(sign,x[j],f_list[j])

    print "(measuring time in microseconds)"
    print "Sum of squares of residuals:", resids
    print "RMS error = %0.2g percent"%(math.sqrt(resids/len(A))*100.0)
    # print "Rank:",rank
    # print "SVD:",s
    sys.stdout.flush()
    
import scipy.optimize

def fit2(A,b):
    """ Relative error minimizer """
    def f(x):
        assert len(x) == len(A[0])
        resids = []
        for i in range(len(A)):
            sum = 0.0
            for j in range(len(A[0])):
                sum += A[i][j]*x[j]
            relative_error = (sum-b[i])/b[i]
            resids.append(relative_error)
        return resids
    ans = scipy.optimize.leastsq(f,[0.0]*len(A[0]))
    x = ans[0]

    sum_square_resids = sum(r*r for r in f(x))
    return (x,sum_square_resids,0,0)

def test_misc():
    print
    print "Test Misc-1: running time should be n+2*m+7+3*n*lg(n)+17*n*m"
    spec_string = "1<=n<=100000;1<=m<=100000"
    growth_factor = 10
    print "Spec_string: ",spec_string,"by factors of",growth_factor
    var_list,input_list = make_input_list(spec_string,growth_factor)
    run_times = [ eval("n+2*m+7+3*n*lg(n)+17*n*m",D) for D in input_list ]
    f_list = ("(n*m)","n**2","n*lg(n)","n","m","1")
    fit(var_list,input_list,run_times,f_list)

    test("Test Misc-2: pass", 
        "10000<=n<=1000000",
        "",
        "pass",
        ("1",),
        1000)

def test_number():
    test("Test Number-1: time to compute int('1'*n)", 
        "1000<=n<=10000",
        "import string;x='1'*%(n)s",
        "int(x)",
        ("n**2",),
        1000)

    test("Test Number-2: time to compute repr(2**n)", 
        "1000<=n<=10000",
        "x=2**%(n)s",
        "repr(x)",
        ("n**2",),
        1000)

    print
    print "Test Number-3 -- time to convert (2**n) to hex"
    spec_string = "1000<=n<=100000"
    growth_factor = 2
    print "Spec_string: ",spec_string,"by factors of",growth_factor
    var_list, input_list = make_input_list(spec_string,growth_factor)
    # f_list = ("n**2","n","1")
    f_list = ("n",)
    run_times = []
    trials = 1000
    for D in input_list:
        t = timeit.Timer("'%x'%x","x=2**%(n)s"%D)
        run_times.append(t.timeit(trials)*1e6/float(trials))
    fit(var_list,input_list,run_times,f_list)

    test("Test Number-4: time to add 2**n to itself", 
        "1000<=n<=1000000",
        "x=2**%(n)s",
        "x+x",
        ("n",),
        10000)

    test("Test Number-5: time to multiply (2**n/3) by itself", 
        "1000<=n<=100000",
        "x=(2**%(n)s)/3",
        "x*x",
        ("n**1.585",),
        1000)

    test("Test Number-6: time to divide (2**(2n) by (2**n))", 
        "1000<=n<=50000",
        "w=(2**(2*%(n)s));x=(2**(%(n)s))",
        "w/x",
        ("n**2",),
        1000)

    print
    print "Test Number-7 -- time to compute remainder of (2**(2n) by (2**n))"
    spec_string = "1000<=n<=50000"
    growth_factor = 2
    print "Spec_string: ",spec_string,"by factors of",growth_factor
    var_list,input_list = make_input_list(spec_string,growth_factor)
    # f_list = ("n**2","n*lg(n)","n","1")
    f_list = ("n**2",)
    run_times = []
    trials = 1000
    for D in input_list:
        t = timeit.Timer("w%x","w=(2**(2*%(n)s));x=(2**(%(n)s))"%D)
        run_times.append(t.timeit(trials)*1e6/float(trials))
    fit(var_list,input_list,run_times,f_list)

    test("Test Number-8: time to compute pow(x,y,z)", 
        "1000<=n<=5000",
        "z=(2**%(n)s)+3;x=y=(2**%(n)s)+1",
        "pow(x,y,z)",
        ("n**3",),
        10)

    test("Test Number-9: time to compute 2**n", 
        "1000<=n<=1000000",
        "",
        "2**%(n)s",
        ("1",),
        10000)

def test_string():
    test("Test String-1: extract a byte from a string", 
        "1000<=n<=1000000",
        "s='0'*%(n)s",
        "s[500]",
        ("1",),
        1000)

    test("Test String-2: concatenate two string of length n", 
        "1000<=n<=500000",
        "s=t='0'*%(n)s",
        "s+t",
        ("n",),
        1000)

    test("Test String-3: extract a string of length n/2", 
        "1000<=n<=500000",
        "s='0'*%(n)s",
        "s[0:%(n)s/2]",
        ("n",),
        1000)

    test("Test String-4: translate a string of length n", 
        "1000<=n<=500000",
        "s='0'*%(n)s;import string;T=string.maketrans('1','2')",
        "string.translate(s,T)",
        ("n",),
        1000)

def test_list():
    test("Test List-1: create an empty list", 
        "1<=n<=10",
        "",
        "x = list()",
        ("1",),
        1000)

    test("Test List-2: list (array) lookup", 
        "10000<=n<=1000000",
        "L=[0]*%(n)s",
        "x=L[5]",
        ("1",),
        1000)

    test("Test List-3: appending to a list of length n", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "L.append(0)",
        ("1",),
        1000)

    test("Test List-4: Pop", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "L.pop()",
        ("1",))

    test("Test List-5: concatenating two lists", 
        "1000<=n<=100000;1000<=m<=100000",
        "L=[0]*%(n)s;M=[0]*%(m)s",
        "L+M",
        ("n", "m"))

    test("Test List-6: extending a length m list", 
        "1000<=n<=100000;1000<=m<=100000",
        "L=[0]*%(n)s;M=[0]*%(m)s",
        "L.extend(M)",
        ("m",))

    test("Test List-7: extracting a slice of length n/2", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "L[0:%(n)s/2]",
        ("n",))

    test("Test List-8: copy", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "L[:]",
        ("n",))

    test("Test List-8: copy", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "L[:]",
        ("n",))

    test("Test List-9: assigning a slice of length n/2", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "L[0:%(n)s/2]=L[1:1+%(n)s/2]",
        ("n",))

    test("Test List-10: Delete first", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "del L[0]",
        ("n",))

    test("Test List-11: Reverse", 
        "1000<=n<=100000",
        "L=[0]*%(n)s",
        "L.reverse()",
        ("n",))

    test("Test List-12: Sort", 
        "1000<=n<=100000",
        "import random;L=[random.random() for i in range(%(n)s)]",
        "L.sort()",
        ("n*lg(n)",))

def test_dict():
    test("Test Dict-1: create an empty dictionary", 
        "1<=n<=1",
        "",
        "x = dict()",
        ("1",),
        1000)

    test("Test Dict-2: dictionary lookup", 
        "1000<=n<=100000",
        "d = dict([(i,i) for i in range(%(n)s)])",
        "x = d[1]",
        ("1",),
        1000)

    test("Test Dict-3: dictionary copy", 
        "1000<=n<=100000",
        "d = dict([(i,i) for i in range(%(n)s)])",
        "d.copy()",
        ("n",),
        1000)

    test("Test Dict-4: dictionary list items", 
        "1000<=n<=100000",
        "d = dict([(i,i) for i in range(%(n)s)])",
        "d.items()",
        ("n*lg(n)",),
        1000)

def test_set():
    test("Test Set-1: create an empty set", 
        "1<=n<=10",
        "",
        "S = set()",
        ("1",),
        1000)

    test("Test Set-2: adding to a set of length n", 
        "10000<=n<=1000000",
        "S=set(range(%(n)s))",
        "S.add(0)",
        ("1",))

    test("Test Set-3: pop", 
        "1000<=n<=100000",
        "S=set(range(%(n)s))",
        "S.pop()",
        ("1",))

    test("Test Set-4: intersect", 
        "1000<=n<=100000;1000<=m<=100000;min(n,m)<=k<=min(n,m)",
        "S=set(range(%(n)s));S2=set(range(%(m)s))",
        "S & S2",
        ("k",))

    test("Test Set-5: union", 
        "1000<=n<=100000;1000<=m<=100000",
        "S=set(range(%(n)s));S2=set(range(%(n)s,%(n)s+%(m)s))",
        "S | S2",
        ("n","m"))

def test(name, spec_string, setup, method, features, trials = 200):
    print
    print name + ": " + method
    growth_factor = 2
    print "Spec_string: ",spec_string, "by factors of", growth_factor
    var_list, input_list = make_input_list(spec_string,growth_factor)
    run_times = []
    for D in input_list:
        t = timeit.Timer(method % D, setup % D)
        run_times.append(t.timeit(trials)*1e6/float(trials))
    fit(var_list,input_list,run_times,features)

def main():
    test_misc()
    test_number()
    test_string()
    test_list()
    test_dict()
    test_set()

if False:
    import profile
    profile.run("main()")
else:
    main()
