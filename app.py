import random
import streamlit as st

st.set_page_config(
    page_title="AI 판사: 균형의 법정 v12.2",
    page_icon="⚖️",
    layout="wide"
)

# ---------------------------------------------------------
# 판사 사법 성향 진단 로직
# ---------------------------------------------------------
def analyze_judge_persona(humanity, law, public, trust):
    if law >= 65 and humanity < 45:
        return {
            "title": "⚖️ 엄격한 법치주의 원칙관",
            "desc": "법조문과 객관적 증거를 철저히 존중하며 엄벌을 통해 법의 엄정함을 세우는 스타일입니다."
        }
    elif humanity >= 65 and law < 45:
        return {
            "title": "❤️ 온건한 인권 중심 재판관",
            "desc": "피고인의 성장 환경, 교화 가능성, 심신 상태를 깊이 참작하는 스타일입니다."
        }
    elif public >= 65 and trust >= 65:
        return {
            "title": "🛡️ 사회 안전 및 공익 수호관",
            "desc": "공공의 안전과 법질서 유지, 사회적 신뢰 회복을 최우선으로 고려하는 스타일입니다."
        }
    else:
        return {
            "title": "⚖️ 균형 잡힌 중용의 사법관",
            "desc": "법적 엄격함과 피고인의 사정, 공공의 이익을 다각도로 양립시키는 성숙한 재판 스타일입니다."
        }

