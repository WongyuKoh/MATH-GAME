# 식을 만족하는 x 값 찾기

def text_parsing(pb):
	if pb[1]=='(':
		return pb[2:][:-2]
	else:
		return pb[1:][:-1]

def ax_b(text):
     
	spl = text.split("x")
	print(f"spl : {spl}, text : {text}")
	last_v=0

	if len(spl)==1 and spl[0]==text:
		return [0,last_v]

	if spl[1]=='':
		last_v=0
	else:
		last_v=int(spl[1].replace("-","").replace("+",""))

	if spl[0]=='':
		return [1,last_v]

	if spl[0]=='-':
		return [-1,last_v]

	#print(spl)
	return [int(spl[0]),last_v]


def a_n(text):
	
	texts=text.split('^')
	return text_parsing(texts[0]),text_parsing(texts[1])

def data_extract(text):
    
	pb=text
	pb=pb.split(' \\\\ ')[0]
	pbs = pb.split(' = ')


	equation1=a_n(pbs[0])
	equation2=a_n(pbs[1])
 
 
 
	AxB1=ax_b(equation1[1])
	AxB2=ax_b(equation2[1])
 
	return_list=[int(equation1[0])]+AxB1+AxB2

	return return_list


# 5개
def data_bundles():
    return [[0,1],[2,4]] # index