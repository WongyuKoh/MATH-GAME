# 지수 함수 값 계산하기

def number_parsing(pb):
	if pb[1]=='(':
		return int(pb[2:][:-2])
	else:
		return int(pb[1:][:-1])

def data_extract(text):
    # {'id': 23944, 'category': '지수 함수 값 계산하기', 'problem': '{(-2)}^{4} = ?', 'problem_answer': '16', 'user_answers': 'ac', 'record_id': 2104}

    pb=text
    pb=pb.split(' = ')[0]
    pb=pb.split('^')
    
    return [number_parsing(pb[0]),number_parsing(pb[1])]

        