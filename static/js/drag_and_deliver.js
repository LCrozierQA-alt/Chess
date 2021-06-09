$(document).ready(() => {
    var legalist = $('#legalist').text().trimLeft("").split(',\n    \n        ');
    legalist[legalist.length - 1] = legalist[legalist.length - 1].substring(0,4);

    $('.chessblock').on('mousedown', () => {
        var piece_id = event.target.id;
        $('.chessblock').each(function() {
            if (legalist.includes(piece_id.substring(0,2) + $(this).attr("id").substring(2))){
                $(this).css("backgroundColor","#008000")
                $(this).droppable({
                    disabled: false,
                    drop: function(event, ui){
                        var data = piece_id.substring(0,2) + event.target.id.substring(2);
                        $.ajax({
                            url: '/shiss',
                            type: 'POST',
                            data: data,
                            success: function(response){
                                location.reload();
                                console.log(response);
                            },
                            error: function(error){
                                console.log(error);
                            }
                        })
                    }
                })
            }
            else{
                $(this).droppable({
                    disabled: true
                  });
            }
        })
    })
    $(document).on('mouseup', () => {
        $('.chessblock').each(function() {
            $(this).css("backgroundColor","#ffffff")
        })
})
    
    $('.chessblock').draggable({
        revert: true
    })
            
});