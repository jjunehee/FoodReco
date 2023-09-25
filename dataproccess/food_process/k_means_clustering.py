import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# 파일 경로를 변경해야 할 수도 있습니다.
filename = './preprocessed_data/reordered_data.xlsx'  # 여러분의 파일 경로로 변경해 주세요

# 데이터 로드
data = pd.read_excel(filename)

# 선택된 열을 사용하여 조합된 문자열을 만듭니다.
selected_columns = ['음식명', '조리방식'] + list(data.columns[data.columns.get_loc("카레"):]) + ['음식분류2', '음식분류1']
data_selected = data[selected_columns].fillna('')
data_selected['combined'] = data_selected.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)


replacement_dict = {

    '커리': '카레',
    '카레': '카레',
    '된장': '된장',
    '간장': '간장',
    '고추장': '고추장',
    '케챱': '케찹',
    '케첩': '케찹',
    '케찹': '케찹',
    '케쳡': '케찹',
    '오리': '육류',
    '한우': '육류',
    '아롱사태': '육류',
    '어묵': '어묵',
    '오뎅': '어묵',
    '오이': '오이',
    '당근': '채소',
    '양파': '채소',
    '피망': '채소',
    '버섯': '버섯',
    '고추': '고추',
    '닭': '육류',
    '소고기': '육류',
    '돼지고기': '육류',
    '생선': '생선',
    '조개': '조개',
    '고등어': '생선',
    '북어': '생선',
    '오징어': '오징어류',
    '콩': '대두',
    '두부': '대두',
    '브로콜리': '채소',
    '배추': '채소',
    '상추': '채소',
    '파': '채소',
    '강황': '카레',
    '진간장': '간장',
    '생강': '채소',
    '전복': '조개류',
    '굴': '조개류',
    '바지락': '조개류',
    '대구': '생선',
    '명태': '생선',
    '갈치': '생선',
    '광어': '생선',
    '우럭': '생선',
    '참치': '생선',
    '도미': '생선',
    '돔': '생선',
    '연어': '생선',
    '장어': '생선',
    '민어': '생선',
    '삼치': '생선',
    '조기': '생선',
    '방어': '생선',
    '숭어': '생선',
    '날치': '생선',
    '아귀': '생선',
    '코다리': '생선',
    '굴비': '생선',
    '병어': '생선',
    '전어': '생선',
    '소라': '조개류',
    '낙지': '오징어류',
    '동태': '생선',
    '추어': '생선',
    '홍어': '생선',
    '아구': '생선',
    '문어': '오징어류',
    '쭈꾸미': '오징어류',
    '도다리': '생선',
    '농어': '생선',
    '서대': '생선',
    '송어': '생선',
    '볼락': '생선',
    '청어': '생선',
    '노가리': '생선',
    '돼지': '육류',
    '소갈비': '육류',
    '쇠고기': '육류',
    '제육': '육류',
    '양갈비': '육류',
    '소불고기': '육류',
    '가오리': '생선',
    '메기': '생선',
    '임연수': '생선',
    '과메기': '생선',
    '안심': '육류',
    '목살': '육류',
    '삼겹살': '육류',
    '항정살': '육류',
    '오리고기': '육류',
    '양지머리': '육류',
    '가지': '채소',
    '고구마': '채소',
    '감자': '채소',
    '콜리플라워': '채소',
    '파프리카': '채소',
    '황태': '생선',
    '홍합': '조개류',
    '치킨': '육류',
    '가자미': '생선'

}

allergy_ingredient_category_dict = {
    '카슈넛':'견과류',
    '유부':'대두',
    '두부':'대두',
    '콩':'대두',
    '수제비':'밀가루',
    '땅콩버터': '견과류',
    '라면': '밀가루',
    '토마토': '토마토',
    '복숭아': '복숭아',
    '새우': '갑각류',
    '꽃게': '갑각류',
    '랍스타': '갑각류',
    '랍스터': '갑각류',
    '게살': '갑각류',
    '킹크랩': '갑각류',
    '아몬드': '견과류',
    '피칸': '견과류',
    '헤이즐넛': '견과류',
    '캐슈넛': '견과류',
    '피스타치오': '견과류',
    '잣':'견과류',
    '호두': '견과류',
    '전복': '조개류',
    '굴': '조개류',
    '바지락': '조개류',
    '홍합':'조개류',
    '소라':'조개류',
    '두유': '대두',
    '메밀': '메밀',
    '밀가루': '밀가루',
    '대두': '대두',
    '우유': '우유',
    '치즈': '우유',
    '생크림': '우유',
    '요거트': '우유',
    '모짜렐라': '우유',
    '까르보': '우유',
    '크림':'우유',
    '로제':'우유',
    '마요네즈':'알류',
    '땅콩': '견과류',
    '새알류': '알류',
    '케찹': '토마토',
    '케챱': '토마토',
    '케첩': '토마토',
    '케쳡': '토마토',
    '굴소스': '조개류',
    '우렁': '갑각류'
}
category_dict = {
    '닭고기': '육류',
    '돼지고기': '육류',
    '밀가루': '밀가루',
    '육류': '육류',
    '소고기': '육류'
}

ingredient_list = list(replacement_dict.values()) + list(allergy_ingredient_category_dict.values()) + list(category_dict.values())


ingredient_weight_dict = {ingredient: 5 for ingredient in ingredient_list}

# 리스트에 가중치를 어떻게 부여
weights = {
    '음식명': 2,  # 음식명에 높은 가중치 부여
    '조리방식': 1,  # 조리방식에 높은 가중치 부여
    # 다른 열에 대한 가중치도 설정할 수 있습니다.
    '음식분류2': 3,
    '음식분류1':4
}

combined_dict = {**ingredient_weight_dict, **weights}

# 가중치 적용
for column, weight in combined_dict.items():
    data_selected[column] = data_selected[column].apply(lambda x: (str(x) + ' ') * weight)


# TF-IDF 벡터화
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data_selected['combined'])



# K-means 군집화
k = 599  # 군집의 수
model = KMeans(n_clusters=k, init='k-means++', random_state=42)
model.fit(X)

# 군집 레이블을 원본 데이터에 추가
data['cluster_labels'] = model.labels_

# 결과를 새로운 엑셀 파일로 저장
output_filename = './preprocessed_data/menu_ingredient/weighted_clustered_new_ingredient_599_clusters.xlsx'  # 원하는 파일명으로 변경 가능
data.to_excel(output_filename, index=False)

