import streamlit as st
import plotly.graph_objects as go
import json

st.set_page_config(
    page_title="커피 레시피 퀴즈",
    page_icon='🧋',
    layout='centered',
    initial_sidebar_state='expanded'
)

@st.cache_data
def get_questions():
    return [
        {
            'id': 1,
            'beverage': "카푸치노",
            'layers': [
                {'name': "에스프레소", 'color': "rgb(61, 35, 20)", 'height': 25},
                {'name': "스팀 밀크", 'color': "rgb(240, 230, 210)", 'height': 35},
                {'name': "우유 거품", 'color': "rgb(255, 255, 255)", 'height': 40}
            ],
            'options': ["카페라떼", "카푸치노", "카페모카", "마끼아또"],
            'answer': "카푸치노",
            'hint': "이 음료는 위에 두꺼운 우유 거품 층이 올라가며 시나몬 가루를 뿌리기도 합니다."
        },
        {
            'id': 2,
            'beverage': "롱블랙",
            'layers': [
                {'name': "뜨거운 물", 'color': "rgb(219, 234, 254)", 'height': 70},
                {'name': "에스프레소", 'color': "rgb(61, 35, 20)", 'height': 30}
            ],
            'options': ["에스프레소", "아메리카노", "롱블랙", "아인슈페너"],
            'answer': "롱블랙",
            'hint': "뜨거운 물을 잔에 먼저 부은 후 에스프레소를 그 위에 추출하여 크레마가 보존되는 음료입니다."
        },
        {
            'id': 3,
            'beverage': "카페모카",
            'layers': [
                {'name': "초콜릿 시럽", 'color': "rgb(35, 18, 11)", 'height': 15},
                {'name': "에스프레소", 'color': "rgb(61, 35, 20)", 'height': 20},
                {'name': "스팀 밀크", 'color': "rgb(240, 230, 210)", 'height': 45},
                {'name': "휘핑크림", 'color': "rgb(255, 255, 255)", 'height': 20}
            ],
            'options': ["카페라떼", "카푸치노", "카페모카", "플랫 화이트"],
            'answer': "카페모카",
            'hint': "초콜릿 시럽과 우유, 에스프레소가 섞여 있으며 보통 휘핑크림이 올라가는 달콤한 커피입니다."
        },
        {
            'id': 4,
            'beverage': "아인슈페너",
            'layers': [
                {'name': "에스프레소", 'color': "rgb(61, 35, 20)", 'height': 20},
                {'name': "물", 'color': "rgb(219, 234, 254)", 'height': 50},
                {'name': "휘핑크림", 'color': "rgb(248, 250, 252)", 'height': 30}
            ],
            'options': ["아인슈페너", "마끼아또", "콘파냐", "카페라떼"],
            'answer': "아인슈페너",
            'hint': "비엔나에서 유래한 커피로 블랙커피 위에 차갑고 달콤한 생크림을 두껍게 올립니다."
        },
        {
            'id': 5,
            'beverage': "아포가토",
            'layers': [
                {'name': "바닐라 아이스크림", 'color': "rgb(254, 240, 138)", 'height': 60},
                {'name': "에스프레소", 'color': "rgb(61, 35, 20)", 'height': 40}
            ],
            'options': ["아포가토", "콘파냐", "에스프레소 마끼아또", "아이스크림 라떼"],
            'answer': "아포가토",
            'hint': "바닐라 아이스크림 한 덩이 위에 뜨거운 에스프레소를 끼얹어 먹는 이탈리아 디저트 음료입니다."
        }
    ]

questions = get_questions()

st.title("커피 레시피 퀴즈")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = ''
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''
if 'current_question' not in st.session_state:
    st.session_state['current_question'] = 0
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if 'quiz_finished' not in st.session_state:
    st.session_state['quiz_finished'] = False
if 'show_hint' not in st.session_state:
    st.session_state['show_hint'] = False
if 'user_answers' not in st.session_state:
    st.session_state['user_answers'] = {}
