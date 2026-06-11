/* ============================================================
   LIGHTBOX — click-to-enlarge for scanned manual pages.
   Vanilla JS + native <dialog>: no libraries, ~2KB.
   Usage: <button data-lightbox="group-name" data-caption="…">
            <picture>…<img …></picture>
          </button>
   Arrow keys / buttons navigate within the same group.
   ESC (native), backdrop click, or × closes.
   ============================================================ */
(function () {
    'use strict';

    var dialog = null;
    var group = [];
    var index = 0;

    function build() {
        if (dialog) return dialog;
        dialog = document.createElement('dialog');
        dialog.className = 'lightbox';
        dialog.setAttribute('aria-label', 'Enlarged page view');
        dialog.innerHTML =
            '<button type="button" class="lightbox__close" aria-label="Close enlarged view">&times;</button>' +
            '<button type="button" class="lightbox__nav lightbox__nav--prev" aria-label="Previous page">&#8249;</button>' +
            '<figure class="lightbox__figure">' +
            '  <img class="lightbox__img" alt="" />' +
            '  <figcaption class="lightbox__caption"></figcaption>' +
            '</figure>' +
            '<button type="button" class="lightbox__nav lightbox__nav--next" aria-label="Next page">&#8250;</button>';
        document.body.appendChild(dialog);

        dialog.querySelector('.lightbox__close').addEventListener('click', function () { dialog.close(); });
        dialog.querySelector('.lightbox__nav--prev').addEventListener('click', function () { show(index - 1); });
        dialog.querySelector('.lightbox__nav--next').addEventListener('click', function () { show(index + 1); });

        /* Backdrop click closes — the figure itself swallows inner clicks */
        dialog.addEventListener('click', function (e) {
            if (e.target === dialog) dialog.close();
        });

        dialog.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowLeft') { e.preventDefault(); show(index - 1); }
            else if (e.key === 'ArrowRight') { e.preventDefault(); show(index + 1); }
        });

        return dialog;
    }

    function show(i) {
        if (!group.length) return;
        index = (i + group.length) % group.length;
        var trigger = group[index];
        var thumb = trigger.querySelector('img');
        var img = dialog.querySelector('.lightbox__img');
        /* currentSrc resolves the <picture> WebP/JPEG choice the browser made */
        img.src = (thumb.currentSrc || thumb.src);
        img.alt = thumb.alt || '';
        dialog.querySelector('.lightbox__caption').textContent =
            trigger.getAttribute('data-caption') || thumb.alt || '';
        var multi = group.length > 1;
        dialog.querySelector('.lightbox__nav--prev').hidden = !multi;
        dialog.querySelector('.lightbox__nav--next').hidden = !multi;
    }

    document.addEventListener('click', function (e) {
        var trigger = e.target.closest('[data-lightbox]');
        if (!trigger) return;
        e.preventDefault();
        var key = trigger.getAttribute('data-lightbox');
        group = Array.prototype.slice.call(
            document.querySelectorAll('[data-lightbox="' + key + '"]')
        );
        build();
        show(group.indexOf(trigger));
        if (!dialog.open) dialog.showModal();
    });
})();
