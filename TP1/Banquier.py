def func():
    val=2.71828
    for i in range(1,50):
        val= val - 1.0
        val*=i
        print(val)
    print(val)
    with open("answer_banquier.txt", "w", encoding="utf-8") as answer_file:
            answer_file.write(
                f"Résultat: {val})\n"
            )    
func()
