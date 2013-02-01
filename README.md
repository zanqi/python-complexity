Python Running Time Complexity
================================

Python is a high-level programming language, with many powerful primitives. Analyzing the running time of a Python program requires an understanding of the cost of the various Python primitives.

For example, in Python, you can write:  
`L = L1 + L2`  
where L, L1, and L2 are lists; the given statement computes L as the concatenation of the two input lists L1 and L2. The running time of this statement will depend on the lengths of lists L1 and L2. (The running time is more-or-less proportional to the sum of those two lengths.) In comparison:  
`L = L1.extend(L2)`  
its runing time only depend on the length of L2. If L1 is much larger and can be modified, this is more efficient.

The goal of this project is to review various Python primitive operations, and to determine bounds and/or estimates on their running times. My approach will involve both a review of the relevant Python implementation code, and also some experimentation (analysis of actual running times and fitting a nice curve through the resulting data points).

The Python implementation code base is [here](http://hg.python.org/cpython).

Python Running Time Experiments and Discussion
----------------------------------------------
The running times for various-sized inputs were measured, and then a least-squares fit was used to find the coefficient for the high-order term in the running time. (Which term is high-order was determined by some experimentation; it could have been automated...)

The least-squares fit was designed to minimize the sum of squares of relative error, using scipy.optimize.leastsq.

(Earlier version of this program worked with more than the high-order term; they also found coefficients for lower-order terms. But the interpolation routines tended to be poor at distinguishing n and n lg n. Also, it was judged to be more interesting to work with relative error than with absolute error. Finally, it seemed that looking at only the high-order term, and studying only the relative error, seemed simplest.)

The machine used was an Windows 7 64bit with a 2.40GHz Quad processor and 6.0GB RAM.

The regression code itself is here: [regression.py](https://github.com/zanqi/python-complexity/blob/master/regression.py). Sample output from this code is here: [output.txt](https://github.com/zanqi/python-complexity/blob/master/output.txt). (This output may have results somewhat different than in the charts below, due to random run-time variations...)

Cost of Python Integer Operations
----------------------------------------------
<table>
<caption>
<tt>x,y, and z are n-bit numbers</tt><br />
<tt>w is an 2n-bit number</tt><br />
<tt>s is an n-digit string</tt>
</caption>
<tr>
<td> <b>Convert string to integer</b>
</td><td> <tt>int(s)</tt>
</td><td> <tt>84 * (n/1000)^2 microseconds</tt>
</td><td> <tt> n &lt;= 8000</tt>
</td><td> 6% rms error
</td></tr>
<tr>
<td> <b>Convert integer to string</b>
</td><td> <tt>str(x)</tt>
</td><td> <tt>75 * (n/1000)^2 microseconds</tt>
</td><td> <tt> n &lt;= 8000</tt>
</td><td> 3% rms error
</td></tr>
<tr>
<td> <b>Convert integer to hex</b>
</td><td> <tt>"%x"%x</tt>
</td><td> <tt>2.7 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000</tt>
</td><td> 19% rms error
</td></tr>
<tr>
<td> <b>Addition (or Subtraction)</b>
</td><td> <tt>x+y</tt>
</td><td> <tt>0.75 * (n/1000) microseconds</tt>
</td><td> <tt>n &lt;= 512000</tt>
</td><td> 8% rms error
</td></tr>
<tr>
<td> <b>Multiplication</b>
</td><td> <tt>x*y</tt>
</td><td> <tt>13.73 * (n/1000)^1.585 microseconds</tt>
</td><td> <tt>n &lt;= 64000</tt>
</td><td> 10% rms error
</td></tr>
<tr>
<td> <b>Division (or Remainder)</b>
</td><td> <tt>w/x or w%x</tt>
</td><td> <tt>47 * (n/1000)^2 microseconds</tt>
</td><td> <tt> n &lt;= 32000 </tt>
</td><td> 6% rms error
</td></tr>
<tr>
<td> <b>Modular Exponentiation</b>
</td><td> <tt>pow(x,y,z)</tt>
</td><td> <tt>60000 * (n/1000)^3 microseconds</tt>
</td><td> <tt> n &lt;= 4000 </tt>
</td><td> 8% rms error
</td></tr>
<tr>
<td> <b>n-th power of two</b>
</td><td> <tt>2**n</tt>
</td><td> <tt>0.06 microseconds</tt>
</td><td> <tt> n &lt;= 512000 </tt>
</td><td> 10% rms error
</td></tr></table>
It is perhaps curious that multiplication is implemented using Karatsuba's algorithm, giving an Θ(<i>n</i><sup>lg3</sup>) running time, while division uses an Θ(<i>n</i><sup>2</sup>) algorithm.

Cost of Python String Operations
----------------------------------------------
<table>
<caption>
<tt>s and t are length-n strings</tt><br>
<tt>u is length (n/2)</tt>
</caption>
<tbody><tr>
<td> <b>Extract a byte from a string</b>
</td><td> <tt>s[i]</tt>
</td><td> <tt>0.13 microseconds</tt>
</td><td> <tt> n &lt;= 512000</tt>
</td><td> 29% rms error
</td></tr>
<tr>
<td> <b>Concatenate</b>
</td><td> <tt>s+t</tt>
</td><td> <tt>1 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 256000 </tt>
</td><td> 19% rms error
</td></tr>
<tr>
<td> <b>Extract string of length n/2</b>
</td><td> <tt>s[0:n/2]</tt>
</td><td> <tt>0.3 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 256000 </tt>
</td><td> 28% rms error
</td></tr>
<tr>
<td> <b>Translate a string</b>
</td><td> <tt>s.translate(s,T)</tt>
</td><td> <tt>3.2 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 256000 </tt>
</td><td> 11% rms error
</td></tr></tbody></table>

Cost of Python List Operations
----------------------------------------------
<table>
<caption>
<tt>L is length-n list</tt><br>
<tt>M is length-m lists</tt><br>
<tt>P has length n/2</tt>
</caption>
<tbody><tr>
<td> <b>Create an empty list</b>
</td><td> <tt>list()</tt>
</td><td> <tt>0.40 microseconds</tt>
</td><td> <tt>(n=1)</tt>
</td><td> .5% rms error
</td></tr>
<tr>
<td> <b>Access</b>
</td><td> <tt>L[i]</tt>
</td><td> <tt>0.10 microseconds</tt>
</td><td> <tt> n &lt;= 640000</tt>
</td><td> 3% rms error
</td></tr>
<tr>
<td> <b>Append</b>
</td><td> <tt>L.append(0)</tt>
</td><td> <tt>0.24 microseconds</tt>
</td><td> <tt> n &lt;= 640000</tt>
</td><td> 3% rms error
</td></tr>
<tr>
<td> <b>Pop</b>
</td><td> <tt>L.pop()</tt>
</td><td> <tt>0.25 microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 0.5% rms error
</td></tr>
<tr>
<td> <b>Concatenate</b>
</td><td> <tt>L+M</tt>
</td><td> <tt>7 * (n+m/1000) microseconds</tt>
</td><td> <tt> n,m &lt;= 64000 </tt>
</td><td> 17% rms error
</td></tr>
<tr>
<td> <b>Extend</b>
</td><td> <tt>L.extend(M)</tt>
</td><td> <tt>65 * (m/1000) microseconds</tt>
</td><td> <tt> m &lt;= 64000 </tt>
</td><td> 11% rms error
</td></tr>
<tr>
<td> <b>Slice extraction</b>
</td><td> <tt>L[0:n/2]</tt>
</td><td> <tt> 5.4 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000</tt>
</td><td> 4% rms error
</td></tr>
<tr>
<td> <b>Copy</b>
</td><td> <tt>L[:]</tt>
</td><td> <tt> 11.5 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 10% rms error
</td></tr>
<tr>
<td> <b>Slice assignment</b>
</td><td> <tt>L[0:n/2] = P</tt>
</td><td> <tt> 11 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 4% rms error
</td></tr>
<tr>
<td> <b>Delete first</b>
</td><td> <tt>del L[0]</tt>
</td><td> <tt> 1.7 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 4% rms error
</td></tr>
<tr>
<td> <b>Reverse</b>
</td><td> <tt>L.reverse()</tt>
</td><td> <tt> 1.3 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 10% rms error
</td></tr>
<tr>
<td> <b>Sort</b>
</td><td> <tt>L.sort()</tt>
</td><td> <tt> 0.0039 * n lg(n) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 12% rms error
</td></tr></tbody></table>
The **first** time one appends to a list, there is additional cost as the list is copied over and extra space, about 1/8 of the list size, is added to the end. Whenever the extra space is used up, the list is re-allocated into a new array with about 1.125 the length of the previous version.

Cost of Python Dictionary Operations
----------------------------------------------
<table>
<caption>
<tt>D is a dictionary with n items</tt><br>
</caption>
<tbody><tr>
<td> <b>Create an empty dictionary</b>
</td><td> <tt>dict()</tt>
</td><td> <tt>0.36 microseconds</tt>
</td><td> <tt>(n=1)</tt>
</td><td> 0% rms error
</td></tr>
<tr>
<td> <b>Access</b>
</td><td> <tt>D[i]</tt>
</td><td> <tt>0.12 microseconds</tt>
</td><td> <tt> n &lt;= 64000</tt>
</td><td> 3% rms error
</td></tr>
<tr>
<td> <b>Copy</b>
</td><td> <tt>D.copy()</tt>
</td><td> <tt> 57 * (n/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 27% rms error
</td></tr>
<tr>
<td> <b>List items</b>
</td><td> <tt>D.items()</tt>
</td><td> <tt>0.0096 * n lg(n) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 14% rms error
</td></tr></tbody></table>
What should the right high-order term be for copy and list items? It seems these should be linear, but the data for both looks somewhat super-linear. I've modelled copy here as linear and list items as n lg(n), but these formular need further work and exploration.

Cost of Python Set Operations
----------------------------------------------
<table>
<caption>
<tt>S is length-n sets</tt><br>
<tt>M is length-m sets</tt>
</caption>
<tbody><tr>
<td> <b>Create an empty set</b>
</td><td> <tt>list()</tt>
</td><td> <tt>0.17 microseconds</tt>
</td><td> <tt>(n=1)</tt>
</td><td> 0.8% rms error
</td></tr>
<tr>
<td> <b>Add</b>
</td><td> <tt>S.add(0)</tt>
</td><td> <tt>0.14 microseconds</tt>
</td><td> <tt> n &lt;= 640000</tt>
</td><td> 4% rms error
</td></tr>
<tr>
<td> <b>Pop</b>
</td><td> <tt>S.pop()</tt>
</td><td> <tt>0.12 microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 7.7% rms error
</td></tr>
<tr>
<td> <b>Intersection</b>
</td><td> <tt>S & M</tt>
</td><td> <tt>80 * (min(n,m)/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 18% rms error
</td></tr>
<tr>
<td> <b>Union</b>
</td><td> <tt>S | M</tt>
</td><td> <tt>50 * ((n + m)/1000) microseconds</tt>
</td><td> <tt> n &lt;= 64000 </tt>
</td><td> 36% rms error
</td></tr></tbody></table>
Set is implemented as hash, so checking if element is in a set is constant time.
