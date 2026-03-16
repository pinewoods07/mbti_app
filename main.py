import streamlit as st
import random

# ─────────────────────────────────────────
#  페이지 기본 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="MBTI 명언 🌟",
    page_icon="🧠",
    layout="centered",
)

# ─────────────────────────────────────────
#  전역 CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
  html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }

  @keyframes fall_anim {
    0%   { top: -60px; opacity: 1; transform: rotate(0deg) scale(1); }
    80%  { opacity: 1; }
    100% { top: 110vh;  opacity: 0; transform: rotate(720deg) scale(0.4); }
  }
  @keyframes rise_anim {
    0%   { bottom: -60px; opacity: 1; transform: rotate(0deg) scale(1); }
    80%  { opacity: 1; }
    100% { bottom: 110vh; opacity: 0; transform: rotate(-720deg) scale(0.4); }
  }
  @keyframes pulse-glow {
    0%,100% { box-shadow: 0 0 20px rgba(255,255,255,0.3); }
    50%      { box-shadow: 0 0 50px rgba(255,255,255,0.7); }
  }

  .mbti-card {
    border-radius: 24px;
    padding: 30px 35px;
    color: white;
    text-align: center;
    margin: 20px 0;
    animation: pulse-glow 3s ease-in-out infinite;
  }
  .quote-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    border-radius: 20px;
    padding: 28px 35px;
    color: white;
    text-align: center;
    margin: 16px 0;
    box-shadow: 0 8px 32px rgba(240,147,251,0.35);
    font-size: 1.05rem;
    line-height: 1.85;
  }
  .reason-box {
    background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
    border-radius: 16px;
    padding: 20px 28px;
    color: white;
    margin: 12px 0 24px 0;
    font-size: 0.93rem;
    line-height: 1.75;
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
  .header-emoji { font-size: 3.5rem; display: block; text-align: center; margin-bottom: 4px; }
  .effect-label {
    text-align: center;
    font-size: 0.82rem;
    color: #aaa;
    margin-top: -10px;
    margin-bottom: 10px;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  MBTI 유형별 이펙트 정의
# ─────────────────────────────────────────
EFFECTS = {
    "INTJ": {"particles": ["⭐","🌑","🔭"], "dir": "fall",  "desc": "별이 쏟아집니다 🌌"},
    "INTP": {"particles": ["💡","🔮","⚛️"],  "dir": "fall",  "desc": "아이디어가 떠오릅니다 💡"},
    "ENTJ": {"particles": ["👑","🏆","⚔️"],  "dir": "fall",  "desc": "왕관이 내려옵니다 👑"},
    "ENTP": {"particles": ["💡","🎯","🔥"],  "dir": "rise",  "desc": "아이디어가 솟구칩니다 🚀"},
    "INFJ": {"particles": ["🌌","✨","🔮"],  "dir": "fall",  "desc": "우주가 빛납니다 🌌"},
    "INFP": {"particles": ["🍃","🌸","🌿"],  "dir": "fall",  "desc": "꽃잎이 흩날립니다 🌸"},
    "ENFJ": {"particles": ["💫","💛","🌟"],  "dir": "rise",  "desc": "따뜻한 빛이 올라옵니다 💫"},
    "ENFP": {"particles": ["🎊","🌈","🎆"],  "dir": "rise",  "desc": "폭죽이 터집니다 🎆"},
    "ISTJ": {"particles": ["✅","📌","🏛️"],  "dir": "fall",  "desc": "체크리스트가 완성됩니다 ✅"},
    "ISFJ": {"particles": ["💝","🛡️","🌷"],  "dir": "fall",  "desc": "꽃과 하트가 쏟아집니다 💝"},
    "ESTJ": {"particles": ["🏆","⚖️","📊"],  "dir": "fall",  "desc": "트로피가 내려옵니다 🏆"},
    "ESFJ": {"particles": ["🌸","🤗","💖"],  "dir": "rise",  "desc": "꽃이 피어오릅니다 🌸"},
    "ISTP": {"particles": ["⚙️","🔩","🛠️"],  "dir": "fall",  "desc": "톱니바퀴가 돌아갑니다 ⚙️"},
    "ISFP": {"particles": ["🎨","🌈","🦋"],  "dir": "rise",  "desc": "나비가 날아오릅니다 🦋"},
    "ESTP": {"particles": ["⚡","🔥","💥"],  "dir": "rise",  "desc": "번개가 솟구칩니다 ⚡"},
    "ESFP": {"particles": ["🎉","🎈","🪄"],  "dir": "rise",  "desc": "파티가 시작됩니다 🎉"},
}

# ─────────────────────────────────────────
#  MBTI 데이터 (명언 + 추천 이유)
# ─────────────────────────────────────────
MBTI_DATA = {
    "INTJ": {
        "emoji": "🏰", "name": "전략가",
        "gradient": "linear-gradient(135deg, #4B0082 0%, #9B59B6 100%)",
        "traits": ["독립적", "전략적", "완벽주의", "비전가"],
        "quotes": [
            ("내가 통제할 수 없는 것에 에너지를 낭비하지 않는다. 나는 내가 할 수 있는 것에 집중한다.",
             "마르쿠스 아우렐리우스",
             "통제 불가능한 것을 내려놓고 자신이 할 수 있는 것에만 에너지를 집중하는 INTJ의 완벽주의적 자기 관리 방식을 정확히 표현한 명언입니다."),
            ("남들이 불가능하다고 말하는 일을 하는 것이 즐겁다.",
             "워렌 버핏",
             "INTJ는 타인의 시선보다 자신의 비전을 믿고 나아가는 성향이 강합니다. 대중의 부정적 반응을 오히려 동기로 삼는 이 태도가 INTJ의 전략가 기질과 맞닿아 있습니다."),
            ("계획 없는 목표는 그냥 소망에 불과하다.",
             "앙투안 드 생텍쥐페리",
             "INTJ는 목표를 세울 때 반드시 구체적인 실행 계획을 함께 수립합니다. 이 명언은 그 철저한 전략적 사고방식을 잘 대변합니다."),
            ("가장 위험한 세계관은 세상을 보지 못한 자들의 세계관이다.",
             "알렉산더 폰 훔볼트",
             "끊임없이 배우고 세계를 탐구하며 넓은 시야를 유지하려는 INTJ의 지적 탐구 욕구와 완벽히 부합하는 명언입니다."),
            ("생각은 힘이다. 그 힘을 올바른 방향으로 집중하라.",
             "나폴레온 힐",
             "INTJ는 사고 자체를 가장 강력한 도구로 여깁니다. 에너지를 한 방향으로 집중해 최대 효과를 내는 이 철학이 INTJ의 정수를 담고 있습니다."),
        ],
    },
    "INTP": {
        "emoji": "🔬", "name": "논리술사",
        "gradient": "linear-gradient(135deg, #003366 0%, #2980B9 100%)",
        "traits": ["논리적", "창의적", "탐구적", "철학적"],
        "quotes": [
            ("나는 아무것도 모른다는 것을 안다. 그것이 내 지혜의 시작이다.",
             "소크라테스",
             "INTP는 모든 것을 의심하고 검증하려는 성향을 가집니다. 무지를 인정하는 것이 지식의 출발점이라는 이 철학은 INTP의 끝없는 탐구 정신과 일치합니다."),
            ("진정한 지식은 자신이 무엇을 알고 무엇을 모르는지 아는 것이다.",
             "공자",
             "INTP는 자신의 지식 체계를 정확히 파악하는 메타인지 능력이 뛰어납니다. 앎의 경계를 명확히 하는 것을 중시하는 이 명언이 딱 들어맞습니다."),
            ("상상력은 지식보다 중요하다.",
             "알버트 아인슈타인",
             "논리와 데이터를 중시하면서도 창의적 사고로 기존 틀을 깨는 INTP의 이중성을 이 명언이 완벽히 표현합니다. 아인슈타인 자신도 대표적인 INTP로 알려져 있습니다."),
            ("당신이 충분히 이해하지 못하는 것은 당신이 소유하지 못한 것이다.",
             "요한 볼프강 폰 괴테",
             "INTP는 표면적 이해에 만족하지 않고 깊이 파고들어 완전히 이해해야 직성이 풀리는 성향입니다. 이 완전한 이해에 대한 집착을 잘 담아낸 명언입니다."),
            ("의심은 지식의 시작이다.",
             "르네 데카르트",
             "데카르트의 방법적 회의론은 INTP의 사고방식 그 자체입니다. 당연하게 받아들여지는 것조차 의심하고 검증하려는 INTP의 본능과 완벽히 공명합니다."),
        ],
    },
    "ENTJ": {
        "emoji": "👑", "name": "통솔자",
        "gradient": "linear-gradient(135deg, #800000 0%, #C0392B 100%)",
        "traits": ["결단력", "리더십", "목표지향", "카리스마"],
        "quotes": [
            ("리더십은 다른 사람의 비전을 당신의 비전으로 만드는 기술이다.",
             "나폴레옹 보나파르트",
             "ENTJ는 타인을 자신의 목표 아래 하나로 묶는 통솔력이 탁월합니다. 개인의 비전을 집단의 방향으로 전환시키는 이 리더십 철학이 ENTJ의 본질입니다."),
            ("도전하지 않으면 성공도 없다.",
             "마이클 조던",
             "ENTJ는 불확실성 앞에서도 과감히 행동합니다. 도전을 성장의 전제 조건으로 보는 이 태도는 ENTJ가 매일 실천하는 삶의 방식입니다."),
            ("약한 자는 결코 용서를 베풀 수 없다. 용서는 강한 자의 특성이다.",
             "마하트마 간디",
             "ENTJ는 강인함에서 비롯된 여유와 포용력을 갖습니다. 강함이 진정한 관용의 토대라는 이 역설적 진리가 ENTJ의 리더십 철학과 맞닿아 있습니다."),
            ("성공은 최종적인 것이 아니며, 실패는 치명적인 것이 아니다. 중요한 것은 계속하는 용기다.",
             "윈스턴 처칠",
             "ENTJ는 결과에 집착하면서도 장기적 관점에서 끈질기게 목표를 추구합니다. 지속하는 용기를 핵심 덕목으로 삼는 이 명언이 ENTJ의 집요함과 공명합니다."),
            ("원하는 것을 얻으려면 그것을 받을 자격을 갖춰라.",
             "찰리 멍거",
             "ENTJ는 결과를 원하기 이전에 먼저 자신을 그에 걸맞은 수준으로 끌어올리는 자기 단련을 중시합니다. 이 원칙은 ENTJ의 자기개발 철학의 핵심입니다."),
        ],
    },
    "ENTP": {
        "emoji": "💡", "name": "변론가",
        "gradient": "linear-gradient(135deg, #FF6600 0%, #FFA500 100%)",
        "traits": ["혁신적", "열정적", "논쟁적", "기지넘침"],
        "quotes": [
            ("규칙은 복종하기 위해 존재하는 것이 아니라 현명한 자들의 지침서이자 바보들의 복종 대상이다.",
             "더글러스 베이더",
             "ENTP는 규칙을 맹목적으로 따르는 것을 경멸합니다. 규칙의 본질과 이유를 이해하고 그것을 자신의 방식으로 재해석하는 이 태도가 ENTP의 반항적 창의성을 잘 담습니다."),
            ("당신이 상상할 수 있다면, 당신은 그것을 창조할 수 있다.",
             "윌리엄 아서 워드",
             "ENTP는 아이디어를 현실로 만드는 데 거침이 없습니다. 상상과 실현 사이의 거리를 두려움이 아닌 도전으로 여기는 이 철학이 ENTP의 혁신 정신과 일치합니다."),
            ("새로운 아이디어의 표식은 처음에는 불가능해 보인다는 것이다.",
             "아서 클라크",
             "ENTP는 '불가능'이라는 말을 가장 흥미로운 도전으로 받아들입니다. 혁신적 아이디어가 처음에는 항상 비웃음을 산다는 이 통찰이 ENTP에게 큰 위안과 동기가 됩니다."),
            ("현상 유지는 아무것도 하지 않는 것과 같다.",
             "버락 오바마",
             "ENTP는 변화와 혁신 없는 안정을 정체로 봅니다. 현상 유지에 만족하지 않고 끊임없이 새로운 가능성을 탐색하는 ENTP의 본능을 이 명언이 대변합니다."),
            ("토론은 생각을 날카롭게 한다.",
             "볼테르",
             "ENTP는 토론 자체를 즐기며 진실에 더 가까이 다가가기 위해 논쟁합니다. 지적 유희로서의 토론 철학이 ENTP의 본성과 완벽히 맞습니다."),
        ],
    },
    "INFJ": {
        "emoji": "🌌", "name": "옹호자",
        "gradient": "linear-gradient(135deg, #2E4057 0%, #5C6BC0 100%)",
        "traits": ["통찰력", "이상주의", "헌신적", "예언적"],
        "quotes": [
            ("당신이 세상에서 보고 싶은 변화 자체가 되어라.",
             "마하트마 간디",
             "INFJ는 세상의 변화를 외부에서 기다리지 않고 자신이 그 변화의 시작점이 되려 합니다. 내면의 신념을 삶으로 구현하려는 INFJ의 이상주의적 헌신을 완벽히 담은 명언입니다."),
            ("어둠은 어둠을 몰아낼 수 없다. 오직 빛만이 그럴 수 있다.",
             "마틴 루터 킹 주니어",
             "INFJ는 갈등을 맞대응으로 해결하지 않고 근본적인 선함으로 극복하려 합니다. 이 비폭력적 변화에 대한 믿음이 INFJ의 깊은 인문주의적 세계관과 공명합니다."),
            ("다른 사람을 위한 삶이 가치 있는 삶이다.",
             "알버트 아인슈타인",
             "INFJ는 자신의 재능을 타인과 세상을 위해 쓸 때 진정한 의미를 느낍니다. 이타적 삶에서 의미를 찾는 이 철학이 INFJ의 헌신적 본성을 잘 표현합니다."),
            ("깊은 곳에서 인류는 하나다.",
             "롤먼 타고르",
             "INFJ는 표면적 차이 너머의 본질적 연결을 직관적으로 감지합니다. 인류의 근원적 연대를 강조하는 이 철학적 통찰이 INFJ의 깊은 공감 능력과 일치합니다."),
            ("당신의 목적이 크면, 실패조차 의미가 있다.",
             "J.K. 롤링",
             "INFJ는 결과보다 의미와 목적을 중시합니다. 실패조차 큰 목적 안에서 의미를 가진다는 이 관점이 INFJ가 역경을 견디는 내면의 힘과 맞닿아 있습니다."),
        ],
    },
    "INFP": {
        "emoji": "🌿", "name": "중재자",
        "gradient": "linear-gradient(135deg, #2D6A4F 0%, #52B788 100%)",
        "traits": ["공감능력", "이상주의", "창의적", "내향적"],
        "quotes": [
            ("당신은 충분히 존재한다. 충분히 가졌다. 충분히 행한다.",
             "브레네 브라운",
             "INFP는 완벽하지 않은 자신을 자책하는 경향이 있습니다. 지금 이 순간의 자신이 이미 충분하다는 이 메시지는 INFP가 가장 필요로 하는 따뜻한 위로입니다."),
            ("나는 꿈꾸기 때문에 산다. 꿈이 없다면 살아갈 이유가 없다.",
             "어슐러 K. 르 귄",
             "INFP는 꿈과 이상을 삶의 에너지원으로 삼습니다. 현실에 안주하지 않고 더 아름다운 세계를 상상하며 살아가는 INFP의 본질을 이 명언이 담아냅니다."),
            ("세상을 바꾸는 가장 간단한 방법은 내 마음을 바꾸는 것이다.",
             "버크민스터 풀러",
             "INFP는 변화의 시작이 내면에 있다고 믿습니다. 외부 세계를 바꾸기 전에 자신의 내면을 먼저 탐구하고 변화시키는 이 접근이 INFP의 내향적 이상주의와 잘 맞습니다."),
            ("상처받지 않은 영혼은 없다. 그러나 그 상처에서 꽃이 핀다.",
             "루미",
             "INFP는 아픔과 취약함을 창의성과 공감의 원천으로 전환하는 능력이 있습니다. 상처에서 아름다움을 피워내는 이 시적 통찰이 INFP의 감성 세계를 완벽히 표현합니다."),
            ("너 자신에게 친절하라. 당신이 대하는 모든 이들은 힘든 싸움을 하고 있다.",
             "플라톤",
             "INFP는 타인에게는 무한한 공감을 베풀지만 자신에게는 가혹한 경우가 많습니다. 자기 자신도 타인과 같은 친절함을 받을 자격이 있다는 이 명언이 INFP에게 꼭 필요한 메시지입니다."),
        ],
    },
    "ENFJ": {
        "emoji": "🌟", "name": "선도자",
        "gradient": "linear-gradient(135deg, #6A0572 0%, #C77DFF 100%)",
        "traits": ["따뜻함", "리더십", "공감", "영감을 줌"],
        "quotes": [
            ("최고의 방법으로 사람들을 이끄는 것은 그들에게 길을 보여주는 것이다.",
             "소크라테스",
             "ENFJ는 지시가 아닌 모범과 영감으로 이끕니다. 길을 직접 걸어 보여주는 이 리더십 방식이 ENFJ가 사람들에게 자연스럽게 영향을 미치는 방법과 일치합니다."),
            ("한 사람의 삶에 변화를 주는 것이 세상을 바꾸는 것이다.",
             "앤 프랭크",
             "ENFJ는 거창한 변화보다 한 사람 한 사람에게 실질적인 영향을 미치는 것을 중시합니다. 개인의 변화가 곧 세상의 변화라는 이 믿음이 ENFJ의 인간 중심 철학입니다."),
            ("좋은 리더는 먼저 섬기고, 그 다음 이끈다.",
             "로버트 그린리프",
             "ENFJ는 권위보다 봉사의 마음으로 리더십을 발휘합니다. 섬김의 자세에서 진정한 영향력이 나온다는 이 철학이 ENFJ의 헌신적 리더십 방식과 딱 들어맞습니다."),
            ("당신의 친절은 당신이 가진 최고의 힘이다.",
             "마더 테레사",
             "ENFJ는 친절을 가장 강력한 사회적 힘으로 이해합니다. 온기와 배려가 세상을 움직이는 진정한 동력이라는 이 통찰이 ENFJ의 핵심 가치를 대변합니다."),
            ("사람들이 중요하다고 느끼게 만들어라, 그러면 그들은 중요해질 것이다.",
             "메리 케이 애시",
             "ENFJ는 타인의 잠재력을 먼저 알아보고 그것을 이끌어냅니다. 인정과 존중이 사람을 성장시킨다는 이 믿음이 ENFJ가 주변을 변화시키는 핵심 방법입니다."),
        ],
    },
    "ENFP": {
        "emoji": "🎆", "name": "활동가",
        "gradient": "linear-gradient(135deg, #FF9500 0%, #FF5500 100%)",
        "traits": ["열정적", "창의적", "자유로운", "사교적"],
        "quotes": [
            ("인생은 용기 있는 모험이거나 아무것도 아니다.",
             "헬렌 켈러",
             "ENFP는 삶을 안전한 루틴이 아닌 끊임없는 탐험으로 봅니다. 가능성을 향해 용감히 뛰어드는 모험가 정신이 ENFP의 생동감 넘치는 삶의 방식을 정확히 표현합니다."),
            ("당신이 사랑하는 일을 하라, 그러면 일생에 하루도 일한 날이 없을 것이다.",
             "공자",
             "ENFP는 열정과 일치하지 않는 삶을 오래 유지하지 못합니다. 사랑하는 일에 삶을 바치는 것이 최고의 행복이라는 이 믿음이 ENFP의 진로 철학과 완벽히 맞습니다."),
            ("미래는 꿈의 아름다움을 믿는 사람들의 것이다.",
             "엘리너 루즈벨트",
             "ENFP는 아직 존재하지 않는 것을 상상하고 그것을 현실로 만들려는 낙관적 에너지를 가집니다. 꿈을 믿는 용기가 미래를 만든다는 이 메시지가 ENFP에게 깊이 울립니다."),
            ("가능성 속에 살라.",
             "에밀리 디킨슨",
             "ENFP는 확정된 현실보다 열려 있는 가능성의 공간에서 가장 빛납니다. 무한한 선택지와 잠재력 속에서 살아가는 이 철학이 ENFP의 자유로운 영혼을 담아냅니다."),
            ("즐겁게 사는 것이 최고의 복수다.",
             "조지 허버트",
             "ENFP는 부정적인 상황이나 사람에 에너지를 낭비하지 않고 자신의 기쁨을 최고의 답으로 삼습니다. 이 유쾌한 삶의 태도가 ENFP의 회복탄력성을 잘 표현합니다."),
        ],
    },
    "ISTJ": {
        "emoji": "📋", "name": "물류관리자",
        "gradient": "linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%)",
        "traits": ["책임감", "신뢰성", "체계적", "근면"],
        "quotes": [
            ("규율은 목표와 성취 사이의 다리다.",
             "짐 론",
             "ISTJ는 꾸준한 규율과 원칙을 통해 목표를 달성합니다. 화려한 재능보다 일관된 실천이 결과를 만든다는 이 철학이 ISTJ의 근면함과 완벽히 일치합니다."),
            ("작은 일에 성실한 사람이 큰 일도 해낸다.",
             "루크복음 16:10",
             "ISTJ는 어떤 일도 소홀히 하지 않고 맡은 바를 끝까지 완수합니다. 작은 책임을 신뢰롭게 이행하는 것이 큰 성취의 기반이라는 이 원칙이 ISTJ의 성실함을 대변합니다."),
            ("탁월함은 한 번의 행동이 아니라 습관이다.",
             "아리스토텔레스",
             "ISTJ는 뛰어난 성과가 타고난 재능이 아닌 일관된 습관에서 나온다고 믿습니다. 꾸준함을 탁월함의 조건으로 보는 이 철학이 ISTJ의 본질을 담아냅니다."),
            ("무엇이든 할 가치가 있다면, 제대로 할 가치가 있다.",
             "필립 체스터필드",
             "ISTJ는 어설프게 하느니 하지 않는 것이 낫다고 생각합니다. 완성도와 정확성에 대한 이 높은 기준이 ISTJ의 완벽주의적 성실함을 잘 표현합니다."),
            ("신뢰는 쌓는 데 오래 걸리고 무너지는 건 한순간이다.",
             "작자 미상",
             "ISTJ는 신뢰를 가장 소중한 자산으로 여기며 그것을 지키기 위해 일관된 행동을 합니다. 신뢰의 소중함을 이보다 더 잘 표현한 명언은 없습니다."),
        ],
    },
    "ISFJ": {
        "emoji": "🛡️", "name": "수호자",
        "gradient": "linear-gradient(135deg, #2C5F2E 0%, #74C69D 100%)",
        "traits": ["헌신적", "배려", "신뢰성", "따뜻함"],
        "quotes": [
            ("사랑은 행동이지 감정이 아니다.",
             "스티브 마라볼리",
             "ISFJ는 사랑을 말이 아닌 행동으로 표현합니다. 조용하지만 꾸준히 타인을 돌보고 지원하는 ISFJ의 실천적 사랑 방식을 이 명언이 정확히 담아냅니다."),
            ("당신이 할 수 있는 가장 큰 일은 다른 사람을 돕는 것이다.",
             "마하트마 간디",
             "ISFJ는 타인을 돕는 것에서 삶의 가장 큰 의미를 찾습니다. 헌신과 봉사가 삶의 가장 숭고한 목적이라는 이 철학이 ISFJ의 이타적 본성과 공명합니다."),
            ("배려하는 마음을 가진 사람이 세상을 더 나은 곳으로 만든다.",
             "헨리 제임스",
             "ISFJ는 조용하지만 강력한 방식으로 주변을 더 따뜻하고 살기 좋은 곳으로 만듭니다. 배려 자체가 세상을 변화시키는 힘이라는 이 믿음이 ISFJ의 역할을 대변합니다."),
            ("작은 친절이 세상을 더 살기 좋은 곳으로 만든다.",
             "작자 미상",
             "ISFJ는 거창한 제스처보다 일상의 작은 친절을 꾸준히 실천합니다. 그 작은 친절들이 쌓여 세상을 바꾼다는 이 메시지가 ISFJ의 가치관과 완벽히 일치합니다."),
            ("당신의 존재 자체가 누군가에게 선물이다.",
             "작자 미상",
             "ISFJ는 자신의 가치를 과소평가하는 경향이 있습니다. 조용히 헌신하고 돌보는 ISFJ의 존재 자체가 주변 사람들에게 얼마나 큰 의미인지를 일깨우는 명언입니다."),
        ],
    },
    "ESTJ": {
        "emoji": "⚖️", "name": "경영자",
        "gradient": "linear-gradient(135deg, #5C4033 0%, #A0522D 100%)",
        "traits": ["결단력", "관리능력", "책임감", "실용적"],
        "quotes": [
            ("질서는 자연의 첫 번째 법칙이다.",
             "알렉산더 포프",
             "ESTJ는 명확한 구조와 질서 속에서 최고의 효율을 발휘합니다. 질서를 모든 시스템의 근본으로 보는 이 철학이 ESTJ의 체계적 성향을 완벽히 대변합니다."),
            ("성공하는 사람은 행동한다. 실패하는 사람은 계획만 한다.",
             "파블로 피카소",
             "ESTJ는 이론보다 실행을 중시합니다. 분석과 준비에 무한정 시간을 쏟기보다 결단하고 행동하는 ESTJ의 실용적 추진력을 이 명언이 잘 표현합니다."),
            ("위대한 결과는 의지로 만들어진다.",
             "나폴레온 힐",
             "ESTJ는 강한 의지와 집중력으로 목표를 반드시 달성합니다. 성취의 핵심이 환경이나 운이 아닌 결단력과 의지라는 이 철학이 ESTJ의 자기 확신과 맞습니다."),
            ("지도자란 희망을 나눠주는 상인이다.",
             "나폴레옹",
             "ESTJ는 불확실한 상황에서도 방향을 제시하고 팀에 확신을 심어줍니다. 리더의 가장 중요한 역할이 희망의 전달임을 강조한 이 명언이 ESTJ의 리더십 철학과 일치합니다."),
            ("원칙 없이 성공은 없다.",
             "존 D. 록펠러",
             "ESTJ는 확고한 원칙과 기준을 갖고 그것을 타협 없이 지킵니다. 원칙을 성공의 전제 조건으로 보는 이 철학이 ESTJ의 규범 중심적 가치관을 담아냅니다."),
        ],
    },
    "ESFJ": {
        "emoji": "🤗", "name": "집정관",
        "gradient": "linear-gradient(135deg, #C2185B 0%, #FF69B4 100%)",
        "traits": ["사교적", "배려심", "충성스러움", "협력적"],
        "quotes": [
            ("혼자 가면 빠르게 갈 수 있지만, 함께 가면 멀리 갈 수 있다.",
             "아프리카 속담",
             "ESFJ는 개인의 성취보다 함께 이루는 것의 가치를 더 높이 삽니다. 협력과 공동체의 힘을 믿는 이 철학이 ESFJ의 사교적 협력 지향 성향을 완벽히 표현합니다."),
            ("삶에서 가장 소중한 것은 우리가 나누는 관계다.",
             "작자 미상",
             "ESFJ는 인간관계를 삶의 중심으로 삼습니다. 소유나 성취가 아닌 연결과 관계에서 최고의 가치를 찾는 이 철학이 ESFJ의 사람 중심 삶의 방식과 일치합니다."),
            ("진정한 친구는 당신의 잠재력을 보는 사람이다.",
             "헨리 데이비드 소로",
             "ESFJ는 타인의 장점과 가능성을 먼저 보고 그것을 응원합니다. 관계 속에서 서로의 잠재력을 발견하고 키워주는 이 따뜻한 우정 철학이 ESFJ의 본성과 맞습니다."),
            ("친절은 전염된다. 오늘 친절을 베풀어라.",
             "작자 미상",
             "ESFJ는 자신의 친절이 주변으로 퍼져나가 더 따뜻한 공동체를 만든다고 믿습니다. 친절의 연쇄 반응을 믿는 이 철학이 ESFJ가 매일 실천하는 삶의 방식입니다."),
            ("사랑받고 싶다면 먼저 사랑하라.",
             "벤저민 프랭클린",
             "ESFJ는 관계에서 먼저 베푸는 사람입니다. 사랑과 인정을 받기 위해 먼저 주는 것에서 시작한다는 이 원칙이 ESFJ가 인간관계를 맺는 방식의 핵심입니다."),
        ],
    },
    "ISTP": {
        "emoji": "🔧", "name": "장인",
        "gradient": "linear-gradient(135deg, #4A4A4A 0%, #808080 100%)",
        "traits": ["실용적", "분석적", "독립적", "침착"],
        "quotes": [
            ("말이 아닌 행동이 사람을 증명한다.",
             "작자 미상",
             "ISTP는 말수가 적고 행동으로 자신을 표현합니다. 긴 설명보다 실제 결과물로 가치를 증명하는 이 태도가 ISTP의 과묵하고 실용적인 본성을 완벽히 담아냅니다."),
            ("가장 좋은 도구는 실제로 작동하는 도구다.",
             "작자 미상",
             "ISTP는 이론적 완벽함보다 실제 작동 여부를 더 중시합니다. 기능과 효율을 최우선으로 보는 이 실용적 철학이 ISTP의 장인 정신과 일치합니다."),
            ("침묵은 가장 강력한 대화다.",
             "작자 미상",
             "ISTP는 말보다 침묵과 행동으로 더 많은 것을 전달합니다. 불필요한 말을 아끼고 핵심만 전달하는 ISTP의 과묵한 의사소통 방식을 이 명언이 잘 대변합니다."),
            ("가장 복잡한 문제도 단순한 해결책을 가지고 있다.",
             "작자 미상",
             "ISTP는 복잡한 상황을 빠르게 분석하고 가장 효율적인 해결책을 찾아냅니다. 단순함 속에서 해답을 찾는 이 실용적 문제 해결 능력이 ISTP의 장점입니다."),
            ("경험은 최고의 선생이다.",
             "율리우스 카이사르",
             "ISTP는 책보다 직접 경험을 통해 가장 잘 배웁니다. 이론이 아닌 실제 경험에서 지식을 쌓는 이 학습 방식이 ISTP의 체험적 이해 방식과 완벽히 맞습니다."),
        ],
    },
    "ISFP": {
        "emoji": "🎨", "name": "모험가",
        "gradient": "linear-gradient(135deg, #C0392B 0%, #FF7F7F 100%)",
        "traits": ["예술적", "감성적", "자유로운", "친절"],
        "quotes": [
            ("삶은 예술이다. 당신이 그 예술가다.",
             "작자 미상",
             "ISFP는 삶 자체를 창작 행위로 봅니다. 매 순간을 캔버스 위의 붓질처럼 감각적으로 살아가는 ISFP의 예술적 삶의 태도를 이 명언이 아름답게 표현합니다."),
            ("아름다움은 보는 사람의 눈 속에 있다.",
             "마가렛 헌게르포드",
             "ISFP는 남들이 지나치는 것에서 아름다움을 발견하는 특별한 감수성을 가집니다. 아름다움은 절대적 기준이 아닌 개인의 감성에 있다는 이 철학이 ISFP의 감각을 대변합니다."),
            ("순간 속에 살아라. 그것이 진정한 삶이다.",
             "작자 미상",
             "ISFP는 과거의 후회나 미래의 걱정보다 지금 이 순간의 경험을 가장 소중히 여깁니다. 현재에 온전히 존재하는 이 마음 챙김 철학이 ISFP의 삶의 방식입니다."),
            ("진정한 자유는 자신을 표현하는 것이다.",
             "오스카 와일드",
             "ISFP는 타인의 기대보다 자신의 내면을 표현하는 것에서 자유를 찾습니다. 진정한 해방이 자기 표현에 있다는 이 예술적 철학이 ISFP의 자유로운 영혼과 맞닿아 있습니다."),
            ("당신이 느끼는 것이 당신이 창조하는 것이다.",
             "작자 미상",
             "ISFP는 깊은 감정과 감각을 예술과 행동으로 표현합니다. 내면의 감정이 창작의 원천이 된다는 이 믿음이 ISFP의 감성적 창의성을 완벽히 담아냅니다."),
        ],
    },
    "ESTP": {
        "emoji": "⚡", "name": "사업가",
        "gradient": "linear-gradient(135deg, #B8860B 0%, #FFD700 100%)",
        "traits": ["행동파", "현실적", "에너지 넘침", "대담"],
        "quotes": [
            ("생각만 하는 자는 아무것도 이루지 못한다. 행동하라!",
             "요한 볼프강 폰 괴테",
             "ESTP는 분석과 계획보다 즉각적인 행동을 선호합니다. 아이디어는 실행될 때만 가치가 있다는 이 행동 지향적 철학이 ESTP의 폭발적 추진력을 완벽히 대변합니다."),
            ("기회는 춤추고 있는 사람들에게 온다.",
             "작자 미상",
             "ESTP는 기회를 기다리지 않고 만들어냅니다. 활발하게 움직이고 참여하는 사람에게 기회가 찾아온다는 이 역동적 철학이 ESTP의 에너지 넘치는 삶의 방식과 일치합니다."),
            ("지금 이 순간이 전부다.",
             "작자 미상",
             "ESTP는 현재에 집중하고 지금 주어진 상황에서 최대한을 뽑아냅니다. 과거에 연연하거나 미래를 걱정하기보다 현재의 행동에 집중하는 이 철학이 ESTP의 본성입니다."),
            ("겁쟁이는 죽기 전에 여러 번 죽고, 용감한 자는 한 번만 죽는다.",
             "윌리엄 셰익스피어",
             "ESTP는 두려움보다 행동을 선택합니다. 지나친 망설임이 오히려 더 큰 손해를 부른다는 이 대담한 철학이 ESTP의 위험을 감수하는 용기 있는 성향과 맞습니다."),
            ("언제나 지금이 시작하기 가장 좋은 때다.",
             "작자 미상",
             "ESTP는 완벽한 타이밍을 기다리지 않고 지금 당장 시작합니다. 행동의 가장 좋은 시점은 항상 현재라는 이 실행 중심 철학이 ESTP의 즉흥적 결단력을 담아냅니다."),
        ],
    },
    "ESFP": {
        "emoji": "🎉", "name": "연예인",
        "gradient": "linear-gradient(135deg, #C0392B 0%, #FF4500 100%)",
        "traits": ["활발함", "즉흥적", "사교적", "낙관적"],
        "quotes": [
            ("오늘을 춤처럼 살아라, 내일이 없는 것처럼.",
             "작자 미상",
             "ESFP는 지금 이 순간을 온전히 즐기는 능력이 탁월합니다. 매 순간을 최대한 열정적으로 살아가는 이 자유로운 철학이 ESFP의 즉흥적 생동감을 완벽히 표현합니다."),
            ("웃음은 영혼의 음악이다.",
             "작자 미상",
             "ESFP는 어디에 있든 분위기를 밝게 만들고 웃음을 만들어냅니다. 기쁨과 유머가 삶의 본질적 양식이라는 이 철학이 ESFP의 천성적인 엔터테이너 기질과 일치합니다."),
            ("삶은 파티다. 당신이 주인공이다.",
             "작자 미상",
             "ESFP는 어떤 상황에서도 주인공으로서의 에너지를 발산합니다. 삶 자체를 축제로 보고 그 중심에 당당히 서는 이 태도가 ESFP의 빛나는 존재감을 담아냅니다."),
            ("행복은 스스로 만드는 것이다.",
             "에이브러햄 링컨",
             "ESFP는 행복을 수동적으로 기다리지 않고 스스로 만들어냅니다. 주변 환경에 의존하지 않고 자신이 행복의 주체가 된다는 이 적극적 삶의 자세가 ESFP의 낙관주의를 대변합니다."),
            ("오늘의 기쁨이 내일의 힘이 된다.",
             "작자 미상",
             "ESFP는 현재의 기쁨과 즐거움이 앞으로 나아갈 에너지가 된다고 믿습니다. 즐거움을 내일을 위한 투자로 보는 이 긍정적 관점이 ESFP의 낙천적 회복력과 맞습니다."),
        ],
    },
}

GROUPS = {
    "🔮 분석가": ["INTJ", "INTP", "ENTJ", "ENTP"],
    "🌈 외교관": ["INFJ", "INFP", "ENFJ", "ENFP"],
    "🏛️ 관리자": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
    "🌊 탐험가": ["ISTP", "ISFP", "ESTP", "ESFP"],
}

# ─────────────────────────────────────────
#  커스텀 이펙트 함수 (JS 파티클)
# ─────────────────────────────────────────
def launch_effect(mbti_type: str):
    eff = EFFECTS[mbti_type]
    direction = eff["dir"]
    # Python list → JS array string
    p_list = "[" + ",".join([f'"{p}"' for p in eff["particles"]]) + "]"

    if direction == "fall":
        anim_name = "fall_anim"
        start_css = "top:-60px"
        end_css   = "top:110vh"
    else:
        anim_name = "rise_anim"
        start_css = "bottom:-60px"
        end_css   = "bottom:110vh"

    st.markdown(f"""
    <style>
    @keyframes {anim_name} {{
        0%   {{ {start_css}; opacity:1; transform:rotate(0deg) scale(1); }}
        80%  {{ opacity:1; }}
        100% {{ {end_css}; opacity:0; transform:rotate(720deg) scale(0.4); }}
    }}
    </style>
    <div id="effect_trigger_{mbti_type}" style="display:none;"></div>
    <script>
    (function() {{
        var particles = {p_list};
        var animName  = "{anim_name}";
        var startProp = "{start_css.split(':')[0]}";
        for (var i = 0; i < 45; i++) {{
            var el = document.createElement('div');
            el.innerHTML = particles[Math.floor(Math.random() * particles.length)];
            var size     = Math.random() * 22 + 14;
            var delay    = Math.random() * 1.8;
            var duration = Math.random() * 2.5 + 2;
            var left     = Math.random() * 98;
            el.style.cssText = [
                'position:fixed',
                startProp + ':-60px',
                'left:' + left + 'vw',
                'font-size:' + size + 'px',
                'animation:' + animName + ' ' + duration + 's ' + delay + 's linear forwards',
                'z-index:99999',
                'pointer-events:none',
                'user-select:none'
            ].join(';');
            document.body.appendChild(el);
            (function(elem, dur, del) {{
                setTimeout(function() {{ elem.remove(); }}, (dur + del + 0.5) * 1000);
            }})(el, duration, delay);
        }}
    }})();
    </script>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
#  UI
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
                if st.button(
                    f"{info['emoji']} {mbti_type}\n{info['name']}",
                    key=f"btn_{mbti_type}",
                    use_container_width=True,
                ):
                    st.session_state["selected"]      = mbti_type
                    st.session_state["quote_idx"]     = random.randint(0, len(info["quotes"]) - 1)
                    st.session_state["quote_type"]    = mbti_type
                    st.session_state["trigger_effect"] = True

st.divider()

# ── 결과 출력 ──
if "selected" in st.session_state:
    sel  = st.session_state["selected"]
    info = MBTI_DATA[sel]
    eff  = EFFECTS[sel]

    # 이펙트 발동
    if st.session_state.get("trigger_effect"):
        launch_effect(sel)
        st.session_state["trigger_effect"] = False

    # 이펙트 설명 라벨
    st.markdown(
        f'<div class="effect-label">{eff["desc"]}</div>',
        unsafe_allow_html=True,
    )

    # MBTI 카드
    traits_html = "".join([f'<span class="trait-tag">#{t}</span>' for t in info["traits"]])
    st.markdown(f"""
    <div class="mbti-card" style="background:{info['gradient']};">
        <div class="type-badge">{sel}</div>
        <div style="font-size:2.5rem;margin:8px 0;">{info['emoji']}</div>
        <div style="font-size:1.2rem;font-weight:700;margin-bottom:12px;">{info['name']}</div>
        <div>{traits_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # 명언 + 이유 출력
    q_idx = st.session_state.get("quote_idx", 0)
    q_text, q_author, q_reason = info["quotes"][q_idx]

    st.markdown(f"""
    <div class="quote-box">
        <div style="font-size:2rem;margin-bottom:8px;">💬</div>
        <div>"{q_text}"</div>
        <div class="author-text">— {q_author}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="reason-box">
        <div style="font-weight:700;font-size:1rem;margin-bottom:8px;">🧩 이 명언을 추천한 이유</div>
        <div>{q_reason}</div>
    </div>
    """, unsafe_allow_html=True)

    # 다른 명언 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔀 다른 명언 보기", use_container_width=True):
            current = st.session_state["quote_idx"]
            options = [i for i in range(len(info["quotes"])) if i != current]
            st.session_state["quote_idx"] = random.choice(options)
            st.rerun()
else:
    st.markdown("""
    <div style="text-align:center; padding:40px; color:#888; font-size:1.1rem;">
        ☝️ 위에서 MBTI 유형을 선택해 보세요!
    </div>
    """, unsafe_allow_html=True)

# ── 푸터 ──
st.divider()
st.markdown(
    "<div style='text-align:center;color:#aaa;font-size:0.8rem;'>✨ MBTI 명언 추천기 | Made with Streamlit 🧠</div>",
    unsafe_allow_html=True,
)
