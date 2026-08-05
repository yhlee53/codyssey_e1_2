"""
퀴즈 게임 - 메인 프로그램
터미널에서 동작하는 메뉴 기반 퀴즈 게임
"""

from quiz_game import QuizGame


def display_menu(game):
    # 저장된 데이터 정보 표시
    quiz_count = game.quiz_count()
    max_score = game.get_best_score()
    # print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {max_score}점)")

    """메인 메뉴 표시"""
    print("\n" + "="*60)
    print(f"       🎮 퀴즈 게임 메뉴 (퀴즈 {quiz_count}개, 최고점수 {max_score}점) 🎮")
    print("="*60)
    print("1. 🎯 퀴즈 풀기")
    print("2. ➕ 퀴즈 추가")
    print("3. 🗑️  퀴즈 삭제")
    print("4. 📋 퀴즈 목록")
    print("5. 🏆 최고 점수 확인")
    print("6. 🚪 종료")
    print("="*60)


def get_user_choice():
    """
    사용자로부터 메뉴 선택 입력받기
    
    Returns:
        str: 사용자가 입력한 선택
    """
    while True:
        try:
            choice = input("\n선택: ").strip()
            if not choice:
                print("⚠️  입력이 비어있습니다. 다시 입력해주세요.")
                continue
            if choice not in ['1', '2', '3', '4', '5', '6']:
                print("❌ 1~6 사이의 숫자를 입력해주세요.")
                continue
            return choice
        except KeyboardInterrupt:
            print("\n\n프로그램이 중단되었습니다.")
            return '6'
        except EOFError:
            return '6'


def play_quiz(game):
    """
    전체 퀴즈 풀기
    
    Args:
        game (QuizGame): QuizGame 인스턴스
    """
    if game.quiz_count() == 0:
        print("❌ 저장된 퀴즈가 없습니다.")
        return
    
    quizzes = game.get_all_quizzes()
    total_count = len(quizzes)
    correct_count = 0
    
    print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")
    print("-" * 50)
    
    try:
        for idx, quiz in enumerate(quizzes, 1):
            print(f"\n[문제 {idx}/{total_count}]")
            quiz.display()
            
            while True:
                try:
                    answer_str = input("\n정답을 선택하세요 (1~4): ").strip()
                    if not answer_str:
                        print("⚠️  입력이 비어있습니다.")
                        continue
                    answer = int(answer_str)
                    if answer not in [1, 2, 3, 4]:
                        print("❌ 1~4 사이의 숫자를 입력해주세요.")
                        continue
                    
                    if quiz.is_correct(answer):
                        print("✅ 정답입니다!")
                        correct_count += 1
                    else:
                        correct_answer = quiz.get_correct_answer_text()
                        print(f"❌ 오답입니다. 정답은: {correct_answer}")
                    print("-" * 50)
                    break
                except ValueError:
                    print("❌ 숫자를 입력해주세요.")
        
        # 최종 결과 계산 및 표시
        score = int((correct_count / total_count) * 100)
        
        print("\n" + "="*50)
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")
        
        # 최고 점수 업데이트 및 비교
        old_max_score = game.get_best_score()
        game.update_score(score)
        game.save_data()
        
        if score > old_max_score:
            print("🎉 새로운 최고 점수입니다!")
        
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n\n퀴즈 풀기가 중단되었습니다.")
    except EOFError:
        pass


def add_quiz(game):
    """
    새로운 퀴즈 추가
    
    Args:
        game (QuizGame): QuizGame 인스턴스
    """
    print("\n📝 새로운 퀴즈를 추가합니다.")
    
    try:
        question = input("질문을 입력하세요: ").strip()
        if not question:
            print("⚠️  질문이 비어있습니다.")
            return
        
        # 선택지 입력
        print("선택지를 입력하세요 (4개를 쉼표로 구분):")
        choices_input = input("예) 선택지1, 선택지2, 선택지3, 선택지4\n입력: ").strip()
        choices = [c.strip() for c in choices_input.split(',')]
        
        if len(choices) != 4:
            print(f"❌ 선택지는 정확히 4개여야 합니다. (입력된 개수: {len(choices)})")
            return
        
        # 정답 선택
        for idx, choice in enumerate(choices):
            print(f"  {idx + 1}. {choice}")
        
        while True:
            answer_str = input("정답의 번호를 선택하세요 (1~4): ").strip()
            try:
                answer = int(answer_str)
                if answer not in [1, 2, 3, 4]:
                    print("❌ 1~4 사이의 숫자를 입력해주세요.")
                    continue
                answer_idx = answer - 1  # 0 기반 인덱스로 변환
                break
            except ValueError:
                print("❌ 숫자를 입력해주세요.")
        
        # 퀴즈 추가
        if game.add_quiz(question, choices, answer_idx):
            game.save_data()
    
    except KeyboardInterrupt:
        print("\n\n퀴즈 추가가 중단되었습니다.")
    except EOFError:
        pass


def delete_quiz(game):
    """
    저장된 퀴즈 삭제
    
    Args:
        game (QuizGame): QuizGame 인스턴스
    """
    quizzes = game.get_all_quizzes()
    
    if not quizzes:
        print("❌ 저장된 퀴즈가 없습니다.")
        return
    
    print("\n🗑️ 삭제할 퀴즈를 선택하세요.")
    for idx, quiz in enumerate(quizzes, 1):
        print(f"{idx}. {quiz.question}")
    
    while True:
        try:
            choice = input("\n삭제할 번호를 입력하세요 (0: 취소): ").strip()
            if choice == '0':
                print("삭제를 취소했습니다.")
                return
            
            index = int(choice) - 1
            if not (0 <= index < len(quizzes)):
                print("❌ 올바른 번호를 입력해주세요.")
                continue
            
            confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("삭제를 취소했습니다.")
                return
            
            if game.delete_quiz(index):
                game.save_data()
            break
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n\n삭제가 중단되었습니다.")
            return
        except EOFError:
            return


def show_quiz_list(game):
    """
    저장된 모든 퀴즈 목록 표시
    
    Args:
        game (QuizGame): QuizGame 인스턴스
    """
    quizzes = game.get_all_quizzes()
    
    if not quizzes:
        print("❌ 저장된 퀴즈가 없습니다.")
        return
    
    print("\n" + "="*50)
    print(f"📋 등록된 퀴즈 목록 (총 {len(quizzes)}개)")
    print("="*50)
    
    for idx, quiz in enumerate(quizzes, 1):
        print(f"  {idx}. {quiz.question}")


def show_scores(game):
    """
    최고 점수 표시
    
    Args:
        game (QuizGame): QuizGame 인스턴스
    """
    best_score = game.get_best_score()
    
    if best_score == 0:
        print("\n📊 아직 푼 퀴즈가 없습니다.")
        return
    
    print("\n" + "="*30)
    print("🏆 최고 점수")
    print("="*30)
    print(f"전체: {best_score}점")


def main():
    """메인 함수"""
    game = QuizGame()
    
    # print("\n" + "🎮 "*5)
    # print("   퀴즈 게임에 환영합니다!")
    # print("🎮 "*5)
       
    while True:
        display_menu(game)
        choice = get_user_choice()
        
        if choice == '1':
            play_quiz(game)
        elif choice == '2':
            add_quiz(game)
        elif choice == '3':
            delete_quiz(game)
        elif choice == '4':
            show_quiz_list(game)
        elif choice == '5':
            show_scores(game)
        elif choice == '6':
            print("\n데이터를 저장하고 있습니다...")
            game.save_data()
            print("👋 프로그램을 종료합니다. 안녕히 가세요!")
            break


if __name__ == "__main__":
    main()
