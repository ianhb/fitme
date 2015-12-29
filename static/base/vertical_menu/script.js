(function ($) {
    $(document).ready(function () {
        var menu = $('#vertical_menu');
        menu.find('li.has-sub>a').on('click', function () {
            $(this).removeAttr('href');
            var element = $(this).parent('li');
            if (element.hasClass('open')) {
                element.removeClass('open');
                element.find('li').removeClass('open');
                element.find('ul').slideUp();
            }
            else {
                element.addClass('open');
                element.children().slideDown();
            }
        });

        menu.find('>ul>li.has-sub>a').append('<span class="holder"></span>');

        (function getColor() {
            var r, g, b;
            var textColor = menu.css('color');
            textColor = textColor.slice(4);
            r = textColor.slice(0, textColor.indexOf(','));
            textColor = textColor.slice(textColor.indexOf(' ') + 1);
            g = textColor.slice(0, textColor.indexOf(','));
            textColor = textColor.slice(textColor.indexOf(' ') + 1);
            b = textColor.slice(0, textColor.indexOf(')'));
            var l = rgbToHsl(r, g, b);
            if (l > 0.7) {
                menu.find('>ul>li>a').css('text-shadow', '0 1px 1px rgba(0, 0, 0, .35)');
                menu.find('>ul>li>a>span').css('border-color', 'rgba(0, 0, 0, .35)');
            }
            else {
                menu.find('>ul>li>a').css('text-shadow', '0 1px 0 rgba(255, 255, 255, .35)');
                menu.find('>ul>li>a>span').css('border-color', 'rgba(255, 255, 255, .35)');
            }
        })();

        function rgbToHsl(r, g, b) {
            r /= 255;
            g /= 255;
            b /= 255;
            var max = Math.max(r, g, b), min = Math.min(r, g, b);
            return (max + min) / 2;
        }

    });
})(jQuery);
