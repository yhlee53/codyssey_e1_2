"""
퀴즈 게임 - 메인 프로그램
터미널에서 동작하는 메뉴 기반 퀴즈 게임
"""

import random
from quiz_game import QuizGame

BONUS_TASKS = [
    "랜덤 출제     - 퀴즈 풀기에 적용",
    "문제 수 선택   - 퀴즈 풀기에 적용",
    "힌트 기능      - 퀴즈 풀기에 적용(힌트 : + 정답)",
    "퀴즈 삭제 기능   - 메뉴 추가",
    "점수 기록 히스토리 -  메뉴 추가"
]


def build_menu_options(game):
    """보너스 선택에 따라 동적 메뉴 옵션 리스트를 생성한다.

    Returns: list of (label, handler_function or None)
    """
    options = []
    options.append(("🎯 퀴즈 풀기", play_quiz))
    options.append(("➕ 퀴즈 추가", add_quiz))

    # '퀴즈 삭제 기능' 보너스가 선택된 경우 메뉴에 추가
    if 3 in game.get_selected_bonus():
        options.append(("🗑️  퀴즈 삭제", delete_quiz))

    options.append(("📋 퀴즈 목록", show_quiz_list))

    # '점수 기록 히스토리' 보너스가 선택된 경우 메뉴에 추가
    if 4 in game.get_selected_bonus():
        options.append(("🏆 최고 점수 확인", show_scores))
        options.append(("📜 플레이 기록 보기", show_history))

    options.append((f"✨ 보너스 과제 선택 ({len(game.get_selected_bonus())}개)", select_bonus_tasks))
    options.append(("🚪 종료", None))
    return options


def render_menu(game, options):
    """헤더와 동적 옵션을 출력한다."""
    quiz_count = game.quiz_count()
    max_score = game.get_best_score()
    print("\n" + "="*60)
    print(f"       🎮 퀴즈 게임 메뉴 (퀴즈 {quiz_count}개, 최고점수 {max_score}점) 🎮")
    print("="*60)
    for idx, (label, _) in enumerate(options, 1):
        print(f"{idx}. {label}")
    print("="*60)


def display_menu(game):
    # 저장된 데이터 정보 표시
    quiz_count = game.quiz_count()
    max_score = game.get_best_score()
    # print(f"\n📂 저장된 데이터를 불러왔습니다. (퀴즈 {quiz_count}개, 최고점수 {max_score}점)")

    """메인 메뉴 표시"""
    # 기존 정적 메뉴는 사용하지 않고, 동적 메뉴는 main 루프에서 생성하여 전달합니다.
    print("\n" + "="*60)
    print(f"       🎮 퀴즈 게임 메뉴 (퀴즈 {quiz_count}개, 최고점수 {max_score}점) 🎮")
    print("="*60)
    print("이 메뉴는 동적으로 생성됩니다. 메인 루프에서 항목을 확인하세요.")
    print("="*60)


def get_user_choice(max_choice):
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
            if not choice.isdigit():
                print(f"❌ 1~{max_choice} 사이의 숫자를 입력해주세요.")
                continue
            num = int(choice)
            if num < 1 or num > max_choice:
                print(f"❌ 1~{max_choice} 사이의 숫자를 입력해주세요.")
                continue
            return str(num)
        except KeyboardInterrupt:
            print("\n\n프로그램이 중단되었습니다.")
            return str(max_choice)
        except EOFError:
            return str(max_choice)


def get_question_count(total_count):
    """사용자가 풀 문제 수를 선택하도록 한다."""
    while True:
        try:
            choice = input(f"\n몇 문제를 풀까요? (1~{total_count}, Enter=전체): ").strip()
            if not choice:
                return total_count
            count = int(choice)
            if count < 1 or count > total_count:
                print(f"❌ 1에서 {total_count} 사이의 숫자를 입력해주세요.")
                continue
            return count
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n\n퀴즈 선택이 중단되었습니다.")
            return total_count
        except EOFError:
            return total_count


def select_bonus_tasks(game):
    """보너스 과제를 선택하거나 해제한다."""
    while True:
        print("\n" + "="*50)
        print("✨ 보너스 과제 선택")
        print("="*50)
        for idx, task in enumerate(BONUS_TASKS, 1):
            checked = "x" if idx - 1 in game.get_selected_bonus() else " "
            print(f"  {idx}. [{checked}] {task}")
        print("  0. 완료")

        try:
            choice = input("\n선택할 과제 번호를 입력하세요 (0: 완료): ").strip()
            if not choice:
                print("⚠️  입력이 비어있습니다.")
                continue
            if choice == '0':
                return

            selected_index = int(choice) - 1
            if selected_index < 0 or selected_index >= len(BONUS_TASKS):
                print(f"❌ 1에서 {len(BONUS_TASKS)} 사이의 번호를 입력해주세요.")
                continue

            is_selected = game.toggle_bonus_task(selected_index)
            game.save_data()
            status = "선택됨" if is_selected else "해제됨"
            print(f"✅ '{BONUS_TASKS[selected_index]}' 보너스 과제 {status}.")
        except ValueError:
            print("❌ 숫자를 입력해주세요.")
        except KeyboardInterrupt:
            print("\n\n보너스 과제 선택이 중단되었습니다.")
            return
        except EOFError:
            return


