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
            {"label": "⚖️ [보강판결] 징역 1년 집행유예 선고", "effects": {"humanity": -10, "law": -
