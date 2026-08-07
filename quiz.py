"""
Quiz 클래스 - 개별 퀴즈 관리
"""


class Quiz:
    """
    퀴즈를 관리하는 클래스
    
    속성:
        question (str): 퀴즈 질문
        choices (list): 선택지 리스트
        answer (int): 정답의 인덱스
        hint (str): 힌트 텍스트
    """
    
    def __init__(self, question, choices, answer, hint=""):
        """
        Quiz 인스턴스 초기화
        
        Args:
            question (str): 퀴즈 질문
            choices (list): 선택지 리스트 (4개)
            answer (int): 정답의 인덱스 (0~3)
            hint (str): 힌트 텍스트 (선택)
        """
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint
    
    def display(self):
        """퀴즈를 보기 좋게 표시"""
        print(f"\nQ: {self.question}")
        for idx, choice in enumerate(self.choices):
            print(f"  {idx + 1}. {choice}")
    
    def is_correct(self, user_answer):
        """
        사용자의 답변이 정답인지 확인
        
        Args:
            user_answer (int): 사용자가 선택한 번호 (1~4)
        
        Returns:
            bool: 정답이면 True, 오답이면 False
        """
        return (user_answer - 1) == self.answer
    
    def get_correct_answer_text(self):
        """정답을 텍스트로 반환"""
        return self.choices[self.answer]

    def get_hint_text(self):
        """힌트 텍스트를 반환"""
        return self.hint
    
    def to_dict(self):
        """퀴즈를 딕셔너리로 변환 (JSON 저장용)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }
    
    @staticmethod
    def from_dict(data):
        """딕셔너리로부터 Quiz 객체 생성"""
        return Quiz(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", "")
        )
