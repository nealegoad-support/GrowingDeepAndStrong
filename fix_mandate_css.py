import re

# Update coach.html
with open('coach.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The section uses class="mandate" and inner classes mandate__*
# Let's replace 'class="mandate"' with 'class="coach-mandate"'
content = content.replace('class="mandate"', 'class="coach-mandate"')
content = content.replace('mandate__', 'coach-mandate__')

with open('coach.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
in_coach_mandate_section = False
for i, line in enumerate(lines):
    # CSS region C2 is for COACH'S MANDATE starting at ~2367
    if "C2. COACH'S MANDATE" in line:
        in_coach_mandate_section = True
    
    # CSS region C3 is for 4-PHASE COACH JOURNEY starting at ~2497
    if "C3. 4-PHASE COACH JOURNEY" in line:
        in_coach_mandate_section = False
    
    if in_coach_mandate_section:
        line = line.replace('.mandate', '.coach-mandate')
        
    # Also update the `.mandate__copy` near line 2954
    if '.mandate__copy' in line:
        line = line.replace('.mandate__copy', '.coach-mandate__copy')
        
    new_lines.append(line)

with open('style.css', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Updated coach.html and style.css")
