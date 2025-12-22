import streamlit as st
import pandas as pd

# --- 설정 및 데이터 ---

# 1. 질문 정의 (총 12개, 각 차원별 3개)
# Format: (질문, 옵션 A (E/S/T/J, +1점), 옵션 B (I/N/F/P, -1점), 차원 인덱스)
# 인덱스: 0:E/I, 1:S/N, 2:T/F, 3:J/P
QUESTIONS = [
    ("1. 파티나 모임에 갔을 때, 당신은 주로...", "새로운 사람들에게 먼저 다가가 대화를 시작한다.", "아는 사람들 근처에 머물며 누가 말을 걸어주기를 기다린다.", 0),
    ("2. 에너지를 얻는 방식은...", "여러 사람과 함께 활발한 시간을 보낼 때 활력을 느낀다.", "혼자만의 조용하고 깊은 사색의 시간을 가질 때 에너지를 얻는다.", 0),
    ("3. 생각을 정리할 때, 당신은...", "생각을 말로 표현하거나 다른 사람과 논의하며 명확해진다.", "혼자 속으로 깊이 고민하고 정리한 후에야 말로 표현한다.", 0),
    
    ("4. 새로운 정보를 접할 때, 당신은 주로...", "현재의 사실, 경험, 구체적인 것에 집중한다.", "미래의 가능성, 아이디어, 숨겨진 의미에 집중한다.", 1),
    ("5. 설명을 하거나 들을 때, 당신은...", "실용적이고 구체적인 단계별 설명을 선호한다.", "은유적이고 추상적인, 전체적인 개념에 흥미를 느낀다.", 1),
    ("6. 중요한 결정을 내릴 때, 당신은...", "직접 경험하거나 확인된 자료를 바탕으로 신중하게 결정한다.", "직감과 영감을 통해 장기적인 패턴을 예측하며 결정한다.", 1),

    ("7. 결정을 내리는 기준은...", "논리, 객관적인 분석, 공정성을 가장 중요하게 생각한다.", "타인에게 미칠 영향, 개인의 가치, 조화를 우선적으로 고려한다.", 2),
    ("8. 논쟁이나 갈등 상황에서, 당신은...", "감정적으로 받아들이기보다 사실을 따져 해결책을 찾는 데 집중한다.", "상대방의 기분과 관계의 조화를 유지하는 것을 가장 중요하게 생각한다.", 2),
    ("9. 누군가에게 피드백을 줄 때, 당신은...", "때로는 진실이 중요하므로 솔직하고 명확하게 말하는 편이다.", "상대방의 기분을 보호하기 위해 부드럽고 우회적으로 표현한다.", 2),

    ("10. 삶의 방식에 대해, 당신은...", "계획을 세우고 그 계획을 따르는 것이 심적으로 편안하다.", "유연하게 상황에 맞춰 즉흥적으로 행동하는 것을 선호한다.", 3),
    ("11. 일을 처리할 때, 당신은...", "마감 기한을 준수하고 체계적으로 미리미리 일을 처리한다.", "선택지를 열어두고 마감 직전에 집중하여 에너지를 발휘하는 편이다.", 3),
    ("12. 여행을 준비할 때, 당신은...", "여행 시작 전에 모든 일정을 결정하고 확정하는 것을 선호한다.", "큰 틀만 잡고, 현지에서 즉흥적으로 계획을 세우는 것을 좋아한다.", 3),
]

