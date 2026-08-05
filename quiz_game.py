"""
QuizGame 클래스 - 게임 로직 및 저장소 관리
"""

import json
import os
import random
from quiz import Quiz


class QuizGame:
    """
    퀴즈 게임을 관리하는 클래스
    
    속성:
        data_file (str): 데이터 저장 파일 경로
        quizzes (list): Quiz 객체 리스트
        best_score (int): 최고 점수
    """
    
    def __init__(self, data_file="state.json"):
        """
        QuizGame 인스턴스 초기화
        
        Args:
            data_file (str): 데이터 저장 파일 경로 (기본값: state.json)
        """
        self.data_file = data_file
        self.quizzes = []
        self.best_score = 0
        self.load_data()
    
    def load_data(self):
        """
        파일에서 데이터 로드
        파일이 없거나 손상되면 기본 데이터로 초기화
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Quiz 객체 복원
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score", data.get("scores", {}).get("전체", 0))
            else:
                self._init_default_data()
        except (json.JSONDecodeError, KeyError):
            print("⚠️  데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
            self._init_default_data()
    
    def _init_default_data(self):
        """기본 데이터로 초기화"""
        self.quizzes = [
            Quiz(
                "파이썬은 몇 년에 만들어졌을까?",
                ["1989년", "1991년", "1995년", "1999년"],
                1  # 정답: 1991년
            ),
            Quiz(
                "다음 중 파이썬의 창시자는?",
                ["Guido van Rossum", "Bjarne Stroustrup", "Dennis Ritchie", "Niklaus Wirth"],
                0  # 정답: Guido van Rossum
            )
        ]
        self.best_score = 0
    
    def save_data(self):
        """
        데이터를 파일에 저장 (UTF-8 인코딩)
        """
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # print("✅ 데이터가 저장되었습니다.")
        except Exception as e:
            print(f"❌ 저장 중 오류 발생: {e}")
    
    def add_quiz(self, question, choices, answer):
        """
        새로운 퀴즈 추가
        
        Args:
            question (str): 퀴즈 질문
            choices (list): 선택지 리스트
            answer (int): 정답의 인덱스
        
        Returns:
            bool: 성공 여부
        """
        if len(choices) != 4:
            print("❌ 선택지는 정확히 4개여야 합니다.")
            return False
        
        if not (0 <= answer <= 3):
            print("❌ 정답 인덱스는 0~3 사이여야 합니다.")
            return False
        
        quiz = Quiz(question, choices, answer)
        self.quizzes.append(quiz)
        print(f"✅ 퀴즈가 추가되었습니다!")
        return True
    
    def delete_quiz(self, index):
        """
        지정한 인덱스의 퀴즈 삭제
        
        Args:
            index (int): 삭제할 퀴즈의 인덱스
        
        Returns:
            bool: 삭제 성공 여부
        """
        if not (0 <= index < len(self.quizzes)):
            print("❌ 올바른 퀴즈 번호가 아닙니다.")
            return False
        
        removed = self.quizzes.pop(index)
        print(f"✅ '{removed.question}' 퀴즈가 삭제되었습니다.")
        return True
    
    def get_random_quiz(self):
        """
        랜덤 퀴즈 반환
        
        Returns:
            Quiz: 랜덤으로 선택된 Quiz 객체 또는 None
        """
        if not self.quizzes:
            print("❌ 저장된 퀴즈가 없습니다.")
            return None
        return random.choice(self.quizzes)
    
    def update_score(self, new_score):
        """
        최고 점수 업데이트
        
        Args:
            new_score (int): 새로운 점수
        """
        if self.best_score < new_score:
            self.best_score = new_score
    
    def get_all_quizzes(self):
        """모든 퀴즈 반환"""
        return self.quizzes
    
    def get_best_score(self):
        """현재 최고 점수 반환"""
        return self.best_score
    
    def quiz_count(self):
        """저장된 퀴즈 개수 반환"""
        return len(self.quizzes)
