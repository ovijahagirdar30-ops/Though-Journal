thought = input("Enter thought:  " )

print(thought)

with open("thoughts.txt", "a") as file:
    file.write(thought + "\n")