# 2. 결과 정의 (MBTI 16가지 타입별 감성적인 파스텔 이미지 테마 + 이모지 추가)
# Format: (테마 제목, 테마 설명, 테마 이모지)
RESULTS = {
    "ISTJ": ("클래식 베이지", "정돈된 미니멀리즘과 베이지 톤의 안정적인 공간. 질서와 평온함이 느껴지는 테마.", "🗄️"),
    "ISFJ": ("소프트 핑크", "따뜻한 톤의 핑크와 화이트가 조화된 아늑한 홈 데코. 배려와 안락함이 느껴지는 테마.", "🌸"),
    "INFJ": ("라벤더 퍼플", "은은한 라벤더와 보라색 안개가 낀 몽환적인 새벽 풍경. 깊은 통찰과 신비로움이 느껴지는 테마.", "🌌"),
    "INTJ": ("스카이 그레이", "절제된 스카이 그레이 톤의 모던하고 구조적인 오피스/서재. 논리와 비전이 느껴지는 테마.", "♟️"),
    "ISTP": ("민트 그린", "자유로운 민트 그린과 청량한 하늘 아래의 캠핑 또는 여행 사진. 독립심과 탐험이 느껴지는 테마.", "🏕️"),
    "ISFP": ("파스텔 블루", "빈티지 파스텔 블루 톤의 예술적인 작업실 또는 캔버스. 부드러운 감성과 창조성이 느껴지는 테마.", "🎨"),
    "INFP": ("코랄 오렌지", "코랄 빛 노을과 잔잔한 호수, 감성적인 손글씨가 담긴 일러스트. 이상과 따뜻함이 느껴지는 테마.", "🌅"),
    "INTP": ("아이보리 화이트", "아이보리 톤의 복잡하고 기하학적인 패턴의 배경 또는 도식. 지적 호기심과 분석이 느껴지는 테마.", "💡"),
    "ESTP": ("밝은 옐로우", "햇살이 가득한 밝은 옐로우 톤의 역동적인 도시 거리 풍경. 활동성과 에너지가 느껴지는 테마.", "☀️"),
    "ESFP": ("비비드 핑크", "화려하지만 파스텔 톤을 잃지 않은 비비드 핑크의 축제 또는 즐거운 모임. 자유로움과 유쾌함이 느껴지는 테마.", "🎈"),
    "ENFP": ("무지개 파스텔", "무지개 빛깔의 파스텔 톤이 섞인 창의적인 브레인스토밍 보드. 상상력과 영감이 느껴지는 테마.", "🌈"),
    "ENTP": ("네온 블루", "미래 지향적인 네온 블루 톤의 기술 컨셉 또는 실험실 디자인. 혁신과 도전을 상징하는 테마.", "🚀"),
    "ENTJ": ("골드 & 마블", "파스텔 톤을 배경으로 한 골드 포인트와 대리석 무늬의 고급스러운 공간. 리더십과 성취가 느껴지는 테마.", "👑"),
    "ESTJ": ("다크 네이비 & 화이트", "파스텔 톤의 배경과 대비되는 명확한 다크 네이비 차트/도표. 책임감과 효율성이 느껴지는 테마.", "📊"),
    "ENFJ": ("따뜻한 피치", "따뜻한 피치 톤의 부드러운 일러스트, 서로를 안아주는 모습. 공감과 이타심이 느껴지는 테마.", "🫂"),
    "ESFJ": ("연한 레몬색", "연한 레몬색과 화이트 톤의 행복한 가족 식사 또는 사교적인 모임 장면. 친절함과 조화가 느껴지는 테마.", "🍰"),
}

# 3. Streamlit 세션 상태 초기화
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0  # 현재 질문 인덱스
if 'answers' not in st.session_state:
    # 4개 차원 (E/I, S/N, T/F, J/P)의 점수 저장. 초기값 0
    st.session_state.answers = [0, 0, 0, 0]
if 'mbti_result' not in st.session_state:
    st.session_state.mbti_result = None

