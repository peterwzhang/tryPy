# team members: Peter Zhang, Madeline Moore, Cara Cannarozzi

# **NOTE: for all examples, variables must be set in the blocks and can be manipulated from there. the blocks do not take user input**
# **NOTE: these examples are geared towards middle schoolers and late elementary schoolers as they will be the users of tryPy**

# example 1
# task: add up all numbers from 1 to 100. try to do this using by going through a loop only 50 times!
x=0
for i in range(50):
    x+=i+(100-i)
x+=50
print(x)
print()

# example 2
# task: check if a number is even or odd! print "odd" if the number is odd or "even" if the number is even
x=13
if x%2==0:
    print("even")
else:
    print("odd")
print()

# example 3
# task: use the base and height of a triangle to calculate its area
base=2
height=3
print(.5*base*height)
print()

# example 4
# task: using the diameter of a circle, calculate its circumference and its area (use 3.14 for pi)
diam=5
print("circumference:")
print(3.14*diam)
print("area:")
rad=diam/2
print(3.14*rad*rad)
print()

# example 5
# task: using a number of your choice, print out all non-negative numbers leading up to it
x=4
for i in range(x+1):
    print(i)
print()

# example 6
# task: using two numbers (a coefficient and an exponent), print the coefficient to the power of the exponent
co=2
exp=5
res=1
for i in range(exp):
    res*=co
print(res)
print()

# example 7
# task: print the absoulute value of a number
x=-17
if x<0:
    print(0-x)
else:
    print(x)
print()

# example 8
# task: print the difference between a given number and 21, if the number is greater than 21 print double the absolute difference
x=44
if x>21:
    print(2*(x-21))
else:
    print(21-x)
print()

# example 9
# task: use a number and a range to check if the number is within the range of 5000 (inclusive). print "yes!" if it is or "no" if it isn't
ran=100
num=4900
if num>=5000-ran and num<=5000+ran:
    print("yes!")
else:
    print("no")
print()

# example 10
# task: print the sum of two numbers, but if the numbers are equal, print 0
x=15
y=15
if x!=y:
    print(x+y)
else:
    print(0)
print()

# example 11
# task: print the square of the sum of two numbers (x+y)^2
x=2
y=3
print((x+y)*(x+y))
print()

# example 12
# task: print the sum of all digits from an integer (ex. 12345 will output 15)
x=12345
sum=0
while x>0:
    sum+=x%10
    x//=10
print(sum)
print()

# example 13
# task: print the future value of a specified principal amount, rate of interest, and a number of years. don't worry about rounding
amt=10000
intr=3.5
yrs=7
intr=1+(intr/100)
for i in range(yrs):
    amt*=intr
print(amt)
print()

# example 14
# task: convert a length in feet and inches to centimeters using inch to centimeter conversion of 2.54 cm/in
ft=5
inch=8
inch+=(12*ft)
print(2.54*inch)
print()

# example 15
# task: convert a temperature in F to C
tempF=72
print((tempF-32)*5/9)
print()

# example 16
# task: check if all digits of an integer are the same (print "all the same" if they are, "at least one difference" if not)
x=6663666
val=x%10
while x>0:
    if x%10!=val:
        print("at least one difference")
        break
    x//=10
if x==0:
    print("all the same")
print()

# example 17
# task: remove and print every third digit from an integer (start from end, move to beginning)
x=123456789
while x!=0:
    for i in range(3):
        if i==2:
            print(x%10)
        x//=10
print()

# example 18
# task: find the median of three numbers
a=12
b=14
c=13
if (a<b and a>c) or (a>b and a<c):
    print(a)
elif (b<a and b>c) or (b>a and b<c):
    print(b)
elif (c<a and c>b) or (c>a and c<b):
    print(c)
elif (a==b or a==c):
    print(a)
elif (b==c):
    print(b)
print()

# example 19
# task: count the number of times a specified digit appears in an integer
key=2
num=98765432123456789
count=0
while num!=0:
    if num%10==key:
        count+=1
    num//=10
print(count)
print()

# example 20
# task: check if three lengths form a valid triangle (print "could be a triangle" if yes, "no triangle here" if no)
a=1
b=1
c=100
if (a+b>c) and (a+c>b) and (b+c>a):
    print("could be a triangle")
else:
    print("no triangle here")
print()


# example 21
# task: print the absolute value of the difference between the first digit and last digit of an integer
x=68342986
last=x%10
while x!=0:
    first=x%10
    x//=10
diff=last-first
if diff<0:
    diff=0-diff
print(diff)
print()

# example 22
# task: print the absolute value of the difference between the smallest digit and largest digit of an integer
x=1239994823653
large=x%10
small=x%10
while x!=0:
    dig=x%10
    if dig>large:
        large=dig
    if dig<small:
        small=dig
    x//=10
diff=large-small
print(diff)
print()

# example 23
# task: from two integers, print the sum of all values between the two numbers (not inclusive)
x=2
y=6
sum=0
for i in range(x+1, y):
    sum+=i
print(sum)
print()

# example 24
# task: check if each digit in an integer is increasing or staying the same
# if there is any decreasing, print "at least one decrease found". otherwise print "all increasing or staying the same"
x=123456789
last=x%10
while x!=0:
    next=x%10
    if next>last:
        print("at least one decrease found")
        break
    last=next
    x//=10
if x==0:
    print("all increasing or staying the same")
print()

# example 25
# task: print the sum of all squares of all digits in an integer (ex. 123=1^2+2^2+3^2=14)
x=12301
sum=0
while x!=0:
    val=x%10
    sum+=val*val
    x//=10
print(sum)
print()