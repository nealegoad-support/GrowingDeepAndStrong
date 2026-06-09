import os
import re
import glob

nav_standard = """<div class="nav-strip">
            <nav class="primary-nav" id="primary-nav" aria-label="Primary">
                <ul class="primary-nav__list">
                    <li><a href="index.html">Home</a></li>
                    <li class="has-dropdown">
                        <a href="new-christian-training.html" aria-haspopup="true" aria-expanded="false">
                            New Christian Training
                            <span class="caret" aria-hidden="true"></span>
                        </a>
                        <ul class="dropdown" role="menu">
                            <li role="none"><a role="menuitem" href="why-moves-of-god-succeeded-and-faded.html">Why Moves of God Succeeded and Faded</a></li>
                            <li role="none"><a role="menuitem" href="how-to-open-a-new-christian-training-center.html">How to Open a New Christian Training Center</a></li>
                            <li role="none"><a role="menuitem" href="curriculum.html">Curriculum</a></li>
                            <li role="none"><a role="menuitem" href="teacher-training-tutorials.html">Teacher Training Tutorials</a></li>
                        </ul>
                    </li>
                    <li class="has-dropdown">
                        <a href="coach.html" aria-haspopup="true" aria-expanded="false">
                            Be A Coach / Coaching
                            <span class="caret" aria-hidden="true"></span>
                        </a>
                        <ul class="dropdown" role="menu">
                            <li role="none"><a role="menuitem" href="coach.html">Be A Coach Online Training</a></li>
                        </ul>
                    </li>
                    <li><a href="disciple.html">Be A Disciple / Discipleship</a></li>
                    <li class="has-dropdown">
                        <a href="shop.html" aria-haspopup="true" aria-expanded="false">
                            Shop
                            <span class="caret" aria-hidden="true"></span>
                        </a>
                        <ul class="dropdown" role="menu">
                            <li role="none"><a role="menuitem" href="#">Return &amp; Refund Policy</a></li>
                        </ul>
                    </li>
                    <li class="has-dropdown">
                        <a href="#" aria-haspopup="true" aria-expanded="false">
                            Testimonies
                            <span class="caret" aria-hidden="true"></span>
                        </a>
                        <ul class="dropdown" role="menu">
                            <li role="none"><a role="menuitem" href="#">Endorsement</a></li>
                        </ul>
                    </li>
                </ul>
            </nav>
        </div>"""

footer_standard = """<footer class="site-footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col footer-col--brand">
                    <p class="footer-brand">Growing Deep <em>and</em> Strong<sup>®</sup></p>
                    <address>
                        Bairnsdale 3875<br />
                        Victoria, Australia<br />
                        <a href="mailto:info@growingdeepandstrong.com">info@growingdeepandstrong.com</a>
                    </address>
                    <ul class="social-list" aria-label="Social media">
                        <li><a href="#" aria-label="Facebook">Fb</a></li>
                        <li><a href="#" aria-label="Instagram">Ig</a></li>
                        <li><a href="#" aria-label="YouTube">Yt</a></li>
                        <li><a href="#" aria-label="LinkedIn">In</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Navigation</h4>
                    <ul class="footer-links">
                        <li><a href="index.html">Home</a></li>
                        <li><a href="#">About Us</a></li>
                        <li><a href="disciple.html">I Want to Be a Disciple</a></li>
                        <li><a href="coach.html">I Want to Coach Others</a></li>
                        <li><a href="curriculum.html">Curriculum / Course Outline</a></li>
                        <li><a href="shop.html">Shop</a></li>
                        <li><a href="#">Blog</a></li>
                        <li><a href="#">Testimonies</a></li>
                        <li><a href="new-christian-training.html">New Christian Training Hubs</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>Resources</h4>
                    <ul class="footer-links">
                        <li><a href="#">SEED for the Sower</a></li>
                        <li><a href="#">Strategic Blueprint (Free)</a></li>
                        <li><a href="#">Endorsement</a></li>
                        <li><a href="#">Contact Us</a></li>
                        <li><a href="#">Sitemap</a></li>
                        <li><a href="#">Disclaimer</a></li>
                        <li><a href="#">Terms of Service</a></li>
                        <li><a href="#">Privacy Statement</a></li>
                        <li><a href="#">Vision Decree</a></li>
                        <li><a href="#">Partners</a></li>
                    </ul>
                </div>
                <div class="footer-col footer-col--form">
                    <h4>Contact Us</h4>
                    <form class="contact-form" onsubmit="return false;">
                        <label class="visually-hidden" for="cf-name-nctc">Name</label>
                        <input type="text" id="cf-name-nctc" name="name" placeholder="Name" />
                        <label class="visually-hidden" for="cf-email-nctc">Email Address</label>
                        <input type="email" id="cf-email-nctc" name="email" placeholder="Email Address" />
                        <label class="visually-hidden" for="cf-message-nctc">Message</label>
                        <textarea id="cf-message-nctc" name="message" rows="4" placeholder="Message"></textarea>
                        <label for="cf-captcha-nctc" class="captcha-label">
                            <span>7 + 8 = ?</span>
                            <input type="text" id="cf-captcha-nctc" name="captcha" />
                        </label>
                        <button type="submit" class="btn btn--primary btn--block">Submit</button>
                    </form>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Growing Deep and Strong. All Rights Reserved.</p>
                <p>Digital Marketing Solutions by: <a href="#">Strategy Consultants Pty Ltd</a></p>
            </div>
        </div>
    </footer>"""

html_files = glob.glob('*.html')

for filepath in html_files:
    if "index-print.html" in filepath:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace nav strip
    nav_pattern = re.compile(r'<div class="nav-strip">.*?</nav>\s*</div>', re.DOTALL)
    if nav_pattern.search(content):
        content = nav_pattern.sub(nav_standard, content)
    else:
        print(f"Warning: nav-strip not found in {filepath}")

    # Replace footer
    footer_pattern = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)
    if footer_pattern.search(content):
        content = footer_pattern.sub(footer_standard, content)
    else:
        print(f"Warning: site-footer not found in {filepath}")

    # Inject aria-current="page"
    filename = os.path.basename(filepath)
    # Remove existing aria-current="page" just in case they slipped into the template somehow
    # (though nav_standard has none)
    
    # We want to match `href="filename"` and insert ` aria-current="page"`
    # Example: <a href="index.html"> -> <a href="index.html" aria-current="page">
    # Wait, the dropdown parents also need it? The top-level nav might be "new-christian-training.html" but we are on "curriculum.html".
    # For now, just add it to the EXACT matching filename:
    content = content.replace(f'href="{filename}"', f'href="{filename}" aria-current="page"')
    
    # If the user is on a sub-page of New Christian Training, the parent should also get aria-current.
    # The parent link is new-christian-training.html
    new_christian_pages = [
        "why-moves-of-god-succeeded-and-faded.html",
        "how-to-open-a-new-christian-training-center.html",
        "curriculum.html",
        "teacher-training-tutorials.html"
    ]
    if filename in new_christian_pages:
        content = content.replace('href="new-christian-training.html" aria-haspopup="true" aria-expanded="false"',
                                  'href="new-christian-training.html" aria-haspopup="true" aria-expanded="false" aria-current="page"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated navigation and footers for all HTML files.")
