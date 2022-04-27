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
        #           flashcards.append(flashcard)
        else:
            print(f"{sub_selection} is not an option")
        print()
    return


def practice_flashcards():
    flashcards = session.query(Flashcard).all()
    if flashcards is not None:
        for flashcard in flashcards:
            print(f"Question: {flashcard.question}")
            print('Please press "y" to see the answer or press "n" to skip:')
            if input() == "y":
                print()
                print(f"Answer: {flashcard.answer}")
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
