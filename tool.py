from collections import defaultdict
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

main_menu = """1. Add flashcards
2. Practice flashcards
3. Exit"""
sub_menu = """1. Add a new flashcard
2. Exit"""

engine = create_engine("sqlite:///flashcard.db?check_same_thread=False")
Base = declarative_base()


class Flashcard(Base):
    __tablename__ = "flashcard"
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box_number = Column(Integer, default=1)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def display_main_menu():
    print(main_menu)


def add_flashcards():
    while True:
        flashcard = defaultdict(str)
        print(sub_menu)
        sub_selection = input()
        print()
        if sub_selection == "2":
            break
        elif sub_selection == "1":

            while True:
                print("Question:")
                question = input()
                if question.strip() == "" or not question:
                    pass
                else:
                    break

            while True:
                print("Answer:")
                answer = input()
                if answer.strip() == "" or not answer:
                    pass
                else:
                    break
            flashcard["question"] = question
            flashcard["answer"] = answer
            session.add(Flashcard(question=question, answer=answer))
            session.commit()
        else:
            print(f"{sub_selection} is not an option")
        print()
    return


def practice_flashcards():
    flashcards = (
        (
            session.query(Flashcard)
            .filter(Flashcard.box_number >= 1)
            .filter(Flashcard.box_number <= 3)
        )
        .order_by(Flashcard.box_number.desc())
        .all()
    )
    if bool(flashcards):
        for flashcard in flashcards:
            current_flashcard = session.query(Flashcard).filter(
                Flashcard.question == flashcard.question
            )
            print(f"Question: {flashcard.question}")
            while True:
                print('press "y" to see the answer:')
                print('press "n" to skip:')
                print('press "u" to update:')
                practice_input = input()
                if practice_input in ("y", "n", "u"):
                    if practice_input == "y":
                        print(f"Answer: {flashcard.answer}")
                        while True:
                            print('press "y" if your answer is correct:')
                            print('press "n" if your answer is wrong:')
                            leitner_input = input()
                            if leitner_input in ("y", "n"):
                                if leitner_input == "y":
                                    current_flashcard.update(
                                        {"box_number": Flashcard.box_number + 1}
                                    )
                                elif leitner_input == "n":
                                    current_flashcard.update({"box_number": 1})
                                session.commit()
                                if current_flashcard.first().box_number > 3:
                                    current_flashcard.delete()
                                    session.commit()
                                break
                            else:
                                print(leitner_input, "is not an option")
                    elif practice_input == "n":
                        return
                    elif practice_input == "u":

                        while True:
                            print('press "d" to delete the flashcard:')
                            print('press "e" to edit the flashcard:')
                            update_input = input()
                            if update_input in ("e", "d"):
                                if update_input == "e":
                                    print()
                                    print(f"current question: {flashcard.question}")
                                    print("please write a new question:")
                                    new_question = input()

                                    print()
                                    print(f"current answer: {flashcard.answer}")
                                    print("please write a new answer:")
                                    new_answer = input()

                                    current_flashcard.update(
                                        {"question": new_question, "answer": new_answer}
                                    )
                                    session.commit()
                                    break
                                elif update_input == "d":
                                    current_flashcard.delete()
                                    break
                            else:
                                print(update_input, "is not an option")
                    break
                else:
                    print(practice_input, "is not an option")
            print()
    else:
        print("There is no flashcard to practice!")


def play(main_selection: int):
    if main_selection == 1:
        add_flashcards()
    elif main_selection == 2:
        practice_flashcards()
    else:
        print(f"{main_selection} is not an option")


if __name__ == "__main__":
    while True:
        display_main_menu()
        menu = input()
        print()
        try:
            menu = int(menu)
        except ValueError:
            print(f"{menu} is not an option")
        else:
            if menu == 3:
                break
            play(menu)
        print()

    print("Bye!")
