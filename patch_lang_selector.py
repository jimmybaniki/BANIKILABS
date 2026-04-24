from pathlib import Path

root = Path('.')
fragment = '''                <div class="relative">
                    <button id="langBtn" class="flex items-center text-gray-400 hover:text-[var(--gold)] font-bold text-[10px] uppercase tracking-widest transition duration-150">
                        <span id="currentLangDisplay">FR</span>
                        <svg class="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M19 9l-7 7-7-7" stroke-width="3"/></svg>
                    </button>
                    <div id="langMenu" class="absolute right-0 mt-2 w-32 rounded-xl shadow-2xl bg-neutral-900 border border-white/10 z-20 hidden overflow-hidden">
                        <a href="#" class="lang-option block px-4 py-2 text-xs font-bold text-gray-400 hover:bg-[var(--gold)] hover:text-black" data-lang="fr">FRANÇAIS</a>
                        <a href="#" class="lang-option block px-4 py-2 text-xs font-bold text-gray-400 hover:bg-[var(--gold)] hover:text-black" data-lang="en">ENGLISH</a>
                        <a href="#" class="lang-option block px-4 py-2 text-xs font-bold text-gray-400 hover:bg-[var(--gold)] hover:text-black" data-lang="sw">KISWAHILI</a>
                    </div>
                </div>
'''
script = '''    <script>
        const translations = {
            fr: {},
            en: {},
            sw: {}
        };

        let currentLang = 'fr';

        function setLanguage(lang) {
            currentLang = lang;
            document.getElementById('currentLangDisplay').textContent = lang.toUpperCase();
            document.documentElement.lang = lang;

            // Update all elements with data-translate or data-key
            document.querySelectorAll('[data-translate], [data-key]').forEach(el => {
                const key = el.getAttribute('data-translate') || el.getAttribute('data-key');
                if (translations[lang][key]) {
                    el.innerHTML = translations[lang][key];
                }
            });

            // Store in localStorage
            localStorage.setItem('lang', lang);
        }

        // Language selector functionality
        document.addEventListener('DOMContentLoaded', function() {
            const langBtn = document.getElementById('langBtn');
            const langMenu = document.getElementById('langMenu');
            if (!langBtn || !langMenu) return;
            langBtn.addEventListener('click', function(event) {
                event.preventDefault();
                langMenu.classList.toggle('hidden');
            });
            document.querySelectorAll('.lang-option').forEach(option => {
                option.addEventListener('click', function(event) {
                    event.preventDefault();
                    const lang = this.getAttribute('data-lang');
                    setLanguage(lang);
                    langMenu.classList.add('hidden');
                });
            });
            document.addEventListener('click', function(event) {
                if (!langBtn.contains(event.target) && !langMenu.contains(event.target)) {
                    langMenu.classList.add('hidden');
                }
            });
            // Load saved language
            const savedLang = localStorage.getItem('lang') || 'fr';
            setLanguage(savedLang);
        });
    </script>\n'''
updated = []
for path in sorted(root.glob('*.html')):
    text = path.read_text(encoding='utf-8')
    if 'id="langBtn"' in text:
        continue
    if '<div class="flex items-center gap-' in text:
        new_text = text.replace('<div class="flex items-center gap-', '<div class="flex items-center gap-\n' + fragment, 1)
        if 'document.querySelectorAll(\'.lang-option\')' not in new_text and '</body>' in new_text:
            new_text = new_text.replace('</body>', script + '</body>')
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            updated.append(path.name)
report = root / 'lang-update-report.txt'
report.write_text('\n'.join(updated), encoding='utf-8')
print('updated', updated)
