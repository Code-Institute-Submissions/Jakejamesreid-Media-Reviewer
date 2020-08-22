$(function() {

    $(".progress").each(function() {

        var value = $(this).attr('data-value');
        var left = $(this).find('.progress-left .progress-bar');
        var right = $(this).find('.progress-right .progress-bar');

        if (value > 0) {

            // Determine fill if progress bar
            if (value <= 50) {
                right.css('transform', 'rotate(' + percentageToDegrees(value) + 'deg)');
            } 
            else {
                right.css('transform', 'rotate(180deg)');
                left.css('transform', 'rotate(' + percentageToDegrees(value - 50) + 'deg)');
            }

            // Add border colours based on value
            switch(true) {
                case (value >= 70):
                    right.addClass('green-border')
                    left.addClass('green-border')
                    break;
                case (value < 70 && value >=40):
                    right.addClass('orange-border')
                    left.addClass('orange-border')
                    break;
                case (value < 40):
                    left.addClass('red-border')
                    break;
              }
        }
    })

    function percentageToDegrees(percentage) {
        // Convert rating value to degrees
        return percentage / 100 * 360

    }

});