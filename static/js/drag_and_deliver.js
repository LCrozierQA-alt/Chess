$(document).ready(() => {
    var legalist = $('#legalist').text().split(',\n    \n        ');


    $('.chessblock').on('mousedown', () => {
        var piece_id = event.target.id;
        $('.chessblock').each(function() {
            if (legalist.includes(piece_id.substring(0,2) + $(this).attr("id").substring(2))){
                $(this).css("backgroundColor","#008000")
                $(this).droppable({
                    drop: function(event, ui){
                        var data = piece_id.substring(0,2) + event.target.id.substring(2);
                        console.log(data)
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