# ---------------------------------------------------------
# 사건 데이터베이스 (총 50개: 무죄 25 / 무기 15 / 유기 10)
# ---------------------------------------------------------
ALL_CASES = [
    # --- [무죄 판례 25개] ---
    {
        "id": "m_01",
        "title": "치과의사 모녀 살인 사건",
        "category": "무죄 판례 / 간접증거와 무죄추정",
        "story": "출근한 치과의사 남편이 집을 나선 후 아내와 딸이 안방 욕조에서 숨진 채 발견되었습니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "수온 변화와 체온 감정 결과 출근 전 살해함이 명백하므로 사형에 처해야 합니다.",
        "defense": "사망시각 법의학 오차가 크며 직접증거가 없으므로 무죄입니다.",
        "ev2": "[정밀감정] 욕조 수온 식는 속도 오차로 정확한 사망 시각 특정이 불가능함이 확인됨.",
        "real_verdict": "무죄 확정 (대법원)",
        "real_reason": "간접증거만으로는 합리적 의심을 배척할 만큼 범죄가 입증되지 않아 무죄 확정.",
        "choices": [
            {"label": "증거불충분으로 무죄 선고", "effects": {"humanity": 10, "law": 15, "public": -5, "trust": 10}},
            {"label": "정황증거 인정으로 사형 선고 (유죄)", "effects": {"humanity": -15, "law": -15, "public": 10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 사망시각 불특정에 따른 무죄 확정", "effects": {"humanity": 10, "law": 15, "public": -5, "trust": 15}},
            {"label": "⚖️ [보강판결] 정황증거 인정으로 무기징역 선고", "effects": {"humanity": -10, "law": -10, "public": 5, "trust": -5}}
        ]
    },
    {
        "id": "m_02",
        "title": "낙동강 변 자갈타이어 살인 사건",
        "category": "무죄 판례 / 고문 자백과 재심 무죄",
        "story": "낙동강 변에서 발생한 살인 사건으로 체포되어 자백했으나, 21년 뒤 고문에 의한 허위 자백임이 밝혀졌습니다.",
        "img1": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "prosecution": "당시 자백 진술이 구체적이므로 기존 유죄 판결이 유지되어야 합니다.",
        "defense": "불법 체포 및 물고문으로 인한 허위 자백이므로 무죄입니다.",
        "ev2": "[재심 조사] 수사관들의 불법 감금 및 물고문 정황과 위법 수사가 공식 확인됨.",
        "real_verdict": "재심 무죄 확정 (대법원)",
        "real_reason": "고문으로 얻은 자백은 증거능력이 없으며 이를 제외하면 범행 입증 증거가 없음.",
        "choices": [
            {"label": "위법수사 증거 배제 및 무죄 선고", "effects": {"humanity": 15, "law": 15, "public": 5, "trust": 20}},
            {"label": "기존 자백 인정 및 무기징역 유지", "effects": {"humanity": -20, "law": -20, "public": -10, "trust": -25}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 불법고문 인정 피고인 전원 무죄 선고", "effects": {"humanity": 15, "law": 20, "public": 5, "trust": 20}},
            {"label": "⚖️ [보강판결] 증거 일부 인정 감형 선고", "effects": {"humanity": -10, "law": -10, "public": -5, "trust": -15}}
        ]
    },
    {
        "id": "m_03",
        "title": "삼례 나라슈퍼 강도치사 사건",
        "category": "무죄 판례 / 강압수사 재심 무죄",
        "story": "슈퍼마켓 강도 사건으로 지적장애 청소년 3명이 범인으로 처벌받았으나 훗날 진범이 나타났습니다.",
        "img1": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "당시 현장 검증 자백이 존재하므로 유죄가 타당합니다.",
        "defense": "지적장애에 대한 폭행 및 강압 수사로 만든 거짓 자백입니다.",
        "ev2": "[진범 자백] 진범의 유류품 일치 증거 및 진술 확보.",
        "real_verdict": "재심 무죄 확정 (대법원)",
        "real_reason": "진범의 자백과 경찰 강압 수사 입증으로 무죄 선고.",
        "choices": [
            {"label": "무죄 선고", "effects": {"humanity": 15, "law": 15, "public": 0, "trust": 15}},
            {"label": "유죄 선고", "effects": {"humanity": -15, "law": -15, "public": 0, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 진범 확인에 따른 무죄 확정", "effects": {"humanity": 15, "law": 20, "public": 5, "trust": 20}},
            {"label": "⚖️ [보강판결] 자백 인정 유죄 선고", "effects": {"humanity": -15, "law": -15, "public": -5, "trust": -15}}
        ]
    },
    {
        "id": "m_04",
        "title": "약촌오거리 택시기사 살인 사건",
        "category": "무죄 판례 / 목격자 누명 재심 무죄",
        "story": "택시기사 살인 사건의 최초 목격자였던 10대 청소년이 수사 기관의 폭행으로 누명을 쓴 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1508962914676-134849a727f0?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "prosecution": "자백 진술의 구체성이 인정되므로 유죄입니다.",
        "defense": "경찰의 여관 감금 및 가혹행위로 인한 허위 자백입니다.",
        "ev2": "[재심 증거] 칼의 모양과 상해 형태가 피고인 자백과 불일치함 확인.",
        "real_verdict": "재심 무죄 확정 (대법원)",
        "real_reason": "가혹행위로 얻은 자백의 증거능력 배제 및 무죄 판결.",
        "choices": [
            {"label": "무죄 선고", "effects": {"humanity": 15, "law": 15, "public": 5, "trust": 15}},
            {"label": "유죄 유지", "effects": {"humanity": -15, "law": -15, "public": -5, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 가혹행위 입증에 따른 무죄 선고", "effects": {"humanity": 15, "law": 20, "public": 5, "trust": 20}},
            {"label": "⚖️ [보강판결] 유죄 유지 선고", "effects": {"humanity": -15, "law": -15, "public": -5, "trust": -15}}
        ]
    },
    {
        "id": "m_05",
        "title": "춘천 파호식당 여굴 살인 사건",
        "category": "무죄 판례 / 허위자백 재심 무죄",
        "story": "파호식당 여주인 살해 혐의로 15년간 복역한 파출소장이 고문에 의한 허위자백이었음을 주장한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "자백 진술 및 유류품 발견 정황으로 볼 때 유죄입니다.",
        "defense": "잠 안 재우기와 고문에 의한 가혹행위 자백이었습니다.",
        "ev2": "[재심 검증] 수사 기록상의 유류품 조작 정황 및 가혹행위 입증.",
        "real_verdict": "재심 무죄 확정 (대법원)",
        "real_reason": "고문 자백 배제 및 공소사실 입증 부족으로 무죄 확정.",
        "choices": [
            {"label": "무죄 선고", "effects": {"humanity": 15, "law": 15, "public": 0, "trust": 15}},
            {"label": "유죄 선고", "effects": {"humanity": -15, "law": -15, "public": 0, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 수사조작 입증 무죄 선고", "effects": {"humanity": 15, "law": 20, "public": 5, "trust": 20}},
            {"label": "⚖️ [보강판결] 유죄 선고", "effects": {"humanity": -15, "law": -15, "public": -5, "trust": -15}}
        ]
    },
    {
        "id": "m_06",
        "title": "고유정 의붓아들 살인 사건 혐의",
        "category": "무죄 판례 / 간접증거 불충분 무죄",
        "story": "고유정이 전 남편 살인과 더불어 의붓아들을 자는 동안 눌러 숨지게 했다는 혐의로 추가 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1553531384-cc64ac80f931?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&q=80",
        "prosecution": "정황 및 약물 검색 기록으로 볼 때 고의 살인입니다.",
        "defense": "친부의 다리에 눌린 단순 압착 사고사 가능성을 배척할 수 없습니다.",
        "ev2": "[국과수 정밀] 타인에 의한 강제 질식과 단순 압착 질식의 구분이 불분명함.",
        "real_verdict": "의붓아들 살인 혐의 무죄 확정 (대법원)",
        "real_reason": "타인에 의한 살해 간접증거가 부족하며 사고사 가능성을 배척하기 어려움.",
        "choices": [
            {"label": "증거불충분 무죄 선고", "effects": {"humanity": 5, "law": 15, "public": -10, "trust": 10}},
            {"label": "정황 인정 유죄 선고", "effects": {"humanity": -10, "law": -15, "public": 10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 압착사 가능성 인정 무죄 확정", "effects": {"humanity": 5, "law": 15, "public": -5, "trust": 10}},
            {"label": "⚖️ [보강판결] 정황증거로 유죄 인정", "effects": {"humanity": -10, "law": -10, "public": 5, "trust": -5}}
        ]
    },
    {
        "id": "m_07",
        "title": "만삭 의사 부인 사망 사건 (1심 무죄 공방)",
        "category": "무죄 판례 / 법의학적 오차 공방",
        "story": "출산을 앞둔 부인이 욕조에서 숨진 채 발견되어 의사 남편이 살인 혐의로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "목 부위 찰과상 및 질식 흔적으로 볼 때 남편에 의한 살인입니다.",
        "defense": "만성 피로로 인한 욕조 낙상 사고사입니다.",
        "ev2": "[해외 법의학자 자문] 단순 낙상 및 이상 자세에 의한 질식사 가능성 제출.",
        "real_verdict": "1심 무죄 (이후 상고심 공방 거침)",
        "real_reason": "합리적 의심을 배척할 정황 입증 부족 시 무죄 취지.",
        "choices": [
            {"label": "무죄 선고", "effects": {"humanity": 10, "law": 15, "public": -5, "trust": 10}},
            {"label": "유죄 선고", "effects": {"humanity": -10, "law": -10, "public": 5, "trust": -5}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 정밀 증거 부족 무죄 선고", "effects": {"humanity": 10, "law": 15, "public": -5, "trust": 10}},
            {"label": "⚖️ [보강판결] 정황 인정 유죄 선고", "effects": {"humanity": -10, "law": -10, "public": 5, "trust": -5}}
        ]
    },
    {
        "id": "m_08",
        "title": "야간 침입자 제압 호신술 사건",
        "category": "무죄 판례 / 정당방위 인정",
        "story": "심야에 집 안에 침입한 흉기 소지 흉한을 집주인이 제압하는 과정에서 흉한이 중상을 입었습니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "과도한 폭행으로 중상을 입혔으므로 상해죄 유죄입니다.",
        "defense": "야간 침입 및 흉기 위협에 대응한 정당방위입니다.",
        "ev2": "[현장 감정] 침입자의 흉기 소지 및 연속 공격 정황 확인.",
        "real_verdict": "무죄 (정당방위 인정)",
        "real_reason": "자신과 가족의 생명을 지키기 위한 불가피한 정당방위 행위임.",
        "choices": [
            {"label": "정당방위 인정 무죄 선고", "effects": {"humanity": 15, "law": 10, "public": 10, "trust": 15}},
            {"label": "과잉방위 인정 유죄(집행유예)", "effects": {"humanity": -10, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 정당방위 원칙에 따른 무죄 확정", "effects": {"humanity": 15, "law": 15, "public": 10, "trust": 15}},
            {"label": "⚖️ [보강판결] 과잉방위 벌금형 선고", "effects": {"humanity": -10, "law": -5, "public": -5, "trust": -10}}
        ]
    },
    {
        "id": "m_09",
        "title": "의료 수술 후 사망 및 과실 사건",
        "category": "무죄 판례 / 의료 과실 인과관계 불성립",
        "story": "복강경 수술을 받은 환자가 사흘 뒤 합병증으로 사망하여 주치의가 업무상과실치사로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "수술 후 경과 관찰 소홀로 인한 명백한 과실입니다.",
        "defense": "의학적 표준 절차를 준수했으며 불가항력적 합병증입니다.",
        "ev2": "[대한의사협회 감정] 최선의 조치를 다했으며 통상적 오차 범위 내 부작용임.",
        "real_verdict": "무죄 확정",
        "real_reason": "의료 행위와 사망 간의 직접적 인과관계 입증 부족.",
        "choices": [
            {"label": "의료과실 미입증 무죄 선고", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "주의의무 위반 인정 유죄 선고", "effects": {"humanity": -10, "law": -15, "public": 5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 의학적 인과관계 부정 무죄 확정", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "⚖️ [보강판결] 금고형 집행유예 선고", "effects": {"humanity": -10, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_10",
        "title": "기업 경영 투자의 배임 혐의 사건",
        "category": "무죄 판례 / 경영상 판단 원칙",
        "story": "기업 대표가 추진한 신사업 투자가 대규모 손실로 이어져 배임 혐의로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "회사에 막대한 손실을 입혔으므로 배임죄가 성립합니다.",
        "defense": "정상적인 이사회 절차를 거친 '경영상 판단'이었습니다.",
        "ev2": "[회계감사 정밀] 투자 당시 타당성 검토 보고서 및 이사회 의결록 확인.",
        "real_verdict": "무죄 확정",
        "real_reason": "경영상 판단의 원칙에 따라 사적 이익 추구가 없는 정상적 투자 행위로 인정.",
        "choices": [
            {"label": "경영상 판단 인정 무죄 선고", "effects": {"humanity": 0, "law": 15, "public": 5, "trust": 10}},
            {"label": "배임죄 적용 유죄 선고", "effects": {"humanity": 0, "law": -15, "public": -5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 경영상 판단 원칙 적용 무죄 확정", "effects": {"humanity": 0, "law": 20, "public": 5, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 3년 선고", "effects": {"humanity": -5, "law": -10, "public": -5, "trust": -10}}
        ]
    },
    {
        "id": "m_11",
        "title": "SNS 비판 게시물 명예훼손 사건",
        "category": "무죄 판례 / 공공의 이익과 위법성 조각",
        "story": "업체의 서비스 불만족 후기를 인터넷 카페에 상세히 적어 정보통신망법상 명예훼손으로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "비방 목적의 허위/비판글로 업체에 손해를 끼쳤습니다.",
        "defense": "다른 소비자들을 위한 '공공의 이익' 목적이었습니다.",
        "ev2": "[게시물 분석] 게시글의 내용이 객관적 사실에 기반하며 비방 목적이 없음.",
        "real_verdict": "무죄 확정",
        "real_reason": "공공의 이익을 위한 게시물로서 위법성이 조각됨.",
        "choices": [
            {"label": "공공의 이익 인정 무죄 선고", "effects": {"humanity": 10, "law": 15, "public": 10, "trust": 15}},
            {"label": "명예훼손 인정 벌금형 선고", "effects": {"humanity": -10, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 위법성 조각사유 인정 무죄 확정", "effects": {"humanity": 10, "law": 15, "public": 10, "trust": 15}},
            {"label": "⚖️ [보강판결] 벌금 200만원 선고", "effects": {"humanity": -10, "law": -10, "public": -5, "trust": -10}}
        ]
    },
    {
        "id": "m_12",
        "title": "음주운전 위법채혈 절차 사건",
        "category": "무죄 판례 / 위법수사 수집증거 배제",
        "story": "음주운전 의심 운전자의 혈액을 영장 없이 강제 동의를 받아 채혈한 수사 절차가 쟁점이 되었습니다.",
        "img1": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "prosecution": "혈중 알코올 농도가 단속 기준을 초과했으므로 유죄입니다.",
        "defense": "적법 영장 없는 채혈은 위법 수사이므로 증거 능력이 없습니다.",
        "ev2": "[절차 검증] 사후 영장 청구 등 적법 절차가 모두 누락되었음.",
        "real_verdict": "무죄 확정",
        "real_reason": "헌법상 적법절차를 위반하여 수집한 증거는 증거능력이 없음.",
        "choices": [
            {"label": "위법증거 배제 무죄 선고", "effects": {"humanity": 5, "law": 20, "public": -5, "trust": 15}},
            {"label": "실체적 진실 우선 유죄 선고", "effects": {"humanity": -10, "law": -20, "public": 5, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 적법절차 위반 증거배제 무죄 확정", "effects": {"humanity": 5, "law": 20, "public": -5, "trust": 15}},
            {"label": "⚖️ [보강판결] 벌금 500만원 선고", "effects": {"humanity": -10, "law": -15, "public": 0, "trust": -10}}
        ]
    },
    {
        "id": "m_13",
        "title": "마약 강제 투여 피해 주장 사건",
        "category": "무죄 판례 / 자의성 미입증 무죄",
        "story": "모임 장소에서 마약 성분이 검출되어 기소되었으나, 타인에 의해 몰래 음료에 타진 것이라고 주장합니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "체내 마약 성분이 양성 반응이므로 투약 유죄입니다.",
        "defense": "본인 의지와 상관없이 몰래 투여당한 퐁당 마약 피해입니다.",
        "ev2": "[CCTV 분석] 제3자가 음료에 의문 물질을 넣는 정황 영상 확인.",
        "real_verdict": "무죄 확정",
        "real_reason": "자의로 마약을 투약했다는 고의성이 입증되지 않음.",
        "choices": [
            {"label": "고의성 미입증 무죄 선고", "effects": {"humanity": 10, "law": 15, "public": 0, "trust": 10}},
            {"label": "양성 반응 기준 유죄 선고", "effects": {"humanity": -10, "law": -15, "public": 5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 고의성 부인 무죄 확정", "effects": {"humanity": 10, "law": 15, "public": 0, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 1년 집행유예 선고", "effects": {"humanity": -10, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_14",
        "title": "강도 피의자 도주 중 정당행위",
        "category": "무죄 판례 / 정당행위 인정",
        "story": "강도를 추격하던 시민이 강도의 도주 차량을 막어서다가 차량 소손이 발생하여 재물손괴로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "타인의 재물을 직접 손상시켰으므로 손괴죄 유죄입니다.",
        "defense": "현행범 체포 및 사회상규에 위배되지 않는 정당행위입니다.",
        "ev2": "[현장 감정] 강도 현행범 체포를 위한 불가피한 최소한의 제압 행위임.",
        "real_verdict": "무죄 확정",
        "real_reason": "형법 제20조 정당행위에 해당하여 위법성이 조각됨.",
        "choices": [
            {"label": "정당행위 인정 무죄 선고", "effects": {"humanity": 10, "law": 15, "public": 15, "trust": 15}},
            {"label": "재물손괴 인정 벌금형 선고", "effects": {"humanity": -10, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 정당행위 위법성 조각 무죄 확정", "effects": {"humanity": 10, "law": 20, "public": 15, "trust": 20}},
            {"label": "⚖️ [보강판결] 벌금 50만원 선고", "effects": {"humanity": -10, "law": -10, "public": -10, "trust": -10}}
        ]
    },
    {
        "id": "m_15",
        "title": "선거법 위반 단순 사실 전달 사건",
        "category": "무죄 판례 / 표현의 자유와 기부행위 구분",
        "story": "선거 출마 후보의 공약집을 주민들에게 단순히 나누어 준 행위가 불법 기부 및 선거운동으로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1540910419892-4a36d2c3266c?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "사전 선거운동 및 불법 유인물 배포로 유죄입니다.",
        "defense": "정당한 정보 전달 및 의정 활동 보고서 배포였습니다.",
        "ev2": "[선관위 답변] 통상적인 의정보고서 배포 범위를 벗어나지 않음.",
        "real_verdict": "무죄 확정",
        "real_reason": "선거 운동 목적이 입증되지 않으며 정보 전달 행위로 인정.",
        "choices": [
            {"label": "무죄 선고", "effects": {"humanity": 5, "law": 15, "public": 5, "trust": 10}},
            {"label": "선거법 위반 유죄 선고", "effects": {"humanity": -5, "law": -10, "public": -5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 정당 정보전달 인정 무죄 확정", "effects": {"humanity": 5, "law": 15, "public": 5, "trust": 10}},
            {"label": "⚖️ [보강판결] 벌금 100만원 선고", "effects": {"humanity": -5, "law": -10, "public": -5, "trust": -10}}
        ]
    },
    {
        "id": "m_16",
        "title": "스토킹 처벌법 제정 전 소급 행위",
        "category": "무죄 판례 / 죄형법정주의 소급효 금지",
        "story": "스토킹 처벌법 시행 이전에 일어난 지속적 연락 행위를 신설 법으로 처벌해달라는 기소건입니다.",
        "img1": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "피해자 고통이 극심하므로 법 시행 전 행위도 처벌해야 합니다.",
        "defense": "죄형법정주의상 법률불소급의 원칙에 따라 무죄입니다.",
        "ev2": "[법리 검토] 행위 당시에는 해당 형벌 조항이 존재하지 않았음.",
        "real_verdict": "무죄 확정",
        "real_reason": "죄형법정주의 및 소급효 금지의 원칙 준수.",
        "choices": [
            {"label": "소급효 금지 적용 무죄 선고", "effects": {"humanity": 0, "law": 20, "public": -5, "trust": 15}},
            {"label": "소급 처벌 유죄 선고", "effects": {"humanity": -10, "law": -25, "public": 5, "trust": -20}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 헌법 원칙에 따른 무죄 선고", "effects": {"humanity": 0, "law": 20, "public": -5, "trust": 20}},
            {"label": "⚖️ [보강판결] 징역 6개월 선고", "effects": {"humanity": -10, "law": -20, "public": 0, "trust": -15}}
        ]
    },
    {
        "id": "m_17",
        "title": "무고죄 피소자의 권리 행사 사건",
        "category": "무죄 판례 / 무고죄 고의성 부인",
        "story": "상대방을 고소했으나 불기소 처분이 나오자, 상대방이 역으로 무고죄로 고소한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "불기소 처분이 나왔으므로 허위 고소임이 명백합니다.",
        "defense": "정당한 주관적 확신에 기반한 고소였으며 허위 인식이 없었습니다.",
        "ev2": "[고소장 검토] 객관적 사실관계를 다소 과장했으나 허위의 사실을 공작한 것은 아님.",
        "real_verdict": "무죄 확정",
        "real_reason": "무고죄는 객관적 허위사실에 대한 고의가 입증되어야 함.",
        "choices": [
            {"label": "무고 고의 부인 무죄 선고", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "무고죄 유죄 선고", "effects": {"humanity": -5, "law": -10, "public": 0, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 허위 인식 부재로 무죄 확정", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 6개월 선고", "effects": {"humanity": -5, "law": -10, "public": 0, "trust": -10}}
        ]
    },
    {
        "id": "m_18",
        "title": "영아 유기 치사 미필적 고의 사건",
        "category": "무죄 판례 / 방임 고의 미입증",
        "story": "출산 직후 중증 질환으로 아기가 숨지자 당황하여 방치한 미혼모가 영아유기치사로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1553531384-cc64ac80f931?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "의료 조치를 취하지 않아 사망에 이르게 한 유기치사입니다.",
        "defense": "출산 당시 영아가 이미 선천적 질환으로 자연사한 상태였습니다.",
        "ev2": "[부검 결과] 출생 직후 선천성 기형 및 호흡곤란으로 인한 자연사 확인.",
        "real_verdict": "유기치사 무죄 (단 단순유기 일부 다툼)",
        "real_reason": "방임 행위와 사망 사이의 직접적 인과관계 부정.",
        "choices": [
            {"label": "치사 혐의 무죄 선고", "effects": {"humanity": 15, "law": 10, "public": -5, "trust": 10}},
            {"label": "유기치사 유죄 선고", "effects": {"humanity": -15, "law": -10, "public": 5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 인과관계 부인 치사 무죄 선고", "effects": {"humanity": 15, "law": 15, "public": -5, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 3년 선고", "effects": {"humanity": -10, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_19",
        "title": "건설 현장 안전관리자 과실 부인",
        "category": "무죄 판례 / 예측 불가능 과실 배척",
        "story": "안전수칙을 완전히 고지했음에도 작업자가 무단으로 안전고리를 풀고 작업하다 추락한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "현장 총괄 책임자로서 주의의무를 다하지 않은 과실이 있습니다.",
        "defense": "안전장비를 지급하고 일대일 교육까지 마친 상태의 돌발 돌출행위였습니다.",
        "ev2": "[CCTV 및 안전일지] 직전까지 안전고리 착용을 지시한 기록 입증.",
        "real_verdict": "무죄 확정",
        "real_reason": "관리자가 예측 및 회피할 수 없는 돌발 사고로 인정.",
        "choices": [
            {"label": "과실 미입증 무죄 선고", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "안전 관리 책임 유죄 선고", "effects": {"humanity": -5, "law": -10, "public": 5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 예측불가 과실 배척 무죄 확정", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "⚖️ [보강판결] 벌금 1,000만원 선고", "effects": {"humanity": -5, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_20",
        "title": "사업 자금 차용 후 부도 사기 사건",
        "category": "무죄 판례 / 변제 의사 사기죄 부인",
        "story": "사업 자금을 빌린 후 갑작스러운 시장 악화로 회사가 부도가 나 채권자가 사기죄로 고소했습니다.",
        "img1": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "돈을 갚지 못했으므로 처음부터 기망 의도가 있었습니다.",
        "defense": "차용 당시에는 정상적 변제 능력과 변제 의사가 있었습니다.",
        "ev2": "[금융 거래 내역] 차용금 대부분이 실제 회사 정상 운영비로 지급됨.",
        "real_verdict": "무죄 확정",
        "real_reason": "차용 당시 기망의 편취 범의가 입증되지 않는 단순 채무불이행.",
        "choices": [
            {"label": "사기 범의 부인 무죄 선고", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "사기죄 유죄 선고", "effects": {"humanity": -5, "law": -15, "public": 0, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 편취 범의 부재로 무죄 확정", "effects": {"humanity": 5, "law": 15, "public": 0, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 1년 6개월 선고", "effects": {"humanity": -5, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_21",
        "title": "위법한 영장 집행 저항 사건",
        "category": "무죄 판례 / 공무집행방해 성립 요건",
        "story": "절차상 위법하게 제시된 압수수색 영 집행에 강력히 저항하다 몸싸움을 벌인 피의자 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "경찰관의 물리적 공무 집행을 방해했으므로 유죄입니다.",
        "defense": "위법한 공무 집행에 대한 정당한 거부 및 저항입니다.",
        "ev2": "[영장 검증] 압수수색 영장의 제시 및 고지 절차가 심각하게 위반됨.",
        "real_verdict": "무죄 확정",
        "real_reason": "적법성이 결여된 공무집행에 대한 저항은 공무집행방해죄 미성립.",
        "choices": [
            {"label": "공무집행 위법 무죄 선고", "effects": {"humanity": 5, "law": 20, "public": -5, "trust": 15}},
            {"label": "공무집행방해 유죄 선고", "effects": {"humanity": -5, "law": -20, "public": 5, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 적법성 결여 공무 저항 무죄 확정", "effects": {"humanity": 5, "law": 20, "public": -5, "trust": 15}},
            {"label": "⚖️ [보강판결] 벌금 300만원 선고", "effects": {"humanity": -5, "law": -15, "public": 0, "trust": -10}}
        ]
    },
    {
        "id": "m_22",
        "title": "개인정보 동의 절차 유효성 사건",
        "category": "무죄 판례 / 개인정보보호법 무지 부인",
        "story": "약관 내 개인정보 제공 동의를 받은 후 제3자에게 제공한 서비스업체가 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "동의 필수 항목 글씨가 작아 명확한 동의로 볼 수 없습니다.",
        "defense": "법이 정한 서식과 자격 기준을 준수하여 동의를 받았습니다.",
        "ev2": "[서식 정밀] 규정된 폰트 크기 및 체크 항목 절차를 완비함.",
        "real_verdict": "무죄 확정",
        "real_reason": "법령상의 형식적·실질적 동의 요건을 갖춘 것으로 인정.",
        "choices": [
            {"label": "적법 동의 인정 무죄 선고", "effects": {"humanity": 0, "law": 15, "public": 0, "trust": 10}},
            {"label": "개인정보법 위반 유죄 선고", "effects": {"humanity": -5, "law": -10, "public": 5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 적법 절차 준수 무죄 확정", "effects": {"humanity": 0, "law": 15, "public": 0, "trust": 10}},
            {"label": "⚖️ [보강판결] 벌금 500만원 선고", "effects": {"humanity": -5, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_23",
        "title": "추천서 내용 일부 수정 문서위조 혐의",
        "category": "무죄 판례 / 사문서위조 성립 부정",
        "story": "지도교수의 구두 동의를 받고 추천서 양식 일부분을 보완하여 제출한 학생이 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "권한 없이 서류 내용을 수정했으므로 문서위조입니다.",
        "defense": "교수의 포괄적 위임 및 구두 승인 하에 작성되었습니다.",
        "ev2": "[교수 증언] 작성을 위임하고 승인한 바 있다는 증언 확보.",
        "real_verdict": "무죄 확정",
        "real_reason": "위임 범위 내의 작성으로 문서위조죄의 위조에 해당하지 않음.",
        "choices": [
            {"label": "위임 인정 무죄 선고", "effects": {"humanity": 10, "law": 10, "public": 0, "trust": 10}},
            {"label": "문서위조 유죄 선고", "effects": {"humanity": -10, "law": -10, "public": 0, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 포괄 위임 인정 무죄 확정", "effects": {"humanity": 10, "law": 15, "public": 0, "trust": 15}},
            {"label": "⚖️ [보강판결] 벌금 100만원 선고", "effects": {"humanity": -10, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_24",
        "title": "보이스피싱 단순 알바 수거책 사건",
        "category": "무죄 판례 / 범죄 인식 미필적 고의 부인",
        "story": "단순 채권추심 아르바이트로 알고 현금을 수거해 전달한 청년이 사기방조로 기소되었습니다.",
        "img1": "https://images.unsplash.com/photo-1553531384-cc64ac80f931?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "수상한 전달 방식으로 볼 때 보이스피싱임을 인지했습니다.",
        "defense": "정식 구직 사이트 공고를 보고 속은 단순 인지 불능 상태였습니다.",
        "ev2": "[메시지 내역] 회사의 거짓 지시 및 계약서 양식에 속아 위법성을 몰랐음이 입증됨.",
        "real_verdict": "무죄 확정",
        "real_reason": "보이스피싱 범행을 인식하거나 예견했다는 미필적 고의 미입증.",
        "choices": [
            {"label": "고의 부재 무죄 선고", "effects": {"humanity": 15, "law": 10, "public": -5, "trust": 10}},
            {"label": "사기방조 유죄 선고", "effects": {"humanity": -15, "law": -10, "public": 5, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 미필적 고의 부정 무죄 확정", "effects": {"humanity": 15, "law": 15, "public": -5, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 1년 집행유예 선고", "effects": {"humanity": -10, "law": -10, "public": 0, "trust": -5}}
        ]
    },
    {
        "id": "m_25",
        "title": "유사 상표권 침해 모호성 사건",
        "category": "무죄 판례 / 상표 유사성 부인",
        "story": "자사 로고 디자인이 유명 브랜드 상표권을 침해했다고 기소된 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "외관과 외형이 유사하여 소비자에게 혼동을 줍니다.",
        "defense": "호칭, 관념, 전체적 구성에서 혼동 가능성이 없습니다.",
        "ev2": "[특허청 감정] 일반 소비자의 직관적 오인·혼동 가능성이 극히 낮음.",
        "real_verdict": "무죄 확정",
        "real_reason": "상표의 외관·호칭·관념을 종합할 때 상품 출처의 혼동 우려가 없음.",
        "choices": [
            {"label": "혼동 가능성 부인 무죄 선고", "effects": {"humanity": 0, "law": 15, "public": 0, "trust": 10}},
            {"label": "상표법 위반 유죄 선고", "effects": {"humanity": 0, "law": -10, "public": 0, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 상표 유사성 부정 무죄 확정", "effects": {"humanity": 0, "law": 15, "public": 0, "trust": 10}},
            {"label": "⚖️ [보강판결] 벌금 300만원 선고", "effects": {"humanity": 0, "law": -10, "public": 0, "trust": -5}}
        ]
    },

    # --- [무기징역 판례 15개] ---
    {
        "id": "l_01",
        "title": "고유정 전 남편 살인 사건",
        "category": "무기징역 판례 / 약물 계획 살인",
        "story": "피고인은 전 남편에게 졸피뎀을 투여한 후 살해하고 사체를 훼손 및 유기했습니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "치밀하게 계획된 살인이므로 무기징역 선고가 필요합니다.",
        "defense": "성폭행 시도에 대응한 우발적 정당방위였습니다.",
        "ev2": "[국과수 감정] 계획적 졸피뎀 구입 및 사전 수색 기록 확보.",
        "real_verdict": "무기징역 확정 (대법원)",
        "real_reason": "사전 약물 준비 및 잔혹한 사체 훼손 등 치밀한 계획 살인 인정.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 10, "trust": 10}},
            {"label": "정당방위 인정 무죄 선고", "effects": {"humanity": 10, "law": -15, "public": -15, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 계획 살인 입증 무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 12, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 15, "trust": 10}}
        ]
    },
    {
        "id": "l_02",
        "title": "강호순 부녀자 연쇄 살인 사건",
        "category": "무기징역/사형 판례 / 연쇄 살인",
        "story": "경기 서남부 일대에서 여성 8명을 납치하여 살해한 연쇄 살인 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "인명 경시의 극치이며 사회적 격리가 필수적이므로 중벌을 선고해야 합니다.",
        "defense": "범행을 인정하고 자백했음을 참작해 주십시오.",
        "ev2": "[DNA 정밀 분석] 피해자 소지품에서 피고인의 DNA 확증 검출.",
        "real_verdict": "사형/무기징역 확정",
        "real_reason": "반인륜적 연쇄 살인으로 영구적 사회 격리가 불가피함.",
        "choices": [
            {"label": "무기징역/사형 선고", "effects": {"humanity": -10, "law": 20, "public": 20, "trust": 20}},
            {"label": "징역 30년 감형", "effects": {"humanity": 10, "law": -15, "public": -20, "trust": -20}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 선고", "effects": {"humanity": -5, "law": 20, "public": 15, "trust": 20}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 20, "trust": 15}}
        ]
    },
    {
        "id": "l_03",
        "title": "신림역 흉기 난동 사건",
        "category": "무기징역 판례 / 묻지마 테러 살인",
        "story": "낮 시간대 보행자 밀집 지역에서 무차별 흉기 난동으로 인명 피해를 낸 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "무고한 시민들을 향한 테러형 범죄로 무기징역이 필요합니다.",
        "defense": "열등감 및 심신미약 상태에서의 우발적 범행입니다.",
        "ev2": "[정신감정] 사이코패스 성향 및 사전 흉기 준비 계획성 입증.",
        "real_verdict": "무기징역 확정",
        "real_reason": "사회적 불안감을 야기한 무차별 흉기 살인으로 영구 격리 선고.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "심신미약 감형(징역 20년)", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 20, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 20, "trust": 10}}
        ]
    },
    {
        "id": "l_04",
        "title": "가평 계곡 살인 사건 (이은해)",
        "category": "무기징역 판례 / 미필적 고의 부작위 살인",
        "story": "수영을 못하는 남편을 다이빙하게 유도한 후 구조하지 않아 숨지게 한 보험금 목적 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "보험금을 노린 미필적 고의에 의한 직접/부작위 살인입니다.",
        "defense": "피해자 스스로 다이빙한 사고사였습니다.",
        "ev2": "[음성 복원] 현장 구조 요청을 무시하고 방관한 정황 복원.",
        "real_verdict": "무기징역 확정",
        "real_reason": "구조 의무를 저버린 부작위에 의한 살인 고의 인정.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "과실치사 인정 감형 선고", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 부작위 살인 인정 무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 20년 선고", "effects": {"humanity": 0, "law": -10, "public": -10, "trust": -10}}
        ]
    },
    {
        "id": "l_05",
        "title": "노원구 세 모녀 살인 사건",
        "category": "무기징역 판례 / 스토킹 일가족 살인",
        "story": "스토킹하던 피해자의 집에 퀵서비스 기사로 위장 침입하여 일가족 세 모녀를 살해했습니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "치밀한 계획하에 일가족을 참살했으므로 극형에 처해야 합니다.",
        "defense": "우발적 감정 조절 실패 및 자백 참작을 요청합니다.",
        "ev2": "[포렌식] 침입 수법, 도구 준비, 피해자 동선 사전 조사 입증.",
        "real_verdict": "무기징역 확정",
        "real_reason": "잔혹한 계획 살인으로 사회로부터 영구히 격리함.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 35년 감형 선고", "effects": {"humanity": 5, "law": -10, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 15, "trust": 10}}
        ]
    },
    {
        "id": "l_06",
        "title": "부산 돌려차기 강간살인미수 사건",
        "category": "무기징역/중형 판례 / 무차별 폭행 강간미수",
        "story": "귀가하던 여성을 뒤따라가 무차별 머리 돌려차기로 의식을 잃게 한 후 은밀한 곳으로 이동시킨 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "강간목적 살인미수로 중형이 선고되어야 합니다.",
        "defense": "강간 목적이 없었으며 우발적 폭행 상해였습니다.",
        "ev2": "[DNA 재감정] 피해자 청바지 안쪽에서 피고인의 DNA 확증 검출.",
        "real_verdict": "징역 20년 확정 (항소심 중형)",
        "real_reason": "강간 살인 미수 인정으로 중형 선고.",
        "choices": [
            {"label": "징역 20년 이상/무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "단순 상해 인정 징역 12년 선고", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 강간살인미수 인정 중형 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 무기징역 선고", "effects": {"humanity": -10, "law": 20, "public": 15, "trust": 15}}
        ]
    },
    {
        "id": "l_07",
        "title": "어금니 아빠 이영학 사건",
        "category": "무기징역 판례 / 아동 유괴 살인",
        "story": "딸의 친구인 여중생을 유괴하여 추행하고 살해한 후 사체를 유기한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "아동 대상 추행 및 계획 살인으로 무기징역이 마땅합니다.",
        "defense": "심신미약 및 반성문을 제출했음을 참작해 주십시오.",
        "ev2": "[약물 감정] 피해자 체내에서 수면제 성분 대량 검출.",
        "real_verdict": "무기징역 확정",
        "real_reason": "추악한 아동 대상 범죄로 무기징역 선고.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 20년 감형", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 15, "trust": 10}}
        ]
    },
    {
        "id": "l_08",
        "title": "울산 아동학대 치사 사건",
        "category": "무기징역/중형 판례 / 아동학대 살인",
        "story": "계모가 8세 여아를 지속적으로 무자비하게 폭행하여 갈비뼈 부러짐 등으로 숨지게 한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1553531384-cc64ac80f931?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "치사 행위를 넘어선 미필적 고의에 의한 살인입니다.",
        "defense": "훈육 목적의 폭행이었으며 살해 고의는 없었습니다.",
        "ev2": "[부검 결과] 지속적 폭행에 의한 장기 파열 및 다발성 골절 검출.",
        "real_verdict": "징역 18년~무기징역 다툼 끝 중형",
        "real_reason": "아동학대 살인의 고의성 인정.",
        "choices": [
            {"label": "살인죄 적용 무기징역/중형 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "학대치사 인정 징역 10년 선고", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 살인죄 인정 징역 18년 선고", "effects": {"humanity": -5, "law": 15, "public": 10, "trust": 10}},
            {"label": "⚖️ [보강판결] 무기징역 선고", "effects": {"humanity": -10, "law": 20, "public": 15, "trust": 15}}
        ]
    },
    {
        "id": "l_09",
        "title": "창원 골프연습장 납치 살인 사건",
        "category": "무기징역 판례 / 강도 살인",
        "story": "골프연습장 주차장에서 여성을 납치한 후 금품을 빼앗고 살해 및 유기한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "금품을 노린 치밀한 납치 살인으로 무기징역 선고가 필요합니다.",
        "defense": "우발적 목 누름이었음을 감안해 주십시오.",
        "ev2": "[CCTV] 사전 차량 번호판 위조 및 유기 장소물 사전 탐색 입증.",
        "real_verdict": "무기징역 확정",
        "real_reason": "강도살인죄의 계획성 및 잔혹성 인정.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 25년 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 30년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },
    {
        "id": "l_10",
        "title": "안양 초등학생 유괴 살인 사건",
        "category": "무기징역/사형 판례 / 아동 유괴 잔혹 살인",
        "story": "초등학생 2명을 유괴하여 잔혹하게 살해하고 시신을 훼손해 암매장한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "어린 어린이들을 향한 극악무도한 범죄이므로 극형이 마땅합니다.",
        "defense": "시신 훼손에 대해 반성하고 있습니다.",
        "ev2": "[현장 감정] 피고인 자택에서 피해 어린이들의 유류품 및 DNA 다수 발견.",
        "real_verdict": "사형/무기징역 확정",
        "real_reason": "반인륜적 범죄로 사회적 격리 선고.",
        "choices": [
            {"label": "무기징역/사형 선고", "effects": {"humanity": -10, "law": 20, "public": 20, "trust": 20}},
            {"label": "징역 30년 감형", "effects": {"humanity": 10, "law": -20, "public": -20, "trust": -20}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 20, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 20, "trust": 15}}
        ]
    },
    {
        "id": "l_11",
        "title": "서현역 AK플라자 차/흉기 난동 사건",
        "category": "무기징역 판례 / 테러형 무차별 살인",
        "story": "차량으로 인도 위 보행자를 친 후 백화점으로 들어가 무차별 흉기 난동을 부린 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "불특정 다수를 향한 테러 범죄로 무기징역이 필수적입니다.",
        "defense": "조현병 및 피해망상으로 인한 심신미약 상태였습니다.",
        "ev2": "[정신 감정] 심신미약 상태는 인정되나 범행의 위험성 및 재범 가능성이 매우 높음.",
        "real_verdict": "무기징역 확정",
        "real_reason": "사회 안전을 저해한 대형 무차별 살인으로 영구 격리.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "조현병 감형(징역 20년)", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 20, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 20, "trust": 10}}
        ]
    },
    {
        "id": "l_12",
        "title": "시흥 토막 사체 훼손 살인 사건",
        "category": "무기징역 판례 / 금전관계 계획 살인",
        "story": "동거녀를 목 눌러 살해한 후 사체를 잔혹하게 훼손하여 하천에 유기한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "살해 수법과 사체 훼손이 비인간적이므로 무기징역에 처해야 합니다.",
        "defense": "다투는 과정에서의 우발적 범행이었습니다.",
        "ev2": "[현장 정밀] 사전 사체 훼손 도구 준비 및 하천 유기 계획성 입증.",
        "real_verdict": "무기징역 확정",
        "real_reason": "잔혹한 사체 훼손 및 인명 경시 범죄 인정.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 20년 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 30년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },
    {
        "id": "l_13",
        "title": "존속 살해 및 사체 유기 사건",
        "category": "무기징역 판례 / 반인륜 존속 살인",
        "story": "재산 상속을 노리고 친부모에게 약물을 투여하여 살해한 반인륜 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "천륜을 어긴 반인륜적 범죄이므로 무기징역이 마땅합니다.",
        "defense": "부모의 그간 폭언에 대한 충동적 반응이었습니다.",
        "ev2": "[약물 감정] 사전 희석 약물 제조법 및 상속 포기 각서 조작 입증.",
        "real_verdict": "무기징역 확정",
        "real_reason": "존속살해죄 가중처벌 및 반인륜성 적용.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 20년 선고", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 20, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 20, "trust": 10}}
        ]
    },
    {
        "id": "l_14",
        "title": "보복 살인 및 스토킹 살해 사건",
        "category": "무기징역 판례 / 특가법 보복 살인",
        "story": "경찰 신고에 앙심을 품고 스마트워치를 차고 있던 피해자를 찾아가 살해한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "사법 시스템을 무시한 보복 살인으로 무기징역에 처해야 합니다.",
        "defense": "우발적 우울증 상태에서의 행동이었습니다.",
        "ev2": "[위치 추적] 피해자 주거지 사전 4차례 흉기 소지 방문 기록 입증.",
        "real_verdict": "무기징역 확정",
        "real_reason": "특가법상 보복살인죄 적용 및 무기징역 확정.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 25년 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 사형 선고", "effects": {"humanity": -15, "law": 20, "public": 15, "trust": 10}}
        ]
    },
    {
        "id": "l_15",
        "title": "인천 영종도 강도살인 및 사체유기",
        "category": "무기징역 판례 / 강도 살인",
        "story": "택시 기사를 유인하여 살해하고 금품을 빼앗은 뒤 영종도 해안가에 유기했습니다.",
        "img1": "https://images.unsplash.com/photo-1508962914676-134849a727f0?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "서민 대상 계획 강도 살인으로 무기징역이 타당합니다.",
        "defense": "요금 다툼 과정의 우발적 범행이었습니다.",
        "ev2": "[CCTV] 대포폰을 사용한 유인 및 사전 흉기 소지 입증.",
        "real_verdict": "무기징역 확정",
        "real_reason": "치밀한 계획 강도 살인죄 인정.",
        "choices": [
            {"label": "무기징역 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 20년 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 무기징역 확정", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 30년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },

    # --- [유기징역 판례 10개] ---
    {
        "id": "t_01",
        "title": "음주운전 2회 적발 인명 피해 사건",
        "category": "유기징역 판례 / 윤창호법 특가법",
        "story": "음주운전 재범 상태에서 인도로 돌진하여 보행자에게 중상을 입히고 도주하려 한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "윤창호법을 적용하여 징역 8년 중형에 처해야 합니다.",
        "defense": "자백하고 피해자와 합의를 진행 중입니다.",
        "ev2": "[블랙박스] 음주 수치 0.18% 및 도주 시도 정황 확보.",
        "real_verdict": "징역 6년 선고 확정",
        "real_reason": "특가법상 위험운전치상 및 재범 가중처벌 적용.",
        "choices": [
            {"label": "징역 8년 선고", "effects": {"humanity": -5, "law": 10, "public": 10, "trust": 10}},
            {"label": "합의 참작 징역 3년 선고", "effects": {"humanity": 10, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 6년 선고", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 4년 집행유예 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ]
    },
    {
        "id": "t_02",
        "title": "대형 전세사기 다수 피해자 사건",
        "category": "유기징역 판례 / 사기죄 법정 최고형 부근",
        "story": "수백 채의 빌라를 이용해 무자본 갭투자로 청년들의 전세보증금 수백억을 편취했습니다.",
        "img1": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "서민 삶을 흔든 범죄로 사기죄 법정 최고형인 징역 15년을 구형합니다.",
        "defense": "부동산 경기 하락에 따른 불가피한 부도였습니다.",
        "ev2": "[계약서 정밀] 리베이트 수수 및 보증금 반환 불가능 구조 사전 인지 입증.",
        "real_verdict": "징역 15년 확정",
        "real_reason": "다수 피해자를 낳은 조직적 사기죄 최고형 적용.",
        "choices": [
            {"label": "징역 15년(최고형) 선고", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "징역 7년 선고", "effects": {"humanity": 5, "law": -10, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 15년 확정", "effects": {"humanity": -5, "law": 15, "public": 15, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 10년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },
    {
        "id": "t_03",
        "title": "층간소음 흉기 상해치사 사건",
        "category": "유기징역 판례 / 상해치사 우발적 범행",
        "story": "지속된 층간소음 갈등 중 홧김에 흉기로 이웃을 공격하여 숨지게 한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "살인의 미필적 고의가 인정되므로 징역 15년이 필요합니다.",
        "defense": "살해 고의가 없었던 상해치사이며 유족과 합의했습니다.",
        "ev2": "[녹음 파일] 충동적 다툼 상황 및 치명상 부위 비조준 입증.",
        "real_verdict": "징역 12년 확정",
        "real_reason": "살인 고의 부정, 상해치사죄 인정 및 감형 참작.",
        "choices": [
            {"label": "상해치사 징역 12년 선고", "effects": {"humanity": 5, "law": 10, "public": 5, "trust": 10}},
            {"label": "살인죄 적용 징역 20년 선고", "effects": {"humanity": -10, "law": -5, "public": 5, "trust": -5}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 12년 확정", "effects": {"humanity": 5, "law": 10, "public": 5, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 15년 선고", "effects": {"humanity": -5, "law": 5, "public": 5, "trust": 0}}
        ]
    },
    {
        "id": "t_04",
        "title": "고위 공직자 뇌물 수수 사건",
        "category": "유기징역 판례 / 뇌물죄 징역형",
        "story": "인허가 대가로 건설업체로부터 수억 원 상당의 금품 및 특혜를 받은 혐의입니다.",
        "img1": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "공직 청렴성을 훼손했으므로 징역 7년 및 벌금/추징금을 구형합니다.",
        "defense": "차용금이었을 뿐 대가성이 없었습니다.",
        "ev2": "[계좌 추적] 대가성 차명 계좌 송금 내역 확증.",
        "real_verdict": "징역 7년 및 벌금 5억원 확정",
        "real_reason": "특가법상 뇌물수수죄 대가성 인정.",
        "choices": [
            {"label": "징역 7년 및 벌금 선고", "effects": {"humanity": 0, "law": 15, "public": 10, "trust": 15}},
            {"label": "징역 3년 집행유예 선고", "effects": {"humanity": 0, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 7년 확정", "effects": {"humanity": 0, "law": 15, "public": 10, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 5년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },
    {
        "id": "t_05",
        "title": "데이트 폭력 치사 사건",
        "category": "유기징역 판례 / 폭행치사 징역형",
        "story": "연인을 폭행하여 상해를 입힌 후 사망에 이르게 한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&q=80",
        "prosecution": "중한 폭행에 따른 사망으로 징역 12년이 선고되어야 합니다.",
        "defense": "치료 조치를 하려 했으며 우발적 폭행이었습니다.",
        "ev2": "[부검 결과] 폭행에 따른 장기 손상이 직접 사망 원인임.",
        "real_verdict": "징역 10년 확정",
        "real_reason": "폭행과 사망 사이 인과관계 인정으로 상해치사죄 중형.",
        "choices": [
            {"label": "징역 10년 선고", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "징역 5년 감형 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 10년 확정", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 12년 선고", "effects": {"humanity": -5, "law": 5, "public": 5, "trust": 5}}
        ]
    },
    {
        "id": "t_06",
        "title": "음주 뺑소니(특가법 도주치사) 사건",
        "category": "유기징역 판례 / 도주치사 징역형",
        "story": "음주 상태에서 보행자를 치어 숨지게 한 후 사고 현장을 이탈해 도주했습니다.",
        "img1": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "도주 및 증거인멸 시도로 징역 8년을 구형합니다.",
        "defense": "당황하여 도주했으나 이튿날 자수했습니다.",
        "ev2": "[CCTV 영상] 사고 후 블랙박스 칩을 은닉하려 한 정황 포착.",
        "real_verdict": "징역 6년 선고 확정",
        "real_reason": "특가법상 도주치사죄 중형 선고.",
        "choices": [
            {"label": "징역 6년 선고", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "자수 참작 징역 2년 6개월 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 6년 확정", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 8년 선고", "effects": {"humanity": -5, "law": 5, "public": 5, "trust": 5}}
        ]
    },
    {
        "id": "t_07",
        "title": "응급실 의료진 난동 폭행 사건",
        "category": "유기징역 판례 / 응급의료법 위반",
        "story": "술에 취해 응급실에서 의료진을 난동 폭행하여 전치 6주의 상해를 입혔습니다.",
        "img1": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "응급의료 체계를 방해한 중범죄로 징역 3년 6개월이 필요합니다.",
        "defense": "음주로 인한 심신미약 상태였습니다.",
        "ev2": "[응급실 CCTV] 의료 장비를 파손하고 진료를 지속 방해함.",
        "real_verdict": "징역 3년 확정",
        "real_reason": "응급의료법 위반 및 공공 안전 저해 중형 선고.",
        "choices": [
            {"label": "징역 3년 실형 선고", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "음주 참작 집행유예 선고", "effects": {"humanity": 5, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 3년 확정", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 1년 6개월 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },
    {
        "id": "t_08",
        "title": "체육계 지위 이용 강제추행 사건",
        "category": "유기징역 판례 / 성폭력 가중처벌",
        "story": "감독이라는 지위를 이용해 오랜 기간 선수들을 상습 추행한 사건입니다.",
        "img1": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "위력에 의한 상습 범행으로 징역 5년을 구형합니다.",
        "defense": "친밀감의 표시였으며 위력 행사가 아니었습니다.",
        "ev2": "[피해자 진술] 일관된 피해 진술 및 선수 기평가 불이익 위협 입증.",
        "real_verdict": "징역 4년 확정",
        "real_reason": "위력에 의한 강제추행 인정.",
        "choices": [
            {"label": "징역 4년 실형 선고", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "집행유예 선고", "effects": {"humanity": 5, "law": -15, "public": -15, "trust": -15}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 4년 확정", "effects": {"humanity": 0, "law": 10, "public": 10, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 2년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },
    {
        "id": "t_09",
        "title": "불법 도박 사이트 개설 총책 사건",
        "category": "유기징역 판례 / 도박개장 및 추징",
        "story": "해외 서버를 두고 불법 도박 사이트를 운영하여 수백억 원의 불법 이득을 취득했습니다.",
        "img1": "https://images.unsplash.com/photo-1611162617213-7d7a39e9b1d7?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "조직적 사기 및 도박개장으로 징역 6년 및 추징금을 구형합니다.",
        "defense": "단순 시스템 개발자일 뿐 총책이 아니었습니다.",
        "ev2": "[수사 기록] 수익금 배분 계좌 총괄 관리자임이 입증됨.",
        "real_verdict": "징역 5년 및 추징금 확정",
        "real_reason": "불법 도박개장 총책 혐의 인정.",
        "choices": [
            {"label": "징역 5년 및 추징금 선고", "effects": {"humanity": 0, "law": 15, "public": 10, "trust": 10}},
            {"label": "징역 2년 감형 선고", "effects": {"humanity": 0, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 5년 확정", "effects": {"humanity": 0, "law": 15, "public": 10, "trust": 10}},
            {"label": "⚖️ [보강판결] 징역 3년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    },
    {
        "id": "t_10",
        "title": "보이스피싱 중간 간부 범죄단체 가입",
        "category": "유기징역 판례 / 범죄단체조직죄",
        "story": "보이스피싱 콜센터 팀장으로서 상담원들을 관리하고 송금을 총괄했습니다.",
        "img1": "https://images.unsplash.com/photo-1553531384-cc64ac80f931?w=800&q=80",
        "img2": "https://images.unsplash.com/photo-1450133064473-71024230f91b?w=800&q=80",
        "prosecution": "범죄단체 조직 및 핵심 가담으로 징역 10년이 필요합니다.",
        "defense": "상부의 지시만 따랐던 수동적 역할이었습니다.",
        "ev2": "[통화 내역] 상담원 수수료 배분 및 행동 수칙 교육 정황 입증.",
        "real_verdict": "징역 9년 확정",
        "real_reason": "범죄단체 가입 및 조직적 사기죄 적용.",
        "choices": [
            {"label": "징역 9년 선고", "effects": {"humanity": 0, "law": 15, "public": 10, "trust": 15}},
            {"label": "징역 4년 감형 선고", "effects": {"humanity": 0, "law": -10, "public": -10, "trust": -10}}
        ],
        "post_choices": [
            {"label": "⚖️ [보강판결] 징역 9년 확정", "effects": {"humanity": 0, "law": 15, "public": 10, "trust": 15}},
            {"label": "⚖️ [보강판결] 징역 6년 선고", "effects": {"humanity": 0, "law": -5, "public": -5, "trust": -5}}
        ]
    }
]

def clamp(v):
    return max(0, min(100, v))

# 세션 초기화
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.judge_name = "전자고사법관"
    st.session_state.humanity = 50
    st.session_state.law = 50
    st.session_state.public = 50
    st.session_state.trust = 60
    st.session_state.case_index = 0
    st.session_state.postpone_credits = 1  # 💡 한 게임(3 사건) 당 딱 1번만 가능
    st.session_state.is_postponed = False
    st.session_state.history = []

    # 전체 50개 사건 중 3개를 무작위 추출
    st.session_state.cases = random.sample(ALL_CASES, min(3, len(ALL_CASES)))

st.title("⚖️ AI 판사: 균형의 법정 v12.2")

# 사이드바
with st.sidebar:
    st.header(f"🏛️ {st.session_state.judge_name}")
    st.divider()
    st.subheader("📊 현재 사법 지표")
    st.progress(st.session_state.humanity / 100, text=f"❤️ 인간 중심: {st.session_state.humanity}")
    st.progress(st.session_state.law / 100, text=f"📜 법적 엄격함: {st.session_state.law}")
    st.progress(st.session_state.public / 100, text=f"🏛️ 공공 이익: {st.session_state.public}")
    st.progress(st.session_state.trust / 100, text=f"🛡️ 사회적 신뢰: {st.session_state.trust}")
    st.divider()
    st.info(f"🔍 2차 정밀 증거 요청 찬스: **{st.session_state.postpone_credits} / 1회 남음**")
    st.divider()
    if st.button("🔄 새 게임 시작"):
        st.session_state.clear()
        st.rerun()

# 게임 진행 화면
if st.session_state.case_index < len(st.session_state.cases):
    case = st.session_state.cases[st.session_state.case_index]
    
    st.caption(f"📍 재판 진행도: {st.session_state.case_index + 1} / 3")
    st.subheader(f"⚖️ 사건 {st.session_state.case_index + 1}: {case['title']}")
    st.caption(f"분야: {case['category']}")

    col_img, col_info = st.columns([1, 1.2])
    with col_img:
        if not st.session_state.is_postponed:
            st.image(case["img1"], caption="📸 1차 제출 현장 증거 사진", use_container_width=True)
        else:
            st.image(case["img2"], caption="🔍 2차 정밀 포렌식/부검 증거 사진", use_container_width=True)

    with col_info:
        st.info(f"**사건 개요:**\n\n{case['story']}")
        t1, t2 = st.tabs(["⚖️ 검찰 구형", "🛡️ 변호인 변론"])
        with t1:
            st.write(case["prosecution"])
        with t2:
            st.write(case["defense"])

    if st.session_state.is_postponed:
        st.success(f"🔍 **2차 추가 증거 개시:**\n\n{case['ev2']}")

    st.divider()
    st.subheader("⚖️ 판결 선택")

    if not st.session_state.is_postponed:
        if st.session_state.postpone_credits > 0:
            if st.button("🔍 판결 유예 및 2차 정밀 증거 요청 (게임 당 1회 제한)", key=f"postpone_{st.session_state.case_index}"):
                st.session_state.postpone_credits -= 1
                st.session_state.is_postponed = True
                st.rerun()
        else:
            st.caption("⚠️ *이번 게임의 2차 정밀 증거 요청 찬스를 이미 사용하셨습니다.*")

        st.write("")
        for idx, choice in enumerate(case["choices"]):
            with st.container(border=True):
                st.markdown(f"**{choice['label']}**")
                if st.button("⚖️ 이 판결 선고", key=f"btn_{st.session_state.case_index}_{idx}"):
                    for k, v in choice["effects"].items():
                        st.session_state[k] = clamp(st.session_state[k] + v)
                    
                    st.session_state.history.append({
                        "case": case["title"],
                        "my_decision": choice["label"],
                        "real_verdict": case["real_verdict"],
                        "real_reason": case["real_reason"]
                    })
                    st.session_state.case_index += 1
                    st.session_state.is_postponed = False
                    st.rerun()

    else:
        for idx, choice in enumerate(case["post_choices"]):
            with st.container(border=True):
                st.markdown(f"**{choice['label']}**")
                if st.button("⚖️ 이 보강 판결 선고", key=f"btn_post_{st.session_state.case_index}_{idx}"):
                    for k, v in choice["effects"].items():
                        st.session_state[k] = clamp(st.session_state[k] + v)
                    
                    st.session_state.history.append({
                        "case": f"{case['title']} (2차 증거 제출)",
                        "my_decision": choice["label"],
                        "real_verdict": case["real_verdict"],
                        "real_reason": case["real_reason"]
                    })
                    st.session_state.case_index += 1
                    st.session_state.is_postponed = False
                    st.rerun()

# 재판 종결 리포트 화면
else:
    st.balloons()
    st.title("🏛️ 재판 종결: 판사 성향 및 판례 비교 리포트")
    
    persona = analyze_judge_persona(
        st.session_state.humanity,
        st.session_state.law,
        st.session_state.public,
        st.session_state.trust
    )
    
    st.container(border=True).markdown(f"""
    ## 🧐 {st.session_state.judge_name}님의 사법 성향 진단
    ### **{persona['title']}**
    
    {persona['desc']}
    """)

    st.divider()
    st.subheader("📜 내 판결 VS 실제 대법원 판례 비교")
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"사건 {idx+1}: {item['case']}", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.warning(f"**내 판결:** {item['my_decision']}")
            with col_b:
                st.success(f"**실제 대법원:** {item['real_verdict']}")
            st.caption(f"**판단 이유:** {item['real_reason']}")

    if st.button("🔄 새 게임 시작", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()
