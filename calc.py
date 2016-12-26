import re
import operator

outlist=[];
stack=[]

def calculate(expr):
	global outlist
	global stack
	outlist=[]
	stack=[]
	#remove space
	expr="".join(expr.split())
	valid,msg=evaluate(expr)
	if not valid:
		# print "Invalid expression : "+msg
		raise Exception("Invalid expression : "+msg)
	expr=preprocess(expr)
	expr=tokenize(expr)
	print 'tokens',expr
	for token in expr:
		if isinstance(token,float):
			outlist.append(token)
		elif is_operator(token):
			while not is_greater_prior(token):
				outlist.append(stack[-1])
				del stack[-1]
			stack.append(token)
		elif token=='(':
			stack.append(token)
		elif token==')':
			while stack[-1]!='(':
				outlist.append(stack[-1])
				del stack[-1]
			del stack[-1]#discarding '('
	outlist+=stack[::-1]
	# print outlist

	try:
		while len(outlist)>1:
			for index,token in enumerate(outlist):
				if token in ('+','-','*','/','^'):
					i=index
					oper=token
					break
			operations={
			'+':operator.add,
			'-':operator.sub,
			'*':operator.mul,
			'/':operator.div,
			'^':operator.pow
			}
			res=reduce(operations[oper],(outlist[i-2],outlist[i-1]))
			del outlist[i-2]
			del outlist[i-2]
			outlist[i-2]=res
	except Exception as e:
		if 'OverflowError' in str(e):
			print 'The expression produces huge number that cannot be handled by this program'
			return 0
	if len(outlist)>1:
		raise Exception("len(outlist)!=1");
	return outlist[0]

def preprocess(expr):
	expr=expr.strip()
	#correct brackets
	bcounter=0
	for char in expr:
		if char=='(':
			bcounter+=1
		elif char==')':
			bcounter-=1
	if bcounter>0:
		expr+=')'*bcounter

	li=list(expr)
	imax=len(li)-1
	i=0
	while i < imax:
		#insert star
		if ( li[i].isdigit() or li[i]==')' ) and li[i+1]=='(':
			li.insert(i+1,'*')
			imax=len(li)-1
		elif li[i]==')' and ( li[i+1].isdigit() or li[i+1]=='(' ):
			li.insert(i+1,'*')
			imax=len(li)-1
		#convert sign of bracket
		elif li[i]=='-' and li[i+1]=='(':
			li.insert(i+1,'1')
			li.insert(i+2,'*')
			imax=len(li)-1
		i+=1
	# print "* inserted and -( solved:","".join(li)
	return li


def evaluate(expr):
	first=['d','(','-']
	last=['d',')']
	op=re.compile(r'[-+*/^]')
	successor={
		"d" : ['d','.',')','o','(','^'],
		"o" : ['d','-','('],
		"(" : ['d','(','-'],
		')' : ['o','d',')','(','^'],
		'.' : ['d'],
		}
	if expr=="" or expr==None:
		return False,'Empty expression'
	t=expr[0]
	if t.isdigit():
		t='d'
	elif op.match(t) and t!='-':
		t='o'
	if t not in first:
		return False,'invalid first character'
	
	t=expr[-1]
	if t.isdigit():
		t='d'
	elif op.match(t):
		t='o'
	if t not in last:  
		return False,'invalid ending character'

	bcounter=0
	for i in xrange(0,len(expr)-1):
		t1=expr[i]
		first=t1
		t2=expr[i+1]
		second=t2
		
		if t1=='(':bcounter+=1
		elif t1==')':bcounter-=1

		if bcounter<0:return False,'closing unopened brackets?'

		if t1.isdigit():t1='d'
		elif op.match(t1):t1='o'
		
		if t2.isdigit():t2='d'
		elif op.match(t2):t2='o'
		
		if t2 not in successor[t1] and second not in successor[t1]:
			return False,t1+' or '+first+' cannot be followed by '+t2+' or '+second

	if expr[-1]=='(':bcounter+=1
	elif expr[-1]==')':bcounter-=1
	if bcounter<0:return False,'closing unopened brackets?'

	return True,'correct'


def tokenize(li):
	tokens=[]
	imax=len(li)
	i=0
	while i<imax:
		#- is sign when
			 # first is -
			 # (-
			 # operator-
		if li[i].isdigit() or ( li[i]=='-' and (i==0 or li[i-1]=='(' or is_operator(li[i-1]))):
			j=1
			while i+j<imax and (li[i+j].isdigit() or li[i+j]=='.'):
				j+=1
			num=float("".join(li[i:i+j]))
			tokens.append(num)
			i=i+j
		else:
			tokens.append(li[i])
			i+=1
	return tokens


def is_operator(char):
	return char in ['+','-','*','/','^']

def is_greater_prior(oper):
	if len(stack)<1:
		return True
	greaters={
	'+':['*','/','^'],
	'-':['*','/','^'],
	'*':['^'],
	'/':['^'],
	'^':[],
	'(':['+','-','*','/','^']
	}
	return oper in greaters[stack[-1]]

# print calculate(raw_input("Enter a mathematical expression:"))
# print calculate('7*(8+2*(2+7')
# print eval('1+2.2*3^(4^5)/(6+-7)')
print calculate('1+2.2*3^(4^5)/(6+-7)')
print eval('1+2.2*3^(4^5)/(6+-7)')
