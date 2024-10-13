import re

def get_tag_text(text):
    match = re.search(r'<([^>]+)>(.*?)</\1>', text, re.DOTALL)
    if match:
        return match.group(2)
    else:
        raise ValueError(f"Invalid format: No closing tag found in text '{text}'")

def main():
    test_cases = [
        "<filename>GarlicNutriSpice</filename>",
        "GarlicNutriSpice",
        "<file>GarlicNutriSpice",
        "GarlicNutriSpice<	ag>",
        "<file>GarlicNutriSpice</wrong_tag>"
    ]

    for case in test_cases:
        try:
            result = get_tag_text(case)
            print(f"Input: {case}")
            print(f"Output: {result}")
        except ValueError as e:
            print(f"Input: {case}")
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
