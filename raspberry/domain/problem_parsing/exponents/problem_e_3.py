# 제곱근 계산

#\sqrt{\sqrt{{3}^{4}}} = ?
#\sqrt{{2}^{12}} = ?



def text_parsing(pb):
	if pb[1]=='(':
		return pb[2:][:-2]
	else:
		return pb[1:][:-1]

def ax_b(text):
     
	spl = text.split("x")
	#print(f"spl : {spl}, text : {text}")
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


def number_parsing(pb):
	if pb[1]=='(':
		return int(pb[2:][:-2])
	else:
		return int(pb[1:][:-1])

def data_extract_e_1(text):
    # {'id': 23944, 'category': '지수 함수 값 계산하기', 'problem': '{(-2)}^{4} = ?', 'problem_answer': '16', 'user_answers': 'ac', 'record_id': 2104}

    pb=text
    pb=pb.split(' = ')[0]
    pb=pb.split('^')
    
    return [number_parsing(pb[0]),number_parsing(pb[1])]

        

def a_n(text):
	
	texts=text.split('^')
	return text_parsing(texts[0]),text_parsing(texts[1])

def data_extract(text):
    
    #print("-"*10)
    #print(text)
    
    pb=text
    pb = pb.split(' = ')[0]
    pb = pb.split('\\sqrt')
    #print("pb")
    #print(pb)
    stack=[]
    # '\\sqrt[4]{\\sqrt[4]{{2}^{16}}}
    # {{2}^{16}}}
    for i in range(1,len(pb)-1):
        text=pb[i]
        #print(i,text)
        if text[0]=='[':
            stack.append(int(text.split("[")[1].split("]{")[0]))
        else:
            stack.append(2)
            
    last_text=pb[len(pb)-1].split("]")
    if len(last_text)>1:
        stack.append(int(last_text[0][1:]))
        stack+=data_extract_e_1(last_text[1][1:-(len(pb)-1)])
    else:
        stack.append(2)
        stack+=data_extract_e_1(last_text[0][1:-(len(pb)-1)])
    
    
    
    return stack  
    
    
#print(data_extract("\sqrt{\sqrt{{3}^{4}}} = ?"))
#print(data_extract("\sqrt{{2}^{12}} = ?"))
#print(data_extract("\sqrt{\sqrt{\sqrt[4]{{3}^{24}}}} = ?"))


# 3 ~ 5개
def data_bundles():
    return [[-2,-1]] # index, 뒤에 2개 조합, 나머지랑 인덱스 조합