def play_quiz(game):
    """
    전체 퀴즈 풀기
    
    Args:
        game (QuizGame): QuizGame 인스턴스
    """
    if game.quiz_count() == 0:
        print("❌ 저장된 퀴즈가 없습니다.")
        return
    
    total_count = game.quiz_count()
    selected_bonus = game.get_selected_bonus()

    # 문제 수 선택 보너스가 활성화된 경우에만 사용자에게 문제 수를 물어본다.
    if 1 in selected_bonus:
        question_count = get_question_count(total_count)
    else:
        question_count = total_count

    quizzes_all = game.get_all_quizzes()
    # 랜덤 출제 보너스가 활성화된 경우에만 문제를 랜덤으로 선택
    if 0 in selected_bonus:
        selected_quizzes = random.sample(quizzes_all, question_count)
    else:
        selected_quizzes = quizzes_all[:question_count]
    correct_count = 0
    hint_used_count = 0
    
    print(f"\n📝 퀴즈를 시작합니다! (총 {question_count}문제)")
    print("-" * 50)
    
    try:
        for idx, quiz in enumerate(selected_quizzes, 1):
            print(f"\n[문제 {idx}/{question_count}]")
            quiz.display()
            
            while True:
                try:
                    answer_str = input(f"\n정답을 선택하세요 (1~4, h: 힌트-{quiz.answer + 1}): ").strip()
                    if not answer_str:
                        print("⚠️  입력이 비어있습니다.")
                        continue

                    if answer_str.lower() == 'h':
                        hint_text = quiz.get_hint_text()
                        if hint_text:
                            # 요청에 따라 힌트 출력 형식: "힌트: {힌트텍스트} | {정답번호}"
                            print(f"힌트:{hint_text} | {quiz.answer + 1}")
                            hint_used_count += 1
                        else:
                            print("ℹ️  이 문제에는 힌트가 없습니다.")
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
        
        score = int((correct_count / question_count) * 100)
        deduction = hint_used_count * 10
        if deduction > 0:
            score = max(0, score - deduction)

        print("\n" + "="*50)
        print(f"🏆 결과: {question_count}문제 중 {correct_count}문제 정답! ({score}점)")
        if hint_used_count > 0:
            print(f"💡 힌트 사용 {hint_used_count}회로 {deduction}점 감점되었습니다.")
        
        old_max_score = game.get_best_score()
        game.update_score(score)
        game.record_history(question_count, correct_count, score, hint_used_count)
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
        
        hint = input("힌트를 입력하세요 (선택, 없으면 Enter): ").strip()

        # 퀴즈 추가
        if game.add_quiz(question, choices, answer_idx, hint):
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
    최고 점수 및 플레이 기록 표시
    
    Args:
        game (QuizGame): QuizGame 인스턴스
    """
    best_score = game.get_best_score()
    history = game.get_history()
    
    if not history:
        print("\n📊 아직 푼 퀴즈가 없습니다.")
        if best_score > 0:
            print(f"🏆 현재 최고 점수: {best_score}점")
        return
    
    print("\n" + "="*40)
    print("🏆 최고 점수 및 플레이 기록")
    print("="*40)
    print(f"전체 최고 점수: {best_score}점")
    print()
    print("📜 플레이 기록:")
    for record in history[-5:]:
        print(f"  {record['timestamp']} - {record['questions']}문제, {record['correct']}정답, {record['score']}점, 힌트 {record['hints_used']}회")


def show_history(game):
    """플레이 기록 전체를 출력하고 삭제할 수 있는 옵션을 제공한다."""
    history = game.get_history()
    if not history:
        print("\n📜 저장된 플레이 기록이 없습니다.")
        return

    print("\n" + "="*50)
    print("📜 플레이 기록 전체")
    print("="*50)
    for idx, record in enumerate(history, 1):
        print(f"{idx}. {record['timestamp']} - {record['questions']}문제, {record['correct']}정답, {record['score']}점, 힌트 {record['hints_used']}회")

    # 기록 초기화 옵션
    while True:
        try:
            choice = input("\n기록을 삭제하려면 'd' 입력, 아니면 Enter: ").strip().lower()
            if not choice:
                return
            if choice == 'd':
                confirm = input("정말 모든 기록을 삭제하시겠습니까? (y/n): ").strip().lower()
                if confirm in ['y', 'yes']:
                    game.history = []
                    game.save_data()
                    print("✅ 모든 플레이 기록을 삭제했습니다.")
                else:
                    print("삭제를 취소했습니다.")
                return
            else:
                print("⚠️ 잘못된 입력입니다. Enter 또는 'd'를 입력하세요.")
        except KeyboardInterrupt:
            print("\n\n작업이 중단되었습니다.")
            return
        except EOFError:
            return


def main():
    """메인 함수"""
    game = QuizGame()
    
    # print("\n" + "🎮 "*5)
    # print("   퀴즈 게임에 환영합니다!")
    # print("🎮 "*5)
       
    while True:
        options = build_menu_options(game)
        render_menu(game, options)
        choice = get_user_choice(len(options))

        try:
            idx = int(choice) - 1
        except Exception:
            continue

        handler = options[idx][1]
        if handler is None:
            print("\n데이터를 저장하고 있습니다...")
            game.save_data()
            print("👋 프로그램을 종료합니다. 안녕히 가세요!\n\n")
            break

        # 실행
        try:
            handler(game)
        except Exception as e:
            print(f"❌ 메뉴 실행 중 오류가 발생했습니다: {e}")


if __name__ == "__main__":
    main()