# --- Custom CSS (파스텔 톤 테마 적용) ---
def apply_pastel_style():
    """감성적인 파스텔 톤의 CSS 스타일을 적용합니다."""
    st.markdown("""
    <style>
        /* 배경 및 전체 폰트 */
        .stApp {
            background-color: #F8F8FF; /* 은은한 라벤더 블러시 */
            color: #333333;
            font-family: 'Inter', sans-serif;
        }
        /* 제목 스타일 */
        h1 {
            color: #7B68EE; /* 미디엄 슬레이트 블루 */
            text-align: center;
            font-weight: 700;
            padding-bottom: 10px;
            border-bottom: 3px solid #E6E6FA; /* 라벤더 */
        }
        h2 {
            color: #8A2BE2; /* 블루 바이올렛 */
            text-align: center;
        }
        /* 질문 카드 스타일 */
        .question-card {
            background-color: #FFFFFF;
            border: 2px solid #E0FFFF; /* 라이트 시안 */
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            text-align: center;
        }
        /* 답변 버튼 스타일 (파스텔 톤) */
        .stButton>button {
            width: 100%;
            height: 70px;
            margin: 10px 0;
            border-radius: 8px;
            border: none;
            color: #333333;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        /* 옵션 A 버튼 (Warm Pastel: 연한 코랄) */
        .stButton:nth-child(1) button {
            background-color: #FFDAB9; /* 피치 퍼프 */
        }
        .stButton:nth-child(1) button:hover {
            background-color: #FFA07A; /* 라이트 살몬 */
            color: white;
        }
        /* 옵션 B 버튼 (Cool Pastel: 연한 민트) */
        .stButton:nth-child(2) button {
            background-color: #E0FFFF; /* 라이트 시안 */
        }
        .stButton:nth-child(2) button:hover {
            background-color: #AFEEEE; /* 페일 터콰이즈 */
            color: white;
        }

        /* 결과 화면 스타일 */
        .result-box {
            background-color: #FFFFFF;
            padding: 30px;
            border-radius: 15px;
            border: 3px solid #8A2BE2;
            text-align: center;
            box-shadow: 0 6px 20px rgba(138, 43, 226, 0.3);
        }
        .mbti-type {
            font-size: 48px;
            font-weight: 900;
            color: #7B68EE; /* 미디엄 슬레이트 블루 */
            margin-bottom: 15px;
        }
        .theme-emoji { /* 초대형 이모티콘을 위한 새로운 클래스 */
            font-size: 100px; 
            margin: 20px 0;
            line-height: 1; /* 이모티콘 주변 공백 최소화 */
        }
        .theme-title { /* 테마 제목 텍스트 (이모티콘보다 작게 유지) */
            font-size: 28px; 
            color: #8A2BE2;
            font-weight: 700;
            margin-top: 10px;
        }
        .theme-description {
            /* 사용자 요청에 따라 설명을 표시하지 않음 */
            display: none; 
        }
    </style>
    """, unsafe_allow_html=True)

# --- 로직 함수 ---

def calculate_mbti(scores):
    """점수를 바탕으로 MBTI 결과를 계산합니다."""
    # 점수가 0보다 크거나 같으면 첫 번째 문자, 아니면 두 번째 문자
    mbti = ""
    mbti += "E" if scores[0] >= 0 else "I"
    mbti += "S" if scores[1] >= 0 else "N"
    mbti += "T" if scores[2] >= 0 else "F"
    mbti += "J" if scores[3] >= 0 else "P"
    return mbti

def handle_answer(score_change, dimension_index):
    """답변을 처리하고 다음 질문으로 넘어갑니다."""
    # 현재 차원에 점수 반영
    st.session_state.answers[dimension_index] += score_change
    
    # 다음 질문으로 이동
    if st.session_state.current_q < len(QUESTIONS) - 1:
        st.session_state.current_q += 1
    else:
        # 모든 질문 완료, 결과 계산
        final_mbti = calculate_mbti(st.session_state.answers)
        st.session_state.mbti_result = final_mbti
        st.session_state.current_q += 1 # 결과 화면을 위해 인덱스 12로 이동

# --- UI 구성 ---

apply_pastel_style()

st.title("💖 감성 파스텔 MBTI 테스트 🎨")

