"""
QuizGame 클래스 - 게임 로직 및 저장소 관리
"""

import json
import os
import random
from datetime import datetime
from quiz import Quiz


class QuizGame:
    """
    퀴즈 게임을 관리하는 클래스
    
    속성:
        data_file (str): 데이터 저장 파일 경로
        quizzes (list): Quiz 객체 리스트
        best_score (int): 최고 점수
        history (list): 플레이 기록 리스트
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
        self.history = []
        self.selected_bonus = []
        self.load_data()
    
    def load_data(self):
        """
        파일에서 데이터 로드
        파일이 없거나 손상되면 기본 데이터로 초기화하고 복구
        """
        try:
            if not os.path.exists(self.data_file):
                print("ℹ️  데이터 파일을 찾을 수 없습니다. 기본 퀴즈 데이터를 사용합니다.")
                self._init_default_data()
                self.save_data()
                return

            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, dict):
                raise ValueError("데이터 형식이 올바르지 않습니다.")

            quizzes_data = data.get("quizzes")
            if not isinstance(quizzes_data, list):
                raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

            self.quizzes = [Quiz.from_dict(q) for q in quizzes_data]
            self.best_score = data.get("best_score", 0)
            if not isinstance(self.best_score, int):
                raise ValueError("최고 점수 형식이 올바르지 않습니다.")

            history_data = data.get("history", [])
            if not isinstance(history_data, list):
                raise ValueError("기록 데이터 형식이 올바르지 않습니다.")
            self.history = [record for record in history_data if isinstance(record, dict)]

            selected_bonus_data = data.get("selected_bonus", [])
            if not isinstance(selected_bonus_data, list):
                raise ValueError("보너스 과제 데이터 형식이 올바르지 않습니다.")
            self.selected_bonus = [item for item in selected_bonus_data if isinstance(item, int)]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError) as e:
            print("⚠️  데이터 파일 로드 중 오류가 발생했습니다. 기본 데이터로 복구합니다.")
            print(f"   오류: {e}")
            self._init_default_data()
            try:
                self.save_data()
            except Exception:
                pass

    def _init_default_data(self):
        """기본 데이터로 초기화"""
        self.quizzes = [
            Quiz(
                "파이썬은 몇 년에 만들어졌을까?",
                ["1989년", "1991년", "1995년", "1999년"],
                1,
                "파이썬은 1991년에 공식 발표되었습니다."
            ),
            Quiz(
                "다음 중 파이썬의 창시자는?",
                ["Guido van Rossum", "Bjarne Stroustrup", "Dennis Ritchie", "Niklaus Wirth"],
                0,
                "파이썬의 창시자는 네덜란드 개발자입니다."
            ),
            Quiz(
                "파이썬에서 변수의 자료형을 확인하는 함수는?",
                ["python", "type()", "upper()", "dict[]"],
                1,
                "자료형을 알려주는 함수는 type입니다."
            ),
            Quiz(
                "리스트를 만들 때 사용하는 구분자는?",
                ["()", "{}", "[]", "<>"],
                2,
                "리스트는 대괄호로 만듭니다."
            ),
            Quiz(
                "문자열을 모두 대문자로 바꾸는 메서드는?",
                ["range()", "type()", "dict[]", "upper()"],
                3,
                "문자열 대문자 변환 메서드는 upper입니다."
            ),
            Quiz(
                "None 은 파이썬에서 무엇을 의미하는가?",
                ["빈 값", "\"None\"", "\"    \"", "\"1234\""],
                0,
                "None은 값이 없음을 뜻합니다."
            )
        ]
        self.best_score = 0
        self.history = []
        self.selected_bonus = []
    
    def save_data(self):
        """
        데이터를 파일에 저장 (UTF-8 인코딩)
        """
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
                "history": self.history,
                "selected_bonus": self.selected_bonus
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            # print("✅ 데이터가 저장되었습니다.")
        except Exception as e:
            print(f"❌ 저장 중 오류 발생: {e}")
    
    def add_quiz(self, question, choices, answer, hint=""):
        """
        새로운 퀴즈 추가
        
        Args:
            question (str): 퀴즈 질문
            choices (list): 선택지 리스트
            answer (int): 정답의 인덱스
            hint (str): 힌트 텍스트
        
        Returns:
            bool: 성공 여부
        """
        if len(choices) != 4:
            print("❌ 선택지는 정확히 4개여야 합니다.")
            return False
        
        if not (0 <= answer <= 3):
            print("❌ 정답 인덱스는 0~3 사이여야 합니다.")
            return False
        
        quiz = Quiz(question, choices, answer, hint)
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
    
    def record_history(self, question_count, correct_count, score, hints_used):
        """플레이 기록을 저장한다."""
        self.history.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "questions": question_count,
            "correct": correct_count,
            "score": score,
            "hints_used": hints_used
        })
    
    def get_all_quizzes(self):
        """모든 퀴즈 반환"""
        return self.quizzes
    
    def get_best_score(self):
        """현재 최고 점수 반환"""
        return self.best_score
    
    def get_history(self):
        """플레이 기록 반환"""
        return self.history

    def get_selected_bonus(self):
        """선택된 보너스 과제 인덱스 리스트 반환"""
        return self.selected_bonus

    def toggle_bonus_task(self, index):
        """보너스 과제 선택 상태를 토글한다."""
        if index in self.selected_bonus:
            self.selected_bonus.remove(index)
            return False
        self.selected_bonus.append(index)
        return True

    def quiz_count(self):
        """저장된 퀴즈 개수 반환"""
        return len(self.quizzes)
