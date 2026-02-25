# streamlit run ai_chatbot.py
import streamlit as st
from google import genai
from google.genai import types
import datetime
import json

if "GEMINAI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINAI_API_KEY"]

client = genai.Client(api_key=api_key)

def get_today():
    """이 함수는 오늘날짜에 대한 답변"""
    return datetime.datetime.now()

def get_who():
    """이 함수는 챗봇에 대해 물어보는 대답에 대한 답변"""
    info={'이름':'사랑이', '생일':'2016년 3월 3일', '좋아하는 음식':'아이스크림 케이크 초콜렛',
          '사는 곳':'서울 동작구 사당동', '학교':'삼일조'}
    return json.dumps(info, ensure_ascii=False)

config= types.GenerateContentConfig(
    max_output_tokens=300, 
    temperature=0.9,
    response_mime_type="text/plain",
    system_instruction="너는 초등 학생이야. 어투도 귀엽게 대답해. 잘 모르는 것이나 어려운 것은 모른 다고 대답해.5초 이내로 대답해.",
    tools=[get_today, get_who],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="ANY", 
            allowed_function_names=["get_who"]
        )
    ),
)

def rtn_ans(qus):
    ans = client._models.generate_content(
        # model="gemini-3-flash-preview",
        model="gemini-2.5-flash",
        contents=qus,
        config= config
    )

    return ans.text

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

ques = st.chat_input('질문을 입력해 주세여.')
if ques:
    ques = ques.replace('\n', '  \n')
    st.session_state.messages.append({'role':'user', 'content':ques})
    st.chat_message('user').write(ques)
    # msg.append({'role':'assistant', 'content':resp})
    # st.chat_message('assistant').write(resp)
    with st.spinner('AI가 응답중'):
        resp=rtn_ans(ques)
        st.session_state.messages.append({'role':'assistant', 'content':resp})
        st.chat_message('assistant').write(resp)