# 질문 진행 상황 표시
total_q = len(QUESTIONS)
if st.session_state.mbti_result is None:
    progress = st.session_state.current_q / total_q
    # 현재 질문이 시작 화면(0)이 아닐 때만 진행률 표시
    if st.session_state.current_q > 0:
         st.progress(progress, text=f"진행률: {st.session_state.current_q}/{total_q} 질문")


# 1. 질문 화면
if st.session_state.current_q < total_q:
    q_index = st.session_state.current_q
    question_data = QUESTIONS[q_index]
    
    # 질문 카드
    st.markdown(f"""
        <div class="question-card">
            <p style='font-size: 20px; font-weight: 700; color: #5B45E5;'>
                Q{q_index + 1}. {question_data[0]}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # 답변 버튼 (Streamlit의 col을 사용하여 버튼을 나란히 배치)
    col1, col2 = st.columns(2)
    
    # 옵션 A (+1점)
    with col1:
        # 버튼을 클릭하면 handle_answer 함수 호출 (+1점, 해당 차원 인덱스)
        st.button(
            question_data[1], 
            on_click=handle_answer, 
            args=[1, question_data[3]], 
            key=f"q{q_index}_A"
        )

    # 옵션 B (-1점)
    with col2:
        # 버튼을 클릭하면 handle_answer 함수 호출 (-1점, 해당 차원 인덱스)
        st.button(
            question_data[2], 
            on_click=handle_answer, 
            args=[-1, question_data[3]], 
            key=f"q{q_index}_B"
        )
    
    st.markdown("---")
    st.markdown(f"<p style='text-align: center; color: #AAAAAA;'>({['E/I', 'S/N', 'T/F', 'J/P'][question_data[3]]} 차원 질문)</p>", unsafe_allow_html=True)


# 2. 결과 화면
elif st.session_state.mbti_result:
    mbti_type = st.session_state.mbti_result
    # RESULTS에서 이모지까지 함께 가져옴
    theme_title, theme_desc, theme_emoji = RESULTS.get(mbti_type, ("테마 미정", "결과를 찾을 수 없습니다.", "❓"))

    # '테스트 결과가 나왔습니다' 제목과 설명 텍스트를 제거하고 시각적 요소만 남김
    
    st.markdown(f"""
        <div class="result-box">
            {/* MBTI 유형 */}
            <p class="mbti-type">{mbti_type}</p>
            
            <hr style='border: 1px dashed #E0FFFF; margin: 20px 0;'>

            {/* 초대형 이모티콘 */}
            <p class="theme-emoji">{theme_emoji}</p>
            
            {/* 테마 제목 (이모티콘에 대한 텍스트 레이블) */}
            <p class="theme-title">『{theme_title}』</p>
            
            {/* 이전의 상세 설명과 면책 조항은 모두 제거됨 */}
            
        </div>
    """, unsafe_allow_html=True)

    # 다시 시작 버튼
    def reset_test():
        st.session_state.current_q = 0
        st.session_state.answers = [0, 0, 0, 0]
        st.session_state.mbti_result = None

    st.markdown("<br>", unsafe_allow_html=True)
    st.button("다시 검사하기", on_click=reset_test, key="reset_button")

# 3. 테스트 시작 전 초기 화면 (사용자가 새로고침하거나 초기 상태일 때)
else:
    st.markdown("""
        <div style="text-align: center; padding: 50px; border: 1px solid #E6E6FA; border-radius: 12px; background-color: white;">
            <h2 style='color: #7B68EE;'>당신의 파스텔 톤 감성은 무엇일까요?</h2>
            <p style='font-size: 18px; color: #555555; margin-top: 20px;'>
                12가지 간단한 질문에 답하고, 당신의 MBTI 유형과 가장 잘 어울리는 감성 이미지 테마를 확인해 보세요.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    def start_test():
        st.session_state.current_q = 0

    st.button("테스트 시작하기", on_click=start_test, key="start_button")
