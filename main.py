import streamlit as st
import random

# ─────────────────────────────────────────
#  페이지 기본 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MBTI 명언 🌟",
    page_icon="✨",
    layout="centered",
)

# ─────────────────────────────────────────
#  CSS 커스텀 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
  }

  .mbti-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 30px 35px;
    color: white;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 8px 32px rgba(102,126,234,0.35);
  }

  .quote-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 20px;
    padding: 28px 35px;
    color: white;
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 8px 32px rgba(240,147,251,0.35);
    font-size: 1.1rem;
    line-height: 1.8;
  }

  .author-text {
    margin-top: 14px;
    font-size: 0.9rem;
    opacity: 0.85;
    font-style: italic;
  }

  .type-badge {
    display: inline-block;
    background: rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 8px;
  }

  .trait-tag {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.82rem;
    margin: 3px;
  }

  .header-emoji {
    font-size: 3.5rem;
    display: block;
    text-align: center;
    margin-bottom: 4px;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  데이터 정의
# ─────────────────────────────────────────

MBTI_DATA = {
    # ── 분석가 그룹 ──
    "INTJ": {
        "emoji": "🏰",
        "name": "전략가",
        "color": "#4B0082",
        "traits": ["독립적", "전략적", "완벽주의", "비전가"],
        "quotes": [
            ("내가 통제할 수 없는 것에 에너지를 낭비하지 않는다. 나는 내가 할 수 있는 것에 집중한다.", "마르쿠스 아우렐리우스"),
            ("남들이 불가능하다고 말하는 일을 하는 것이 즐겁다.", "워렌 버핏"),
            ("계획 없는 목표는 그냥 소망에 불과하다.", "앙투안 드 생텍쥐페리"),
            ("가장 위험한 세계관은 세상을 보지 못한 자들의 세계관이다.", "알렉산더 폰 훔볼트"),
            ("생각은 힘이다. 그 힘을 올바른 방향으로 집중하라.", "나폴레온 힐"),
        ],
    },
    "INTP": {
        "emoji": "🔬",
        "name": "논리술사",
        "color": "#003366",
        "traits": ["논리적", "창의적", "탐구적", "철학적"],
        "quotes": [
            ("나는 아무것도 모른다는 것을 안다. 그것이 내 지혜의 시작이다.", "소크라테스"),
            ("진정한 지식은 자신이 무엇을 알고 무엇을 모르는지 아는 것이다.", "공자"),
            ("상상력은 지식보다 중요하다.", "알버트 아인슈타인"),
            ("당신이 충분히 이해하지 못하는 것은 당신이 소유하지 못한 것이다.", "요한 볼프강 폰 괴테"),
            ("의심은 지식의 시작이다.", "르네 데카르트"),
        ],
    },
    "ENTJ": {
        "emoji": "👑",
        "name": "통솔자",
        "color": "#800000",
        "traits": ["결단력", "리더십", "목표지향", "카리스마"],
        "quotes": [
            ("리더십은 다른 사람의 비전을 당신의 비전으로 만드는 기술이다.", "나폴레옹 보나파르트"),
            ("도전하지 않으면 성공도 없다.", "마이클 조던"),
            ("약한 자는 결코 용서를 베풀 수 없다. 용서는 강한 자의 특성이다.", "마하트마 간디"),
            ("성공은 최종적인 것이 아니며, 실패는 치명적인 것이 아니다. 중요한 것은 계속하는 용기다.", "윈스턴 처칠"),
            ("원하는 것을 얻으려면 그것을 받을 자격을 갖춰라.", "찰리 멍거"),
        ],
    },
    "ENTP": {
        "emoji": "💡",
        "name": "변론가",
        "color": "#FF6600",
        "traits": ["혁신적", "열정적", "논쟁적", "기지넘침"],
        "quotes": [
            ("규칙은 복종하기 위해 존재하는 것이 아니라 현명한 자들의 지침서이자 바보들의 복종 대상이다.", "더글러스 베이더"),
            ("당신이 상상할 수 있다면, 당신은 그것을 창조할 수 있다.", "윌리엄 아서 워드"),
            ("새로운 아이디어의 표식은 처음에는 불가능해 보인다는 것이다.", "아서 클라크"),
            ("현상 유지는 아무것도 하지 않는 것과 같다.", "버락 오바마"),
            ("토론은 생각을 날카롭게 한다.", "볼테르"),
        ],
    },
    # ── 외교관 그룹 ──
    "INFJ": {
        "emoji": "🌌",
        "name": "옹호자",
        "color": "#2E4057",
        "traits": ["통찰력", "이상주의", "헌신적", "예언적"],
        "quotes": [
            ("당신이 세상에서 보고 싶은 변화 자체가 되어라.", "마하트마 간디"),
            ("어둠은 어둠을 몰아낼 수 없다. 오직 빛만이 그럴 수 있다.", "마틴 루터 킹 주니어"),
            ("다른 사람을 위한 삶이 가치 있는 삶이다.", "알버트 아인슈타인"),
            ("깊은 곳에서 인류는 하나다.", "롤먼 타고르"),
            ("당신의 목적이 크면, 실패조차 의미가 있다.", "J.K. 롤링"),
        ],
    },
    "INFP": {
        "emoji": "🌿",
        "name": "중재자",
        "color": "#2D6A4F",
        "traits": ["공감능력", "이상주의", "창의적", "내향적"],
        "quotes": [
            ("당신은 충분히 존재한다. 충분히 가졌다. 충분히 행한다.", "브레네 브라운"),
            ("나는 꿈꾸기 때문에 산다. 꿈이 없다면 살아갈 이유가 없다.", "어슐러 K. 르 귄"),
            ("세상을 바꾸는 가장 간단한 방법은 내 마음을 바꾸는 것이다.", "버크민스터 풀러"),
            ("상처받지 않은 영혼은 없다. 그러나 그 상처에서 꽃이 핀다.", "루미"),
            ("너 자신에게 친절하라. 당신이 대하는 모든 이들은 힘든 싸움을 하고 있다.", "플라톤"),
        ],
    },
    "ENFJ": {
        "emoji": "🌟",
        "name": "선도자",
        "color": "#C77DFF",
        "traits": ["따뜻함", "리더십", "공감", "영감을 줌"],
        "quotes": [
            ("최고의 방법으로 사람들을 이끄는 것은 그들에게 길을 보여주는 것이다.", "소크라테스"),
            ("한 사람의 삶에 변화를 주는 것이 세상을 바꾸는 것이다.", "앤 프랭크"),
            ("좋은 리더는 먼저 섬기고, 그 다음 이끈다.", "로버트 그린리프"),
            ("당신의 친절은 당신이 가진 최고의 힘이다.", "마더 테레사"),
            ("사람들이 중요하다고 느끼게 만들어라, 그러면 그들은 중요해질 것이다.", "메리 케이 애시"),
        ],
    },
    "ENFP": {
        "emoji": "🎆",
        "name": "활동가",
        "color": "#FF9500",
        "traits": ["열정적", "창의적", "자유로운", "사교적"],
        "quotes": [
            ("인생은 용기 있는 모험이거나 아무것도 아니다.", "헬렌 켈러"),
            ("당신이 사랑하는 일을 하라, 그러면 일생에 하루도 일한 날이 없을 것이다.", "공자"),
            ("미래는 꿈의 아름다움을 믿는 사람들의 것이다.", "엘리너 루즈벨트"),
            ("가능성 속에 살라.", "에밀리 디킨슨"),
            ("즐겁게 사는 것이 최고의 복수다.", "조지 허버트"),
        ],
    },
    # ── 관리자 그룹 ──
    "ISTJ": {
        "emoji": "📋",
        "name": "물류관리자",
        "color": "#1B4332",
        "traits": ["책임감", "신뢰성", "체계적", "근면"],
        "quotes": [
            ("규율은 목표와 성취 사이의 다리다.", "짐 론"),
            ("작은 일에 성실한 사람이 큰 일도 해낸다.", "루크복음 16:10"),
            ("탁월함은 한 번의 행동이 아니라 습관이다.", "아리스토텔레스"),
            ("무엇이든 할 가치가 있다면, 제대로 할 가치가 있다.", "필립 체스터필드"),
            ("신뢰는 쌓는 데 오래 걸리고 무너지는 건 한순간이다.", "작자 미상"),
        ],
    },
    "ISFJ": {
        "emoji": "🛡️",
        "name": "수호자",
        "color": "#2C5F2E",
        "traits": ["헌신적", "배려", "신뢰성", "따뜻함"],
        "quotes": [
            ("사랑은 행동이지 감정이 아니다.", "스티브 마라볼리"),
            ("당신이 할 수 있는 가장 큰 일은 다른 사람을 돕는 것이다.", "마하트마 간디"),
            ("배려하는 마음을 가진 사람이 세상을 더 나은 곳으로 만든다.", "헨리 제임스"),
            ("작은 친절이 세상을 더 살기 좋은 곳으로 만든다.", "작자 미상"),
            ("당신의 존재 자체가 누군가에게 선물이다.", "작자 미상"),
        ],
    },
    "ESTJ": {
        "emoji": "⚖️",
        "name": "경영자",
        "color": "#5C4033",
        "traits": ["결단력", "관리능력", "책임감", "실용적"],
        "quotes": [
            ("질서는 자연의 첫 번째 법칙이다.", "알렉산더 포프"),
            ("성공하는 사람은 행동한다. 실패하는 사람은 계획만 한다.", "파블로 피카소"),
            ("위대한 결과는 의지로 만들어진다.", "나폴레온 힐"),
            ("지도자란 희망을 나눠주는 상인이다.", "나폴레옹"),
            ("원칙 없이 성공은 없다.", "존 D. 록펠러"),
        ],
    },
    "ESFJ": {
        "emoji": "🤗",
        "name": "집정관",
        "color": "#FF69B4",
        "traits": ["사교적", "배려심", "충성스러움", "협력적"],
        "quotes": [
            ("혼자 가면 빠르게 갈 수 있지만, 함께 가면 멀리 갈 수 있다.", "아프리카 속담"),
            ("삶에서 가장 소중한 것은 우리가 나누는 관계다.", "작자 미상"),
            ("진정한 친구는 당신의 잠재력을 보는 사람이다.", "헨리 데이비드 소로"),
            ("친절은 전염된다. 오늘 친절을 베풀어라.", "작자 미상"),
            ("사랑받고 싶다면 먼저 사랑하라.", "벤저민 프랭클린"),
        ],
    },
    # ── 탐험가 그룹 ──
    "ISTP": {
        "emoji": "🔧",
        "name": "장인",
        "color": "#4A4A4A",
        "traits": ["실용적", "분석적", "독립적", "침착"],
        "quotes": [
            ("말이 아닌 행동이 사람을 증명한다.", "작자 미상"),
            ("가장 좋은 도구는 실제로 작동하는 도구다.", "작자 미상"),
            ("침묵은 가장 강력한 대화다.", "작자 미상"),
            ("가장 복잡한 문제도 단순한 해결책을 가지고 있다.", "작자 미상"),
            ("경험은 최고의 선생이다.", "율리우스 카이사르"),
        ],
    },
    "ISFP": {
        "emoji": "🎨",
        "name": "모험가",
        "color": "#FF7F7F",
        "traits": ["예술적", "감성적", "자유로운", "친절"],
        "quotes": [
            ("삶은 예술이다. 당신이 그 예술가다.", "작자 미상"),
            ("아름다움은 보는 사람의 눈 속에 있다.", "마가렛 헌게르포드"),
            ("순간 속에 살아라. 그것이 진정한 삶이다.", "작자 미상"),
            ("진정한 자유는 자신을 표현하는 것이다.", "오스카 와일드"),
            ("당신이 느끼는 것이 당신이 창조하는 것이다.", "작자 미상"),
        ],
    },
    "ESTP": {
        "emoji": "⚡",
        "name": "사업가",
        "color": "#FFD700",
        "traits": ["행동파", "현실적", "에너지 넘침", "대담"],
        "quotes": [
            ("생각만 하는 자는 아무것도 이루지 못한다. 행동하라!", "요한 볼프강 폰 괴테"),
            ("기회는 춤추고 있는 사람들에게 온다.", "작자 미상"),
            ("지금 이 순간이 전부다.", "작자 미상"),
            ("겁쟁이는 죽기 전에 여러 번 죽고, 용감한 자는 한 번만 죽는다.", "윌리엄 셰익스피어"),
            ("언제나 지금이 시작하기 가장 좋은 때다.", "작자 미상"),
        ],
    },
    "ESFP": {
        "emoji": "🎉",
        "name": "연예인",
        "color": "#FF4500",
        "traits": ["활발함", "즉흥적", "사교적", "낙관적"],
        "quotes": [
            ("오늘을 춤처럼 살아라, 내일이 없는 것처럼.", "작자 미상"),
            ("웃음은 영혼의 음악이다.", "작자 미상"),
            ("삶은 파티다. 당신이 주인공이다.", "작자 미상"),
            ("행복은 스스로 만드는 것이다.", "에이브러햄 링컨"),
            ("오늘의 기쁨이 내일의 힘이 된다.", "작자 미상"),
        ],
    },
}

# 그룹 분류
GROUPS = {
    "🔮 분석가": ["INTJ", "INTP", "ENTJ", "ENTP"],
    "🌈 외교관": ["INFJ", "INFP", "ENFJ", "ENFP"],
    "🏛️ 관리자": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
    "🌊 탐험가": ["ISTP", "ISFP", "ESTP", "ESFP"],
}

# ─────────────────────────────────────────
#  UI 레이아웃
# ─────────────────────────────────────────

st.markdown('<span class="header-emoji">🧠</span>', unsafe_allow_html=True)
st.title("MBTI 명언 추천기")
st.markdown("**당신의 MBTI 유형에 어울리는 명언을 찾아보세요!**")
st.divider()

# ── 그룹 탭 ──
tabs = st.tabs(list(GROUPS.keys()))

for tab, (group_name, types) in zip(tabs, GROUPS.items()):
    with tab:
        cols = st.columns(4)
        for i, mbti_type in enumerate(types):
            info = MBTI_DATA[mbti_type]
            with cols[i]:
                btn_label = f"{info['emoji']}\n**{mbti_type}**\n{info['name']}"
                if st.button(
                    f"{info['emoji']} {mbti_type}\n{info['name']}",
                    key=f"btn_{mbti_type}",
                    use_container_width=True,
                ):
                    st.session_state["selected"] = mbti_type

st.divider()

# ── 결과 출력 ──
if "selected" in st.session_state:
    sel = st.session_state["selected"]
    info = MBTI_DATA[sel]

    # 풍선 🎈
    st.balloons()

    # MBTI 카드
    traits_html = "".join(
        [f'<span class="trait-tag">#{t}</span>' for t in info["traits"]]
    )
    st.markdown(
        f"""
        <div class="mbti-card">
            <div class="type-badge">{sel}</div>
            <div style="font-size:2.5rem; margin:8px 0;">{info['emoji']}</div>
            <div style="font-size:1.2rem; font-weight:700; margin-bottom:12px;">{info['name']}</div>
            <div>{traits_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 명언 랜덤 선택
    if "quote_idx" not in st.session_state or st.session_state.get("quote_type") != sel:
        st.session_state["quote_idx"] = random.randint(0, len(info["quotes"]) - 1)
        st.session_state["quote_type"] = sel

    q_text, q_author = info["quotes"][st.session_state["quote_idx"]]

    st.markdown(
        f"""
        <div class="quote-box">
            <div style="font-size:2rem; margin-bottom:8px;">💬</div>
            <div>"{q_text}"</div>
            <div class="author-text">— {q_author}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 다른 명언 보기 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔀 다른 명언 보기", use_container_width=True):
            current = st.session_state["quote_idx"]
            options = list(range(len(info["quotes"])))
            options.remove(current)
            st.session_state["quote_idx"] = random.choice(options)
            st.rerun()

else:
    st.markdown(
        """
        <div style="text-align:center; padding: 40px; color: #888; font-size:1.1rem;">
            ☝️ 위에서 MBTI 유형을 선택해 보세요!
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────
#  푸터
# ─────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center; color:#aaa; font-size:0.8rem;'>✨ MBTI 명언 추천기 | Made with Streamlit 🎈</div>",
    unsafe_allow_html=True,
)
