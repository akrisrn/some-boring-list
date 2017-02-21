$(function () {
  $(".tag").each(function () {
    Math.seed = parseInt(encodeURIComponent($(this).text().replace(/[a-z|A-Z]/g, function ($1) {
        return $1.charCodeAt(0);
      })).replace(/%/g, ''), 16) / 8;
    $(this).css("background", function () {
      return '#' + (function (color) {
          return (color += '0123456789abcdef' [Math.floor(function (min, max) {
              max = max || 1;
              min = min || 0;
              Math.seed = (Math.seed * 9301 + 49297) % 233280;
              var rnd = Math.seed / 233280.0;
              return min + rnd * (max - min);
            }() * 16)])
          && (color.length == 6) ? color : arguments.callee(color);
        })('');
    })
  });
});