if 'rankings' not in st.session_state:
    st.session_state['rankings'] = []
if 'score_recorded' not in st.session_state:
    st.session_state['score_recorded'] = False
if 'menu_selection' not in st.session_state:
    st.session_state['menu_selection'] = "퀴즈 풀기"

if not st.session_state['logged_in']:
    with st.form('login_form'):
        st.info("광운대학교 소프트웨어학부  \n학번: 2022203045  \n이름: 곽희재")
        st.subheader("로그인")
        login_id = st.text_input("학번")
        login_name = st.text_input("이름")
        submitted = st.form_submit_button("로그인")
        if submitted:
            if login_id.strip() and login_name.strip():
                st.session_state['logged_in'] = True
                st.session_state['user_id'] = login_id.strip()
                st.session_state['user_name'] = login_name.strip()
                st.rerun()
            else:
                st.error("학번과 이름을 정확히 입력해 주세요.")
else:
    with st.sidebar:
        st.write(f"접속자: {st.session_state['user_name']}")
        st.write(f"학번: {st.session_state['user_id']}")
        st.divider()
        menu_options = ["퀴즈 풀기", "정답 순위", "로그아웃"]
        current_sel = st.session_state.get('menu_selection', "퀴즈 풀기")
        default_idx = menu_options.index(current_sel) if current_sel in menu_options else 0
        menu = st.selectbox("메뉴", menu_options, index=default_idx)
        if menu != current_sel:
            st.session_state['menu_selection'] = menu
            st.rerun()
    
    if menu == "로그아웃":
        st.session_state['logged_in'] = False
        st.session_state['user_id'] = ''
        st.session_state['user_name'] = ''
        st.session_state['current_question'] = 0
        st.session_state['score'] = 0
        st.session_state['quiz_finished'] = False
        st.session_state['show_hint'] = False
        st.session_state['user_answers'] = {}
        st.session_state['score_recorded'] = False
        st.session_state['menu_selection'] = "퀴즈 풀기"
        st.rerun()
        
    elif menu == "퀴즈 풀기":
        if not st.session_state['quiz_finished']:
            current_idx = st.session_state['current_question']
            q = questions[current_idx]
            
            st.subheader(f"문제 {current_idx + 1} / {len(questions)}")
            st.write("아래 비율을 보고 어떤 음료인지 맞추세요.")
            
            fig = go.Figure()
            for layer in q['layers']:
                fig.add_trace(go.Bar(
                    name=layer['name'],
                    x=["레시피"],
                    y=[layer['height']],
                    marker=dict(
                        color=layer['color'],
                        line=dict(color="rgb(51, 65, 85)", width=2)
                    ),
                    hovertemplate=f"{layer['name']}: %{{y}}%<extra></extra>",
                    text=[layer['name']],
                    textposition='inside',
                    insidetextanchor='middle',
                    insidetextfont=dict(size=16),
                    width=0.3
                ))
            fig.update_layout(
                barmode='stack',
                showlegend=True,
                height=350,
                margin=dict(l=10, r=10, t=15, b=15),
                yaxis=dict(
                    title="비율 (%)",
                    range=[-2, 102],
                    showgrid=True,
                    zeroline=False
                ),
                xaxis=dict(
                    showticklabels=False,
                    showgrid=False
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            
            selected_option = st.radio("선택지", q['options'], key=f'q_{current_idx}')
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("정답 제출", use_container_width=True, type="primary"):
                    st.session_state['user_answers'][str(current_idx)] = selected_option
                    if selected_option == q['answer']:
                        st.session_state['score'] += 1
                    
                    if current_idx + 1 < len(questions):
                        st.session_state['current_question'] += 1
                        st.session_state['show_hint'] = False
                    else:
                        st.session_state['quiz_finished'] = True
                        if not st.session_state.get('score_recorded', False):
                            st.session_state['rankings'].append({
                                'user_name': st.session_state['user_name'],
                                'user_id': st.session_state['user_id'],
                                'score': st.session_state['score'],
                                'total': len(questions),
                                'percentage': (st.session_state['score'] / len(questions)) * 100
                            })
                            st.session_state['score_recorded'] = True
                    st.rerun()
            with col2:
                hint_label = "힌트 닫기" if st.session_state['show_hint'] else "힌트 보기"
                if st.button(hint_label, use_container_width=True):
                    st.session_state['show_hint'] = not st.session_state['show_hint']
                    st.rerun()
            
            if st.session_state['show_hint']:
                st.info(q['hint'])
        else:
            st.subheader("퀴즈 결과")
            score = st.session_state['score']
            total = len(questions)
            percentage = (score / total) * 100

            with st.container(border=True):
                st.subheader("퀴즈 결과")
                st.markdown(f"**성명:** {st.session_state['user_name']}")
                st.markdown(f"**학번:** {st.session_state['user_id']}")
                st.success(f"점수: {score} / {total} ({percentage:.0f}%)")

            
            st.subheader("문제별 결과 확인")
            for idx, item in enumerate(questions):
                user_ans = st.session_state['user_answers'].get(str(idx))
                correct_ans = item['answer']
                result_text = ":green[정답]" if user_ans == correct_ans else ":red[오답]"
                
                with st.container(border=True):
                    col_left, col_right = st.columns([2, 3])
                    with col_left:
                        fig_small = go.Figure()
                        for layer in item['layers']:
                            fig_small.add_trace(go.Bar(
                                name=layer['name'],
                                x=["레시피"],
                                y=[layer['height']],
                                marker=dict(
                                    color=layer['color'],
                                    line=dict(color="rgb(51, 65, 85)", width=1)
                                ),
                                hovertemplate=f"{layer['name']}: %{{y}}%<extra></extra>",
                                text=[layer['name']],
                                textposition='inside',
                                insidetextanchor='middle',
                                insidetextfont=dict(size=12),
                                width=0.4
                            ))
                        fig_small.update_layout(
                            barmode='stack',
                            showlegend=False,
                            height=200,
                            margin=dict(l=5, r=5, t=15, b=15),
                            yaxis=dict(
                                range=[-2, 102],
                                showticklabels=False,
                                showgrid=False,
                                zeroline=False
                            ),
                            xaxis=dict(
                                showticklabels=False,
                                showgrid=False
                            ),
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig_small, use_container_width=True, config={'displayModeBar': False}, key=f'chart_small_{idx}')
                    
                    with col_right:
                        st.markdown(f"**문제 {idx + 1}.**")
                        st.write(f"본인 선택: {user_ans}")
                        st.write(f"실제 정답: {correct_ans} ({result_text})")
                        st.info(f"설명: {item['hint']}")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("다시 풀기", use_container_width=True, type="primary"):
                    st.session_state['current_question'] = 0
                    st.session_state['score'] = 0
                    st.session_state['quiz_finished'] = False
                    st.session_state['show_hint'] = False
                    st.session_state['user_answers'] = {}
                    st.session_state['score_recorded'] = False
                    st.session_state['menu_selection'] = "퀴즈 풀기"
                    st.rerun()
            with col_btn2:
                if st.button("순위 보기", use_container_width=True):
                    st.session_state['menu_selection'] = "정답 순위"
                    st.rerun()
                
    elif menu == "정답 순위":
        st.subheader("정답 순위")
        if not st.session_state['rankings']:
            st.info("기록이 없습니다.")
        else:
            sorted_ranks = sorted(st.session_state['rankings'], key=lambda x: x['percentage'], reverse=True)
            display_data = []
            for i, r in enumerate(sorted_ranks):
                display_data.append({
                    "순위": f"{i + 1}위",
                    "이름": r['user_name'],
                    "학번": r['user_id'],
                    "점수": f"{r['score']} / {r['total']} ({r['percentage']:.0f}%)"
                })
            st.table(display_data)
