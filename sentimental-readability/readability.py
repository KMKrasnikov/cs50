from cs50 import get_string
# Get text
text = get_string("Text: ")
l = 0
s = 0
w = 1

# Check simbols and count
for i in text:
    if i.isalpha():
        l += 1
    elif i == '.' or i == '!' or i == '?':
        s += 1
    elif i == ' ':
        w += 1

# Count grade
l = l / w * 100
s = s / w * 100
index = 0.0588 * l - 0.296 * s - 15.8

# Print grade
if index >= 16:
    print("Grade 16+")
elif index < 1:
    print("Before Grade 1")
else:
    print(f"Grade {round(index)}")