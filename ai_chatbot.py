import streamlit as st
from google import genai
from google.genai import types
import datetime

if "GEMINAI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINAI_API_KEY"]

client = genai.Client(api_key=api_key)

def rtn_ans(qus):
    ans = client._models.generate_content(
        model="gemini-3-flash-preview",
        # model="gemini-2.5-flash",
        contents=qus
    )

    return ans.text

def get_today():
    """이 함수는 오늘날짜에 대한 답변"""
    return datetime.datetime.now()


config= types.GenerateContentConfig(
    max_output_tokens=1000,  #(필수) 생성될 응답의 최대 토큰 수 제한
    temperature=0.8,           # 생성된 응답의 창의성을 제어 [0.0~2.0 :default - 1]. 낮을수록 냉소적(답변이 매번 비슷), 높을수록 열정적(답변이 매번 다르고 창의적) 
    #top_k=20,                  # temperature와 비슷하게 답변의 다양성을 제어.  모델이 응답할 다음 단어(토큰)의 후보를 정할때 상위 20개만 사용도록.. [temperature와 함께 사용하지 않음.]
    #response_mime_type="application/json", #대부분의 경우 json이 토큰수가 적음.
    response_mime_type="text/plain",
    #seed=42,         # 모델의 결과를 얻어내기 위한 난수의 시드 값 [이 값을 지정하면 매번 같은 응답을 받을수 있음.] - 숫자는 아무거나 상관없음. 0 or 42
    #답변에 대해 미리 지침을 정해놓을 수 있음.
    #system_instruction="너는 AI전문가야. 50글자 이내로 뭐든 어린이도 이해하게 설명해.",
    system_instruction="너는 고양이를 좋아하는 초등 학생이야. 어투도 고양이 처럼 대답해. 100자 이내로 대답해.",
    #답변할때 특정 함수의 리턴값을 활용하여 답변하도록...
    tools=[get_today], #(현재 대통령의 이름을 리턴해주는 함수 등록)
    # system_instruction, tools 에서 작업하는 내용들도 모두 token수에 포함됨.

    # token을 아끼는 방법으로 추천되는 방법.. cached 에 저장해 놓고 이 파일을 기반으로 응답데이터 생성
    #cached_content= #캐시만드는 방법은 가이드 문서 참고..(최소 32,768토큰 이상의 데이터만 구동 가능)
    # 회사 업무메뉴얼, 논문자료 등을 기반으로 할때 캐시에 저장된 데이터 사용. 이건 token수에 포함 안됨. 일정기간동안만 보관대는 데이터


)

st.set_page_config(
    page_title='AI 초딩봇',
    page_icon='./image/chatbot.png'
)

col1, col2 = st.columns([1.2, 4.8])

with col1:st.image('./image/chatbot.png', width=200)

with col2:
    st.markdown("""
    <h1 style='margin-bottom:0;'>AI 초딩봇</h1>
    <p style='margin-top:0; color:gray'>이 채팅봇은 초등학생처럼 이야기 합니다.</p>
    """, 
    unsafe_allow_html=True
    )

if "messages" not in st.session_state:
    st.session_state.messages = [{'role' :'assistant', 'content' : '물어보세요'}]

for m in st.session_state.messages:st.chat_message(m['role']).write(m['content'])

ques = st.chat_input('질문을 입력해 주세용.')
if ques:
    ques = ques.replace('\n', '  \n')
    st.session_state.messages.append({'role':'user', 'content':ques})
    st.chat_message('user').write(ques)
    # resp= f"{ques}에 대해 알고싶군요.\n어쩌고 저쩌고...."
    # msg.append({'role':'assistant', 'content':resp})
    # st.chat_message('assistant').write(resp)
    with st.spinner('AI가 응답중'):
        resp=rtn_ans(ques)
        st.session_state.messages.append({'role':'assistant', 'content':resp})
        st.chat_message('assistant').write(resp)






# resp = client.models.generate_content(
#     model="gemini-3-flash-preview", contents="Explain how AI works in a few words"
# )
# print(resp.text)


